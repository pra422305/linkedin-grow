function makeChart(id, config) {
  const element = document.getElementById(id);
  if (!element) return;
  new Chart(element, config);
}

function groupedTotals(points, keyField, valueField) {
  const totals = {};
  points.forEach((row) => {
    const key = row[keyField] || "Unknown";
    totals[key] = (totals[key] || 0) + (row[valueField] || 0);
  });
  return totals;
}

const analyticsPayload = window.linkGrowChartData || {};
const analyticsPoints = analyticsPayload.points || [];
if (analyticsPoints.length) {
  makeChart("engagementChart", {
    type: "line",
    data: {
      labels: analyticsPoints.map((row) => row.date),
      datasets: [
        {
          label: "Engagement rate",
          data: analyticsPoints.map((row) => row.rate || 0),
          borderColor: "#6f4df6",
          backgroundColor: "rgba(111,77,246,0.12)",
          fill: true,
          tension: 0.35,
        },
      ],
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } },
  });

  makeChart("impressionsLikesChart", {
    type: "bar",
    data: {
      labels: analyticsPoints.map((row) => row.date),
      datasets: [
        { label: "Impressions", data: analyticsPoints.map((row) => row.impressions), backgroundColor: "#6f4df6" },
        { label: "Likes", data: analyticsPoints.map((row) => row.reactions), backgroundColor: "#12d6a0" },
      ],
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } },
  });

  const topicTotals = groupedTotals(analyticsPoints, "topic", "interactions");
  makeChart("topicChart", {
    type: "doughnut",
    data: {
      labels: Object.keys(topicTotals),
      datasets: [{ data: Object.values(topicTotals), backgroundColor: ["#6f4df6", "#12d6a0", "#ff6f91", "#ffc857", "#3fb8af"] }],
    },
    options: { responsive: true },
  });

  const formatTotals = groupedTotals(analyticsPoints, "format", "impressions");
  makeChart("formatChart", {
    type: "bar",
    data: {
      labels: Object.keys(formatTotals),
      datasets: [{ label: "Impressions", data: Object.values(formatTotals), backgroundColor: "#45b49d" }],
    },
    options: { responsive: true, indexAxis: "y", scales: { x: { beginAtZero: true } } },
  });
}

const dashboardPoints = window.linkGrowDashboardData || [];
if (dashboardPoints.length) {
  const labels = dashboardPoints.map((row) => row.date);
  makeChart("dashboardVisitorChart", {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Impressions", data: dashboardPoints.map((row) => row.impressions), borderColor: "#6f4df6", tension: 0.38 },
        { label: "Likes", data: dashboardPoints.map((row) => row.reactions), borderColor: "#12d6a0", tension: 0.38 },
        { label: "Comments", data: dashboardPoints.map((row) => row.comments), borderColor: "#f26d75", tension: 0.38 },
      ],
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } },
  });

  makeChart("dashboardImpressionChart", {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Last Post", data: dashboardPoints.map((row) => row.impressions), borderColor: "#6f4df6", backgroundColor: "rgba(111,77,246,.12)", fill: true, tension: 0.35 },
        { label: "New Post", data: dashboardPoints.map((row) => row.reactions * 10), borderColor: "#12d6a0", backgroundColor: "rgba(18,214,160,.12)", fill: true, tension: 0.35 },
      ],
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } },
  });

  makeChart("dashboardBarsChart", {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Impressions", data: dashboardPoints.map((row) => row.impressions), backgroundColor: "#6f4df6" },
        { label: "Likes", data: dashboardPoints.map((row) => row.reactions), backgroundColor: "#12d6a0" },
      ],
    },
    options: { responsive: true, scales: { x: { stacked: true }, y: { beginAtZero: true, stacked: true } } },
  });

  makeChart("dashboardTargetChart", {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Reality", data: dashboardPoints.map((row) => row.impressions), backgroundColor: "#45b49d" },
        { label: "Target", data: dashboardPoints.map((row) => Math.max(row.impressions * 1.25, 20)), backgroundColor: "#6f4df6" },
      ],
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } },
  });
}
