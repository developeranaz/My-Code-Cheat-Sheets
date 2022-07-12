//creating a function as sleep to call sleep in milliseconds

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
// simple count 
var x = 1;
while (true) {
    //your code
//var x = 0;
var x = x * 2;
console.log(x);
sleep(10);
if (x >= 500000) { break; }
}
