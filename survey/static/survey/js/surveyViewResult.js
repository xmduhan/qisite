/***************************************
 *          饼图的参数定义             *
 ***************************************/
pieOpition = {
    seriesDefaults: {
        // Make this a pie chart.
        renderer: jQuery.jqplot.PieRenderer,
        rendererOptions: {
            // Put data labels on the pie slices.
            // By default, labels show the percentage of the slice.
            showDataLabels: true
        }
    },
    legend: { show: true, location: 'e' },
    grid: {shadow: false, borderWidth: 0}
}

/***************************************
 *          柱状图的参数定义           *
 ***************************************/
barOpition = {
    seriesDefaults: {
        // Make this a pie chart.
        renderer: jQuery.jqplot.PieRenderer,
        rendererOptions: {
            // Put data labels on the pie slices.
            // By default, labels show the percentage of the slice.
            showDataLabels: true
        }
    },
    legend: { show: true, location: 'e' },
    grid: {shadow: false, borderWidth: 0}
}
/***************************************
 *          展现一个饼图               *
 ***************************************/

function renderPieChart(chartId) {
    data = eval($("#" + chartId).data('chart-data'));
    jQuery.jqplot(chartId, [data], pieOpition);
}

/***************************************
 *          展现一个柱状图             *
 ***************************************/

function renderBarChart(chartId) {
    data = eval($("#" + chartId).data('chart-data'));
    jQuery.jqplot(chartId, [data], barOpition);
}

/***************************************
 *          展现所有的图表             *
 ***************************************/

function renderAllChart() {

    $(".jqplot-pie-chart").each(function () {
        renderPieChart($(this).attr('id'));
    })

    //$(".jqplot-bar-chart").each(function () {
    //    renderBarChart($(this).attr('id'));
    //})

}

/***************************************
 *          全局初始化函数             *
 ***************************************/

function test01(){
    $.jqplot.config.enablePlugins = true;
    var s1 = [2, 6, 7, 10];
    var ticks = ['a', 'b', 'c', 'd'];

    plot1 = $.jqplot('chart3', [s1], {
        animate: false,
        seriesDefaults:{
            renderer:$.jqplot.BarRenderer,
            pointLabels: { show: true }
        },
        axes: {
            xaxis: {
                renderer: $.jqplot.CategoryAxisRenderer,
                ticks: ticks
            }
        },
        highlighter: { show: false }
    });

}



$(document).ready(function () {
    renderAllChart();
    //test01();
});
