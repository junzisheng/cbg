

////////////////// 公用的方法 //////////////////////////////////////
// js报错跟踪
window.onerror = function(msg, url, line, col, error){
    var col = col || (window.event && window.event.errorCharacter) || 0;
    var err_msg = "";
    if(error && error.stack){
        err_msg = error.stack.toString();
    }else if(arguments.callee){
        var ext = [];
        var fn = arguments.callee.caller;
        var floor = 3; //这里只拿三层堆栈信息
        while (fn && (--floor>0)) {
            ext.push(fn.toString());
            if (fn === fn.caller) {
                break;//如果有环
            }
            fn = fn.caller;
        }
        ext = ext.join(",");
        err_msg = error.stack.toString();
    }
    report_data = {err_js: url, line: line, col: col, err_msg: err_msg};
    normal_ajax('/others/track_js', 'POST', report_data)
    if(superuser){
        var v = new Vue();
        v.$Modal.error({
            title: 'js发生错误，请截图给管理员',
            content: '<div>{0}</div>\
            <div>第{1}行,{2}列</div>\
            <div>错误详情</div>\
            <div style="word-break: break-all;word-wrap: break-word;">{3}</div>'.format(url, line, col, err_msg)
        })

    }
}
$(function(){
    // 控制a标签的点击事件
    $('a').click(function(){
        if($(this).attr('b') == '1'){
            alert(123);
            return;
        }
        var a = $(this).clone();
        var has_href = true;
        a.attr('href', function(i, href){
            has_href = !!href;
            if(!has_href) return false;
            return encodeURI(href + (href.indexOf('?') == -1 ? '?' :'&') + 'timestamp=' + get_timestamp());
        })
        if(!has_href) return false;
        a.attr('b', '1');
        a[0].click();
        return false;
    })


})
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if(args[key]!=undefined){
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}
// 通用的AJAX操作，请求URL，请求数据为data_user，成功和失败分别调用不同的函数
function normal_ajax(url, method, _data, before_callback,  succ_callback , fail_callback , complete_callback , datatype , args_advance, sync){
    if(url.indexOf('?') != -1) url+= '&timestamp=' + get_timestamp()
    else url += '?timestamp=' + get_timestamp();
    url = encodeURI(url);

    var arg_ajax = {    url         : url,
                        async       : sync,
                        type        : method || "GET",
                        data        : _data,
                        dataType    : datatype || "json",
                        beforeSend  : function(xhr){
                            xhr.setRequestHeader("X-CSRFtoken", csrf_token);
                            if ($.isFunction(before_callback))
                                before_callback()
                        },

                        complete    : function(XMLHttpRequest, textStatus){
                                        // textStatus的值：success,notmodified,nocontent,error,timeout,abort,parsererror

                                        if ($.isFunction(complete_callback))
                                            complete_callback(XMLHttpRequest, textStatus)
                                    } ,

                        success     : function(data, textStatus) {
                                        if(data.retcode != 'SUCC'){
                                            if(data.msg == 'LOGIN'){
                                                login_redirect()
                                                return false;
                                            }
                                        }
                                        var timestamp = parseFloat(data.timestamp);
                                        console.log(url, 'ajax耗时',  (get_timestamp() - timestamp))
                                        if ($.isFunction(succ_callback)){
                                            succ_callback(data, textStatus)
                                        }
                                    } ,

                        error       : function (XMLHttpRequest, textStatus, errorThrown) {
                                        // XMLHttpRequest.readyState:
                                        //   0 － （未初始化）还没有调用send()方法
                                        //   1 － （载入）已调用send()方法，正在发送请求
                                        //   2 － （载入完成）send()方法执行完成，已经接收到全部响应内容
                                        //   3 － （交互）正在解析响应内容
                                        //   4 － （完成）响应内容解析完成，可以在客户端调用了
                                        // XMLHttpRequest.status:
                                        //   200-确定。客户端请求已成功。
                                        //   3xx-重定向
                                        // textStatus的值：null, timeout, error, abort, parsererror4
                                        // errorThrown的值：收到http出错文本，如 Not Found 或 Internal Server Error.

                                        if ($.isFunction(fail_callback))
                                            fail_callback(XMLHttpRequest, textStatus, errorThrown);
                                    }
                    };

    if (args_advance)
        $.extend(arg_ajax, args_advance);

    return $.ajax(arg_ajax);
}

function form_ajax(url, data, before_callback,succ_callback, fail_callback, complete_callback, sync){
    if(url.indexOf('?') != -1) url+= '&timestamp=' + get_timestamp()
    else url += '?timestamp=' + get_timestamp();
    url = encodeURI(url);
    var form = new FormData();
    for(var key in data){
        form.append(key, data[key]);
    }
    var arg_ajax = {    
                    url         : url,
                    async       : sync,
                    type        : 'POST',
                    data        : form,
                    dataType    : 'json',
                    cache: false,
                    processData : false,
                    contentType : false,
                    beforeSend   : function(xhr){
                        xhr.setRequestHeader("X-CSRFtoken", '{{csrf_token}}');
                        if ($.isFunction(before_callback))
                            before_callback()
                    },
                    complete    : function(XMLHttpRequest, textStatus){
                                    if ($.isFunction(complete_callback))
                                        complete_callback(XMLHttpRequest, textStatus)
                                } ,
                    success     : function(data, textStatus) {
                                    var timestamp = parseFloat(data.timestamp);
                                    console.log(url, 'ajax耗时',  (get_timestamp() - timestamp))
                                    if(data.retcode != 'SUCC'){
                                        if(data.msg == 'LOGIN'){
                                            login_redirect()
                                            return false;
                                        }
                                    }
                                    if ($.isFunction(succ_callback)){
                                        succ_callback(data, textStatus)
                                    }
                                } ,
                    error       : function (XMLHttpRequest, textStatus, errorThrown) {
                                    if(window.navigator.onLine === false){
                                        Vue.$Message.warning('网络连接异常！');
                                    }
                                    if ($.isFunction(fail_callback))
                                        fail_callback(XMLHttpRequest, textStatus, errorThrown);
                                }
                    };
    $.ajax(arg_ajax);
}

