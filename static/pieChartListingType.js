function makePieChartListingType (data) {
    var pieChartListingTypeChart = AmCharts.makeChart("pieChartListingType", {
        "type": "pie",
        "theme": "light",
        "color":"#e9ecef",
        "dataProvider": data,
        "valueField": "Count",
        "labelTickColor":"#e9ecef",
        "legend" : {
          "color" : "#e9ecef",
          "position" : "right",
          "mariginRight": 150,
          "autoMarigins" : false
        },
        "titleField": "Type",
        "titles": [
            {
                "text": "Listing Types",
                "size" : 25
            }
        ],
    });
}
