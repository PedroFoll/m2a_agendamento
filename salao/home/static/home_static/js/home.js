document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".qtd-agen").forEach(el => {
        const percent = el.getAttribute("data-percent");
        if (percent) {
            el.style.setProperty("--bar-width", percent + "%");
            el.style.setProperty("width", percent + "%");
            el.style.setProperty("transition", "width 1.5s ease");
            el.style.setProperty("background", "rgba(100,100,255,0.2)");
        }
    });
});

    const ctx1 = document.getElementById('servicosChart');
    new Chart(ctx1, {
      type: 'pie',
      data: {
        labels: ['Corte', 'Unhas', 'Maquiagem', 'Spa'],
        datasets: [{
          data: [12, 19, 7, 5],
          backgroundColor: ['#4caf50', '#2196f3', '#ff9800', '#e91e63']
        }]
      }
    });

    const ctx2 = document.getElementById('linhaChart');
    new Chart(ctx2, {
      type: 'line',
      data: {
        labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [{
          label: 'Agendamentos',
          data: [5, 9, 12, 8, 15, 20, 7],
          borderColor: '#2196f3',
          backgroundColor: 'rgba(33,150,243,0.2)',
          fill: true,
          tension: 0.3
        }]
      }
    });