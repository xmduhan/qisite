/***************************************
 *         初始表单提交按钮            *
 ***************************************/
function initFormSubmitButton(scope) {
    logger.debug('initFormSubmitButton is called');
    scope.find('.form-submit-button').on('click', function () {
        logger.debug('form-submit-button.click is called');
        formId = $(this).data('form-id');
        form = $('#' + formId);
        form.submit();
    });
}
/***************************************
 *        所有控件初始化操作工作       *
 ***************************************/
function initial(scope) {
    initFormSubmitButton(scope);
}
/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 绑定body中的所有相关控件的事件
    // 并初始化switch和select
    initial($('body'));
});
