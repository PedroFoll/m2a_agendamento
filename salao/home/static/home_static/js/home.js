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

    document.addEventListener("DOMContentLoaded", () => {
    const listItems = document.querySelectorAll(".qtd-agen[data-percent]");
    let labels = [];
    let data = [];

    listItems.forEach(item => {
        const nomeDoServico = item.dataset.servicoNome;
        let percent = item.getAttribute("data-percent");

        // Converte o percentual para um número para o gráfico
        // E remove o "%" caso ele venha do backend
        percent = parseFloat(percent.replace('%', '')); 

        labels.push(nomeDoServico);
        data.push(percent);

        // Para a barra de progresso (seu código original)
        item.style.setProperty("--bar-width", `${percent}%`); 
    });


    
    // AQUI É O AJUSTE PRINCIPAL: Use .getContext("2d")
    const ctx1 = document.getElementById("servicosChart").getContext("2d");

    new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: labels, // Array de nomes de serviços
            datasets: [{
                data: data, // Array de percentuais (agora como números)
                backgroundColor: [
                    '#4caf50', 
                    '#2196f3', 
                    '#ff9800', 
                    '#e91e63', 
                    '#9c27b0', 
                    '#673ab7', 
                    '#00bcd4',
                    '#8bc34a',
                    '#ff00ccff',
                ] 
                // Adicione mais cores se tiver mais de 4 serviços
            }]
        },
        options: {
            responsive: true, // Torna o gráfico responsivo
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Distribuição de Serviços'
                }
            }
        }
    });
});
