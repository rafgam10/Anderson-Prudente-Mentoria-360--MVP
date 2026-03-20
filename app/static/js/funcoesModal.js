// static/js/funcoesModal.js

// Funções globais para modais
function abrirModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
  }
}

function fecharModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden");
    
    // Só remove o overflow-hidden se não houver outros modais abertos
    const modaisAbertos = document.querySelectorAll('[id^="modal-"]:not(.hidden)');
    if (modaisAbertos.length === 0) {
      document.body.classList.remove("overflow-hidden");
    }
  }
}

// Configurar fechamento ao clicar fora e com ESC
document.addEventListener("DOMContentLoaded", function () {
  // Fechar ao clicar fora
  document.querySelectorAll('[id^="modal-"]').forEach((modal) => {
    modal.addEventListener("click", function (e) {
      // Se clicou exatamente no fundo (backdrop) e não no conteúdo
      if (e.target.id && e.target.id === this.id) {
        fecharModal(this.id);
      }
    });
  });

  // Fechar com ESC
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      const modalAtivo = Array.from(document.querySelectorAll('[id^="modal-"]'))
        .find(m => !m.classList.contains("hidden"));
      if (modalAtivo) {
        fecharModal(modalAtivo.id);
      }
    }
  });
});

/**
 * Exibe uma notificação Toast (flutuante) no canto da tela
 * @param {string} mensagem - Texto da notificação
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 * @param {number} duracao - Tempo em ms
 */
function mostrarToast(mensagem, tipo = 'info', duracao = 4000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  
  // Cores e Ícones baseados no tipo
  let bg = 'bg-[#171717]';
  let border = 'border-[#2a2a2a]';
  let icon = 'ph-info';
  let iconColor = 'text-blue-400';

  // Normalizar tipo
  const tipoStr = (tipo || 'info').toLowerCase();

  if (tipoStr.includes('success') || tipoStr.includes('sucesso')) {
    border = 'border-green-500/50';
    icon = 'ph-check-circle';
    iconColor = 'text-green-500';
  } else if (tipoStr.includes('error') || tipoStr.includes('erro')) {
    border = 'border-red-500/50';
    icon = 'ph-x-circle';
    iconColor = 'text-red-500';
  } else if (tipoStr.includes('warning')) {
    border = 'border-yellow-500/50';
    icon = 'ph-warning-circle';
    iconColor = 'text-yellow-500';
  }

  toast.className = `flex items-center gap-3 p-4 rounded-lg border ${bg} ${border} shadow-2xl pointer-events-auto transform transition-all duration-300 translate-x-full opacity-0 max-w-xs animate-toast-in`;
  toast.innerHTML = `
    <i class="ph ${icon} ${iconColor} text-2xl flex-shrink-0"></i>
    <span class="text-gray-200 text-sm font-medium">${mensagem}</span>
    <button class="toast-close ml-auto text-gray-500 hover:text-white transition-colors p-1">
      <i class="ph ph-x"></i>
    </button>
  `;

  container.appendChild(toast);

  // Função interna para remover com animação
  const fecharToast = () => {
    toast.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => { if (toast.parentElement) toast.remove(); }, 300);
  };

  // Evento do botão X
  const btnClose = toast.querySelector('.toast-close');
  if (btnClose) {
    btnClose.onclick = (e) => {
      e.stopPropagation();
      fecharToast();
    };
  }

  // Auto-remove
  setTimeout(() => {
    if (toast.parentElement) {
      fecharToast();
    }
  }, duracao);

  // Trigger animation (entrada)
  requestAnimationFrame(() => {
    toast.classList.remove('translate-x-full', 'opacity-0');
  });
}

/**
 * Exibe um aviso (Agora via Toast para não ser intrusivo)
 * @param {string} mensagem - Texto do aviso
 * @param {string} tipo - Tipo do toast
 * @param {function} callback - Função opcional após fechar
 */
function mostrarAviso(mensagem, tipo = 'info', callback = null) {
  mostrarToast(mensagem, tipo);
  if (callback) {
    // Se tiver callback, executa após um pequeno delay para o user ler o toast
    setTimeout(callback, 1000);
  }
}

/**
 * Exibe um modal de confirmação estilizado (REVERTIDO PARA CONFIRM)
 * @param {string} mensagem - Pergunta ao usuário
 * @param {function} callback - Função executada se confirmar
 * @param {string} titulo - Título do modal (não usado no confirm)
 */
function mostrarConfirmacao(mensagem, callback, titulo = 'Confirmação') {
  if (confirm(mensagem)) {
    callback();
  }
}



