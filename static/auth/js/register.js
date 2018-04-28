var a;
jQuery(document).ready(function() {
    // vue.component('input-item', {
    //     template: '\
    //         <input type="text" v-model="username" name="form-username" \
    //         maxlength="12" placeholder="请输入账号" :class="{'input-error': username_error}" \
    //         class="form-username form-control" id="form-username">\
    // })


     a = new Vue({
        el: '#register-vue',
        data: {
            nickname: '',
            username : '',
            pwd: '',
            checkcode: '',
            //nickname_error : '',
            checkcode_src: '/user/checkcode_img/',
            username_error: false,
            pwd_error: false,
            checkcode_error: false,
            is_click: false,
        },
        methods: {
            checkcode_img: function(){
                this.checkcode_src = '/user/checkcode_img/?r=' + Math.random();
            },
            submit: function(event){
                // if(this.is_click) return false;
                // if(!this.nickname){
                //     $.top_notic('请输入昵称');
                //     this.nickname_error= true;
                //     return false;
                // }
                if(this.nickname.indexOf(' ') != -1){
                    $.top_notic('昵称不能包含空格！');
                    this.nickname_error= true;
                    return false;
                }
                if(!this.username){
                    $.top_notic('请输入账号！');
                    this.username_error= true;
                    return false;
                }
                if(this.username.indexOf(' ') != -1){
                    $.top_notic('账号不能包含空格！');
                    this.username_error = true;
                    return false;
                }
                if(this.username.length<6 || this.username.length > 12){
                    this.username_error = true;
                    $.top_notic('账号需要在6-12位之间！');
                    return false;
                }
                if(this.pwd.length < 6 || this.pwd.length > 16){
                    this.pwd_error = true;
                    $.top_notic('密码需要在6-16位之间！');
                    return false;
                }
                if(this.checkcode.length == 0){
                    this.checkcode_error = true;
                    $.top_notic('请填写验证码！');
                    return false;
                }
                if(this.checkcode.length != 4){
                    this.checkcode_error = true;
                    this.checkcode_img();
                    $.top_notic('验证码错误');

                    return false;
                }
                var that = this;
                this.is_click = true;
                var _data = {'username': this.username, 'pwd': this.pwd, 'nickname': this.nickname, 'checkcode': this.checkcode};
                normal_ajax('/user/userreg/', 'POST', _data, 
                    function(data){ // success
                        if(data.retcode == 'SUCC'){  
                            that.is_click = false;
                            location.href = '/user/login'
                        }else{
                            that.checkcode_img();
                            $.top_notic(data.description);
                        }
                    },
                    function(){
                            $.top_notic('发生错误，上传失败！');
                    },
                    function(){
                        that.is_click = false;
                    }
                );

            },
            input_focus: function(event){
                this.username_error = false;this.pwd_error = false; this.checkcode_error = false;//this.nickname_error = false;
            }
        }

    })
	
});
