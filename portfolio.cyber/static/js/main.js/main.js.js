document.addEventListener("DOMContentLoaded", () => {
    // Efeito de Revelação (Scroll Animation) para alto desempenho no Front-end
    const observerOptions = {
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
            }
        });
    }, observerOptions);

    document.querySelectorAll(".cyber-section").forEach(section => {
        observer.observe(section);
    });

    // Efeito Typing (Datilografia) para o título principal
    const heroTitle = document.getElementById("typing-effect");
    if(heroTitle) {
        const text = "Mateus Antonio | Full Stack & Cybersecurity";
        let index = 0;
        function typeText() {
            if (index < text.length) {
                heroTitle.innerHTML += text.charAt(index);
                index++;
                setTimeout(typeText, 70);
            }
        }
        typeText();
    }
});