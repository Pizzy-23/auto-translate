import { apiClient } from "./modules/api-client.js";
import { themeManager } from "./modules/theme-manager.js";
import { uiManager } from "./modules/ui-manager.js";

const main = async () => {
  await new Promise((resolve) =>
    document.addEventListener("DOMContentLoaded", resolve)
  );

  try {
    uiManager.init();
    await themeManager.init(uiManager);

    let isRealtimeActive = false;

    uiManager.elements.navTranslateBtn.addEventListener("click", () =>
      uiManager.switchView("translation-view")
    );
    uiManager.elements.navSettingsBtn.addEventListener("click", () =>
      uiManager.switchView("settings-view")
    );

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

    themeManager.selectElement.addEventListener("change", () =>
      themeManager.apply(themeManager.selectElement.value)
    );

    uiManager.switchView("translation-view");
    uiManager.log("Aplicação pronta.");
  } catch (err) {
    console.error("ERRO CRÍTICO:", err);
    const logsDiv = document.getElementById("logs-div");
    if (logsDiv)
      logsDiv.innerHTML += `<p class="log-error">> ERRO FATAL: ${err.message}.</p>`;
  }
};

main();
