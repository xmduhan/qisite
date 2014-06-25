/***************************************
 *      将问题id转为dom对象中的id      *
 ***************************************/
function getQuestionDocument(questionId) {
    return $('#question-' + questionId.replace(':', ''));
}


/***************************************
 *  初始化相关的bootstrap switch控件   *
 ***************************************/
function initBootstrapSwitch(scope) {
    scope.find(".bootstrap-switch-input").bootstrapSwitch.defaults.onText = '是';
    scope.find(".bootstrap-switch-input").bootstrapSwitch.defaults.offText = '否';
    scope.find(".bootstrap-switch-input").bootstrapSwitch();
    // 这段代码需要重构
    scope.find(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.onText = '乱序';
    scope.find(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.offText = '正常';
    scope.find(".bootstrap-switch-input-confused").bootstrapSwitch();

}

/***************************************
 *  初始化相关的bootstrap select控件   *
 ***************************************/
function initBootstrapSelect(scope) {
    scope.find('.selectpicker').selectpicker();
}

/***************************************
 *         初始化数据绑定字段          *
 ***************************************/
function initDataBinding(scope) {
    // 俘获文本框修改信息
    scope.find(".data-binding-field-text").on("change", function (event) {
        console.log('text edit is changed(' + $(this).val() + ')');
        saveFieldValue(this, $(this).val());
    });
    // 俘获开关控件的变动信息
    scope.find('.data-binding-field-switch').on('switchChange.bootstrapSwitch', function (event, state) {
        console.log('switch is changed(' + state + ')');
        saveFieldValue(this, state);
    });
    // 俘获选择控件的变动信息
    scope.find(".data-binding-field-select").on("change", function (event) {
        console.log('select is changed(' + $(this).val() + ')');
        saveFieldValue(this, $(this).val());
    });
}


/***************************************
 *       保存绑定字段数据到数据库      *
 ***************************************/
function saveFieldValue(control, value) {
    // 从控件中读取数据
    id = $(control).data('binding-id')
    field_name = $(control).data('binding-field-name')
    action = $(control).data('binding-action')
    data = {}
    data['id'] = id;
    data[field_name] = value;
    // 向服务器提交数据
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
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('save error');
        }
    });
}


/***************************************
 *          加载新增问题的DOM          *
 ***************************************/
function loadNewQuestionDocument(questionId) {
    action = "/survey/view/question/edit/" + encodeURIComponent(questionId)
    $.ajax({
        url: action,
        type: "get",
        async: true,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            console.log('loadNewQuestionDocument:success');
            //console.log(result);
            // 把问题的DOM补充到页面中
            $('#questionBox').append(result);
            // 重新绑定初始化的操作
            questionDocument = getQuestionDocument(questionId);
            initial(questionDocument);
            // 滚屏到最后
            $("html, body").animate({ scrollTop: $(document).height() }, 500);
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('loadNewQuestionDocument:error');
        }
    });
}


/***************************************
 *          绑定新增问题事件           *
 ***************************************/
function initQuestionAddAction(scope) {
    scope.find('#addSingleButton').on('click', function () {
        // 禁用所有新增按钮
        $(".btn-paper-add-question").attr('disabled', true);
        // 准备提交到服务器的数据
        paperId = $(this).data('binding-paperId')
        action = $(this).data('binding-action')
        data = {}
        data['paper'] = paperId;
        console.log('paper=' + paperId);
        // 向服务器提交数据
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
                    console.log('id:' + result['id']);
                    loadNewQuestionDocument(result['id']);
                    $('#addQuestionDialog').modal('hide');
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
                //console.log("The request is complete!");
                // 恢复按钮状态
                $(".btn-paper-add-question").attr('disabled', false);
            }
        });
    });
}

/***************************************
 *         更新修改问题的DOM信息       *
 ***************************************/
function refreshQuestionDocument(questionId) {
    console.log('refreshQuestionDocument is call id=' + questionId);
    action = "/survey/view/question/edit/" + encodeURIComponent(questionId);
    $.ajax({
        url: action,
        type: "get",
        async: true,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            console.log('refreshQuestionDocument:success');
            //console.log(result);
            //console.log("#question:" + questionId);
            // 替换question的document内容
            questionDocument = getQuestionDocument(questionId);
            questionDocument.replaceWith(result);
            // 重新绑定初始化的操作(注意：这里需要重新查询jQuery对象，因为replaceWith后原来jQuery对象失效了)
            initial(getQuestionDocument(questionId));
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('refreshQuestionDocument:error');
        }
    });
}

/***************************************
 *          绑定新增选项事件           *
 ***************************************/
function initBranchAddAction(scope) {
    scope.find('.btn-question-add-branch').on('click', function () {
        console.log('btn-question-add-branch is call');
        // 将按钮禁用，待question的DOM重新加载后，按钮会自动恢复。
        $(this).attr('disabled', true);
        // 准备提交到服务器的数据
        questionId = $(this).data('binding-questionId')
        action = $(this).data('binding-action')
        data = {}
        data['question'] = questionId;
        console.log('question=' + questionId);
        // 向服务器提交数据
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
                    // 更新问题的DOM信息
                    refreshQuestionDocument(questionId);
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
                //console.log("The request is complete!");
            }
        });
    });
}

