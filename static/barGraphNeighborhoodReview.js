function makeBarGraphNeighborhoodReviewChart (data) {
    var barGraphZipReviewChart = AmCharts.makeChart("barGraphNeighborhoodReview", {
        "type": "serial",
        "theme": "light",
        "color":"#e9ecef",
        "dataProvider": data,
        "gridAboveGraphs": true,
        "startDuration": 1,
        "orderByField" : "Average Review",
        "titles": [
            {
                "text": "Reviews in Different Neighborhoods",
                "size" : 25
        }],
        "graphs": [{
            "balloonText": "[[category]]: <b>[[value]]</b>",
            "fillAlphas": 0.8,
            "lineAlpha": 0.2,
            "type": "column",
            "valueField": "Average Review",
        }],
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "Neighborhood",
        "categoryAxis": {
            "gridPosition": "start",
            "gridAlpha": 0,
            "tickPosition": "start",
            "tickLength": 20,
            "labelRotation": 90,
            "fontSize" : 0
        },
        "export": {
            "enabled": true
        },
        "valueAxes": [
            {
                "axisColor": "#e9ecef",
                "gridColor": "#e9ecef",
                "title": "Average Review (out of 100)"
            }
        ],
    } );

}
