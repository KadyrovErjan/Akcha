// AkchaAI — Analytics Charts

const BAR_COLORS = ['#ff8a3d','#4d9fff','#a57bff','#2ee8b6','#555d76'];

const barCanvas = document.getElementById('barChart');
if (barCanvas) {
  new Chart(barCanvas, {
    type: 'bar',
    data: {
      labels: analyticsData.labels,
      datasets: [{
        data: analyticsData.amounts,
        backgroundColor: BAR_COLORS,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.parsed.y.toLocaleString('ru')} сом`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#8890a8', font: { family: "'DM Sans'" } },
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#8890a8', font: { family: "'DM Sans'" },
            callback: v => v.toLocaleString('ru') + ' ₸'
          },
          beginAtZero: true,
        }
      }
    }
  });
}