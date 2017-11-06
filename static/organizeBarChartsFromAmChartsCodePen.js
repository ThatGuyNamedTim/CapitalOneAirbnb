// This is from a demo for amCharts
// citation: https://codepen.io/team/amcharts/pen/cbdf6451e693c98e57255705a50229f0
AmCharts.addInitHandler( function( barGraph ) {  
    // Re-order the data provider
    barGraph.dataProvider.sort( function( a, b ) {
      if ( a[ barGraph.orderByField ] > b[ barGraph.orderByField ] ) {
        return -1;
      } else if ( a[ barGraph.orderByField ] == b[ barGraph.orderByField ] ) {
        return 0;
      }
      return 1;
    } );
  
  }, [ "serial" ] );

