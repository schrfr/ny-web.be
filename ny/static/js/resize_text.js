//
//     JQuery Text resize + Cookie recall
//     Adapted for nY
//     by Jonny Kamaly
//     based on scripts written by Jonny Kamaly andFaisal &amp; Homar
//     http://www.shopdev.co.uk/blog/text-resizing-with-jquery/#comment-1044
 
 
var sitefunctions = {
	textresize : function(){
		// show text resizing links
		$(".FontSize").show();
		var $cookie_name = "sitename-FontSize";
		var originalFontSize = $("html").css("font-size");
		// if exists load saved value, otherwise store it
		if($.cookie($cookie_name)) {
			var $getSize = $.cookie($cookie_name);
			$("html").css({fontSize : $getSize + ($getSize.indexOf("px")!=-1 ? "" : "px")}); // IE fix for double "pxpx" error
		} else {
			$.cookie($cookie_name, originalFontSize);
		}
		// reset link
		$(".FontSizeReset").bind("click", function() {
			$("html").css("font-size", originalFontSize);
			$.cookie($cookie_name, originalFontSize);
		});
		// text "+" link
		$(".FontSizeInc").bind("click", function() {
			var currentFontSize = $("html").css("font-size");
			var currentFontSizeNum = parseFloat(currentFontSize, 10);
			var newFontSize = currentFontSizeNum*1.2;
			if (newFontSize  11) {
				$("html").css("font-size", newFontSize);
				$.cookie($cookie_name, newFontSize);
			}
			return false;	
		});
	}
}
 
$(document).ready(function(){
		sitefunctions.textresize();	
})