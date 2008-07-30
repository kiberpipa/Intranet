$(document).ready(function() {
   $(".hideme").hide();
   
   $(".expand").click(function() {
        //alert(1);
        $(this).parent().children("div").toggle(); //To lahko bindamo tudi na class "hideme" :)
   });
});

