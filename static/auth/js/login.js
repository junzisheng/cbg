var v;
jQuery(document).ready(function() {
	v = new Vue({
		el: '#body',
        delimiters : ["((", "))"],
		data: function(){
            return {
    			username: '',
    			pwd: '',
    			username_error: false,
    	        pwd_error: false,
    	        is_click: false,
    	        single: true,
            };
		},
		methods: {
            checkcode_img: function(){
                this.checkcode_src = '/user/checkcode_img/?r=' + Math.random();
            },
            submit: function(event){
                if(this.is_click) return false;
                if(!this.username){
                    this.$Message.warning('请输入账号！');
                    this.username_error = true;
                    return false;
                }
                if(this.username.indexOf(' ') != -1){
                    this.$Message.warning('账号不能包含空格！');
                    this.username_error = true;
                    return false;
                }
                if(this.username.length<6 || this.username.length > 12){
                    this.username_error = true;
                    this.$Message.warning('账号需要在6-12位之间！');
                    return false;
                }
                if(this.pwd.length < 6 || this.pwd.length > 16){
                    this.pwd_error = true;
                    this.$Message.warning('密码需要在6-16位之间！');
                    return false;
                }
                var that = this;
                var _data = {'username': this.username, 'pwd': this.pwd, 'auto_login': this.single};
                normal_ajax('/user/userlogin/', 'POST', _data, 
                    function(){
                        that.is_click = true;
                    },
                    function(data){ // success
                        if(data.retcode == 'SUCC'){  
                            that.is_click = false;
                            // is_login 表示是登陆进来的， 
                            var _redirect = redirect.indexOf('?') ? redirect + '&is_login=1' : redirect + '?is_login=1';
                            location.href = _redirect;
                        }else{
                            that.$Message.warning(data.description);
                        }
                    },
                    function(){
                            that.$Message.warning('发生错误，上传失败！');
                    },
                    function(){
                        that.is_click = false;
                    }
                )

            },
            input_focus: function(event){
                this.username_error = false;this.pwd_error = false; this.checkcode_error = false;//this.nickname_error = false;
            },
        }
	})



})