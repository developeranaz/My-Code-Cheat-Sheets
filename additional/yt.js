addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request));
});

const parseQueryString = queryString =>
  Object.assign(
    {},
    ...queryString.split("&").map(kvp => {
      kva = kvp.split("=").map(decodeURIComponent);
      return {
        [kva[0]]: kva[1]
      };
    })
  );

const getJsPlayer = async videoPage => {
  let playerURL = JSON.parse(
    /"assets":.+?"js":\s*("[^"]+")/gm.exec(videoPage)[1]
  );
  if (playerURL.startsWith("//")) playerURL = "https:" + playerURL;
  else if (!playerURL.startsWith("http"))
    playerURL = "https://www.youtube.com" + playerURL;

  const jsPlayerFetch = await fetch(playerURL);
  const jsPlayer = await jsPlayerFetch.text();
  return jsPlayer;
};

async function handleRequest(request) {
  try {
    const query = parseQueryString(request.url.split("?")[1]);
    console.log("Parsed query", query);

    const videoId = query["v"];
    const videoPageReq = await fetch(
      `https://www.youtube.com/watch?v=${encodeURIComponent(
        videoId
      )}&gl=US&hl=en&has_verified=1&bpctr=9999999999`
    );
    const videoPage = await videoPageReq.text();

    const playerConfigRegex = /;ytplayer\.config\s*=\s*({.+?});ytplayer|;ytplayer\.config\s*=\s*({.+?});/gm;
    const playerConfig = JSON.parse(playerConfigRegex.exec(videoPage)[1]);
    const playerResponse = JSON.parse(playerConfig.args.player_response);
    const jsPlayer = await getJsPlayer(videoPage);
    const formatURLs = playerResponse.streamingData.adaptiveFormats.map(
      format => {
        let url = format.url;
        const cipher = format.signatureCipher || format.cipher;
        if (!!cipher) {
          const components = parseQueryString(cipher);

          const sig = applyActions(extractActions(jsPlayer), components.s);
          url =
            components["url"] +
            `&${encodeURIComponent(components.sp)}=${encodeURIComponent(sig)}`;
        }

        return {
          ...format,
          _decryptedURL: url
        };
      }
    );

    if ("f" in query) {
      const format = formatURLs.find(
        format => format.itag === parseInt(query.f)
      );
      const stream = await fetch(format._decryptedURL);
      const { readable, writable } = new TransformStream();
      stream.body.pipeTo(writable);
      return new Response(readable, stream);
    } else {
      return new Response(
        JSON.stringify(
          formatURLs.map(({ _decryptedURL, ...format }) => format),
          null,
          2
        ),
        {
          status: 200,
          headers: {
            "Content-Type": "application/json"
          }
        }
      );
    }

    return new Response(`hello world, ${JSON.stringify(query)}`, {
      status: 200
    });
  } catch (ex) {
    return new Response(
      JSON.stringify({ ok: false, message: ex.toString(), payload: ex.trace }),
      { status: 500 }
    );
  }
}


const jsVarStr = "[a-zA-Z_\\$][a-zA-Z_0-9]*";
const jsSingleQuoteStr = `'[^'\\\\]*(:?\\\\[\\s\\S][^'\\\\]*)*'`;
const jsDoubleQuoteStr = `"[^"\\\\]*(:?\\\\[\\s\\S][^"\\\\]*)*"`;
const jsQuoteStr = `(?:${jsSingleQuoteStr}|${jsDoubleQuoteStr})`;
const jsKeyStr = `(?:${jsVarStr}|${jsQuoteStr})`;
const jsPropStr = `(?:\\.${jsVarStr}|\\[${jsQuoteStr}\\])`;
const jsEmptyStr = `(?:''|"")`;
const reverseStr =
  ":function\\(a\\)\\{" + "(?:return )?a\\.reverse\\(\\)" + "\\}";
const sliceStr = ":function\\(a,b\\)\\{" + "return a\\.slice\\(b\\)" + "\\}";
const spliceStr = ":function\\(a,b\\)\\{" + "a\\.splice\\(0,b\\)" + "\\}";
const swapStr =
  ":function\\(a,b\\)\\{" +
  "var c=a\\[0\\];a\\[0\\]=a\\[b(?:%a\\.length)?\\];a\\[b(?:%a\\.length)?\\]=c(?:;return a)?" +
  "\\}";