function guid() {
    function S4() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function sns_time(str_time, now){
    // 不对的写法
//     var now =  now || new Date()
//     var pre = new Date(Date.parse(str_time))
//     var now_year = now.getFullYear();
//     var now_month = now.getMonth() + 1;
//     var now_day = now.getDate();
//     var now_hour = now.getHours();
//     var now_minute = now.getMinutes();
//     var now_seconds = now.getSeconds();
//     var pre_year = pre.getFullYear();
//     var pre_month = pre.getMonth() + 1;
//     var pre_day = pre.getDate();
//     var pre_hour = pre.getHours();
//     var pre_minute = pre.getMinutes();
//     var pre_seconds = pre.getSeconds();
//     if(now_year - pre_year > 1){
//         return  now_year - pre_year + '年前';
//     }
//     if(now_month - pre_month > 1){
//         return now_month - pre_month + '月前';
//     }
//     if(now_day - pre_day > 1){
//         return now_day - pre_day + '天前';
//     }
//     if(now_hour - pre_hour){
//         return now_hour - pre_hour + '小时前';
//     }
//     if(now_minute - pre_minute > 1){
//         return now_minute - pre_minute + '分钟前';
//     }
//     return '刚刚';
}

//验证手机号格式
function checkMobile(value) {
    if (!/^1[3|4|5|8|7|6|9][0-9]\d{4,8}$/.test(value) || value == "" || value.length != 11) {
        return false
    }
    return true
}

function login_redirect(){
    location.href = '/user/login?redirect=' + location.href;
}

function get_timestamp(){
    return new Date().getTime() / 1000
}
function get_win_size(){
    if(g_app_os == 'ios'){
            return [$(window).width() , window.innerHeight || $(window).height()];
    }else{
        return [$(window).width() , $(window).height()];
    }
}
function get_document_size(el){
    var $el;
    if(el == undefined) $el = $(document)
    else $el = $(el);
    return [$el.width(), $el.height()]
}

$.extend({
    top_notic: function(text){
        var time = function(){
           setTimeout(function(){
                top_notic.fadeOut();
            }, 2000)
        }
        $('#top_notic').remove();
        // if(top_notic.length){
        //     top_notic.text(text).stop().hide().fadeIn(time);

        // }else{
        top_notic = $('<div id="top_notic">{0}</div>'.format(text));
        $('body').append(top_notic);
        top_notic.fadeIn(time);
        // }
    },
    fullScreen: function () {  
        var elem = document.documentElement;  
        if (elem.webkitRequestFullScreen) {  
            elem.webkitRequestFullScreen();  
        } else if (elem.mozRequestFullScreen) {  
            elem.mozRequestFullScreen();  
        } else if (elem.requestFullScreen) {  
            elem.requestFullscreen();  
        }

   },
    exitFullScreen: function() {  
        var elem = document;  
        if (elem.webkitCancelFullScreen) {  
            elem.webkitCancelFullScreen();  
        } else if (elem.mozCancelFullScreen) {  
            elem.mozCancelFullScreen();  
        } else if (elem.cancelFullScreen) {  
            elem.cancelFullScreen();  
        } else if (elem.exitFullscreen) {  
            elem.exitFullscreen();  
        } 
        return false;
    },
    // 一个简单的函数节流
    debounce: function debounce(fn, delay){
        var timestamp = 0;
        function _(){
            if(Date.now() - timestamp>=delay) fn();
            timestamp = Date.now();  
        }
        return _;
    },
    cloneObject:  function(obj){
        var str, newobj = obj.constructor === Array ? [] : {};
        if(typeof obj !== 'object'){
            return obj;
        } else if(window.JSON){
            str = JSON.stringify(obj), //系列化对象
            newobj = JSON.parse(str); //还原
        } else {
            for(var i in obj){
                newobj[i] = typeof obj[i] === 'object' ? 
                cloneObj(obj[i]) : obj[i]; 
            }
        }
        return newobj;
    },
})


///////////////////////// Vue的部分: 过滤器模块等;///////////
Vue.filter('gtlt', function(key){
    return key.slice(-3) == 'max' ? '<= ' : '>= ';
});

// 全局混入
// window.getWinSize= function(){
//     if(g_app_os == 'ios'){
//         return [$(window).width() , window.innerHeight || $(window).height()];
//     }else{
//         return [$(window).width() , $(window).height()];
//     }

// }

// window.getScrollPos= function(){
//     return [$(document).scrollLeft() , $(document).scrollTop()]
// }
var base_mixin =  {
    data: function(){
        var service_obj = {};
        for(var i=0;i<service_list.length;i++){
            var _obj = service_list[i];
            service_obj[_obj.id] = _obj;
        }
        return {
                service_obj: service_obj,
                menu_choice_list: [{text: '首页'}, {text:'我的'}, {text:'服务'}, {text:'提交问题'}],
                csrf_token: csrf_token,
                render_loading: true,  // 页面渲染完成前的loading图片
                loading_show: false, // ajax数据加载的底部bottom
                // warn_model
                warn_modal_show: false,
                warn_modal_header: '',
                warn_modal_body: '',
                warn_modal_footer: '删除',
                warn_modal_loading: false,
                warn_modal_closable: true,
                // toptop
                totop_show: false,
                // simple_modal
                simple_modal_show: false,
                simple_modal_title: '',
                simple_modal_left: '取消',
                simple_modal_right: '确定',
                this: this,
                // pay_list
             

            }
    },
    mounted: function(){
        this.render_loading = false;
    },
    methods: {
        warn_del_click: function(){},
        simple_modal_handle: function(){},
        simple_modal_init: function(title, func){
            this.simple_modal_title = title;
            this.simple_modal_handle = func;
            this.simple_modal_show = true;
        },
        get_el_size: function(el){
            var $el;
            if(el == undefined) $el = $(window)
            else $el = $(el);
            return [$el.width() , $el.height()];
        },

        get_win_size: function(){
            if(g_app_os == 'ios'){
                    return [$(window).width() , window.innerHeight || $(window).height()];
            }else{
                return [$(window).width() , $(window).height()];
            }
        },
        get_document_size: function(el){
            var $el;
            if(el == undefined) $el = $(document)
            else $el = $(el);
            return [$el.width(), $el.height()]
        },
        get_scroll_pos: function(el){
            var $el;
            if(el == undefined) $el = $(document)
            else $el = $(el);
            return [$el.scrollLeft() , $el.scrollTop()];
        },
        is_visible_on_screen: function(full_viewable, el, box_el){
        // 判断该元素是否在屏幕上可见
            var othis = $(el);
            if (!othis.length)
                return false;
            // console.log($('.slot-container', box_el)[0])

            var size_win    = box_el === window ? this.get_win_size() : this.get_el_size(box_el);
            var scroll_win  = this.get_scroll_pos(box_el)

            var offset_this = othis.offset();
            var height_this = othis.outerHeight();
            // console.log(size_win, scroll_win, offset_this, height_this, el)
            // 没有在容器里面刷新
            if(box_el === window){
                if (full_viewable)
                {
                    // 上边必须大于窗口上边，下边必须小于窗口下边
                    if ( (offset_this.top > scroll_win[1])
                        &&  (offset_this.top + height_this  < scroll_win[1] + size_win[1]) )
                        return true;

                    return false;
                }
                else{
                    // 当元素在窗口上方，或元素上边框在窗口的下方，表示窗口在窗口不可见
                    if ( (offset_this.top + height_this < scroll_win[1])
                        ||  (offset_this.top > scroll_win[1] + size_win[1]) )
                        return false;
                    return true;
                }
            }else{
                $box_el = $(box_el)
                if($box_el.offset().top + $box_el.outerHeight() - $(el).outerHeight() + 10 >= $(el).offset().top){
                    return true;
                }
            }
        },
        // footer底部菜单点击
        menu_show: function(){
            this.$refs.menu.show();
        },
        menu_choose: function(text){
            switch(text){
                case '首页':
                    location.href = '/';
                    break
                case '我的':
                    location.href = '/user/mine';
                    break
                case '服务':
                    location.href = '/service/index';
		    break
                case '提交问题':
                    location.href = '/others/bug_submit_page';
            }
        },
        location_back: function(){history.back()},
    }
}


var scroll_refresh_mixin = {
    // 监听滚动， 目前支持 自定义元素监听和window监听
    // 自定义则为每个自定义元素绑定， window由于只能监听一个， 所以将tab处理函数放到list window滚动回掉处理所有的滚动函数
    data: function(){
        return {
            // refresh_obj_list : [],   //[[refresh_obj, tab_obj]]
            win_scroll_handler : [],
        }
    },
    methods: {
        // 刷新方法
        refresh_func: function(obj){
            var that = this;  // this>>>>子组件
            if(obj.refreshing || obj.is_last) return false;  //正在刷新的和刷新到结尾了
            obj.refreshing = true;
            normal_ajax(obj.url, 'GET', obj.query_obj, null,function(ret){
                if(ret.retcode === 'SUCC'){
                    if(that.query_list_handle && typeof that.query_list_handle == 'function'){
                        obj.query_list = that.query_list_handle(obj.query_list, ret.query_list);
                    }else{
                        obj.query_list = obj.query_list.concat(ret.query_list);
                    }
                    obj.query_obj.offset = ret.offset;
                    obj.is_last = ret.is_last;
                }
            }, null, function(){obj.refreshing = false});
        },
        // 监听滚动事件
        bind_scroll_refresh: function(box_el, visible_el, refresh_obj){
            var that = this;
            var $visible_el = $(visible_el);
            if(box_el == window){
                this.win_scroll_handler.push(function(){
                    if(refresh_obj.active && that.is_visible_on_screen(false, visible_el, box_el)) {
                        that.refresh_func(refresh_obj);
                        return false;
                    }
                })
                if(this.win_scroll_handler.length === 1 ){
                    window.onscroll = function(){
                        for(var i=0;i < that.win_scroll_handler.length;i++){
                            that.win_scroll_handler[i]();
                        };
                    };
                }
                return false;
            }

            box_el.onscroll = function(){
                // 获取当前展示的tab
                if(that.is_visible_on_screen(false, visible_el, box_el)) {
                    that.refresh_func(refresh_obj);
                    return false;
                }
            };
        },
    },
}

Vue.mixin({
     mixins: [base_mixin, scroll_refresh_mixin],
})





// 自定义的监听滚动的元素
var Scroll = {
    delimiters : ["((", "))"],
    template: "<div ref='scroll_el' style='overflow-x: hidden;overflow-y: auto;'>\
                 <div class='slot-container'>\
                     <slot></slot>\
                 </div>\
                <div v-if='refresh_obj.is_last && !refresh_obj.refreshing && refresh_obj.query_list.length == 0' class='no-data-notic'>\
                    暂无数据\
                </div>\
                 <div class='no-data-notic' v-if='refresh_obj.is_last && refresh_obj.query_list.length != 0'>\
                    ㄟ( ▔, ▔ )ㄏ&nbsp;&nbsp;&nbsp;再怎么找也没有啦\
                </div>\
                <i-col ref='loading' class='loading-container' :style='{\"visibility\": refresh_obj.refreshing ? \"visible\" : \"hidden\"}' span='8'>\
                    <spin fix>\
                        <icon type='load-c' size=18 class='load'></icon>\
                        <div>加载中....</div>\
                    </spin>\
                </i-col>\
              </div>",
    props: ['refresh_obj', 'scroll_win'],
    // refresh_obj: 存储ajax请求数据所需要的数据， that指向vue实例, scroll_win 是否为window绑定
    mounted: function(){
        // 将监听对象丢入到scroll中 scroll的时候会增量刷新
        // this.that.refresh_obj_list.push([this.refresh_obj, this.tab_obj])
        // 立刻刷新
        if(this.refresh_obj.active){
            this.$root.refresh_func(this.refresh_obj);
        }
        // console.log(this.$refs.scroll_el);
        this.$root.bind_scroll_refresh(this.scroll_win ? window : this.$refs.scroll_el, this.$refs.loading.$el, this.refresh_obj)
    },
    watch:{
        // 监听tab active
        'refresh_obj.active': {
            handler: function(){
                if(this.refresh_obj.is_last === ''){
                    this.$root.refresh_func(this.refresh_obj);
                };
            },
            immediate: false // 变量无效
        },
        // 监听排序
        'refresh_obj.order': function(){
            this.refresh_obj.query_list = [];
            this.refresh_obj.is_last = false;
            this.$root.refresh_func(this.refresh_obj);
        },
    }
}

// Tabs组件
var tabs_conmonent = {
    template: '<div style="position: relative">\
                    <ul class="tabs-container">\
                        <li v-for="(v,k, index) in tabs_object" :class="{\'tabs-active\': v.active}" :style="{\'width\': li_width}" @click.stop="tab_click(k, 1)">{{v.title}}</li>\
                    </ul>\
                    <ul class="panel-contanier swiper-container" :class="cls" :style="{height: content_height || \'auto\'}">\
                        <div class="swiper-wrapper">\
                            <li class="swiper-slide" v-for="(v,k, index) in tabs_object" :index="index">\
                                <slot :name="\'panel-\' + index"></slot>\
                            </li>\
                        </div>\
                        <slot :name=" \'bottom_loading\' "></slot>\
                    </ul>\
                </div>\
             ',
    props : ['tab_object', 'content_height'],
    data: function(){
        var swiper_key = 'swpier_' + parseInt(Math.random()*10000 + 1)
        var cls = [];
        if(!!this.content_height){
            cls.push(tab_container_fixed);
        }
        cls.push(swiper_key)
        return {
            tabs_object: this.tab_object,
            li_width: 100/Object.keys(this.tab_object).length + '%',
            swiper_key: swiper_key,
            object_list: [],
            swiper: null,
            cls: cls,
        }
    },
    mounted: function(){
        var n = 0;
        var initialSlide = 0;
        for(var item in this.tab_object){
            var ob = this.tab_object[item];
            ob.key = item;
            this.object_list.push(ob)
            if(ob.active == true){
                initialSlide = n;
            }
            n++;
        }
        var vm = this;
        this.swiper = new Swiper ('.' + vm.swiper_key, {
            initialSlide :initialSlide,
            on: {
                slideChangeTransitionEnd: function(){
                    var key = vm.object_list[this.activeIndex].key;
                    vm.tab_click(key);
                }
            },
        })
    },
    methods: {
        tab_click: function(key, c){
            if(c){
                //获取key对应得swiper_list索引
                for(var i=0;i<this.object_list.length;i++){
                    var item = this.object_list[i];
                    if(item.key == key){
                        this.swiper.slideTo(i, 0, false)
                    }
                }

            }
            for(var item in this.tab_object) this.tab_object[item].active = false;
            this.tab_object[key].active = true;
            this.$emit('handle_click', key);
        }
    },

};

// var a_item = {
//     template: '<a @click="handleClick"><slot></slot></a>',
//     props: ['href',]
//     methods: {
//         handleClick: function(){
//             var href =  this.href + (this.href.indexOf('?') != -1 ? '&' : '?') + 'timestamp=' + get_timestamp(); 
//             var _a = document.createElement('a');
//             _a.href = href;
//             _a.click();
//         }
//     }

// }
var form = {
    delimiters : ["((", "))"],
    props: ['action', 'method'],
    template: '\
    <div ref="form_wrap">\
        <form ref="form" style="display:none">\
            <slot>\
            </slot>\
        </form>\
    </div>\
    ',
    methods: {
        submit: function(){
            this.$refs.form.action = this.action.indexOf('?') != -1 ? this.action + '&timestamp=' + get_timestamp() : this.action + '?timestamp=' + get_timestamp();
            this.$refs.form.method = this.method || 'GET';
            this.$refs.form.submit();
        }
    }
}

var pay_channel = {
    template: '<div class="pay-tab-conmonent">\
                    <ul>\
                        <form-item style="display:none" id="pay_form" method="post" :action="\'/order/currency_pay_page\'" ref="form2">\
                            <input name="order_id" type="text" :value="((token.orderid))">\
                            <input type="hidden" name="csrfmiddlewaretoken" :value="((csrf_token))">\
                        </form-item>\
                        <form-item style="display:none" id="pay_form" method="post" :action="\'https://pay.bbbapi.com/\'" ref="form">\
                            <input name="goodsname" type="text" :value="((token.goodsname))">\
                            <input name="uid" type="text" :value="((token.uid))">\
                            <input name="price" type="text" :value="((token.price))">\
                            <input name="istype" type="text" :value="((token.istype))">\
                            <input name="notify_url" type="text" :value="((token.notify_url))">\
                            <input name="return_url" type="text" :value="((token.return_url))">\
                            <input name="orderid" type="text" :value="((token.orderid))">\
                            <input name="orderuid" type="text" :value="((token.orderuid))">\
                            <input name="key" type="text" :value="(( token.key ))">\
                            <input type="submit" >\
                        </form-item>\
                        <li v-for="(obj, k) in pay_object" @click.stop="pay_type_select(obj.type)" :style="{\'opacity\': currency < real_price && obj.type == 3 ? 0.4 : 1}">\
                            <span>\
                                <Icon type="ios-circle-outline" style="font-size: 20px;" v-show="!obj.active" @click.native="pay_type_select(obj.type)"></Icon>\
                                <Icon type="ios-checkmark" style="font-size: 20px;color: #ff5b5b" v-show="obj.active"> </Icon>\
                            </span>\
                            <div class="img-box">\
                                <img :src="obj.src">\
                            </div>\
                            <div class="pay-introduce">\
                                <div>{{obj.title}}{{ currency < real_price  && obj.type == 3 ? \'(余额不够本次支付 剩余\'+currency+\'元 )\' : \'\'}}</div>\
                                <div>{{obj.introduce}}</div>\
                            </div>\
                        </li>\
                        <submit-loading-item :show="ajaxing" :text="\'正在提交订单\'"></submit-loading-item>\
                    </ul>\
                </div>',
    props: ['support_type', 'currency', 'real_price'],
    data: function(){
        var all_pay_object= {
                        'ali': {
                            'type': 1,
                            'title': '支付宝支付',
                            'active': true,
                            'introduce': '支持信用卡、储蓄卡快捷支付及支付宝',
                            'src': '/static/public_img/order/paybyali.png',
                        },
                        'wx': {
                            'type': 2,
                            'title': '微信支付',
                            'active': false,
                            'introduce': '支持信用卡、储蓄卡快捷支付及支付宝',
                            'src': '/static/public_img/order/paybywx.png',
                        },
                        'mhb': {
                            'type': 3,
                            'title': '盒币支付',
                            'active': false,
                            'introduce': '方便、快捷、充值优惠多多',
                            'src': '/static/public_img/order/mhb.gif',
                        }
                    }
        var pay_object = {};
        for(var i=0; i < this.support_type.length;i++){
            var type = this.support_type[i];
            pay_object[type] = all_pay_object[type]
        }
        return {
            pay_object: pay_object,
            ajaxing: false,
            token: {},

    }},
    methods: {
        pay_type_select: function(type){
            if(type == 3 && this.skip_mhb) return false;
            for(var key in this.pay_object){
                this.pay_object[key].active = this.pay_object[key].type == type;
            }
        },
        submit: function(url, params){
            if(this.active_obj.type == 3){
                window.location.href = '/order/currency_pay_page/{0}?coupon_id={1}'.format(params.order_id, params.coupon_id)
                return false;
            }
            this.$nextTick(function(){
                var pay_type = this.active_obj.type;
                var that = this;
                normal_ajax(url + pay_type, 'GET', params,
                    function(){that.ajaxing=true},
                    function(ret){
                        if(ret.retcode === 'SUCC'){
                            that.token = ret.token;
                            that.$nextTick(function(){
                                this.$refs.form.submit();
                            })
                        }else{
                            that.$Message.warning(ret.description);
                        }
                    },
                    null,
                    function(){that.ajaxing=false}
                )
            })
            // else 
        }

    },
    computed: {
        active_obj: function() {
            for(var k in this.pay_object){
                if(this.pay_object[k].active){
                    return {
                        'type': this.pay_object[k].type,
                    }
                }
            }
        },
        skip_mhb: function(){
            return this.currency < this.real_price;
        }
    }
}

// 短信组件
var captcha = {
    template: '<div class="captcha" @click.stop="send_captcha" ref="captcha"> {{text}} </div>',
    props: ['type', 'username', 'checkcode', 'token'], // type发送的类型  username发送的手机号（没有为登陆用户的手机号码） checkcode 可无
    data: function(){
        return {
            captcha_active: false,
            text: '获取验证码',

        }
    },
    mounted:function(){
    },
    methods: {
        send_captcha: function(){
            // 需要判断checkcode
            if(this.username != undefined || this.checkcode != undefined){
                if(!this.username || !checkMobile(this.username)){
                    this.$Message.warning('请输入正确的手机号');
                    this.$root.username_error = true;
                    return false;
                }
                if(this.checkcode.length < 4){
                    this.$Message.warning('请填写正确的验证码！');
                    this.$root.checkcode_error = true;
                    return false;
                }
            }
            if(this.captcha_active) return false;
            var that = this;
            normal_ajax('/user/send_captcha?type=' + that.type, 'GET', {'checkcode': that.checkcode, 'token': that.token, 'username': this.username},  function(){
                    that.captcha_active = true;
                },
                function(data){
                    if(data.retcode === 'SUCC'){
                        if(superuser){
                            that.$root.captcha = data.captcha;
                        }
                        that.send_captcha_active();
                    }else if(data.msg == 'ErrorCheckCode'){
                        that.$root.checkcode_img()
                        that.$root.checkcode = '';
                        that.$Message.warning('验证码错误！');
                    }else if(data.msg == 'TokenExpired'){
                        that.$Message.warning('token已经过期！');
                        setTimeout(function(){location.reload(true)}, 500)
                    }else if(data.msg == 'HasSend'){
                        that.$Message.warning('请勿重复发送！');
                        if(that.$root.checkcode_img != undefined){
                            that.$root.checkcode_img()
                        }
                        that.send_captcha_active();
                        that.captcha_active = true;
                    }else if(data.msg == 'IpSmsMaxed'){
                        that.$Message.warning('已检测到该ip发送短信受限，24小时内无法发送短信！');
                    }else if(data.msg == 'HasRegistered'){
                        that.$Message.warning('该手机号已被注册！');
                    }else{
                        that.$Message.warning(data.description);
                    }
                }, null, function(){that.captcha_active = false;}
            )
        },
        // 短信动画
        send_captcha_active: function(){
            this.captcha_active = true;
            var that = this;
            that.text = 60;
            var _ = setInterval(function(){
                if(that.text != 1){
                    that.captcha_active = true;
                    that.text --;
                }else{
                    that.text = '获取验证码';
                    clearInterval(_);
                    that.captcha_active = false;
                }
             }, 1000)

        },
    },
}


var page_notic = {
    template: '\
    <div class="friendly-notic">\
        <div class="header">\
            <Icon type="arrow-right-b" style="color:#00b9ff"></Icon>\
            <span style="font-weight: bold;">{{title}}</span>\
        </div>\
        <div class="content">\
            <slot></slot>\
        </div>\
    </div>\
    ',
    props: ['title']
}

var order_options = {
    template: 
        '<div style="background-color: #fff;border-top: 1px solid #e5e5e5;padding: 10px 0;text-align: right;">'+
            '<span class="cbg-button" v-if="[\'待付款\', \'已完成\'].indexOf(order.status) != -1" @click.stop.prevent="del_order">删除</span>'+
            '<a :href="\'/order/pay_page/\' + order.id" v-if="[\'待付款\'].indexOf(order.status) != -1"><span class="cbg-button">支付</span></a>'+
            '<a  :href=" order.modify_times <=0 ? \'javascript:void(0);\' : \'/service/service_modify/\' + order.id" v-if="[\'待付款\', \'进行中\'].indexOf(order.status) != -1"><span class="cbg-button" :class="{disable: order.modify_times <=0}">修改参数({{order.modify_times}})</span></a>'+

            '<a :href="\'/order/crawl_data_page/\' + order.id"  v-if="[\'已完成\', \'进行中\'].indexOf(order.status) != -1"><span class="cbg-button">查看通知</span></a>'+
        '</div>',
    props: ['order',  'order_id_str', 'call_back'],
    methods: {
        del_order: function(){
            // 删除订单
            var that = this;
            this.$root.simple_modal_title = '您确定要删除该订单吗';
            this.$root.simple_modal_init('您确定要删除该订单吗', function(){
                that.call_back(that.order.id);
            })
            return false;
        },
    },
}

var swiper = {
    template: '\
        <div>\
            <div class="swiper-container" :class="swiper_key" v-if="banner_list.length > 1">\
                <div class="swiper-wrapper">\
                    <div class="swiper-slide" v-for="banner in banner_list" :key="banner.id">\
                        <a :href="banner.href">\
                            <img :src="banner.img_url">\
                        </a>\
                    </div>\
                </div>\
                <div class="swiper-pagination" :class="page_class"></div>\
            </div>\
            <div v-if="banner_list.length==1">\
                <a :href="banner_list[0].href"><img :src="banner_list[0].img_url" style="width: 100%" /></a>\
            </div>\
        </div>\
    ',
    data: function(){
        return {
            page_class: 'pagination' + this.swiper_key,
        }
    },
    mounted: function(){
        var that = this;
        new Swiper ('.' + that.swiper_key, {
            loop: true,
            autoplay: {
                disableOnInteraction: false,
                delay: 2000,
            },
            // 如果需要分页器
            pagination: {
              el: that.page_class,
              clickable :true,
            },
            // on: {
            //     slideChangeTransitionEnd: function(){
            //         alert(this.activeIndex);//切换结束时，告诉我现在是第几个slide
            //     }
            // },
        })
    },
    props: ['swiper_key', 'banner_list'],
}

//     v-for="todo in todos"
//     v-bind:key="todo.id"
//   >
//     <!-- 我们为每个 todo 提供一个 slot 元素， -->
//     <!-- 然后，将 `todo` 对象作为 slot 元素的一个 prop 传入。 -->
//     <slot v-bind:todo="todo">
//       <!-- 这里是回退内容(fallback content) -->
//       {{ todo.text }}
//     </slot>
//   </li>
// </ul>
// 现在，在我们引用 <todo-list> 组件的位置，我们可以将 todo items 插槽内容稍作修改，定义为一个 <template>，并且通过 slot-scope 特性访问子组件数据：

// <todo-list v-bind:todos="todos">
//   <!-- 将 `slotProps` 作为插槽内容所在作用域(slot scope)的引用名称 -->
//   <template slot-scope="slotProps">
//     <!-- 为 todo items 定义一个模板， -->
//     <!-- 通过 `slotProps` 访问每个 todo 对象。 -->
//     <span v-if="slotProps.todo.isComplete">✓</span>
//     {{ slotProps.todo.text }}
//   </template>
// </todo-list>
var fullscreen = {
    // 显示有根节点控制， 隐藏由子节点控制
        template: '<div class="fullscreen-box" @click.stop="handleClick" v-show="show">\
                       <slot name="fullscreen_item"></slot>\
                   </div>',
        props: ['_click_hide', 'init_show'],
        data: function(){
            return {
                click_hide: this._click_hide === undefined ? true : !!this._click_hide,
                show: !!this.init_show,
            }
        },
        methods: {
            handleClick: function(){
                if(this.click_hide){
                    this.show = false;
                }
            },
        },
        watch:{
        },

    };

var submit_loading = {
    template: '<full-screen :_click_hide="false" ref="fullscreen">\
        <div slot="fullscreen_item">\
            <div style="position: absolute;top: 30%;left:50%;transform: translate(-50%, -50%);width: 100%;">\
                <img src="/static/public_img/submit_loading.gif" style="width: 20%;position: relative;left: 50%;transform: translate(-50%);">\
                <div style="text-align: center;font-size: 18px;color:rgb(111,81,68);margin-top:10px;">((text_))((suffix_text_))</div>\
            </div>\
        </div>\
    </full-screen>',
    props: ['show', 'text', 'suffix'],
    delimiters : ["((", "))"],
    data: function(){
        return {
            set_interval : null,
            text_ : this.text ? this.text : '正在提交',
            suffix_: this.suffix == undefined ? true : !!this.suffix,
            suffix_text_: "",
        }
    },
    methods: {
    },
    watch: {
        'show': function(nv){
            this.$refs.fullscreen.show = nv;
            var that =this;
            if(this.suffix_ && nv){
                this.set_interval = setInterval(function(){
                    if(that.suffix_text_.length<3){
                        that.suffix_text_ += '。';
                    }else{
                        that.suffix_text_ = '';
                    }
                }, 500)
            }
            if(this.suffix_ && !nv){
                clearInterval(this.set_interval);
            }
        }
        
    }
}
    
var simple_choice = {
    template: '\
        <full-screen ref="fullscreen">\
            <ul class="simple-list-box" slot="fullscreen_item" style="position: absolute;" :style="top===true?simple_top:simple_bottom" ref="simple">\
                <li class="title" v-if="!!title">((title))</li>\
                <li class="border-full" v-for="choose in choice_list" :class="{\'choose-enclickable\': choose.disable === false}" @click.stop="choice(choose)">((choose.text))\
                </li>\
            </ul>\
        </full-screen>\
    ',
    delimiters : ["((", "))"],
    props: ['title', 'choice_list', 'callback', 'top'],
    data: function(){
        return {
            is_simple_choice: true,
            simple_top: {top: 0},
            simple_bottom: {bottom: 0},
            simple_animation_init: {
                transition: 'all 1s',
            }
        }
    },
    methods:{
        show: function(){
            // 当要展示的时候需要关闭所有的simple-choice组件
            if(!this.$refs.fullscreen.show){
                 refs = this.$root.$refs;
                var refs_keys = Object.keys(refs);
                for(var i=0;i<refs_keys.length;i++){
                    var key = refs_keys[i];
                    if(refs[key].is_simple_choice){
                        refs[key].$refs.fullscreen.show = false;

                    }
                }
            }
       
            this.$nextTick(function(){
                this.$refs.fullscreen.show = !this.$refs.fullscreen.show;
            })
        },
        choice: function(choose){
            if(choose.disable === false) return false;
            this.$refs.fullscreen.show = false;
            this.callback(choose.text, choose.extra, choose);
        },
    },
}
var edit_div = {
    template: '\
        <div contenteditable="true" v-html="value" @input="changeText">\
        </div>',

    props: ['value'],
    methods:{
        changeText: function(){
            this.innerText = this.$el.innerHTML;
            this.$emit('input', this.innerText);
        },
    },
}
var coupon = {
    template: '\
    <div class="coupon-box" :class="\'type-\'+type">\
        <div class="coupon-inner-box">\
            <div class="coupon-left-view">\
                <p class="coupon-left-view-price">\
                    <span v-if="info_.discount">\
                        <strong>{{info_.discount/10}}</strong>\
                        <small>折</small>\
                    </span>\
                    <span v-if="info_.reduction">\
                        <small>￥</small>\
                        <strong>{{info_.reduction/100}}</strong>\
                    </span>\
                </p>\
                <p class="coupon-left-view-rule">满{{info_.fill/100}}元可用</p>\
            </div>\
            <div class="coupon-righ-view">\
                <p class="coupon-righ-view-limit">\
                    {{info_.service_range}}可用<span v-if="cp_list && my_cp_list.indexOf(info_.id) == -1">({{info_.total_limit === 0 ? \'不限量\' : (\'限发\'+info_.total_limit+\'个\')}})</span>\
                </p>\
                <p class="coupon-right-view-date">\
                    {{info_.acquire_start_time}} - {{info_.acquire_end_time}}\
                </p>\
                <a class="coupon-user-now" v-if="info_.current_use" :href="\'/coupon/use_coupon_redirect/\' + info_.coupon_id">立刻使用</a>\
                <div style="width: 40%;border-left: 1px dashed #d7c8c8;height: 100%;position: absolute;right: 0;top: 0" v-if="percent_show">\
                    <i-circle :percent="info_.total_limit!=0 ? (info_.acquire_count/info_.total_limit)*100 : 0 " style="width:60%;top:0px;left: 50%;transform: translate(-50%);max-width: 60px" stroke-color="rgb(250,48,42)">\
                        <span style="font-size:12px;color:rgb(250,48,42);"  class="absolute_center">\
                            已抢\
                            <div style="margin-top:5px;">\
                            {{info_.acquire_count}}\
                            </div>\
                        </span>\
                    </i-circle>\
                    <div style="position: absolute;left: 50%;transform: translate(-50%);bottom: 0;width: 85%;\
                    max-width:77px;text-align: center;height: 20px;background-color: rgb(250,48,42);border-radius:10px;line-height: 20px;color:#fff" v-if="my_cp_list.indexOf(info_.id) === -1" @click.stop="get_coupon">\
                        <span v-show="!ajaxing">\
                            <span v-if="info_.acquire_count/info_.total_limit < 1 || info_.total_limit == 0">立刻领取</span>\
                            <span v-if="info_.acquire_count/info_.total_limit == 1 && info_.total_limit !=0 ">已抢完</span>\
                        </span>\
                        <span v-show="ajaxing">\
                            正在领取\
                        </span>\
                    </div>\
                    <div style="position: absolute;left: 50%;transform: translate(-50%);bottom: 0;width: 85%;\
                    max-width:77px;text-align: center;height: 20px;background-color: rgb(181,136,135);border-radius:10px;line-height: 20px;color:#fff" v-if="my_cp_list.indexOf(info_.id) != -1">\
                        已拥有\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>\
    ',
    props: ['info', 'type', 'percent_show', 'cp_list'],   // tupe: 风格 discount:打折 reduction:直减  full: 满多少能够使用 use_range: 使用范围
    data: function(){
        return {
            my_cp_list: this.cp_list || [],
            info_: this.info,
            ajaxing: false,
        }
    },
    methods: {
        get_coupon: function(){
            if(this.info_.acquire_count/this.info_.total_limit>=1 && this.info_.total_limit != 0) return false;
            if(this.ajaxing) return false;
            var that = this;
            normal_ajax('/coupon/get_coupon_api/'+that.info_.id, 'GET', null, function(){
                    that.ajaxing = true;
                },function(ret){
                    if(ret.retcode==='SUCC'){
                        that.my_cp_list.push(that.info.id)
                        that.info_.acquire_count += 1;
                    }else{
                        that.$Message.warning(ret.description);
                    }

                },null,function(){
                    that.ajaxing = false;

            })
        },

    },
}
var order_ul = {
    template: '\
        <div>\
            <div class="order-box">\
                <img :src=" service_obj[order.service_id].show_img ">\
                <div class="order-detail-box">\
                    <div>(( service_obj[order.service_id].name ))</div>\
                    <div style="color: #999">((server_options.service_time))天(有效期)</div>\
                    <div class="service">在线服务</div>\
                    <div style="font-size: 14px">￥(( (order.price / 100).toFixed(2) ))<span style="font-size: 12px"></span></div>\
                </div>\
            </div>\
            <ul class="order-service-box fff-bg" :style="operate_sytle">\
                <li>\
                    <span>已有数据通知</span>\
                    <span>((server_options.first_round_push ? \'是\' : \'否\'))</span>\
                </li>\
                <li>\
                    <span>降价提醒</span>\
                    <span>(( server_options.price_down_push ? \'是\' : \'否\'))</span>\
                </li>\
                <li>\
                    <span>提醒方式</span>\
                    <span>(( server_options.push_type ? server_options.push_type : \'无\' ))</span>\
                </li>\
                <!-- <li>\
                    <span>积分抵扣</span> \
                    <span>￥0.00 </span> \
                </li>-->\
                <li style="position: relative;" @click.stop="show_my_coupon" v-if="operate">\
                    <span>优惠券抵扣</span>\
                    <span>((coupon.text)): ￥(( (coupon.reduction / 100).toFixed(2) )) <Icon type="chevron-right" style="position: absolute;right: -17px;top:3px"></Icon></span>\
                </li>\
                <div v-if="!operate && reduction_log">\
                    <li v-for="log in reduction_log">\
                        <span>(( log.alias ))</span> \
                        <span> -(( (log.reduction / 100).toFixed(2) )) </span> \
                    </li>\
                </div>\
                <li style="position: relative;"  v-if="!operate">\
                    <span style="color:#fe555c">实付</span>\
                    <span>(( (order.real_price/100).toFixed(2) ))</span>\
                </li>\
            </ul>\
            <submit-loading-item :show="ajaxing" :text="ajaxing_txt"></submit-loading-item>\
            <div v-if="operate && coupon_list.length > 1">\
                <simple-choice-item :title="\'我的优惠券\'" :choice_list="coupon_list" ref="choice" :callback="choose_coupon"></simple-choice-item >\
            </div>\
        </div>\
        ',
    props: ['order_', 'server_options_', 'coupon_list_', 'operate', 'reduction_log'],
    delimiters : ["((", "))"],
    data: function(){
        var server_options = {'push_type': this.server_options_[0], 'service_time': this.server_options_[1], 'first_round_push': this.server_options_[2], 'price_down_push': this.server_options_[3], 'memo': this.server_options_[4]};
        // 组装choiselist
        var coupon_list = [];
        var none_coupon = {name: '不使用优惠券', text: '不使用优惠券', style: 1, reduction: 0, id:""};
        console.log(this.coupon_list_)
        if(!this.coupon_list_ || this.coupon_list_.length === 0){
            none_coupon.name = none_coupon.text = '无优惠券可用';
        }
        none_coupon.extra = none_coupon;

        coupon_list.push(none_coupon);

        var init_coupon = none_coupon;
        if(this.coupon_list_ && this.coupon_list_.length >= 1){
            for(var i=0;i<this.coupon_list_.length;i++){
                var coupon = this.coupon_list_[i];
                coupon.extra = coupon
                if(coupon.style === 2) coupon.reduction = (this.order_.price) * (1-coupon.discount/100);
                // 1. 判断是否足够条件
                coupon.text = coupon.coupon_name;
                if(coupon.fill > this.order_.price){
                    coupon.text +=  '(满{0}元可用)'.format(coupon.fill/100);
                    coupon.disable = false;
                }else{
                    // 计算折扣力度，设置初始选择的优惠券
                    if(!init_coupon.reduction || init_coupon.reduction < coupon.reduction){
                        init_coupon = coupon;
                    }
                }
                coupon_list.push(coupon);
            }
        }
        return {
            operate_sytle: this.operate ? "" : {'padding-right': '12px'},
            ajaxing: false,
            ajaxing_txt: "",
            order: this.order_,
            server_options: server_options,
            // 优惠券部分
            coupon: init_coupon,
            coupon_list: coupon_list,
        }
    },
    methods: {
        show_my_coupon: function(){
            if(this.coupon_list.length > 1){
                this.$refs.choice.show()
            }
        },
        choose_coupon: function(text, coupon){
            this.coupon = coupon;
        }
    }

}

// 七牛图片上传组件
var img_item = {
    template: '\
    <div>\
        <div v-for="img in img_list" class="img-box">\
            <div style="height: 100%;">\
                <Icon type="minus-circled" class="img-cancel" @click.native.stop="removeImg(img)" v-if="maxImageLength != 1"></Icon>\
                <img :src="img" style="height: 100%;width: 100%" @click="changeImg">\
            </div>\
        </div>\
        <div class="img-box" v-show="img_list.length < maxImageLength" id="container">\
            <div class="no-img">\
                <Icon type="image"></Icon>\
            </div>\
            <input type="file" class="file-input" id="pickfiles" ref="add_img">\
        </div>\
    </div>',
    props: ['domain', 'token', 'max_length', 'maxSize', 'supportCancel', 'imgs'],
    data: function(){
        return {
            img_list: [],
            maxImageLength: this.max_length || 1,
            maxImageSize: this.maxSize || 1204,
            format: ['jpg', 'png', 'gif'],
        }
    },
    mounted: function(){
        var qiniu_params ={
          // domain为七牛空间对应的域名，选择某个空间后，可通过 空间设置->基本设置->域名设置 查看获取
          // uploader为一个plupload对象，继承了所有plupload的方法
            runtimes: 'html5,flash,html4',      // 上传模式，依次退化
            browse_button: 'pickfiles',         // 上传选择的点选按钮，必需
            // 在初始化时，uptoken，uptoken_url，uptoken_func三个参数中必须有一个被设置
            // 切如果提供了多个，其优先级为uptoken > uptoken_url > uptoken_func
            // 其中uptoken是直接提供上传凭证，uptoken_url是提供了获取上传凭证的地址，如果需要定制获取uptoken的过程则可以设置uptoken_func
            uptoken : null,
            // uptoken_url: '/uptoken',         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
            // uptoken_func: function(){    // 在需要获取uptoken时，该方法会被调用
            //    // do something
            //    return uptoken;
            // },
            get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
            // downtoken_url: '/downtoken',
            // Ajax请求downToken的Url，私有空间时使用，JS-SDK将向该地址POST文件的key和domain，服务端返回的JSON必须包含url字段，url值为该文件的下载地址
            // unique_names: true,              // 默认false，key为文件名。若开启该选项，JS-SDK会为每个文件自动生成key（文件名）
            // save_key: true,                  // 默认false。若在服务端生成uptoken的上传策略中指定了sava_key，则开启，SDK在前端将不对key进行任何处理
            domain: null,     // bucket域名，下载资源时用到，必需
            container: 'container',             // 上传区域DOM ID，默认是browser_button的父元素
            max_file_size: '2mb',             // 最大文件体积限制
            flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入flash，相对路径
            max_retries: 3,                     // 上传失败最大重试次数
            // dragdrop: true,                     // 开启可拖曳上传
            // drop_element: 'input',          // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
            // chunk_size: '4mb',                  // 分块上传时，每块的体积
            auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
            //x_vars : {
            //    查看自定义变量
            //    'time' : function(up,file) {
            //        var time = (new Date()).getTime();
                    // do something with 'time'
            //        return time;
            //    },
            //    'size' : function(up,file) {
            //        var size = file.size;
                    // do something with 'size'
            //        return size;
            //    }
            //},
            filters : {
                max_file_size : '2mb',
                prevent_duplicates: true,
                //Specify what files to browse for
                 mime_types: [
                    {title : "Image files", extensions : "jpg,gif,png"}, //限定jpg,gif,png后缀上传
                ]
            },
            init: {
                'FilesAdded': function(up, files) {
                    plupload.each(files, function(file) {
                // 文件添加进队列后，处理相关的事情
                });
                },
                'BeforeUpload': function(up, file) {
                },
                'UploadProgress': function(up, file) {
                // 每个文件上传时，处理相关的事情
                },
                'Error': function(up, err, errTip) {
                    up.vue.$Message.warning(errTip);
                    // var progress = new FileProgress(err.file, 'fsUploadProgress');
                    //     progress.setError();
                    //     progress.setStatus(errTip);
                    //     return false;
                },
                'FileUploaded': function(up, file, info) {
                    up.vue.FileUploaded(up, file, info);
                },
                'UploadComplete': function() {
                //队列文件处理完毕后，处理相关的事情
                },
                'Key': function(up, file) {
                    // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
                    // 该配置必须要在unique_names: false，save_key: false时才生效
                    var date = new Date();
                    // year = date.getFullYear();
                    // month = date.getMoth();
                    // day = date.getDate();
                    hour = date.getHours();
                    minute = date.getMinutes();
                    seconds = date.getSeconds();
                    miseconds = date.getMilliseconds();
                    return '/bugs/img/{{request.user.id}}/{0}:{1}:{2}:{3}:{4}'.format(date.toLocaleDateString(), hour, minute, seconds, miseconds);
                }
            }
        }
        qiniu_params.uptoken = this.token;
        qiniu_params.domain = this.domain;
        var uploader = Qiniu.uploader(qiniu_params);
        uploader.vue = this;
        this.img_list = this.imgs || [];
    },
    methods: {
        removeImg: function(img){
            var index = this.img_list.indexOf(img);
            this.img_list.splice(index, 1);
        },
        FileUploaded: function(up, file, info) {
            if(this.max_length == 1){
                this.img_list = [];
            }
             this.img_list.push('http://{0}/'.format(this.domain)+ JSON.parse(info.response).key);
             // 每个文件上传成功后，处理相关的事情
             // 其中info.response是文件上传成功后，服务端返回的json，形式如：
             // {
             //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
             //    "key": "gogopher.jpg"
             //  }
             // 查看简单反馈
             // var domain = up.getOption('domain');
             // var res = parseJSON(info.response);
             // var sourceLink = domain +"/"+ res.key; 获取上传成功后的文件的Url
        },
        checkMaxSize:function(file) {
            if(this.maxImageSize && file.size > 1024 * this.maxImageSize){
                this.$Message.warning('图片太大！');
                return true;
            }
        },
        changeImg: function(){
            if(this.max_length > 1)
                return false;
            this.$refs.add_img.click();
        },
        getImgList: function(){
            return this.img_list;
        }
    },
}
Vue.component('img-item', img_item);
Vue.component('coupon-item', coupon);
Vue.component('edit-div', edit_div);
Vue.component('fullScreen', fullscreen);
Vue.component('simple-choice-item', simple_choice);
Vue.component('form-item', form);
Vue.component('tabs-item', tabs_conmonent);
Vue.component('pay-channel', pay_channel);
Vue.component('scroll-item' , Scroll);
Vue.component('captcha-item', captcha);
Vue.component('page-notic-item', page_notic);
Vue.component('order-options-item', order_options);
Vue.component('swiper-item', swiper);
Vue.component('submit-loading-item', submit_loading);
Vue.component('order-ul-item', order_ul);
