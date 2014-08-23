/***************************************
 *        通过调查id获取调查记录       *
 ***************************************/
function getSurveyRecord(surveyId) {
    str = '#survey-' + surveyId.replace(':', '');
    console.log('str=' + str);
    return $(str);
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

/***************************************
 *        初始化删除按钮的颜色变化     *
 ***************************************/

function lightDeleteButton(button) {
    logger.debug('mouseenter() is called');
    $(button).stop(true, true);
    $(button).animate({'color': '#e50a22'}, 800);
}

function slakeDeleteButton(button) {
    logger.debug('mouseleave() is called');
    $(button).stop(true, true);
    $(button).animate({'color': '#421410'}, 800);
}

function initDeleteButtonColorChange(scope) {
    // 为问题删除按钮绑定事件
    scope.find(".btn-delete-survey").on('mouseenter', function (event) {
        lightDeleteButton(this);
    });
    scope.find(".btn-delete-survey").on('mouseleave', function (event) {
        slakeDeleteButton(this);
    });
}


/***************************************
 *          绑定调查删除事件           *
 ***************************************/
function initSurveyDeleteAction(scope) {
    scope.find('.btn-delete-survey').on('click', function () {
        // 读取控件的数据绑定信息
        action = $(this).data('binding-action');
        id = $(this).data('binding-id');

        // 定义用户确认后的具体删除动作
        surveyDeleteConfirmAction = function () {
            logger.debug('surveyDeleteConfirmAction is called');
            // 准备提交到服务器的数据
            data = {}
            data['id'] = id
            $.ajax({
                url: action, data: data, type: "post", dataType: "json", async: true,
                // 通讯成功，解析返回结果做进一步处理
                success: function (result) {
                    if (result['resultCode'] == 0) {
                        // 删除问卷对应的DOM对象
                        getSurveyRecord(id).animate({'opacity': 0}, 1500, callback = function () {
                            location.reload();
                        });
                    } else {
                        // 出错处理(暂缺)
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
        showConfirmDialog('您确认要删除这个调查吗?', surveyDeleteConfirmAction);
    });
}


/***************************************
 *        所有控件初始化操作工作       *
 ***************************************/
// ***** 要考虑一下这个函数如果重复调用是否会出现问题 ******
function initial(scope) {
    initDeleteButtonColorChange(scope);
    initSurveyDeleteAction(scope);
}
/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {

    // 绑定页面切换输入框事件
    initial($('body'));
    initPageSwitcher();
    console.log('---ready is called---');
});