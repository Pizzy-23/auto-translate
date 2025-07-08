export const uiManager = {
  elements: {}, // Será preenchido pelo init()

  init() {
    this.elements = {
      originalTextArea: document.getElementById("original-text"),
      translatedTextArea: document.getElementById("translated-text"),
      logsDiv: document.getElementById("logs-div"),
      themeSelect: document.getElementById("theme-select"),
      views: document.querySelectorAll(".view"),
      navTranslateBtn: document.getElementById("nav-translate"),
      navSettingsBtn: document.getElementById("nav-settings"),
      actionTranslateBtn: document.getElementById("action-translate-area"),
      sidebarButtons: document.querySelectorAll(".sidebar-btn"),
      toggleOriginal: document.getElementById("toggle-original-text"),
      toggleTranslated: document.getElementById("toggle-translated-text"),
      toggleDebugger: document.getElementById("toggle-debugger"),
      debuggerSection: document.getElementById("debugger-section"),
      resultContainer: document.querySelector(".result-container"),
    };
    this.addEventListeners();
  },

  addEventListeners() {
    this.elements.toggleOriginal.addEventListener("change", (e) =>
      this.updateResultLayout()
    );
    this.elements.toggleTranslated.addEventListener("change", (e) =>
      this.updateResultLayout()
    );
    this.elements.toggleDebugger.addEventListener("change", (e) => {
      this.elements.debuggerSection.classList.toggle(
        "hidden",
        !e.target.checked
      );
    });
  },

  log(message, type = "info") {
    if (!this.elements.logsDiv) return;
    const p = document.createElement("p");
    p.textContent = `> ${message}`;
    p.className = `log-${type}`;
    this.elements.logsDiv.appendChild(p);
    this.elements.logsDiv.scrollTop = this.elements.logsDiv.scrollHeight;
  },

  updateResultPanels({ original_text, translated_text }) {
    this.elements.originalTextArea.value = original_text || "";
    this.elements.translatedTextArea.value = translated_text || "";
  },

  updateResultLayout() {
    const showOriginal = this.elements.toggleOriginal.checked;
    const showTranslated = this.elements.toggleTranslated.checked;
    this.elements.originalTextArea.classList.toggle("hidden", !showOriginal);
    this.elements.translatedTextArea.classList.toggle(
      "hidden",
      !showTranslated
    );

    this.elements.resultContainer.classList.toggle(
      "two-columns",
      showOriginal && showTranslated
    );
  },

  switchView(viewId) {
    this.elements.views.forEach((view) => {
      view.style.display = view.id === `${viewId}-view` ? "flex" : "none";
    });
    this.elements.sidebarButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.id === `nav-${viewId}`);
    });
  },

  getCurrentOptions() {
    return {
      outputMode: document.querySelector('input[name="output-mode"]:checked')
        .value,
      styleKey: this.elements.themeSelect.value,
    };
  },

  setLoadingState(isLoading) {
    this.elements.originalTextArea.value = isLoading ? "Processando..." : "";
    this.elements.translatedTextArea.value = isLoading ? "Aguardando..." : "";
  },
};
