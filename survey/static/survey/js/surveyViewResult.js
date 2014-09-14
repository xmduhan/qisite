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
 *          展现一个饼图               *
 ***************************************/

function renderPieChart(chartId) {
    data = eval($("#" + chartId).data('chart-data'));
    jQuery.jqplot(chartId, [data], pieOpition);
}

/***************************************
 *          展现所有的图表             *
 ***************************************/

function renderAllChart() {
    $(".jqplot-target").each(function () {
        renderPieChart($(this).attr('id'));
    })
}

/***************************************
 *          全局初始化函数             *
 ***************************************/
$(document).ready(function () {
    renderAllChart();
});