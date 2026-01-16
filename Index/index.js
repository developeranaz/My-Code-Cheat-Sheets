/**
 * Cloudflare Worker - Enhanced Video Proxy
 * Clean URL structure with API integration
 */

const VIDOZA_API_KEY = '0nwjvf3jzf9zeo1xppukkvkc4dqrxxxzda86exvsiwkzxoy'
const VIDOZA_BASE_URL = 'https://videzz.net'

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const path = url.pathname
  
  // Root: File listing from Vidoza API
  if (path === '/') {
    return await handleFileListing()
  }
  
  // /url: Video proxy UI
  if (path === '/url') {
    return new Response(getProxyUI(), {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    })
  }
  
  // /download?id=VIDEO_ID: Clean download/stream URL
  if (path === '/download') {
    const videoId = url.searchParams.get('id')
    if (!videoId) {
      return new Response('Missing video ID', { status: 400 })
    }
    
    const pageUrl = `${VIDOZA_BASE_URL}/${videoId}.html`
    
    try {
      return await proxyVideo(pageUrl, request, true)
    } catch (error) {
      console.error('Proxy error:', error)
      return new Response(`Error: ${error.message}`, { 
        status: error.status || 500,
        headers: { 'Content-Type': 'text/plain' }
      })
    }
  }
  
  // /stream?id=VIDEO_ID: Stream in browser (no download prompt)
  if (path === '/stream') {
    const videoId = url.searchParams.get('id')
    if (!videoId) {
      return new Response('Missing video ID', { status: 400 })
    }
    
    const pageUrl = `${VIDOZA_BASE_URL}/${videoId}.html`
    
    try {
      return await proxyVideo(pageUrl, request, false)
    } catch (error) {
      console.error('Proxy error:', error)
      return new Response(`Error: ${error.message}`, { 
        status: error.status || 500,
        headers: { 'Content-Type': 'text/plain' }
      })
    }
  }
  
  // Legacy /proxy endpoint for compatibility
  if (path === '/proxy') {
    const videoUrl = url.searchParams.get('url')
    if (!videoUrl) {
      return new Response('Missing video URL', { status: 400 })
    }
    
    try {
      return await proxyVideo(videoUrl, request, false)
    } catch (error) {
      console.error('Proxy error:', error)
      return new Response(`Error: ${error.message}`, { 
        status: error.status || 500,
        headers: { 'Content-Type': 'text/plain' }
      })
    }
  }
  
  return new Response('Not Found', { status: 404 })
}

/**
 * Fetch and display file listing from Vidoza API
 */
