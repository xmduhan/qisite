/***************************************
 *  初始化相关的bootstrap switch控件   *
 ***************************************/
function initBootstrapSwitch() {
    $(".bootstrap-switch-input").bootstrapSwitch.defaults.onText = '是';
    $(".bootstrap-switch-input").bootstrapSwitch.defaults.offText = '否';
    $(".bootstrap-switch-input").bootstrapSwitch();
    // 这段代码需要重构
    $(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.onText = '乱序';
    $(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.offText = '正常';
    $(".bootstrap-switch-input-confused").bootstrapSwitch();
    $('.selectpicker').selectpicker();
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
 *         初始化数据绑定字段          *
 ***************************************/
function initDataBinding() {
    // 俘获文本框修改信息
    $(".data-binding-field-text").on("change", function (event) {
        console.log('text edit is changed(' + $(this).val() + ')');
        saveFieldValue(this, $(this).val());
    });
    // 俘获开关控件的变动信息
    $('.data-binding-field-switch').on('switchChange.bootstrapSwitch', function (event, state) {
        console.log('switch is changed(' + state + ')');
        saveFieldValue(this, state);
    });
    // 俘获选择控件的变动信息
    $(".data-binding-field-select").on("change", function (event) {
        console.log('select is changed(' + $(this).val() + ')');
        saveFieldValue(this, $(this).val());
    });
}

/***************************************
 *        获取问题修改DOM代码块        *
 ***************************************/
function loadQuestionDocument(id) {
    action = "/survey/view/question/edit/" + encodeURIComponent(id)
    $.ajax({
        url: action,
        type: "get",
        async: true,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            console.log('loadQuestionDocument:success');
            //console.log(result);
            // 把问题的DOM补充到页面中
            $('#questionBox').append(result);
            // 滚屏到最后
            $("html, body").animate({ scrollTop: $(document).height() }, 500);
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('loadQuestionDocument:error');
        }
    });
}


/***************************************
 *          绑定新增按钮事件           *
 ***************************************/
function initButtonAddAction() {
    $('#addSingleButton').on('click', function () {
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
                    loadQuestionDocument(result['id']);
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
 *          全局初始化加载操作         *
 ***************************************/
$(document).ready(function () {
    // 初始化bootstrap switch控件
    initBootstrapSwitch();
    // 初始化数据绑定字段
    initDataBinding();
    // 初始化新增按钮事件
    initButtonAddAction()
});