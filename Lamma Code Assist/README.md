# AI Code Assistant

This is a simple AI Code Assistant application that uses the Ollama language model (specifically `codellama`) to generate code based on user prompts. It provides a graphical user interface (GUI) built with Tkinter, allowing users to interact with the model easily.

## Features

*   **Prompt Input:** Enter code descriptions or instructions in a multi-line text area.
*   **Code Generation:** Generate code snippets based on your prompts using the `codellama` model.
*   **Real-time Output:** See the generated code appear in the response area as it's being generated.
*   **Stop Generation:** Stop the code generation process at any time.
*   **Clear Output:** Clear the response area to start fresh.
*   **Status Updates:** Get feedback on the current state of the application (e.g., "Generating code...", "Code generation complete.").
*   **Automatic Model Download:** The application will automatically download the `codellama` model if it is not present.
*   **Ollama Server Check:** The application checks if the Ollama server is running and prompts the user to start it if it is not.

## Prerequisites

*   **Ollama:** You **must** have Ollama installed and running on your system. This application relies on the Ollama server to provide the language model functionality.
    *   **Ollama Installation:** Follow the instructions on the official Ollama website: https://ollama.com/
    *   **Ollama Server:** After installing Ollama, you need to start the Ollama server in your terminal:
        ```bash
        ollama serve
        ```
        Keep this terminal window open while using the AI Code Assistant.
*   **`codellama` Model:** The application will automatically download the `codellama` model if it is not present.
*   **Python 3:** This application requires Python 3.
*   **Python `ollama` Library:** You need to install the `ollama` Python library to interact with the Ollama server.
    ```bash
    pip install ollama
    ```
*   **Tkinter:** Tkinter is usually included with Python, but you may need to install it separately on some Linux distributions (see installation instructions below).

## Installation

1.  **Clone the Repository (Optional):** If you have the code in a Git repository, clone it:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install the `ollama` and `requests` libraries.

3.  **Start Ollama Server:**
    ```bash
    ollama serve
    ```
    **Important:** The Ollama server must be running in a separate terminal window for the application to work.

4.  **Run the Application:**
    ```bash
    python main.py
    ```

## Tkinter Installation (Linux - If Needed)

If you encounter errors related to Tkinter on Linux, you may need to install it separately:

*   **Ubuntu/Debian:**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

*   **Fedora/CentOS/RHEL:**
    ```bash
    sudo dnf install python3-tkinter  # Or sudo yum install python3-tkinter
    ```

## Usage

1.  **Start the Ollama server** using `ollama serve` in a terminal window.
2.  Run the application using `python main.py`.
3.  The application will check if the Ollama server is running and if the `codellama` model is downloaded. If not, it will prompt you to start the server or download the model.
4.  Enter your code description or prompt in the "Enter your Prompt" text area.
5.  Click "Submit your Prompt" to start generating code.
6.  The generated code will appear in the "Generated Response" area.
7.  Click "Stop Generation" to halt the code generation process.

## Files

*   `main.py`: The main Python script containing the GUI and code generation logic.
*   `requirements.txt`: Lists the required Python packages.
*   `README.md`: This file.

## License

This project is licensed under the **MIT License**.
