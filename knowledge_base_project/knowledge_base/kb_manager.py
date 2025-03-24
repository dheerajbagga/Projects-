import os
from knowledge_base.kb_item import KBItem

class KBManager:
    def __init__(self, data_dir="data/knowledge_items"):
        self.data_dir = data_dir
        self.knowledge_items = []
        self._load_knowledge()

    def _load_knowledge(self):
        """Loads knowledge items from text files in the data directory."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            return
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, "r") as f:
                    title = filename[:-4]  # Remove .txt extension
                    content = f.read()
                    self.knowledge_items.append(KBItem(title, content))

    def add_knowledge(self, title, content):
        """Adds a new knowledge item to the knowledge base and saves it to a file."""
        new_item = KBItem(title, content)
        self.knowledge_items.append(new_item)
        self._save_knowledge(new_item)

    def _save_knowledge(self, item):
        """Saves a knowledge item to a text file."""
        filepath = os.path.join(self.data_dir, f"{item.title}.txt")
        with open(filepath, "w") as f:
            f.write(item.content)

    def search_knowledge(self, keyword):
        """Searches for knowledge items based on a keyword (case-insensitive)."""
        results = []
        for item in self.knowledge_items:
            if keyword.lower() in item.title.lower() or keyword.lower() in item.content.lower():
                results.append(item)
        return results
    
    def display_knowledge(self):
        """Displays all the knowledge items."""
        for item in self.knowledge_items:
            print(item)
