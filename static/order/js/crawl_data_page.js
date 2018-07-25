var v;
window.onload = function(){
	var clipboard = new Clipboard('.copy-btn');
	 clipboard.on('success',function(e){
         // e.clearSelection();
         Vue.prototype.$Message.destroy();
         Vue.prototype.$Message.success('复制链接成功')
         return false;
    });
    clipboard.on('error',function(e){
         // e.clearSelection();
         Vue.prototype.$Message.destroy();
         Vue.prototype.$Message.warning('复制链接失败')
    });
	
	 v = new Vue({
			el: '#body',
	        delimiters : ["((", "))"],
			data: function(){
				return {
					scroll_height: this.get_win_size()[1] - 41  + 'px',
					// warn_model 构建
					warn_modal_header: '删除确认',
                	warn_modal_body: '<p>该商品降价后将会再次显示</p>',
                	warn_modal_closable: true,

                	totop_show: true,

					data_list: [],
					order_id: order_id,
					all_data_info: {
						query_list: [],
						refreshing: false,
						is_last: '',
						url: '/order/crawl_data_api',
						query_obj: {
							order_id: order_id,
							offset: 0,
							filter: JSON.stringify({order_id: order_id})
						},
						active: true,
					},
					price_data_info: {  // 降价商品
						query_list: [],
						refreshing: false,
						is_last: '',
						url: '/order/crawl_data_api',
						active: false,
						query_obj: {
							offset: 0,
							filter: JSON.stringify({old_price__isnull: 'False', order_id: order_id})
						},
					},
					show: '全部记录',
					edit: false,
					all_choose: false,
				}
			},
			methods: {
				query_list_handle: function(old_list, new_list){
					for(var i=0;i<new_list.length;i++){
						var item = new_list[i];
						item.link = 'http://xyq-m.cbg.163.com/cgi/mweb/product/detail/{0}/{1}'.format(item['serverid'], item['game_ordersn'])
						console.log(item.icon)
						if(item.service_id == 1 || item.service_id == 3){
						    item.icon = 'https://cbg-xyq.res.netease.com/images/small/{0}.gif'.format(item.icon)
						}else if(item.service_id == 2){
						    item.icon = 'https://cbg-xyq.res.netease.com/images/app/bigface/{0}.png'.format(item.icon)
						}
						if(!item.checked){
							item.checked = false;
							this.all_choose = false;
						}
					};
					return old_list.concat(new_list);
				},
				switch_tab: function(){
					this.$refs.wsitch_tab_menu.show()
				},
				choose_price_down: function(key){
					this.all_data_info.active = key == '全部记录';
					this.price_data_info.active = key == '降价记录';
					this.show = key;
					this.edit = false;
				},
				container_click: function(data, e){
					if(this.edit) data.checked = data.checked ? false: true;
					else window.open(data.link, 'link')
				},
				edit_click: function(){
					this.edit = !this.edit;
				},
				all_choose_click: function(){
					this.all_choose = !this.all_choose;
					for(var i=0;i<this.info.query_list.length;i++){
						var item = this.info.query_list[i];
						item.checked = this.all_choose;
					};
				},
				checked_exist: function(){
					// 判断是否有checked被选中
					var del_list = []
					for(var i=0;i<this.info.query_list.length;i++){
						var item = this.info.query_list[i];
						if(item.checked) del_list.push(item);
					}
					return del_list;
				},
				del_btn_click: function(){
					if(!this.checked_exist().length) return false;
					this.warn_modal_show = true;
				},
				warn_del_click: function(){
					var that = this;
					var del_list = this.checked_exist();
					if(!del_list) return false;
					that.warn_modal_loading = true;
					that.warn_modal_footer = '删除中';
					var del_id_list = [];
					for(var i=0;i<del_list.length;i++){
						var item = del_list;
						del_id_list.push(item.id);
					}
					normal_ajax('/order/delete_crawl_data_api', 'GET', {'del_id_list': JSON.stringify(del_id_list), order_id: that.order_id},null,function(ret){
						if(ret.retcode == 'SUCC'){
							for(var i=0;i<del_list.length;i++){
								var item = del_list[i];
								var index = that.info.query_list.indexOf(item);
								that.info.query_list.splice(index, 1);
							}
							that.warn_modal_loading = false;
							that.warn_modal_show = false;
							that.warn_modal_footer = '删除';
							that.$Message.success('删除成功');
							that.$nextTick(function(){  // dom更新完成的回调  this.nextTick 数据更新完成的回调
							// 删除成功后如果页面没有滚动条，则继续添加一些数据
								if(document.documentElement.scrollHeight <= document.documentElement.offsetHeight + 10){
									that.refresh_func(that.info);
									that.all_choose = false;
								}
				            })
						}else{
							that.warn_modal_loading = false;
							that.warn_modal_show = false;
							that.warn_modal_footer = '删除';
							that.$Message.error(ret.description);
						}
					})
				},
				switch_tab_active: function(){
					return !!this.$refs.wsitch_tab_menu && !!this.$refs.wsitch_tab_menu.$refs.fullscreen.show;					
				},
			},
			computed: {
				info: function(){
					return this.show == '全部记录' ? this.all_data_info : this.price_data_info;
				},
				
			},
			watch: {
				edit: function(nv){
					if(!this.edit){
						this.all_choose = false;
						var _list = this.all_data_info.query_list.concat(this.price_data_info.query_list);
						for(var i=0;i<_list.length;i++){
							var item = _list[i];
							item.checked = false;
						}
					}
				},

			},

		})

}

