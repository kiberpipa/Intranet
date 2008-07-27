$(document).ready(function() {
   $("#diary_box, #bug_box, #lend_box").hide();
   
   $(".expand").click(function() {
        //alert(1);
        $(this).parent().children("div").toggle();
   });
});

