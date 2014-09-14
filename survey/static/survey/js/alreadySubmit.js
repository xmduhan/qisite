function initReturnBackButton(scope) {
    scope.find('#returnBackButton').on('click', function () {
        logger.debug('returnBackButton.click is called');
        action = $(this).data('binding-action');
        logger.debug('action=' + action);
        location.replace(action);
    });
}

/***************************************
 *        所有控件初始化操作工作       *
 ***************************************/
function initial(scope) {
    // 初始化发送短信按钮事件
    initReturnBackButton(scope);
}

/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 全局初始化
    initial($('body'));
});
