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

function Logger() {
    this.logger = console;
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