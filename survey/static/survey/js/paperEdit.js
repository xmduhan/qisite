/***************************************
 *      将问题id转为dom对象中的id      *
 ***************************************/
function getQuestionDocument(questionId) {
    return $('#question-' + questionId.replace(':', ''));
}

function getBranchDocument(branchId) {
    return $('#branch-' + branchId.replace(':', ''));
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
    scope.find('.bootstrap-select').selectpicker();
    // 这好像是bootstrap-select是bootstrap的一个bug，我们并没有指定title但它还是出现，文档中说默认是null
    // 由于莫名奇妙的被加了一个title进去，这里之后设置了一段代码将其去掉
    scope.find('.bootstrap-select').find('button').attr('title', '');
    // 每次mouseover事件发生时都去掉一次，这样就没有机会套弹出这个title提示了。
    scope.find('.bootstrap-select').find('button').on('mouseover', function () {
        console.log('bootstrap-select.button.mouseover is call');
        $(this).attr('title', '');
    });
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
function displayRefreshIcon(control) {
    console.log('displayRefreshIcon is called');
    //icon = itemSaved.closest('.data-binding-refresh-icon');
    icon = $(control).closest('.panel').find('.data-binding-refresh-icon');
    //console.log(icon);
    icon.stop(true, true);
    icon.css('opacity', 1);
    icon.animate({'opacity': 0}, 3000);
}

function disableFinishButton() {
    console.log('disableFinishButton() is called');
    $('#finishButton').attr('disabled', true);
}
function enableFinishButton() {
    console.log('enableFinishButton() is called');
    $('#finishButton').attr('disabled', false);
}

function saveFieldValue(control, value) {
    // 保存期间禁止完成按钮
    disableFinishButton();
    // 从控件中读取数据
    console.log('saveFieldValue is called');
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
            displayRefreshIcon(control);
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('save error');
        },
        complete: function (xhr, status) {
            // 保存操作完成使完成按钮可用
            enableFinishButton();
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
                    getQuestionDocument(id).animate({'opacity': 0}, 1500, callback = function () {
                        $(this).remove();
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
                    getBranchDocument(id).animate({'opacity': 0}, 1000, callback = function () {
                        refreshQuestionDocument(questionId);
                        //$(this).remove();
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
// 由于bootstrap-select bootstrap-switch这样的控件会自己生成一个显示的div元素，并截取消息，原本的select对象实际是收不到
// mouseover这样的校园的。而新生成的div显示div是不包含data-*元素的拷贝，这样无法显示提示信息，所以如果是这种情况就要尝试
// 的找到那个原始定义的select元素，这个元素的位置是新生成div元素的前一个同级的元素。
function findPopoverDataElement(e) {
    // 普通的bootstrap元素
    if ($(e).data('placement') != undefined) {
        return $(e);
    }
    //尝试将元素当成一个bootstrap-select元素寻找其popover数据节点
    // 处理bootstrap-select如此复杂，源于其dom结构，其结构大体如下：
    // <select class='selectpicker ...' data-placement='...' data-content='..' ></select>   // 代码中定义的
    // <div ...>                                  // 以下都是由bootstrap-select初始化函数添加的
    //    <button ... data-original-title >
    //        <span class='filter-option ...'></span>
    //        <span class = 'caret'>...</span>
    //    </button>
    //    <div class='dropdown-menu'>...</div>
    // </div>
    // 1、不能使用顶级的div来绑定消息，这样导致鼠标在选择下拉菜单时也会出现提示，因为顶级div是下来菜单的父节点。
    // 2、本来button是最好选择，但是由于在data-original-title在此button中的含义有预定，而该属性是提示框的默认标题参数名
    // 称，而且该参数如果在DOM中指定了，无法在javascript重新指定。
    // 3、所以才被迫使用button下的一个span来绑定事件和弹出提示。
    if ($(e).parent().parent().prev().data('placement') != undefined) {
        return $(e).parent().parent().prev();
    }
    // 尝试将元素当成一个bootstrap-switch元素寻找其popover数据节点
    if ($(e).find('.bootstrap-switch-with-popover').data('placement') != undefined) {
        return $(e).find('.bootstrap-switch-with-popover');
    }
    return undefined;
}
// 鼠标进入事件
function popoverOnMouseOver() {
    //console.log('mouseover is call');
    dataElement = findPopoverDataElement(this);
    //console.log(dataElement);
    $(this).popover('destroy');
    $(this).popover({
        trigger: 'manual',
        container: 'body',
        title: "<span class='glyphicon glyphicon-hand-right'></span> 提示",
        placement: dataElement.data('placement'),
        content: dataElement.data('content'),
        html: true
    });
    $(this).popover('show');
}

// 鼠标移出事件
function popoverOnMouseLeave(e) {
    //console.log('mouseleave is call');
    $(this).popover('destroy');
}

// 绑定弹出事件
function initPopover(scope) {
    // 绑定普通的bootstrap控件
    scope.find(".with-popover").on('mouseover', popoverOnMouseOver);
    scope.find(".with-popover").on('mouseleave', popoverOnMouseLeave);
    scope.find(".with-popover").on('click', popoverOnMouseLeave);
    // 绑定bootstrap-switch控件
    scope.find('.bootstrap-switch-with-popover').parent('.bootstrap-switch-container').on('mouseover', popoverOnMouseOver);
    scope.find('.bootstrap-switch-with-popover').parent('.bootstrap-switch-container').on('mouseleave', popoverOnMouseLeave);
    scope.find('.bootstrap-switch-with-popover').parent('.bootstrap-switch-container').on('click', popoverOnMouseLeave);
    // 绑定bootstrap-select控件(如此复杂处理，原因具体见findPopoverDataElement中的说明)
    scope.find(".bootstrap-select-with-popover").find('button').find('.filter-option').on('mouseover', popoverOnMouseOver);
    scope.find(".bootstrap-select-with-popover").find('button').find('.filter-option').on('mouseleave', popoverOnMouseLeave);
    scope.find(".bootstrap-select-with-popover").find('button').find('.filter-option').on('click', popoverOnMouseLeave);
}

/***************************************
 *       绑定问题折叠按钮的事件        *
 ***************************************/
function initQuestionCollapse(scope) {
    scope.find('#collapse-all-question-hide').on('click', function (e) {
        $('.question-body').collapse('hide');
    });
    scope.find('#collapse-all-question-show').on('click', function (e) {
        $('.question-body').collapse('show');
    });
    scope.find('.collapse-this-question').on('dblclick', function (e) {
        $(this).parent().find('.question-body').collapse('toggle');
    });
}

/***************************************
 *       下来框的可选数据的绑定        *
 ***************************************/
function OptionDecoder() {
    return OptionDecoder.prototype;
}
OptionDecoder.prototype.defaultSelect = function (question) {
    selected = '';
    if (question['selected']) {
        selected = 'selected = "selected"';
    }
    option = '<option ' + selected + ' value="' + question['id'] + '">' + question['num'] + '</option>';
    return option;
}
OptionDecoder.prototype.branchReachableQuestion = function (question) {
    selected = '';
    if (question['selected']) {
        selected = 'selected = "selected"';
    }
    // 根据不同的问题类型显示不同的图标
    console.log('question["type"]=' + question['type']);
    switch (question['type']) {
        case 'EndValid':
            iconName = "glyphicon-ok";
            break;
        case 'EndInvalid':
            iconName = "glyphicon-ban-circle";
            break;
        case null:
            iconName = "glyphicon-arrow-down";
            break;
        default:
            iconName = 'glyphicon-arrow-right';
    }
    option = '<option data-icon="' + iconName + '" ' + selected + ' value="' + question['id'] + '">' + question['num'] + '</option>';
    return option;
}

// 通过链接和参数获取select的option列表的函数，提供给initBindingDropdown是用
function getSelectOptionsHtml(action, parameters, decoder) {
    serviceUrl = action + '?' + parameters;
    ajaxSuccess = false;
    questionList = null;
    $.ajax({
        url: serviceUrl,
        type: "post",
        dataType: "json",
        async: false,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            ajaxSuccess = true;
            questionList = result['questionList'];
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            // 出错处理(暂缺)
        }
    });
    // 如果失败返回空串
    if (!ajaxSuccess) {
        return undefined;
    }
    // 将返回结果转化html的select选项格式
    selectOptionsHtml = '';
    for (i in questionList) {
        question = questionList[i];
        //option = decodeOptionDefault(question);
        option = decoder(question);
        selectOptionsHtml += option;
    }
    console.log(selectOptionsHtml);
    return selectOptionsHtml;
}

function initBindingDropdown(scope) {
    // 锁定鼠标的mousedown事件，这个时间比click要来的早，所以在这个是用先把select的信息更新，并且refresh
    // ******************************************** 存在问题 ********************************************
    // 由于bootstrap-select似乎存在一个bug就是在启用data-icon属性，且同时俘获了mousedown事件，点击按钮中间的文字部分
    // 下拉框是无法弹出的，请见云笔记中bootstrap中的bootstrap-select记录
    // 所以这里只好先用mouseenter代替，但是这个是会给服务器增加很多不必要的请求。
    // 但目前没有更好的办法，后续再解决这个问题。
    // --------------------------
    // 后来改用了click时间似乎就可以了，但如何保证click时间比bootstrap中定义的来得早？还不完全清楚
    // 但目前来看是能正常工作了。
    scope.find('.bootstrap-select-binding-dropdown').find('button').on('click', function (event) {
        console.log('mouseenter is called');
        // 找到对应的数据节点并读取信息
        dataElement = $(this).parent().prev();
        action = dataElement.data('binding-dropdown-action');
        parameters = dataElement.data('binding-dropdown-parameters');
        decoderName = dataElement.data('binding-dropdown-decoder');
        // 读取设置选项处理器
        decoder = null;
        optionDecoder = OptionDecoder();
        if (decoderName in optionDecoder) {
            decoder = optionDecoder[decoderName];
        } else {
            decoder = optionDecoder.defaultSelect;
        }
        // 向服务器请求选项数据并转为html的select option的格式
        selectOptionsHtml = getSelectOptionsHtml(action, parameters, decoder);
        if (selectOptionsHtml != undefined) {
            dataElement.html(selectOptionsHtml);
            dataElement.selectpicker('refresh');
            // 这好像是bootstrap-select是bootstrap的一个bug，我们并没有指定title但它还是出现，文档中说默认是null
            $('.bootstrap-select').find('button').attr('title', '');
        } else {
            // 如果请求列表失败，则让select控件保持原来的状态，不做处理。
            console.log('initBindingDropdown:获取选项列表失败');
        }
    });
}

/***************************************
 *  同步问题题干信息和其编辑框的标题   *
 ***************************************/
function initQuestionTitleSynchronization(scope) {
    scope.find(".question-text-editor").on("change", function (event) {
        console.log('question title need change');
        titlePanel = $(this).parents('.panel').find('.question-title-panel-text');
        titlePanel.html($(this).val());
    });
}

/***************************************
 *      初始化问题的顺序调整功能       *
 ***************************************/
function initQuestionSortable() {
    $("#questionBox").sortable();
    $("#questionBox").disableSelection();
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

function initDeleteButtonColorChange(scope) {
    // 为问题删除按钮绑定事件
    $(".btn-paper-delete-question").on('mouseenter', function (event) {
        lightDeleteButton(this);
    });
    $(".btn-paper-delete-question").on('mouseleave', function (event) {
        slakeDeleteButton(this);
    });
    // 为选项删除按钮绑定事件
    $(".btn-question-delete-branch").on('mouseenter', function (event) {
        lightDeleteButton(this);
    });
    $(".btn-question-delete-branch").on('mouseleave', function (event) {
        slakeDeleteButton(this);
    });
}

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
    // 初始化折叠按钮
    initQuestionCollapse(scope);
    // 初始化下拉框可选项数据绑定
    initBindingDropdown(scope);
    // 初始化问题题干和编辑框间的同步操作
    initQuestionTitleSynchronization(scope);
    // 初始化删除按钮的颜色变化
    initDeleteButtonColorChange(scope);
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
    // 初始化问题的排序功能
    initQuestionSortable();
});


