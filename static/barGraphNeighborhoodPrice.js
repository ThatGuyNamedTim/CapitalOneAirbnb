function makeBarGraphNeighborhoodPriceChart (data) {
    var barGraphZipPriceChart = AmCharts.makeChart("barGraphNeighborhoodPrice", {
        "type": "serial",
        "theme": "light",
        "color": "#292b2c",
        "dataProvider": data,
        "gridAboveGraphs": true,
        "startDuration": 1,
        "orderByField" : "Cost Per Square Foot",
        "titles": [
            {
                "text": "Prices in Different Neighborhoods",
                "size" : 25
        }],

        "graphs": [{
            "balloonText": "[[category]]: $<b>[[value]]</b> Per Square Foot",
            "fillAlphas": 0.8,
            "lineAlpha": 0.2,
            "type": "column",
            "valueField": "Cost Per Square Foot",
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
            "labelRotation": 90
        },
        "export": {
            "enabled": true
        },
        "valueAxes": [
            {
                "axisColor": "#e9ecef",
                "gridColor": "#e9ecef",
                "title": "Average Price Per Square Foot (USD)"
            }
        ],

    } );
}
