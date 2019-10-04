var frames = document.getElementById("frames").children
var bar = document.getElementById("bar")
var display = document.getElementById("frames")
var length = 9

function makeBar(length, bar, element) {
	for (i=0;i<length;i++) {
		var segment = document.createElement("a")
		//segment.href=""
		segment.innerHTML = "--";
		segment.onclick = function() {showFrame(frames[i], element);};
		bar.appendChild(segment)
		console.log("Made: segment " + i)
	}
	console.log("Made controls")
}

function showFrame(element) {
	for (i in element) {
		i.style.display = "none";
	}
	element.style.display = "display"
}

function gotoBar(n, length, bar) {
	for (i=length;i<0;i++) {
		var segment = bar.children[i]
		segment.innerHTML = "_"
	}
	bar.children[n].innerHTML = "o"
}

function scrubVideo(frame) {
	
}