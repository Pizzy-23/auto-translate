export const uiManager = {
  elements: {},

  init() {
    this.elements = {
      originalTextArea: document.getElementById("original-text"),
      translatedTextArea: document.getElementById("translated-text"),
      logsDiv: document.getElementById("logs-div"),
      themeSelect: document.getElementById("theme-select"),
      views: document.querySelectorAll(".view"),
      navTranslateBtn: document.getElementById("nav-translation-btn"),
      navSettingsBtn: document.getElementById("nav-settings-btn"),
      actionTranslateBtn: document.getElementById("action-translate-btn"),
    };
    for (const key in this.elements) {
      if (!this.elements[key])
        throw new Error(`[UI Manager] Elemento não encontrado: #${key}`);
    }
  },

  switchView(viewId) {
    this.elements.views.forEach((view) => (view.style.display = "none"));
    document.getElementById(viewId).style.display = "flex";

    document.querySelectorAll(".sidebar-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.id === `nav-${viewId}-btn`);
    });
  },

  updateResultPanels({ original_text, translated_text }) {
    if (original_text !== undefined)
      this.elements.originalTextArea.value = original_text;
    if (translated_text !== undefined)
      this.elements.translatedTextArea.value = translated_text;
  },

  getCurrentOptions() {
    return {
      translationMode: document.querySelector(
        'input[name="translation-mode"]:checked'
      ).value,
      outputMode: document.querySelector('input[name="output-mode"]:checked')
        .value,
      styleKey: this.elements.themeSelect.value,
    };
  },

  setButtonState(isRealtime) {
    const btn = this.elements.actionTranslateBtn;
    btn.disabled = false;
    btn.textContent = isRealtime
      ? "Parar Tradução em Tempo Real"
      : "Iniciar Tradução";
    btn.classList.toggle("stop-btn", isRealtime);
  },

  setLoadingState(isLoading) {
    const btn = this.elements.actionTranslateBtn;
    btn.disabled = isLoading;
    if (isLoading) {
      btn.textContent = "Processando...";
      this.updateResultPanels({
        original_text: "Aguardando seleção...",
        translated_text: "",
      });
    } else {
      this.setButtonState(false);
    }
  },

  log(message, type = "info") {
    const p = document.createElement("p");
    p.textContent = `> ${message}`;
    p.className = `log-${type}`;
    this.elements.logsDiv.appendChild(p);
    this.elements.logsDiv.scrollTop = this.elements.logsDiv.scrollHeight;
  },
};
