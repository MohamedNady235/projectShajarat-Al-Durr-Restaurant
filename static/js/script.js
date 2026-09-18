document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("pageLoader");
  if (loader) {
    window.addEventListener("load", () => {
      loader.classList.add("hidden");
      setTimeout(() => loader.remove(), 500);
    });
  }

  const navbar = document.querySelector(".navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      navbar.classList.toggle("scrolled", window.scrollY > 20);
    });
  }

  const backToTopButton = document.getElementById("backToTop");
  if (backToTopButton) {
    const toggleButton = () => {
      backToTopButton.style.display = window.scrollY > 300 ? "flex" : "none";
    };
    toggleButton();
    window.addEventListener("scroll", toggleButton);
    backToTopButton.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" }),
    );
  }

  const cards = document.querySelectorAll(
    ".menu-card, .info-card, .card, .gallery-card",
  );
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 80}ms`;
    card.classList.add("animate-card");
  });
});
