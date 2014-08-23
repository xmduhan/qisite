/***************************************
 *        通过调查id获取调查记录       *
 ***************************************/
function getCustListRecord(custListId) {
    str = '#custList-' + custListId.replace(':', '');
    console.log('str=' + str);
    return $(str);
}


/***************************************
 *          绑定调查删除事件           *
 ***************************************/
function initCustListDeleteAction() {
    $('.btn-custList-delete').on('click', function () {
        // 读取控件的数据绑定信息
        action = $(this).data('binding-action');
        id = $(this).data('binding-id');
        logger.debug('id=' + id);

        // 定义用户确认后的具体删除动作
        custListDeleteConfirmAction = function () {
            logger.debug('custListDeleteConfirmAction is called');
            // 准备提交到服务器的数据
            data = {}
            data['id'] = id
            $.ajax({
                url: action, data: data, type: "post", dataType: "json", async: true,
                // 通讯成功，解析返回结果做进一步处理
                success: function (result) {
                    if (result['resultCode'] == 0) {
                        // 删除问卷对应的DOM对象
                        getCustListRecord(id).animate({'opacity': 0}, 1500, callback = function () {
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
        showConfirmDialog('您确认要删除这份清单吗?', custListDeleteConfirmAction);
    });
}

/***************************************
 *        初始化新增按钮点击事件       *
 ***************************************/
function initCustListAddButton() {
    logger.debug('initCustListAddButton() is called');
    $('.btn-custList-add').on('click', function () {
        action = '/survey/service/custList/add';
        data = {'name': '新增客户清单'};
        ajaxSuccess = false;
        custListId = undefined;
        // 向服务器提交数据
        $.ajax({
            url: action,
            data: data,
            type: "post",
            dataType: "json",
            async: false,
            // 通讯成功，解析返回结果做进一步处理
            success: function (result) {
                console.log('save successfully');
                console.log('resultCode:' + result['resultCode']);
                console.log('resultMessage:' + result['resultMessage']);
                console.log('custListId:' + result['custListId']);
                custListId = result['custListId'];
                ajaxSuccess = true;
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                console.log('save error');
            }
        });
        // 判断执行是否成功如果成功则转向编辑页面
        if (ajaxSuccess && custListId != undefined) {
            console.log('-----ajaxSuccess && custListId != undefined-----');
            window.location = "/survey/view/custList/edit/" + custListId;
        }
        console.log('ajaxSuccess=' + ajaxSuccess);
        console.log('custListId=' + custListId);
    });
}


/***************************************
 *        初始化删除按钮的颜色变化     *
 ***************************************/

function lightDeleteButton(button) {
    console.log('mouseenter() is called');
    $(button).stop(true, true);
    $(button).animate({'color': '#e50a22'}, 800);
}

function slakeDeleteButton(button) {
    console.log('mouseleave() is called');
    $(button).stop(true, true);
    $(button).animate({'color': '#421410'}, 800);
}

function initDeleteButtonColorChange() {
    // 为问题删除按钮绑定事件
    $(".btn-custList-delete").on('mouseenter', function (event) {
        lightDeleteButton(this);
    });
    $(".btn-custList-delete").on('mouseleave', function (event) {
        slakeDeleteButton(this);
    });
}


/***************************************
 *        绑定页面切换输入框事件       *
 ***************************************/
function initPageSwitcher() {
    $(".page-switcher").on('change', function (event) {
        action = $(this).data('binding-action') + $(this).val();
        window.location = action
    });
}

$(document).ready(function () {
    // 新增按钮事件处理
    initCustListAddButton();
    // 初始化删除按钮变色处理
    initDeleteButtonColorChange();
    //初始化清单删除事件
    initCustListDeleteAction();
    // 绑定页面切换输入框事件
    initPageSwitcher();
});
