document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('input[name="servico"]');
    const totalInput = document.getElementById('total_servicos');

    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            let total = 0;
            checkboxes.forEach(item => {
                if (item.checked) {
                    // Extrai o preço que está ao lado do checkbox
                    const precoEl = item.closest('.descricao').querySelector('.preco');
                    const preco = parseFloat(precoEl.textContent.replace('R$', '').replace(',', '.'));
                    total += preco;
                }
            });
            totalInput.value = total.toFixed(2);
        });
    });

    // Quando o checkbox for alterado, exibe ou esconde o campo de quantidade
    document.querySelectorAll('.servico-checkbox').forEach(chk => {
        chk.addEventListener('change', e => {
            const id = e.target.value;
            const container = document.querySelector(`.quantidade-container[data-id="${id}"]`);
            
            // Se o checkbox for marcado, exibe o campo de quantidade
            if (e.target.checked) {
                container.style.display = 'flex';  // Ou 'inline-flex' se preferir
            } else {
                container.style.display = 'none';
            }
        });
    });

    // Função para incrementar a quantidade
    document.querySelectorAll('.btn-mais').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = document.querySelector(`input[data-id="${btn.dataset.id}"]`);
            input.value = parseInt(input.value) + 1;
        });
    });

    // Função para decrementar a quantidade
    document.querySelectorAll('.btn-menos').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = document.querySelector(`input[data-id="${btn.dataset.id}"]`);
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });
});
