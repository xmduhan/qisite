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
    id = $(control).data('id')
    field_name = $(control).data('field-name')
    action = $(control).data('action')
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
            console.log('errorCode:' + result['errorCode']);
            console.log('errorMessage:' + result['errorMessage']);
            if ($(control).data('reload-page') == true) {
                console.log('page need reload');
            }
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

function test() {
    ('#addSingleButton').on('click', function (event) {
        console.log('addSingleButton is push');
    });
    ('#addQuestionButton').on('click', function (event) {
        console.log('addQuestionButton is push');
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
});