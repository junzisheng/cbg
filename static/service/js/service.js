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
		// 静态数据
	static_data = {
		// 传给后台的数据
		service_obj: {
			1: '召唤兽服务',
			2: '角色服务'
		},
		is_submit: false,  // 上传
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
	$.extend(static_data, role_static);
	public_dynamic = {
		server_container_active: false,   // 服务器列表的页的动画显示
		server_detail_show: '',
		done_show: false,
		option_model: false,
		service_id: service_id,
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
		},
	};
	dynamic_data ={};
	dynamic_data.public_params = order_public_params || public_dynamic;  // 各服务共有的动态参数
	dynamic_data.bb_params = order_bb_params || bb_params;
	dynamic_data.role_params = order_role_params || role_params;
	// 方法
	var methods = {
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
		// 切换服务
		service_choose: function(){
			this.$refs.switch_tab_menu.show();
		},
		switch_tab_active: function(){
			return !!this.$refs.switch_tab_menu && !!this.$refs.switch_tab_menu.$refs.fullscreen.show;					
		},
		service_choose_callback: function(k, v){
			this.public_params.service_id = v
		},
		// 区的时间范围选择
		choose: function(server_type){
			// 选择的是区的范围
			if(this.public_params.params.server_type == server_type) this.public_params.params.server_type = ''
			else this.public_params.params.server_type = server_type;
			this.public_params.params.serverid = '';
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
		},
		server_choose: function(name, id){
			this.public_params.params.serverid= id;
			this.public_params.params.server_type = '';
			this.public_params.server_detail_show = name;
			this.hide_server_list();
		},
		more_server: function(){
			this.public_params.server_container_active = true;
		},
		hide_server_list: function(){
			this.public_params.server_container_active = false;
		},
		// 价格按钮点击事件
		
		clear_params_click: function() {
			var that = this;
			this.simple_modal_init('确定要清空条件', function(){
				// 清除服务选项
				if(that.public_params.service_id == 1){
					for(var k in bb_params){
						that.bb_params[k] = $.cloneObject(bb_params[k]);
					}
				}else if(that.public_params.service_id == 2){
					for(var k in role_params){
						that.role_params[k] = $.cloneObject(role_params[k]);
					}
				}
				that.simple_modal_show = false;
			})

		},
		// 生成订单前的数据准备
		ajax_params_ready: function(_public_params, _private_params){
			// 公共数据
			for (var k in this.public_params){
				if(typeof this.public_params[k] == 'object'){
				 	_public_params[k] = $.cloneObject(this.public_params[k]);   // 这里有个坑， 如果值为undefined的话 再stringify时 不会带有这个键值对
				} else{ 
					_public_params[k] = this.public_params[k]
				}
			}
			// 各自的私有数据
			// 1.召唤兽
			if(this.public_params.service_id == 1){
				for (var k in this.bb_params){
					if(typeof this.bb_params[k] == 'object'){
					 	_private_params[k] = $.cloneObject(this.bb_params[k]);   // 这里有个坑， 如果值为undefined的话 再stringify时 不会带有这个键值对
					} else{ 
						_private_params[k] = this.bb_params[k]
					}
				}
			// 角色
			}else if(this.public_params.service_id == 2){
				for (var k in this.role_params){
					if(typeof this.role_params[k] == 'object'){
					 	_private_params[k] = $.cloneObject(this.role_params[k]);   // 这里有个坑， 如果值为undefined的话 再stringify时 不会带有这个键值对
					} else{ 
						_private_params[k] = this.role_params[k]
					}
				}
				// 一些特殊处理
				if(_private_params.params.xiangrui_list.length == 0){
					_private_params.params.xiangrui_match_all = "";
				}
				if(_private_params.params.pet_type_list.length == 0){
					_private_params.params.pet_match_all = "";
				}
				if(!_private_params.params.school_skill_level){
					_private_params.params.school_skill_num= "";
				}
			}
		},
		done: function(){
			if(order_id)  return false;
			this.public_params.done_show = true;
		},
		memo_ok: function(){
			if(order_id) return false;
			// 将数据传到后台
			// 对this.params去除空的数据:
			// var params = {};
			if(this.is_submit) return false;
			var that = this;
			var _public_params = {};
			var _private_params = {}
			this.ajax_params_ready(_public_params, _private_params);
			var _params = {public_params: _public_params, private_params: _private_params}
			normal_ajax('/service/crawl_request', 'POST', {'params': JSON.stringify(_params)},function(){
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
			var _public_params = {};
			var _private_params = {}
			this.ajax_params_ready(_public_params, _private_params);
			var _params = {public_params: _public_params, private_params: _private_params};
			console.log(_params);
			normal_ajax('/service/service_modify_api/' + order_id, 'POST', {'params': JSON.stringify(_params)}, function(){
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
	};
	$.extend(methods ,bb_methods, role_methods);
	var watch = {};
	$.extend(watch, bb_watch, role_watch);
	var computed = {}
	$.extend(computed, bb_computed, role_computed)


	
	v = new Vue({
		el: '#body',
		delimiters : ["((", "))"],
		data: function(){
			return $.extend(true, {}, static_data, dynamic_data);
		},
		components: {
			'i-button-item': _c,
			'cbtn-item': cbtn,
		},
		methods: methods,
		watch: watch,
		computed: computed,
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

