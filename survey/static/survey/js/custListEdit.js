/***************************************
 *   给定一个表单读取其中的所有信息项  *
 ***************************************/
function readFormValue(form) {
    result = {};
    form.find('input').each(function () {
        result[$(this).attr('name')] = $(this).val();
    });
    return result;
}


/***************************************
 *    初始化新增客户清单项的确定按钮   *
 ***************************************/
function initAddCustListItemConfirm() {
    $('#addCustListItemConfirm').on('click', function () {
        //logger.debug('addCustListItemConfirm() is call');
        data = readFormValue($("#custListItemAddForm"));
        action = $("#custListItemAddForm").data('binding-action');
        // 向服务器提交数据
        $.ajax({
            url: action,
            data: data,
            type: "post",
            dataType: "json",
            async: true,
            // 通讯成功，解析返回结果做进一步处理
            success: function (result) {
                logger.debug('save successfully');
                logger.debug('resultCode:' + result['resultCode']);
                logger.debug('resultMessage:' + result['resultMessage']);
                //
                if (result['resultCode'] == 0) {
                    logger.debug('id:' + result['id']);

                } else {
                    // 出错处理(暂缺)
                }
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                logger.debug('network error!');
                // 出错处理(暂缺)
            },
            complete: function (xhr, status) {
                //logger.debug("The request is complete!");
                // 恢复按钮状态

            }
        });

    });
}


/***************************************
 *          全局初始化加载操作         *
 ***************************************/

$(document).ready(function () {
    initAddCustListItemConfirm();

});