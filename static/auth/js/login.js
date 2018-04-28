var v;
jQuery(document).ready(function() {
	v = new Vue({
		el: '#login-vue',
		data: {
			username: '',
			pwd: '',
			username_error: false,
	        pwd_error: false,
	        is_click: false,
	        checked: true,
		},
		methods: {
            checkcode_img: function(){
                this.checkcode_src = '/user/checkcode_img/?r=' + Math.random();
            },
            submit: function(event){
                if(!this.username){
                    $.top_notic('请输入账号！');
                    this.username_error = true;
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
                var that = this;
                this.is_click = true;
                var _data = {'username': this.username, 'pwd': this.pwd, 'auto_login': this.checked};
                normal_ajax('/user/userlogin/', 'POST', _data, 
                    function(data){ // success
                        if(data.retcode == 'SUCC'){  
                            that.is_click = false;
                            location.href = data.redirect;
                        }else{
                            $.top_notic(data.description);
                        }
                    },
                    function(){
                            $.top_notic('发生错误，上传失败！');
                    },
                    function(){
                        that.is_click = false;
                    },
                )

            },
            input_focus: function(event){
                this.username_error = false;this.pwd_error = false; this.checkcode_error = false;//this.nickname_error = false;
            }
        }
	})



})