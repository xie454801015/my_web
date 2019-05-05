$(document).ready(function(){
    var $submit_button=$('.button_box #sub_button');
    var $jump_button=$('.button_box #jump_button');
    var $verify_code=add_mark($('#id_verify_code'),'key_pass',false);
    var $elem_array=[$('#id_username'),$('#id_password'),$verify_code];
    var $img_code=$('#verify_code');
    var $p_message = $('#error_message');

    enter_cut($elem_array,$submit_button);
    add_focus($p_message,$elem_array,['请输入用户名！','请输入密码！','请输入验证码！'],'#000')
    // 验证码刷新,反复点击会让后台
    $('#refresh_code').click(function () {
       $img_code.attr("src",$img_code.attr("src")+'?');
       $verify_code.key_pass = false;
       $verify_code.val("");
       $verify_code.focus();
    });

    // 提交表单并接收反馈
    $submit_button.click(function () {
        if ($verify_code.key_pass &&
            (is_none($p_message,$elem_array,['请输入用户名!','请输入密码!','请输入验证码!']))) {
            console.log(1);
            var form_array = $('form#login').serializeArray();
            var form_json = {};
            for (var i = 0; i < form_array.length; i++) {
                form_json[form_array[i].name] = form_array[i].value;
            }
            $.post('', form_json, function (data, status) {
                if (status == 'success') {
                    if (data.jump_url) {
                        location.href = data.jump_url;
                    } else if (data.user_error) {
                        $p_message.text('用户名或密码不正确，请重新输入').css({color:'#bc1717'});
                    }
                }
        })
        }
        else{
            $p_message.css({color:'bc1717'})
        }
    });
    // 验证码校验
    $verify_code.blur(function () {
        var i_name= $verify_code.prop('name');
        var i_value = $verify_code.val();
        if (i_value){
            var i_data = {k1:i_name,k2:i_value};
            $.ajax({
                 type: "get",
                 async: true,
                 url: '/register/check',
                 data: i_data,
                 dataType: 'json',
                 success: function (data) {
                     // 后台返回count数字作为验证结果，重复或不匹配范围为非零数
                     if (data.count) {
                         $p_message.text('验证码错误！请重新输入');
                         $p_message.css({color: '#bc1717'});
                     }
                     else{$p_message.text('验证码正确!').css({color:'#00ff7f'});
                        $verify_code.key_pass=true;}
                 },
                 error: function () {console.log('error');}
            })
        }
        else{
            $p_message.text('请输入验证码').css({color:'#808080'});
        }
    });

    // 跳转到注册页面
    $jump_button.click(function () {
        location.href='/register/'
    });

});

// 数组中元素value的非空验证
function is_none($elem_p,$elem_array,text_array) {
    var p;
    for (p in $elem_array){
        var $elem = $elem_array[p];
        if (!(($elem).val())){
            $elem_p.text(text_array[p]).css({color:'#bc1717'});
            ($elem).focus();
            return false;
        }
    }
    return true;
}


// 聚焦信息提tips更改事件方法封装
function add_focus($tips_elem,$elem_array,text_array,color){
    $.each($elem_array,function (i) {
        if (i<$elem_array.length){
            $elem_array[i].focus(function () {
                $tips_elem.text(text_array[i]).css({color:color})
            })
        }
    })
}