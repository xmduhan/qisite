/***************************************
 *         禁用按钮短信发送按钮        *
 ***************************************/
var timer;
var timerCounter;
function disableendSurveyToPhone(seconds) {
    /*
     将按钮状态改为禁用状态，并在倒计时结束将按钮状态改为可用
     注意：如果按钮原来状态就为禁用，倒计时结束后按钮会可用状态，而不是之前的禁用状态。
     */
    // 设置默认参数
    if (arguments.length == 0) {
        seconds = 60;
    }
    // 将按钮设置为无效，并倒计时后将其恢复
    sendCheckCode = $('#sendSurveyToPhone');
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

/***************************************
 *          发送短信按钮事件           *
 ***************************************/
function initSendSurveyToPhone(scope) {
    scope.find('#sendSurveyToPhone').on('click', function () {
        // 读取控件的数据绑定信息
        action = $(this).data('binding-action');
        id = $(this).data('binding-id');
        message = $('#message').val();
        //
        logger.debug('action' + action);
        logger.debug('id' + id);

        // 定义用户确认后的具体删除动作
        sendSurveyToPhoneAction = function () {
            logger.debug('sendSurveyToPhoneAction is call');
            $(this).attr('disabled', true);
            $.ajax({
                url: action,
                data: { id: id, message: message },
                type: "post",
                dataType: "json",
                async: true,
                // 通讯成功，解析返回结果做进一步处理
                success: function (result) {
                    if (result.secondsRemain != undefined) {
                        // 如果服务返回了延时控制信息，根据延时控制信息禁用按钮
                        disableendSurveyToPhone(result.secondsRemain);
                    } else {
                        $('#sendCheckCode').attr('disabled', false);
                    }
                    if (result.resultCode != 0) {
                        // 如果返回失败显示出错信息
                        showMessageDialog(result.resultMessage);
                    }
                },
                // 失败说明网络有问题或者服务器有问题
                error: function (xhr, status, errorThrown) {
                    showMessageDialog('网络连接不稳定，请稍后重试!');
                    $('#sendCheckCode').attr('disabled', false);
                }
            });
        }
        // 显示确定对话框
        showConfirmDialog('您确定要发送短信到手机吗?', sendSurveyToPhoneAction);
    });
}

/***************************************
 *        所有控件初始化操作工作       *
 ***************************************/
function initial(scope) {
    // 初始化发送短信按钮事件
    initSendSurveyToPhone(scope);
}

/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 全局初始化
    initial($('body'));
});