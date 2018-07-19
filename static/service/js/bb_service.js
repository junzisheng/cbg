var v;
var v_data;
// 获取cookie
var cookie_data = $.cookie('cookie_data');
var static_data;
var dynamic_data;
	//条件筛选的按钮

window.onload = function(){
	var cbtn = {
		data: function(){
			return {
			}
		},
		template: '<span :show="show" :index="index" :name="name" :pk="pk" class="button i-button-item " >\
					 {{show}}\
					 <span :show="show" :index="index" :name="name" :pk="pk" class="require-cancel"></span>\
				   </span>',
		props: ['v', 'show', 'index', 'pk', 'name'],
	}

	var _c = {
		template: '<i-button class="i-button-item" @click="select($event)">{{name}}<slot></slot></i-button>',
		props: ['name', 'server_type', 'area'],
		methods:{
			select: function(e){
				this.$emit('handle_click', this.server_type);
			}

		},
	};
	dynamic_data = {
		server_container_active: false,   // 服务器列表的页的动画显示
		server_detail_show: '',
		price_show: '',   // 选择价格的展示
		level_show: '',
		pet_container_show: false,
		pet_active_index : '',
		pet_show : '',
		done_show: false,
		// 设置
		option_model: false,
		option_params: {
			'first_round_push' : false,
			'sms_notic': false,
			'email_notic': false,
			'price_notic': false,
			'service_time': 7,
		},
		params : {
			'serverid': '',  // 
			'server_type': '', // 服务器范围
			// 价格
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

		},

	};
	// 静态数据
	static_data = {
		// 传给后台的数据
		is_submit: false,  // 上传
		service_id: service_id,
		args: '',
		memo: '',
		area_name: '',// 选择大区的名字
		area_server_list: [],  // 大区下的服务器
		// simple_modal
		server_range: {'': '全服', 3: '3年以上区', 1: '一年以内服', 2: '1到3年服'},
		server_list:server_list,
		server_letter_list : ['A', 'B', 'C', 'G', 'H', 'J', 'L', 'N', 'S', 'T', 'W', 'X', 'Y', 'Z'],
		// 数据模板部分
			//1.价格
		price_list: ['10-999', '1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000以上'],
			//2.等级	
		level_list: ['0级-69级','0级-79级','0级-119级','0级-139级','0级-169级','0级-180级'],
			//3.参战等级
		kindid_list : {'65': '参战45-65',  '66': '参战75-105', '67': '参战125-145', '68': '飞升120-155', '69': '渡劫155-175', '70': '化圣175', '75': '个性宠', '71': '神兽'},
			//4.召唤兽技能

		high_skill_list : high_skills,
		low_skill_list : low_skills,
		special_skills : special_skills,

			// 5.召唤兽概况: 技能数 灵性值 成长  炼兽真经数 元宵数
		// over_view_list = [{'技能数', 'skill_num'], ['灵性值', 'lingxing'], ['成长', 'growth'], ['已用炼兽真经数', 'used_lianshou_max'], '已用元宵数', 'used_lianshou_max']
		over_view : {'skill_num': '技能数', 'lingxing': '灵性值', 'growth': '成长'}, //'used_lianshou_max': '炼兽真经数', 'used_yuanxiao_max': '元宵数'},
			// 6.召唤兽类型
		pet_name_info: pet_name_info,
		pet_letter_list: ['B', 'C', 'D', 'F', 'G', 'H',  'J', 'K', 'L', 'M', 'N', 'O', 'P',  'R', 'S', 'T', 'W', 'X', 'Y', 'Z'],
		pet_id_dict: pet_id_dict,
			// 7.资质
		pet_aptitude: {'attack_aptitude': '攻击资质', 'defence_aptitude': '防御资质', 'physical_aptitude': '体力资质', 'magic_aptitude': '法力资质', 'speed_aptitude_min': '速度资质', 'speed_aptitude_max': '速度资质'},
			// 8. 属性
		pet_attr: {'max_blood': '气血', 'attack': '攻击', 'defence': '防御', 'speed': '速度', 'wakan': '灵力', 'speed_max': '速度'},
			// 9.特性
		texing_types : TexingTypes,
		TexingPositiveEffectTypes: TexingPositiveEffectTypes,
		TexingNegativeEffectTypes: TexingNegativeEffectTypes,
			// 10.内丹
		HighNeidans: HighNeidans,
		LowNeidans: LowNeidans,
	};
	
	v = new Vue({
		el: '#body',
		delimiters : ["((", "))"],
		data: function(){
			return $.extend(true, {}, static_data, params ? JSON.parse(params) : dynamic_data);
		},
		components: {
			'i-button-item': _c,
			'cbtn-item': cbtn,
		},
		methods: {
			option_help: function(){
			},
			list_or_number_eq: function(o, k, v){
				if($.isArray(o)){
					$.each(o, function(index, key){
						key[k] = v
					})
				}else{
					o[k] = v;
				}
			},
			// 区的时间范围选择
			choose: function(server_type){
				// 选择的是区的范围
				if(this.params.server_type == server_type) this.params.server_type = ''
				else this.params.server_type = server_type;
				this.params.serverid = '';
			},
			// 大区选择
			area_choose: function($e){
				var e = $e.target;
				var server_list = e.getAttribute('server_list');
				var area_name = e.getAttribute('area_name');
				if(!server_list) return false;
				server_list = server_list.split(';')  // "1,区;2,区"
				this.area_name = area_name;
				this.area_server_list = [];
				for(var i=0;i<server_list.length;i++){
					var server = server_list[i]  //  '1,区'
					var server = server.split(',')  
					this.area_server_list.push({text: server[1], extra: server[0]});
				}
				this.$nextTick(function(){
					this.$refs.server_list_choice.show();
				})
				// var name_pk = e.getAttribute('name_pk');
				// // 选择的是具体的某个区
				// this.params.serverid= name_pk.split('-')[0];
				// this.params.server_type = '';
				// this.server_detail_show = name_pk.split('-')[1];
				// this.hide_server_list();
			},
			server_choose: function(name, id){
				console.log(name, id)
				this.params.serverid= id;
				this.params.server_type = '';
				this.server_detail_show = name;
				this.hide_server_list();
			},
			more_server: function(){
				this.server_container_active = true;
			},
			hide_server_list: function(){
				this.server_container_active = false;
			},
			// 价格按钮点击事件
			price_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var show = $e.target.getAttribute('show');
				var price_min = show.split('-')[0];
				var price_max = show.split('-')[1];
				if(show == '5000以上'){
					price_max = '1000000';
					price_min = '5000';
					if(this.params.price_max == '1000000' && this.params.price_min == '5000'){
						this.params.price_min = this.params.price_max = ''
					} else{
						this.params.price_min = price_min;
						this.params.price_max = price_max;
					}
				}else{
					if(this.params.price_min == price_min &&  this.params.price_max == price_max){
						this.params.price_min = '';
						this.params.price_max = '';
					}else{
						this.params.price_min = price_min;
						this.params.price_max = price_max;
					}
				}
			},  
			level_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var show = $e.target.getAttribute('show');
				var level_min = show.split('-')[0].split('级')[0];
				var level_max = show.split('-')[1].split('级')[0];
				if(this.params.level_min == level_min && this.params.level_max == level_max){
					this.params.level_min = '';
					this.params.level_max = '';
				}else{
					this.params.level_min = level_min;
					this.params.level_max = level_max;
				}
			},
			kindid_click : function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var pk = $e.target.getAttribute('pk')
				var i = this.params.kindid.indexOf(pk);
				if(i == -1) this.params.kindid.push(pk);
				else this.params.kindid.splice(i, 1);
			},
			skill_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var pk = $e.target.getAttribute('pk')
				var i = this.params.skill.indexOf(pk);
				if(i == -1) this.params.skill.push(pk);
				else this.params.skill.splice(i, 1);
			},
			pet_click: function(){
				this.pet_container_show = true;
			},
			pet_hide: function(){
				this.pet_container_show = false;
			},
			pet_name_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var e = $e.target;
				var index = e.getAttribute('index');var show=e.getAttribute('show');
				if(this.pet_active_index == index){
					this.pet_show = '';
					this.params.type = [];
					this.pet_active_index = '';
				}else{
					this.pet_active_index = index;
					this.pet_show = show;
					this.params.type = this.pet_id_dict[show];
				}
				this.pet_container_show = false;
			},
			texing_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var pk = $e.target.getAttribute('pk');
				var i = this.params.texing.indexOf(pk);
				if(i==-1) this.params.texing.push(pk)
				else this.params.texing.splice(i, 1);
			},
			positive_effect_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var pk = $e.target.getAttribute('pk');
				var i = this.params.positive_effect.indexOf(pk);
				if(i==-1) this.params.positive_effect.push(pk)
				else this.params.positive_effect.splice(i, 1);

			},
			negative_effect_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var pk = $e.target.getAttribute('pk');
				var i = this.params.negative_effect.indexOf(pk);
				if(i==-1) this.params.negative_effect.push(pk)
				else this.params.negative_effect.splice(i, 1);
			
			},
			high_neidan_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var e = $e.target;
				var pk = e.getAttribute('pk');
				var i = this.params.high_neidan.indexOf(pk);
				if(i==-1) this.params.high_neidan.push(pk)
				else this.params.high_neidan.splice(i, 1);
			},

			low_neidan_click: function($e){
				if($e.target.nodeName.toLowerCase() != 'span') return false;
				var e = $e.target;
				var pk = e.getAttribute('pk');
				var i = this.params.low_neidan.indexOf(pk);
				if(i==-1) this.params.low_neidan.push(pk)
				else this.params.low_neidan.splice(i, 1);

			},

			// 值改变事件
			price_change: function(n, o){  // 用户输入价格的触发
				if(!this.params.price_min && !this.params.price_max) this.price_show = '';
				if(this.params.price_min && !this.params.price_max) this.price_show = '>=' + this.params.price_min;
				if(!this.params.price_min && this.params.price_max) this.price_show = '<=' + this.params.price_max;
				if(this.params.price_min && this.params.price_max) this.price_show = this.params.price_min + '-' + this.params.price_max;
				if(this.price_show.slice(-2) == '以上') this.price_show = this.price_show.slice(0,-2)
			},
			level_change: function(n, o){
				if(!this.params.level_min && !this.params.level_max) this.level_show = '';
				if(this.params.level_min && !this.params.level_max) this.level_show = '>=' + this.params.level_min;
				if(!this.params.level_min && this.params.level_max) this.level_show = '<=' + this.params.level_max;
				if(this.params.level_min && this.params.level_max) this.level_show = this.params.level_min + '-' + this.params.level_max

			},
			clear_params_click: function() {
				var that = this;
				this.simple_modal_init('确定要清空条件', function(){
					for(var k in dynamic_data){
						that[k] = $.cloneObject(dynamic_data[k]);
					}
					that.simple_modal_show = false;
				})

			},
			// simple_modal_handle: function(){
			// },
			done: function(){
				if(order_id)  return false;
				this.done_show = true;
			},
			memo_ok: function(){
				if(order_id) return false;
				// 将数据传到后台
				// 对this.params去除空的数据:
				// var params = {};
				if(this.is_submit) return false;
				var that = this;
				var _dynamic_data = {};
				for (var k in dynamic_data){
					if(k == 'params') _dynamic_data[k] = $.cloneObject(this[k]);   // 这里有个坑， 如果值为undefined的话 再stringify时 不会带有这个键值对
					else _dynamic_data[k] = this[k];
				}
				normal_ajax('/service/crawl_request', 'POST', {'args': JSON.stringify(_dynamic_data), 'memo': this.memo, 'service_id': that.service_id},function(){
						that.is_submit = true;
					} ,function(ret){
						if(ret.retcode == 'SUCC'){
							// that.$Message.success('成功');
							location.href = '/order/pay_page/' + ret.order_id;
						}else{
							that.$Message.warning(ret.description);
						}
					}, function(){
						that.$Message.warning('提交失败！');
					}, function(){
						that.is_submit = false;
					}
				)
			},
			// 订单修改参数
			modify: function(){
				if(this.is_submit) return false;
				var that = this;
				var _dynamic_data = {};
				for (var k in dynamic_data){
					if(k == 'params') _dynamic_data[k] = $.cloneObject(this[k]);   // 这里有个坑， 如果值为undefined的话 再stringify时 不会带有这个键值对
					else _dynamic_data[k] = this[k];
				}
				post_data = {'args': JSON.stringify(_dynamic_data), 'memo': this.memo, 'service_id': this.service_id, 'order_id': order_id};
				normal_ajax('/service/service_modify_api/' + order_id, 'POST', post_data, function(){
						that.is_submit = true;
					} ,function(ret){
						if(ret.retcode == 'SUCC'){
							that.$Modal.success({
								title: '订单修改成功！',
								content: '您的订单已经修改成功，当前还能能够修改' + ret.left_modify_times + '次',
								okText:'确定',
								onOk: function(){
									location.href = '/order/main'
								},
							});
						}else{
							that.$Message.warning(ret.description);
						}
					}, null, function(){
						that.is_submit = false;
					}
				)
			},

		},
		watch: {
			'params.price_min': function(){this.price_change()},
			'params.price_max': function(){this.price_change()},
			'params.level_min': function(){this.level_change()},
			'params.level_max': function(){this.level_change()},
		},
		computed: {
			price_active: function(){
				var show = this.params.price_min + '-' + this.params.price_max;
				show = show == '5000-1000000' ? '5000以上'   : show;
				return this.price_list.indexOf(show);
			},
			level_active: function(){
				var show = this.params.level_min + '级-' + this.params.level_max+'级';
				return this.level_list.indexOf(show);
			},
			// kindid_active: function(){
			// 	return this.params.kindid
			// }
			kindid_show: function(){
				var _s = "";
				// for(var item of this.params.kindid){
				// 	_s += this.kindid_list[item] + ',';
				// }
				for(var i=0;i<this.params.kindid.length;i++){
					var item = this.params.kindid[i];
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
					if(item.indexOf('max') != -1 && this.params[item] != '') _s += this.over_view[item] + '<=' + this.params[item] + ',';
					if(item.indexOf('max') == -1 && this.params[item] != '') _s += this.over_view[item] + '>=' + this.params[item] + ',';
				}
				return _s;
			},
			aptitude_show: function(){
				var _s = '';
				var pet_aptitude_keys = Object.keys(this.pet_aptitude);
				for(var i=0;i<pet_aptitude_keys.length;i++){
					var item = pet_aptitude_keys[i];
					if(item.indexOf('max') != -1 && this.params[item] != '') _s += this.pet_aptitude[item] + '<=' + this.params[item] + ',';
					if(item.indexOf('max') == -1 && this.params[item] != '') _s += this.pet_aptitude[item] + '>=' + this.params[item] + ',';
				}
				return _s;
			},
			attr_show: function(){
				var _s = '';
				var pet_attr_keys = Object.keys(this.pet_attr);
				for(var i=0;i<pet_attr_keys.length;i++){
					var item = pet_attr_keys[i];
					if(item.slice(-3) != 'max' && this.params[item] != '') _s += this.pet_attr[item] + '<=' + this.params[item] + ',';
					if(item.slice(-3) == 'max' && this.params[item] != '') _s += this.pet_attr[item] + '>=' + this.params[item] + ',';
				}
				return _s;
			},
			skill_show: function(){
				var _s = "";
				for(var i=0;i<this.params.skill.length;i++){
					var item = this.params.skill[i];
					if(Object.keys(this.high_skill_list).indexOf(item) != -1) _s += this.high_skill_list[item] + ',';
					if(Object.keys(this.low_skill_list).indexOf(item) != -1) _s += this.low_skill_list[item] + ',';
					if(Object.keys(this.special_skills).indexOf(item) != -1) _s += special_skills[item] + ',';
				}
				return _s;
			},
			texing_show: function(){
				var _s = "";
				for(var i=0;i<this.params.texing.length;i++){
					var item = this.params.texing[i];
					_s += this.texing_types[item] + ',';
				}
				for(var i=0;i<this.params.positive_effect.length;i++){
					var item = this.params.positive_effect[i];
					_s += this.TexingPositiveEffectTypes[item] + ',';
				}
				for(var i=0;i<this.params.negative_effect.length;i++){
					var item = this.params.negative_effect[i];
					_s += this.TexingNegativeEffectTypes[item] + ',';
				}
				return _s;
			},
			neidan_show: function(){
				var _s = "";
				for(var i=0;i<this.params.high_neidan.length;i++){
					var item = this.params.high_neidan[i];
					_s+=this.HighNeidans[item] + ',';
				}
				for(var i=0;i<this.params.low_neidan.length;i++){
					var item = this.params.low_neidan[i];
				 	_s+=this.LowNeidans[item] + ',';
				}
				return _s;
			},
			option_show: function(){
				var _s = "";
				if(this.option_params.first_round_push) _s+= '已有数据通知;';
				if(this.option_params.sms_notic) _s+='短信提醒';
				if(this.option_params.email_notic) _s+='邮件提醒;';
				if(this.option_params.price_notic) _s+='降价提醒;';
				_s += '服务时长{0}天'.format(this.option_params.service_time);
				return _s;
			}

		}

	});

	
	$(function(){

		(function(){
			// 移动端的键盘
			$('input').focus(function(){
				var that =this;
				setTimeout(function(){
					// that.scrollIntoView();
					that.scrollIntoViewIfNeeded();
				}, 100)
			})
			var _d = $.debounce(function(){
				$('.server-list-container').click();
			}, 500);
			$('.server-list-container').scroll(function(){
				// 滑动屏幕的时候将dropdown隐藏
				_d();
			})
		})();

	})
}