/***************************************
 *          绑定问题删除事件           *
 ***************************************/
function initQuestionDeleteConfirmButtonAction() {
    $('#questionDeleteConfirmButton').on('click', function () {
        console.log('initQuestionDeleteAction() is called');
        confirmButton = $(this);
        confirmButton.attr('disabled', true);
        // 准备提交到服务器的数据
        id = confirmButton.data('binding-id');
        action = confirmButton.data('binding-action');
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
                    // 删除问题对应的DOM对象
                    getQuestionDocument(id).remove();
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
                console.log('initQuestionDeleteConfirmButtonAction:complete');
                confirmButton.attr('disabled', false);
                $('#questionDeleteConfirmDialog').modal('hide');
            }
        });
    });
}

/***************************************
 *          绑定问题删除事件           *
 ***************************************/
function initQuestionDeleteAction(scope) {
    scope.find('.btn-paper-delete-question').on('click', function () {
        // 要删除的选项信息放到确定按钮的data中,以便在点确定按钮的时间函数中可以直接用$(this).data来访问
        $('#questionDeleteConfirmButton').data('binding-id', $(this).data('binding-id'));
        $('#questionDeleteConfirmButton').data('binding-action', $(this).data('binding-action'));
        // 将对象框显示出来
        $('#questionDeleteConfirmDialog').modal('show');
    });
}

/***************************************
 *     选项删除确认按钮的事件处理      *
 ***************************************/

function initBranchDeleteConfirmButtonAction() {
    $('#branchDeleteConfirmButton').on('click', function () {
        console.log('initBranchDeleteConfirmButtonAction() is called');
        confirmButton = $(this);
        confirmButton.attr('disabled', true);
        // 准备提交到服务器的数据
        id = confirmButton.data('binding-id')
        action = confirmButton.data('binding-action')
        questionId = confirmButton.data('binding-question-id')
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
                    // 删除问题对应的DOM对象
                    refreshQuestionDocument(questionId);
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
                console.log('initBranchDeleteConfirmButtonAction:complete');
                confirmButton.attr('disabled', false);
                $('#branchDeleteConfirmDialog').modal('hide');
            }
        });
    });
}

/***************************************
 *          绑定选项删除事件           *
 ***************************************/
function initBranchDeleteAction(scope) {
    scope.find('.btn-question-delete-branch').on('click', function () {
        // 要删除的选项信息放到确定按钮的data中,以便在点确定按钮的时间函数中可以直接用$(this).data来访问
        $('#branchDeleteConfirmButton').data('binding-id', $(this).data('binding-id'));
        $('#branchDeleteConfirmButton').data('binding-action', $(this).data('binding-action'));
        $('#branchDeleteConfirmButton').data('binding-question-id', $(this).data('binding-question-id'));
        // 将对象框显示出来
        $('#branchDeleteConfirmDialog').modal('show');
    });
}

/***************************************
 *          绑定弹出提示事件           *
 ***************************************/
// 由于bootstrap这样的控件会自己生成一个显示的div元素，并截取消息，原本的select对象实际是收不到mouseover这样的校园的。
// 而新生成的div显示div是不包含data-*元素的拷贝，这样无法显示提示信息，所以如果是这种情况就要尝试的找到那个原始定义的
// select元素，这个元素的位置是新生成div元素的前一个同级的元素。
function findPopoverDataElement(e) {
    if ($(e).data('data-placement') == undefined) {
        // 特殊处理
        return $(e).prev();
    } else {
        return $(e);
    }
}
function initPopover(scope) {
    scope.find(".with-popover").on('mouseover', function (e) {
        console.log('mouseover is call');
        dataElement = findPopoverDataElement(this);
        $(this).popover('destroy');
        $(this).popover({
            trigger: 'manual',
            container: 'body',
            placement: dataElement.data('placement'),
            title: dataElement.data('original-title'),
            content: dataElement.data('content'),
            html: true
        });
        $(this).popover('show');
    });
    scope.find(".with-popover").on('mouseleave', function (e) {
        console.log('mouseleave is call');
        $(this).popover('destroy');
    });
}

// 找到switch控件
// $('.with-popover').parent('.bootstrap-switch-container')
// $('.with-popover').parent('.bootstrap-switch-container').find('.with-popover')

/***************************************
 *        所有空间初始化操作工作       *
 ***************************************/
// ***** 要考虑一下这个函数如果重复调用是否会出现问题 ******
function initial(scope) {
    // 初始化Bootstrap switch控件
    initBootstrapSwitch(scope);
    // 初始化Bootstrap select控件
    initBootstrapSelect(scope);
    // 初始化数据绑定字段
    initDataBinding(scope);
    // 初始化新增问题事件
    initQuestionAddAction(scope);
    // 初始化新增选项事件
    initBranchAddAction(scope);
    // 初始化问题删除事件
    initQuestionDeleteAction(scope);
    // 初始化分支删除事件
    initBranchDeleteAction(scope);
    // 初始化弹出框信息
    initPopover(scope);
}
/***************************************
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 绑定body中的所有相关控件的事件
    // 并初始化switch和selec
    initial($('body'));

    // 初始问题确认删除按钮事件
    initQuestionDeleteConfirmButtonAction();
    // 初始化选项确认删除按钮事件
    initBranchDeleteConfirmButtonAction();
});