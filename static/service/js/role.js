var role_static = {
	role_price_list: ['60-999', '1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000以上'],
	role_level_list: ['69级','70级-109级','110级-129级','130级-159级','160级-175级'],
	role_school_list: {'9': '狮驼岭', '6': '普陀山', '12': '盘丝洞', '15': '无底洞', '4': '方寸山', '14': '凌波城', '2': '化生寺', '10': '魔王寨', '5': '天宫', '7': '龙宫', '13': '神木林', '11': '阴曹地府', '3': '女儿村', '17': '天机城', '18': '花果山', '1': '大唐官府', '16': '女魃墓', '8': '五庄观'},
	role_expt_obj: {'expt_total': '修炼总和', 'expt_gongji': '攻击修炼', 'expt_kangfa': '抗法修炼', 'expt_fangyu': '防御修炼', 'max_expt_gongji': '攻击上限', 'expt_fashu': '法术修炼','max_expt_fashu': '法术上限', 'max_expt_kangfa': '抗法上限', 'max_expt_fangyu': '防御上限', 'expt_lieshu': '猎术修炼'},
	role_bb_expt_obj: {'bb_expt_fashu': '法术控制', 'bb_expt_fangyu': '防御控制', 'bb_expt_total': '宠修总和', 'bb_expt_gongji': '攻击控制', 'bb_expt_kangfa': '抗法修炼'},
	role_feisheng_list: ['已飞升', '已渡劫', '化圣一','化圣二','化圣三','化圣四','化圣五','化圣六','化圣七','化圣八','化圣九'],
	role_feisheng_obj: {'已飞升': 1, '已渡劫': 2, '化圣一':10 ,'化圣二': 20,'化圣三' : 30,'化圣四': 40,'化圣五': 50,'化圣六': 60,'化圣七': 70,'化圣八':80,'化圣九': 90, "": ""}	,
	role_live_skill: {'skill_qiang_shen': '强身术', 'skill_qiang_zhuang': '强壮', 'skill_shensu': '神速', 'skill_ming_xiang': '冥想',  'skill_yangsheng': '养生之道', 'skill_jianshen': '健身术',  'skill_dazao': '打造技巧', 'skill_caifeng': '裁缝技巧','skill_lianjin': '炼金术','skill_cuiling': '淬灵之术', 'skill_qiaojiang': '巧匠之术', 'skill_lingshi': '灵石技巧','skill_ronglian': '熔炼技巧','skill_zhongyao': '中药医理', 'skill_pengren': '烹饪技巧',  'skill_taoli': '逃离技巧',  'skill_zhuibu': '追捕技巧', 'skill_anqi': '暗器技巧'},
	role_race_obj : {'1': '逍遥生', '205': '杀破狼', '9': '神天兵', '12': '玄彩娥', '10': '龙太子', '2': '剑侠客', '8': '骨精灵', '211': '桃夭夭', '209': '羽灵神', '4': '英女侠', '201': '偃无师', '5': '巨魔王', '207': '鬼潇潇', '6': '虎头怪', '203': '巫蛮儿', '11': '舞天姬', '3': '飞燕女', '7': '狐美人'},
	role_attr_obj : {'shang_hai': '伤害', 'fang_yu': '防御',  'hp': '气血', 'fa_shang': '法伤','fa_fang': '法防','ling_li': '灵力','speed': '速度','ming_zhong': '命中', 'qian_neng_guo': '潜能果' },
	role_movie_skill: {'skill_jianzhu': '建筑之术', 'skill_danyuan': '丹元济会', 'skill_miaoshou': '妙手空空', 'skill_dazuo': '打坐 ', 'skill_gudong': '古董评估', 'skill_huoyan': '火眼金睛', 'skill_qimen': '奇门遁甲', 'skill_tiaoxi': '调息 ', 'skill_bianhua': '变化之术', 'skill_xianling': '仙灵店铺', 'skill_baoshi': '宝石工艺'},
	role_pet_obj: {'1': '力劈宠','2': '善恶宠', '3': '须弥宠', '4': '死亡宠', '5': '法防宠', '6': '壁垒宠','7': '隐攻宠', '8': '高连宠', '102060': '超级青鸾', '102250': '超级六耳猕猴', '102100': '超级灵鹿', '102005': '超级泡泡', '102032': '超级孔雀', '102313': '超级神猴', '102018': '超级金猴',  '102317': '超级玉兔', '102249': '超级神羊', '102019': '超级人参娃娃', '102016': '超级大熊猫', '102131': '超级海豚', '102051': '超级神蛇', '102049': '超级神马', '102008': '超级神虎', '102101': '超级白泽', '102311': '超级土地公公', '102050': '超级麒麟', '102315': '超级神鸡', '102110': '超级神牛', '102108': '超级赤焰兽',  '102109': '超级大鹏', '102031': '超级灵狐', '102021': '超级筋斗云', '102827': '超级猪小戒', '102132': '超级神兔',  '102325': '超级神狗',  '102035': '超级神龙', '102020': '超级大象'},
	role_xiangrui_obj: {'玄火神驹': '玄火神驹', '玄冰灵虎': '玄冰灵虎', '战火穷奇': '战火穷奇', '星华飞马': '星华飞马', '逐日天辇': '逐日天辇', '七彩祥云': '七彩祥云', '萤火霜兔': '萤火霜兔', '青霄天麟': '青霄天麟', '甜蜜泡泡': '甜蜜泡泡', '猪猪小侠': '猪猪小侠', '甜蜜猪猪': '甜蜜猪猪', '九尾冰狐': '九尾冰狐', '铃儿叮当': '铃儿叮当', '天使猪猪': '天使猪猪', '冰晶雪魄': '冰晶雪魄', '飞天猪猪': '飞天猪猪', '九幽灵虎': '九幽灵虎', '玉脂福羊': '玉脂福羊', '翠灵锦篮': '翠灵锦篮', '冰晶小雪魄': '冰晶小雪魄', '莽林猛犸': '莽林猛犸', '神行小驴': '神行小驴', '跃动精灵': '跃动精灵', '齐天小轿': '齐天小轿', '幽骨战龙': '幽骨战龙', '魔骨战熊': '魔骨战熊', '七彩小驴': '七彩小驴', '九霄冰凤': '九霄冰凤', '冰晶魅灵': '冰晶魅灵', '鹤雪锦犀': '鹤雪锦犀', '玉瓷葫芦': '玉瓷葫芦', '竹林熊猫': '竹林熊猫', '如意宝狮': '如意宝狮', '萌萌小狗': '萌萌小狗', '碧海鳐鱼': '碧海鳐鱼', '粉红小驴': '粉红小驴', '萌动猪猪': '萌动猪猪', '月影天马': '月影天马', '暗影战豹': '暗影战豹', '九霄幽凰': '九霄幽凰', '妙缘暖犀': '妙缘暖犀'},
	role_clothes_obj: {'12512': '青花瓷（上衣）', '12498': '冰寒绡（衣服）', '12648': '青花瓷·月白（头饰）', '40023': '冰寒绡·月白（衣服）', '12767': '冰寒绡·墨黑（头饰）', '12765': '冰寒绡·月白（头饰）', '40025': '冰寒绡·墨黑（衣服）', '12652': '青花瓷（下衣）', '13790': '冰寒绡（头饰）', '12750': '落星织（头饰）', '12514': '青花瓷·月白（上衣）', '12850': '冰雪玉兔（头饰）', '12646': '青花瓷（头饰）', '40013': '落星织（衣服）', '40108': '冰雪玉兔（衣服）', '12647': '青花瓷·墨黑（头饰）', '12654': '青花瓷·月白（下衣）', '12513': '青花瓷·墨黑（上衣）', '12653': '青花瓷·墨黑（下衣）'},
	role_other_attr_obj: {'clothes_num': '锦衣数量', 'badness': '善恶', 'cheng_jiu': '成就', 'all_caiguo': '所有染色折算彩果数', 'box_caiguo': '保存染色方案数', 'body_caiguo': '身上染色折算彩果数', 'school_offer': '门贡', 'special_equip_max_level': '专用装备等级', 'org_offer': '帮贡', 'addon_point': '月饼粽子食用量'},
	role_clothes_obj: {'12512': '青花瓷（上衣）', '12498': '冰寒绡（衣服）', '12648': '青花瓷·月白（头饰）', '40023': '冰寒绡·月白（衣服）', '12767': '冰寒绡·墨黑（头饰）', '12765': '冰寒绡·月白（头饰）', '40025': '冰寒绡·墨黑（衣服）', '12652': '青花瓷（下衣）', '13790': '冰寒绡（头饰）', '12750': '落星织（头饰）', '12514': '青花瓷·月白（上衣）', '12850': '冰雪玉兔（头饰）', '12646': '青花瓷（头饰）', '40013': '落星织（衣服）', '40108': '冰雪玉兔（衣服）', '12647': '青花瓷·墨黑（头饰）', '12654': '青花瓷·月白（下衣）', '12513': '青花瓷·墨黑（上衣）', '12653': '青花瓷·墨黑（下衣）'},
};
var role_params = {
	feisheng_show: "",
	params: {
		price_min: '', 
		price_max: '',
		// 等级
		level_min: '',
		level_max: '',
		// 门派
		school: [],
		// 历史门派
		school_change_list: [],
		// 修炼
		expt_fashu:"" ,
		expt_lieshu:"" ,
		expt_gongji:"" ,
		expt_kangfa:"" ,
		max_expt_fashu:"" ,
		max_expt_fangyu:"" ,
		expt_fangyu:"" ,
		max_expt_kangfa:"" ,
		max_expt_gongji:"" ,
		expt_total:"" ,
		// 召唤兽修炼
		bb_expt_fangyu:"",
		bb_expt_kangfa:"",
		bb_expt_fashu:"",
		bb_expt_gongji:"",
		bb_expt_total:"",
		// 是否飞升:
		zhuang_zhi: "",
		// 师门技能
		school_skill_level: "",  //******************school_skill_num有值， school_skill_level未空 则都不传
		school_skill_num: "",   //*******************如果school_skill_level有值， school_skill_num也要带上 school_skill_level=
		// 乾元丹
		qian_yuan_dan: "",
		// 角色类型
		race: [],
		// 角色经验
		sum_exp_min: "",  //******未验证
		sum_exp_max: "",
		// 身上携带的召唤兽类型
		pet_match_all: 0,  //0: 满足一种 1: 满足所有
		pet_type_list: [],  // 这个没有值上面也为空
		// 祥瑞
		xiangrui_match_all: 0, // 规则同上
		xiangrui_list: [],
		// 锦衣
		limit_clothes_logic: "or",  // 一种or 全部 and
		limit_clothes: [],
	}
}
// 写入生活技能
var role_live_skill_list = Object.keys(role_static.role_live_skill);
for(var i=0;i<role_live_skill_list.length;i++){
	var key = role_live_skill_list[i];
	role_params.params[key] = "";
}
// 写入人物属性
var role_attr_list = Object.keys(role_static.role_attr_obj);
for(var i=0;i<role_attr_list.length;i++){
	var key = role_attr_list[i];
	role_params.params[key] = "";
}
// 剧情技能
var role_movie_list = Object.keys(role_static.role_movie_skill);
for(var i=0;i<role_movie_list.length;i++){
	var key = role_movie_list[i];
	role_params.params[key] = "";
}
// 其它条件
var role_other_list = Object.keys(role_static.role_other_attr_obj);
for(var i=0;i<role_other_list.length;i++){
	var key = role_other_list[i];
	role_params.params[key] = "";
}



