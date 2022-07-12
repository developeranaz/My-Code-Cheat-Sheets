//creating a function as sleep to call sleep in milliseconds

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

// simple count app 

// set initial value x as 1
var x = 1;

// starting while loop
while (true) {

// put previous value of x multiplied by 2
var x = x * 2;

// printing value of x
console.log(x);

// sleep function to sleep 10 second 
sleep(10);

// if condition - if x greater than or equal to 500000, end the loop
if (x >= 500000) { break; }
}
