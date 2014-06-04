// 初始化
$(document).ready(function () {
    $(".bootstrap-switch-input").bootstrapSwitch.defaults.onText = '是';
    $(".bootstrap-switch-input").bootstrapSwitch.defaults.offText = '否';
    $(".bootstrap-switch-input").bootstrapSwitch();
    // 这段代码需要重构
    $(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.onText = '乱序';
    $(".bootstrap-switch-input-confused").bootstrapSwitch.defaults.offText = '正常';
    $(".bootstrap-switch-input-confused").bootstrapSwitch();


    $('.selectpicker').selectpicker();

});

// 俘获文本框修改信息
$(".paper-attr-text").on("change", function (event) {
    console.log('text edit is changed(' + $(this).val() + ')');
});

// 俘获开关控件的变动信息
$('.paper-attr-switch').on('switchChange.bootstrapSwitch', function (event, state) {
    console.log('switch is changed(' + state + ')');
});

// 俘获选择控件的变动信息
$(".paper-attr-select").on("change", function (event) {
    console.log('select is changed(' + $(this).val() + ')');
});

