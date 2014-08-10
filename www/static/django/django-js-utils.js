Django = function () {

}

//警告:该接口使用逗号分隔串来传递url中需要应用的参数列表(args)，如果参数中含有逗号将要出现异常
//注意: 这里不能对参数(args)使用encodeURIComponent，因为reverse本身就会对参数进行encode
Django.prototype.reverse = function (viewname, args) {
    logger.debug('reverse(viewname=' + viewname + ')');
    args = args || [];
    resultUrl = undefined;
    data = {}
    data['viewname'] = viewname;
    data['args'] = args.toString();
    logger.debug(data);
    errorMessage = undefined;
    $.ajax({
        url: "/www/django/reverse",
        type: "post",
        async: false,
        data: data,
        dataType: "json",
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            if (result['resultCode'] != 0) {
                logger.debug('result["resultCode"]=' + result['resultCode']);
                logger.debug(result['resultMessage']);
                errorMessage = result['resultMessage'];
            }
            resultUrl = result['url'];
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            errorMessage = '无法连接服务器';
        }
    });
    // 在ajax调用中异常是抛不出去的
    if (errorMessage != undefined) {
        throw errorMessage;
    }
    // 返回url
    return resultUrl;
}

django = new Django();