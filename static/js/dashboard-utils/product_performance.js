function renderTopGrossing(rawData) {
  var data = JSON.parse(`${rawData}`);
  new ApexCharts(document.querySelector("#topGrossing"), {
    chart: {
      type: "bar",
      height: "350",
    },
    series: [
      {
        type: "bar",
        data: data.y,
      },
    ],
    xaxis: {
      //   type: "datetime",
      categories: data.x,
      labels: {
        show: true,
      },
    },
    colors: ["#1F8537"],
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
    },
    title: {
      text: "Top Grossing Products",
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
    responsive: [
      {
        breakpoint: 540,
        options: {
          xaxis: {
            labels: {
              show: false,
            },
          },
          tooltip: {
            enabled: true,
            x: {
              show: true,
              formatter: undefined,
            },
          },
        },
      },
    ],
  }).render();
}
function renderTrendingProducts(rawData) {
  var data = JSON.parse(`${rawData}`);
  new ApexCharts(document.querySelector("#trendingProducts"), {
    chart: {
      type: "donut",
      height: "350",
    },
    // series: [4, 4, 4, 4, 4],
    // labels: ["1", "2", "3", "4", "5"],
    series: data.y,
    labels: data.x,
    colors: ["#F0512C", "#EF3859", "#6FBFE8", "#F1932D", "#89CA46"],
    legend: {
      show: true,
      position: "top",
      horizontalAlign: "left",
    },
    title: {
      text: "Trending Products",
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
    plotOptions: {
      pie: {
        donut: {
          size: "45%",
        },
      },
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
    responsive: [
      {
        breakpoint: 540,
        options: {
          tooltip: {
            enabled: true,
            x: {
              show: true,
              formatter: undefined,
            },
          },
        },
      },
    ],
  }).render();
}
