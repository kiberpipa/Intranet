dojo.require("dojo.fx.*");
dojo.require("dojo.style");
//dojo.require("dojo.widget.Editor");

//dojo.require("dojo.widget.*");
//dojo.require("dojo.widget.InlineEditBox");
//dojo.require("dojo.event.*");

function formExplode(start, unique) {
    var end = document.getElementById("dnevnikForm");
    var mr = (Math.floor((document.body.offsetWidth/2)) - 240);
    end.style.left = mr + "px";

    document.dnevnikForm.uniqueSpot.value = unique;
    dojo.fx.html.explode(start, end, 250);
}

function formImplode(start) {
    var end = document.getElementById("dnevnikForm");
    dojo.fx.html.implode(end, start, 250);
}

window.onload=function myLoad(){
    Rounded("div#dezurni","all","#fff","#ff8200");
    Rounded("div#dnevnikForm","all","transparent","#ff8200","border");
    Rounded("h3","top","#efefef","#ff8200","small border #999");
    Rounded("div#log","all","#fff","#ff8200");
}


//function saveHandler(newValue, oldValue) {
//    dojo.debug("New Value: " + newValue + " Old Value: " + oldValue);
//}
//
//function init() {
//    var editable = dojo.widget.byId("editable");
//   editable.onSave = saveHandler;
//    
//    myLoad();
//}
//
//dojo.addOnLoad(init)
