

////////////////// 公用的方法 //////////////////////////////////////
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



function sns_convert_time(string_time , now){
    if (now == undefined)
        now = Date.now()

    //ts_this = Date.parse(string_time) ios上不支持-的时间转换
    var ts_this = Date.parse(string_time.replace(/-/g,"/"));
    var now_delta = now - ts_this;

    if (now_delta < -3600000 * 24 * 3) {
        return '刚刚';
    }
    else if (now_delta > 3600000 * 24 * 3) {
        var dt_this = new Date(ts_this);
        var dt_now  = new Date();

        var dt_ret  = dt_now.getFullYear() != dt_this.getFullYear() ? dt_this.getFullYear() + '-' : '';
        return dt_ret + fmt_integer_low100((dt_this.getMonth() + 1)) + '-' + fmt_integer_low100(dt_this.getDate()) + ' ' + fmt_integer_low100(dt_this.getHours()) + ':' + fmt_integer_low100(dt_this.getMinutes());
    }
    else if (now_delta > 3600000 * 24) {
        return Math.floor(now_delta / 3600000 / 24) + '天前';
    }
    else if (now_delta > 3600000) {
        return Math.floor(now_delta / 3600000) + '小时前';
    }
    else if (now_delta > 60000) {
        return Math.floor(now_delta / 60000) + '分钟前';
    }

    return '刚刚';
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
            return;
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
        return {
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
                case '提交问题':
                    location.href = '/others/bug_submit_page';
            }
        }
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
                        obj.query_list = that.query_list_handle(obj.query_list.concat(ret.query_list));
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
    template: '<div>\
                    <ul class="tabs-container">\
                        <li v-for="(v,k, index) in tabs_object" :class="{\'tabs-active\': v.active}" :style="{\'width\': li_width}" @click.stop="tab_click(k)">{{v.title}}</li>\
                    </ul>\
                    <ul class="panel-contanier">\
                        <li v-for="(v,k, index) in tabs_object" :index="index" v-show="v.active">\
                        <slot :name="\'panel-\' + index"></slot>\
                        </li>\
                        <slot :name=" \'bottom_loading\' "></slot>\
                    </ul>\
                </div>\
             ',
    data: function(){
        return {
            tabs_object: this.tab_object,
            li_width: 100/Object.keys(this.tab_object).length + '%',
        }
    },
    props : ['tab_object'],
    methods: {
        tab_click: function(key){
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
                            <input name="order_id" type="text" :value="((_goods_obj.orderid))">\
                            <input type="hidden" name="csrfmiddlewaretoken" :value="((csrf_token))">\
                        </form-item>\
                        <form-item style="display:none" id="pay_form" method="post" :action="\'https://pay.bbbapi.com/\'" ref="form">\
                            <input name="goodsname" type="text" :value="((_goods_obj.goodsname))">\
                            <input name="uid" type="text" :value="((_goods_obj.uid))">\
                            <input name="price" type="text" :value="((_goods_obj.price))">\
                            <input name="istype" type="text" :value="((active_obj.type))">\
                            <input name="notify_url" type="text" :value="((_goods_obj.notify_url)).slice(0, -1) + ((active_obj.type))">\
                            <input name="return_url" type="text" :value="((_goods_obj.return_url))">\
                            <input name="orderid" type="text" :value="((_goods_obj.orderid))">\
                            <input name="orderuid" type="text" :value="((_goods_obj.orderuid))">\
                            <input name="key" type="text" :value="(( that.signature_obj[active_obj.type] ))">\
                            <input type="submit" >\
                        </form-item>\
                        <li v-for="(obj, k) in pay_object" @click.stop="pay_type_select(obj.type)" :style="{\'opacity\': currency < _goods_obj.price && obj.type == 3 ? 0.4 : 1}">\
                            <span>\
                                <Icon type="ios-circle-outline" style="font-size: 20px;" v-show="!obj.active" @click.native="pay_type_select(obj.type)"></Icon>\
                                <Icon type="ios-checkmark" style="font-size: 20px;color: #ff5b5b" v-show="obj.active"> </Icon>\
                            </span>\
                            <div class="img-box">\
                                <img :src="obj.src">\
                            </div>\
                            <div class="pay-introduce">\
                                <div>{{obj.title}}{{ currency < _goods_obj.price  && obj.type == 3 ? \'(余额不够本次支付 剩余\'+currency+\'元 )\' : \'\'}}</div>\
                                <div>{{obj.introduce}}</div>\
                            </div>\
                        </li>\
                    </ul>\
                </div>',
    props: ['that', '_goods_obj', '_signature_obj', 'support_type', 'currency'],
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
        var skip_mhb = this.currency < this._goods_obj.price
        for(var i=0; i < this.support_type.length;i++){
            var type = this.support_type[i];
            pay_object[type] = all_pay_object[type]
        }
        return {
            pay_object: pay_object,
            skip_mhb: skip_mhb,

    }},
    methods: {
        pay_type_select: function(type){
            if(type == 3 && this.skip_mhb) return false;
            for(var key in this.pay_object){
                this.pay_object[key].active = this.pay_object[key].type == type;
            }
        },
        submit: function(){
            if(this.active_obj.type == 3) this.$refs.form2.submit()
            else this.$refs.form.submit();
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
                        if(that.$root.checkcode_img != undefined && typeof that.$root.checkcode_img == 'function'){
                            that.$root.checkcode_img()
                            that.send_captcha_active();
                        }
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
    template: ' \
        <div style="background-color: #fff;border-top: 1px solid #e5e5e5;padding: 10px 0;text-align: right;">\
            <span class="cbg-button" v-if="[\'待付款\', \'已完成\'].indexOf(order.status) != -1" @click.stop.prevent="del_order">删除</span>\
            <a :href="\'/order/pay_page/\' + order.id" v-if="[\'待付款\'].indexOf(order.status) != -1"><span class="cbg-button">支付</span></a>\
            <a :href="\'/service/service_page/召唤兽?params=\' + order.upload_params" v-if="[\'待付款\', \'进行中\'].indexOf(order.status) != -1"><span class="cbg-button">修改参数</span></a>\
            <a :href="\'/order/crawl_data_page/\' + order.id"  v-if="[\'已完成\', \'进行中\'].indexOf(order.status) != -1"><span class="cbg-button">查看通知</span></a>\
        </div>',
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
        props: ['_click_hide'],
        data: function(){
            return {
                click_hide: this.click_hide === undefined ? true : !!click_hide,
                show: false,
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
    
var simple_choice = {
    template: '\
        <full-screen ref="fullscreen">\
            <ul class="simple-list-box" slot="fullscreen_item" style="position: absolute;" :style="top===true?simple_top:simple_bottom" ref="simple">\
                <li class="title">((title))</li>\
                <li class="border-full" v-for="choose in choice_list" :class="{\'choose-enclickable\': choose.disable === false}" @click.stop="choice(choose)">((choose.text))\
                </li>\
            </ul>\
        </full-screen>\
    ',
    delimiters : ["((", "))"],
    props: ['title', 'choice_list', 'callback', 'top'],
    data: function(){
        return {
            simple_top: {top: 0},
            simple_bottom: {bottom: 0},
            simple_animation_init: {
                transition: 'all 1s',
            }
        }
    },
    methods:{
        show: function(){
            var that = this;
            this.$refs.fullscreen.show = true;
            this.$nextTick(function(){
                console.log(this.$refs.fullscreen.$el.offsetTop, this.$refs.simple.offsetHeight);
            })
        },
        choice: function(choose){
            if(choose.disable === false) return false;
            this.$refs.fullscreen.show = false;
            this.callback(choose.text, choose.extra);
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