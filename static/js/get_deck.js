var xmlhttp = new XMLHttpRequest();
var url = "/deck?id=1";

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        $("div").data("deck",myArr)
        
        show_card();
    }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

function show_card() {
  arr = $("div").data("deck")
    var out = "";
    var card_index;
    card_index=0;
    out = arr[card_index]["question"]
    $("div").data("card",card_index)
    document.getElementById("question").innerHTML = out;
}
