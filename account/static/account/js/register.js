/* 让一个对象上下震动 */
function shake(obj, cycle, n) {
    /*
     参数说明：
     1、obj要产生震动效果的对象
     2、震动效果的周期，单位是毫秒
     3、要震动的次数
     */
    /* 设置默认参数 */
    if (arguments.length < 2) {
        cycle = 30;
    }
    if (arguments.length < 3) {
        n = 30;
    }
    /* 循环上下移动对象形成震动效果 */
    for (i = 0; i < n; i++) {
        pos = Math.sin(Math.PI * i / 2) * 10;
        obj.animate({"margin-top": pos + "px"}, cycle);
    }
    /* 对象位置复位 */
    obj.animate({"margin-top": "0"}, cycle);
}

function showErrorMessage(message) {
    /* 如果提供了消息内容，填写到消息版中 */
    if (arguments.length != 0) {
        $('#errorMessage').html(message);
    }
    /* 如果消息版中有内容，将其显示出来并，震动消息框 */
    if ($('#errorMessage').html() != '') {
        errorMessageBox = $('#errorMessageBox')
        errorMessageBox.stop(true, true)
        errorMessageBox.show();
        errorMessageBox.css({'opacity': "1"});
        shake(errorMessageBox, 25, 30);
        errorMessageBox.animate({'opacity': 0}, 10 * 1000);
    }
}

function disableSendCheckCode(seconds) {
    /* 设置默认参数 */
    if (arguments.length == 0) {
        seconds = 60;
    }
    /* 将按钮设置为无效，并倒计时后将其恢复 */
    sendCheckCode = $('#sendCheckCode');
    if (sendCheckCode.attr('disabled') == undefined) {
        sendCheckCode.attr('disabled', true);
        i = seconds;
        /* 保存按钮原来的html内容 */
        buttonHtml = sendCheckCode.html();
        /* 启动一个定时器 */
        timer = setInterval(function () {
            if (i-- > 0) {
                sendCheckCode.html("" + i + "秒后可重发");
            } else {
                clearInterval(timer);
                sendCheckCode.html(buttonHtml);
                sendCheckCode.attr('disabled', false);
            }
        }, 1000);
    }
}

/* document ready 的加载动作 */
$(document).ready(function () {

    /* 定义发送验证码按钮事件 */
    $('#sendCheckCode').on('click', function () {
        /* 调用发送短信验证码的服务 */
        $.ajax({
            url: $('#sendCheckCode').data('service-url'),
            data: { phone: $('#registerForm #phone').val() },
            type: "post",
            dataType: "json",
            async: true,
            /* 通讯成功，解析返回结果做进一步处理 */
            success: function (result) {
                /* 返回结果是成功的,禁用按钮30秒 */
                if (result.errorCode == 0) {
                    disableSendCheckCode(180);
                } else {
                    /* 返回失败直接显示错误信息，如果是服务延时控制造成，按剩余秒数禁用发送按钮 */
                    if (result.secondsRemain != undefined) {
                        disableSendCheckCode(result.secondsRemain);
                    }
                    showErrorMessage(result.errorMessage);
                }
            },
            /* 失败说明网络有问题或者服务器有问题 */
            error: function (xhr, status, errorThrown) {
                showErrorMessage('网络连接不稳定，请稍后重试!');
            }
        });
    });

    /* 如果有错误提示信息将其显示出来 */
    showErrorMessage();
});