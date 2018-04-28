

////////////////// 公用的方法 //////////////////////////////////////
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
function normal_ajax(url, method, _data, succ_callback , fail_callback , complete_callback , datatype , args_advance){

    var arg_ajax = {    url         : url,
                        type        : method || "GET",
                        data        : _data,
                        dataType    : datatype || "json",

                        complete    : function(XMLHttpRequest, textStatus){
                                        // textStatus的值：success,notmodified,nocontent,error,timeout,abort,parsererror

                                        if ($.isFunction(complete_callback))
                                            complete_callback(XMLHttpRequest, textStatus)
                                    } ,

                        success     : function(data, textStatus) {
                                        if ($.isFunction(succ_callback))
                                            succ_callback(data, textStatus)
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
    }
})


