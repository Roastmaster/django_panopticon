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
                                method: "POST",
                                data: "timespan=instant"
                            }).done(function(data) {
                                var list = $.parseJSON(data);
                                var x = (new Date(list[0])).getTime();
                                var y = list[1];
                                series.addPoint([x,y], true, false, false);
                                console.log(data);
                            });
                        }, 1000 * 60 * 60);
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
            method: "POST",
            data: "timespan=day"
        }).done(function(data) {
            console.log(data);
            console.log("ANYTHING");
            var list = $.parseJSON(data);
            console.log("HELLO");
            console.log(list[0]);
            var x, y;
            for (var i = 0; i < list.length; i++) {
                x = (new Date(list[i][0])).getTime();
                y = list[i][1];
                chartOptions.series[0].data.push({x: x, y: y});
            }

            Highcharts.chart('analytics_container', chartOptions);
        });

        // var real_time = new Highcharts.Chart({
        //     chart: {
        //         renderTo: "analytics_container",
        //         zoomType: "x",
        //         type: 'spline',
        //         animation: Highcharts.svg, // don't animate in old IE
        //         marginRight: 10,
        //         events: {
        //             load: function () {
        //
        //                 // set up the updating of the chart each second
        //                 var series = this.series[0];
        //                 console.log(series);
        //                 setInterval(function () {
        //                     $.ajax({
        //                         url: '/incident_data/',
        //                         method: "POST",
        //                         data: "timespan=instant"
        //                     }).done(function(data) {
        //                         var list = $.parseJSON(data);
        //                         var x = (new Date(list[0])).getTime();
        //                         var y = list[1];
        //                         series.addPoint([x,y], true, false, false);
        //                         console.log(data);
        //                     });
        //                 }, 5000);
        //             }
        //         }
        //     },
        //     title: {
        //         text: 'Live random data'
        //     },
        //     xAxis: {
        //         type: 'datetime',
        //         tickPixelInterval: 150
        //     },
        //     yAxis: {
        //         title: {
        //             text: 'Value'
        //         },
        //         plotLines: [{
        //             value: 0,
        //             width: 1,
        //             color: '#808080'
        //         }]
        //     },
        //     tooltip: {
        //         formatter: function () {
        //             return '<b>' + this.series.name + '</b><br/>' +
        //                 Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
        //                 Highcharts.numberFormat(this.y, 2);
        //         }
        //     },
        //     legend: {
        //         enabled: false
        //     },
        //     exporting: {
        //         enabled: false
        //     },
        //     series: [{
        //         name: 'Incidents',
        //         data: []
        //     }]
        // });
        //
        // $.ajax({
        //     url: '/incident_data/',
        //     method: "POST",
        //     data: "timespan=day"
        // }).done(function (data) {
        //     var list = $.parseJSON(data);
        //     var chartData = [];
        //     real_time.options.series[0].data = [];
        //     for (var i = 0; i < list.length; i++) {
        //         var x = (new Date(list[i][0])).getTime();
        //         var y = list[i][1];
        //         chartData.push({x: x, y: y});
        //     }
        //
        //     real_time.addSeries({
        //         name: 'Incidents',
        //         data: chartData
        //     });
        // });
    });
});