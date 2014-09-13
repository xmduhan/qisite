/* 让一个对象上下震动 */


function showErrorMessage(message) {
    // 如果提供了消息内容，填写到消息版中
    if (arguments.length != 0) {
        $('#errorMessage').html(message);
    }
    // 如果消息版中有内容，将其显示出来并，震动消息框
    if ($('#errorMessage').html() != '') {
        errorMessageBox = $('#errorMessageBox')
        errorMessageBox.stop(true, true)
        errorMessageBox.show();
        errorMessageBox.css({'opacity': "1"});
        shake(errorMessageBox, 25, 30);
        errorMessageBox.animate({'opacity': 0}, 10 * 1000);
    }
}

var timer;
var timerCounter;
function disableSendCheckCode(seconds) {
    /*
     将按钮状态改为禁用状态，并在倒计时结束将按钮状态改为可用
     注意：如果按钮原来状态就为禁用，倒计时结束后按钮会可用状态，而不是之前的禁用状态。
     */
    // 设置默认参数
    if (arguments.length == 0) {
        seconds = 60;
    }
    // 将按钮设置为无效，并倒计时后将其恢复
    sendCheckCode = $('#sendCheckCode');
    if (sendCheckCode.attr('disabled') == undefined) {
        sendCheckCode.attr('disabled', true);
    }
    timerCounter = seconds;
    // 保存按钮原来的html内容
    buttonHtml = sendCheckCode.html();
    // 启动一个定时器
    timer = setInterval(function () {
        if (timerCounter-- > 0) {
            sendCheckCode.html("" + timerCounter + "秒后可重发");
        } else {
            clearInterval(timer);
            sendCheckCode.html(buttonHtml);
            sendCheckCode.attr('disabled', false);
        }
    }, 1000);
}

// document ready 的加载动作
$(document).ready(function () {

    // 定义发送验证码按钮事件
    $('#sendCheckCode').on('click', function () {
        // 调用发送短信验证码的服务
        $(this).attr('disabled', true);
        $.ajax({
            url: $('#sendCheckCode').data('service-url'),
            data: { phone: $('#registerForm #phone').val() },
            type: "post",
            dataType: "json",
            async: true,
            // 通讯成功，解析返回结果做进一步处理
            success: function (result) {
                if (result.secondsRemain != undefined) {
                    // 如果服务返回了延时控制信息，根据延时控制信息禁用按钮
                    disableSendCheckCode(result.secondsRemain);
                } else {
                    $('#sendCheckCode').attr('disabled', false);
                }
                if (result.resultCode != 0) {
                    // 如果返回失败显示出错信息
                    showErrorMessage(result.resultMessage);
                }
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                showErrorMessage('网络连接不稳定，请稍后重试!');
                $('#sendCheckCode').attr('disabled', false);
            }
        });
    });

    // 如果有错误提示信息将其显示出来
    showErrorMessage();
});