var equip_static = {
	equip_price_list: ['10-499', '500-999', '1000-1499', '1500-1999', '2000-19999', '20000以上'],
	equip_kind_obj: { 19: '鞋子',  21: '饰品',20: '腰带', 18: '铠甲', 59: '女衣', 17: '头盔',58: '发钗',  10: '扇', 6: '剑', 14: '刀', 73: '巨剑', 4: '枪',15: '锤', 5: '斧',  8: '飘带',13: '双环',12: '鞭子',11: '魔棒',9: '爪刺', 7: '双剑', 72: '灯笼', 52: '宝珠', 53: '弓箭', 54: '法杖',    74: '伞'},
	equip_special_skill_obj: {1027: '罗汉金钟', 1015: '晶清诀',1011: '慈航普度', 1012: '水清诀', 1013: '冰清诀', 1036: '破血狂攻',1030: '放下屠刀', 1018: '笑里藏刀', 1037: '弱点击破',1008: '四海升平',1006: '气归术', 1007: '命归术',1024: '流云诀',1032: '破甲术', 1033: '碎甲术',1025: '啸风诀', 1026: '太极护法', 1028: '修罗咒', 1029: '天衣无缝',  1031: '河东狮吼', 1034: '凝滞术', 1035: '停陷术',  1038: '吸血', 1039: '残月', 1040: '冥王暴杀', 1042: '破碎无双', 1043: '帝释无双', 1044: '伽罗无双', 1045: '虚空之刃', 1046: '亡灵之刃', 1047: '死亡之音', 1048: '身似菩提', 1049: '心如明镜', 1050: '移形换影', 2001: '凝心决', 2002: '聚精会神', 2003: '先发制人', 2004: '燃烧之光', 2005: '毁灭之光', 2006: '金刚不坏', 2007: '菩提心佑', '2041,1041': '乾坤斩', 1001: '气疗术', 1002: '心疗术', 1003: '命疗术', 1004: '凝气诀', 1005: '凝神决', 1009: '回魂咒', 1010: '起死回生',   1014: '玉清诀', 1016: '诅咒之伤', 1017: '诅咒之亡', 1019: '绝幻魔音', 1020: '野兽之力', 1021: '魔兽之印', 1022: '光辉之甲', 1023: '圣灵之甲'},
	equip_special_effect_obj: {1: '无级别', 2: '简易', 3: '愤怒', 4: '暴怒', 5: '永不磨损', 6: '神农', 7: '神佑', 8: '精致', 9: '坚固', 10: '狩猎', 11: '绝杀', 12: '专注', 13: '伪装', 14: '易修理', 15: '再生', 16: '必中', 17: '迷踪', 18: '珍宝'},
	// 套装
	equip_suit_tab_obj: {
		addStatus : {
			title: '附加状态',
			active: true,
		},
		AppendSkills: {
			title: '追加法术',
			active: false,
		},
		TransformSkills: {
			title: '变身术之',
			active: false,
		},
		TransformCharms: {
			title: '变化咒之',
			active: false
		}
	},
	equip_suit_content_height: get_win_size()[1] - 30 - 52 + 'px',
	SuitAddedStatus: SuitAddedStatus, // 附加状态
	SuitAppendSkills: SuitAppendSkills, // 追加法术
	SuitTransformSkills: SuitTransformSkills, // 变身术之
	SuitTransformCharms: SuitTransformCharms, // 变化咒之
	// 装备属性
	equip_attr_obj: { 'all_damage': '总伤', 'init_damage': '初伤（包含命中）', 'init_damage_raw': '初伤（不含命中）', 'init_wakan': '初灵', 'init_defense': '初防',  'init_hp': '初血',  'init_dex': '初敏', 'damage': '伤害'},
	// 装备属性计算
	equip_attr_sum_obj: {'dex': '敏捷', 'power': '力量', 'magic': '魔力', 'endurance': '耐力', 'physique': '体质'},
	equip_gem_obj: {1: '红玛瑙', 2: '太阳石', 3: '舍利子', 4: '光芒石', 5: '月亮石', 6: '黑宝石', 7: '神秘石', 12: '翡翠石'},
	// 160装备属性效果
	equip_attr160_obj: {1: '物理暴击几率', 2: '法术暴击几率', 3: '物理暴击伤害', 4: '法术暴击伤害', 5: '治疗能力', 6: '封印命中率', 7: '抵抗封印命中率', 8: '穿刺效果', 9: '格挡物理伤害', 10: '魔法回复', 11: '法术伤害减免效果'},
	equip_repair_ob: {0: '无失败', 1:'≤1次', 2:'≤2次', 3:'≤3次'},
	// 人造2 系统1
	equip_product_obj: {1: '系统', 2: '人造'},
}
var equip_params = {
	suit_display: false,
	suit_show: "",
	params: {
		// 价格
		price_min: '', 
		price_max: '',
		// 等级
		level_min: 60,  // 
		level_max: 160, // 如果为60-160则不需要上传
		// 类型
		kindid: [],
		// 特技
		special_skill: [],
		// 特效
		special_effect: [],  // 如果这个没有值， 那么下面的为空
		special_mode: 'and',//是否全部满足
		// 附加状态, 法术， 变身术， 变身咒
		suit_effect: "",
		// 属性计算
		sum_attr_type: [],
		sum_attr_value: "",
		// 镶嵌宝石
		gem_value: [],
		gem_level: "",// 锻造等级
		// 160装备效果
		'160_attr': "",
		hole_num: "", // 开孔数目
		star: "", // 开启星位 // **********如果为false 需要改为""
		// 修理失败次数
		repair_fail: "",
		// 装备出处 人造 系统
		produce_from:[],
	}
}
// 装备属性
var equip_attr_list = Object.keys(equip_static.equip_attr_obj);
for(var i=0;i<equip_attr_list.length;i++){
	var key = equip_attr_list[i];
	equip_params.params[key] = "";
}

