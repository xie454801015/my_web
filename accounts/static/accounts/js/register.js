$(document).ready(function(){
    var $username=add_mark($('#id_username'),'key_pass',false);
    var $email=add_mark($('#id_email'),'key_pass',false);
    var $password1=add_mark($('#id_password1'),'key_pass',false);
    var $password2=add_mark($('#id_password2'),'key_pass',false);
    var $verify_code=add_mark($('#id_verify_code'),'key_pass',false);
    var $submit_button=$('.button_box #sub_button');
    var $input_array=[$username,$password1,$password2,$email,$verify_code];
    enter_cut($input_array,$submit_button);
    // 验证码刷新,反复点击会让后台
    $('#refresh_code').click(function () {
        var $img_code=$('#verify_code');
        $img_code.attr("src",$img_code.attr("src")+'?');
        $verify_code.val("");
        $verify_code.focus();
    });

    // 用户名校验事件绑定
    $username.focus(function () {
        change_css($username,'6~18个字符，可使用字母、数字、下划线，需以字母开头,区分大小写!','#000');
    });

    $username.blur(function () {
        username_check($username);
    });

    // 电子邮箱校验事件绑定
    $email.focus(function () {
        change_css($email,'请输入您的邮箱地址!','#000');
    });

    $email.blur(function () {
        email_check($email);
    });

    // 密码规范性校验事件绑定
    $password1.focus(function () {
        change_css($password1,'6~16个字符，区分大小写!','#000');
    });

    $password1.blur(function () {
        password_check($password1);
    });

    $password2.focus(function () {
        change_css($password2,'请再次输入密码!','#000');
    });
    $password2.blur(function(){
        password2_check($password2,$password1);
    });

    // 验证码校验事件绑定
    $verify_code.focus(function () {
        change_css($verify_code,'请根据右图输入验证码!','#000');
    });

    $verify_code.blur(function () {
        verify_check($verify_code);
    });

    // 1、数据提交设计到二次校验的异步，无法很好解决等待数据完全验证导致未能及时阻止提交，只能将这轮ajax验证async改为false
    $submit_button.click(function () {
        var form_array = $('form#register').serializeArray();
        var form_json = {};
        for (var i = 0; i < form_array.length; i++) {
            form_json[form_array[i].name] = form_array[i].value
        }
        $.post('',form_json,function (data,status) {
            if (status =='success'){
                if (data.jump_url){
                    location.href=data.jump_url
                }
            }
            else{
                username_check($username,);
                email_check($email);
                password_check($password1);
                password2_check($password2);
                verify_check($verify_code);
            }
        })
    });
    // 切换input，最后一个聚焦提交
});

// 用户名校验
function username_check($elem,asy=true) {
    $elem.key_pass=false;
    var u_name = ($elem).val();
    if ((5<u_name.length) && (u_name.length<19) && (u_name!=null)){
        if (/^[a-zA-Z]/.test(u_name)) {
            if (/^[a-zA-Z][a-zA-Z0-9_]{5,17}$/.test(u_name)) {
                input_checkout($elem, 'check/', '用户名被占用！请重新输入！', '恭喜，该用户名可用！',asy);
            }
            else{ change_css($elem,'用户名必须以字母、数字或下划线组成!','#bc1717');}
        }
        else { change_css($elem,'用户名必须以字母开头','#bc1717');}
    }
    else{ change_css($elem,'用户名必须在6-18位之间!','#bc1717');}
}

// 邮箱地址校验
function email_check($elem,asy=true){
    $elem.key_pass=false;
    var u_email = $elem.val();
    if (/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/.test(u_email))
            {input_checkout($elem,'check/','邮箱地址被占用！请重新输入！','该邮箱地址可用！',asy);}
    else{ change_css($elem,'请输入正确的邮箱格式!','#bc1717');}
}

// 首次密码规范性校验
function password_check($elem){
    $elem.key_pass=false;
    var u_password1 = $elem.val();
    if (/^.{6,16}/.test(u_password1)){
        change_css($elem,'密码符合规范!','#00ff7f');
        $elem.key_pass=true;
    }
    else{
        change_css($elem,'密码长度为6-16字符，请重新输入!','#bc1717');
    }
}

// 二次输入密码比对
function password2_check($elem1,$elem2) {
    $elem1.key_pass=false;
    var $i_pw=$elem1.val();
    if (!$i_pw){ change_css($elem1,'请再次输入密码!','#bc1717');
    }
    else if ($i_pw || $elem2.val()){
        if ($i_pw != $elem2.val()){
             change_css($elem1,'两次密码输入不一致!','#bc1717');
        }
        else{change_css($elem1,'两次密码一致,请进行后续操作','#00ff7f');
        $elem1.key_pass=true;}
    }
}

// 验证码校验
function verify_check($elem){
    if($elem.val())
        {input_checkout($elem,'check/','验证码错误！请重新输入！','验证码输入正确！');}
    else{
        change_css($elem,'请输入验证码!',"#bc1717")
    }
}

// 校验后端异步交互传递，元素对象，url，默认为本级，存在提示文本，不存在提示文本，async值默认为true;
function input_checkout($elem,url1,text1,text2,async){
    var i_name= $elem.prop('name');
    var i_value = $elem.val();
    var $p_message = latest_elem($elem,'P');
    if (i_value){
        var i_data = {k1:i_name,k2:i_value};
        $.ajax({
             type: "get",
             async: async,
             url: url1,
             data: i_data,
             dataType: 'json',
             success: function (data) {
                 if (data.count) {
                     $p_message.text(text1);
                     $p_message.css({color: '#bc1717'});
                 }
                 else{$p_message.text(text2).css({color:'#00ff7f'});
                    $elem.key_pass=true}
             },
             error: function () {console.log('error');}
        })
    }
    else{
        $p_message.css({color:'#808080'})
    }
}



