$(document).ready(function () {
    $(".bootstrap-switch").bootstrapSwitch.defaults.onText = '是';
    $(".bootstrap-switch").bootstrapSwitch.defaults.offText = '否';
    $(".bootstrap-switch").bootstrapSwitch();
    $(".bootstrap-switch-confused").bootstrapSwitch.defaults.onText = '乱序';
    $(".bootstrap-switch-confused").bootstrapSwitch.defaults.offText = '正常';
    $(".bootstrap-switch-confused").bootstrapSwitch();
});