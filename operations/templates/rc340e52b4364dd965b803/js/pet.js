
function correct_pet_desc(pet_desc){var num_re=/^[0-9]*$/;var PetAttrNum=33;var OldAttrNum=30;var OldestAttrNum=29;var AttrNum=pet_desc.split(";").length;if(AttrNum>=PetAttrNum||AttrNum==OldAttrNum||AttrNum==OldestAttrNum){return pet_desc;}
var sep_num=0;var check_num=PetAttrNum-1-1;var new_desc=""
for(var i=pet_desc.length-1;i>0;i--){var ch=pet_desc.charAt(i);if(ch!=";"&&ch!="|"&&!num_re.test(ch)){break;}else{new_desc=ch+new_desc;}}
if(new_desc.charAt(0)!=";"){new_desc=";"+new_desc;}
return"-"+new_desc;}
var check_undefined=function(item_value){if(item_value==undefined){return"未知";}else{return item_value;}};function get_yuanxiao(input_value){if(!input_value){return check_undefined(input_value);}
var agent_time=parseDatetime(EquipRequestTime);var cur_time=parseDatetime(ServerCurrentTime);var fresh_time=new Date(cur_time.getFullYear(),0,1);if(agent_time>fresh_time){return input_value;}else{return 0;}}
var get_ruyidan=get_yuanxiao;function get_lianshou(input_value){if(!input_value){return check_undefined(input_value);}
var agent_time=parseDatetime(EquipRequestTime);var cur_time=parseDatetime(ServerCurrentTime);var fresh_time=new Date(cur_time.getFullYear(),8,1);if(cur_time<fresh_time){fresh_time.setFullYear(fresh_time.getFullYear()-1);}
if(agent_time>fresh_time){return input_value;}else{return 0;}}
function get_pet_attrs_info(pet_desc,get_basic){var pet_desc=correct_pet_desc(pet_desc);var attrs=pet_desc.split(";");var get_baobao_info=function(is_baobao){if(is_baobao==undefined){return"未知";}
if(parseInt(is_baobao)){return"是";}else{return"否";}};var attrs_info={pet_name:attrs[0],pet_grade:attrs[2],blood:attrs[3],magic:attrs[4],attack:attrs[5],defence:attrs[6],speed:attrs[7],soma:attrs[9],magic_powner:attrs[10],strength:attrs[11],endurance:attrs[12],smartness:attrs[13],potential:attrs[14],wakan:attrs[15],max_blood:attrs[16],max_magic:attrs[17],lifetime:parseInt(attrs[18],10)>=65432?"永生":attrs[18],five_aptitude:attrs[19],attack_aptitude:attrs[20],defence_aptitude:attrs[21],physical_aptitude:attrs[22],magic_aptitude:attrs[23],speed_aptitude:attrs[24],avoid_aptitude:attrs[25],growth:parseInt(attrs[26],10)/1000,all_skill:attrs[27],sp_skill:attrs[28],is_baobao:get_baobao_info(attrs[29]),used_qianjinlu:check_undefined(attrs[32]),other:attrs[34],PET_WUXING_INFO:window.PET_WUXING_INFO||{}};var allSkills=attrs_info.all_skill?attrs_info.all_skill.split('|'):[];var spSkillId=(attrs_info.sp_skill||'0').toString().trim();if(spSkillId!='0'&&(attrs_info.all_skill||'').search(new RegExp('(^|\\|)'+spSkillId+'($|\\|)'))<0){allSkills.push(spSkillId);}
attrs_info.sp_skill_id=spSkillId;attrs_info.all_skills=allSkills;var other_attr={};if(attrs_info["other"]){var pos=pet_desc.indexOf(attrs_info["other"]);attrs_info["other"]=js_eval(lpc_2_js(pet_desc.substr(pos)));other_attr=attrs_info["other"];}
if(other_attr["core_close"]||other_attr["core_close"]==0){attrs_info["core_close"]=other_attr.core_close==0?"已开启":"已关闭";}
if(other_attr.csavezz){get_pet_ext_zz(attrs_info,{attrs:'attack_ext,defence_ext,speed_ext,avoid_ext,physical_ext,magic_ext',total_attrs:'attack_aptitude,defence_aptitude,speed_aptitude,avoid_aptitude,physical_aptitude,magic_aptitude',csavezz:other_attr.csavezz,carrygradezz:other_attr.carrygradezz,lastchecksubzz:other_attr.lastchecksubzz,pet_id:attrs[1]});}
if(attrs_info["other"]){attrs_info["equip_list"]=parse_pet_equips(attrs_info["other"]);attrs_info["neidan"]=parse_neidan(attrs_info["other"]);attrs_info["color"]=attrs_info["other"]["iColor"];attrs_info['summon_color']=attrs_info.other.summon_color;}
else{attrs_info["neidan"]=[];}
var jinjie_info=dict_get(other_attr,"jinjie",{});attrs_info['jinjie']=jinjie_info;attrs_info["lx"]=dict_get(jinjie_info,"lx",0);attrs_info["jinjie_cnt"]=dict_get(jinjie_info,"cnt","0");attrs_info["texing"]=dict_get(jinjie_info,"core",{});if(get_basic){return attrs_info;}
attrs_info['used_yuanxiao']=get_yuanxiao(attrs[30]);attrs_info['used_ruyidan']=get_ruyidan(attrs[31]);attrs_info['used_lianshou']=get_lianshou(attrs[33]);return attrs_info;}
function get_pet_shipin_icon(typeid){return ResUrl+"/images/pet_shipin/small/"+typeid+".png";};function parse_pet_equips(pet)
{var equip_list=[];var max_equip_num=3;var img_dir=ResUrl+"/images/equip/small/";for(var i=0;i<max_equip_num;i++){var item=pet["summon_equip"+(i+1)];if(item){var equip_name_info=RoleNameInfo.get_equip_info(item["iType"]);equip_list.push({"name":equip_name_info["name"],"icon":img_dir+item["iType"]+".gif","type":item["iType"],"desc":item["cDesc"],"static_desc":equip_name_info["desc"].replace(/#R/g,"<br />")});}else{equip_list.push(null);}}
if(pet.summon_equip4_type)
equip_list.push({"name":RoleNameInfo.pet_shipin_info[pet.summon_equip4_type],"icon":get_pet_shipin_icon(pet.summon_equip4_type),"type":pet.summon_equip4_type,"desc":pet.summon_equip4_desc,"static_desc":''});return equip_list;}
function parse_neidan(pet){var neidan_list=[];var neidan_data=pet.summon_core;if(neidan_data!=undefined){for(var p in neidan_data){var neidan_info=neidan_data[p];neidan_list.push({"name":safe_attr(PetNeidanInfo[p]),"icon":ResUrl+"/images/neidan/"+p+".jpg","level":neidan_info[0]});}}
return neidan_list;}
function fill_format(num){if(num/1000>=1){return num;}
if(num/100>=1){return"0"+num;}
if(num/10>=1){return"00"+num;}
return"000"+num;}
function show_pet_skill_in_grade(pet_skills,sp_skill,row_len,col_len,conf){var all_skills=pet_skills.split("|");var offset=0;var grid=document.createElement("table");grid.cellspacing=0;grid.cellpadding=0;if(conf.table_class){grid.className=conf.table_class;}
for(var i=0;i<row_len;i++){var r=grid.insertRow(i);for(var j=0;j<col_len;j++){var c=r.insertCell(j);var s_i=i*col_len+j+offset;if(s_i<all_skills.length&&all_skills[s_i]==sp_skill){offset++;s_i++;}
if(s_i<all_skills.length&&all_skills[s_i]!=""){var skill_id=all_skills[s_i];var content="<img src=\""+conf.pet_skill_url+fill_format(skill_id)+".gif\">";c.innerHTML=content;}else{c.innerHTML="&nbsp;";}}}
if(all_skills.length<=row_len*col_len&&trim(String(sp_skill))!="0"){var sp_cell=grid.rows[row_len-1].cells[col_len-1];var content="<img src=\""+conf.pet_skill_url+fill_format(sp_skill)+".gif\" class=\"on\">";sp_cell.innerHTML=content;}
if(conf.notice_node_name&&all_skills.length>row_len*col_len){var notice_node=document.getElementById(conf.notice_node_name);notice_node.style.display="block";}
$(conf.skill_panel_name).appendChild(grid);}
function get_summon_color_desc(value){if(value==undefined){return'未知';}else if(value==1){return'是';}else{return'否';}}