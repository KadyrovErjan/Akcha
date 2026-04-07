// AkchaAI — Dashboard Charts

const CAT_COLORS = {
  food:       '#ff8a3d',
  transport:  '#4d9fff',
  fun:        '#a57bff',
  education:  '#2ee8b6',
  other:      '#555d76',
};

const keys    = Object.keys(categoryData);
const labels  = keys.map(k => categoryData[k].label);
const amounts = keys.map(k => parseFloat(categoryData[k].amount));
const colors  = keys.map(k => CAT_COLORS[k] || '#8890a8');

const canvas = document.getElementById('categoryChart');
if (canvas && amounts.some(a => a > 0)) {
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: amounts,
        backgroundColor: colors,
        borderColor: '#13161e',
        borderWidth: 3,
        hoverOffset: 6,
      }]
    },
    options: {
      cutout: '70%',
      plugins: { legend: { display: false }, tooltip: {
        callbacks: {
          label: ctx => ` ${ctx.label}: ${ctx.parsed.toLocaleString('ru')} сом`
        }
      }},
    }
  });
} else if (canvas) {
  // empty state — draw grey ring
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      datasets: [{ data: [1], backgroundColor: ['#1a1e2a'], borderWidth: 0 }]
    },
    options: { cutout: '70%', plugins: { legend: { display: false }, tooltip: { enabled: false } } }
  });
}