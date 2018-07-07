var v;
jQuery(document).ready(function() {
    // vue.component('input-item', {
    //     template: '\
    //         <input type="text" v-model="username" name="form-username" \
    //         maxlength="12" placeholder="请输入账号" :class="{'input-error': username_error}" \
    //         class="form-username form-control" id="form-username">\
    // })


     v = new Vue({
        el: '#body',
        delimiters : ["((", "))"],
        data: {
            nickname: '',
            username : '',
            pwd: '',
            checkcode: '',
            captcha: '',
            token: $('#token').val(),
            //nickname_error : '',
            checkcode_src: '/user/checkcode_img/',
            username_error: false,
            pwd_error: false,
            checkcode_error: false,
            is_click: false,
            captcha_error: false,

            captcha_active: false,
        },
        methods: {
            checkcode_img: function(){
                this.checkcode_src = '/user/checkcode_img/?r=' + Math.random();
            },
            submit: function(event){
                // if(this.nickname.indexOf(' ') != -1){
                //     this.$Message.warning('昵称不能包含空格！');
                //     this.nickname_error = true;
                //     return false;
                // }
                if(!this.username || !checkMobile(this.username)){
                    this.$Message.warning('请输入正确的手机号');
                    this.username_error= true;
                    return false;
                }
                if(this.pwd.length < 6 || this.pwd.length > 16){
                    this.$Message.warning('密码需要在6-16位之间！');
                    this.pwd_error = true;
                    return false;
                }
                if(this.captcha.length != 4){
                    this.$Message.warning('请输入4位验证码！');
                    this.captcha_error = true;
                    return false;
                }
                var that = this;
                var _data = {'username': this.username, 'pwd': this.pwd, 'nickname': this.nickname, 'captcha': this.captcha};
                normal_ajax('/user/userreg/', 'POST', _data, function(){
                        that.is_click = true;
                    },
                    function(data){ // success
                        if(data.retcode == 'SUCC'){  
                            that.$Message.loading({content:'注册成功', duration: 1, onClose:function(){
                                location.href = '/user/login'}
                            });
                        }else{
                            that.checkcode_img();
                            that.$Message.warning(data.description);
                        }
                    },
                    function(){
                        that.$Message.warning('发生错误，上传失败！')
                    },
                    function(){
                        that.is_click = false;
                    }
                );

            },
            input_focus: function(event){
                this.username_error = false;this.pwd_error = false; this.checkcode_error = false;//this.nickname_error = false;
                this.captcha_error = false;
            },
        }

    })

     // 发送验证码的动画
     setInterval(function(){
        $('.captcha-active').text(function(s, text){
            var text = text.trim();
            if(text == '获取验证码'){ 
                return 60
            }
            else if(text != '0'){
                 return text - 1;
            }
            else if(text == '0') {
                v.captcha_active = false;
                return '获取验证码';
            }
        })

     }, 1000)
	
});
