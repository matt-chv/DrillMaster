
// Update the count down every 1 second
var x = setInterval(function() {

  time = parseInt(document.getElementById("timer").innerHTML);
  session_time = parseInt(document.getElementById("session_timer").innerHTML);
  
  //update session timer
  document.getElementById("session_timer").innerHTML = session_time+1;
  
  //decrement card timer
  if (time===0){
    document.getElementById("timer").innerHTML = 15;
    //document.getElementById("status").innerHTML += '<div class="cross">x</div>';
    document.getElementById("status").innerHTML += '<div class="cross">⌛ </div>';
  }
  else {
    time = time -1 ;
    document.getElementById("timer").innerHTML = time;

  }
}, 1000);