var equip_methods = {
	equip_price_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		var price_min = show.split('-')[0];
		var price_max = show.split('-')[1];
		if(show == '20000以上'){
			price_max = '1000000';
			price_min = '20000';
			if(this.equip_params.params.price_max == '1000000' && this.equip_params.params.price_min == '20000'){
				this.equip_params.params.price_min = this.equip_params.params.price_max = ''
			} else{
				this.equip_params.params.price_min = price_min;
				this.equip_params.params.price_max = price_max;
			}
		}else{
			if(this.equip_params.params.price_min == price_min &&  this.equip_params.params.price_max == price_max){
				this.equip_params.params.price_min = '';
				this.equip_params.params.price_max = '';
			}else{
				this.equip_params.params.price_min = price_min;
				this.equip_params.params.price_max = price_max;
			}
		}
	},
	// 装备类型
	equip_kind_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.kindid.indexOf(pk);
		if(i == -1) this.equip_params.params.kindid.push(pk);
		else this.equip_params.params.kindid.splice(i, 1);
	},
	// 特技
	equip_special_skill_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.special_skill.indexOf(pk);
		if(i == -1) this.equip_params.params.special_skill.push(pk);
		else this.equip_params.params.special_skill.splice(i, 1);
	},
	// 特效
	equip_special_effect_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.special_effect.indexOf(pk);
		if(i == -1) this.equip_params.params.special_effect.push(pk);
		else this.equip_params.params.special_effect.splice(i, 1);
	},
	special_effect_filter_click: function(){
		if(this.equip_params.params.special_mode == 'and'){
			this.equip_params.params.special_mode ='or';
		}else{
			this.equip_params.params.special_mode ='and';
		}
	},
	// 套装
	equip_suit_display: function(){
		this.equip_params.suit_display = true;
	},
	equip_suit_tab_click: function(key){
	},
	equip_suit_click($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var show = $e.target.getAttribute('show')
		var title= $e.target.getAttribute('title')
		this.equip_params.suit_show = title+show;
		if(this.equip_params.params.suit_effect == pk){
			this.equip_params.params.suit_effect= ""
			this.equip_params.suit_show = "";
		}else{
			this.equip_params.params.suit_effect = pk
		}
		this.equip_params.suit_display = false;
	},
	// 装备属性和
	equip_attr_sum_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.sum_attr_type.indexOf(pk);
		if(i == -1) this.equip_params.params.sum_attr_type.push(pk);
		else this.equip_params.params.sum_attr_type.splice(i, 1);
	},
	// 镶嵌宝石
	equip_gem_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.gem_value.indexOf(pk);
		if(i == -1) this.equip_params.params.gem_value.push(pk);
		else this.equip_params.params.gem_value.splice(i, 1);
	},
	// 160装备效果
	equip_160attr_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		if(this.equip_params.params['160_attr'] == pk){
			this.equip_params.params['160_attr'] = ""
		}else{
			this.equip_params.params['160_attr'] = pk
		}
	},
	// 修理失败次数
	equip_repair_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		if(this.equip_params.params.repair_fail == pk){
			this.equip_params.params.repair_fail = ""
		}else{
			this.equip_params.params.repair_fail = pk
		}
	},
	// 人造， 系统
	equip_product_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.equip_params.params.produce_from.indexOf(pk);
		if(i == -1) this.equip_params.params.produce_from.push(pk);
		else this.equip_params.params.produce_from.splice(i, 1);
	}


}
var equip_watch = {
	// 宝石锻造等级
	'equip_params.params.gem_level': function(v){
		if(v > 15){
			this.equip_params.params.gem_level = 15;
		}
		if(v < 0){
			this.equip_params.params.gem_level = "";
		}
	},
	// 开孔数目
	'equip_params.params.hole_num': function(v){
		if(v > 5){
			this.equip_params.params.hole_num = 5;
		}
		if(v < 0){
			his.equip_params.params.hole_num = "";
		}

	}


}
var equip_computed = {
	//装备价格
	equip_price_active: function(){
		var show = this.equip_params.params.price_min + '-' + this.equip_params.params.price_max;
		show = show == '20000-1000000' ? '20000以上'   : show;
		return this.equip_price_list.indexOf(show);
	},
	equip_price_show: function(){
		if(!this.equip_params.params.price_min && !this.equip_params.params.price_max) show = '';
		if(this.equip_params.params.price_min && !this.equip_params.params.price_max) show = '>=' + this.equip_params.params.price_min;
		if(!this.equip_params.params.price_min && this.equip_params.params.price_max) show = '<=' + this.equip_params.params.price_max;
		if(this.equip_params.params.price_min && this.equip_params.params.price_max) show = this.equip_params.params.price_min + '-' + this.equip_params.params.price_max;
		return show;
	},
	// 等级
	equip_price_range: {
		get: function(){
			return [this.equip_params.params.level_min, this.equip_params.params.level_max]
		},
		set: function(newValue){
			this.equip_params.params.level_min = newValue[0];
			this.equip_params.params.level_max= newValue[1];
		}
	},
	equip_level_show: function(){
		if(this.equip_params.params.level_min == this.equip_params.params.level_max){
			return this.equip_params.params.level_min
		}else{
			return this.equip_params.params.level_min + '-'+ this.equip_params.params.level_max
		}
	},
	// 装备类型
	equip_kind_show: function(){
		var _s = "";
		for(var i=0;i<this.equip_params.params.kindid.length;i++){
			var item = this.equip_params.params.kindid[i];
			_s += this.equip_kind_obj[item] + ',';
		}
		return _s;
	},
	// 特技
	equip_special_skill_show: function(){
		var _s = "";
		for(var i=0;i<this.equip_params.params.special_skill.length;i++){
			var item = this.equip_params.params.special_skill[i];
			_s += this.equip_special_skill_obj[item] + ',';
		}
		return _s;

	},
	// 特效
	equip_special_effect_show: function(){
		if(!this.equip_params.params.special_effect.length){
			return ""
		}
		var _s = this.equip_params.params.special_mode == 'and' ? '满足全部:' : '满足一种:';
		for(var i=0;i<this.equip_params.params.special_effect.length;i++){
			var item = this.equip_params.params.special_effect[i];
			_s += this.equip_special_effect_obj[item] + ',';
		}
		return _s;
	},
	// 装备属性
	equip_attr_show: function(){
		var _s = '';
		var attr_list = Object.keys(this.equip_attr_obj);
		for(var i=0;i<attr_list.length;i++){
			var item = attr_list[i];
			if(this.equip_params.params[item] && this.equip_params.params[item] > 999999){
				this.equip_params.params[item] = 999999;
			}
			if(this.equip_params.params[item] && this.equip_params.params[item] <= 0){
				this.equip_params.params[item] = "";
			}
			if(this.equip_params.params[item] != '') _s += this.equip_attr_obj[item] + '>=' + this.equip_params.params[item] + ',';
		}
		return _s;

	},
	equip_attr_sum_list_show: function(){
		var l = [];
		for(var i=0;i<this.equip_params.params.sum_attr_type.length;i++){
			var item = this.equip_params.params.sum_attr_type[i];
			l.push(this.equip_attr_sum_obj[item]);
		}
		return l.join(',');
	},
	// 宝石锻造等级
	equip_gem_show: function(){
		var l = [];
		for(var i=0;i<this.equip_params.params.gem_value.length;i++){
			var item = this.equip_params.params.gem_value[i];
			l.push(this.equip_gem_obj[item]);
		}
		return l.join(',');
	},
	// 人造 系统
	equip_product_show: function(){
		var l = [];
		for(var i=0;i<this.equip_params.params.produce_from.length;i++){
			var item = this.equip_params.params.produce_from[i];
			l.push(this.equip_product_obj[item])
		}
		return l.join(',')
	}


}
