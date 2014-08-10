/***************************************
 *       让页面中对象震动的函数        *
 ***************************************/

function shake(obj, cycle, n) {
    /*
     参数说明：
     1、obj要产生震动效果的对象
     2、震动效果的周期，单位是毫秒
     3、要震动的次数
     */
    // 设置默认参数
    if (arguments.length < 2) {
        cycle = 30;
    }
    if (arguments.length < 3) {
        n = 30;
    }
    // 循环上下移动对象形成震动效果
    for (i = 0; i < n; i++) {
        pos = Math.sin(Math.PI * i / 2) * 10;
        obj.animate({"margin-top": pos + "px"}, cycle);
    }
    // 对象位置复位
    obj.animate({"margin-top": "0"}, cycle);
}

/***************************************
 *          定义日志工具               *
 ***************************************/
function FakeLogger() {
}

FakeLogger.prototype.log = function () {
}

FakeLogger.prototype.debug = function () {
}

FakeLogger.prototype.error = function () {
}

FakeLogger.prototype.warn = function () {
}

function Logger() {
    this.logger = console;
    //this.logger = new FakeLogger();
}

Logger.prototype.log = function (msg) {
    this.logger.log(msg);
}

Logger.prototype.debug = function (msg) {
    this.logger.debug(msg);
}

Logger.prototype.warn = function (msg) {
    this.logger.warn(msg);
}

Logger.prototype.error = function (msg) {
    this.logger.error(msg);
}

logger = new Logger();


/***************************************
 *             加载DOM                 *
 ***************************************/
function loadDomcument(url) {
    domResult = '';
    $.ajax({
        url: url,
        type: "get",
        async: false,
        // 通讯成功，解析返回结果做进一步处理
        success: function (result) {
            domResult = result;
        },
        // 失败说明网络有问题或者服务器有问题
        error: function (xhr, status, errorThrown) {
            logger.error('loadDomcument:failed');
            throw 'loadDomcument:failed';
        }
    });
    return domResult;
}

/***************************************
 *            确认对话框               *
 ***************************************/
function showConfirmDialog(message, action, title, icon) {

    // 处理参数的默认值
    message = message || '请确认';
    action = action || function () {
    };
    icon = icon || 'glyphicon-exclamation-sign';
    title = title || '请确认';

    // 尝试寻找对话框如果不存在则动态加载
    dialogDomId = '#confirmDialog';
    if ($(dialogDomId).length == 0) {
        logger.debug('showConfirmDialog:加载对话框')
        domResult = loadDomcument('/www/dialog/confirmDialog');
        $('body').append(domResult);
    }
    // 如果找不到需要自动加载(暂缺)
    dialog = $(dialogDomId);
    button = dialog.find('#confirmButton');
    // 生成对话框标题
    formation = '<span class="glyphicon %s"></span> %s';
    titleContent = sprintf(formation, icon, title);
    dialog.find('#title').html(titleContent);

    // 生成提示内容
    dialog.find('#content').html(message);

    // 将确认后要做的动作绑定到确认按钮上
    button.unbind('click');
    button.on('click', function () {
        button.attr('disabled', true);
        action();
        button.attr('disabled', false);
        dialog.modal('hide');
    });

    //  显示对话框
    dialog.modal('show');
}




