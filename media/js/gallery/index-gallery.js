
function gallery_init() {
	$('#galerija-thumbnails').galleria({
        history   : true, // deactivates the history object for bookmarking, back-button etc.
        clickNext : false, // helper for making the image clickable. Let's not have that in this example.
        insert    : ".galerija-content", // the containing selector for our main image. 
                                // If not found or undefined (like here), galleria will create a container 
                                // before the ul with the class .galleria_container (see CSS)
        //onImage   : function() { $('.nav').css('display','block'); } // shows the nav when the image is showing
        onImage   : function(image,caption,thumb) { // let's add some image effects for demonstration purposes
        	console.log("on image   ---  ", image, caption, thumb);
            // fade in the image & caption
            if(! ($.browser.mozilla && navigator.appVersion.indexOf("Win")!=-1) ) { // FF/Win fades large images terribly slow
                image.css('display','none').fadeIn(1000);
            }
            caption.css('display','none').fadeIn(1000);
           
            // fetch the thumbnail container
            var _li = thumb.parent('li');
           
            // fade out inactive thumbnail
            _li.siblings().children('img.selected').fadeTo(500,0.3);
           
            // fade in active thumbnail
            thumb.fadeTo('fast',1).addClass('selected');
           
            // add a title for the clickable image
            image.attr('title','Next image >>');
        },
        onThumb : function(thumb) { // thumbnail effects goes here
			console.log("clicked thumb 1", thumb);
            // fetch the thumbnail container
            var _li = thumb.parent('li');
           
            // if thumbnail is active, fade all the way.
            var _fadeTo = _li.is('.active') ? '1' : '0.3';
           
            // fade in the thumbnail when finnished loading
            thumb.css({display:'none',opacity:_fadeTo}).fadeIn(1500);
           
            // hover effects
            thumb.hover(
                function() { thumb.fadeTo('fast',1); },
                function() { _li.not('.active').children('img').fadeTo('fast',0.3); } // don't fade out if the parent is active
            );

            thumb.click(function() { 
				console.log("clicked thumb 2", thumb);
				url = thumb.attr("src");
				//new_url = url.replace(/(.*)\/cache(.*)_[^.]*(\..*)/, '$1$2$3');
				//$("#full_size").attr("href", new_url);


                    /*hackery i'm not particually proud of
                    example input:
                    /img/wireframes/cache/cp-wire-kiberpipin-blog02_normal.png
                    example output:
                    /img/wireframes/cp-wire-kiberpipin-blog02.png */

                    //alert("#" + thumb.attr("src"));
                    //alert($("#" + thumb.attr("src") + " " + "#exif").text());
                    //alert("#" + thumb.attr("class"));
                    //alert($("#"+thumb.attr("src")));
                    //alert($('#' + thumb.attr("class").slice(' ')[0]).html());
                    //$("#"+thumb.attr("src")).hide();
			});
		}
	});
}

$(function(){
	gallery_init();
	console.log("konec z dodajanjem galerije");
});

function recurse(me) {    
	if ($("#gallery"+me).length){
		var classes = $("#gallery"+me).attr("class").split(' ');
		var num = "";
	    for (i=0; i < classes.length; i++) {
	        if (classes[i] > "parent") {
	            num = classes[i].slice(6); 
	            if (num !== 0) {
	                $("#gallery"+num).show();
	                return num;
	            }
	        }
	    }
	}

    return -1;
}
function menuToggle(me) {
	console.log("we klikedz");
    $(".nontop").hide();
    //show callers children..
    $(".parent"+me).show();
    //..and the caller itself...
    $("#gallery"+me).show();
    //...and its parents
    num = me;
    while (num != -1) {
        num = recurse(num);
    }
    $.getJSON("/ajax/gallery/"+me, {
        cache: false
    }, function(data){
		console.log(data);
		//the gallery_init() bellow creates a new one
		$(".galleria_wrapper").remove();
		$("ul#galerija-thumbnails li").remove();
		
		for(var i=0;i<data.length;i++){
			list_elem = $("<li class='galerija-button'><img class='thumb noscale' width='120' height='100' src='"+data[i].normal_url+"' rel='"+data[i].normal_url+"' /></li>");    
			$("ul#galerija-thumbnails").prepend(list_elem);
		}

		gallery_init();
		
		//now makes sense to display the full size link
		$("#full_size").show();
    });
}
$(function(){
    //TODO: make copy/pastable urls work
    bits = location.hash.split('/');
    if (bits[2]) {
        $.getJSON("/ajax/gallery/"+bits[2], {
            cache: false
        }, function(data){ 
                //the gallery_init() bellow creates a new one
                $(".galleria_wrapper").remove();
                $("ul#galerija-thumbnails li").remove();
                for(var i=0;i<data.length;i++){
                    list_elem = $("<li class='galerija-button'><img class='thumb noscale' width='120' height='100' src='"+data[i].normal_url+"' rel='"+data[i].normal_url+"' /></li>");
                    $("ul#galerija-thumbnails").append(list_elem);
                }

				gallery_init();

                //now makes sense to display the full size link
                $("#full_size").show();
        });
    } else {
        //display default image if none has been requested
		console.log("blabla, brisem kontent");
        $(".galerija-content").html('<div class="galleria_wrapper"><img src="http://www.screensite.org/courses/Jbutler/T340/TreasonOfImagesShadow.jpg"></div>');
    }
    $(".nontop").hide(); //show only the top galleries a first
    $('.galerija-content').addClass('gallery_demo'); // adds new class name to maintain degradability
});