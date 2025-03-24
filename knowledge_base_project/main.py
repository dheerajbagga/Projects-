import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import os
from knowledge_base.kb_manager import KBManager  # Assuming kb_manager.py is in knowledge_base package

class KnowledgeBaseUI:
    def __init__(self, master):
        self.master = master
        master.title("Knowledge Base UI")

        self.kb_manager = KBManager()  # Initialize KBManager

        # --- Upload Frame ---
        self.upload_frame = ttk.LabelFrame(master, text="Upload Knowledge")
        self.upload_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.upload_button = ttk.Button(self.upload_frame, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.upload_status_label = ttk.Label(self.upload_frame, text="No file uploaded")
        self.upload_status_label.grid(row=1, column=0, padx=5, pady=5)

        # --- Add Knowledge Frame ---
        self.add_frame = ttk.LabelFrame(master, text="Add Knowledge")
        self.add_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.title_label = ttk.Label(self.add_frame, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(self.add_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.content_label = ttk.Label(self.add_frame, text="Content:")
        self.content_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.content_text = scrolledtext.ScrolledText(self.add_frame, width=40, height=10)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Knowledge", command=self.add_knowledge_item)
        self.add_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        # --- Prompt and Response Frame ---
        self.prompt_frame = ttk.LabelFrame(master, text="Prompt and Response")
        self.prompt_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.prompt_label = ttk.Label(self.prompt_frame, text="Prompt:")
        self.prompt_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.prompt_entry = ttk.Entry(self.prompt_frame, width=40)
        self.prompt_entry.grid(row=0, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.prompt_frame, text="Search", command=self.search_knowledge)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.clear_button = ttk.Button(self.prompt_frame, text="Clear", command=self.clear_response)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)

        self.response_label = ttk.Label(self.prompt_frame, text="Response:")
        self.response_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.response_text = scrolledtext.ScrolledText(self.prompt_frame, width=40, height=10)
        self.response_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        self.response_text.config(state="disabled")

        # --- Configure Grid Weights ---
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.add_frame.grid_rowconfigure(1, weight=1)
        self.add_frame.grid_columnconfigure(1, weight=1)
        self.prompt_frame.grid_rowconfigure(1, weight=1)
        self.prompt_frame.grid_columnconfigure(1, weight=1)

    def upload_file(self):
        """Opens a file dialog to select a text file and adds its content to the knowledge base."""
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                with open(filepath, "r") as f:
                    content = f.read()
                    filename = os.path.basename(filepath)
                    title = filename[:-4] if filename.endswith(".txt") else filename
                    self.kb_manager.add_knowledge(title, content)
                    self.upload_status_label.config(text=f"Uploaded: {filename}")
            except Exception as e:
                self.upload_status_label.config(text=f"Error: {e}")
        else:
            self.upload_status_label.config(text="No file selected")

    def add_knowledge_item(self):
        """Adds a new knowledge item from the title and content fields."""
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END)
        if title and content:
            self.kb_manager.add_knowledge(title, content)
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.upload_status_label.config(text="Knowledge added successfully")
        else:
            self.upload_status_label.config(text="Title and content are required")

    def search_knowledge(self):
        """Searches the knowledge base based on the prompt and displays the results."""
        keyword = self.prompt_entry.get()
        results = self.kb_manager.search_knowledge(keyword)
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", tk.END)
        if results:
            for item in results:
                self.response_text.insert(tk.END, str(item))
        else:
            self.response_text.insert(tk.END, "No results found.")
        self.response_text.config(state="disabled")
    
    def clear_response(self):
        """Clears the response text area."""
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state="disabled")


def main():
    root = tk.Tk()
    KnowledgeBaseUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
