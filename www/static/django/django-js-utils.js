Django = function () {

}

//警告:该接口使用逗号分隔串来传递url中需要应用的参数列表(args)，如果参数中含有逗号将要出现异常
Django.prototype.reverse = function (viewname, args) {
    args = args || [];
    resultUrl = '';
    data = {}
    data['viewname'] = viewname;
    data['args'] = args.toString();
    logger.debug(data);
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
                throw  result['resultMessage'];
            }
            resultUrl = result['url'];
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            throw '无法连接服务器';
        }
    });
    return resultUrl;
}

django = new Django();