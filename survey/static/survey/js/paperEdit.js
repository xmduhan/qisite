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
function getQuestion(id) {
    action = "/survey/view/question/edit/" + id
    $.ajax({
        url: action,
        type: "get",
        async: true,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            console.log('getQuestion:success');
            console.log(result);
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            console.log('getQuestion:error');
        }
    });
}

/***************************************
 *          绑定新增按钮事件           *
 ***************************************/
function initButtonAddAction() {
    $('#addSingleButton').on('click', function () {
        // 调用增加服务（获取新增问题的id
        // 调用选项增加服务，增加两个默认选项
        // 调用后台服务读取html文件的DOM
        //
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
            },
            // 失败说明网络有问题或者服务器有问题
            error: function (xhr, status, errorThrown) {
                console.log('save error');
            },
            complete: function (xhr, status) {
                console.log("The request is complete!");
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