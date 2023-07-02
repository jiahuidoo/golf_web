var ctx = document.getElementById('myChart').getContext('2d');

debugger
// Retrieve email id from element with id 'myChart'
var email_id = $("#myChart").attr("email_id")

$.ajax({
  url:"/chart",
  type:"POST",
  contentType: 'application/json;charset=UTF-8',
  data: JSON.stringify({'email_id':  email_id}),
  error: function() {
      alert("Error");
  },
  success: function(data) {

    var chartDim = {};
      
    var chartDim = data.chartDim; 
    // var xLabels = data.labels;

    debugger
    var vLabels = []; 
    var vData = [];

    for (const [key, values] of Object.entries(chartDim)) {
      vLabels.push(key);
      let xy = [];
      for (let i = 0; i < values.length; i++) {
        debugger
        let d = new Date(values[i][0]);
        let year = d.getFullYear();
        let month = ('' + (d.getMonth()+1)).padStart(2, '0');
        let day = ('' + d.getDate()).padStart(2, '0');
        let hour = ('' + d.getHours()).padStart(2, '0');
        let mins = ('' + d.getMinutes()).padStart(2, '0');
        aDateTime = year + '-' + month + '-' + day + ' ' + hour + ':' + mins
        xy.push({'x': aDateTime, 'y': values[i][1]});
      }
      vData.push(xy);
    }

    debugger

    var myChart = new Chart(ctx, {
      data: {
      // labels: xLabels,
      datasets: []
      },
      options: {
          responsive: true,
          maintainaspectratio: false,
        scales: {
          x: {
            type: 'time',
            time: {
              // parser: 'MM/DD/YYYY HH:mm',
              parser: 'yyyy-MM-dd HH:mm',
            },
            scaleLabel: {
              display: true,
              labelString: 'Date'
            }
          },
          y: {
            scaleLabel: {
              display: true,
              labelString: 'value'
            }
          }
        }
      }
    });

    debugger
    
    for (i= 0; i < vLabels.length; i++ ) {
      myChart.data.datasets.push({
      label: vLabels[i],
      type: "line",
      borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
      backgroundColor: "rgba(249, 238, 236, 0.74)",
      data: vData[i],
      spanGaps: true
      });
      myChart.update();
    }
}
})

