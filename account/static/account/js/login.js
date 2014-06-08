function showErrorMessage(message) {
    // 如果提供了消息内容，填写到消息版中
    if (arguments.length != 0) {
        $('#errorMessage').html(message);
    }
    // 如果消息版中有内容，将其显示出来并，震动消息框
    if ($('#errorMessage').html() != '') {
        errorMessageBox = $('#errorMessageBox')
        errorMessageBox.stop(true, true)
        errorMessageBox.show();
        errorMessageBox.css({'opacity': "1"});
        shake(errorMessageBox, 25, 30);
        errorMessageBox.animate({'opacity': 0}, 10 * 1000);
    }
}

$(document).ready(function () {
    // 如果有错误提示信息将其显示出来
    showErrorMessage();
});