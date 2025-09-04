document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".qtd-agen").forEach(el => {
        let percent = el.getAttribute("data-percent") || 0;

        el.addEventListener("mouseover", () => {
            el.style.setProperty("--bar-width", percent + "%");
        });

        el.addEventListener("mouseleave", () => {
            el.style.setProperty("--bar-width", "0%");
        });
    });
});
