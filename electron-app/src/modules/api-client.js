// Este objeto é o único lugar no app que sabe como
// falar com o servidor backend.
export const apiClient = {
  /**
   * Busca a lista de temas disponíveis do backend.
   * @returns {Promise<object>} Uma promessa que resolve para o objeto de temas.
   */
  async fetchThemes() {
    try {
      const response = await fetch("http://127.0.0.1:5000/get-themes");
      if (!response.ok) {
        // Se a resposta não for OK (ex: erro 500, 404), lança um erro.
        throw new Error(
          `Erro de rede: ${response.status} ${response.statusText}`
        );
      }
      return await response.json();
    } catch (error) {
      console.error("API_CLIENT_ERROR (fetchThemes):", error);
      // Re-lança o erro para que o chamador (theme-manager) possa tratá-lo.
      throw error;
    }
  },

  /**
   * Envia um pedido para traduzir uma área selecionada da tela.
   * @param {object} options - As opções da tradução.
   * @param {string} options.outputMode - 'app' ou 'overlay'.
   * @param {string} options.styleKey - A chave do tema (ex: 'dark', 'purple_dark').
   * @returns {Promise<object>} Uma promessa que resolve para o resultado da tradução.
   */
  async translateArea(options) {
    try {
      const response = await fetch("http://127.0.0.1:5000/translate-area", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          output_mode: options.outputMode,
          style_key: options.styleKey,
          source_lang: "Inglês", // Fixo por enquanto
          target_lang: "Português",
        }),
      });

      if (!response.ok) {
        throw new Error(
          `Erro de rede: ${response.status} ${response.statusText}`
        );
      }
      return await response.json();
    } catch (error) {
      console.error("API_CLIENT_ERROR (translateArea):", error);
      throw error;
    }
  },
};
