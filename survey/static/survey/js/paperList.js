function getPaperRecord(paperId) {
    str = '#paper-' + paperId.replace(':', '');
    console.log('str=' + str);
    return $(str);
}


/***************************************
 *        初始化新增按钮点击事件       *
 ***************************************/
function initPaperAddButton() {
    $('.btn-paper-add').on('click', function () {
        action = '/survey/service/paper/add';
        data = {'title': '新增问卷'};
        ajaxSuccess = false;
        paperId = undefined;
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
                console.log('paperId:' + result['paperId']);
                paperId = result['paperId'];
                ajaxSuccess = true;
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                console.log('save error');
            }
        });
        // 判断执行是否成功如果成功则转向编辑页面
        if (ajaxSuccess && paperId != undefined) {
            console.log('-----ajaxSuccess && paperId != undefined-----');
            window.location = "/survey/view/paper/edit/" + paperId;
        }
        console.log('ajaxSuccess=' + ajaxSuccess);
        console.log('paperId=' + paperId);
    });
}

/***************************************
 *          绑定问题删除事件           *
 ***************************************/
function initQuestionDeleteAction() {
    $('.btn-paper-delete').on('click', function () {
        console.log('.btn-paper-delete.click is call');
        // 要删除的选项信息放到确定按钮的data中,以便在点确定按钮的时间函数中可以直接用$(this).data来访问
        $('#paperDeleteConfirmButton').data('binding-id', $(this).data('binding-id'));
        $('#paperDeleteConfirmButton').data('binding-action', $(this).data('binding-action'));
        // 将对象框显示出来
        $('#paperDeleteConfirmDialog').modal('show');
    });
}

/***************************************
 *        绑定问卷删除确定事件         *
 ***************************************/
function initPaperDeleteConfirmButtonAction() {
    $('#paperDeleteConfirmButton').on('click', function () {
        console.log('initPaperDeleteConfirmButtonAction() is called');
        confirmButton = $(this);
        confirmButton.attr('disabled', true);
        // 准备提交到服务器的数据
        id = confirmButton.data('binding-id')
        action = confirmButton.data('binding-action')
        //console.log('action=' + action);
        //console.log('id=' + id);
        data = {}
        data['id'] = id
        $.ajax({
            url: action,
            data: data,
            type: "post",
            dataType: "json",
            async: true,
            // 通讯成功，解析返回结果做进一步处理
            success: function (result) {
                console.log('save successfully');
                console.log('resultCode:' + result['resultCode']);
                console.log('resultMessage:' + result['resultMessage']);
                //
                if (result['resultCode'] == 0) {
                    // 被删除的问卷记录的淡出效果，并更新页面
                    getPaperRecord(id).animate({'opacity': 0}, 1500, callback = function () {
                        location.reload();
                    });
                } else {
                    // 出错处理(暂缺)
                }
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                console.log('network error!');
                // 出错处理(暂缺)
            },
            complete: function (xhr, status) {
                console.log('initPaperDeleteConfirmButtonAction:complete');
                confirmButton.attr('disabled', false);
                $('#paperDeleteConfirmDialog').modal('hide');
            }
        });
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
    $(".btn-paper-delete").on('mouseenter', function (event) {
        lightDeleteButton(this);
    });
    $(".btn-paper-delete").on('mouseleave', function (event) {
        slakeDeleteButton(this);
    });
}


/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 新增按钮事件处理
    initPaperAddButton();
    // 初始化删除按钮点击事件
    initQuestionDeleteAction();
    // 初始化删除按钮的确认事件
    initPaperDeleteConfirmButtonAction();
    // 删除按钮的颜色变化效果
    initDeleteButtonColorChange();
    console.log('---ready is called---');
});
