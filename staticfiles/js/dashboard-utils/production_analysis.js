function renderProductionCostAnalysis(rawData) {
  var data = JSON.parse(`${rawData}`);
  new ApexCharts(document.querySelector("#productionCostOverTime"), {
    chart: {
      type: "area",
      height: "350",
    },
    series: [
      {
        type: "area",
        data: data.y,
      },
    ],
    xaxis: {
      type: "datetime",
      categories: data.x,
    },
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
    },
    title: {
      text: "Production",
      margin: 20,
      style: {
        fontWeight: "600",
        fontSize: "16",
      },
    },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    dataLabels: {
      enabled: false,
    },
    yaxis: {
      show: true,
      labels: {
        formatter: function (value) {
          return Math.floor(value);
        },
      },
    },
    grid: {
      show: false,
    },
  }).render();
}
