/*
	Copyright (c) 2004-2005, The Dojo Foundation
	All Rights Reserved.

	Licensed under the Academic Free License version 2.1 or above OR the
	modified BSD license. For more information on Dojo licensing, see:

		http://dojotoolkit.org/community/licensing.shtml
*/

/*
	This is a compiled version of Dojo, built for deployment and not for
	development. To get an editable version, please visit:

		http://dojotoolkit.org

	for documentation and information on getting the source.
*/

var dj_global=this;
function dj_undef(_1,_2){
if(!_2){
_2=dj_global;
}
return (typeof _2[_1]=="undefined");
}
if(dj_undef("djConfig")){
var djConfig={};
}
var dojo;
if(dj_undef("dojo")){
dojo={};
}
dojo.version={major:0,minor:2,patch:2,flag:"",revision:Number("$Rev: 2836 $".match(/[0-9]+/)[0]),toString:function(){
with(dojo.version){
return major+"."+minor+"."+patch+flag+" ("+revision+")";
}
}};
dojo.evalObjPath=function(_3,_4){
if(typeof _3!="string"){
return dj_global;
}
if(_3.indexOf(".")==-1){
if((dj_undef(_3,dj_global))&&(_4)){
dj_global[_3]={};
}
return dj_global[_3];
}
var _5=_3.split(/\./);
var _6=dj_global;
for(var i=0;i<_5.length;++i){
if(!_4){
_6=_6[_5[i]];
if((typeof _6=="undefined")||(!_6)){
return _6;
}
}else{
if(dj_undef(_5[i],_6)){
_6[_5[i]]={};
}
_6=_6[_5[i]];
}
}
return _6;
};
dojo.errorToString=function(_8){
return ((!dj_undef("message",_8))?_8.message:(dj_undef("description",_8)?_8:_8.description));
};
dojo.raise=function(_9,_a){
if(_a){
_9=_9+": "+dojo.errorToString(_a);
}
var he=dojo.hostenv;
if((!dj_undef("hostenv",dojo))&&(!dj_undef("println",dojo.hostenv))){
dojo.hostenv.println("FATAL: "+_9);
}
throw Error(_9);
};
dj_throw=dj_rethrow=function(m,e){
dojo.deprecated("dj_throw and dj_rethrow deprecated, use dojo.raise instead");
dojo.raise(m,e);
};
dojo.debug=function(){
if(!djConfig.isDebug){
return;
}
var _e=arguments;
if(dj_undef("println",dojo.hostenv)){
dojo.raise("dojo.debug not available (yet?)");
}
var _f=dj_global["jum"]&&!dj_global["jum"].isBrowser;
var s=[(_f?"":"DEBUG: ")];
for(var i=0;i<_e.length;++i){
if(!false&&_e[i] instanceof Error){
var msg="["+_e[i].name+": "+dojo.errorToString(_e[i])+(_e[i].fileName?", file: "+_e[i].fileName:"")+(_e[i].lineNumber?", line: "+_e[i].lineNumber:"")+"]";
}else{
try{
var msg=String(_e[i]);
}
catch(e){
if(dojo.render.html.ie){
var msg="[ActiveXObject]";
}else{
var msg="[unknown]";
}
}
}
s.push(msg);
}
if(_f){
jum.debug(s.join(" "));
}else{
dojo.hostenv.println(s.join(" "));
}
};
dojo.debugShallow=function(obj){
if(!djConfig.isDebug){
return;
}
dojo.debug("------------------------------------------------------------");
dojo.debug("Object: "+obj);
for(i in obj){
dojo.debug(i+": "+obj[i]);
}
dojo.debug("------------------------------------------------------------");
};
var dj_debug=dojo.debug;
function dj_eval(s){
return dj_global.eval?dj_global.eval(s):eval(s);
}
dj_unimplemented=dojo.unimplemented=function(_15,_16){
var _17="'"+_15+"' not implemented";
if((!dj_undef(_16))&&(_16)){
_17+=" "+_16;
}
dojo.raise(_17);
};
dj_deprecated=dojo.deprecated=function(_18,_19,_1a){
var _1b="DEPRECATED: "+_18;
if(_19){
_1b+=" "+_19;
}
if(_1a){
_1b+=" -- will be removed in version: "+_1a;
}
dojo.debug(_1b);
};
dojo.inherits=function(_1c,_1d){
if(typeof _1d!="function"){
dojo.raise("superclass: "+_1d+" borken");
}
_1c.prototype=new _1d();
_1c.prototype.constructor=_1c;
_1c.superclass=_1d.prototype;
_1c["super"]=_1d.prototype;
};
dj_inherits=function(_1e,_1f){
dojo.deprecated("dj_inherits deprecated, use dojo.inherits instead");
dojo.inherits(_1e,_1f);
};
dojo.render=(function(){
function vscaffold(_20,_21){
var tmp={capable:false,support:{builtin:false,plugin:false},prefixes:_20};
for(var x in _21){
tmp[x]=false;
}
return tmp;
}
return {name:"",ver:dojo.version,os:{win:false,linux:false,osx:false},html:vscaffold(["html"],["ie","opera","khtml","safari","moz"]),svg:vscaffold(["svg"],["corel","adobe","batik"]),vml:vscaffold(["vml"],["ie"]),swf:vscaffold(["Swf","Flash","Mm"],["mm"]),swt:vscaffold(["Swt"],["ibm"])};
})();
dojo.hostenv=(function(){
var _24={isDebug:false,allowQueryConfig:false,baseScriptUri:"",baseRelativePath:"",libraryScriptUri:"",iePreventClobber:false,ieClobberMinimal:true,preventBackButtonFix:true,searchIds:[],parseWidgets:true};
if(typeof djConfig=="undefined"){
djConfig=_24;
}else{
for(var _25 in _24){
if(typeof djConfig[_25]=="undefined"){
djConfig[_25]=_24[_25];
}
}
}
var djc=djConfig;
function _def(obj,_28,def){
return (dj_undef(_28,obj)?def:obj[_28]);
}
return {name_:"(unset)",version_:"(unset)",pkgFileName:"__package__",loading_modules_:{},loaded_modules_:{},addedToLoadingCount:[],removedFromLoadingCount:[],inFlightCount:0,modulePrefixes_:{dojo:{name:"dojo",value:"src"}},setModulePrefix:function(_2a,_2b){
this.modulePrefixes_[_2a]={name:_2a,value:_2b};
},getModulePrefix:function(_2c){
var mp=this.modulePrefixes_;
if((mp[_2c])&&(mp[_2c]["name"])){
return mp[_2c].value;
}
return _2c;
},getTextStack:[],loadUriStack:[],loadedUris:[],post_load_:false,modulesLoadedListeners:[],getName:function(){
return this.name_;
},getVersion:function(){
return this.version_;
},getText:function(uri){
dojo.unimplemented("getText","uri="+uri);
},getLibraryScriptUri:function(){
dojo.unimplemented("getLibraryScriptUri","");
}};
})();
dojo.hostenv.getBaseScriptUri=function(){
if(djConfig.baseScriptUri.length){
return djConfig.baseScriptUri;
}
var uri=new String(djConfig.libraryScriptUri||djConfig.baseRelativePath);
if(!uri){
dojo.raise("Nothing returned by getLibraryScriptUri(): "+uri);
}
var _30=uri.lastIndexOf("/");
djConfig.baseScriptUri=djConfig.baseRelativePath;
return djConfig.baseScriptUri;
};
dojo.hostenv.setBaseScriptUri=function(uri){
djConfig.baseScriptUri=uri;
};
dojo.hostenv.loadPath=function(_32,_33,cb){
if((_32.charAt(0)=="/")||(_32.match(/^\w+:/))){
dojo.raise("relpath '"+_32+"'; must be relative");
}
var uri=this.getBaseScriptUri()+_32;
if(djConfig.cacheBust&&dojo.render.html.capable){
uri+="?"+String(djConfig.cacheBust).replace(/\W+/g,"");
}
try{
return ((!_33)?this.loadUri(uri,cb):this.loadUriAndCheck(uri,_33,cb));
}
catch(e){
dojo.debug(e);
return false;
}
};
dojo.hostenv.loadUri=function(uri,cb){
if(this.loadedUris[uri]){
return;
}
var _38=this.getText(uri,null,true);
if(_38==null){
return 0;
}
this.loadedUris[uri]=true;
var _39=dj_eval(_38);
return 1;
};
dojo.hostenv.loadUriAndCheck=function(uri,_3b,cb){
var ok=true;
try{
ok=this.loadUri(uri,cb);
}
catch(e){
dojo.debug("failed loading ",uri," with error: ",e);
}
return ((ok)&&(this.findModule(_3b,false)))?true:false;
};
dojo.loaded=function(){
};
dojo.hostenv.loaded=function(){
this.post_load_=true;
var mll=this.modulesLoadedListeners;
for(var x=0;x<mll.length;x++){
mll[x]();
}
dojo.loaded();
};
dojo.addOnLoad=function(obj,_41){
if(arguments.length==1){
dojo.hostenv.modulesLoadedListeners.push(obj);
}else{
if(arguments.length>1){
dojo.hostenv.modulesLoadedListeners.push(function(){
obj[_41]();
});
}
}
};
dojo.hostenv.modulesLoaded=function(){
if(this.post_load_){
return;
}
if((this.loadUriStack.length==0)&&(this.getTextStack.length==0)){
if(this.inFlightCount>0){
dojo.debug("files still in flight!");
return;
}
if(typeof setTimeout=="object"){
setTimeout("dojo.hostenv.loaded();",0);
}else{
dojo.hostenv.loaded();
}
}
};
dojo.hostenv.moduleLoaded=function(_42){
var _43=dojo.evalObjPath((_42.split(".").slice(0,-1)).join("."));
this.loaded_modules_[(new String(_42)).toLowerCase()]=_43;
};
dojo.hostenv._global_omit_module_check=false;
dojo.hostenv.loadModule=function(_44,_45,_46){
if(!_44){
return;
}
_46=this._global_omit_module_check||_46;
var _47=this.findModule(_44,false);
if(_47){
return _47;
}
if(dj_undef(_44,this.loading_modules_)){
this.addedToLoadingCount.push(_44);
}
this.loading_modules_[_44]=1;
var _48=_44.replace(/\./g,"/")+".js";
var _49=_44.split(".");
var _4a=_44.split(".");
for(var i=_49.length-1;i>0;i--){
var _4c=_49.slice(0,i).join(".");
var _4d=this.getModulePrefix(_4c);
if(_4d!=_4c){
_49.splice(0,i,_4d);
break;
}
}
var _4e=_49[_49.length-1];
if(_4e=="*"){
_44=(_4a.slice(0,-1)).join(".");
while(_49.length){
_49.pop();
_49.push(this.pkgFileName);
_48=_49.join("/")+".js";
if(_48.charAt(0)=="/"){
_48=_48.slice(1);
}
ok=this.loadPath(_48,((!_46)?_44:null));
if(ok){
break;
}
_49.pop();
}
}else{
_48=_49.join("/")+".js";
_44=_4a.join(".");
var ok=this.loadPath(_48,((!_46)?_44:null));
if((!ok)&&(!_45)){
_49.pop();
while(_49.length){
_48=_49.join("/")+".js";
ok=this.loadPath(_48,((!_46)?_44:null));
if(ok){
break;
}
_49.pop();
_48=_49.join("/")+"/"+this.pkgFileName+".js";
if(_48.charAt(0)=="/"){
_48=_48.slice(1);
}
ok=this.loadPath(_48,((!_46)?_44:null));
if(ok){
break;
}
}
}
if((!ok)&&(!_46)){
dojo.raise("Could not load '"+_44+"'; last tried '"+_48+"'");
}
}
if(!_46){
_47=this.findModule(_44,false);
if(!_47){
dojo.raise("symbol '"+_44+"' is not defined after loading '"+_48+"'");
}
}
return _47;
};
dojo.hostenv.startPackage=function(_50){
var _51=_50.split(/\./);
if(_51[_51.length-1]=="*"){
_51.pop();
}
return dojo.evalObjPath(_51.join("."),true);
};
dojo.hostenv.findModule=function(_52,_53){
var lmn=(new String(_52)).toLowerCase();
if(this.loaded_modules_[lmn]){
return this.loaded_modules_[lmn];
}
var _55=dojo.evalObjPath(_52);
if((_52)&&(typeof _55!="undefined")&&(_55)){
this.loaded_modules_[lmn]=_55;
return _55;
}
if(_53){
dojo.raise("no loaded module named '"+_52+"'");
}
return null;
};
if(typeof window=="undefined"){
dojo.raise("no window object");
}
(function(){
if(djConfig.allowQueryConfig){
var _56=document.location.toString();
var _57=_56.split("?",2);
if(_57.length>1){
var _58=_57[1];
var _59=_58.split("&");
for(var x in _59){
var sp=_59[x].split("=");
if((sp[0].length>9)&&(sp[0].substr(0,9)=="djConfig.")){
var opt=sp[0].substr(9);
try{
djConfig[opt]=eval(sp[1]);
}
catch(e){
djConfig[opt]=sp[1];
}
}
}
}
}
if(((djConfig["baseScriptUri"]=="")||(djConfig["baseRelativePath"]==""))&&(document&&document.getElementsByTagName)){
var _5d=document.getElementsByTagName("script");
var _5e=/(__package__|dojo)\.js([\?\.]|$)/i;
for(var i=0;i<_5d.length;i++){
var src=_5d[i].getAttribute("src");
if(!src){
continue;
}
var m=src.match(_5e);
if(m){
root=src.substring(0,m.index);
if(!this["djConfig"]){
djConfig={};
}
if(djConfig["baseScriptUri"]==""){
djConfig["baseScriptUri"]=root;
}
if(djConfig["baseRelativePath"]==""){
djConfig["baseRelativePath"]=root;
}
break;
}
}
}
var dr=dojo.render;
var drh=dojo.render.html;
var dua=drh.UA=navigator.userAgent;
var dav=drh.AV=navigator.appVersion;
var t=true;
var f=false;
drh.capable=t;
drh.support.builtin=t;
dr.ver=parseFloat(drh.AV);
dr.os.mac=dav.indexOf("Macintosh")>=0;
dr.os.win=dav.indexOf("Windows")>=0;
dr.os.linux=dav.indexOf("X11")>=0;
drh.opera=dua.indexOf("Opera")>=0;
drh.khtml=(dav.indexOf("Konqueror")>=0)||(dav.indexOf("Safari")>=0);
drh.safari=dav.indexOf("Safari")>=0;
var _68=dua.indexOf("Gecko");
drh.mozilla=drh.moz=(_68>=0)&&(!drh.khtml);
if(drh.mozilla){
drh.geckoVersion=dua.substring(_68+6,_68+14);
}
drh.ie=(document.all)&&(!drh.opera);
drh.ie50=drh.ie&&dav.indexOf("MSIE 5.0")>=0;
drh.ie55=drh.ie&&dav.indexOf("MSIE 5.5")>=0;
drh.ie60=drh.ie&&dav.indexOf("MSIE 6.0")>=0;
dr.vml.capable=drh.ie;
dr.svg.capable=f;
dr.svg.support.plugin=f;
dr.svg.support.builtin=f;
dr.svg.adobe=f;
if(document.implementation&&document.implementation.hasFeature&&document.implementation.hasFeature("org.w3c.dom.svg","1.0")){
dr.svg.capable=t;
dr.svg.support.builtin=t;
dr.svg.support.plugin=f;
dr.svg.adobe=f;
}else{
if(navigator.mimeTypes&&navigator.mimeTypes.length>0){
var _69=navigator.mimeTypes["image/svg+xml"]||navigator.mimeTypes["image/svg"]||navigator.mimeTypes["image/svg-xml"];
if(_69){
dr.svg.adobe=_69&&_69.enabledPlugin&&_69.enabledPlugin.description&&(_69.enabledPlugin.description.indexOf("Adobe")>-1);
if(dr.svg.adobe){
dr.svg.capable=t;
dr.svg.support.plugin=t;
}
}
}else{
if(drh.ie&&dr.os.win){
var _69=f;
try{
var _6a=new ActiveXObject("Adobe.SVGCtl");
_69=t;
}
catch(e){
}
if(_69){
dr.svg.capable=t;
dr.svg.support.plugin=t;
dr.svg.adobe=t;
}
}else{
dr.svg.capable=f;
dr.svg.support.plugin=f;
dr.svg.adobe=f;
}
}
}
})();
dojo.hostenv.startPackage("dojo.hostenv");
dojo.hostenv.name_="browser";
dojo.hostenv.searchIds=[];
var DJ_XMLHTTP_PROGIDS=["Msxml2.XMLHTTP","Microsoft.XMLHTTP","Msxml2.XMLHTTP.4.0"];
dojo.hostenv.getXmlhttpObject=function(){
var _6b=null;
var _6c=null;
try{
_6b=new XMLHttpRequest();
}
catch(e){
}
if(!_6b){
for(var i=0;i<3;++i){
var _6e=DJ_XMLHTTP_PROGIDS[i];
try{
_6b=new ActiveXObject(_6e);
}
catch(e){
_6c=e;
}
if(_6b){
DJ_XMLHTTP_PROGIDS=[_6e];
break;
}
}
}
if(!_6b){
return dojo.raise("XMLHTTP not available",_6c);
}
return _6b;
};
dojo.hostenv.getText=function(uri,_70,_71){
var _72=this.getXmlhttpObject();
if(_70){
_72.onreadystatechange=function(){
if((4==_72.readyState)&&(_72["status"])){
if(_72.status==200){
_70(_72.responseText);
}
}
};
}
_72.open("GET",uri,_70?true:false);
_72.send(null);
if(_70){
return null;
}
return _72.responseText;
};
dojo.hostenv.defaultDebugContainerId="dojoDebug";
dojo.hostenv._println_buffer=[];
dojo.hostenv._println_safe=false;
dojo.hostenv.println=function(_73){
if(!dojo.hostenv._println_safe){
dojo.hostenv._println_buffer.push(_73);
}else{
try{
var _74=document.getElementById(djConfig.debugContainerId?djConfig.debugContainerId:dojo.hostenv.defaultDebugContainerId);
if(!_74){
_74=document.getElementsByTagName("body")[0]||document.body;
}
var div=document.createElement("div");
div.appendChild(document.createTextNode(_73));
_74.appendChild(div);
}
catch(e){
try{
document.write("<div>"+_73+"</div>");
}
catch(e2){
window.status=_73;
}
}
}
};
dojo.addOnLoad(function(){
dojo.hostenv._println_safe=true;
while(dojo.hostenv._println_buffer.length>0){
dojo.hostenv.println(dojo.hostenv._println_buffer.shift());
}
});
function dj_addNodeEvtHdlr(_76,_77,fp,_79){
var _7a=_76["on"+_77]||function(){
};
_76["on"+_77]=function(){
fp.apply(_76,arguments);
_7a.apply(_76,arguments);
};
return true;
}
dj_addNodeEvtHdlr(window,"load",function(){
if(dojo.render.html.ie){
dojo.hostenv.makeWidgets();
}
dojo.hostenv.modulesLoaded();
});
dojo.hostenv.makeWidgets=function(){
var _7b=[];
if(djConfig.searchIds&&djConfig.searchIds.length>0){
_7b=_7b.concat(djConfig.searchIds);
}
if(dojo.hostenv.searchIds&&dojo.hostenv.searchIds.length>0){
_7b=_7b.concat(dojo.hostenv.searchIds);
}
if((djConfig.parseWidgets)||(_7b.length>0)){
if(dojo.evalObjPath("dojo.widget.Parse")){
try{
var _7c=new dojo.xml.Parse();
if(_7b.length>0){
for(var x=0;x<_7b.length;x++){
var _7e=document.getElementById(_7b[x]);
if(!_7e){
continue;
}
var _7f=_7c.parseElement(_7e,null,true);
dojo.widget.getParser().createComponents(_7f);
}
}else{
if(djConfig.parseWidgets){
var _7f=_7c.parseElement(document.getElementsByTagName("body")[0]||document.body,null,true);
dojo.widget.getParser().createComponents(_7f);
}
}
}
catch(e){
dojo.debug("auto-build-widgets error:",e);
}
}
}
};
dojo.hostenv.modulesLoadedListeners.push(function(){
if(!dojo.render.html.ie){
dojo.hostenv.makeWidgets();
}
});
try{
if(dojo.render.html.ie){
document.write("<style>v:*{ behavior:url(#default#VML); }</style>");
document.write("<xml:namespace ns=\"urn:schemas-microsoft-com:vml\" prefix=\"v\"/>");
}
}
catch(e){
}
dojo.hostenv.writeIncludes=function(){
};
dojo.hostenv.byId=dojo.byId=function(id,doc){
if(typeof id=="string"||id instanceof String){
if(!doc){
doc=document;
}
return doc.getElementById(id);
}
return id;
};
dojo.hostenv.byIdArray=dojo.byIdArray=function(){
var ids=[];
for(var i=0;i<arguments.length;i++){
if((arguments[i] instanceof Array)||(typeof arguments[i]=="array")){
for(var j=0;j<arguments[i].length;j++){
ids=ids.concat(dojo.hostenv.byIdArray(arguments[i][j]));
}
}else{
ids.push(dojo.hostenv.byId(arguments[i]));
}
}
return ids;
};
dojo.hostenv.conditionalLoadModule=function(_85){
var _86=_85["common"]||[];
var _87=(_85[dojo.hostenv.name_])?_86.concat(_85[dojo.hostenv.name_]||[]):_86.concat(_85["default"]||[]);
for(var x=0;x<_87.length;x++){
var _89=_87[x];
if(_89.constructor==Array){
dojo.hostenv.loadModule.apply(dojo.hostenv,_89);
}else{
dojo.hostenv.loadModule(_89);
}
}
};
dojo.hostenv.require=dojo.hostenv.loadModule;
dojo.require=function(){
dojo.hostenv.loadModule.apply(dojo.hostenv,arguments);
};
dojo.requireAfter=dojo.require;
dojo.requireIf=function(){
if((arguments[0]===true)||(arguments[0]=="common")||(dojo.render[arguments[0]].capable)){
var _8a=[];
for(var i=1;i<arguments.length;i++){
_8a.push(arguments[i]);
}
dojo.require.apply(dojo,_8a);
}
};
dojo.requireAfterIf=dojo.requireIf;
dojo.conditionalRequire=dojo.requireIf;
dojo.kwCompoundRequire=function(){
dojo.hostenv.conditionalLoadModule.apply(dojo.hostenv,arguments);
};
dojo.hostenv.provide=dojo.hostenv.startPackage;
dojo.provide=function(){
return dojo.hostenv.startPackage.apply(dojo.hostenv,arguments);
};
dojo.setModulePrefix=function(_8c,_8d){
return dojo.hostenv.setModulePrefix(_8c,_8d);
};
dojo.profile={start:function(){
},end:function(){
},dump:function(){
}};
dojo.exists=function(obj,_8f){
var p=_8f.split(".");
for(var i=0;i<p.length;i++){
if(!(obj[p[i]])){
return false;
}
obj=obj[p[i]];
}
return true;
};
dojo.provide("dojo.lang");
dojo.provide("dojo.AdapterRegistry");
dojo.provide("dojo.lang.Lang");
dojo.lang.mixin=function(obj,_93){
var _94={};
for(var x in _93){
if(typeof _94[x]=="undefined"||_94[x]!=_93[x]){
obj[x]=_93[x];
}
}
if(dojo.render.html.ie&&dojo.lang.isFunction(_93["toString"])&&_93["toString"]!=obj["toString"]){
obj.toString=_93.toString;
}
return obj;
};
dojo.lang.extend=function(_96,_97){
this.mixin(_96.prototype,_97);
};
dojo.lang.extendPrototype=function(obj,_99){
this.extend(obj.constructor,_99);
};
dojo.lang.anonCtr=0;
dojo.lang.anon={};
dojo.lang.nameAnonFunc=function(_9a,_9b){
var nso=(_9b||dojo.lang.anon);
if((dj_global["djConfig"])&&(djConfig["slowAnonFuncLookups"]==true)){
for(var x in nso){
if(nso[x]===_9a){
return x;
}
}
}
var ret="__"+dojo.lang.anonCtr++;
while(typeof nso[ret]!="undefined"){
ret="__"+dojo.lang.anonCtr++;
}
nso[ret]=_9a;
return ret;
};
dojo.lang.hitch=function(_9f,_a0){
if(dojo.lang.isString(_a0)){
var fcn=_9f[_a0];
}else{
var fcn=_a0;
}
return function(){
return fcn.apply(_9f,arguments);
};
};
dojo.lang.forward=function(_a2){
return function(){
return this[_a2].apply(this,arguments);
};
};
dojo.lang.curry=function(ns,_a4){
var _a5=[];
ns=ns||dj_global;
if(dojo.lang.isString(_a4)){
_a4=ns[_a4];
}
for(var x=2;x<arguments.length;x++){
_a5.push(arguments[x]);
}
var _a7=_a4.length-_a5.length;
function gather(_a8,_a9,_aa){
var _ab=_aa;
var _ac=_a9.slice(0);
for(var x=0;x<_a8.length;x++){
_ac.push(_a8[x]);
}
_aa=_aa-_a8.length;
if(_aa<=0){
var res=_a4.apply(ns,_ac);
_aa=_ab;
return res;
}else{
return function(){
return gather(arguments,_ac,_aa);
};
}
}
return gather([],_a5,_a7);
};
dojo.lang.curryArguments=function(ns,_b0,_b1,_b2){
var _b3=[];
var x=_b2||0;
for(x=_b2;x<_b1.length;x++){
_b3.push(_b1[x]);
}
return dojo.lang.curry.apply(dojo.lang,[ns,_b0].concat(_b3));
};
dojo.lang.setTimeout=function(_b5,_b6){
var _b7=window,argsStart=2;
if(!dojo.lang.isFunction(_b5)){
_b7=_b5;
_b5=_b6;
_b6=arguments[2];
argsStart++;
}
if(dojo.lang.isString(_b5)){
_b5=_b7[_b5];
}
var _b8=[];
for(var i=argsStart;i<arguments.length;i++){
_b8.push(arguments[i]);
}
return setTimeout(function(){
_b5.apply(_b7,_b8);
},_b6);
};
dojo.lang.isObject=function(wh){
return typeof wh=="object"||dojo.lang.isArray(wh)||dojo.lang.isFunction(wh);
};
dojo.lang.isArray=function(wh){
return (wh instanceof Array||typeof wh=="array");
};
dojo.lang.isArrayLike=function(wh){
if(dojo.lang.isString(wh)){
return false;
}
if(dojo.lang.isArray(wh)){
return true;
}
if(typeof wh!="undefined"&&wh&&dojo.lang.isNumber(wh.length)&&isFinite(wh.length)){
return true;
}
return false;
};
dojo.lang.isFunction=function(wh){
return (wh instanceof Function||typeof wh=="function");
};
dojo.lang.isString=function(wh){
return (wh instanceof String||typeof wh=="string");
};
dojo.lang.isAlien=function(wh){
return !dojo.lang.isFunction()&&/\{\s*\[native code\]\s*\}/.test(String(wh));
};
dojo.lang.isBoolean=function(wh){
return (wh instanceof Boolean||typeof wh=="boolean");
};
dojo.lang.isNumber=function(wh){
return (wh instanceof Number||typeof wh=="number");
};
dojo.lang.isUndefined=function(wh){
return ((wh==undefined)&&(typeof wh=="undefined"));
};
dojo.lang.whatAmI=function(wh){
try{
if(dojo.lang.isArray(wh)){
return "array";
}
if(dojo.lang.isFunction(wh)){
return "function";
}
if(dojo.lang.isString(wh)){
return "string";
}
if(dojo.lang.isNumber(wh)){
return "number";
}
if(dojo.lang.isBoolean(wh)){
return "boolean";
}
if(dojo.lang.isAlien(wh)){
return "alien";
}
if(dojo.lang.isUndefined(wh)){
return "undefined";
}
for(var _c4 in dojo.lang.whatAmI.custom){
if(dojo.lang.whatAmI.custom[_c4](wh)){
return _c4;
}
}
if(dojo.lang.isObject(wh)){
return "object";
}
}
catch(E){
}
return "unknown";
};
dojo.lang.whatAmI.custom={};
dojo.lang.find=function(arr,val,_c7){
if(!dojo.lang.isArrayLike(arr)&&dojo.lang.isArrayLike(val)){
var a=arr;
arr=val;
val=a;
}
var _c9=dojo.lang.isString(arr);
if(_c9){
arr=arr.split("");
}
if(_c7){
for(var i=0;i<arr.length;++i){
if(arr[i]===val){
return i;
}
}
}else{
for(var i=0;i<arr.length;++i){
if(arr[i]==val){
return i;
}
}
}
return -1;
};
dojo.lang.indexOf=dojo.lang.find;
dojo.lang.findLast=function(arr,val,_cd){
if(!dojo.lang.isArrayLike(arr)&&dojo.lang.isArrayLike(val)){
var a=arr;
arr=val;
val=a;
}
var _cf=dojo.lang.isString(arr);
if(_cf){
arr=arr.split("");
}
if(_cd){
for(var i=arr.length-1;i>=0;i--){
if(arr[i]===val){
return i;
}
}
}else{
for(var i=arr.length-1;i>=0;i--){
if(arr[i]==val){
return i;
}
}
}
return -1;
};
dojo.lang.lastIndexOf=dojo.lang.findLast;
dojo.lang.inArray=function(arr,val){
return dojo.lang.find(arr,val)>-1;
};
dojo.lang.getNameInObj=function(ns,_d4){
if(!ns){
ns=dj_global;
}
for(var x in ns){
if(ns[x]===_d4){
return new String(x);
}
}
return null;
};
dojo.lang.has=function(obj,_d7){
return (typeof obj[_d7]!=="undefined");
};
dojo.lang.isEmpty=function(obj){
if(dojo.lang.isObject(obj)){
var tmp={};
var _da=0;
for(var x in obj){
if(obj[x]&&(!tmp[x])){
_da++;
break;
}
}
return (_da==0);
}else{
if(dojo.lang.isArrayLike(obj)||dojo.lang.isString(obj)){
return obj.length==0;
}
}
};
dojo.lang.forEach=function(arr,_dd,_de){
var _df=dojo.lang.isString(arr);
if(_df){
arr=arr.split("");
}
var il=arr.length;
for(var i=0;i<((_de)?il:arr.length);i++){
if(_dd(arr[i],i,arr)=="break"){
break;
}
}
};
dojo.lang.map=function(arr,obj,_e4){
var _e5=dojo.lang.isString(arr);
if(_e5){
arr=arr.split("");
}
if(dojo.lang.isFunction(obj)&&(!_e4)){
_e4=obj;
obj=dj_global;
}else{
if(dojo.lang.isFunction(obj)&&_e4){
var _e6=obj;
obj=_e4;
_e4=_e6;
}
}
if(Array.map){
var _e7=Array.map(arr,_e4,obj);
}else{
var _e7=[];
for(var i=0;i<arr.length;++i){
_e7.push(_e4.call(obj,arr[i]));
}
}
if(_e5){
return _e7.join("");
}else{
return _e7;
}
};
dojo.lang.tryThese=function(){
for(var x=0;x<arguments.length;x++){
try{
if(typeof arguments[x]=="function"){
var ret=(arguments[x]());
if(ret){
return ret;
}
}
}
catch(e){
dojo.debug(e);
}
}
};
dojo.lang.delayThese=function(_eb,cb,_ed,_ee){
if(!_eb.length){
if(typeof _ee=="function"){
_ee();
}
return;
}
if((typeof _ed=="undefined")&&(typeof cb=="number")){
_ed=cb;
cb=function(){
};
}else{
if(!cb){
cb=function(){
};
if(!_ed){
_ed=0;
}
}
}
setTimeout(function(){
(_eb.shift())();
cb();
dojo.lang.delayThese(_eb,cb,_ed,_ee);
},_ed);
};
dojo.lang.shallowCopy=function(obj){
var ret={},key;
for(key in obj){
if(dojo.lang.isUndefined(ret[key])){
ret[key]=obj[key];
}
}
return ret;
};
dojo.lang.every=function(arr,_f2,_f3){
var _f4=dojo.lang.isString(arr);
if(_f4){
arr=arr.split("");
}
if(Array.every){
return Array.every(arr,_f2,_f3);
}else{
if(!_f3){
if(arguments.length>=3){
dojo.raise("thisObject doesn't exist!");
}
_f3=dj_global;
}
for(var i=0;i<arr.length;i++){
if(!_f2.call(_f3,arr[i],i,arr)){
return false;
}
}
return true;
}
};
dojo.lang.some=function(arr,_f7,_f8){
var _f9=dojo.lang.isString(arr);
if(_f9){
arr=arr.split("");
}
if(Array.some){
return Array.some(arr,_f7,_f8);
}else{
if(!_f8){
if(arguments.length>=3){
dojo.raise("thisObject doesn't exist!");
}
_f8=dj_global;
}
for(var i=0;i<arr.length;i++){
if(_f7.call(_f8,arr[i],i,arr)){
return true;
}
}
return false;
}
};
dojo.lang.filter=function(arr,_fc,_fd){
var _fe=dojo.lang.isString(arr);
if(_fe){
arr=arr.split("");
}
if(Array.filter){
var _ff=Array.filter(arr,_fc,_fd);
}else{
if(!_fd){
if(arguments.length>=3){
dojo.raise("thisObject doesn't exist!");
}
_fd=dj_global;
}
var _ff=[];
for(var i=0;i<arr.length;i++){
if(_fc.call(_fd,arr[i],i,arr)){
_ff.push(arr[i]);
}
}
}
if(_fe){
return _ff.join("");
}else{
return _ff;
}
};
dojo.AdapterRegistry=function(){
this.pairs=[];
};
dojo.lang.extend(dojo.AdapterRegistry,{register:function(name,_102,wrap,_104){
if(_104){
this.pairs.unshift([name,_102,wrap]);
}else{
this.pairs.push([name,_102,wrap]);
}
},match:function(){
for(var i=0;i<this.pairs.length;i++){
var pair=this.pairs[i];
if(pair[1].apply(this,arguments)){
return pair[2].apply(this,arguments);
}
}
throw new Error("No match found");
},unregister:function(name){
for(var i=0;i<this.pairs.length;i++){
var pair=this.pairs[i];
if(pair[0]==name){
this.pairs.splice(i,1);
return true;
}
}
return false;
}});
dojo.lang.reprRegistry=new dojo.AdapterRegistry();
dojo.lang.registerRepr=function(name,_10b,wrap,_10d){
dojo.lang.reprRegistry.register(name,_10b,wrap,_10d);
};
dojo.lang.repr=function(obj){
if(typeof (obj)=="undefined"){
return "undefined";
}else{
if(obj===null){
return "null";
}
}
try{
if(typeof (obj["__repr__"])=="function"){
return obj["__repr__"]();
}else{
if((typeof (obj["repr"])=="function")&&(obj.repr!=arguments.callee)){
return obj["repr"]();
}
}
return dojo.lang.reprRegistry.match(obj);
}
catch(e){
if(typeof (obj.NAME)=="string"&&(obj.toString==Function.prototype.toString||obj.toString==Object.prototype.toString)){
return o.NAME;
}
}
if(typeof (obj)=="function"){
obj=(obj+"").replace(/^\s+/,"");
var idx=obj.indexOf("{");
if(idx!=-1){
obj=obj.substr(0,idx)+"{...}";
}
}
return obj+"";
};
dojo.lang.reprArrayLike=function(arr){
try{
var na=dojo.lang.map(arr,dojo.lang.repr);
return "["+na.join(", ")+"]";
}
catch(e){
}
};
dojo.lang.reprString=function(str){
return ("\""+str.replace(/(["\\])/g,"\\$1")+"\"").replace(/[\f]/g,"\\f").replace(/[\b]/g,"\\b").replace(/[\n]/g,"\\n").replace(/[\t]/g,"\\t").replace(/[\r]/g,"\\r");
};
dojo.lang.reprNumber=function(num){
return num+"";
};
(function(){
var m=dojo.lang;
m.registerRepr("arrayLike",m.isArrayLike,m.reprArrayLike);
m.registerRepr("string",m.isString,m.reprString);
m.registerRepr("numbers",m.isNumber,m.reprNumber);
m.registerRepr("boolean",m.isBoolean,m.reprNumber);
})();
dojo.lang.unnest=function(){
var out=[];
for(var i=0;i<arguments.length;i++){
if(dojo.lang.isArrayLike(arguments[i])){
var add=dojo.lang.unnest.apply(this,arguments[i]);
out=out.concat(add);
}else{
out.push(arguments[i]);
}
}
return out;
};
dojo.lang.firstValued=function(){
for(var i=0;i<arguments.length;i++){
if(typeof arguments[i]!="undefined"){
return arguments[i];
}
}
return undefined;
};
dojo.lang.toArray=function(_119,_11a){
var _11b=[];
for(var i=_11a||0;i<_119.length;i++){
_11b.push(_119[i]);
}
return _11b;
};
dojo.provide("dojo.string");
dojo.require("dojo.lang");
dojo.string.trim=function(str,wh){
if(!dojo.lang.isString(str)){
return str;
}
if(!str.length){
return str;
}
if(wh>0){
return str.replace(/^\s+/,"");
}else{
if(wh<0){
return str.replace(/\s+$/,"");
}else{
return str.replace(/^\s+|\s+$/g,"");
}
}
};
dojo.string.trimStart=function(str){
return dojo.string.trim(str,1);
};
dojo.string.trimEnd=function(str){
return dojo.string.trim(str,-1);
};
dojo.string.paramString=function(str,_122,_123){
for(var name in _122){
var re=new RegExp("\\%\\{"+name+"\\}","g");
str=str.replace(re,_122[name]);
}
if(_123){
str=str.replace(/%\{([^\}\s]+)\}/g,"");
}
return str;
};
dojo.string.capitalize=function(str){
if(!dojo.lang.isString(str)){
return "";
}
if(arguments.length==0){
str=this;
}
var _127=str.split(" ");
var _128="";
var len=_127.length;
for(var i=0;i<len;i++){
var word=_127[i];
word=word.charAt(0).toUpperCase()+word.substring(1,word.length);
_128+=word;
if(i<len-1){
_128+=" ";
}
}
return new String(_128);
};
dojo.string.isBlank=function(str){
if(!dojo.lang.isString(str)){
return true;
}
return (dojo.string.trim(str).length==0);
};
dojo.string.encodeAscii=function(str){
if(!dojo.lang.isString(str)){
return str;
}
var ret="";
var _12f=escape(str);
var _130,re=/%u([0-9A-F]{4})/i;
while((_130=_12f.match(re))){
var num=Number("0x"+_130[1]);
var _132=escape("&#"+num+";");
ret+=_12f.substring(0,_130.index)+_132;
_12f=_12f.substring(_130.index+_130[0].length);
}
ret+=_12f.replace(/\+/g,"%2B");
return ret;
};
dojo.string.summary=function(str,len){
if(!len||str.length<=len){
return str;
}else{
return str.substring(0,len).replace(/\.+$/,"")+"...";
}
};
dojo.string.escape=function(type,str){
var args=[];
for(var i=1;i<arguments.length;i++){
args.push(arguments[i]);
}
switch(type.toLowerCase()){
case "xml":
case "html":
case "xhtml":
return dojo.string.escapeXml.apply(this,args);
case "sql":
return dojo.string.escapeSql.apply(this,args);
case "regexp":
case "regex":
return dojo.string.escapeRegExp.apply(this,args);
case "javascript":
case "jscript":
case "js":
return dojo.string.escapeJavaScript.apply(this,args);
case "ascii":
return dojo.string.encodeAscii.apply(this,args);
default:
return str;
}
};
dojo.string.escapeXml=function(str,_13a){
str=str.replace(/&/gm,"&amp;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").replace(/"/gm,"&quot;");
if(!_13a){
str=str.replace(/'/gm,"&#39;");
}
return str;
};
dojo.string.escapeSql=function(str){
return str.replace(/'/gm,"''");
};
dojo.string.escapeRegExp=function(str){
return str.replace(/\\/gm,"\\\\").replace(/([\f\b\n\t\r])/gm,"\\$1");
};
dojo.string.escapeJavaScript=function(str){
return str.replace(/(["'\f\b\n\t\r])/gm,"\\$1");
};
dojo.string.repeat=function(str,_13f,_140){
var out="";
for(var i=0;i<_13f;i++){
out+=str;
if(_140&&i<_13f-1){
out+=_140;
}
}
return out;
};
dojo.string.endsWith=function(str,end,_145){
if(_145){
str=str.toLowerCase();
end=end.toLowerCase();
}
return str.lastIndexOf(end)==str.length-end.length;
};
dojo.string.endsWithAny=function(str){
for(var i=1;i<arguments.length;i++){
if(dojo.string.endsWith(str,arguments[i])){
return true;
}
}
return false;
};
dojo.string.startsWith=function(str,_149,_14a){
if(_14a){
str=str.toLowerCase();
_149=_149.toLowerCase();
}
return str.indexOf(_149)==0;
};
dojo.string.startsWithAny=function(str){
for(var i=1;i<arguments.length;i++){
if(dojo.string.startsWith(str,arguments[i])){
return true;
}
}
return false;
};
dojo.string.has=function(str){
for(var i=1;i<arguments.length;i++){
if(str.indexOf(arguments[i]>-1)){
return true;
}
}
return false;
};
dojo.string.pad=function(str,len,c,dir){
var out=String(str);
if(!c){
c="0";
}
if(!dir){
dir=1;
}
while(out.length<len){
if(dir>0){
out=c+out;
}else{
out+=c;
}
}
return out;
};
dojo.string.padLeft=function(str,len,c){
return dojo.string.pad(str,len,c,1);
};
dojo.string.padRight=function(str,len,c){
return dojo.string.pad(str,len,c,-1);
};
dojo.string.normalizeNewlines=function(text,_15b){
if(_15b=="\n"){
text=text.replace(/\r\n/g,"\n");
text=text.replace(/\r/g,"\n");
}else{
if(_15b=="\r"){
text=text.replace(/\r\n/g,"\r");
text=text.replace(/\n/g,"\r");
}else{
text=text.replace(/([^\r])\n/g,"$1\r\n");
text=text.replace(/\r([^\n])/g,"\r\n$1");
}
}
return text;
};
dojo.string.splitEscaped=function(str,_15d){
var _15e=[];
for(var i=0,prevcomma=0;i<str.length;i++){
if(str.charAt(i)=="\\"){
i++;
continue;
}
if(str.charAt(i)==_15d){
_15e.push(str.substring(prevcomma,i));
prevcomma=i+1;
}
}
_15e.push(str.substr(prevcomma));
return _15e;
};
dojo.string.addToPrototype=function(){
for(var _160 in dojo.string){
if(dojo.lang.isFunction(dojo.string[_160])){
var func=(function(){
var meth=_160;
switch(meth){
case "addToPrototype":
return null;
break;
case "escape":
return function(type){
return dojo.string.escape(type,this);
};
break;
default:
return function(){
var args=[this];
for(var i=0;i<arguments.length;i++){
args.push(arguments[i]);
}
dojo.debug(args);
return dojo.string[meth].apply(dojo.string,args);
};
}
})();
if(func){
String.prototype[_160]=func;
}
}
}
};
dojo.provide("dojo.io.IO");
dojo.require("dojo.string");
dojo.io.transports=[];
dojo.io.hdlrFuncNames=["load","error"];
dojo.io.Request=function(url,_167,_168,_169){
if((arguments.length==1)&&(arguments[0].constructor==Object)){
this.fromKwArgs(arguments[0]);
}else{
this.url=url;
if(_167){
this.mimetype=_167;
}
if(_168){
this.transport=_168;
}
if(arguments.length>=4){
this.changeUrl=_169;
}
}
};
dojo.lang.extend(dojo.io.Request,{url:"",mimetype:"text/plain",method:"GET",content:undefined,transport:undefined,changeUrl:undefined,formNode:undefined,sync:false,bindSuccess:false,useCache:false,preventCache:false,load:function(type,data,evt){
},error:function(type,_16e){
},handle:function(){
},abort:function(){
},fromKwArgs:function(_16f){
if(_16f["url"]){
_16f.url=_16f.url.toString();
}
if(!_16f["method"]&&_16f["formNode"]&&_16f["formNode"].method){
_16f.method=_16f["formNode"].method;
}
if(!_16f["handle"]&&_16f["handler"]){
_16f.handle=_16f.handler;
}
if(!_16f["load"]&&_16f["loaded"]){
_16f.load=_16f.loaded;
}
if(!_16f["changeUrl"]&&_16f["changeURL"]){
_16f.changeUrl=_16f.changeURL;
}
_16f.encoding=dojo.lang.firstValued(_16f["encoding"],djConfig["bindEncoding"],"");
_16f.sendTransport=dojo.lang.firstValued(_16f["sendTransport"],djConfig["ioSendTransport"],true);
var _170=dojo.lang.isFunction;
for(var x=0;x<dojo.io.hdlrFuncNames.length;x++){
var fn=dojo.io.hdlrFuncNames[x];
if(_170(_16f[fn])){
continue;
}
if(_170(_16f["handle"])){
_16f[fn]=_16f.handle;
}
}
dojo.lang.mixin(this,_16f);
}});
dojo.io.Error=function(msg,type,num){
this.message=msg;
this.type=type||"unknown";
this.number=num||0;
};
dojo.io.transports.addTransport=function(name){
this.push(name);
this[name]=dojo.io[name];
};
dojo.io.bind=function(_177){
if(!(_177 instanceof dojo.io.Request)){
try{
_177=new dojo.io.Request(_177);
}
catch(e){
dojo.debug(e);
}
}
var _178="";
if(_177["transport"]){
_178=_177["transport"];
if(!this[_178]){
return _177;
}
}else{
for(var x=0;x<dojo.io.transports.length;x++){
var tmp=dojo.io.transports[x];
if((this[tmp])&&(this[tmp].canHandle(_177))){
_178=tmp;
}
}
if(_178==""){
return _177;
}
}
this[_178].bind(_177);
_177.bindSuccess=true;
return _177;
};
dojo.io.queueBind=function(_17b){
if(!(_17b instanceof dojo.io.Request)){
try{
_17b=new dojo.io.Request(_17b);
}
catch(e){
dojo.debug(e);
}
}
var _17c=_17b.load;
_17b.load=function(){
dojo.io._queueBindInFlight=false;
var ret=_17c.apply(this,arguments);
dojo.io._dispatchNextQueueBind();
return ret;
};
var _17e=_17b.error;
_17b.error=function(){
dojo.io._queueBindInFlight=false;
var ret=_17e.apply(this,arguments);
dojo.io._dispatchNextQueueBind();
return ret;
};
dojo.io._bindQueue.push(_17b);
dojo.io._dispatchNextQueueBind();
return _17b;
};
dojo.io._dispatchNextQueueBind=function(){
if(!dojo.io._queueBindInFlight){
dojo.io._queueBindInFlight=true;
dojo.io.bind(dojo.io._bindQueue.shift());
}
};
dojo.io._bindQueue=[];
dojo.io._queueBindInFlight=false;
dojo.io.argsFromMap=function(map,_181){
var _182=new Object();
var _183="";
var enc=/utf/i.test(_181||"")?encodeURIComponent:dojo.string.encodeAscii;
for(var x in map){
if(!_182[x]){
_183+=enc(x)+"="+enc(map[x])+"&";
}
}
return _183;
};
dojo.provide("dojo.dom");
dojo.require("dojo.lang");
dojo.dom.ELEMENT_NODE=1;
dojo.dom.ATTRIBUTE_NODE=2;
dojo.dom.TEXT_NODE=3;
dojo.dom.CDATA_SECTION_NODE=4;
dojo.dom.ENTITY_REFERENCE_NODE=5;
dojo.dom.ENTITY_NODE=6;
dojo.dom.PROCESSING_INSTRUCTION_NODE=7;
dojo.dom.COMMENT_NODE=8;
dojo.dom.DOCUMENT_NODE=9;
dojo.dom.DOCUMENT_TYPE_NODE=10;
dojo.dom.DOCUMENT_FRAGMENT_NODE=11;
dojo.dom.NOTATION_NODE=12;
dojo.dom.dojoml="http://www.dojotoolkit.org/2004/dojoml";
dojo.dom.xmlns={svg:"http://www.w3.org/2000/svg",smil:"http://www.w3.org/2001/SMIL20/",mml:"http://www.w3.org/1998/Math/MathML",cml:"http://www.xml-cml.org",xlink:"http://www.w3.org/1999/xlink",xhtml:"http://www.w3.org/1999/xhtml",xul:"http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",xbl:"http://www.mozilla.org/xbl",fo:"http://www.w3.org/1999/XSL/Format",xsl:"http://www.w3.org/1999/XSL/Transform",xslt:"http://www.w3.org/1999/XSL/Transform",xi:"http://www.w3.org/2001/XInclude",xforms:"http://www.w3.org/2002/01/xforms",saxon:"http://icl.com/saxon",xalan:"http://xml.apache.org/xslt",xsd:"http://www.w3.org/2001/XMLSchema",dt:"http://www.w3.org/2001/XMLSchema-datatypes",xsi:"http://www.w3.org/2001/XMLSchema-instance",rdf:"http://www.w3.org/1999/02/22-rdf-syntax-ns#",rdfs:"http://www.w3.org/2000/01/rdf-schema#",dc:"http://purl.org/dc/elements/1.1/",dcq:"http://purl.org/dc/qualifiers/1.0","soap-env":"http://schemas.xmlsoap.org/soap/envelope/",wsdl:"http://schemas.xmlsoap.org/wsdl/",AdobeExtensions:"http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/"};
dojo.dom.isNode=dojo.lang.isDomNode=function(wh){
if(typeof Element=="object"){
try{
return wh instanceof Element;
}
catch(E){
}
}else{
return wh&&!isNaN(wh.nodeType);
}
};
dojo.lang.whatAmI.custom["node"]=dojo.dom.isNode;
dojo.dom.getTagName=function(node){
var _188=node.tagName;
if(_188.substr(0,5).toLowerCase()!="dojo:"){
if(_188.substr(0,4).toLowerCase()=="dojo"){
return "dojo:"+_188.substring(4).toLowerCase();
}
var djt=node.getAttribute("dojoType")||node.getAttribute("dojotype");
if(djt){
return "dojo:"+djt.toLowerCase();
}
if((node.getAttributeNS)&&(node.getAttributeNS(this.dojoml,"type"))){
return "dojo:"+node.getAttributeNS(this.dojoml,"type").toLowerCase();
}
try{
djt=node.getAttribute("dojo:type");
}
catch(e){
}
if(djt){
return "dojo:"+djt.toLowerCase();
}
if((!dj_global["djConfig"])||(!djConfig["ignoreClassNames"])){
var _18a=node.className||node.getAttribute("class");
if((_18a)&&(_18a.indexOf)&&(_18a.indexOf("dojo-")!=-1)){
var _18b=_18a.split(" ");
for(var x=0;x<_18b.length;x++){
if((_18b[x].length>5)&&(_18b[x].indexOf("dojo-")>=0)){
return "dojo:"+_18b[x].substr(5).toLowerCase();
}
}
}
}
}
return _188.toLowerCase();
};
dojo.dom.getUniqueId=function(){
do{
var id="dj_unique_"+(++arguments.callee._idIncrement);
}while(document.getElementById(id));
return id;
};
dojo.dom.getUniqueId._idIncrement=0;
dojo.dom.firstElement=dojo.dom.getFirstChildElement=function(_18e,_18f){
var node=_18e.firstChild;
while(node&&node.nodeType!=dojo.dom.ELEMENT_NODE){
node=node.nextSibling;
}
if(_18f&&node&&node.tagName&&node.tagName.toLowerCase()!=_18f.toLowerCase()){
node=dojo.dom.nextElement(node,_18f);
}
return node;
};
dojo.dom.lastElement=dojo.dom.getLastChildElement=function(_191,_192){
var node=_191.lastChild;
while(node&&node.nodeType!=dojo.dom.ELEMENT_NODE){
node=node.previousSibling;
}
if(_192&&node&&node.tagName&&node.tagName.toLowerCase()!=_192.toLowerCase()){
node=dojo.dom.prevElement(node,_192);
}
return node;
};
dojo.dom.nextElement=dojo.dom.getNextSiblingElement=function(node,_195){
if(!node){
return null;
}
do{
node=node.nextSibling;
}while(node&&node.nodeType!=dojo.dom.ELEMENT_NODE);
if(node&&_195&&_195.toLowerCase()!=node.tagName.toLowerCase()){
return dojo.dom.nextElement(node,_195);
}
return node;
};
dojo.dom.prevElement=dojo.dom.getPreviousSiblingElement=function(node,_197){
if(!node){
return null;
}
if(_197){
_197=_197.toLowerCase();
}
do{
node=node.previousSibling;
}while(node&&node.nodeType!=dojo.dom.ELEMENT_NODE);
if(node&&_197&&_197.toLowerCase()!=node.tagName.toLowerCase()){
return dojo.dom.prevElement(node,_197);
}
return node;
};
dojo.dom.moveChildren=function(_198,_199,trim){
var _19b=0;
if(trim){
while(_198.hasChildNodes()&&_198.firstChild.nodeType==dojo.dom.TEXT_NODE){
_198.removeChild(_198.firstChild);
}
while(_198.hasChildNodes()&&_198.lastChild.nodeType==dojo.dom.TEXT_NODE){
_198.removeChild(_198.lastChild);
}
}
while(_198.hasChildNodes()){
_199.appendChild(_198.firstChild);
_19b++;
}
return _19b;
};
dojo.dom.copyChildren=function(_19c,_19d,trim){
var _19f=_19c.cloneNode(true);
return this.moveChildren(_19f,_19d,trim);
};
dojo.dom.removeChildren=function(node){
var _1a1=node.childNodes.length;
while(node.hasChildNodes()){
node.removeChild(node.firstChild);
}
return _1a1;
};
dojo.dom.replaceChildren=function(node,_1a3){
dojo.dom.removeChildren(node);
node.appendChild(_1a3);
};
dojo.dom.removeNode=function(node){
if(node&&node.parentNode){
return node.parentNode.removeChild(node);
}
};
dojo.dom.getAncestors=function(node,_1a6,_1a7){
var _1a8=[];
var _1a9=dojo.lang.isFunction(_1a6);
while(node){
if(!_1a9||_1a6(node)){
_1a8.push(node);
}
if(_1a7&&_1a8.length>0){
return _1a8[0];
}
node=node.parentNode;
}
if(_1a7){
return null;
}
return _1a8;
};
dojo.dom.getAncestorsByTag=function(node,tag,_1ac){
tag=tag.toLowerCase();
return dojo.dom.getAncestors(node,function(el){
return ((el.tagName)&&(el.tagName.toLowerCase()==tag));
},_1ac);
};
dojo.dom.getFirstAncestorByTag=function(node,tag){
return dojo.dom.getAncestorsByTag(node,tag,true);
};
dojo.dom.isDescendantOf=function(node,_1b1,_1b2){
if(_1b2&&node){
node=node.parentNode;
}
while(node){
if(node==_1b1){
return true;
}
node=node.parentNode;
}
return false;
};
dojo.dom.innerXML=function(node){
if(node.innerXML){
return node.innerXML;
}else{
if(typeof XMLSerializer!="undefined"){
return (new XMLSerializer()).serializeToString(node);
}
}
};
dojo.dom.createDocumentFromText=function(str,_1b5){
if(!_1b5){
_1b5="text/xml";
}
if(typeof DOMParser!="undefined"){
var _1b6=new DOMParser();
return _1b6.parseFromString(str,_1b5);
}else{
if(typeof ActiveXObject!="undefined"){
var _1b7=new ActiveXObject("Microsoft.XMLDOM");
if(_1b7){
_1b7.async=false;
_1b7.loadXML(str);
return _1b7;
}else{
dojo.debug("toXml didn't work?");
}
}else{
if(document.createElement){
var tmp=document.createElement("xml");
tmp.innerHTML=str;
if(document.implementation&&document.implementation.createDocument){
var _1b9=document.implementation.createDocument("foo","",null);
for(var i=0;i<tmp.childNodes.length;i++){
_1b9.importNode(tmp.childNodes.item(i),true);
}
return _1b9;
}
return tmp.document&&tmp.document.firstChild?tmp.document.firstChild:tmp;
}
}
}
return null;
};
dojo.dom.prependChild=function(node,_1bc){
if(_1bc.firstChild){
_1bc.insertBefore(node,_1bc.firstChild);
}else{
_1bc.appendChild(node);
}
return true;
};
dojo.dom.insertBefore=function(node,ref,_1bf){
if(_1bf!=true&&(node===ref||node.nextSibling===ref)){
return false;
}
var _1c0=ref.parentNode;
_1c0.insertBefore(node,ref);
return true;
};
dojo.dom.insertAfter=function(node,ref,_1c3){
var pn=ref.parentNode;
if(ref==pn.lastChild){
if((_1c3!=true)&&(node===ref)){
return false;
}
pn.appendChild(node);
}else{
return this.insertBefore(node,ref.nextSibling,_1c3);
}
return true;
};
dojo.dom.insertAtPosition=function(node,ref,_1c7){
if((!node)||(!ref)||(!_1c7)){
return false;
}
switch(_1c7.toLowerCase()){
case "before":
return dojo.dom.insertBefore(node,ref);
case "after":
return dojo.dom.insertAfter(node,ref);
case "first":
if(ref.firstChild){
return dojo.dom.insertBefore(node,ref.firstChild);
}else{
ref.appendChild(node);
return true;
}
break;
default:
ref.appendChild(node);
return true;
}
};
dojo.dom.insertAtIndex=function(node,_1c9,_1ca){
var _1cb=_1c9.childNodes;
if(!_1cb.length){
_1c9.appendChild(node);
return true;
}
var _1cc=null;
for(var i=0;i<_1cb.length;i++){
var _1ce=_1cb.item(i)["getAttribute"]?parseInt(_1cb.item(i).getAttribute("dojoinsertionindex")):-1;
if(_1ce<_1ca){
_1cc=_1cb.item(i);
}
}
if(_1cc){
return dojo.dom.insertAfter(node,_1cc);
}else{
return dojo.dom.insertBefore(node,_1cb.item(0));
}
};
dojo.dom.textContent=function(node,text){
if(text){
dojo.dom.replaceChildren(node,document.createTextNode(text));
return text;
}else{
var _1d1="";
if(node==null){
return _1d1;
}
for(var i=0;i<node.childNodes.length;i++){
switch(node.childNodes[i].nodeType){
case 1:
case 5:
_1d1+=dojo.dom.textContent(node.childNodes[i]);
break;
case 3:
case 2:
case 4:
_1d1+=node.childNodes[i].nodeValue;
break;
default:
break;
}
}
return _1d1;
}
};
dojo.dom.collectionToArray=function(_1d3){
dojo.deprecated("dojo.dom.collectionToArray","use dojo.lang.toArray instead");
return dojo.lang.toArray(_1d3);
};
dojo.dom.hasParent=function(node){
if(!node||!node.parentNode||(node.parentNode&&!node.parentNode.tagName)){
return false;
}
return true;
};
dojo.dom.isTag=function(node){
if(node&&node.tagName){
var arr=dojo.lang.toArray(arguments,1);
return arr[dojo.lang.find(node.tagName,arr)]||"";
}
return "";
};
dojo.provide("dojo.io.BrowserIO");
dojo.require("dojo.io");
dojo.require("dojo.lang");
dojo.require("dojo.dom");
try{
if((!djConfig["preventBackButtonFix"])&&(!dojo.hostenv.post_load_)){
document.write("<iframe style='border: 0px; width: 1px; height: 1px; position: absolute; bottom: 0px; right: 0px; visibility: visible;' name='djhistory' id='djhistory' src='"+(dojo.hostenv.getBaseScriptUri()+"iframe_history.html")+"'></iframe>");
}
}
catch(e){
}
dojo.io.checkChildrenForFile=function(node){
var _1d8=false;
var _1d9=node.getElementsByTagName("input");
dojo.lang.forEach(_1d9,function(_1da){
if(_1d8){
return;
}
if(_1da.getAttribute("type")=="file"){
_1d8=true;
}
});
return _1d8;
};
dojo.io.formHasFile=function(_1db){
return dojo.io.checkChildrenForFile(_1db);
};
dojo.io.encodeForm=function(_1dc,_1dd){
if((!_1dc)||(!_1dc.tagName)||(!_1dc.tagName.toLowerCase()=="form")){
dojo.raise("Attempted to encode a non-form element.");
}
var enc=/utf/i.test(_1dd||"")?encodeURIComponent:dojo.string.encodeAscii;
var _1df=[];
for(var i=0;i<_1dc.elements.length;i++){
var elm=_1dc.elements[i];
if(elm.disabled||elm.tagName.toLowerCase()=="fieldset"||!elm.name){
continue;
}
var name=enc(elm.name);
var type=elm.type.toLowerCase();
if(type=="select-multiple"){
for(var j=0;j<elm.options.length;j++){
if(elm.options[j].selected){
_1df.push(name+"="+enc(elm.options[j].value));
}
}
}else{
if(dojo.lang.inArray(type,["radio","checkbox"])){
if(elm.checked){
_1df.push(name+"="+enc(elm.value));
}
}else{
if(!dojo.lang.inArray(type,["file","submit","reset","button"])){
_1df.push(name+"="+enc(elm.value));
}
}
}
}
var _1e5=_1dc.getElementsByTagName("input");
for(var i=0;i<_1e5.length;i++){
var _1e6=_1e5[i];
if(_1e6.type.toLowerCase()=="image"&&_1e6.form==_1dc){
var name=enc(_1e6.name);
_1df.push(name+"="+enc(_1e6.value));
_1df.push(name+".x=0");
_1df.push(name+".y=0");
}
}
return _1df.join("&")+"&";
};
dojo.io.setIFrameSrc=function(_1e7,src,_1e9){
try{
var r=dojo.render.html;
if(!_1e9){
if(r.safari){
_1e7.location=src;
}else{
frames[_1e7.name].location=src;
}
}else{
var idoc;
if(r.ie){
idoc=_1e7.contentWindow.document;
}else{
if(r.moz){
idoc=_1e7.contentWindow;
}else{
if(r.safari){
idoc=_1e7.document;
}
}
}
idoc.location.replace(src);
}
}
catch(e){
dojo.debug(e);
dojo.debug("setIFrameSrc: "+e);
}
};
dojo.io.XMLHTTPTransport=new function(){
var _1ec=this;
this.initialHref=window.location.href;
this.initialHash=window.location.hash;
this.moveForward=false;
var _1ed={};
this.useCache=false;
this.preventCache=false;
this.historyStack=[];
this.forwardStack=[];
this.historyIframe=null;
this.bookmarkAnchor=null;
this.locationTimer=null;
function getCacheKey(url,_1ef,_1f0){
return url+"|"+_1ef+"|"+_1f0.toLowerCase();
}
function addToCache(url,_1f2,_1f3,http){
_1ed[getCacheKey(url,_1f2,_1f3)]=http;
}
function getFromCache(url,_1f6,_1f7){
return _1ed[getCacheKey(url,_1f6,_1f7)];
}
this.clearCache=function(){
_1ed={};
};
function doLoad(_1f8,http,url,_1fb,_1fc){
if((http.status==200)||(location.protocol=="file:"&&http.status==0)){
var ret;
if(_1f8.method.toLowerCase()=="head"){
var _1fe=http.getAllResponseHeaders();
ret={};
ret.toString=function(){
return _1fe;
};
var _1ff=_1fe.split(/[\r\n]+/g);
for(var i=0;i<_1ff.length;i++){
var pair=_1ff[i].match(/^([^:]+)\s*:\s*(.+)$/i);
if(pair){
ret[pair[1]]=pair[2];
}
}
}else{
if(_1f8.mimetype=="text/javascript"){
try{
ret=dj_eval(http.responseText);
}
catch(e){
dojo.debug(e);
dojo.debug(http.responseText);
ret=null;
}
}else{
if(_1f8.mimetype=="text/json"){
try{
ret=dj_eval("("+http.responseText+")");
}
catch(e){
dojo.debug(e);
dojo.debug(http.responseText);
ret=false;
}
}else{
if((_1f8.mimetype=="application/xml")||(_1f8.mimetype=="text/xml")){
ret=http.responseXML;
if(!ret||typeof ret=="string"){
ret=dojo.dom.createDocumentFromText(http.responseText);
}
}else{
ret=http.responseText;
}
}
}
}
if(_1fc){
addToCache(url,_1fb,_1f8.method,http);
}
_1f8[(typeof _1f8.load=="function")?"load":"handle"]("load",ret,http);
}else{
var _202=new dojo.io.Error("XMLHttpTransport Error: "+http.status+" "+http.statusText);
_1f8[(typeof _1f8.error=="function")?"error":"handle"]("error",_202,http);
}
}
function setHeaders(http,_204){
if(_204["headers"]){
for(var _205 in _204["headers"]){
if(_205.toLowerCase()=="content-type"&&!_204["contentType"]){
_204["contentType"]=_204["headers"][_205];
}else{
http.setRequestHeader(_205,_204["headers"][_205]);
}
}
}
}
this.addToHistory=function(args){
var _207=args["back"]||args["backButton"]||args["handle"];
var hash=null;
if(!this.historyIframe){
this.historyIframe=window.frames["djhistory"];
}
if(!this.bookmarkAnchor){
this.bookmarkAnchor=document.createElement("a");
(document.body||document.getElementsByTagName("body")[0]).appendChild(this.bookmarkAnchor);
this.bookmarkAnchor.style.display="none";
}
if((!args["changeUrl"])||(dojo.render.html.ie)){
var url=dojo.hostenv.getBaseScriptUri()+"iframe_history.html?"+(new Date()).getTime();
this.moveForward=true;
dojo.io.setIFrameSrc(this.historyIframe,url,false);
}
if(args["changeUrl"]){
hash="#"+((args["changeUrl"]!==true)?args["changeUrl"]:(new Date()).getTime());
setTimeout("window.location.href = '"+hash+"';",1);
this.bookmarkAnchor.href=hash;
if(dojo.render.html.ie){
var _20a=_207;
var lh=null;
var hsl=this.historyStack.length-1;
if(hsl>=0){
while(!this.historyStack[hsl]["urlHash"]){
hsl--;
}
lh=this.historyStack[hsl]["urlHash"];
}
if(lh){
_207=function(){
if(window.location.hash!=""){
setTimeout("window.location.href = '"+lh+"';",1);
}
_20a();
};
}
this.forwardStack=[];
var _20d=args["forward"]||args["forwardButton"];
var tfw=function(){
if(window.location.hash!=""){
window.location.href=hash;
}
if(_20d){
_20d();
}
};
if(args["forward"]){
args.forward=tfw;
}else{
if(args["forwardButton"]){
args.forwardButton=tfw;
}
}
}else{
if(dojo.render.html.moz){
if(!this.locationTimer){
this.locationTimer=setInterval("dojo.io.XMLHTTPTransport.checkLocation();",200);
}
}
}
}
this.historyStack.push({"url":url,"callback":_207,"kwArgs":args,"urlHash":hash});
};
this.checkLocation=function(){
var hsl=this.historyStack.length;
if((window.location.hash==this.initialHash)||(window.location.href==this.initialHref)&&(hsl==1)){
this.handleBackButton();
return;
}
if(this.forwardStack.length>0){
if(this.forwardStack[this.forwardStack.length-1].urlHash==window.location.hash){
this.handleForwardButton();
return;
}
}
if((hsl>=2)&&(this.historyStack[hsl-2])){
if(this.historyStack[hsl-2].urlHash==window.location.hash){
this.handleBackButton();
return;
}
}
};
this.iframeLoaded=function(evt,_211){
var isp=_211.href.split("?");
if(isp.length<2){
if(this.historyStack.length==1){
this.handleBackButton();
}
return;
}
var _213=isp[1];
if(this.moveForward){
this.moveForward=false;
return;
}
var last=this.historyStack.pop();
if(!last){
if(this.forwardStack.length>0){
var next=this.forwardStack[this.forwardStack.length-1];
if(_213==next.url.split("?")[1]){
this.handleForwardButton();
}
}
return;
}
this.historyStack.push(last);
if(this.historyStack.length>=2){
if(isp[1]==this.historyStack[this.historyStack.length-2].url.split("?")[1]){
this.handleBackButton();
}
}else{
this.handleBackButton();
}
};
this.handleBackButton=function(){
var last=this.historyStack.pop();
if(!last){
return;
}
if(last["callback"]){
last.callback();
}else{
if(last.kwArgs["backButton"]){
last.kwArgs["backButton"]();
}else{
if(last.kwArgs["back"]){
last.kwArgs["back"]();
}else{
if(last.kwArgs["handle"]){
last.kwArgs.handle("back");
}
}
}
}
this.forwardStack.push(last);
};
this.handleForwardButton=function(){
var last=this.forwardStack.pop();
if(!last){
return;
}
if(last.kwArgs["forward"]){
last.kwArgs.forward();
}else{
if(last.kwArgs["forwardButton"]){
last.kwArgs.forwardButton();
}else{
if(last.kwArgs["handle"]){
last.kwArgs.handle("forward");
}
}
}
this.historyStack.push(last);
};
this.inFlight=[];
this.inFlightTimer=null;
this.startWatchingInFlight=function(){
if(!this.inFlightTimer){
this.inFlightTimer=setInterval("dojo.io.XMLHTTPTransport.watchInFlight();",10);
}
};
this.watchInFlight=function(){
for(var x=this.inFlight.length-1;x>=0;x--){
var tif=this.inFlight[x];
if(!tif){
this.inFlight.splice(x,1);
continue;
}
if(4==tif.http.readyState){
this.inFlight.splice(x,1);
doLoad(tif.req,tif.http,tif.url,tif.query,tif.useCache);
if(this.inFlight.length==0){
clearInterval(this.inFlightTimer);
this.inFlightTimer=null;
}
}
}
};
var _21a=dojo.hostenv.getXmlhttpObject()?true:false;
this.canHandle=function(_21b){
return _21a&&dojo.lang.inArray((_21b["mimetype"]||"".toLowerCase()),["text/plain","text/html","application/xml","text/xml","text/javascript","text/json"])&&dojo.lang.inArray(_21b["method"].toLowerCase(),["post","get","head"])&&!(_21b["formNode"]&&dojo.io.formHasFile(_21b["formNode"]));
};
this.multipartBoundary="45309FFF-BD65-4d50-99C9-36986896A96F";
this.bind=function(_21c){
if(!_21c["url"]){
if(!_21c["formNode"]&&(_21c["backButton"]||_21c["back"]||_21c["changeUrl"]||_21c["watchForURL"])&&(!djConfig.preventBackButtonFix)){
this.addToHistory(_21c);
return true;
}
}
var url=_21c.url;
var _21e="";
if(_21c["formNode"]){
var ta=_21c.formNode.getAttribute("action");
if((ta)&&(!_21c["url"])){
url=ta;
}
var tp=_21c.formNode.getAttribute("method");
if((tp)&&(!_21c["method"])){
_21c.method=tp;
}
_21e+=dojo.io.encodeForm(_21c.formNode,_21c.encoding);
}
if(url.indexOf("#")>-1){
dojo.debug("Warning: dojo.io.bind: stripping hash values from url:",url);
url=url.split("#")[0];
}
if(_21c["file"]){
_21c.method="post";
}
if(!_21c["method"]){
_21c.method="get";
}
if(_21c.method.toLowerCase()=="get"){
_21c.multipart=false;
}else{
if(_21c["file"]){
_21c.multipart=true;
}else{
if(!_21c["multipart"]){
_21c.multipart=false;
}
}
}
if(_21c["backButton"]||_21c["back"]||_21c["changeUrl"]){
this.addToHistory(_21c);
}
var _221=_21c["content"]||{};
if(_21c.sendTransport){
_221["dojo.transport"]="xmlhttp";
}
do{
if(_21c.postContent){
_21e=_21c.postContent;
break;
}
if(_221){
_21e+=dojo.io.argsFromMap(_221,_21c.encoding);
}
if(_21c.method.toLowerCase()=="get"||!_21c.multipart){
break;
}
var t=[];
if(_21e.length){
var q=_21e.split("&");
for(var i=0;i<q.length;++i){
if(q[i].length){
var p=q[i].split("=");
t.push("--"+this.multipartBoundary,"Content-Disposition: form-data; name=\""+p[0]+"\"","",p[1]);
}
}
}
if(_21c.file){
if(dojo.lang.isArray(_21c.file)){
for(var i=0;i<_21c.file.length;++i){
var o=_21c.file[i];
t.push("--"+this.multipartBoundary,"Content-Disposition: form-data; name=\""+o.name+"\"; filename=\""+("fileName" in o?o.fileName:o.name)+"\"","Content-Type: "+("contentType" in o?o.contentType:"application/octet-stream"),"",o.content);
}
}else{
var o=_21c.file;
t.push("--"+this.multipartBoundary,"Content-Disposition: form-data; name=\""+o.name+"\"; filename=\""+("fileName" in o?o.fileName:o.name)+"\"","Content-Type: "+("contentType" in o?o.contentType:"application/octet-stream"),"",o.content);
}
}
if(t.length){
t.push("--"+this.multipartBoundary+"--","");
_21e=t.join("\r\n");
}
}while(false);
var _227=_21c["sync"]?false:true;
var _228=_21c["preventCache"]||(this.preventCache==true&&_21c["preventCache"]!=false);
var _229=_21c["useCache"]==true||(this.useCache==true&&_21c["useCache"]!=false);
if(!_228&&_229){
var _22a=getFromCache(url,_21e,_21c.method);
if(_22a){
doLoad(_21c,_22a,url,_21e,false);
return;
}
}
var http=dojo.hostenv.getXmlhttpObject();
var _22c=false;
if(_227){
this.inFlight.push({"req":_21c,"http":http,"url":url,"query":_21e,"useCache":_229});
this.startWatchingInFlight();
}
if(_21c.method.toLowerCase()=="post"){
http.open("POST",url,_227);
setHeaders(http,_21c);
http.setRequestHeader("Content-Type",_21c.multipart?("multipart/form-data; boundary="+this.multipartBoundary):(_21c.contentType||"application/x-www-form-urlencoded"));
http.send(_21e);
}else{
var _22d=url;
if(_21e!=""){
_22d+=(_22d.indexOf("?")>-1?"&":"?")+_21e;
}
if(_228){
_22d+=(dojo.string.endsWithAny(_22d,"?","&")?"":(_22d.indexOf("?")>-1?"&":"?"))+"dojo.preventCache="+new Date().valueOf();
}
http.open(_21c.method.toUpperCase(),_22d,_227);
setHeaders(http,_21c);
http.send(null);
}
if(!_227){
doLoad(_21c,http,url,_21e,_229);
}
_21c.abort=function(){
return http.abort();
};
return;
};
dojo.io.transports.addTransport("XMLHTTPTransport");
};
dojo.require("dojo.lang");
dojo.provide("dojo.event");
dojo.event=new function(){
this.canTimeout=dojo.lang.isFunction(dj_global["setTimeout"])||dojo.lang.isAlien(dj_global["setTimeout"]);
function interpolateArgs(args){
var dl=dojo.lang;
var ao={srcObj:dj_global,srcFunc:null,adviceObj:dj_global,adviceFunc:null,aroundObj:null,aroundFunc:null,adviceType:(args.length>2)?args[0]:"after",precedence:"last",once:false,delay:null,rate:0,adviceMsg:false};
switch(args.length){
case 0:
return;
case 1:
return;
case 2:
ao.srcFunc=args[0];
ao.adviceFunc=args[1];
break;
case 3:
if((dl.isObject(args[0]))&&(dl.isString(args[1]))&&(dl.isString(args[2]))){
ao.adviceType="after";
ao.srcObj=args[0];
ao.srcFunc=args[1];
ao.adviceFunc=args[2];
}else{
if((dl.isString(args[1]))&&(dl.isString(args[2]))){
ao.srcFunc=args[1];
ao.adviceFunc=args[2];
}else{
if((dl.isObject(args[0]))&&(dl.isString(args[1]))&&(dl.isFunction(args[2]))){
ao.adviceType="after";
ao.srcObj=args[0];
ao.srcFunc=args[1];
var _231=dojo.lang.nameAnonFunc(args[2],ao.adviceObj);
ao.adviceFunc=_231;
}else{
if((dl.isFunction(args[0]))&&(dl.isObject(args[1]))&&(dl.isString(args[2]))){
ao.adviceType="after";
ao.srcObj=dj_global;
var _231=dojo.lang.nameAnonFunc(args[0],ao.srcObj);
ao.srcFunc=_231;
ao.adviceObj=args[1];
ao.adviceFunc=args[2];
}
}
}
}
break;
case 4:
if((dl.isObject(args[0]))&&(dl.isObject(args[2]))){
ao.adviceType="after";
ao.srcObj=args[0];
ao.srcFunc=args[1];
ao.adviceObj=args[2];
ao.adviceFunc=args[3];
}else{
if((dl.isString(args[0]))&&(dl.isString(args[1]))&&(dl.isObject(args[2]))){
ao.adviceType=args[0];
ao.srcObj=dj_global;
ao.srcFunc=args[1];
ao.adviceObj=args[2];
ao.adviceFunc=args[3];
}else{
if((dl.isString(args[0]))&&(dl.isFunction(args[1]))&&(dl.isObject(args[2]))){
ao.adviceType=args[0];
ao.srcObj=dj_global;
var _231=dojo.lang.nameAnonFunc(args[1],dj_global);
ao.srcFunc=_231;
ao.adviceObj=args[2];
ao.adviceFunc=args[3];
}else{
if(dl.isObject(args[1])){
ao.srcObj=args[1];
ao.srcFunc=args[2];
ao.adviceObj=dj_global;
ao.adviceFunc=args[3];
}else{
if(dl.isObject(args[2])){
ao.srcObj=dj_global;
ao.srcFunc=args[1];
ao.adviceObj=args[2];
ao.adviceFunc=args[3];
}else{
ao.srcObj=ao.adviceObj=ao.aroundObj=dj_global;
ao.srcFunc=args[1];
ao.adviceFunc=args[2];
ao.aroundFunc=args[3];
}
}
}
}
}
break;
case 6:
ao.srcObj=args[1];
ao.srcFunc=args[2];
ao.adviceObj=args[3];
ao.adviceFunc=args[4];
ao.aroundFunc=args[5];
ao.aroundObj=dj_global;
break;
default:
ao.srcObj=args[1];
ao.srcFunc=args[2];
ao.adviceObj=args[3];
ao.adviceFunc=args[4];
ao.aroundObj=args[5];
ao.aroundFunc=args[6];
ao.once=args[7];
ao.delay=args[8];
ao.rate=args[9];
ao.adviceMsg=args[10];
break;
}
if((typeof ao.srcFunc).toLowerCase()!="string"){
ao.srcFunc=dojo.lang.getNameInObj(ao.srcObj,ao.srcFunc);
}
if((typeof ao.adviceFunc).toLowerCase()!="string"){
ao.adviceFunc=dojo.lang.getNameInObj(ao.adviceObj,ao.adviceFunc);
}
if((ao.aroundObj)&&((typeof ao.aroundFunc).toLowerCase()!="string")){
ao.aroundFunc=dojo.lang.getNameInObj(ao.aroundObj,ao.aroundFunc);
}
if(!ao.srcObj){
dojo.raise("bad srcObj for srcFunc: "+ao.srcFunc);
}
if(!ao.adviceObj){
dojo.raise("bad adviceObj for adviceFunc: "+ao.adviceFunc);
}
return ao;
}
this.connect=function(){
var ao=interpolateArgs(arguments);
var mjp=dojo.event.MethodJoinPoint.getForMethod(ao.srcObj,ao.srcFunc);
if(ao.adviceFunc){
var mjp2=dojo.event.MethodJoinPoint.getForMethod(ao.adviceObj,ao.adviceFunc);
}
mjp.kwAddAdvice(ao);
return mjp;
};
this.connectBefore=function(){
var args=["before"];
for(var i=0;i<arguments.length;i++){
args.push(arguments[i]);
}
return this.connect.apply(this,args);
};
this.connectAround=function(){
var args=["around"];
for(var i=0;i<arguments.length;i++){
args.push(arguments[i]);
}
return this.connect.apply(this,args);
};
this._kwConnectImpl=function(_239,_23a){
var fn=(_23a)?"disconnect":"connect";
if(typeof _239["srcFunc"]=="function"){
_239.srcObj=_239["srcObj"]||dj_global;
var _23c=dojo.lang.nameAnonFunc(_239.srcFunc,_239.srcObj);
_239.srcFunc=_23c;
}
if(typeof _239["adviceFunc"]=="function"){
_239.adviceObj=_239["adviceObj"]||dj_global;
var _23c=dojo.lang.nameAnonFunc(_239.adviceFunc,_239.adviceObj);
_239.adviceFunc=_23c;
}
return dojo.event[fn]((_239["type"]||_239["adviceType"]||"after"),_239["srcObj"]||dj_global,_239["srcFunc"],_239["adviceObj"]||_239["targetObj"]||dj_global,_239["adviceFunc"]||_239["targetFunc"],_239["aroundObj"],_239["aroundFunc"],_239["once"],_239["delay"],_239["rate"],_239["adviceMsg"]||false);
};
this.kwConnect=function(_23d){
return this._kwConnectImpl(_23d,false);
};
this.disconnect=function(){
var ao=interpolateArgs(arguments);
if(!ao.adviceFunc){
return;
}
var mjp=dojo.event.MethodJoinPoint.getForMethod(ao.srcObj,ao.srcFunc);
return mjp.removeAdvice(ao.adviceObj,ao.adviceFunc,ao.adviceType,ao.once);
};
this.kwDisconnect=function(_240){
return this._kwConnectImpl(_240,true);
};
};
dojo.event.MethodInvocation=function(_241,obj,args){
this.jp_=_241;
this.object=obj;
this.args=[];
for(var x=0;x<args.length;x++){
this.args[x]=args[x];
}
this.around_index=-1;
};
dojo.event.MethodInvocation.prototype.proceed=function(){
this.around_index++;
if(this.around_index>=this.jp_.around.length){
return this.jp_.object[this.jp_.methodname].apply(this.jp_.object,this.args);
}else{
var ti=this.jp_.around[this.around_index];
var mobj=ti[0]||dj_global;
var meth=ti[1];
return mobj[meth].call(mobj,this);
}
};
dojo.event.MethodJoinPoint=function(obj,_249){
this.object=obj||dj_global;
this.methodname=_249;
this.methodfunc=this.object[_249];
this.before=[];
this.after=[];
this.around=[];
};
dojo.event.MethodJoinPoint.getForMethod=function(obj,_24b){
if(!obj){
obj=dj_global;
}
if(!obj[_24b]){
obj[_24b]=function(){
};
}else{
if((!dojo.lang.isFunction(obj[_24b]))&&(!dojo.lang.isAlien(obj[_24b]))){
return null;
}
}
var _24c=_24b+"$joinpoint";
var _24d=_24b+"$joinpoint$method";
var _24e=obj[_24c];
if(!_24e){
var _24f=false;
if(dojo.event["browser"]){
if((obj["attachEvent"])||(obj["nodeType"])||(obj["addEventListener"])){
_24f=true;
dojo.event.browser.addClobberNodeAttrs(obj,[_24c,_24d,_24b]);
}
}
obj[_24d]=obj[_24b];
_24e=obj[_24c]=new dojo.event.MethodJoinPoint(obj,_24d);
obj[_24b]=function(){
var args=[];
if((_24f)&&(!arguments.length)&&(window.event)){
args.push(dojo.event.browser.fixEvent(window.event));
}else{
for(var x=0;x<arguments.length;x++){
if((x==0)&&(_24f)&&(dojo.event.browser.isEvent(arguments[x]))){
args.push(dojo.event.browser.fixEvent(arguments[x]));
}else{
args.push(arguments[x]);
}
}
}
return _24e.run.apply(_24e,args);
};
}
return _24e;
};
dojo.lang.extend(dojo.event.MethodJoinPoint,{unintercept:function(){
this.object[this.methodname]=this.methodfunc;
},run:function(){
var obj=this.object||dj_global;
var args=arguments;
var _254=[];
for(var x=0;x<args.length;x++){
_254[x]=args[x];
}
var _256=function(marr){
if(!marr){
dojo.debug("Null argument to unrollAdvice()");
return;
}
var _258=marr[0]||dj_global;
var _259=marr[1];
if(!_258[_259]){
dojo.raise("function \""+_259+"\" does not exist on \""+_258+"\"");
}
var _25a=marr[2]||dj_global;
var _25b=marr[3];
var msg=marr[6];
var _25d;
var to={args:[],jp_:this,object:obj,proceed:function(){
return _258[_259].apply(_258,to.args);
}};
to.args=_254;
var _25f=parseInt(marr[4]);
var _260=((!isNaN(_25f))&&(marr[4]!==null)&&(typeof marr[4]!="undefined"));
if(marr[5]){
var rate=parseInt(marr[5]);
var cur=new Date();
var _263=false;
if((marr["last"])&&((cur-marr.last)<=rate)){
if(dojo.event.canTimeout){
if(marr["delayTimer"]){
clearTimeout(marr.delayTimer);
}
var tod=parseInt(rate*2);
var mcpy=dojo.lang.shallowCopy(marr);
marr.delayTimer=setTimeout(function(){
mcpy[5]=0;
_256(mcpy);
},tod);
}
return;
}else{
marr.last=cur;
}
}
if(_25b){
_25a[_25b].call(_25a,to);
}else{
if((_260)&&((dojo.render.html)||(dojo.render.svg))){
dj_global["setTimeout"](function(){
if(msg){
_258[_259].call(_258,to);
}else{
_258[_259].apply(_258,args);
}
},_25f);
}else{
if(msg){
_258[_259].call(_258,to);
}else{
_258[_259].apply(_258,args);
}
}
}
};
if(this.before.length>0){
dojo.lang.forEach(this.before,_256,true);
}
var _266;
if(this.around.length>0){
var mi=new dojo.event.MethodInvocation(this,obj,args);
_266=mi.proceed();
}else{
if(this.methodfunc){
_266=this.object[this.methodname].apply(this.object,args);
}
}
if(this.after.length>0){
dojo.lang.forEach(this.after,_256,true);
}
return (this.methodfunc)?_266:null;
},getArr:function(kind){
var arr=this.after;
if((typeof kind=="string")&&(kind.indexOf("before")!=-1)){
arr=this.before;
}else{
if(kind=="around"){
arr=this.around;
}
}
return arr;
},kwAddAdvice:function(args){
this.addAdvice(args["adviceObj"],args["adviceFunc"],args["aroundObj"],args["aroundFunc"],args["adviceType"],args["precedence"],args["once"],args["delay"],args["rate"],args["adviceMsg"]);
},addAdvice:function(_26b,_26c,_26d,_26e,_26f,_270,once,_272,rate,_274){
var arr=this.getArr(_26f);
if(!arr){
dojo.raise("bad this: "+this);
}
var ao=[_26b,_26c,_26d,_26e,_272,rate,_274];
if(once){
if(this.hasAdvice(_26b,_26c,_26f,arr)>=0){
return;
}
}
if(_270=="first"){
arr.unshift(ao);
}else{
arr.push(ao);
}
},hasAdvice:function(_277,_278,_279,arr){
if(!arr){
arr=this.getArr(_279);
}
var ind=-1;
for(var x=0;x<arr.length;x++){
if((arr[x][0]==_277)&&(arr[x][1]==_278)){
ind=x;
}
}
return ind;
},removeAdvice:function(_27d,_27e,_27f,once){
var arr=this.getArr(_27f);
var ind=this.hasAdvice(_27d,_27e,_27f,arr);
if(ind==-1){
return false;
}
while(ind!=-1){
arr.splice(ind,1);
if(once){
break;
}
ind=this.hasAdvice(_27d,_27e,_27f,arr);
}
return true;
}});
dojo.require("dojo.event");
dojo.provide("dojo.event.topic");
dojo.event.topic=new function(){
this.topics={};
this.getTopic=function(_283){
if(!this.topics[_283]){
this.topics[_283]=new this.TopicImpl(_283);
}
return this.topics[_283];
};
this.registerPublisher=function(_284,obj,_286){
var _284=this.getTopic(_284);
_284.registerPublisher(obj,_286);
};
this.subscribe=function(_287,obj,_289){
var _287=this.getTopic(_287);
_287.subscribe(obj,_289);
};
this.unsubscribe=function(_28a,obj,_28c){
var _28a=this.getTopic(_28a);
_28a.unsubscribe(obj,_28c);
};
this.publish=function(_28d,_28e){
var _28d=this.getTopic(_28d);
var args=[];
if((arguments.length==2)&&(_28e.length)&&(typeof _28e!="string")){
args=_28e;
}else{
var args=[];
for(var x=1;x<arguments.length;x++){
args.push(arguments[x]);
}
}
_28d.sendMessage.apply(_28d,args);
};
};
dojo.event.topic.TopicImpl=function(_291){
this.topicName=_291;
var self=this;
self.subscribe=function(_293,_294){
var tf=_294||_293;
var to=(!_294)?dj_global:_293;
dojo.event.kwConnect({srcObj:self,srcFunc:"sendMessage",adviceObj:to,adviceFunc:tf});
};
self.unsubscribe=function(_297,_298){
var tf=(!_298)?_297:_298;
var to=(!_298)?null:_297;
dojo.event.kwDisconnect({srcObj:self,srcFunc:"sendMessage",adviceObj:to,adviceFunc:tf});
};
self.registerPublisher=function(_29b,_29c){
dojo.event.connect(_29b,_29c,self,"sendMessage");
};
self.sendMessage=function(_29d){
};
};
dojo.provide("dojo.event.browser");
dojo.require("dojo.event");
dojo_ie_clobber=new function(){
this.clobberNodes=[];
function nukeProp(node,prop){
try{
node[prop]=null;
}
catch(e){
}
try{
delete node[prop];
}
catch(e){
}
try{
node.removeAttribute(prop);
}
catch(e){
}
}
this.clobber=function(_2a0){
var na;
var tna;
if(_2a0){
tna=_2a0.getElementsByTagName("*");
na=[_2a0];
for(var x=0;x<tna.length;x++){
if(tna[x]["__doClobber__"]){
na.push(tna[x]);
}
}
}else{
try{
window.onload=null;
}
catch(e){
}
na=(this.clobberNodes.length)?this.clobberNodes:document.all;
}
tna=null;
var _2a4={};
for(var i=na.length-1;i>=0;i=i-1){
var el=na[i];
if(el["__clobberAttrs__"]){
for(var j=0;j<el.__clobberAttrs__.length;j++){
nukeProp(el,el.__clobberAttrs__[j]);
}
nukeProp(el,"__clobberAttrs__");
nukeProp(el,"__doClobber__");
}
}
na=null;
};
};
if(dojo.render.html.ie){
window.onunload=function(){
dojo_ie_clobber.clobber();
try{
if((dojo["widget"])&&(dojo.widget["manager"])){
dojo.widget.manager.destroyAll();
}
}
catch(e){
}
try{
window.onload=null;
}
catch(e){
}
try{
window.onunload=null;
}
catch(e){
}
dojo_ie_clobber.clobberNodes=[];
};
}
dojo.event.browser=new function(){
var _2a8=0;
this.clean=function(node){
if(dojo.render.html.ie){
dojo_ie_clobber.clobber(node);
}
};
this.addClobberNode=function(node){
if(!node["__doClobber__"]){
node.__doClobber__=true;
dojo_ie_clobber.clobberNodes.push(node);
node.__clobberAttrs__=[];
}
};
this.addClobberNodeAttrs=function(node,_2ac){
this.addClobberNode(node);
for(var x=0;x<_2ac.length;x++){
node.__clobberAttrs__.push(_2ac[x]);
}
};
this.removeListener=function(node,_2af,fp,_2b1){
if(!_2b1){
var _2b1=false;
}
_2af=_2af.toLowerCase();
if(_2af.substr(0,2)=="on"){
_2af=_2af.substr(2);
}
if(node.removeEventListener){
node.removeEventListener(_2af,fp,_2b1);
}
};
this.addListener=function(node,_2b3,fp,_2b5,_2b6){
if(!node){
return;
}
if(!_2b5){
var _2b5=false;
}
_2b3=_2b3.toLowerCase();
if(_2b3.substr(0,2)!="on"){
_2b3="on"+_2b3;
}
if(!_2b6){
var _2b7=function(evt){
if(!evt){
evt=window.event;
}
var ret=fp(dojo.event.browser.fixEvent(evt));
if(_2b5){
dojo.event.browser.stopEvent(evt);
}
return ret;
};
}else{
_2b7=fp;
}
if(node.addEventListener){
node.addEventListener(_2b3.substr(2),_2b7,_2b5);
return _2b7;
}else{
if(typeof node[_2b3]=="function"){
var _2ba=node[_2b3];
node[_2b3]=function(e){
_2ba(e);
return _2b7(e);
};
}else{
node[_2b3]=_2b7;
}
if(dojo.render.html.ie){
this.addClobberNodeAttrs(node,[_2b3]);
}
return _2b7;
}
};
this.isEvent=function(obj){
return (typeof obj!="undefined")&&(typeof Event!="undefined")&&(obj.eventPhase);
};
this.currentEvent=null;
this.callListener=function(_2bd,_2be){
if(typeof _2bd!="function"){
dojo.raise("listener not a function: "+_2bd);
}
dojo.event.browser.currentEvent.currentTarget=_2be;
return _2bd.call(_2be,dojo.event.browser.currentEvent);
};
this.stopPropagation=function(){
dojo.event.browser.currentEvent.cancelBubble=true;
};
this.preventDefault=function(){
dojo.event.browser.currentEvent.returnValue=false;
};
this.keys={KEY_BACKSPACE:8,KEY_TAB:9,KEY_ENTER:13,KEY_SHIFT:16,KEY_CTRL:17,KEY_ALT:18,KEY_PAUSE:19,KEY_CAPS_LOCK:20,KEY_ESCAPE:27,KEY_SPACE:32,KEY_PAGE_UP:33,KEY_PAGE_DOWN:34,KEY_END:35,KEY_HOME:36,KEY_LEFT_ARROW:37,KEY_UP_ARROW:38,KEY_RIGHT_ARROW:39,KEY_DOWN_ARROW:40,KEY_INSERT:45,KEY_DELETE:46,KEY_LEFT_WINDOW:91,KEY_RIGHT_WINDOW:92,KEY_SELECT:93,KEY_F1:112,KEY_F2:113,KEY_F3:114,KEY_F4:115,KEY_F5:116,KEY_F6:117,KEY_F7:118,KEY_F8:119,KEY_F9:120,KEY_F10:121,KEY_F11:122,KEY_F12:123,KEY_NUM_LOCK:144,KEY_SCROLL_LOCK:145};
this.revKeys=[];
for(var key in this.keys){
this.revKeys[this.keys[key]]=key;
}
this.fixEvent=function(evt){
if((!evt)&&(window["event"])){
var evt=window.event;
}
if((evt["type"])&&(evt["type"].indexOf("key")==0)){
evt.keys=this.revKeys;
for(var key in this.keys){
evt[key]=this.keys[key];
}
if((dojo.render.html.ie)&&(evt["type"]=="keypress")){
evt.charCode=evt.keyCode;
}
}
if(dojo.render.html.ie){
if(!evt.target){
evt.target=evt.srcElement;
}
if(!evt.currentTarget){
evt.currentTarget=evt.srcElement;
}
if(!evt.layerX){
evt.layerX=evt.offsetX;
}
if(!evt.layerY){
evt.layerY=evt.offsetY;
}
if(evt.fromElement){
evt.relatedTarget=evt.fromElement;
}
if(evt.toElement){
evt.relatedTarget=evt.toElement;
}
this.currentEvent=evt;
evt.callListener=this.callListener;
evt.stopPropagation=this.stopPropagation;
evt.preventDefault=this.preventDefault;
}
return evt;
};
this.stopEvent=function(ev){
if(window.event){
ev.returnValue=false;
ev.cancelBubble=true;
}else{
ev.preventDefault();
ev.stopPropagation();
}
};
};
dojo.hostenv.conditionalLoadModule({common:["dojo.event","dojo.event.topic"],browser:["dojo.event.browser"]});
dojo.hostenv.moduleLoaded("dojo.event.*");
dojo.provide("dojo.alg.Alg");
dojo.require("dojo.lang");
dj_deprecated("dojo.alg.Alg is deprecated, use dojo.lang instead");
dojo.alg.find=function(arr,val){
return dojo.lang.find(arr,val);
};
dojo.alg.inArray=function(arr,val){
return dojo.lang.inArray(arr,val);
};
dojo.alg.inArr=dojo.alg.inArray;
dojo.alg.getNameInObj=function(ns,item){
return dojo.lang.getNameInObj(ns,item);
};
dojo.alg.has=function(obj,name){
return dojo.lang.has(obj,name);
};
dojo.alg.forEach=function(arr,_2cc,_2cd){
return dojo.lang.forEach(arr,_2cc,_2cd);
};
dojo.alg.for_each=dojo.alg.forEach;
dojo.alg.map=function(arr,obj,_2d0){
return dojo.lang.map(arr,obj,_2d0);
};
dojo.alg.tryThese=function(){
return dojo.lang.tryThese.apply(dojo.lang,arguments);
};
dojo.alg.delayThese=function(farr,cb,_2d3,_2d4){
return dojo.lang.delayThese.apply(dojo.lang,arguments);
};
dojo.alg.for_each_call=dojo.alg.map;
dojo.require("dojo.alg.Alg",false,true);
dojo.hostenv.moduleLoaded("dojo.alg.*");
dojo.provide("dojo.uri.Uri");
dojo.uri=new function(){
this.joinPath=function(){
var arr=[];
for(var i=0;i<arguments.length;i++){
arr.push(arguments[i]);
}
return arr.join("/").replace(/\/{2,}/g,"/").replace(/((https*|ftps*):)/i,"$1/");
};
this.dojoUri=function(uri){
return new dojo.uri.Uri(dojo.hostenv.getBaseScriptUri(),uri);
};
this.Uri=function(){
var uri=arguments[0];
for(var i=1;i<arguments.length;i++){
if(!arguments[i]){
continue;
}
var _2da=new dojo.uri.Uri(arguments[i].toString());
var _2db=new dojo.uri.Uri(uri.toString());
if(_2da.path==""&&_2da.scheme==null&&_2da.authority==null&&_2da.query==null){
if(_2da.fragment!=null){
_2db.fragment=_2da.fragment;
}
_2da=_2db;
}else{
if(_2da.scheme==null){
_2da.scheme=_2db.scheme;
if(_2da.authority==null){
_2da.authority=_2db.authority;
if(_2da.path.charAt(0)!="/"){
var path=_2db.path.substring(0,_2db.path.lastIndexOf("/")+1)+_2da.path;
var segs=path.split("/");
for(var j=0;j<segs.length;j++){
if(segs[j]=="."){
if(j==segs.length-1){
segs[j]="";
}else{
segs.splice(j,1);
j--;
}
}else{
if(j>0&&!(j==1&&segs[0]=="")&&segs[j]==".."&&segs[j-1]!=".."){
if(j==segs.length-1){
segs.splice(j,1);
segs[j-1]="";
}else{
segs.splice(j-1,2);
j-=2;
}
}
}
}
_2da.path=segs.join("/");
}
}
}
}
uri="";
if(_2da.scheme!=null){
uri+=_2da.scheme+":";
}
if(_2da.authority!=null){
uri+="//"+_2da.authority;
}
uri+=_2da.path;
if(_2da.query!=null){
uri+="?"+_2da.query;
}
if(_2da.fragment!=null){
uri+="#"+_2da.fragment;
}
}
this.uri=uri.toString();
var _2df="^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\\?([^#]*))?(#(.*))?$";
var r=this.uri.match(new RegExp(_2df));
this.scheme=r[2]||(r[1]?"":null);
this.authority=r[4]||(r[3]?"":null);
this.path=r[5];
this.query=r[7]||(r[6]?"":null);
this.fragment=r[9]||(r[8]?"":null);
if(this.authority!=null){
_2df="^((([^:]+:)?([^@]+))@)?([^:]*)(:([0-9]+))?$";
r=this.authority.match(new RegExp(_2df));
this.user=r[3]||null;
this.password=r[4]||null;
this.host=r[5];
this.port=r[7]||null;
}
this.toString=function(){
return this.uri;
};
};
};
dojo.provide("dojo.math");
dojo.math.degToRad=function(x){
return (x*Math.PI)/180;
};
dojo.math.radToDeg=function(x){
return (x*180)/Math.PI;
};
dojo.math.factorial=function(n){
if(n<1){
return 0;
}
var _2e4=1;
for(var i=1;i<=n;i++){
_2e4*=i;
}
return _2e4;
};
dojo.math.permutations=function(n,k){
if(n==0||k==0){
return 1;
}
return (dojo.math.factorial(n)/dojo.math.factorial(n-k));
};
dojo.math.combinations=function(n,r){
if(n==0||r==0){
return 1;
}
return (dojo.math.factorial(n)/(dojo.math.factorial(n-r)*dojo.math.factorial(r)));
};
dojo.math.bernstein=function(t,n,i){
return (dojo.math.combinations(n,i)*Math.pow(t,i)*Math.pow(1-t,n-i));
};
dojo.math.gaussianRandom=function(){
var k=2;
do{
var i=2*Math.random()-1;
var j=2*Math.random()-1;
k=i*i+j*j;
}while(k>=1);
k=Math.sqrt((-2*Math.log(k))/k);
return i*k;
};
dojo.math.mean=function(){
var _2f0=dojo.lang.isArray(arguments[0])?arguments[0]:arguments;
var mean=0;
for(var i=0;i<_2f0.length;i++){
mean+=_2f0[i];
}
return mean/_2f0.length;
};
dojo.math.round=function(_2f3,_2f4){
if(!_2f4){
var _2f5=1;
}else{
var _2f5=Math.pow(10,_2f4);
}
return Math.round(_2f3*_2f5)/_2f5;
};
dojo.math.sd=function(){
var _2f6=dojo.lang.isArray(arguments[0])?arguments[0]:arguments;
return Math.sqrt(dojo.math.variance(_2f6));
};
dojo.math.variance=function(){
var _2f7=dojo.lang.isArray(arguments[0])?arguments[0]:arguments;
var mean=0,squares=0;
for(var i=0;i<_2f7.length;i++){
mean+=_2f7[i];
squares+=Math.pow(_2f7[i],2);
}
return (squares/_2f7.length)-Math.pow(mean/_2f7.length,2);
};
dojo.math.range=function(a,b,step){
if(arguments.length<2){
b=a;
a=0;
}
if(arguments.length<3){
step=1;
}
var _2fd=[];
if(step>0){
for(var i=a;i<b;i+=step){
_2fd.push(i);
}
}else{
if(step<0){
for(var i=a;i>b;i+=step){
_2fd.push(i);
}
}else{
throw new Error("dojo.math.range: step must be non-zero");
}
}
return _2fd;
};
dojo.provide("dojo.graphics.color");
dojo.require("dojo.lang");
dojo.require("dojo.string");
dojo.require("dojo.math");
dojo.graphics.color.Color=function(r,g,b,a){
if(dojo.lang.isArray(r)){
this.r=r[0];
this.g=r[1];
this.b=r[2];
this.a=r[3]||1;
}else{
if(dojo.lang.isString(r)){
var rgb=dojo.graphics.color.extractRGB(r);
this.r=rgb[0];
this.g=rgb[1];
this.b=rgb[2];
this.a=g||1;
}else{
if(r instanceof dojo.graphics.color.Color){
this.r=r.r;
this.b=r.b;
this.g=r.g;
this.a=r.a;
}else{
this.r=r;
this.g=g;
this.b=b;
this.a=a;
}
}
}
};
dojo.lang.extend(dojo.graphics.color.Color,{toRgb:function(_304){
if(_304){
return this.toRgba();
}else{
return [this.r,this.g,this.b];
}
},toRgba:function(){
return [this.r,this.g,this.b,this.a];
},toHex:function(){
return dojo.graphics.color.rgb2hex(this.toRgb());
},toCss:function(){
return "rgb("+this.toRgb().join()+")";
},toString:function(){
return this.toHex();
},toHsv:function(){
return dojo.graphics.color.rgb2hsv(this.toRgb());
},toHsl:function(){
return dojo.graphics.color.rgb2hsl(this.toRgb());
},blend:function(_305,_306){
return dojo.graphics.color.blend(this.toRgb(),new Color(_305).toRgb(),_306);
}});
dojo.graphics.color.named={white:[255,255,255],black:[0,0,0],red:[255,0,0],green:[0,255,0],blue:[0,0,255],navy:[0,0,128],gray:[128,128,128],silver:[192,192,192]};
dojo.graphics.color.blend=function(a,b,_309){
if(typeof a=="string"){
return dojo.graphics.color.blendHex(a,b,_309);
}
if(!_309){
_309=0;
}else{
if(_309>1){
_309=1;
}else{
if(_309<-1){
_309=-1;
}
}
}
var c=new Array(3);
for(var i=0;i<3;i++){
var half=Math.abs(a[i]-b[i])/2;
c[i]=Math.floor(Math.min(a[i],b[i])+half+(half*_309));
}
return c;
};
dojo.graphics.color.blendHex=function(a,b,_30f){
return dojo.graphics.color.rgb2hex(dojo.graphics.color.blend(dojo.graphics.color.hex2rgb(a),dojo.graphics.color.hex2rgb(b),_30f));
};
dojo.graphics.color.extractRGB=function(_310){
var hex="0123456789abcdef";
_310=_310.toLowerCase();
if(_310.indexOf("rgb")==0){
var _312=_310.match(/rgba*\((\d+), *(\d+), *(\d+)/i);
var ret=_312.splice(1,3);
return ret;
}else{
var _314=dojo.graphics.color.hex2rgb(_310);
if(_314){
return _314;
}else{
return dojo.graphics.color.named[_310]||[255,255,255];
}
}
};
dojo.graphics.color.hex2rgb=function(hex){
var _316="0123456789ABCDEF";
var rgb=new Array(3);
if(hex.indexOf("#")==0){
hex=hex.substring(1);
}
hex=hex.toUpperCase();
if(hex.replace(new RegExp("["+_316+"]","g"),"")!=""){
return null;
}
if(hex.length==3){
rgb[0]=hex.charAt(0)+hex.charAt(0);
rgb[1]=hex.charAt(1)+hex.charAt(1);
rgb[2]=hex.charAt(2)+hex.charAt(2);
}else{
rgb[0]=hex.substring(0,2);
rgb[1]=hex.substring(2,4);
rgb[2]=hex.substring(4);
}
for(var i=0;i<rgb.length;i++){
rgb[i]=_316.indexOf(rgb[i].charAt(0))*16+_316.indexOf(rgb[i].charAt(1));
}
return rgb;
};
dojo.graphics.color.rgb2hex=function(r,g,b){
if(dojo.lang.isArray(r)){
g=r[1]||0;
b=r[2]||0;
r=r[0]||0;
}
return ["#",dojo.string.pad(r.toString(16),2),dojo.string.pad(g.toString(16),2),dojo.string.pad(b.toString(16),2)].join("");
};
dojo.graphics.color.rgb2hsv=function(r,g,b){
if(dojo.lang.isArray(r)){
b=r[2]||0;
g=r[1]||0;
r=r[0]||0;
}
var h=null;
var s=null;
var v=null;
var min=Math.min(r,g,b);
v=Math.max(r,g,b);
var _323=v-min;
s=(v==0)?0:_323/v;
if(s==0){
h=0;
}else{
if(r==v){
h=60*(g-b)/_323;
}else{
if(g==v){
h=120+60*(b-r)/_323;
}else{
if(b==v){
h=240+60*(r-g)/_323;
}
}
}
if(h<0){
h+=360;
}
}
h=(h==0)?360:Math.ceil((h/360)*255);
s=Math.ceil(s*255);
return [h,s,v];
};
dojo.graphics.color.hsv2rgb=function(h,s,v){
if(dojo.lang.isArray(h)){
v=h[2]||0;
s=h[1]||0;
h=h[0]||0;
}
h=(h/255)*360;
if(h==360){
h=0;
}
s=s/255;
v=v/255;
var r=null;
var g=null;
var b=null;
if(s==0){
r=v;
g=v;
b=v;
}else{
var _32a=h/60;
var i=Math.floor(_32a);
var f=_32a-i;
var p=v*(1-s);
var q=v*(1-(s*f));
var t=v*(1-(s*(1-f)));
switch(i){
case 0:
r=v;
g=t;
b=p;
break;
case 1:
r=q;
g=v;
b=p;
break;
case 2:
r=p;
g=v;
b=t;
break;
case 3:
r=p;
g=q;
b=v;
break;
case 4:
r=t;
g=p;
b=v;
break;
case 5:
r=v;
g=p;
b=q;
break;
}
}
r=Math.ceil(r*255);
g=Math.ceil(g*255);
b=Math.ceil(b*255);
return [r,g,b];
};
dojo.graphics.color.rgb2hsl=function(r,g,b){
if(dojo.lang.isArray(r)){
b=r[2]||0;
g=r[1]||0;
r=r[0]||0;
}
r/=255;
g/=255;
b/=255;
var h=null;
var s=null;
var l=null;
var min=Math.min(r,g,b);
var max=Math.max(r,g,b);
var _338=max-min;
l=(min+max)/2;
s=0;
if((l>0)&&(l<1)){
s=_338/((l<0.5)?(2*l):(2-2*l));
}
h=0;
if(_338>0){
if((max==r)&&(max!=g)){
h+=(g-b)/_338;
}
if((max==g)&&(max!=b)){
h+=(2+(b-r)/_338);
}
if((max==b)&&(max!=r)){
h+=(4+(r-g)/_338);
}
h*=60;
}
h=(h==0)?360:Math.ceil((h/360)*255);
s=Math.ceil(s*255);
l=Math.ceil(l*255);
return [h,s,l];
};
dojo.graphics.color.hsl2rgb=function(h,s,l){
if(dojo.lang.isArray(h)){
l=h[2]||0;
s=h[1]||0;
h=h[0]||0;
}
h=(h/255)*360;
if(h==360){
h=0;
}
s=s/255;
l=l/255;
while(h<0){
h+=360;
}
while(h>360){
h-=360;
}
if(h<120){
r=(120-h)/60;
g=h/60;
b=0;
}else{
if(h<240){
r=0;
g=(240-h)/60;
b=(h-120)/60;
}else{
r=(h-240)/60;
g=0;
b=(360-h)/60;
}
}
r=Math.min(r,1);
g=Math.min(g,1);
b=Math.min(b,1);
r=2*s*r+(1-s);
g=2*s*g+(1-s);
b=2*s*b+(1-s);
if(l<0.5){
r=l*r;
g=l*g;
b=l*b;
}else{
r=(1-l)*r+2*l-1;
g=(1-l)*g+2*l-1;
b=(1-l)*b+2*l-1;
}
r=Math.ceil(r*255);
g=Math.ceil(g*255);
b=Math.ceil(b*255);
return [r,g,b];
};
dojo.graphics.color.hsl2hex=function(h,s,l){
var rgb=dojo.graphics.color.hsl2rgb(h,s,l);
return dojo.graphics.color.rgb2hex(rgb[0],rgb[1],rgb[2]);
};
dojo.graphics.color.hex2hsl=function(hex){
var rgb=dojo.graphics.color.hex2rgb(hex);
return dojo.graphics.color.rgb2hsl(rgb[0],rgb[1],rgb[2]);
};
dojo.provide("dojo.style");
dojo.require("dojo.dom");
dojo.require("dojo.uri.Uri");
dojo.require("dojo.graphics.color");
dojo.style.boxSizing={marginBox:"margin-box",borderBox:"border-box",paddingBox:"padding-box",contentBox:"content-box"};
dojo.style.getBoxSizing=function(node){
if(dojo.render.html.ie||dojo.render.html.opera){
var cm=document["compatMode"];
if(cm=="BackCompat"||cm=="QuirksMode"){
return dojo.style.boxSizing.borderBox;
}else{
return dojo.style.boxSizing.contentBox;
}
}else{
if(arguments.length==0){
node=document.documentElement;
}
var _344=dojo.style.getStyle(node,"-moz-box-sizing");
if(!_344){
_344=dojo.style.getStyle(node,"box-sizing");
}
return (_344?_344:dojo.style.boxSizing.contentBox);
}
};
dojo.style.isBorderBox=function(node){
return (dojo.style.getBoxSizing(node)==dojo.style.boxSizing.borderBox);
};
dojo.style.getUnitValue=function(_346,_347,_348){
var _349={value:0,units:"px"};
var s=dojo.style.getComputedStyle(_346,_347);
if(s==""||(s=="auto"&&_348)){
return _349;
}
if(dojo.lang.isUndefined(s)){
_349.value=NaN;
}else{
var _34b=s.match(/([\d.]+)([a-z%]*)/i);
if(!_34b){
_349.value=NaN;
}else{
_349.value=Number(_34b[1]);
_349.units=_34b[2].toLowerCase();
}
}
return _349;
};
dojo.style.getPixelValue=function(_34c,_34d,_34e){
var _34f=dojo.style.getUnitValue(_34c,_34d,_34e);
if(isNaN(_34f.value)){
return 0;
}
if((_34f.value)&&(_34f.units!="px")){
return NaN;
}
return _34f.value;
};
dojo.style.getNumericStyle=dojo.style.getPixelValue;
dojo.style.isPositionAbsolute=function(node){
return (dojo.style.getComputedStyle(node,"position")=="absolute");
};
dojo.style.getMarginWidth=function(node){
var _352=dojo.style.isPositionAbsolute(node);
var left=dojo.style.getPixelValue(node,"margin-left",_352);
var _354=dojo.style.getPixelValue(node,"margin-right",_352);
return left+_354;
};
dojo.style.getBorderWidth=function(node){
var left=(dojo.style.getStyle(node,"border-left-style")=="none"?0:dojo.style.getPixelValue(node,"border-left-width"));
var _357=(dojo.style.getStyle(node,"border-right-style")=="none"?0:dojo.style.getPixelValue(node,"border-right-width"));
return left+_357;
};
dojo.style.getPaddingWidth=function(node){
var left=dojo.style.getPixelValue(node,"padding-left",true);
var _35a=dojo.style.getPixelValue(node,"padding-right",true);
return left+_35a;
};
dojo.style.getContentWidth=function(node){
return node.offsetWidth-dojo.style.getPaddingWidth(node)-dojo.style.getBorderWidth(node);
};
dojo.style.getInnerWidth=function(node){
return node.offsetWidth;
};
dojo.style.getOuterWidth=function(node){
return dojo.style.getInnerWidth(node)+dojo.style.getMarginWidth(node);
};
dojo.style.setOuterWidth=function(node,_35f){
if(!dojo.style.isBorderBox(node)){
_35f-=dojo.style.getPaddingWidth(node)+dojo.style.getBorderWidth(node);
}
_35f-=dojo.style.getMarginWidth(node);
if(!isNaN(_35f)&&_35f>0){
node.style.width=_35f+"px";
return true;
}else{
return false;
}
};
dojo.style.getContentBoxWidth=dojo.style.getContentWidth;
dojo.style.getBorderBoxWidth=dojo.style.getInnerWidth;
dojo.style.getMarginBoxWidth=dojo.style.getOuterWidth;
dojo.style.setMarginBoxWidth=dojo.style.setOuterWidth;
dojo.style.getMarginHeight=function(node){
var _361=dojo.style.isPositionAbsolute(node);
var top=dojo.style.getPixelValue(node,"margin-top",_361);
var _363=dojo.style.getPixelValue(node,"margin-bottom",_361);
return top+_363;
};
dojo.style.getBorderHeight=function(node){
var top=(dojo.style.getStyle(node,"border-top-style")=="none"?0:dojo.style.getPixelValue(node,"border-top-width"));
var _366=(dojo.style.getStyle(node,"border-bottom-style")=="none"?0:dojo.style.getPixelValue(node,"border-bottom-width"));
return top+_366;
};
dojo.style.getPaddingHeight=function(node){
var top=dojo.style.getPixelValue(node,"padding-top",true);
var _369=dojo.style.getPixelValue(node,"padding-bottom",true);
return top+_369;
};
dojo.style.getContentHeight=function(node){
return node.offsetHeight-dojo.style.getPaddingHeight(node)-dojo.style.getBorderHeight(node);
};
dojo.style.getInnerHeight=function(node){
return node.offsetHeight;
};
dojo.style.getOuterHeight=function(node){
return dojo.style.getInnerHeight(node)+dojo.style.getMarginHeight(node);
};
dojo.style.setOuterHeight=function(node,_36e){
if(!dojo.style.isBorderBox(node)){
_36e-=dojo.style.getPaddingHeight(node)+dojo.style.getBorderHeight(node);
}
_36e-=dojo.style.getMarginHeight(node);
if(!isNaN(_36e)&&_36e>0){
node.style.height=_36e+"px";
return true;
}else{
return false;
}
};
dojo.style.setContentWidth=function(node,_370){
if(dojo.style.isBorderBox(node)){
_370+=dojo.style.getPaddingWidth(node)+dojo.style.getBorderWidth(node);
}
if(!isNaN(_370)&&_370>0){
node.style.width=_370+"px";
return true;
}else{
return false;
}
};
dojo.style.setContentHeight=function(node,_372){
if(dojo.style.isBorderBox(node)){
_372+=dojo.style.getPaddingHeight(node)+dojo.style.getBorderHeight(node);
}
if(!isNaN(_372)&&_372>0){
node.style.height=_372+"px";
return true;
}else{
return false;
}
};
dojo.style.getContentBoxHeight=dojo.style.getContentHeight;
dojo.style.getBorderBoxHeight=dojo.style.getInnerHeight;
dojo.style.getMarginBoxHeight=dojo.style.getOuterHeight;
dojo.style.setMarginBoxHeight=dojo.style.setOuterHeight;
dojo.style.getTotalOffset=function(node,type,_375){
var _376=(type=="top")?"offsetTop":"offsetLeft";
var _377=(type=="top")?"scrollTop":"scrollLeft";
var _378=(type=="top")?"y":"x";
var _379=0;
if(node["offsetParent"]){
if(dojo.render.html.safari&&node.style.getPropertyValue("position")=="absolute"&&node.parentNode==dojo.html.body()){
var _37a=dojo.html.body();
}else{
var _37a=dojo.html.body().parentNode;
}
if(_375&&node.parentNode!=document.body){
_379-=dojo.style.sumAncestorProperties(node,_377);
}
do{
_379+=node[_376];
node=node.offsetParent;
}while(node!=_37a&&node!=null);
}else{
if(node[_378]){
_379+=node[_378];
}
}
return _379;
};
dojo.style.sumAncestorProperties=function(node,prop){
if(!node){
return 0;
}
var _37d=0;
while(node){
var val=node[prop];
if(val){
_37d+=val-0;
}
node=node.parentNode;
}
return _37d;
};
dojo.style.totalOffsetLeft=function(node,_380){
return dojo.style.getTotalOffset(node,"left",_380);
};
dojo.style.getAbsoluteX=dojo.style.totalOffsetLeft;
dojo.style.totalOffsetTop=function(node,_382){
return dojo.style.getTotalOffset(node,"top",_382);
};
dojo.style.getAbsoluteY=dojo.style.totalOffsetTop;
dojo.style.getAbsolutePosition=function(node,_384){
var _385=[dojo.style.getAbsoluteX(node,_384),dojo.style.getAbsoluteY(node,_384)];
_385.x=_385[0];
_385.y=_385[1];
return _385;
};
dojo.style.styleSheet=null;
dojo.style.insertCssRule=function(_386,_387,_388){
if(!dojo.style.styleSheet){
if(document.createStyleSheet){
dojo.style.styleSheet=document.createStyleSheet();
}else{
if(document.styleSheets[0]){
dojo.style.styleSheet=document.styleSheets[0];
}else{
return null;
}
}
}
if(arguments.length<3){
if(dojo.style.styleSheet.cssRules){
_388=dojo.style.styleSheet.cssRules.length;
}else{
if(dojo.style.styleSheet.rules){
_388=dojo.style.styleSheet.rules.length;
}else{
return null;
}
}
}
if(dojo.style.styleSheet.insertRule){
var rule=_386+" { "+_387+" }";
return dojo.style.styleSheet.insertRule(rule,_388);
}else{
if(dojo.style.styleSheet.addRule){
return dojo.style.styleSheet.addRule(_386,_387,_388);
}else{
return null;
}
}
};
dojo.style.removeCssRule=function(_38a){
if(!dojo.style.styleSheet){
dojo.debug("no stylesheet defined for removing rules");
return false;
}
if(dojo.render.html.ie){
if(!_38a){
_38a=dojo.style.styleSheet.rules.length;
dojo.style.styleSheet.removeRule(_38a);
}
}else{
if(document.styleSheets[0]){
if(!_38a){
_38a=dojo.style.styleSheet.cssRules.length;
}
dojo.style.styleSheet.deleteRule(_38a);
}
}
return true;
};
dojo.style.insertCssFile=function(URI,doc,_38d){
if(!URI){
return;
}
if(!doc){
doc=document;
}
if(doc.baseURI){
URI=new dojo.uri.Uri(doc.baseURI,URI);
}
if(_38d&&doc.styleSheets){
var loc=location.href.split("#")[0].substring(0,location.href.indexOf(location.pathname));
for(var i=0;i<doc.styleSheets.length;i++){
if(doc.styleSheets[i].href&&URI.toString()==new dojo.uri.Uri(doc.styleSheets[i].href.toString())){
return;
}
}
}
var file=doc.createElement("link");
file.setAttribute("type","text/css");
file.setAttribute("rel","stylesheet");
file.setAttribute("href",URI);
var head=doc.getElementsByTagName("head")[0];
if(head){
head.appendChild(file);
}
};
dojo.style.getBackgroundColor=function(node){
var _393;
do{
_393=dojo.style.getStyle(node,"background-color");
if(_393.toLowerCase()=="rgba(0, 0, 0, 0)"){
_393="transparent";
}
if(node==document.getElementsByTagName("body")[0]){
node=null;
break;
}
node=node.parentNode;
}while(node&&dojo.lang.inArray(_393,["transparent",""]));
if(_393=="transparent"){
_393=[255,255,255,0];
}else{
_393=dojo.graphics.color.extractRGB(_393);
}
return _393;
};
dojo.style.getComputedStyle=function(_394,_395,_396){
var _397=_396;
if(_394.style.getPropertyValue){
_397=_394.style.getPropertyValue(_395);
}
if(!_397){
if(document.defaultView){
var cs=document.defaultView.getComputedStyle(_394,"");
if(cs){
_397=cs.getPropertyValue(_395);
}
}else{
if(_394.currentStyle){
_397=_394.currentStyle[dojo.style.toCamelCase(_395)];
}
}
}
return _397;
};
dojo.style.getStyle=function(_399,_39a){
var _39b=dojo.style.toCamelCase(_39a);
var _39c=_399.style[_39b];
return (_39c?_39c:dojo.style.getComputedStyle(_399,_39a,_39c));
};
dojo.style.toCamelCase=function(_39d){
var arr=_39d.split("-"),cc=arr[0];
for(var i=1;i<arr.length;i++){
cc+=arr[i].charAt(0).toUpperCase()+arr[i].substring(1);
}
return cc;
};
dojo.style.toSelectorCase=function(_3a0){
return _3a0.replace(/([A-Z])/g,"-$1").toLowerCase();
};
dojo.style.setOpacity=function setOpacity(node,_3a2,_3a3){
node=dojo.byId(node);
var h=dojo.render.html;
if(!_3a3){
if(_3a2>=1){
if(h.ie){
dojo.style.clearOpacity(node);
return;
}else{
_3a2=0.999999;
}
}else{
if(_3a2<0){
_3a2=0;
}
}
}
if(h.ie){
if(node.nodeName.toLowerCase()=="tr"){
var tds=node.getElementsByTagName("td");
for(var x=0;x<tds.length;x++){
tds[x].style.filter="Alpha(Opacity="+_3a2*100+")";
}
}
node.style.filter="Alpha(Opacity="+_3a2*100+")";
}else{
if(h.moz){
node.style.opacity=_3a2;
node.style.MozOpacity=_3a2;
}else{
if(h.safari){
node.style.opacity=_3a2;
node.style.KhtmlOpacity=_3a2;
}else{
node.style.opacity=_3a2;
}
}
}
};
dojo.style.getOpacity=function getOpacity(node){
if(dojo.render.html.ie){
var opac=(node.filters&&node.filters.alpha&&typeof node.filters.alpha.opacity=="number"?node.filters.alpha.opacity:100)/100;
}else{
var opac=node.style.opacity||node.style.MozOpacity||node.style.KhtmlOpacity||1;
}
return opac>=0.999999?1:Number(opac);
};
dojo.style.clearOpacity=function clearOpacity(node){
var h=dojo.render.html;
if(h.ie){
if(node.filters&&node.filters.alpha){
node.style.filter="";
}
}else{
if(h.moz){
node.style.opacity=1;
node.style.MozOpacity=1;
}else{
if(h.safari){
node.style.opacity=1;
node.style.KhtmlOpacity=1;
}else{
node.style.opacity=1;
}
}
}
};
dojo.provide("dojo.html");
dojo.require("dojo.dom");
dojo.require("dojo.style");
dojo.require("dojo.string");
dojo.lang.mixin(dojo.html,dojo.dom);
dojo.lang.mixin(dojo.html,dojo.style);
dojo.html.clearSelection=function(){
try{
if(window["getSelection"]){
if(dojo.render.html.safari){
window.getSelection().collapse();
}else{
window.getSelection().removeAllRanges();
}
}else{
if(document.selection){
if(document.selection.empty){
document.selection.empty();
}else{
if(document.selection.clear){
document.selection.clear();
}
}
}
}
return true;
}
catch(e){
dojo.debug(e);
return false;
}
};
dojo.html.disableSelection=function(_3ab){
_3ab=dojo.byId(_3ab)||dojo.html.body();
var h=dojo.render.html;
if(h.mozilla){
_3ab.style.MozUserSelect="none";
}else{
if(h.safari){
_3ab.style.KhtmlUserSelect="none";
}else{
if(h.ie){
_3ab.unselectable="on";
}else{
return false;
}
}
}
return true;
};
dojo.html.enableSelection=function(_3ad){
_3ad=dojo.byId(_3ad)||dojo.html.body();
var h=dojo.render.html;
if(h.mozilla){
_3ad.style.MozUserSelect="";
}else{
if(h.safari){
_3ad.style.KhtmlUserSelect="";
}else{
if(h.ie){
_3ad.unselectable="off";
}else{
return false;
}
}
}
return true;
};
dojo.html.selectElement=function(_3af){
_3af=dojo.byId(_3af);
if(document.selection&&dojo.html.body().createTextRange){
var _3b0=dojo.html.body().createTextRange();
_3b0.moveToElementText(_3af);
_3b0.select();
}else{
if(window["getSelection"]){
var _3b1=window.getSelection();
if(_3b1["selectAllChildren"]){
_3b1.selectAllChildren(_3af);
}
}
}
};
dojo.html.isSelectionCollapsed=function(){
if(document["selection"]){
return document.selection.createRange().text=="";
}else{
if(window["getSelection"]){
var _3b2=window.getSelection();
if(dojo.lang.isString(_3b2)){
return _3b2=="";
}else{
return _3b2.isCollapsed;
}
}
}
};
dojo.html.getEventTarget=function(evt){
if(!evt){
evt=window.event||{};
}
if(evt.srcElement){
return evt.srcElement;
}else{
if(evt.target){
return evt.target;
}
}
return null;
};
dojo.html.getScrollTop=function(){
return document.documentElement.scrollTop||dojo.html.body().scrollTop||0;
};
dojo.html.getScrollLeft=function(){
return document.documentElement.scrollLeft||dojo.html.body().scrollLeft||0;
};
dojo.html.getDocumentWidth=function(){
dojo.deprecated("dojo.html.getDocument* has been deprecated in favor of dojo.html.getViewport*");
return dojo.html.getViewportWidth();
};
dojo.html.getDocumentHeight=function(){
dojo.deprecated("dojo.html.getDocument* has been deprecated in favor of dojo.html.getViewport*");
return dojo.html.getViewportHeight();
};
dojo.html.getDocumentSize=function(){
dojo.deprecated("dojo.html.getDocument* has been deprecated in favor of dojo.html.getViewport*");
return dojo.html.getViewportSize();
};
dojo.html.getViewportWidth=function(){
var w=0;
if(window.innerWidth){
w=window.innerWidth;
}
if(dojo.exists(document,"documentElement.clientWidth")){
var w2=document.documentElement.clientWidth;
if(!w||w2&&w2<w){
w=w2;
}
return w;
}
if(document.body){
return document.body.clientWidth;
}
return 0;
};
dojo.html.getViewportHeight=function(){
if(window.innerHeight){
return window.innerHeight;
}
if(dojo.exists(document,"documentElement.clientHeight")){
return document.documentElement.clientHeight;
}
if(document.body){
return document.body.clientHeight;
}
return 0;
};
dojo.html.getViewportSize=function(){
var ret=[dojo.html.getViewportWidth(),dojo.html.getViewportHeight()];
ret.w=ret[0];
ret.h=ret[1];
return ret;
};
dojo.html.getScrollOffset=function(){
var ret=[0,0];
if(window.pageYOffset){
ret=[window.pageXOffset,window.pageYOffset];
}else{
if(dojo.exists(document,"documentElement.scrollTop")){
ret=[document.documentElement.scrollLeft,document.documentElement.scrollTop];
}else{
if(document.body){
ret=[document.body.scrollLeft,document.body.scrollTop];
}
}
}
ret.x=ret[0];
ret.y=ret[1];
return ret;
};
dojo.html.getParentOfType=function(node,type){
dojo.deprecated("dojo.html.getParentOfType has been deprecated in favor of dojo.html.getParentByType*");
return dojo.html.getParentByType(node,type);
};
dojo.html.getParentByType=function(node,type){
var _3bc=dojo.byId(node);
type=type.toLowerCase();
while((_3bc)&&(_3bc.nodeName.toLowerCase()!=type)){
if(_3bc==(document["body"]||document["documentElement"])){
return null;
}
_3bc=_3bc.parentNode;
}
return _3bc;
};
dojo.html.getAttribute=function(node,attr){
node=dojo.byId(node);
if((!node)||(!node.getAttribute)){
return null;
}
var ta=typeof attr=="string"?attr:new String(attr);
var v=node.getAttribute(ta.toUpperCase());
if((v)&&(typeof v=="string")&&(v!="")){
return v;
}
if(v&&v.value){
return v.value;
}
if((node.getAttributeNode)&&(node.getAttributeNode(ta))){
return (node.getAttributeNode(ta)).value;
}else{
if(node.getAttribute(ta)){
return node.getAttribute(ta);
}else{
if(node.getAttribute(ta.toLowerCase())){
return node.getAttribute(ta.toLowerCase());
}
}
}
return null;
};
dojo.html.hasAttribute=function(node,attr){
node=dojo.byId(node);
return dojo.html.getAttribute(node,attr)?true:false;
};
dojo.html.getClass=function(node){
node=dojo.byId(node);
if(!node){
return "";
}
var cs="";
if(node.className){
cs=node.className;
}else{
if(dojo.html.hasAttribute(node,"class")){
cs=dojo.html.getAttribute(node,"class");
}
}
return dojo.string.trim(cs);
};
dojo.html.getClasses=function(node){
node=dojo.byId(node);
var c=dojo.html.getClass(node);
return (c=="")?[]:c.split(/\s+/g);
};
dojo.html.hasClass=function(node,_3c8){
node=dojo.byId(node);
return dojo.lang.inArray(dojo.html.getClasses(node),_3c8);
};
dojo.html.prependClass=function(node,_3ca){
node=dojo.byId(node);
if(!node){
return false;
}
_3ca+=" "+dojo.html.getClass(node);
return dojo.html.setClass(node,_3ca);
};
dojo.html.addClass=function(node,_3cc){
node=dojo.byId(node);
if(!node){
return false;
}
if(dojo.html.hasClass(node,_3cc)){
return false;
}
_3cc=dojo.string.trim(dojo.html.getClass(node)+" "+_3cc);
return dojo.html.setClass(node,_3cc);
};
dojo.html.setClass=function(node,_3ce){
node=dojo.byId(node);
if(!node){
return false;
}
var cs=new String(_3ce);
try{
if(typeof node.className=="string"){
node.className=cs;
}else{
if(node.setAttribute){
node.setAttribute("class",_3ce);
node.className=cs;
}else{
return false;
}
}
}
catch(e){
dojo.debug("dojo.html.setClass() failed",e);
}
return true;
};
dojo.html.removeClass=function(node,_3d1,_3d2){
node=dojo.byId(node);
if(!node){
return false;
}
var _3d1=dojo.string.trim(new String(_3d1));
try{
var cs=dojo.html.getClasses(node);
var nca=[];
if(_3d2){
for(var i=0;i<cs.length;i++){
if(cs[i].indexOf(_3d1)==-1){
nca.push(cs[i]);
}
}
}else{
for(var i=0;i<cs.length;i++){
if(cs[i]!=_3d1){
nca.push(cs[i]);
}
}
}
dojo.html.setClass(node,nca.join(" "));
}
catch(e){
dojo.debug("dojo.html.removeClass() failed",e);
}
return true;
};
dojo.html.replaceClass=function(node,_3d7,_3d8){
node=dojo.byId(node);
dojo.html.removeClass(node,_3d8);
dojo.html.addClass(node,_3d7);
};
dojo.html.classMatchType={ContainsAll:0,ContainsAny:1,IsOnly:2};
dojo.html.getElementsByClass=function(_3d9,_3da,_3db,_3dc){
_3da=dojo.byId(_3da);
if(!_3da){
_3da=document;
}
var _3dd=_3d9.split(/\s+/g);
var _3de=[];
if(_3dc!=1&&_3dc!=2){
_3dc=0;
}
var _3df=new RegExp("(\\s|^)(("+_3dd.join(")|(")+"))(\\s|$)");
if(!_3db){
_3db="*";
}
var _3e0=_3da.getElementsByTagName(_3db);
outer:
for(var i=0;i<_3e0.length;i++){
var node=_3e0[i];
var _3e3=dojo.html.getClasses(node);
if(_3e3.length==0){
continue outer;
}
var _3e4=0;
for(var j=0;j<_3e3.length;j++){
if(_3df.test(_3e3[j])){
if(_3dc==dojo.html.classMatchType.ContainsAny){
_3de.push(node);
continue outer;
}else{
_3e4++;
}
}else{
if(_3dc==dojo.html.classMatchType.IsOnly){
continue outer;
}
}
}
if(_3e4==_3dd.length){
if(_3dc==dojo.html.classMatchType.IsOnly&&_3e4==_3e3.length){
_3de.push(node);
}else{
if(_3dc==dojo.html.classMatchType.ContainsAll){
_3de.push(node);
}
}
}
}
return _3de;
};
dojo.html.getElementsByClassName=dojo.html.getElementsByClass;
dojo.html.gravity=function(node,e){
node=dojo.byId(node);
var _3e8=e.pageX||e.clientX+dojo.html.body().scrollLeft;
var _3e9=e.pageY||e.clientY+dojo.html.body().scrollTop;
with(dojo.html){
var _3ea=getAbsoluteX(node)+(getInnerWidth(node)/2);
var _3eb=getAbsoluteY(node)+(getInnerHeight(node)/2);
}
with(dojo.html.gravity){
return ((_3e8<_3ea?WEST:EAST)|(_3e9<_3eb?NORTH:SOUTH));
}
};
dojo.html.gravity.NORTH=1;
dojo.html.gravity.SOUTH=1<<1;
dojo.html.gravity.EAST=1<<2;
dojo.html.gravity.WEST=1<<3;
dojo.html.overElement=function(_3ec,e){
_3ec=dojo.byId(_3ec);
var _3ee=e.pageX||e.clientX+dojo.html.body().scrollLeft;
var _3ef=e.pageY||e.clientY+dojo.html.body().scrollTop;
with(dojo.html){
var top=getAbsoluteY(_3ec);
var _3f1=top+getInnerHeight(_3ec);
var left=getAbsoluteX(_3ec);
var _3f3=left+getInnerWidth(_3ec);
}
return (_3ee>=left&&_3ee<=_3f3&&_3ef>=top&&_3ef<=_3f1);
};
dojo.html.renderedTextContent=function(node){
node=dojo.byId(node);
var _3f5="";
if(node==null){
return _3f5;
}
for(var i=0;i<node.childNodes.length;i++){
switch(node.childNodes[i].nodeType){
case 1:
case 5:
var _3f7="unknown";
try{
_3f7=dojo.style.getStyle(node.childNodes[i],"display");
}
catch(E){
}
switch(_3f7){
case "block":
case "list-item":
case "run-in":
case "table":
case "table-row-group":
case "table-header-group":
case "table-footer-group":
case "table-row":
case "table-column-group":
case "table-column":
case "table-cell":
case "table-caption":
_3f5+="\n";
_3f5+=dojo.html.renderedTextContent(node.childNodes[i]);
_3f5+="\n";
break;
case "none":
break;
default:
if(node.childNodes[i].tagName&&node.childNodes[i].tagName.toLowerCase()=="br"){
_3f5+="\n";
}else{
_3f5+=dojo.html.renderedTextContent(node.childNodes[i]);
}
break;
}
break;
case 3:
case 2:
case 4:
var text=node.childNodes[i].nodeValue;
var _3f9="unknown";
try{
_3f9=dojo.style.getStyle(node,"text-transform");
}
catch(E){
}
switch(_3f9){
case "capitalize":
text=dojo.string.capitalize(text);
break;
case "uppercase":
text=text.toUpperCase();
break;
case "lowercase":
text=text.toLowerCase();
break;
default:
break;
}
switch(_3f9){
case "nowrap":
break;
case "pre-wrap":
break;
case "pre-line":
break;
case "pre":
break;
default:
text=text.replace(/\s+/," ");
if(/\s$/.test(_3f5)){
text.replace(/^\s/,"");
}
break;
}
_3f5+=text;
break;
default:
break;
}
}
return _3f5;
};
dojo.html.setActiveStyleSheet=function(_3fa){
var i,a,main;
for(i=0;(a=document.getElementsByTagName("link")[i]);i++){
if(a.getAttribute("rel").indexOf("style")!=-1&&a.getAttribute("title")){
a.disabled=true;
if(a.getAttribute("title")==_3fa){
a.disabled=false;
}
}
}
};
dojo.html.getActiveStyleSheet=function(){
var i,a;
for(i=0;(a=document.getElementsByTagName("link")[i]);i++){
if(a.getAttribute("rel").indexOf("style")!=-1&&a.getAttribute("title")&&!a.disabled){
return a.getAttribute("title");
}
}
return null;
};
dojo.html.getPreferredStyleSheet=function(){
var i,a;
for(i=0;(a=document.getElementsByTagName("link")[i]);i++){
if(a.getAttribute("rel").indexOf("style")!=-1&&a.getAttribute("rel").indexOf("alt")==-1&&a.getAttribute("title")){
return a.getAttribute("title");
}
}
return null;
};
dojo.html.body=function(){
return document.body||document.getElementsByTagName("body")[0];
};
dojo.html.createNodesFromText=function(txt,trim){
if(trim){
txt=dojo.string.trim(txt);
}
var tn=document.createElement("div");
tn.style.visibility="hidden";
document.body.appendChild(tn);
var _401="none";
if((/^<t[dh][\s\r\n>]/i).test(dojo.string.trimStart(txt))){
txt="<table><tbody><tr>"+txt+"</tr></tbody></table>";
_401="cell";
}else{
if((/^<tr[\s\r\n>]/i).test(dojo.string.trimStart(txt))){
txt="<table><tbody>"+txt+"</tbody></table>";
_401="row";
}else{
if((/^<(thead|tbody|tfoot)[\s\r\n>]/i).test(dojo.string.trimStart(txt))){
txt="<table>"+txt+"</table>";
_401="section";
}
}
}
tn.innerHTML=txt;
tn.normalize();
var _402=null;
switch(_401){
case "cell":
_402=tn.getElementsByTagName("tr")[0];
break;
case "row":
_402=tn.getElementsByTagName("tbody")[0];
break;
case "section":
_402=tn.getElementsByTagName("table")[0];
break;
default:
_402=tn;
break;
}
var _403=[];
for(var x=0;x<_402.childNodes.length;x++){
_403.push(_402.childNodes[x].cloneNode(true));
}
tn.style.display="none";
document.body.removeChild(tn);
return _403;
};
if(!dojo.evalObjPath("dojo.dom.createNodesFromText")){
dojo.dom.createNodesFromText=function(){
dojo.deprecated("dojo.dom.createNodesFromText","use dojo.html.createNodesFromText instead");
return dojo.html.createNodesFromText.apply(dojo.html,arguments);
};
}
dojo.html.isVisible=function(node){
node=dojo.byId(node);
return dojo.style.getComputedStyle(node||this.domNode,"display")!="none";
};
dojo.html.show=function(node){
node=dojo.byId(node);
if(node.style){
node.style.display=dojo.lang.inArray(["tr","td","th"],node.tagName.toLowerCase())?"":"block";
}
};
dojo.html.hide=function(node){
node=dojo.byId(node);
if(node.style){
node.style.display="none";
}
};
dojo.html.toggleVisible=function(node){
if(dojo.html.isVisible(node)){
dojo.html.hide(node);
return false;
}else{
dojo.html.show(node);
return true;
}
};
dojo.html.isTag=function(node){
node=dojo.byId(node);
if(node&&node.tagName){
var arr=dojo.lang.map(dojo.lang.toArray(arguments,1),function(a){
return String(a).toLowerCase();
});
return arr[dojo.lang.find(node.tagName.toLowerCase(),arr)]||"";
}
return "";
};
dojo.html.toCoordinateArray=function(_40c,_40d){
if(dojo.lang.isArray(_40c)){
while(_40c.length<4){
_40c.push(0);
}
while(_40c.length>4){
_40c.pop();
}
var ret=_40c;
}else{
var node=dojo.byId(_40c);
var ret=[dojo.html.getAbsoluteX(node,_40d),dojo.html.getAbsoluteY(node,_40d),dojo.html.getInnerWidth(node),dojo.html.getInnerHeight(node)];
}
ret.x=ret[0];
ret.y=ret[1];
ret.w=ret[2];
ret.h=ret[3];
return ret;
};
dojo.html.placeOnScreen=function(node,_411,_412,_413,_414){
if(dojo.lang.isArray(_411)){
_414=_413;
_413=_412;
_412=_411[1];
_411=_411[0];
}
if(!isNaN(_413)){
_413=[Number(_413),Number(_413)];
}else{
if(!dojo.lang.isArray(_413)){
_413=[0,0];
}
}
var _415=dojo.html.getScrollOffset();
var view=dojo.html.getViewportSize();
node=dojo.byId(node);
var w=node.offsetWidth+_413[0];
var h=node.offsetHeight+_413[1];
if(_414){
_411-=_415.x;
_412-=_415.y;
}
var x=_411+w;
if(x>view.w){
x=view.w-w;
}else{
x=_411;
}
x=Math.max(_413[0],x)+_415.x;
var y=_412+h;
if(y>view.h){
y=view.h-h;
}else{
y=_412;
}
y=Math.max(_413[1],y)+_415.y;
node.style.left=x+"px";
node.style.top=y+"px";
var ret=[x,y];
ret.x=x;
ret.y=y;
return ret;
};
dojo.html.placeOnScreenPoint=function(node,_41d,_41e,_41f,_420){
if(dojo.lang.isArray(_41d)){
_420=_41f;
_41f=_41e;
_41e=_41d[1];
_41d=_41d[0];
}
var _421=dojo.html.getScrollOffset();
var view=dojo.html.getViewportSize();
node=dojo.byId(node);
var w=node.offsetWidth;
var h=node.offsetHeight;
if(_420){
_41d-=_421.x;
_41e-=_421.y;
}
var x=-1,y=-1;
if(_41d+w<=view.w&&_41e+h<=view.h){
x=_41d;
y=_41e;
}
if((x<0||y<0)&&_41d<=view.w&&_41e+h<=view.h){
x=_41d-w;
y=_41e;
}
if((x<0||y<0)&&_41d+w<=view.w&&_41e<=view.h){
x=_41d;
y=_41e-h;
}
if((x<0||y<0)&&_41d<=view.w&&_41e<=view.h){
x=_41d-w;
y=_41e-h;
}
if(x<0||y<0||(x+w>view.w)||(y+h>view.h)){
return dojo.html.placeOnScreen(node,_41d,_41e,_41f,_420);
}
x+=_421.x;
y+=_421.y;
node.style.left=x+"px";
node.style.top=y+"px";
var ret=[x,y];
ret.x=x;
ret.y=y;
return ret;
};
dojo.html.BackgroundIframe=function(){
if(this.ie){
this.iframe=document.createElement("<iframe frameborder='0' src='about:blank'>");
var s=this.iframe.style;
s.position="absolute";
s.left=s.top="0px";
s.zIndex=2;
s.display="none";
dojo.style.setOpacity(this.iframe,0);
dojo.html.body().appendChild(this.iframe);
}else{
this.enabled=false;
}
};
dojo.lang.extend(dojo.html.BackgroundIframe,{ie:dojo.render.html.ie,enabled:true,visibile:false,iframe:null,sizeNode:null,sizeCoords:null,size:function(node){
if(!this.ie||!this.enabled){
return;
}
if(dojo.dom.isNode(node)){
this.sizeNode=node;
}else{
if(arguments.length>0){
this.sizeNode=null;
this.sizeCoords=node;
}
}
this.update();
},update:function(){
if(!this.ie||!this.enabled){
return;
}
if(this.sizeNode){
this.sizeCoords=dojo.html.toCoordinateArray(this.sizeNode,true);
}else{
if(this.sizeCoords){
this.sizeCoords=dojo.html.toCoordinateArray(this.sizeCoords,true);
}else{
return;
}
}
var s=this.iframe.style;
var dims=this.sizeCoords;
s.width=dims.w+"px";
s.height=dims.h+"px";
s.left=dims.x+"px";
s.top=dims.y+"px";
},setZIndex:function(node){
if(!this.ie||!this.enabled){
return;
}
if(dojo.dom.isNode(node)){
this.iframe.zIndex=dojo.html.getStyle(node,"z-index")-1;
}else{
if(!isNaN(node)){
this.iframe.zIndex=node;
}
}
},show:function(node){
if(!this.ie||!this.enabled){
return;
}
this.size(node);
this.iframe.style.display="block";
},hide:function(){
if(!this.ie){
return;
}
var s=this.iframe.style;
s.display="none";
s.width=s.height="1px";
},remove:function(){
dojo.dom.removeNode(this.iframe);
}});
dojo.provide("dojo.math.curves");
dojo.require("dojo.math");
dojo.math.curves={Line:function(_42e,end){
this.start=_42e;
this.end=end;
this.dimensions=_42e.length;
for(var i=0;i<_42e.length;i++){
_42e[i]=Number(_42e[i]);
}
for(var i=0;i<end.length;i++){
end[i]=Number(end[i]);
}
this.getValue=function(n){
var _432=new Array(this.dimensions);
for(var i=0;i<this.dimensions;i++){
_432[i]=((this.end[i]-this.start[i])*n)+this.start[i];
}
return _432;
};
return this;
},Bezier:function(pnts){
this.getValue=function(step){
if(step>=1){
return this.p[this.p.length-1];
}
if(step<=0){
return this.p[0];
}
var _436=new Array(this.p[0].length);
for(var k=0;j<this.p[0].length;k++){
_436[k]=0;
}
for(var j=0;j<this.p[0].length;j++){
var C=0;
var D=0;
for(var i=0;i<this.p.length;i++){
C+=this.p[i][j]*this.p[this.p.length-1][0]*dojo.math.bernstein(step,this.p.length,i);
}
for(var l=0;l<this.p.length;l++){
D+=this.p[this.p.length-1][0]*dojo.math.bernstein(step,this.p.length,l);
}
_436[j]=C/D;
}
return _436;
};
this.p=pnts;
return this;
},CatmullRom:function(pnts,c){
this.getValue=function(step){
var _440=step*(this.p.length-1);
var node=Math.floor(_440);
var _442=_440-node;
var i0=node-1;
if(i0<0){
i0=0;
}
var i=node;
var i1=node+1;
if(i1>=this.p.length){
i1=this.p.length-1;
}
var i2=node+2;
if(i2>=this.p.length){
i2=this.p.length-1;
}
var u=_442;
var u2=_442*_442;
var u3=_442*_442*_442;
var _44a=new Array(this.p[0].length);
for(var k=0;k<this.p[0].length;k++){
var x1=(-this.c*this.p[i0][k])+((2-this.c)*this.p[i][k])+((this.c-2)*this.p[i1][k])+(this.c*this.p[i2][k]);
var x2=(2*this.c*this.p[i0][k])+((this.c-3)*this.p[i][k])+((3-2*this.c)*this.p[i1][k])+(-this.c*this.p[i2][k]);
var x3=(-this.c*this.p[i0][k])+(this.c*this.p[i1][k]);
var x4=this.p[i][k];
_44a[k]=x1*u3+x2*u2+x3*u+x4;
}
return _44a;
};
if(!c){
this.c=0.7;
}else{
this.c=c;
}
this.p=pnts;
return this;
},Arc:function(_450,end,ccw){
var _453=dojo.math.points.midpoint(_450,end);
var _454=dojo.math.points.translate(dojo.math.points.invert(_453),_450);
var rad=Math.sqrt(Math.pow(_454[0],2)+Math.pow(_454[1],2));
var _456=dojo.math.radToDeg(Math.atan(_454[1]/_454[0]));
if(_454[0]<0){
_456-=90;
}else{
_456+=90;
}
dojo.math.curves.CenteredArc.call(this,_453,rad,_456,_456+(ccw?-180:180));
},CenteredArc:function(_457,_458,_459,end){
this.center=_457;
this.radius=_458;
this.start=_459||0;
this.end=end;
this.getValue=function(n){
var _45c=new Array(2);
var _45d=dojo.math.degToRad(this.start+((this.end-this.start)*n));
_45c[0]=this.center[0]+this.radius*Math.sin(_45d);
_45c[1]=this.center[1]-this.radius*Math.cos(_45d);
return _45c;
};
return this;
},Circle:function(_45e,_45f){
dojo.math.curves.CenteredArc.call(this,_45e,_45f,0,360);
return this;
},Path:function(){
var _460=[];
var _461=[];
var _462=[];
var _463=0;
this.add=function(_464,_465){
if(_465<0){
dojo.raise("dojo.math.curves.Path.add: weight cannot be less than 0");
}
_460.push(_464);
_461.push(_465);
_463+=_465;
computeRanges();
};
this.remove=function(_466){
for(var i=0;i<_460.length;i++){
if(_460[i]==_466){
_460.splice(i,1);
_463-=_461.splice(i,1)[0];
break;
}
}
computeRanges();
};
this.removeAll=function(){
_460=[];
_461=[];
_463=0;
};
this.getValue=function(n){
var _469=false,value=0;
for(var i=0;i<_462.length;i++){
var r=_462[i];
if(n>=r[0]&&n<r[1]){
var subN=(n-r[0])/r[2];
value=_460[i].getValue(subN);
_469=true;
break;
}
}
if(!_469){
value=_460[_460.length-1].getValue(1);
}
for(j=0;j<i;j++){
value=dojo.math.points.translate(value,_460[j].getValue(1));
}
return value;
};
function computeRanges(){
var _46d=0;
for(var i=0;i<_461.length;i++){
var end=_46d+_461[i]/_463;
var len=end-_46d;
_462[i]=[_46d,end,len];
_46d=end;
}
}
return this;
}};
dojo.provide("dojo.animation");
dojo.provide("dojo.animation.Animation");
dojo.require("dojo.lang");
dojo.require("dojo.math");
dojo.require("dojo.math.curves");
dojo.animation.Animation=function(_471,_472,_473,_474,rate){
if(dojo.lang.isArray(_471)){
_471=new dojo.math.curves.Line(_471[0],_471[1]);
}
this.curve=_471;
this.duration=_472;
this.repeatCount=_474||0;
this.rate=rate||25;
if(_473){
if(dojo.lang.isFunction(_473.getValue)){
this.accel=_473;
}else{
var i=0.35*_473+0.5;
this.accel=new dojo.math.curves.CatmullRom([[0],[i],[1]],0.45);
}
}
};
dojo.lang.extend(dojo.animation.Animation,{curve:null,duration:0,repeatCount:0,accel:null,onBegin:null,onAnimate:null,onEnd:null,onPlay:null,onPause:null,onStop:null,handler:null,_animSequence:null,_startTime:null,_endTime:null,_lastFrame:null,_timer:null,_percent:0,_active:false,_paused:false,_startRepeatCount:0,play:function(_477){
if(_477){
clearTimeout(this._timer);
this._active=false;
this._paused=false;
this._percent=0;
}else{
if(this._active&&!this._paused){
return;
}
}
this._startTime=new Date().valueOf();
if(this._paused){
this._startTime-=(this.duration*this._percent/100);
}
this._endTime=this._startTime+this.duration;
this._lastFrame=this._startTime;
var e=new dojo.animation.AnimationEvent(this,null,this.curve.getValue(this._percent),this._startTime,this._startTime,this._endTime,this.duration,this._percent,0);
this._active=true;
this._paused=false;
if(this._percent==0){
if(!this._startRepeatCount){
this._startRepeatCount=this.repeatCount;
}
e.type="begin";
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onBegin=="function"){
this.onBegin(e);
}
}
e.type="play";
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onPlay=="function"){
this.onPlay(e);
}
if(this._animSequence){
this._animSequence._setCurrent(this);
}
this._cycle();
},pause:function(){
clearTimeout(this._timer);
if(!this._active){
return;
}
this._paused=true;
var e=new dojo.animation.AnimationEvent(this,"pause",this.curve.getValue(this._percent),this._startTime,new Date().valueOf(),this._endTime,this.duration,this._percent,0);
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onPause=="function"){
this.onPause(e);
}
},playPause:function(){
if(!this._active||this._paused){
this.play();
}else{
this.pause();
}
},gotoPercent:function(pct,_47b){
clearTimeout(this._timer);
this._active=true;
this._paused=true;
this._percent=pct;
if(_47b){
this.play();
}
},stop:function(_47c){
clearTimeout(this._timer);
var step=this._percent/100;
if(_47c){
step=1;
}
var e=new dojo.animation.AnimationEvent(this,"stop",this.curve.getValue(step),this._startTime,new Date().valueOf(),this._endTime,this.duration,this._percent,Math.round(fps));
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onStop=="function"){
this.onStop(e);
}
this._active=false;
this._paused=false;
},status:function(){
if(this._active){
return this._paused?"paused":"playing";
}else{
return "stopped";
}
},_cycle:function(){
clearTimeout(this._timer);
if(this._active){
var curr=new Date().valueOf();
var step=(curr-this._startTime)/(this._endTime-this._startTime);
fps=1000/(curr-this._lastFrame);
this._lastFrame=curr;
if(step>=1){
step=1;
this._percent=100;
}else{
this._percent=step*100;
}
if(this.accel&&this.accel.getValue){
step=this.accel.getValue(step);
}
var e=new dojo.animation.AnimationEvent(this,"animate",this.curve.getValue(step),this._startTime,curr,this._endTime,this.duration,this._percent,Math.round(fps));
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onAnimate=="function"){
this.onAnimate(e);
}
if(step<1){
this._timer=setTimeout(dojo.lang.hitch(this,"_cycle"),this.rate);
}else{
e.type="end";
this._active=false;
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onEnd=="function"){
this.onEnd(e);
}
if(this.repeatCount>0){
this.repeatCount--;
this.play(true);
}else{
if(this.repeatCount==-1){
this.play(true);
}else{
if(this._startRepeatCount){
this.repeatCount=this._startRepeatCount;
this._startRepeatCount=0;
}
if(this._animSequence){
this._animSequence._playNext();
}
}
}
}
}
}});
dojo.animation.AnimationEvent=function(anim,type,_484,_485,_486,_487,dur,pct,fps){
this.type=type;
this.animation=anim;
this.coords=_484;
this.x=_484[0];
this.y=_484[1];
this.z=_484[2];
this.startTime=_485;
this.currentTime=_486;
this.endTime=_487;
this.duration=dur;
this.percent=pct;
this.fps=fps;
};
dojo.lang.extend(dojo.animation.AnimationEvent,{coordsAsInts:function(){
var _48b=new Array(this.coords.length);
for(var i=0;i<this.coords.length;i++){
_48b[i]=Math.round(this.coords[i]);
}
return _48b;
}});
dojo.animation.AnimationSequence=function(_48d){
this._anims=[];
this.repeatCount=_48d||0;
};
dojo.lang.extend(dojo.animation.AnimationSequence,{repeateCount:0,_anims:[],_currAnim:-1,onBegin:null,onEnd:null,onNext:null,handler:null,add:function(){
for(var i=0;i<arguments.length;i++){
this._anims.push(arguments[i]);
arguments[i]._animSequence=this;
}
},remove:function(anim){
for(var i=0;i<this._anims.length;i++){
if(this._anims[i]==anim){
this._anims[i]._animSequence=null;
this._anims.splice(i,1);
break;
}
}
},removeAll:function(){
for(var i=0;i<this._anims.length;i++){
this._anims[i]._animSequence=null;
}
this._anims=[];
this._currAnim=-1;
},clear:function(){
this.removeAll();
},play:function(_492){
if(this._anims.length==0){
return;
}
if(_492||!this._anims[this._currAnim]){
this._currAnim=0;
}
if(this._anims[this._currAnim]){
if(this._currAnim==0){
var e={type:"begin",animation:this._anims[this._currAnim]};
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onBegin=="function"){
this.onBegin(e);
}
}
this._anims[this._currAnim].play(_492);
}
},pause:function(){
if(this._anims[this._currAnim]){
this._anims[this._currAnim].pause();
}
},playPause:function(){
if(this._anims.length==0){
return;
}
if(this._currAnim==-1){
this._currAnim=0;
}
if(this._anims[this._currAnim]){
this._anims[this._currAnim].playPause();
}
},stop:function(){
if(this._anims[this._currAnim]){
this._anims[this._currAnim].stop();
}
},status:function(){
if(this._anims[this._currAnim]){
return this._anims[this._currAnim].status();
}else{
return "stopped";
}
},_setCurrent:function(anim){
for(var i=0;i<this._anims.length;i++){
if(this._anims[i]==anim){
this._currAnim=i;
break;
}
}
},_playNext:function(){
if(this._currAnim==-1||this._anims.length==0){
return;
}
this._currAnim++;
if(this._anims[this._currAnim]){
var e={type:"next",animation:this._anims[this._currAnim]};
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onNext=="function"){
this.onNext(e);
}
this._anims[this._currAnim].play(true);
}else{
var e={type:"end",animation:this._anims[this._anims.length-1]};
if(typeof this.handler=="function"){
this.handler(e);
}
if(typeof this.onEnd=="function"){
this.onEnd(e);
}
if(this.repeatCount>0){
this._currAnim=0;
this.repeatCount--;
this._anims[this._currAnim].play(true);
}else{
if(this.repeatCount==-1){
this._currAnim=0;
this._anims[this._currAnim].play(true);
}else{
this._currAnim=-1;
}
}
}
}});
dojo.hostenv.conditionalLoadModule({common:["dojo.animation.Animation",false,false]});
dojo.hostenv.moduleLoaded("dojo.animation.*");
dojo.provide("dojo.fx.html");
dojo.require("dojo.html");
dojo.require("dojo.style");
dojo.require("dojo.lang");
dojo.require("dojo.animation.*");
dojo.require("dojo.event.*");
dojo.require("dojo.graphics.color");
dojo.fx.duration=500;
dojo.fx.html._makeFadeable=function(node){
if(dojo.render.html.ie){
if((node.style.zoom.length==0)&&(dojo.style.getStyle(node,"zoom")=="normal")){
node.style.zoom="1";
}
if((node.style.width.length==0)&&(dojo.style.getStyle(node,"width")=="auto")){
node.style.width="auto";
}
}
};
dojo.fx.html.fadeOut=function(node,_499,_49a,_49b){
return dojo.fx.html.fade(node,_499,dojo.style.getOpacity(node),0,_49a,_49b);
};
dojo.fx.html.fadeIn=function(node,_49d,_49e,_49f){
return dojo.fx.html.fade(node,_49d,dojo.style.getOpacity(node),1,_49e,_49f);
};
dojo.fx.html.fadeHide=function(node,_4a1,_4a2,_4a3){
node=dojo.byId(node);
if(!_4a1){
_4a1=150;
}
return dojo.fx.html.fadeOut(node,_4a1,function(node){
node.style.display="none";
if(typeof _4a2=="function"){
_4a2(node);
}
});
};
dojo.fx.html.fadeShow=function(node,_4a6,_4a7,_4a8){
node=dojo.byId(node);
if(!_4a6){
_4a6=150;
}
node.style.display="block";
return dojo.fx.html.fade(node,_4a6,0,1,_4a7,_4a8);
};
dojo.fx.html.fade=function(node,_4aa,_4ab,_4ac,_4ad,_4ae){
node=dojo.byId(node);
dojo.fx.html._makeFadeable(node);
var anim=new dojo.animation.Animation(new dojo.math.curves.Line([_4ab],[_4ac]),_4aa||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
dojo.style.setOpacity(node,e.x);
});
if(_4ad){
dojo.event.connect(anim,"onEnd",function(e){
_4ad(node,anim);
});
}
if(!_4ae){
anim.play(true);
}
return anim;
};
dojo.fx.html.slideTo=function(node,_4b3,_4b4,_4b5,_4b6){
if(!dojo.lang.isNumber(_4b3)){
var tmp=_4b3;
_4b3=_4b4;
_4b4=tmp;
}
node=dojo.byId(node);
var top=node.offsetTop;
var left=node.offsetLeft;
var pos=dojo.style.getComputedStyle(node,"position");
if(pos=="relative"||pos=="static"){
top=parseInt(dojo.style.getComputedStyle(node,"top"))||0;
left=parseInt(dojo.style.getComputedStyle(node,"left"))||0;
}
return dojo.fx.html.slide(node,_4b3,[left,top],_4b4,_4b5,_4b6);
};
dojo.fx.html.slideBy=function(node,_4bc,_4bd,_4be,_4bf){
if(!dojo.lang.isNumber(_4bc)){
var tmp=_4bc;
_4bc=_4bd;
_4bd=tmp;
}
node=dojo.byId(node);
var top=node.offsetTop;
var left=node.offsetLeft;
var pos=dojo.style.getComputedStyle(node,"position");
if(pos=="relative"||pos=="static"){
top=parseInt(dojo.style.getComputedStyle(node,"top"))||0;
left=parseInt(dojo.style.getComputedStyle(node,"left"))||0;
}
return dojo.fx.html.slideTo(node,_4bc,[left+_4bd[0],top+_4bd[1]],_4be,_4bf);
};
dojo.fx.html.slide=function(node,_4c5,_4c6,_4c7,_4c8,_4c9){
if(!dojo.lang.isNumber(_4c5)){
var tmp=_4c5;
_4c5=_4c7;
_4c7=_4c6;
_4c6=tmp;
}
node=dojo.byId(node);
if(dojo.style.getComputedStyle(node,"position")=="static"){
node.style.position="relative";
}
var anim=new dojo.animation.Animation(new dojo.math.curves.Line(_4c6,_4c7),_4c5||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
with(node.style){
left=e.x+"px";
top=e.y+"px";
}
});
if(_4c8){
dojo.event.connect(anim,"onEnd",function(e){
_4c8(node,anim);
});
}
if(!_4c9){
anim.play(true);
}
return anim;
};
dojo.fx.html.colorFadeIn=function(node,_4cf,_4d0,_4d1,_4d2,_4d3){
if(!dojo.lang.isNumber(_4cf)){
var tmp=_4cf;
_4cf=_4d0;
_4d0=tmp;
}
node=dojo.byId(node);
var _4d5=dojo.html.getBackgroundColor(node);
var bg=dojo.style.getStyle(node,"background-color").toLowerCase();
var _4d7=bg=="transparent"||bg=="rgba(0, 0, 0, 0)";
while(_4d5.length>3){
_4d5.pop();
}
var rgb=new dojo.graphics.color.Color(_4d0).toRgb();
var anim=dojo.fx.html.colorFade(node,_4cf||dojo.fx.duration,_4d0,_4d5,_4d2,true);
dojo.event.connect(anim,"onEnd",function(e){
if(_4d7){
node.style.backgroundColor="transparent";
}
});
if(_4d1>0){
node.style.backgroundColor="rgb("+rgb.join(",")+")";
if(!_4d3){
setTimeout(function(){
anim.play(true);
},_4d1);
}
}else{
if(!_4d3){
anim.play(true);
}
}
return anim;
};
dojo.fx.html.highlight=dojo.fx.html.colorFadeIn;
dojo.fx.html.colorFadeFrom=dojo.fx.html.colorFadeIn;
dojo.fx.html.colorFadeOut=function(node,_4dc,_4dd,_4de,_4df,_4e0){
if(!dojo.lang.isNumber(_4dc)){
var tmp=_4dc;
_4dc=_4dd;
_4dd=tmp;
}
node=dojo.byId(node);
var _4e2=new dojo.graphics.color.Color(dojo.html.getBackgroundColor(node)).toRgb();
var rgb=new dojo.graphics.color.Color(_4dd).toRgb();
var anim=dojo.fx.html.colorFade(node,_4dc||dojo.fx.duration,_4e2,rgb,_4df,_4de>0||_4e0);
if(_4de>0){
node.style.backgroundColor="rgb("+_4e2.join(",")+")";
if(!_4e0){
setTimeout(function(){
anim.play(true);
},_4de);
}
}
return anim;
};
dojo.fx.html.unhighlight=dojo.fx.html.colorFadeOut;
dojo.fx.html.colorFadeTo=dojo.fx.html.colorFadeOut;
dojo.fx.html.colorFade=function(node,_4e6,_4e7,_4e8,_4e9,_4ea){
if(!dojo.lang.isNumber(_4e6)){
var tmp=_4e6;
_4e6=_4e8;
_4e8=_4e7;
_4e7=tmp;
}
node=dojo.byId(node);
var _4ec=new dojo.graphics.color.Color(_4e7).toRgb();
var _4ed=new dojo.graphics.color.Color(_4e8).toRgb();
var anim=new dojo.animation.Animation(new dojo.math.curves.Line(_4ec,_4ed),_4e6||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
node.style.backgroundColor="rgb("+e.coordsAsInts().join(",")+")";
});
if(_4e9){
dojo.event.connect(anim,"onEnd",function(e){
_4e9(node,anim);
});
}
if(!_4ea){
anim.play(true);
}
return anim;
};
dojo.fx.html.wipeShow=function(node,_4f2,_4f3,_4f4){
node=dojo.byId(node);
var _4f5=dojo.html.getStyle(node,"overflow");
node.style.overflow="hidden";
node.style.height=0;
dojo.html.show(node);
var anim=new dojo.animation.Animation([[0],[node.scrollHeight]],_4f2||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
node.style.height=e.x+"px";
});
dojo.event.connect(anim,"onEnd",function(){
node.style.overflow=_4f5;
node.style.height="auto";
if(_4f3){
_4f3(node,anim);
}
});
if(!_4f4){
anim.play();
}
return anim;
};
dojo.fx.html.wipeHide=function(node,_4f9,_4fa,_4fb){
node=dojo.byId(node);
var _4fc=dojo.html.getStyle(node,"overflow");
node.style.overflow="hidden";
var anim=new dojo.animation.Animation([[node.offsetHeight],[0]],_4f9||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
node.style.height=e.x+"px";
});
dojo.event.connect(anim,"onEnd",function(){
node.style.overflow=_4fc;
dojo.html.hide(node);
if(_4fa){
_4fa(node,anim);
}
});
if(!_4fb){
anim.play();
}
return anim;
};
dojo.fx.html.wiper=function(node,_500){
this.node=dojo.byId(node);
if(_500){
dojo.event.connect(dojo.byId(_500),"onclick",this,"toggle");
}
};
dojo.lang.extend(dojo.fx.html.wiper,{duration:dojo.fx.duration,_anim:null,toggle:function(){
if(!this._anim){
var type="wipe"+(dojo.html.isVisible(this.node)?"Hide":"Show");
this._anim=dojo.fx[type](this.node,this.duration,dojo.lang.hitch(this,"_callback"));
}
},_callback:function(){
this._anim=null;
}});
dojo.fx.html.wipeIn=function(node,_503,_504,_505){
node=dojo.byId(node);
var _506=dojo.html.getStyle(node,"height");
dojo.html.show(node);
var _507=node.offsetHeight;
var anim=dojo.fx.html.wipeInToHeight(node,_503,_507,function(e){
node.style.height=_506||"auto";
if(_504){
_504(node,anim);
}
},_505);
};
dojo.fx.html.wipeInToHeight=function(node,_50b,_50c,_50d,_50e){
node=dojo.byId(node);
var _50f=dojo.html.getStyle(node,"overflow");
node.style.height="0px";
node.style.display="none";
if(_50f=="visible"){
node.style.overflow="hidden";
}
var _510=dojo.lang.inArray(node.tagName.toLowerCase(),["tr","td","th"])?"":"block";
node.style.display=_510;
var anim=new dojo.animation.Animation(new dojo.math.curves.Line([0],[_50c]),_50b||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
node.style.height=Math.round(e.x)+"px";
});
dojo.event.connect(anim,"onEnd",function(e){
if(_50f!="visible"){
node.style.overflow=_50f;
}
if(_50d){
_50d(node,anim);
}
});
if(!_50e){
anim.play(true);
}
return anim;
};
dojo.fx.html.wipeOut=function(node,_515,_516,_517){
node=dojo.byId(node);
var _518=dojo.html.getStyle(node,"overflow");
var _519=dojo.html.getStyle(node,"height");
var _51a=node.offsetHeight;
node.style.overflow="hidden";
var anim=new dojo.animation.Animation(new dojo.math.curves.Line([_51a],[0]),_515||dojo.fx.duration,0);
dojo.event.connect(anim,"onAnimate",function(e){
node.style.height=Math.round(e.x)+"px";
});
dojo.event.connect(anim,"onEnd",function(e){
node.style.display="none";
node.style.overflow=_518;
node.style.height=_519||"auto";
if(_516){
_516(node,anim);
}
});
if(!_517){
anim.play(true);
}
return anim;
};
dojo.fx.html.explode=function(_51e,_51f,_520,_521,_522){
var _523=dojo.html.toCoordinateArray(_51e);
var _524=document.createElement("div");
with(_524.style){
position="absolute";
border="1px solid black";
display="none";
}
dojo.html.body().appendChild(_524);
_51f=dojo.byId(_51f);
with(_51f.style){
visibility="hidden";
display="block";
}
var _525=dojo.html.toCoordinateArray(_51f);
with(_51f.style){
display="none";
visibility="visible";
}
var anim=new dojo.animation.Animation(new dojo.math.curves.Line(_523,_525),_520||dojo.fx.duration,0);
dojo.event.connect(anim,"onBegin",function(e){
_524.style.display="block";
});
dojo.event.connect(anim,"onAnimate",function(e){
with(_524.style){
left=e.x+"px";
top=e.y+"px";
width=e.coords[2]+"px";
height=e.coords[3]+"px";
}
});
dojo.event.connect(anim,"onEnd",function(){
_51f.style.display="block";
_524.parentNode.removeChild(_524);
if(_521){
_521(_51f,anim);
}
});
if(!_522){
anim.play();
}
return anim;
};
dojo.fx.html.implode=function(_529,end,_52b,_52c,_52d){
var _52e=dojo.html.toCoordinateArray(_529);
var _52f=dojo.html.toCoordinateArray(end);
_529=dojo.byId(_529);
var _530=document.createElement("div");
with(_530.style){
position="absolute";
border="1px solid black";
display="none";
}
dojo.html.body().appendChild(_530);
var anim=new dojo.animation.Animation(new dojo.math.curves.Line(_52e,_52f),_52b||dojo.fx.duration,0);
dojo.event.connect(anim,"onBegin",function(e){
_529.style.display="none";
_530.style.display="block";
});
dojo.event.connect(anim,"onAnimate",function(e){
with(_530.style){
left=e.x+"px";
top=e.y+"px";
width=e.coords[2]+"px";
height=e.coords[3]+"px";
}
});
dojo.event.connect(anim,"onEnd",function(){
_530.parentNode.removeChild(_530);
if(_52c){
_52c(_529,anim);
}
});
if(!_52d){
anim.play();
}
return anim;
};
dojo.fx.html.Exploder=function(_534,_535){
_534=dojo.byId(_534);
_535=dojo.byId(_535);
var _536=this;
this.waitToHide=500;
this.timeToShow=100;
this.waitToShow=200;
this.timeToHide=70;
this.autoShow=false;
this.autoHide=false;
var _537=null;
var _538=null;
var _539=null;
var _53a=null;
var _53b=null;
var _53c=null;
this.showing=false;
this.onBeforeExplode=null;
this.onAfterExplode=null;
this.onBeforeImplode=null;
this.onAfterImplode=null;
this.onExploding=null;
this.onImploding=null;
this.timeShow=function(){
clearTimeout(_539);
_539=setTimeout(_536.show,_536.waitToShow);
};
this.show=function(){
clearTimeout(_539);
clearTimeout(_53a);
if((_538&&_538.status()=="playing")||(_537&&_537.status()=="playing")||_536.showing){
return;
}
if(typeof _536.onBeforeExplode=="function"){
_536.onBeforeExplode(_534,_535);
}
_537=dojo.fx.html.explode(_534,_535,_536.timeToShow,function(e){
_536.showing=true;
if(typeof _536.onAfterExplode=="function"){
_536.onAfterExplode(_534,_535);
}
});
if(typeof _536.onExploding=="function"){
dojo.event.connect(_537,"onAnimate",this,"onExploding");
}
};
this.timeHide=function(){
clearTimeout(_539);
clearTimeout(_53a);
if(_536.showing){
_53a=setTimeout(_536.hide,_536.waitToHide);
}
};
this.hide=function(){
clearTimeout(_539);
clearTimeout(_53a);
if(_537&&_537.status()=="playing"){
return;
}
_536.showing=false;
if(typeof _536.onBeforeImplode=="function"){
_536.onBeforeImplode(_534,_535);
}
_538=dojo.fx.html.implode(_535,_534,_536.timeToHide,function(e){
if(typeof _536.onAfterImplode=="function"){
_536.onAfterImplode(_534,_535);
}
});
if(typeof _536.onImploding=="function"){
dojo.event.connect(_538,"onAnimate",this,"onImploding");
}
};
dojo.event.connect(_534,"onclick",function(e){
if(_536.showing){
_536.hide();
}else{
_536.show();
}
});
dojo.event.connect(_534,"onmouseover",function(e){
if(_536.autoShow){
_536.timeShow();
}
});
dojo.event.connect(_534,"onmouseout",function(e){
if(_536.autoHide){
_536.timeHide();
}
});
dojo.event.connect(_535,"onmouseover",function(e){
clearTimeout(_53a);
});
dojo.event.connect(_535,"onmouseout",function(e){
if(_536.autoHide){
_536.timeHide();
}
});
dojo.event.connect(document.documentElement||dojo.html.body(),"onclick",function(e){
if(_536.autoHide&&_536.showing&&!dojo.dom.isDescendantOf(e.target,_535)&&!dojo.dom.isDescendantOf(e.target,_534)){
_536.hide();
}
});
return this;
};
dojo.lang.mixin(dojo.fx,dojo.fx.html);
dojo.hostenv.conditionalLoadModule({browser:["dojo.fx.html"]});
dojo.hostenv.moduleLoaded("dojo.fx.*");
dojo.provide("dojo.graphics.htmlEffects");
dojo.require("dojo.fx.*");
dj_deprecated("dojo.graphics.htmlEffects is deprecated, use dojo.fx.html instead");
dojo.graphics.htmlEffects=dojo.fx.html;
dojo.hostenv.conditionalLoadModule({browser:["dojo.graphics.htmlEffects"]});
dojo.hostenv.moduleLoaded("dojo.graphics.*");

