$(function () {
    $(document).ready(function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        var chartOptions = {
            chart: {
                zoomType: "x",
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];
                        console.log(series);
                        setInterval(function () {
                            $.ajax({
                                url: '/incident_data/',
                                method: "POST"
                            }).done(function(data) {
                                var list = $.parseJSON(data);
                                if (list.length > series.length) {
                                    var x, y;
                                    for (var i = 0; i < list.length; i++) {
                                        x = (new Date(list[i][0])).getTime();
                                        y = list[i][1];
                                        chartOptions.series[0].data.push({x: x, y: y});
                                    }

                                    Highcharts.chart('analytics_container', chartOptions);
                                }
                            });
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Incidents Reported'
            },
            xAxis: {
                title: {
                    text: 'Time of Day'
                },
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Number of Incidents'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Incidents',
                data: []
            }]
        };

        $.ajax({
            url: '/incident_data/',
            method: "POST"
        }).done(function(data) {
            var list = $.parseJSON(data);
            var x, y;
            for (var i = 0; i < list.length; i++) {
                x = (new Date(list[i][0])).getTime();
                y = list[i][1];
                chartOptions.series[0].data.push({x: x, y: y});
            }

            Highcharts.chart('analytics_container', chartOptions);
        });
    });
});