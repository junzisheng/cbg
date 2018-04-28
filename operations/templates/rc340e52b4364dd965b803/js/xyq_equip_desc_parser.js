
var StyleStart="#";var EquipDescRed="#R";var EquipDescGreen="#G";var EquipDescBlue="#B";var EquipDescBlack="#K";var EquipDescYellow="#Y";var EquipDescWhite="#W";var EquipDescBlink="#b";var EquipDescUnderline="#u";var EquipDescNormal="#n";var XyqCssSetting={"#R":"equip_desc_red","#G":"equip_desc_green","#B":"equip_desc_blue","#K":"equip_desc_black","#Y":"equip_desc_yellow","#W":"equip_desc_white","#b":"equip_desc_blink","#u":"equip_desc_underline","#n":"equip_desc_white"};var CommonStyleSet=[EquipDescRed,EquipDescGreen,EquipDescBlue,EquipDescBlack,EquipDescYellow,EquipDescWhite];var SepicalStyleSet=[EquipDescBlink,EquipDescUnderline];var ColorLen=6;function get_label_head_with_class(class_name){return"<span class='"+class_name+"'>";}
function get_label_head_with_color(color_value){return"<span style='color:#"+color_value+"'>";}
function get_label_tail(){return"</span>";}
function has_element(el_array,el){for(var i in el_array){if(el_array[i]==el){return true;}}
return false;}
var ClassStyle=0;var ColorStyle=1;function parse_style_info(equip_desc,DefaultCss){DefaultCss=(typeof(DefaultCss)=="undefined")?"#Y":DefaultCss
var result=get_label_head_with_class(XyqCssSetting[DefaultCss]),last_common_style={"kind":ClassStyle,"value":DefaultCss},spcial_class_stack=[];var i=0;var length=equip_desc.length;while(i<length){if(equip_desc.substring(i,i+1)!=StyleStart){result+=equip_desc.substring(i,i+1);i=i+1;continue;}
if(i==length-1){i=i+1;break;}
if(equip_desc.substring(i+1,i+1+1)=="#"){result+="#";i=i+1+1;continue;}
if(equip_desc.substring(i+1,i+1+1)=="r"){result+="<br>";i=i+1+1;continue;}
if(equip_desc.substring(i+1,i+1+1)=="c"){result+=get_label_tail();var color_start=i+1+1;var color_value=equip_desc.substring(color_start,color_start+ColorLen);result+=get_label_head_with_color(color_value);i=i+1+ColorLen+1;last_common_style["kind"]=ColorStyle;last_common_style["value"]=color_value;continue;}
var class_label=equip_desc.substring(i,i+2);if(has_element(CommonStyleSet,class_label)){result+=get_label_tail();result+=get_label_head_with_class(XyqCssSetting[class_label]);i=i+1+1;last_common_style["kind"]=ClassStyle;last_common_style["value"]=class_label;continue}
else if(has_element(SepicalStyleSet,class_label)){if(has_element(spcial_class_stack,class_label)){i=i+1+1;continue;}
result+=get_label_tail();result+=get_label_head_with_class(XyqCssSetting[class_label]);if(last_common_style["kind"]==ClassStyle){result+=get_label_head_with_class(XyqCssSetting[last_common_style["value"]]);}
else{result+=get_label_head_with_color(last_common_style["value"]);}
spcial_class_stack+=[class_label];i=i+1+1;continue;}
else if(class_label==EquipDescNormal){result+=get_label_tail()
for(var j=0;j<spcial_class_stack.length;j++){result+=get_label_tail()}
result+=get_label_head_with_class(XyqCssSetting[DefaultCss])
spcial_class_stack=[];i=i+1+1;}
else{i=i+1;continue;}}
result+=get_label_tail();for(var j=0;j<spcial_class_stack.length;j++){result+=get_label_tail();}
return result;}