//刷新验证码
function refresh_captcha(event) {
    $.get("/captcha/refresh/?" + Math.random(), function (result) {
        $('#' + event.data.form_id + ' .captcha').attr("src", result.image_url);
        $('#id_captcha_0').attr("value", result.key);
    });
    return false;
}

// 登陆和注册验证码
$('#login_form .captcha').click({'form_id': 'login_form'}, refresh_captcha);
$('#register_form .captcha').click({'form_id': 'register_form'}, refresh_captcha);


$('#up-top').hide();         //刚进入页面时设置为隐藏
$("#up-top").bind("click", function () {     //单击时返回顶部
    $('html, body').animate({scrollTop: 0}, 300);
    return false;
});
$(window).bind('scroll resize', function () {   //判断页面所在的位置，小于300就隐藏，否则就显示
    if ($(window).scrollTop() <= 300) {
        $("#up-top").hide();
    } else {
        $("#up-top").show();
    }
});


