export const uiManager = {
  elements: {},

  init() {
    this.elements = {
      navTranslateBtn: document.getElementById("nav-translation-btn"),
      navSettingsBtn: document.getElementById("nav-settings-btn"),
      actionTranslateBtn: document.getElementById("action-translate-btn"),
      originalColumn: document.getElementById("original-column"),
      translatedColumn: document.getElementById("translated-column"),
      originalTextArea: document.getElementById("original-text"),
      translatedTextArea: document.getElementById("translated-text"),
      resultContainer: document.querySelector(".result-container"),
      visibilityCheckboxes: document.querySelectorAll(
        '.visibility-controls input[type="checkbox"]'
      ),
      debuggerToggle: document.getElementById("debugger-toggle"),
      debuggerSection: document.getElementById("debugger-section"),
      views: document.querySelectorAll(".view"),
      themeSelect: document.getElementById("theme-select"),
      logsDiv: document.getElementById("logs-div"),
    };
    for (const key in this.elements) {
      if (
        !this.elements[key] ||
        (this.elements[key] instanceof NodeList &&
          this.elements[key].length === 0)
      ) {
        throw new Error(`[UI Manager] Elemento da UI não encontrado: '${key}'`);
      }
    }
    this.addEventListeners();
    this.updateResultLayout(); // Garante o estado inicial correto das colunas
  },

  addEventListeners() {
    this.elements.navTranslateBtn.addEventListener("click", () =>
      this.switchView("translation-view")
    );
    this.elements.navSettingsBtn.addEventListener("click", () =>
      this.switchView("settings-view")
    );

    this.elements.visibilityCheckboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", () => this.updateResultLayout());
    });

    this.elements.debuggerToggle.addEventListener("change", (e) => {
      this.elements.debuggerSection.classList.toggle(
        "hidden",
        !e.target.checked
      );
    });
  },

  updateResultLayout() {
    let visibleColumns = 0;
    this.elements.visibilityCheckboxes.forEach((checkbox) => {
      const column = document.getElementById(checkbox.dataset.target);
      if (column) {
        const shouldBeHidden = !checkbox.checked;
        column.classList.toggle("hidden", shouldBeHidden);
        if (!shouldBeHidden) visibleColumns++;
      }
    });
    this.elements.resultContainer.classList.toggle(
      "two-columns",
      visibleColumns === 2
    );
  },

  switchView(viewId) {
    this.elements.views.forEach((view) => (view.style.display = "none"));
    const viewToShow = document.getElementById(viewId);
    if (viewToShow) viewToShow.style.display = "flex";
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
    const translationMode = document.querySelector(
      'input[name="translation-mode"]:checked'
    ).value;
    const outputMode = document.querySelector(
      'input[name="output-mode"]:checked'
    ).value;
    return {
      translationMode,
      outputMode,
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
