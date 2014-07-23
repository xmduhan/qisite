

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
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {

    // 绑定页面切换输入框事件
    initPageSwitcher();
    console.log('---ready is called---');
});