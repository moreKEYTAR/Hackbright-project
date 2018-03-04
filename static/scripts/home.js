"use strict"; /*jslint node: true */

let options = { responsive: true };

// Make Donut Chart of percent of different types
let ctx_donut = $("#donut-chart-canvas").get(0).getContext("2d");

$.get("/productivity-stats.json", function (data) {
    let myDonutChart = new Chart(ctx_donut, {
                                           type: 'doughnut',
                                           data: data,
                                           options: options
                                           });
    $('#weekly-chart-legend').html(myDonutChart.generateLegend());
});
$('#carousel-lifestyle').carousel({
  interval: 3000,
  pause: null
  // or put pause: "hover"
});

// <div class="weekly-chart">
//     <canvas id="donut-chart"></canvas>
//     <div id="weekly-chart-legend" class="chart-legend">
//     </div>
//   </div> 


