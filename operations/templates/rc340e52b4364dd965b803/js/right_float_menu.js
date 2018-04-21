
(function(){if(window.localStorage){return;}
var IELocalStorageType=new Class({initialize:function(){var tagid='local_data_tag';this.dataTag=$(tagid);if(!this.dataTag){this.dataTag=new Element('div',{id:tagid,styles:{display:'none',behavior:'url(#default#userData)'}});$(document.body).grab(this.dataTag);}
this.filename='oXMLUserData';},getItem:function(key){this.dataTag.load(this.filename);return this.dataTag.getAttribute(key);},setItem:function(key,value){this.dataTag.setAttribute(key,value);this.dataTag.save(this.filename);}});window.localStorage=new IELocalStorageType();})();function add_latest_view(equipid,equip_name,icon_url,price,storage_key,is_overall_search)
{var item={"equipid":equipid,"equip_name":equip_name,"icon_url":icon_url,"price":price,"serverid":(window.EquipInfo&&EquipInfo.server_id)||(window.equip&&equip.server_id)||(window.ServerInfo&&ServerInfo.server_id)};if(is_overall_search){item["is_overall_search"]=true;}else{item["is_overall_search"]=false;}
var latest_equips=window.localStorage.getItem(storage_key);if(latest_equips){latest_equips=JSON.decode(latest_equips);}else{latest_equips=[];}
latest_equips.each(function(e,i){if(e.equipid==item.equipid&&e.serverid==item.serverid){latest_equips.erase(e);}});latest_equips.unshift(item);while(latest_equips.length>10){latest_equips.pop();}
try{window.localStorage.setItem(storage_key,JSON.encode(latest_equips));}catch(e){}}
function add_latest_view_overall_search(equipid,equip_name,icon_url,price)
{add_latest_view(equipid,equip_name,icon_url,price,"latest_overall_search",true);}
function get_latest_view_overall_search()
{try{return window.localStorage.getItem("latest_overall_search");}catch(e){}}
function gen_latest_view_overall_search()
{var panel_el=$("recent_list_panel");var latest_equips=get_latest_view_overall_search();if(latest_equips){latest_equips=JSON.decode(latest_equips);}else{latest_equips=[];}
latest_equips=latest_equips.filter(function(item){return item.serverid;});if(latest_equips.length>0){render_to_replace('recent_list_panel','recent_list_templ',{"equip_list":latest_equips});}else{render_to_replace('recent_list_panel','recent_empty_templ');}}