const actionsObjRegexp = new RegExp(
  `var (${jsVarStr})=\\{((?:(?:${jsKeyStr}${reverseStr}|${jsKeyStr}${sliceStr}|${jsKeyStr}${spliceStr}|${jsKeyStr}${swapStr}),?\\r?\\n?)+)\\};`
);
const actionsFuncRegexp = new RegExp(
  `${`function(?: ${jsVarStr})?\\(a\\)\\{` +
    `a=a\\.split\\(${jsEmptyStr}\\);\\s*` +
    `((?:(?:a=)?${jsVarStr}`}${jsPropStr}\\(a,\\d+\\);)+)` +
    `return a\\.join\\(${jsEmptyStr}\\)` +
    `\\}`
);
const reverseRegexp = new RegExp(`(?:^|,)(${jsKeyStr})${reverseStr}`, "m");
const sliceRegexp = new RegExp(`(?:^|,)(${jsKeyStr})${sliceStr}`, "m");
const spliceRegexp = new RegExp(`(?:^|,)(${jsKeyStr})${spliceStr}`, "m");
const swapRegexp = new RegExp(`(?:^|,)(${jsKeyStr})${swapStr}`, "m");

const swapHeadAndPosition = (arr, position) => {
  const first = arr[0];
  arr[0] = arr[position % arr.length];
  arr[position] = first;
  return arr;
};

const extractActions = body => {
  const objResult = actionsObjRegexp.exec(body);
  const funcResult = actionsFuncRegexp.exec(body);
  if (!objResult || !funcResult) {
    return null;
  }

  const obj = objResult[1].replace(/\$/g, "\\$");
  const objBody = objResult[2].replace(/\$/g, "\\$");
  const funcBody = funcResult[1].replace(/\$/g, "\\$");

  let result = reverseRegexp.exec(objBody);
  const reverseKey =
    result && result[1].replace(/\$/g, "\\$").replace(/\$|^'|^"|'$|"$/g, "");
  result = sliceRegexp.exec(objBody);
  const sliceKey =
    result && result[1].replace(/\$/g, "\\$").replace(/\$|^'|^"|'$|"$/g, "");
  result = spliceRegexp.exec(objBody);
  const spliceKey =
    result && result[1].replace(/\$/g, "\\$").replace(/\$|^'|^"|'$|"$/g, "");
  result = swapRegexp.exec(objBody);
  const swapKey =
    result && result[1].replace(/\$/g, "\\$").replace(/\$|^'|^"|'$|"$/g, "");

  const keys = `(${[reverseKey, sliceKey, spliceKey, swapKey].join("|")})`;
  const myreg =
    `(?:a=)?${obj}(?:\\.${keys}|\\['${keys}'\\]|\\["${keys}"\\])` +
    `\\(a,(\\d+)\\)`;
  const tokenizeRegexp = new RegExp(myreg, "g");
  const tokens = [];
  while ((result = tokenizeRegexp.exec(funcBody)) !== null) {
    let key = result[1] || result[2] || result[3];
    switch (key) {
      case swapKey:
        tokens.push(`w${result[4]}`);
        break;
      case reverseKey:
        tokens.push("r");
        break;
      case sliceKey:
        tokens.push(`s${result[4]}`);
        break;
      case spliceKey:
        tokens.push(`p${result[4]}`);
        break;
    }
  }
  return tokens;
};

const applyActions = (tokens, _sig) => {
  let sig = _sig.split("");
  for (let i = 0, len = tokens.length; i < len; i++) {
    let token = tokens[i],
      pos;
    switch (token[0]) {
      case "r":
        sig = sig.reverse();
        break;
      case "w":
        pos = ~~token.slice(1);
        sig = swapHeadAndPosition(sig, pos);
        break;
      case "s":
        pos = ~~token.slice(1);
        sig = sig.slice(pos);
        break;
      case "p":
        pos = ~~token.slice(1);
        sig.splice(0, pos);
        break;
    }
  }
  return sig.join("");
};
