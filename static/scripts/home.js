"use strict"; /*jslint node: true */


// whatever is in the parens needs to resolve to a true or false. 
    // some things resolve to a boolean, but booleans are already boolean
if (userIsLoggedIn) {
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
    let $vid = $("#blurry-work-vid");
    let $wdwWidth = $(window).width();
    $(window).on('resize', function () {
        $wdwWidth = $(window).width(); // update window height to new size
        $vid.width($wdwWidth);  
            // note it resizes the item div, to keep with the window's height not width
    });
}
// generic format:
// <div class="weekly-chart">
//     <canvas id="donut-chart"></canvas>
//     <div id="weekly-chart-legend" class="chart-legend">
//     </div>
//   </div> 


