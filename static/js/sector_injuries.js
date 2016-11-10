/**
 * Created by vargaj94 on 11/4/16.
 */
var chartObj;

$.ajax({
    url: "../incident_data/injuries_per_sector/",
    method: "POST"
}).done(function(d) {
    var list = $.parseJSON(d);
    var data = {
        labels: [],
        datasets: [
            {
                label: "Number of Injuries",
                backgroundColor: "rgba(179, 181, 198, 0.2)",
                data: []
            }
        ]
    };
    console.log(list);
    for (var key in list) {
        data.labels.push(key);
        data.datasets[0].data.push(list[key]);
    }

    var ctx = document.getElementById("sector_injuries");
    chartObj = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            scale: {
                reverse: true,
                ticks: {
                    beginAtZero: true
                }
            }
        }
    });
});

setInterval(function() {
    $.ajax({
        url: "../incident_data/injuries_per_sector/",
        method: "POST"
    }).done(function(d) {
        var list = $.parseJSON(d);
        var i = 0;
        for (var key in list) {
            for (var j = 0; j < chartObj.data.labels.length; j++) {
                if (key == chartObj.data.labels[j]) {
                    chartObj.data.datasets[0].data[j] = list[key];
                }
            }
        }
    });
}, 5000);