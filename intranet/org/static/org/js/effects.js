$(document).ready(function() {
   $(".hideme").hide();
   
   $(".expand").click(function() {
        $(this).parent().children("div").toggle(); //To lahko bindamo tudi na class "hideme" :)
   });
});

