# Live Screen Translator

 <!-- Sugestão: Tire um screenshot do seu app e substitua este link -->

A powerful, real-time screen translation application built with a modern Python backend and an Electron.js frontend. This tool allows users to select any portion of their screen, automatically perform Optical Character Recognition (OCR) on it, and get an instant translation.

It's designed to be a versatile utility for translating text from games, images, videos, or any application where text cannot be easily copied.

## ✨ Features

- **Real-Time Area Translation:** Click a button, drag a rectangle over any part of your screen, and get an instant translation.
- **Client-Server Architecture:** Robust separation of concerns with a powerful **Python/Flask backend** for processing and a modern **Electron.js frontend** for the user interface.
- **Dual Display Mode:** Choose how to view your translation:
  - **In-App:** View original and translated text side-by-side inside the app's clean UI.
  - **Overlay Mode:** Display the translation as a floating overlay directly on top of the selected area.
- **Dynamic Theming System:**
  - The entire app interface and the translation overlay can be themed.
  - Comes with several built-in themes (Dark, Light, Gamer, Ocean, Purple Dark).
  - Themes are fetched from the backend, allowing for easy expansion.
- **Intuitive & Modern UI:**
  - A clean sidebar for navigation between translation and settings views.
  - Collapsible panels to keep the interface tidy.
  - Built-in debugger log to monitor the application's status in real-time.
- **Modular and Extensible:** The codebase is organized into logical modules for UI management, theme control, and API communication, making it easy to add new features.

## 🛠️ Built With

- **Backend:**

  - [Python](https://www.python.org/)
  - [Flask](https://flask.palletsprojects.com/) - For the local web server API.
  - [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) - The core OCR engine.
  - [Pillow](https://python-pillow.org/) - For image processing and enhancement.
  - [googletrans](https://pypi.org/project/googletrans/) - For language translation.
  - [mss](https://pypi.org/project/mss/) - For fast screen captures.

- **Frontend:**
  - [Electron.js](https://www.electronjs.org/) - To create the desktop application shell.
  - [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
  - [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
  - [JavaScript (ES Modules)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You need to have the following software installed on your system:

- **Python 3.7+**
  - Make sure `pip` is installed and accessible from your terminal.
- **Node.js and npm**
  - Download and install the LTS version from [nodejs.org](https://nodejs.org/).
- **Tesseract-OCR Engine**
  - This is crucial. The application will not work without it.
  - **Windows:** Download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). During installation, ensure you install it to a simple path like `C:\Tesseract-OCR` and include the language packs you need (especially English).
  - **macOS:** `brew install tesseract`
  - **Linux (Ubuntu):** `sudo apt install tesseract-ocr`

### Installation & Setup

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Configure Backend (Python):**

    - Navigate to the backend directory:
      ```sh
      cd backend
      ```
    - (Recommended) Create and activate a virtual environment:
      ```sh
      python -m venv venv
      # On Windows
      .\venv\Scripts\activate
      # On macOS/Linux
      source venv/bin/activate
      ```
    - Install Python dependencies:
      ```sh
      pip install -r requirements.txt
      ```
    - **Important:** Open `backend/ocr_engine.py` and verify that the `TESSERACT_PATH` variable points to your Tesseract installation (e.g., `r'C:\Tesseract-OCR\tesseract.exe'`).

3.  **Configure Frontend (Electron):**
    - Navigate to the frontend directory:
      ```sh
      cd electron-app
      ```
    - Install npm packages:
      ```sh
      npm install
      ```

## ▶️ Usage

The project is configured to run both the backend efeitos secundários ao mesmo tempo.

1.  **Open one terminal** and navigate to the `electron-app` directory.
2.  Run the developer script:
    ```sh
    npm run dev
    ```
    This single command will start the Python Flask server and launch the Electron application concurrently.
3.  The application window will appear.
4.  Click the "Traduzir Área" button. The screen will dim.
5.  Click and drag to select the text you want to translate.
6.  The result will appear in the app's panels or as a floating overlay, depending on your selected settings.
7.  Use the settings icon on the sidebar to change the output mode and theme.
8.  To stop both the app and the server, simply press `Ctrl + C` in the terminal.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
