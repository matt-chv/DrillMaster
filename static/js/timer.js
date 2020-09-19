
// Update the count down every 1 second
var x = setInterval(function() {

  time = parseInt(document.getElementById("timer").innerHTML);
  if (time===0){
    document.getElementById("timer").innerHTML = 15;
    document.getElementById("status").innerHTML += '<div class="cross">x</div>';
  }
  else {
    time = time -1 ;
    document.getElementById("timer").innerHTML = time;

  }
}, 1000);
