# Semantic Knowledge Base Application

This project implements a knowledge base system with a graphical user interface (GUI) that allows users to store, manage, and search through knowledge items. It utilizes semantic search powered by a Hugging Face sentence-transformer model and FAISS for efficient indexing, enabling users to find relevant information based on the meaning of their queries, not just keyword matches.

## Features

*   **Knowledge Storage:** Persistently stores knowledge items (text snippets) in a structured way as text files.
*   **Add Knowledge:**
    *   **Manual Entry:** Add new knowledge items by entering a title and content directly in the GUI.
    *   **File Upload:** Upload knowledge items from various file types, including:
        *   Text files (`.txt`)
        *   PDF files (`.pdf`)
        *   Word files (`.docx`, `.doc`)
*   **Semantic Search:** Search for knowledge items based on semantic similarity to a user's query. The application uses a pre-trained sentence-transformer model to understand the meaning of the query and find the most relevant knowledge items.
*   **Efficient Indexing:** Employs FAISS (Facebook AI Similarity Search) for fast and efficient indexing and searching of knowledge item embeddings.
*   **Display Results:** Presents the most relevant knowledge items in the response box of the GUI.
*   **Clear Results:** Provides a button to clear the response box.
*   **User-Friendly GUI:** Offers a simple and intuitive graphical interface for easy interaction.
*   **Persistence:** Knowledge items, their embeddings, and the FAISS index are saved to files, ensuring that the knowledge base is preserved between application sessions.

## Getting Started

### Prerequisites

*   **Python 3.7+**
*   **Required Python Packages:**
    *   `sentence-transformers` (For generating sentence embeddings)
    *   `faiss-cpu` (For efficient similarity search and indexing)
    *   `numpy`  (For numerical operations used by `sentence-transformers` and `faiss-cpu`)
    *   `PyPDF2` (For extracting text from PDF files)
    *   `python-docx` (For extracting text from Word files)
    *   `pymupdf` (For extracting text from PDF files)
    * **`tkinter`:** `tkinter` is part of the Python standard library and is typically installed with Python itself. On Windows, make sure to select the "tcl/tk and IDLE" option during Python installation.

    You can install these packages using `pip`:

    ```bash
    pip install sentence-transformers faiss-cpu numpy PyPDF2 python-docx pymupdf
    ```

    Alternatively, if you have a `requirements.txt` file (which is recommended), you can install them all at once:

    ```bash
    pip install -r requirements.txt
    ```

### Installation

1.  **Clone the repository (if applicable):**

    If you're using Git, clone the repository to your local machine:

    ```bash
    git clone <your_repository_url>
    cd semantic_knowledge_base_project
    ```

    (Replace `<your_repository_url>` with the actual URL of your Git repository.)

2.  **Create a virtual environment (recommended):**

    It's highly recommended to use a virtual environment to manage your project's dependencies.
    ```bash
    python -m venv .venv
    ```
    Activate the virtual environment:
    *   Windows (Command Prompt): `.venv\Scripts\activate`
    *   Windows (PowerShell): `.venv\Scripts\Activate.ps1`
    *   macOS/Linux: `source .venv/bin/activate`

3.  **Create a `requirements.txt` file (recommended):**

    It's good practice to create a `requirements.txt` file to keep track of your project's dependencies.
    
    This project uses the following packages:
    1. `sentence-transformers`: For generating sentence embeddings.
    2. `faiss-cpu`: For efficient similarity search and indexing.
    3. `numpy`: For numerical operations (used by `sentence-transformers` and `faiss-cpu`).
    4. `PyPDF2`: For extracting text from PDF files.
    5. `python-docx`: For extracting text from Word files.
    6. `pymupdf`: For extracting text from PDF files.

    You can create a `requirements.txt` file by running:

    ```bash
    pip freeze > requirements.txt
    ```
    This command will list all the packages installed in your current environment and save them to `requirements.txt`.
    
    Install the packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    Navigate to the project directory and run the main script:

    ```bash
    python main.py
    ```

### Folder Structure


### Modules

*   **`main.py`:**
    *   Contains the main application logic and the `KnowledgeBaseUI` class.
    *   Handles the GUI elements, user interactions, and calls to the `KBManager`.
*   **`knowledge_base/kb_item.py`:**
    *   Defines the `KBItem` class, which represents a single knowledge item with a title and content.
*   **`knowledge_base/kb_manager.py`:**
    *   Defines the `KBManager` class, which handles the core knowledge base logic.
    *   Manages the SentenceTransformer model, FAISS index, knowledge item storage, and semantic search.
*   **`knowledge_base/__init__.py`:**
    *   Makes the `knowledge_base` directory a Python package.

## Usage

1.  **Adding Knowledge:**
    *   **Manually:**
        *   Enter a title in the "Title" field.
        *   Enter the content in the "Content" text area.
        *   Click the "Add Knowledge" button.
    *   **Upload from File:**
        *   Click the "Upload File" button in the "Upload Knowledge" section.
        *   Select a `.txt`, `.pdf`, `.docx`, or `.doc` file from your computer.
        *   The file's content will be added to the knowledge base.
2.  **Searching:**
    *   Enter your search query in the "Prompt" field in the "Prompt and Response" section.
    *   Click the "Search" button.
3.  **Viewing Results:**
    *   The most relevant knowledge items will be displayed in the "Response" text area.
4.  **Clearing Results:**
    *   Click the "Clear" button to clear the "Response" text area.

## Notes

*   **First Run:** The first time you run the application, it will download the `all-mpnet-base-v2` SentenceTransformer model. This may take a few minutes depending on your internet connection.
*   **Automatic Directory Creation:** The `data/knowledge_items` and `embeddings` directories will be created automatically if they don't exist.
*   **Automatic File Creation:** The `index.bin` and `embeddings.pkl` files will be created automatically by the application.
*   **File type:** The application supports `.txt`, `.pdf`, `.docx`, or `.doc` files.
* **tkinter:** `tkinter` is part of the Python standard library and is typically installed with Python itself. On Windows, make sure to select the "tcl/tk and IDLE" option during Python installation.

## Contributing

If you'd like to contribute to this project, please feel free to open a pull request or submit an issue on the project's repository.

## License

This project is licensed under the **MIT License**.
