import { apiClient } from "./modules/api-client.js";
import { themeManager } from "./modules/theme-manager.js";
import { uiManager } from "./modules/ui-manager.js";

(async function main() {
  await new Promise((resolve) =>
    document.addEventListener("DOMContentLoaded", resolve)
  );

  try {
    uiManager.init();
    await themeManager.init(uiManager);

    let isRealtimeActive = false;

    // --- Conecta ao WebSocket ---
    function connectWebSocket() {
      const ws = new WebSocket("ws://127.0.0.1:5000/ws-updates");
      ws.onopen = () =>
        uiManager.log("Conectado para atualizações em tempo real.", "success");
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        uiManager.log("Nova tradução recebida em tempo real.");
        uiManager.updateResultPanels(data);
      };
      ws.onclose = () => {
        uiManager.log(
          "Conexão de tempo real perdida. Reconectando...",
          "error"
        );
        setTimeout(connectWebSocket, 3000);
      };
      ws.onerror = (err) => console.error("WebSocket Error:", err);
    }
    connectWebSocket(); // Inicia a conexão

    // --- Event Listeners ---
    uiManager.elements.actionTranslateBtn.addEventListener(
      "click",
      async () => {
        const options = uiManager.getCurrentOptions();

        if (options.translationMode === "single") {
          uiManager.setLoadingState(true);
          const data = await apiClient.translateOnce(options);
          uiManager.setLoadingState(false);
          if (data.error) return uiManager.log(`ERRO: ${data.error}`, "error");
          uiManager.updateResultPanels(data);
          uiManager.log("Tradução única concluída.", "success");
        } else {
          if (isRealtimeActive) {
            const data = await apiClient.stopRealtime();
            isRealtimeActive = false;
          } else {
            const data = await apiClient.startRealtime(options);
            if (data.error)
              return uiManager.log(`ERRO: ${data.error}`, "error");
            isRealtimeActive = true;
          }
          uiManager.setButtonState(isRealtimeActive);
          uiManager.log(data.logs.join("\n"));
        }
      }
    );

    // O resto é igual
    themeManager.selectElement.addEventListener("change", () =>
      themeManager.apply(themeManager.selectElement.value)
    );
    uiManager.elements.navTranslateBtn.addEventListener("click", () =>
      uiManager.switchView("translation-view")
    );
    uiManager.elements.navSettingsBtn.addEventListener("click", () =>
      uiManager.switchView("settings-view")
    );
    uiManager.switchView("translation-view");
    uiManager.log("Aplicação pronta.");
  } catch (err) {
    console.error("ERRO CRÍTICO:", err);
  }
})();
