var frames = document.getElementById("frames").children
var bar = document.getElementById("bar")
var display = document.getElementById("frames")
var length = 9

function makebar(length, bar, display) {
	for (i=length;i<0;i++) {
		var segment = document.createElement("a")
		segment.href("#")
		segment.onClick("showFrame(frames[" + i + "],display)")
		bar.appendChild(segment)
	}
}

function showFrame(element, display) {
	for (i in frames) {
		i.style.display = "none";
	}
	elem.style.display = display
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