async function handleFileListing() {
  try {
    const response = await fetch('https://api.vidoza.net/v1/files', {
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${VIDOZA_API_KEY}`,
        'cache-control': 'no-cache'
      }
    })
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    
    const data = await response.json()
    return new Response(generateFileListingHTML(data), {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    })
    
  } catch (error) {
    return new Response(generateErrorHTML(error.message), {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' },
      status: 500
    })
  }
}

/**
 * Generate simple HTTP index-style listing
 */
function generateFileListingHTML(apiData) {
  const files = apiData.data || []
  const total = apiData.meta?.total || 0
  
      const fileRows = files.map(file => {
    const downloadUrl = `/download?id=${file.id}`
    const streamUrl = `/stream?id=${file.id}`
    const size = formatBytes(file.size)
    const date = file.created.split(' ')[0]
    
    return `<tr>
      <td><a href="${streamUrl}">${file.name}</a></td>
      <td>${size}</td>
      <td>${date}</td>
      <td>${file.views_paid || 0}</td>
      <td><a href="${downloadUrl}" download>Download</a></td>
    </tr>`
  }).join('')
  
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Index of /</title>
<style>
body{font-family:monospace;margin:20px;background:#fff;color:#000}
h1{font-size:18px;border-bottom:1px solid #ccc;padding-bottom:5px}
table{width:100%;border-collapse:collapse;margin-top:10px}
th{text-align:left;padding:8px;border-bottom:2px solid #000;font-weight:bold}
td{padding:8px;border-bottom:1px solid #ddd}
a{color:#0000ee;text-decoration:none}
a:hover{text-decoration:underline}
a:visited{color:#551a8b}
.info{margin:10px 0;color:#666;font-size:13px}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #ccc;color:#666;font-size:12px}
</style>
</head>
<body>
<h1>Index of /</h1>
<div class="info">Total files: ${total}</div>
<table>
<tr>
<th>Name</th>
<th>Size</th>
<th>Date</th>
<th>Views</th>
<th>Action</th>
</tr>
${fileRows}
</table>
<div class="footer">
<a href="/url">Upload/Proxy Interface</a> | Powered by Cloudflare Workers
</div>
</body>
</html>`
}

/**
 * Generate error page
 */
function generateErrorHTML(errorMsg) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Error</title>
<style>
body{font-family:monospace;margin:20px;background:#fff;color:#000}
h1{color:#c00}
</style>
</head>
<body>
<h1>Error</h1>
<p>${errorMsg}</p>
<p><a href="/">Back to index</a></p>
</body>
</html>`
}

/**
 * Format bytes to human readable
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Main proxy function with enhanced request handling
 */
async function proxyVideo(pageUrl, clientRequest, forceDownload = false) {
  // Step 1: Fetch HTML page to activate IP
  const pageResponse = await fetch(pageUrl, {
    headers: buildPageHeaders(pageUrl),
    cf: {
      cacheTtl: 0,
      cacheEverything: false
    }
  })
  
  if (!pageResponse.ok) {
    const error = new Error(`Failed to fetch page: ${pageResponse.status}`)
    error.status = pageResponse.status
    throw error
  }
  
  const html = await pageResponse.text()
  
  // Step 2: Extract video URL
  const videoUrl = extractVideoUrl(html, pageUrl)
  
  if (!videoUrl) {
    throw new Error('Could not extract video URL from page')
  }
  
  // Small delay to ensure IP registration (100ms)
  await new Promise(resolve => setTimeout(resolve, 100))
  
  // Step 3: Fetch video with same IP and proper headers
  const rangeHeader = clientRequest.headers.get('range')
  const videoHeaders = buildVideoHeaders(pageUrl, rangeHeader)
  
  const videoResponse = await fetch(videoUrl, {
    headers: videoHeaders,
    cf: {
      cacheTtl: 3600,
      cacheEverything: true
    }
  })
  
  if (!videoResponse.ok) {
    const error = new Error(`Failed to fetch video: ${videoResponse.status}`)
    error.status = videoResponse.status
    throw error
  }
  
  // Step 4: Stream response with proper headers
  return buildProxyResponse(videoResponse, videoUrl, forceDownload, rangeHeader)
}

/**
 * Build headers for page request
 */
function buildPageHeaders(pageUrl) {
  const headers = new Headers()
  headers.set('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
  headers.set('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
  headers.set('Accept-Language', 'en-US,en;q=0.9')
  headers.set('Accept-Encoding', 'gzip, deflate, br')
  headers.set('DNT', '1')
  headers.set('Connection', 'keep-alive')
  headers.set('Upgrade-Insecure-Requests', '1')
  headers.set('Sec-Fetch-Dest', 'document')
  headers.set('Sec-Fetch-Mode', 'navigate')
  headers.set('Sec-Fetch-Site', 'none')
  headers.set('Cache-Control', 'max-age=0')
  
  return headers
}

/**
 * Build headers for video request (must match browser behavior)
 */
function buildVideoHeaders(refererUrl, rangeHeader) {
  const headers = new Headers()
  headers.set('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
  headers.set('Accept', 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5')
  headers.set('Accept-Language', 'en-US,en;q=0.9')
  headers.set('Accept-Encoding', 'identity')
  headers.set('Referer', refererUrl)
  headers.set('Origin', new URL(refererUrl).origin)
  headers.set('DNT', '1')
  headers.set('Connection', 'keep-alive')
  headers.set('Sec-Fetch-Dest', 'video')
  headers.set('Sec-Fetch-Mode', 'no-cors')
  headers.set('Sec-Fetch-Site', 'same-origin')
  
  // Handle range requests properly
  if (rangeHeader) {
    headers.set('Range', rangeHeader)
  } else {
    // Request in chunks to avoid overwhelming the worker
    headers.set('Range', 'bytes=0-')
  }
  
  return headers
}

/**
 * Build proxy response with proper streaming headers
 */
function buildProxyResponse(videoResponse, videoUrl, forceDownload = false, rangeHeader = null) {
  const headers = new Headers()
  
  // Content type
  const contentType = videoResponse.headers.get('Content-Type') || 'video/mp4'
  headers.set('Content-Type', contentType)
  
  // Content length
  const contentLength = videoResponse.headers.get('Content-Length')
  if (contentLength) {
    headers.set('Content-Length', contentLength)
  }
  
  // Range support - CRITICAL for download managers and pause/resume
  headers.set('Accept-Ranges', 'bytes')
  
  const contentRange = videoResponse.headers.get('Content-Range')
  if (contentRange) {
    headers.set('Content-Range', contentRange)
  }
  
  // CORS headers - essential for browser compatibility
  headers.set('Access-Control-Allow-Origin', '*')
  headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
  headers.set('Access-Control-Allow-Headers', 'Range, Content-Type')
  headers.set('Access-Control-Expose-Headers', 'Content-Length, Content-Range, Accept-Ranges, Content-Disposition')
  
  // Cache control - balance between speed and freshness
  headers.set('Cache-Control', 'public, max-age=86400, immutable')
  
  // ETag support for better caching and resume capability
  const etag = videoResponse.headers.get('ETag')
  if (etag) {
    headers.set('ETag', etag)
  }
  
  // Last-Modified for conditional requests
  const lastModified = videoResponse.headers.get('Last-Modified')
  if (lastModified) {
    headers.set('Last-Modified', lastModified)
  }
  
  // Content disposition - CRITICAL for forcing download
  const filename = extractFilename(videoUrl)
  if (forceDownload) {
    // Force download with attachment
    headers.set('Content-Disposition', `attachment; filename="${filename}"`)
  } else {
    // Allow inline viewing
    headers.set('Content-Disposition', `inline; filename="${filename}"`)
  }
  
  // X-Content-Type-Options - security header
  headers.set('X-Content-Type-Options', 'nosniff')
  
  // Add custom header to indicate this is a proxied request
  headers.set('X-Proxy-Cache', rangeHeader ? 'PARTIAL' : 'FULL')
  
  // Determine status code based on range request
  let status = videoResponse.status
  if (rangeHeader && contentRange) {
    status = 206 // Partial Content
  } else if (rangeHeader && !contentRange) {
    // Server doesn't support ranges, return full content
    status = 200
  }
  
  return new Response(videoResponse.body, {
    status: status,
    statusText: status === 206 ? 'Partial Content' : videoResponse.statusText,
    headers: headers
  })
}

/**
 * Extract video URL with multiple fallback methods
 */
function extractVideoUrl(html, baseUrl) {
  // Method 1: Video tag with src
  let match = html.match(/<video[^>]+src=["']([^"']+)["']/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  // Method 2: Source tag with video/mp4
  match = html.match(/<source[^>]+src=["']([^"']+)["'][^>]*type=["']video\/mp4["']/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  // Method 3: Any source tag
  match = html.match(/<source[^>]+src=["']([^"']+)["']/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  // Method 4: JavaScript file variable
  match = html.match(/file:\s*["']([^"']+\.mp4[^"']*)["']/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  // Method 5: sources array
  match = html.match(/sources:\s*\[["']([^"']+\.mp4[^"']*)["']/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  // Method 6: Direct .mp4 URL
  match = html.match(/https?:\/\/[^\s"'<>]+\.mp4[^\s"'<>]*/i)
  if (match) return match[0]
  
  // Method 7: Look for common video hosting patterns
  match = html.match(/(?:src|file|url)["':\s]+["']([^"']+\.(?:mp4|m3u8)[^"']*)/i)
  if (match) return resolveUrl(match[1], baseUrl)
  
  return null
}

/**
 * Resolve relative URLs
 */
function resolveUrl(url, baseUrl) {
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  
  const base = new URL(baseUrl)
  
  if (url.startsWith('//')) {
    return base.protocol + url
  }
  
  if (url.startsWith('/')) {
    return base.origin + url
  }
  
  return new URL(url, baseUrl).href
}

/**
 * Extract filename from URL
 */
function extractFilename(url) {
  try {
    const pathname = new URL(url).pathname
    const filename = pathname.split('/').pop()
    return filename || 'video.mp4'
  } catch {
    return 'video.mp4'
  }
}

/**
 * Proxy UI at /url
 */
function getProxyUI() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Video Proxy</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#1a1a2e;color:#eee;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.container{background:#16213e;border-radius:12px;padding:30px;max-width:700px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.4)}
h1{font-size:24px;margin-bottom:20px;color:#0f3460}
input{width:100%;padding:12px;border:2px solid #0f3460;border-radius:6px;font-size:14px;background:#1a1a2e;color:#eee;margin-bottom:12px}
input:focus{outline:none;border-color:#e94560}
.btn{width:100%;padding:14px;border:none;border-radius:6px;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:8px;transition:.3s}
.btn-primary{background:#e94560;color:#fff}
.btn-primary:hover{background:#d63850}
.btn-secondary{background:#0f3460;color:#fff}
.btn-secondary:hover{background:#1a4d7a}
.status{padding:10px;border-radius:6px;margin:12px 0;display:none;font-size:14px}
.status.show{display:block}
.info{background:#1e3a5f;color:#64b5f6}
.success{background:#1b5e20;color:#81c784}
.error{background:#b71c1c;color:#e57373}
#videoContainer{display:none;margin-top:20px}
video{width:100%;border-radius:8px;background:#000}
.hint{font-size:12px;color:#888;margin-top:16px;line-height:1.6}
.link{margin-top:10px}
.link a{color:#64b5f6;font-size:12px}
</style>
</head>
<body>
<div class="container">
<h1>🎬 Video Proxy</h1>
<input type="text" id="url" placeholder="Enter video page URL" value="https://videzz.net/7cm0l7oo8t6q.html">
<button class="btn btn-primary" onclick="stream()">Stream Video</button>
<button class="btn btn-secondary" onclick="download()">Force Download</button>
<div id="status" class="status"></div>
<div id="videoContainer">
<video id="player" controls preload="metadata"></video>
</div>
<div class="hint">Worker fetches HTML → Extracts video URL → Streams through Cloudflare<br>Download supports pause/resume in browsers and download managers</div>
<div class="link"><a href="/">← Back to file listing</a></div>
</div>
<script>
const status=document.getElementById('status'),player=document.getElementById('player'),container=document.getElementById('videoContainer');
function show(msg,type){status.textContent=msg;status.className='status show '+type}
function proxy(url){
const match=url.match(/\\/([a-z0-9]+)\\.html$/i);
if(match)return'/download?id='+match[1];
return'/proxy?url='+encodeURIComponent(url);
}
async function stream(){
const url=document.getElementById('url').value.trim();
if(!url)return show('Enter a URL','error');
show('Loading...','info');
const p=proxy(url);
try{
const r=await fetch(p,{method:'HEAD'});
if(!r.ok)throw new Error('Failed: '+r.status);
player.src=p;
container.style.display='block';
show('✓ Ready','success');
player.play().catch(()=>{});
}catch(e){
show('Error: '+e.message,'error');
container.style.display='none';
}
}
function download(){
const url=document.getElementById('url').value.trim();
if(!url)return show('Enter a URL','error');
show('Starting download...','info');
const a=document.createElement('a');
a.href=proxy(url);
a.download='video.mp4';
a.click();
setTimeout(()=>show('Download started','success'),500);
}
</script>
</body>
</html>`
}
