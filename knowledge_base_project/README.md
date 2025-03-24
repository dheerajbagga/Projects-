# Knowledge Base Project

This project implements a simple knowledge base system with a graphical user interface (GUI) for managing and searching knowledge items. It allows users to add, upload, and search for information stored as text snippets. The project is built using only built-in Python modules, along with `tkinter` for the UI.

## Features

*   **Knowledge Storage:** Stores knowledge items (text snippets) in a structured way as text files.
*   **Add Knowledge:**
    *   Manually add new knowledge items by entering a title and content.
    *   Upload knowledge items from text files.
*   **Search Knowledge:** Search for knowledge items based on keywords (case-insensitive).
*   **Display Knowledge:** Display the knowledge items in the response box.
*   **Clear Response:** Clear the response box.
*   **GUI:** User-friendly graphical interface for easy interaction.
*   **Persistence:** Knowledge items are saved to text files and loaded on startup.
* **Python-Only:** No external libraries are used except `tkinter` for the UI.

## Folder Structure


## Modules

*   **`main.py`:**
    *   Contains the main application logic and the `KnowledgeBaseUI` class.
    *   Handles the GUI elements, user interactions, and calls to the `KBManager`.
*   **`knowledge_base/kb_item.py`:**
    *   Defines the `KBItem` class, which represents a single knowledge item with a title and content.
*   **`knowledge_base/kb_manager.py`:**
    *   Defines the `KBManager` class, which manages the knowledge base.
    *   Handles loading, adding, saving, searching, and displaying knowledge items.
*   **`knowledge_base/__init__.py`:**
    *   An empty file that makes the `knowledge_base` directory a Python package.

## How to Run

1.  **Create the folder structure:**
    ```bash
    mkdir knowledge_base_project
    cd knowledge_base_project
    mkdir knowledge_base
    mkdir data
    mkdir data/knowledge_items
    ```

2.  **Save the files:**
    *   Create the files `kb_item.py`, `kb_manager.py`, and `__init__.py` inside the `knowledge_base` directory.
    *   Create the file `main.py` inside the `knowledge_base_project` directory.
    *   Copy and paste the corresponding code into each file.

3.  **Run `main.py`:**
    ```bash
    python main.py
    ```

## Usage

1.  **Upload Knowledge:** Click the "Upload File" button to select a text file and add its content to the knowledge base.
2.  **Add Knowledge:** Enter a title and content in the "Add Knowledge" section and click "Add Knowledge."
3.  **Search Knowledge:** Enter a keyword in the "Prompt" field and click "Search." The results will be displayed in the "Response" area.
4. **Clear Response:** Click the "Clear" button to clear the response area.

## Future Enhancements

*   **Semantic Search:** Integrate a Large Language Model (LLM) and FAISS for semantic search capabilities.
*   **More Advanced UI:** Improve the UI with more features and better layout.
*   **Database Integration:** Use a database (e.g., SQLite) for more efficient storage and retrieval of knowledge items.
*   **Error Handling:** Add more robust error handling and user feedback.

## Limitations

*   **Basic Search:** The current search is based on simple keyword matching, not semantic understanding.
*   **Text File Storage:** Storing knowledge in text files is not ideal for large knowledge bases.
* **No LLM:** This project does not use any Large Language Model.

## License

This project is licensed under the **MIT License**.
