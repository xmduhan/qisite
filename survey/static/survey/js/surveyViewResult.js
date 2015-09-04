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
    //jQuery.jqplot(chartId, [data], pieOpition);
    $.jqplot(chartId, [data], {
        grid: {shadow: false, borderWidth: 0},
        seriesDefaults:{
            renderer:$.jqplot.PieRenderer,
            trendline:{ show:false },
            rendererOptions: { padding: 8, showDataLabels: true }
        },
        legend:{
            show:true,
            placement: 'outside',
            rendererOptions: {
                numberRows: 1
            },
            location:'s',
            marginTop: '15px'
        }
    });
}

/***************************************
 *          展现一个柱状图             *
 ***************************************/

function renderBarChart(chartId) {
    data = eval($("#" + chartId).data('chart-data'));
    //var ticks = ['a', 'b', 'c', 'd'];
    //var s1 = [2, 6, 7, 10];
    var ticks = data[0]
    var s1 = data[1]

    $.jqplot(chartId, [s1], {
        animate: false,
        seriesDefaults:{
            renderer:$.jqplot.BarRenderer,
            pointLabels: { show: true }
        },
        axes: {
            xaxis: {
                renderer: $.jqplot.CategoryAxisRenderer,
                ticks: ticks,
                tickOptions:{showGridline: false}
            },
            yaxis: {
              tickOptions:{showGridline: false}
            }
        },
        highlighter: { show: false },
        grid: {shadow: false, borderWidth: 0}
    });
}


/***************************************
 *          展现一个泡泡图             *
 ***************************************/

function renderBubbleChart(chartId){

    data = eval($("#" + chartId).data('chart-data'));
    console.log($("#" + chartId).data('chart-data'));

    attr = []
    for(i=0; i<data.length; i++) {
        x = Math.floor((Math.random() * 10 * (i+1)) + 1);
        y = Math.floor((Math.random() * 10 * (i+1)) + 1);
        attr[i] = [x,y,11-i,data[i]]
    }

    $.jqplot(chartId,[attr],{
        //title: 'Transparent Bubbles',
        seriesDefaults:{
            renderer: $.jqplot.BubbleRenderer,
            rendererOptions: {
                bubbleAlpha: 0.6,
                highlightAlpha: 0.8
            },
            shadow: true,
            shadowAlpha: 0.05
        },
        axes: {
            xaxis: {
                tickOptions:{showGridline: false, show: false}
            },
            yaxis: {
                tickOptions:{showGridline: false, show: false}
            }
        },
        grid: {shadow: false, borderWidth: 0}
    });
}


/***************************************
 *          展现所有的图表             *
 ***************************************/

function renderAllChart() {

    $(".jqplot-pie-chart").each(function () {
        renderPieChart($(this).attr('id'));
    })

    $(".jqplot-bar-chart").each(function () {
        renderBarChart($(this).attr('id'));
    })

    $(".jqplot-bubble-chart").each(function () {
        renderBubbleChart($(this).attr('id'));
    })

}

/***************************************
 *          全局初始化函数             *
 ***************************************/

$(document).ready(function () {
    $.jqplot.config.enablePlugins = true;
    renderAllChart();
});