var role_methods = {
	role_price_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		var price_min = show.split('-')[0];
		var price_max = show.split('-')[1];
		if(show == '5000以上'){
			price_max = '1000000';
			price_min = '5000';
			if(this.role_params.params.price_max == '1000000' && this.role_params.params.price_min == '5000'){
				this.role_params.params.price_min = this.role_params.params.price_max = ''
			} else{
				this.role_params.params.price_min = price_min;
				this.role_params.params.price_max = price_max;
			}
		}else{
			if(this.role_params.params.price_min == price_min &&  this.role_params.params.price_max == price_max){
				this.role_params.params.price_min = '';
				this.role_params.params.price_max = '';
			}else{
				this.role_params.params.price_min = price_min;
				this.role_params.params.price_max = price_max;
			}
		}
	},
	level_change: function(n, o){
		if(!this.role_params.params.level_min && !this.role_params.params.level_max) this.role_params.level_show = '';
		if(this.role_params.params.level_min && !this.role_params.params.level_max) this.role_params.level_show = '>=' + this.role_params.params.level_min;
		if(!this.role_params.params.level_min && this.role_params.params.level_max) this.role_params.level_show = '<=' + this.role_params.params.level_max;
		if(this.role_params.params.level_min && this.role_params.params.level_max) this.role_params.level_show = this.role_params.params.level_min + '-' + this.role_params.params.level_max

	},
	// 等级部分
	role_level_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		if(show == '69级'){
			this.role_params.params.level_min = this.role_params.params.level_max  = 69
			return false;
		}
		var level_min = show.split('-')[0].split('级')[0];
		var level_max = show.split('-')[1].split('级')[0];
		if(this.role_params.params.level_min == level_min && this.role_params.params.level_max == level_max){
			this.role_params.params.level_min = '';
			this.role_params.params.level_max = '';
		}else{
			this.role_params.params.level_min = level_min;
			this.role_params.params.level_max = level_max;
		}
	},
	// 门派
	school_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.school.indexOf(pk);
		if(i == -1) this.role_params.params.school.push(pk);
		else this.role_params.params.school.splice(i, 1);
	},
	// 历史门派
	history_school_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.school_change_list.indexOf(pk);
		if(i == -1) this.role_params.params.school_change_list.push(pk);
		else this.role_params.params.school_change_list.splice(i, 1);
	},
	// 是否飞升
	feisheng_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		var val = this.role_feisheng_obj[show];
		if(this.role_params.params.zhuang_zhi == val){
			this.role_params.params.zhuang_zhi = "";
			this.role_params.feisheng_show = "";
		}else{
			this.role_params.params.zhuang_zhi = val;
			this.role_params.feisheng_show = show;
		}
	},
	// 角色类型
	role_race_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.race.indexOf(pk);
		if(i == -1) this.role_params.params.race.push(pk);
		else this.role_params.params.race.splice(i, 1);
	},
	// 身上携带的召唤兽类型
	role_pet_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.pet_type_list.indexOf(pk);
		if(i == -1) this.role_params.params.pet_type_list.push(pk);
		else this.role_params.params.pet_type_list.splice(i, 1);
	},
	// 召唤兽筛选
	role_pet_filter_click: function(){
		if(this.role_params.params.pet_match_all == 1){
			this.role_params.params.pet_match_all =0;
		}else{
			this.role_params.params.pet_match_all =1;
		}
	},
	// 祥瑞
	role_xiangrui_match_click: function(){
		if(this.role_params.params.xiangrui_match_all == 1){
			this.role_params.params.xiangrui_match_all =0;
		}else{
			this.role_params.params.xiangrui_match_all =1;
		}
	},
	role_xiangrui_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.xiangrui_list.indexOf(pk);
		if(i == -1) this.role_params.params.xiangrui_list.push(pk);
		else this.role_params.params.xiangrui_list.splice(i, 1);
	},
	// 锦衣
	role_clothes_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.role_params.params.limit_clothes.indexOf(pk);
		if(i == -1) this.role_params.params.limit_clothes.push(pk);
		else this.role_params.params.limit_clothes.splice(i, 1);
	},
	role_clothes_filter_click: function(){
		if(this.role_params.params.limit_clothes_logic == 'or'){
			this.role_params.params.limit_clothes_logic = 'and';
		}else{
			this.role_params.params.limit_clothes_logic = 'or';
		}
	}



}
var role_watch = {

}
var role_computed = {
	// 价格部分
	role_price_show: function(){
		var show = "";
		if(!this.role_params.params.price_min && !this.role_params.params.price_max) show = '';
		if(this.role_params.params.price_min && !this.role_params.params.price_max) show = '>=' + this.role_params.params.price_min;
		if(!this.role_params.params.price_min && this.role_params.params.price_max) show = '<=' + this.role_params.params.price_max;
		if(this.role_params.params.price_min && this.role_params.params.price_max) show = this.role_params.params.price_min + '-' + this.role_params.params.price_max;
		return show;
	},
	role_price_active: function(){
		var show = this.role_params.params.price_min + '-' + this.role_params.params.price_max;
		show = show == '5000-1000000' ? '5000以上'   : show;
		return this.role_price_list.indexOf(show);
	},
	// 等级部分
	role_level_show: function(){
		var show = "";
		if(!this.role_params.params.level_min && !this.role_params.params.level_max) show = '';
		if(this.role_params.params.level_min && !this.role_params.params.level_max) show = '>=' + this.role_params.params.level_min;
		if(!this.role_params.params.level_min && this.role_params.params.level_max) show = '<=' + this.role_params.params.level_max;
		if(this.role_params.params.level_min && this.role_params.params.level_max) show = this.role_params.params.level_min + '-' + this.role_params.params.level_max
		return show;
	},
	role_level_active: function(){
		var show ="";
		if(this.role_params.params.level_max == this.role_params.params.level_min && this.role_params.params.level_min == '69'){
			show = "69级";
		}else{
		    show = this.role_params.params.level_min + '级-' + this.role_params.params.level_max+'级';
		}
		return this.role_level_list.indexOf(show);
	},
	// 门派
	school_show: function(){
		var _s = "";
		for(var i=0;i<this.role_params.params.school.length;i++){
			var item = this.role_params.params.school[i];
			_s += this.role_school_list[item] + ',';
		}
		return _s;
	},
	history_school_show: function(){
		var _s = "";
		for(var i=0;i<this.role_params.params.school_change_list.length;i++){
			var item = this.role_params.params.school_change_list[i];
			_s += this.role_school_list[item] + ',';
		}
		return _s;
	},
	// 人物修炼
	role_expt_show: function(){
		var _s = '';
		var expt_show_list = Object.keys(this.role_expt_obj);
		for(var i=0;i<expt_show_list.length;i++){
			var item = expt_show_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 25){
				this.role_params.params[item] = 25;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_expt_obj[item] + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	},
	// 召唤兽修炼
	role_bb_expt_show: function(){
		var _s = '';
		var expt_show_list = Object.keys(this.role_bb_expt_obj);
		for(var i=0;i<expt_show_list.length;i++){
			var item = expt_show_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 25){
				this.role_params.params[item] = 25;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_bb_expt_obj[item] + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	},
	// 师门技能等级
	role_school_show: function(){
		if(this.role_params.params.school_skill_level == ""){
			return ""
		}
		if(this.role_params.params.school_skill_num == "" && this.role_params.params.school_skill_level){
			return '不限个技能≥' + this.role_params.params.school_skill_level + ',';
		}
		if(this.role_params.params.school_skill_num  && this.role_params.params.school_skill_level){
			return this.role_params.params.school_skill_num + '个技能≥' + this.role_params.params.school_skill_level + ',';
		}
		return "";
	},
	// 生活技能
	role_live_skill_show: function(){
		var _s = '';
		var expt_show_list = Object.keys(this.role_live_skill);
		for(var i=0;i<expt_show_list.length;i++){
			var item = expt_show_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 200){
				this.role_params.params[item] = 200;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_live_skill[item] + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	},
	// 角色类型
	role_race_show: function(){
		var _s = "";
		for(var i=0;i<this.role_params.params.race.length;i++){
			var item = this.role_params.params.race[i];
			_s += this.role_race_obj[item] + ',';
		}
		return _s;
	},
		// 生活技能
	role_attr_show: function(){
		var _s = '';
		var role_show_list = Object.keys(this.role_attr_obj);
		for(var i=0;i<role_show_list.length;i++){
			var item = role_show_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 999999){
				this.role_params.params[item] = 999999;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_attr_obj[item] + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	},
	// 人物经验
	role_exp_show: function(){
		var _s ="";
		if(this.role_params.params.sum_exp_min && !this.role_params.params.sum_exp_max){
			_s = ">=" + this.role_params.params.sum_exp_min;
		}
		if(!this.role_params.params.sum_exp_min && this.role_params.params.sum_exp_max){
			_s = "<=" + this.role_params.params.sum_exp_max;
		}
		if(this.role_params.params.sum_exp_min && this.role_params.params.sum_exp_max){
			_s = this.role_params.params.sum_exp_min + '-' + this.role_params.params.sum_exp_max;
		}
		return _s
	},
	// 剧情技能
	role_movie_skill_show: function(){
		var _s = '';
		var role_show_list = Object.keys(this.role_movie_skill);
		for(var i=0;i<role_show_list.length;i++){
			var item = role_show_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 200){
				this.role_params.params[item] = 200;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_movie_skill[item] + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	},
	// 携带召唤兽
	role_pet_match_show: function(){
		var _s = "";
		if(this.role_params.params.pet_type_list.length == 0){
			return "";
		}
		if(this.role_params.params.pet_match_all == 1){
			_s = '满足全部:'
		}else{
			_s =   '满足一种:';

		}
		return _s;
	},
	role_pet_show: function(){
		var _s = "";
		for(var i=0;i<this.role_params.params.pet_type_list.length;i++){
			var item = this.role_params.params.pet_type_list[i];
			_s += this.role_pet_obj[item] + ',';
		}
		return _s;
	},
	// 珍稀祥瑞
	role_xiangrui_show: function(){
		var _s = "";
		if(this.role_params.params.xiangrui_list.length == 0){
			return "";
		}
		_s += this.role_params.params.xiangrui_match_all == 1 ? '满足全部:' : '满足一种:'
		for(var i=0;i<this.role_params.params.xiangrui_list.length;i++){
			var item = this.role_params.params.xiangrui_list[i];
			_s += this.role_xiangrui_obj[item] + ',';
		}
		return _s;
	},
	// 锦衣
	role_clothes_show: function(){
		var _s = "";
		if(this.role_params.params.limit_clothes.length == 0){
			return "";
		}
		_s += this.role_params.params.limit_clothes_logic == 'and' ? '整套:' : '一件:'
		for(var i=0;i<this.role_params.params.limit_clothes.length;i++){
			var item = this.role_params.params.limit_clothes[i];
			_s += this.role_clothes_obj[item] + ',';
		}
		return _s;
	},
	// 其它条件
	role_other_attr_show: function(){
		var _s = '';
		var role_other_list = Object.keys(this.role_other_attr_obj);
		for(var i=0;i<role_other_list.length;i++){
			var item = role_other_list[i];
			if(this.role_params.params[item] && this.role_params.params[item] > 999999){
				this.role_params.params[item] = 999999;
			}
			if(this.role_params.params[item] && this.role_params.params[item] <= 0){
				this.role_params.params[item] = "";
			}
			if(this.role_params.params[item] != '') _s += this.role_other_attr_obj[item]  + '>=' + this.role_params.params[item] + ',';
		}
		return _s;
	}


}

