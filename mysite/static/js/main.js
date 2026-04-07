// AkchaAI — Main JS

// Burger menu toggle
const burger = document.getElementById('burgerBtn');
const sidebar = document.getElementById('sidebar');
if (burger && sidebar) {
  burger.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!sidebar.contains(e.target) && !burger.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// Auto-dismiss alerts
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity .4s ease';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 400);
  }, 4000);
});