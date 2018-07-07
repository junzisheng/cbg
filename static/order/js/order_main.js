var v;
window.onload = function(){
	var order_item = {
		template: '<a :href="\'/order/order_detail/\' + order.id"> <div class="order-item-thumb-container" > <!-- 顶部信息 -->\
					    <div class="order-item-top-container">\
					        <div style="float:left">\
					            {{ order.status == \'待付款\' ? \'下单时间\' : \'支付时间\' }}：{{ order.status == \'待付款\' ? order.create_time : order.pay_time}}\
					        </div>\
					        <div style="float:right;color:#fe555c">\
					            {{order.status}}\
					        </div>\
					    </div>\
					    <!-- 中部图片， memo -->\
					    <div class="order-item-center-container">\
					        <div class="order-thumb-container" >\
					            <img src="/static/order/img/102207.gif">\
					        </div>\
					        <div class="order-thumb-text-container">\
					            <span class="order-type">召唤兽</span>\
					            <div class="order-memo clamp-line-text-hidden" style="-webkit-line-clamp: 4;">'+  // 这里有个坑 不能用\ 这样会被认为对\1600
					            	'{{order.memo}}\
					            </div>\
					        </div>\
					    </div>\
					    <!-- 底部付款 -->\
					    <div>\
					        <!-- 价格 -->\
					        <div style="text-align: right;font-size: 13px;height:41px;line-height: 41px;padding-right:10px;margin-bottom:">\
					            &nbsp;&nbsp;&nbsp;付款: <span style="font-size:18px;font-weight: blod;">￥{{ (order.real_price / 100).toFixed(2)}}</span> \
					        </div>\
					        <!-- 操作 -->\
					        <slot></slot>\
					    </div>\
				    </div></a>'
				,
		props: ['order']

	}

//scrollIntoView(alignWithTop)


	v = new Vue({
		el: '#body',
		delimiters : ["((", "))"],
		data: function(){
			return {
				scroll_height: this.get_win_size()[1] - 51 - 46 + 'px',
				totop_show: true,
				tab_active: tab_active,
				tab_object: {
					wait_pay_info: {
						title: '待付款',
						active: active_tab == '待付款',
					},
					doing_order_info: {
						title: '进行中',
						active: active_tab == '进行中',
					},
					done_order_info: {
						title: '已完成',
						active: active_tab == '已完成',
					},
					all_order_info: {
						title: '全部订单',
						active: active_tab == '全部订单',
					},
				},
				wait_pay_info: {
					status: '待付款',
					query_list: [],
					refreshing: false,
					is_last: '',
					url: '/order/pull_order_data/',
					active: active_tab == '待付款',
					query_obj: {
						filter: JSON.stringify({status: '待付款'}),
						offset: 0,
					}
				},
				doing_order_info: {
					status: '进行中',
					query_list: [],
					refreshing: false,
					is_last: '',
					url: '/order/pull_order_data/',
					active: active_tab == '进行中',
					query_obj: {
						filter: JSON.stringify({status: '进行中'}),
						offset: 0,
					}
				},
				done_order_info: {
					status: '已完成',
					query_list: [],
					refreshing: false,
					is_last: '',
					url: '/order/pull_order_data/',
					active: active_tab == '已完成',
					query_obj: {
						filter: JSON.stringify({status: '已完成'}),
						offset: 0,
					}
				},
				all_order_info: {
					status: '全部订单',
					query_list: [],
					refreshing: false,
					is_last: '',
					url: '/order/pull_order_data/',
					active: active_tab == '全部订单',
					query_obj: {
						offset: 0,
					}
				}
			}
		},
		// created: function(){
		// 	this.bind_scroll_refresh();
		// },
		components: {
			'order-item': order_item,
		},
		methods: {
			tab_click: function(key){
				this.tab_active = key;
				var _list = ['wait_pay_info', 'doing_order_info', 'all_order_info', 'done_order_info'];
				for(var i=0;i<_list.length;i++){
					var _key = _list[i]
					this[_key].active = _key == key;
				}
			},
			del_order: function (order_id){
				var that = this;
				// this.simple_modal_title = '您确定要删除这笔订单吗';
				// this.simple_modal_init('您确定要删除这笔订单吗', function(){
				normal_ajax('/order/delete_order/{0}'.format(order_id),'GET', null, null, function(ret){
					if(ret.retcode==='SUCC'){
						// 将其它tab中的相关订单也删除
						var tab_object_keys = Object.keys(that.tab_object)
						for(var i=0;i<tab_object_keys.length;i++){
							var item = tab_object_keys[i];
							var query_list = that[item].query_list
							for(var i;i<query_list.length;i++){
								var temp= query_list[i];
								if(temp.id == order_id){
									var i = that[item].query_list.indexOf(temp);
									that[item].query_list.splice(i, 1);
								}
							}
						}
						that.simple_modal_show = false;
						that.$Message.success('取消成功');
					}else{
						that.$Message.warning(ret.description);
					}
				})
			},
		},
		computed: {
			// merge_list(){
			// 	return this.wait_pay_info.list.concat.(this.doing_order_info.list).concat(this.done_order_info.list).cocat(this.all_order_info.list);
			// }
		}


	})
}






