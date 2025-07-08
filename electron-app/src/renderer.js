import { apiClient } from "./modules/api-client.js";
import { themeManager } from "./modules/theme-manager.js";
import { uiManager } from "./modules/ui-manager.js";

// Função principal que só é chamada quando o HTML está 100% pronto.
const startApp = async () => {
  console.log("DOM Loaded. Initializing app...");

  // 1. Inicializa todos os módulos
  uiManager.init();
  await themeManager.init();

  // Confirma no log que os módulos iniciaram
  uiManager.log("Módulos de UI e Tema iniciados.");

  // 2. Conecta todos os event listeners aos seus elementos

  // Navegação da Sidebar
  uiManager.elements.navTranslateBtn.addEventListener("click", () =>
    uiManager.switchView("translation")
  );
  uiManager.elements.navSettingsBtn.addEventListener("click", () =>
    uiManager.switchView("settings")
  );

  // Botão de Ação Principal
  uiManager.elements.actionTranslateBtn.addEventListener("click", async () => {
    const options = uiManager.getCurrentOptions();
    uiManager.log(
      `Iniciando tradução... [Modo: ${options.outputMode}, Tema: ${options.styleKey}]`
    );
    uiManager.setLoadingState(true);
    try {
      const data = await apiClient.translateArea(options);
      if (data.error) throw new Error(data.error);
      uiManager.updateResultPanels(data);
      (data.logs || []).forEach((log) => uiManager.log(log, "success"));
    } catch (error) {
      uiManager.log(`ERRO: ${error.message}`, "error");
      uiManager.updateResultPanels({
        original_text: "Falha na tradução.",
        translated_text: "",
      });
    }
  });

  // Seletor de Tema
  uiManager.elements.themeSelect.addEventListener("change", () =>
    themeManager.apply(uiManager.elements.themeSelect.value)
  );

  // 3. Define o estado inicial da UI
  uiManager.log("Aplicação pronta.");
  uiManager.switchView("translation"); // Mostra a tela de tradução por padrão
};

// Ponto de entrada do script: espera o evento DOMContentLoaded
document.addEventListener("DOMContentLoaded", startApp);
