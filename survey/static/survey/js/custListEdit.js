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
        action = $("#custListItemAddForm").attr('action')
        logger.debug(action);
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
                //logger.debug('validationMessage:' + result['validationMessage']);
                if (result['resultCode'] == 0) {
                    logger.debug('id:' + result['id']);
                    location.reload();
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
 *        通过调查id获取调查记录       *
 ***************************************/
function getCustListItemRecord(custListId) {
    str = '#custListItem-' + custListId.replace(':', '');
    console.log('str=' + str);
    return $(str);
}

/***************************************
 *          绑定调查删除事件           *
 ***************************************/
function initCustListItemDeleteAction() {
    $('.btn-delete-custListItem').on('click', function () {
        // 读取控件的数据绑定信息
        action = $(this).data('binding-action');
        id = $(this).data('binding-id');
        logger.debug('id=' + id);

        // 定义用户确认后的具体删除动作
        custListItemDeleteConfirmAction = function () {
            logger.debug('custListItemDeleteConfirmAction is called');
            // 准备提交到服务器的数据
            data = {}
            data['id'] = id
            $.ajax({
                url: action, data: data, type: "post", dataType: "json", async: true,
                // 通讯成功，解析返回结果做进一步处理
                success: function (result) {
                    if (result['resultCode'] == 0) {
                        // 删除客户清单对应的DOM对象
                        getCustListItemRecord(id).animate({'opacity': 0}, 1500, callback = function () {
                            location.reload();
                        });
                    } else {
                        // 出错处理(暂缺)
                        logger.debug('resultCode=' + result['resultCode']);
                        logger.debug('resultMessage=' + result['resultMessage']);
                    }
                },
                // 失败说明网络有问题或者服务器有问题
                error: function (xhr, status, errorThrown) {
                    logger.debug('network error!');
                    // 出错处理(暂缺)
                }
            });
        }
        // 显示确定对话框
        showConfirmDialog('您确认要删除这个清单项吗?', custListItemDeleteConfirmAction);
    });
}


/***************************************
 *          全局初始化加载操作         *
 ***************************************/

$(document).ready(function () {
    initAddCustListItemConfirm();
    initCustListItemDeleteAction();
});