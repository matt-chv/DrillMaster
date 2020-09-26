/*var xmlhttp = new XMLHttpRequest();
var url = "/drillpractice/deck?id=1";

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        $("div").data("deck",myArr);
	deck = $("div").data("deck");
	qna=[];
	for (v in deck) {qna.push({"question":v,"answer":deck[v]["answer"]})}
	$("div").data("qna",qna);
        show_card();
    }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();
*/
$("div").data("answers",[]);
get_cards();

function show_cards(data) {
  console.log("show deck0",data);
  deck = data; //JSON.parse(data);
  console.log("show deck1",deck);
  qna=[];
  temp=deck;
  for (v in deck) {qna.push({"question":v,"answer":deck[v]["answer"]})}
  console.log("showdeck2",qna);
  $("div").data("qna",qna);
  qna = $("div").data("qna")
    var out = "";
    var card_index;
    card_index=0;
    $("div").data("count",0)  
    out = qna[card_index]["question"]
    $("div").data("card",card_index)
    document.getElementById("question").innerHTML = out;
}

function push_answers() {
  // here we push the answers to the server
  //list of answer
      // answer: q, timestamp, answer, ok/nok, delta_time, number_attemps
  var myurl = "/drillmaster/deck";
  console.log("pushing answers",$("div").data("answers"));
  json_str = JSON.stringify($("div").data("answers"));
  console.log("pushing json str",json_str);
  //$.post(url,json_str,function(data){show_cards(data)});
  $.ajax({
    type: "POST",
    url: myurl,
    //data: $("div").data("answers"),
    data:json_str,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){show_cards(data)},
    failure: function(errMsg) {console.log("error post:",errMsg);}    
  });
  $("div").data("answers",[]);  
//$.post(url,$("div").data("answers"));  
//$.get(url);
  //get_cards();
  //show_card();
}

function get_cards() {
  //var xmlhttp = new XMLHttpRequest();
  var myurl = "/drillmaster/deck?id=1";
  console.log("GET REQUEST",myurl);
  //$.get(url, function(data){show_cards(data)});
  $.ajax({
    type: "GET",
    url: myurl,
    //contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){show_cards(data)},
    failure: function(errMsg) {console.log("error post:",errMsg);}
  });

  /*
	xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        $("div").data("deck",myArr);
				deck = $("div").data("deck");
				qna=[];
				for (v in deck) {qna.push({"question":v,"answer":deck[v]["answer"]})}
				$("div").data("qna",qna);
        console.log(myArr);
        show_card();
    }
  };
  xmlhttp.open("GET", url, true);
  xmlhttp.send(); */ 
}

function validate_answer() {
  // code to be executed
  answer = document.getElementById("answer").innerHTML;
  question = document.getElementById("question").innerHTML;
  timer = document.getElementById("timer").innerHTML;
  timestamp = Date.now().toString();
  count = $("div").data("count").toString();
  console.log("mcv validating count",count);
  lang = "fr";
// here if we validate the answer
    console.log("Validating");
    q_index = $("div").data("card");
    q_answer = $("div").data("qna")[q_index].answer;
    console.log("94 new",answer, q_answer, answer===q_answer);
    if (answer===q_answer)
    {
      //right answer
			// answer: q, timestamp, answer, ok/nok, delta_time, number_attemps
      $("div").data("answers").push({"question":question , "answer":answer,"number_attempts":count, "timestamp": timestamp, "timer": timer});
      q_index = parseInt(q_index);
      if (q_index< $("div").data("qna").length-1) {
        q_index+=1;
        $("div").data("card", q_index);
        $("div").data("count",0);
        document.getElementById("question").innerHTML = $("div").data("qna")[q_index].question;
        document.getElementById("answer").innerHTML = "???";
        document.getElementById("timer").innerHTML = "15";
        document.getElementById("status").innerHTML += '<div class="tick">✔</div>';
      }
      else {
        //we reached end of downloaded first few cards
        //push initial results
        push_answers();
        //then get next lot of cards
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
      $("div").data("count",count+1);      
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
    }//end test if right answer

}
