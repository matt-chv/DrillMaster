let v = "0";
document.querySelector("#key_0").setAttribute('data-before', `${v}`);
v = "9";
document.querySelector("#key_9").setAttribute('data-before', `${v}`);
v = "8";
document.querySelector("#key_8").setAttribute('data-before', `${v}`);
v = "7";
document.querySelector("#key_7").setAttribute('data-before', `${v}`);
v = "6";
document.querySelector("#key_6").setAttribute('data-before', `${v}`);
v = "5";
document.querySelector("#key_5").setAttribute('data-before', `${v}`);
v = "4";
document.querySelector("#key_4").setAttribute('data-before', `${v}`);
v = "3";
document.querySelector("#key_3").setAttribute('data-before', `${v}`);
v = "2";
document.querySelector("#key_2").setAttribute('data-before', `${v}`);
v = "1";
document.querySelector("#key_1").setAttribute('data-before', `${v}`);
v = "OK";
document.querySelector("#key_ok").setAttribute('data-before', `${v}`);
v = "DEL";
document.querySelector("#key_del").setAttribute('data-before', `${v}`);

var element = document.getElementById('key_1');
element.addEventListener('click', function(){
	secretDivClick(1);}, false);

var element = document.getElementById('key_2');
		element.addEventListener('click', function(){
		secretDivClick(2);}, false);

var element = document.getElementById('key_3');
	element.addEventListener('click', function(){
		secretDivClick(3);}, false);

var element = document.getElementById('key_4');
		element.addEventListener('click', function(){
			secretDivClick(4);}, false);

var element = document.getElementById('key_5');
		element.addEventListener('click', function(){
			secretDivClick(5);}, false);

var element = document.getElementById('key_6');
		element.addEventListener('click', function(){
			secretDivClick(6);}, false);

var element = document.getElementById('key_7');
		element.addEventListener('click', function(){
			secretDivClick(7);}, false);

var element = document.getElementById('key_8');
		element.addEventListener('click', function(){
			secretDivClick(8);}, false);

var element = document.getElementById('key_9');
		element.addEventListener('click', function(){
			secretDivClick(9);}, false);

var element = document.getElementById('key_0');
		element.addEventListener('click', function(){
			secretDivClick(0);}, false);

var element = document.getElementById('key_ok');
		element.addEventListener('click', function(){
			secretDivClick("ok");}, false);

var element = document.getElementById('key_del');
		element.addEventListener('click', function(){
			secretDivClick("del");}, false);

function secretDivClick(key) {
	console.log('clicked',key);
	prev=$( "div[id|='answer']").html();
	if (key==="del") {
		if (prev.length>0) {
			prev = prev.substring(0,prev.length-1)
		};
		if (prev=="???") {
			$( "div[id|='answer']").html("")
		}
		else {
			$( "div[id|='answer']").html(prev)
		}
	}
	else if (key==="ok"){
		validate_answer();
		$( "div[id|='answer']").html("")
	}
	else {
		if (prev=="???"){
			prev="";
		}
		$( "div[id|='answer']").html(prev+key)
	}	
}
