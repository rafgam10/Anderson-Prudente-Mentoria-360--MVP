// static/js/modal-functions.js

// Funções globais para modais
function abrirModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }
}

function fecharModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden");
    document.body.style.overflow = "auto";
  }
}

// Configurar fechamento ao clicar fora e com ESC
document.addEventListener("DOMContentLoaded", function () {
  // Fechar ao clicar fora
  document.querySelectorAll('[id^="modal-"]').forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === this) {
        fecharModal(this.id);
      }
    });
  });

  // Fechar com ESC
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll('[id^="modal-"]').forEach((modal) => {
        if (!modal.classList.contains("hidden")) {
          fecharModal(modal.id);
        }
      });
    }
  });
});
