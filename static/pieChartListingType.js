function makePieChartListingType (data) {
    var pieChartListingTypeChart = AmCharts.makeChart("pieChartListingType", {
        "type": "pie",
        "theme": "light",
        "color":"#292b2c",
        "dataProvider": data,
        "valueField": "Count",
        "titleField": "Type",
        "titles": [
            {
                "text": "Listing Types",
                "size" : 25
            }
        ],    
    });
}
   
