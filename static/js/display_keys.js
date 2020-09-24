/// listens to keys on keyboard
//


window.addEventListener("keydown", function(event) {
  lang = "en";
  lang = "fr";
  var key = event.key;
  var code = event.keyCode;
  answer = document.getElementById("answer").innerHTML;
  console.log(82,key, code);
  if (answer==="???") {
    document.getElementById("answer").innerHTML="";
  }
  console.log("81");
  if (key==127) {
    if (str.length >0) {
      str = str.substring(0, str.length - 1);
      }
  }
  else if (key==="Backspace") {
    console.log("Backspace");
    if (answer.length >0) {
      document.getElementById("answer").innerHTML = answer.substring(0, answer.length - 1);
      }
  }
  else if (key=="Enter"){
    // here if we validate the answer
    console.log("Validating");
    validate_answer();
    /*
	  q_index = $("div").data("card");
    q_answer = $("div").data("deck")[q_index].answer;
    console.log("132",answer, q_answer, answer===q_answer);
    if (answer===q_answer) 
    {
      //right answer
      q_index = parseInt(q_index);
      if (q_index< $("div").data("deck").length-1) {
        q_index+=1;
        $("div").data("card", q_index);
        document.getElementById("question").innerHTML = $("div").data("deck")[q_index].question;
        document.getElementById("answer").innerHTML = "???";
        document.getElementById("timer").innerHTML = "15";
        document.getElementById("status").innerHTML += '<div class="tick">✔</div>';
      };

      if (lang==="fr") {
        var speech = new SpeechSynthesisUtterance('bravo');
        speech.lang = 'fr-FR';
        window.speechSynthesis.speak(speech);
      }
      else if (lang == "en") {
        var speech = new SpeechSynthesisUtterance('good');
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);
      }

    }
    else 
    {
      //wrong answer reset what is written
      console.log("140");
      document.getElementById("answer").innerHTML = "";
      document.getElementById("status").innerHTML += '<div class="cross">x</div>';
      if (lang==="fr") {
        var speech = new SpeechSynthesisUtterance('essaye encore');
        speech.lang = 'fr-FR';
        window.speechSynthesis.speak(speech);
      }
      else if (lang == "en") {
        var speech = new SpeechSynthesisUtterance('no way');
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);
      }
    
  }*/
  }
  else {  
    //here if we append a character to the answer
    if ((code>=48)&&(code<91)) {
    console.log("90",key);
    console.log("99",String.fromCharCode(key));
    document.getElementById("answer").innerHTML += key;
    }
  }
});

function validate_answer_remove() {
  // code to be executed
  answer = document.getElementById("answer").innerHTML;
  console.log("mcv validating");
  lang = "fr";
// here if we validate the answer
    console.log("Validating");
    q_index = $("div").data("card");
    q_answer = $("div").data("deck")[q_index].answer;
    console.log("94 new",answer, q_answer, answer===q_answer);
    if (answer===q_answer)
    {
      //right answer
      q_index = parseInt(q_index);
      if (q_index< $("div").data("deck").length-1) {
        q_index+=1;
        $("div").data("card", q_index);
        document.getElementById("question").innerHTML = $("div").data("deck")[q_index].question;
        document.getElementById("answer").innerHTML = "???";
        document.getElementById("timer").innerHTML = "15";
        document.getElementById("status").innerHTML += '<div class="tick">✔</div>';
      };

      if (lang==="fr") {
        var speech = new SpeechSynthesisUtterance('bravo');
        speech.lang = 'fr-FR';
        window.speechSynthesis.speak(speech);
      }
      else if (lang == "en") {
        var speech = new SpeechSynthesisUtterance('good');
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);
      }

    }
    else
    {
      //wrong answer reset what is written
      console.log("140");
      document.getElementById("answer").innerHTML = "";
      document.getElementById("status").innerHTML += '<div class="cross">x</div>';
      if (lang==="fr") {
        var speech = new SpeechSynthesisUtterance('essaye encore');
        speech.lang = 'fr-FR';
        window.speechSynthesis.speak(speech);
      }
      else if (lang == "en") {
        var speech = new SpeechSynthesisUtterance('no way');
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);
      }
    }

}
