// 召唤兽的动态数据
var bb_params = {
	pet_container_show: false,
	pet_active_index : '',
	pet_show : '',
	params: {
		'price_min': '', 
		'price_max': '',
		// 等级
		'level_min': '',
		'level_max': '',
		// 参站等级
		'kindid': [], // 这里存储的是展示的['参展67-76']  上传需要转换成 id [1,2]
		'is_baobao': true,  // 这里上传要保存为 1 或者''
		// 技能等级
		'skill': [],
		'skill_with_suit' : false, // 包含套装技能 上传要更改为 1, ''
		// 召唤兽概况
		'skill_num': '',
		'lingxing': '',
		'growth': '',   // 成长值上传需要转为整数， 最高3位小数
		//'used_lianshou_max': '', // 炼兽真经
		//'used_yuanxiao_max': '', //元宵
		'type': [],
		// 资质
		'attack_aptitude': '', 
		'defence_aptitude': '', 
		'physical_aptitude': '',
		'magic_aptitude': '',
		'speed_aptitude_min': '',
		'speed_aptitude_max': '',
		// 属性
		'max_blood': '',
		'attack': '',
		'defence' : '',
		'speed' : '',  // app查询时speed pc查询时 speed_min
		'wakan': '',
		'speed_max': '',
		// 特性
		'texing' : [],
		'positive_effect': [],
		'negative_effect': [],
		'high_neidan': [],
		'low_neidan': [],
	}
}
// 召唤兽的方法
var bb_methods = {
	price_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		var price_min = show.split('-')[0];
		var price_max = show.split('-')[1];
		if(show == '5000以上'){
			price_max = '1000000';
			price_min = '5000';
			if(this.bb_params.params.price_max == '1000000' && this.bb_params.params.price_min == '5000'){
				this.bb_params.params.price_min = this.bb_params.params.price_max = ''
			} else{
				this.bb_params.params.price_min = price_min;
				this.bb_params.params.price_max = price_max;
			}
		}else{
			if(this.bb_params.params.price_min == price_min &&  this.bb_params.params.price_max == price_max){
				this.bb_params.params.price_min = '';
				this.bb_params.params.price_max = '';
			}else{
				this.bb_params.params.price_min = price_min;
				this.bb_params.params.price_max = price_max;
			}
		}
	},  
	level_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var show = $e.target.getAttribute('show');
		var level_min = show.split('-')[0].split('级')[0];
		var level_max = show.split('-')[1].split('级')[0];
		if(this.bb_params.params.level_min == level_min && this.bb_params.params.level_max == level_max){
			this.bb_params.params.level_min = '';
			this.bb_params.params.level_max = '';
		}else{
			this.bb_params.params.level_min = level_min;
			this.bb_params.params.level_max = level_max;
		}
	},
	kindid_click : function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.bb_params.params.kindid.indexOf(pk);
		if(i == -1) this.bb_params.params.kindid.push(pk);
		else this.bb_params.params.kindid.splice(i, 1);
	},
	skill_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk')
		var i = this.bb_params.params.skill.indexOf(pk);
		if(i == -1) this.bb_params.params.skill.push(pk);
		else this.bb_params.params.skill.splice(i, 1);
	},
	pet_click: function(){
		this.bb_params.pet_container_show = true;
	},
	pet_hide: function(){
		this.bb_params.pet_container_show = false;
	},
	pet_name_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var e = $e.target;
		var index = e.getAttribute('index');var show=e.getAttribute('show');
		if(this.bb_params.pet_active_index == index){
			this.bb_params.pet_show = '';
			this.bb_params.params.type = [];
			this.bb_params.pet_active_index = '';
		}else{
			this.bb_params.pet_active_index = index;
			this.bb_params.pet_show = show;
			this.bb_params.params.type = this.pet_id_dict[show];
		}
		this.bb_params.pet_container_show = false;
	},
	texing_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk');
		var i = this.bb_params.params.texing.indexOf(pk);
		if(i==-1) this.bb_params.params.texing.push(pk)
		else this.bb_params.params.texing.splice(i, 1);
	},
	positive_effect_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk');
		var i = this.bb_params.params.positive_effect.indexOf(pk);
		if(i==-1) this.bb_params.params.positive_effect.push(pk)
		else this.bb_params.params.positive_effect.splice(i, 1);

	},
	negative_effect_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var pk = $e.target.getAttribute('pk');
		var i = this.bb_params.params.negative_effect.indexOf(pk);
		if(i==-1) this.bb_params.params.negative_effect.push(pk)
		else this.bb_params.params.negative_effect.splice(i, 1);
	
	},
	high_neidan_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var e = $e.target;
		var pk = e.getAttribute('pk');
		var i = this.bb_params.params.high_neidan.indexOf(pk);
		if(i==-1) this.bb_params.params.high_neidan.push(pk)
		else this.bb_params.params.high_neidan.splice(i, 1);
	},

	low_neidan_click: function($e){
		if($e.target.nodeName.toLowerCase() != 'span') return false;
		var e = $e.target;
		var pk = e.getAttribute('pk');
		var i = this.bb_params.params.low_neidan.indexOf(pk);
		if(i==-1) this.bb_params.params.low_neidan.push(pk)
		else this.bb_params.params.low_neidan.splice(i, 1);

	},
}
var bb_watch =  {
}
var bb_computed = {
	price_show: function(){
		var show = "";
		if(!this.bb_params.params.price_min && !this.bb_params.params.price_max) show = '';
		if(this.bb_params.params.price_min && !this.bb_params.params.price_max) show = '>=' + this.bb_params.params.price_min;
		if(!this.bb_params.params.price_min && this.bb_params.params.price_max) show = '<=' + this.bb_params.params.price_max;
		if(this.bb_params.params.price_min && this.bb_params.params.price_max) show = this.bb_params.params.price_min + '-' + this.bb_params.params.price_max;
		return show
	},
	level_show: function(){
		var show = "";
		if(!this.bb_params.params.level_min && !this.bb_params.params.level_max) show = '';
		if(this.bb_params.params.level_min && !this.bb_params.params.level_max) show = '>=' + this.bb_params.params.level_min;
		if(!this.bb_params.params.level_min && this.bb_params.params.level_max) show = '<=' + this.bb_params.params.level_max;
		if(this.bb_params.params.level_min && this.bb_params.params.level_max) show = this.bb_params.params.level_min + '-' + this.bb_params.params.level_max
		return show;
	},
	price_active: function(){
		var show = this.bb_params.params.price_min + '-' + this.bb_params.params.price_max;
		show = show == '5000-1000000' ? '5000以上'   : show;
		return this.price_list.indexOf(show);
	},
	level_active: function(){
		var show = this.bb_params.params.level_min + '级-' + this.bb_params.params.level_max+'级';
		return this.level_list.indexOf(show);
	},
	// kindid_active: function(){
	// 	return this.bb_params.params.kindid
	// }
	kindid_show: function(){
		var _s = "";
		// for(var item of this.bb_params.params.kindid){
		// 	_s += this.kindid_list[item] + ',';
		// }
		for(var i=0;i<this.bb_params.params.kindid.length;i++){
			var item = this.bb_params.params.kindid[i];
			_s += this.kindid_list[item] + ',';
		}
		return _s;
	},
	// 概况展示
	over_view_show: function(){
		var _s = '';
		var over_view_list = ['skill_num', 'lingxing', 'growth'];
		for(var i=0;i<over_view_list.length;i++){
			var item = over_view_list[i];
			if(item.indexOf('max') != -1 && this.bb_params.params[item] != '') _s += this.over_view[item] + '<=' + this.bb_params.params[item] + ',';
			if(item.indexOf('max') == -1 && this.bb_params.params[item] != '') _s += this.over_view[item] + '>=' + this.bb_params.params[item] + ',';
		}
		return _s;
	},
	aptitude_show: function(){
		var _s = '';
		var pet_aptitude_keys = Object.keys(this.pet_aptitude);
		for(var i=0;i<pet_aptitude_keys.length;i++){
			var item = pet_aptitude_keys[i];
			if(item.indexOf('max') != -1 && this.bb_params.params[item] != '') _s += this.pet_aptitude[item] + '<=' + this.bb_params.params[item] + ',';
			if(item.indexOf('max') == -1 && this.bb_params.params[item] != '') _s += this.pet_aptitude[item] + '>=' + this.bb_params.params[item] + ',';
		}
		return _s;
	},
	attr_show: function(){
		var _s = '';
		var pet_attr_keys = Object.keys(this.pet_attr);
		for(var i=0;i<pet_attr_keys.length;i++){
			var item = pet_attr_keys[i];
			if(item.slice(-3) != 'max' && this.bb_params.params[item] != '') _s += this.pet_attr[item] + '<=' + this.bb_params.params[item] + ',';
			if(item.slice(-3) == 'max' && this.bb_params.params[item] != '') _s += this.pet_attr[item] + '>=' + this.bb_params.params[item] + ',';
		}
		return _s;
	},
	skill_show: function(){
		var _s = "";
		for(var i=0;i<this.bb_params.params.skill.length;i++){
			var item = this.bb_params.params.skill[i];
			if(Object.keys(this.high_skill_list).indexOf(item) != -1) _s += this.high_skill_list[item] + ',';
			if(Object.keys(this.low_skill_list).indexOf(item) != -1) _s += this.low_skill_list[item] + ',';
			if(Object.keys(this.special_skills).indexOf(item) != -1) _s += special_skills[item] + ',';
		}
		return _s;
	},
	texing_show: function(){
		var _s = "";
		for(var i=0;i<this.bb_params.params.texing.length;i++){
			var item = this.bb_params.params.texing[i];
			_s += this.texing_types[item] + ',';
		}
		for(var i=0;i<this.bb_params.params.positive_effect.length;i++){
			var item = this.bb_params.params.positive_effect[i];
			_s += this.TexingPositiveEffectTypes[item] + ',';
		}
		for(var i=0;i<this.bb_params.params.negative_effect.length;i++){
			var item = this.bb_params.params.negative_effect[i];
			_s += this.TexingNegativeEffectTypes[item] + ',';
		}
		return _s;
	},
	neidan_show: function(){
		var _s = "";
		for(var i=0;i<this.bb_params.params.high_neidan.length;i++){
			var item = this.bb_params.params.high_neidan[i];
			_s+=this.HighNeidans[item] + ',';
		}
		for(var i=0;i<this.bb_params.params.low_neidan.length;i++){
			var item = this.bb_params.params.low_neidan[i];
		 	_s+=this.LowNeidans[item] + ',';
		}
		return _s;
	},
	option_show: function(){
		var _s = "";
		if(this.public_params.option_params.first_round_push) _s+= '已有数据通知;';
		if(this.public_params.option_params.sms_notic) _s+='短信提醒';
		if(this.public_params.option_params.email_notic) _s+='邮件提醒;';
		if(this.public_params.option_params.price_notic) _s+='降价提醒;';
		_s += '服务时长{0}天'.format(this.public_params.option_params.service_time);
		return _s;
	}

}