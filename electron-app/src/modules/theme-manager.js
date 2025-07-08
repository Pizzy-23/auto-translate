import { apiClient } from "./api-client.js";

export const themeManager = {
  themes: {},
  selectElement: null,

  async init() {
    this.selectElement = document.getElementById("theme-select");
    if (!this.selectElement)
      return "ERRO: Elemento 'theme-select' não encontrado.";

    try {
      this.themes = await apiClient.fetchThemes();
      this.populateSelect();
      this.selectElement.value = "purple_dark";
      this.apply(this.selectElement.value);
      return "Temas carregados do backend.";
    } catch (error) {
      return `ERRO ao carregar temas: ${error.message}`;
    }
  },

  populateSelect() {
    this.selectElement.innerHTML = "";
    for (const key in this.themes) {
      const option = document.createElement("option");
      option.value = key;
      option.textContent = this.themes[key].name;
      this.selectElement.appendChild(option);
    }
  },

  apply(themeKey) {
    const theme = this.themes[themeKey];
    if (!theme) return;

    const root = document.documentElement;
    root.style.setProperty("--primary-bg", theme.bg);
    root.style.setProperty("--text-color", theme.fg);
    root.style.setProperty("--secondary-bg", this.adjustColor(theme.bg, 10));
    root.style.setProperty("--sidebar-bg", this.adjustColor(theme.bg, -10));
    root.style.setProperty("--border-color", this.adjustColor(theme.bg, 25));
    root.style.setProperty("--accent-color", theme.fg);
  },

  adjustColor(color, amount) {
    return (
      "#" +
      color
        .replace(/^#/, "")
        .replace(/../g, (c) =>
          (
            "0" +
            Math.min(255, Math.max(0, parseInt(c, 16) + amount)).toString(16)
          ).substr(-2)
        )
    );
  },
};
