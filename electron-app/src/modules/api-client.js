export const apiClient = {
  async fetchThemes() {
    const response = await fetch("http://127.0.0.1:5000/get-themes");
    return await response.json();
  },

  async translateOnce(options) {
    const response = await fetch("http://127.0.0.1:5000/translate-once", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options),
    });
    return await response.json();
  },

  async startRealtime(options) {
    const response = await fetch("http://127.0.0.1:5000/start-realtime", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options),
    });
    return await response.json();
  },

  async stopRealtime() {
    const response = await fetch("http://127.0.0.1:5000/stop-realtime", {
      method: "POST",
    });
    return await response.json();
  },
};
