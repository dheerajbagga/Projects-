import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from knowledge_base.kb_item import KBItem

class KBManager:
    def __init__(self, data_dir="data/knowledge_items", embeddings_dir="embeddings", model_name="all-mpnet-base-v2"):
        self.data_dir = data_dir
        self.embeddings_dir = embeddings_dir
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)
        self.knowledge_items = []
        self.embeddings = []
        self.faiss_index = None
        self._load_knowledge()

    def _generate_embedding(self, text):
        """Generates a vector embedding for the given text using the SentenceTransformer model."""
        return self.model.encode(text)

    def _load_knowledge(self):
        """Loads knowledge items from text files and their embeddings."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.embeddings_dir):
            os.makedirs(self.embeddings_dir)

        index_path = os.path.join(self.embeddings_dir, "index.bin")
        embeddings_path = os.path.join(self.embeddings_dir, "embeddings.pkl")

        if os.path.exists(index_path) and os.path.exists(embeddings_path):
            try:
                # Load existing index and embeddings
                self.faiss_index = faiss.read_index(index_path)
                with open(embeddings_path, "rb") as f:
                    self.embeddings = pickle.load(f)
                #load knowledge items
                for filename in os.listdir(self.data_dir):
                    if filename.endswith(".txt"):
                        filepath = os.path.join(self.data_dir, filename)
                        with open(filepath, "r") as f:
                            title = filename[:-4]  # Remove .txt extension
                            content = f.read()
                            self.knowledge_items.append(KBItem(title, content))
            except RuntimeError as e:
                print(f"Error loading index or embeddings: {e}")
                print("Deleting existing index and embeddings files...")
                os.remove(index_path)
                os.remove(embeddings_path)
                self.faiss_index = None
                self.embeddings = []
                self.knowledge_items = []
                
        else:
            # Create new index and embeddings
            for filename in os.listdir(self.data_dir):
                if filename.endswith(".txt"):
                    filepath = os.path.join(self.data_dir, filename)
                    with open(filepath, "r") as f:
                        title = filename[:-4]  # Remove .txt extension
                        content = f.read()
                        self.knowledge_items.append(KBItem(title, content))
                        embedding = self._generate_embedding(content)
                        self.embeddings.append(embedding)

            # Build FAISS index
            if self.embeddings:
                dimension = len(self.embeddings[0])
                self.faiss_index = faiss.IndexFlatL2(dimension)
                self.faiss_index.add(np.array(self.embeddings))
                # Save index and embeddings
                faiss.write_index(self.faiss_index, index_path)
                with open(embeddings_path, "wb") as f:
                    pickle.dump(self.embeddings, f)

    def add_knowledge(self, title, content):
        """Adds a new knowledge item, generates its embedding, and adds it to the index."""
        new_item = KBItem(title, content)
        self.knowledge_items.append(new_item)
        self._save_knowledge(new_item)
        embedding = self._generate_embedding(content)
        self.embeddings.append(embedding)
        if self.faiss_index is None:
            dimension = len(embedding)
            self.faiss_index = faiss.IndexFlatL2(dimension)
            self.faiss_index.add(np.array([embedding]))
        else:
            self.faiss_index.add(np.array([embedding]))
        # Save index and embeddings
        index_path = os.path.join(self.embeddings_dir, "index.bin")
        embeddings_path = os.path.join(self.embeddings_dir, "embeddings.pkl")
        faiss.write_index(self.faiss_index, index_path)
        with open(embeddings_path, "wb") as f:
            pickle.dump(self.embeddings, f)

    def _save_knowledge(self, item):
        """Saves a knowledge item to a text file."""
        filepath = os.path.join(self.data_dir, f"{item.title}.txt")
        with open(filepath, "w") as f:
            f.write(item.content)

    def search_knowledge(self, query, top_k=5):
        """Searches for knowledge items based on semantic similarity to the query."""
        query_embedding = self._generate_embedding(query)
        if self.faiss_index is None:
            return []
        
        # Ensure query_embedding is a 2D array
        query_embedding = np.array([query_embedding])
        
        distances, indices = self.faiss_index.search(query_embedding, top_k)
        results = [self.knowledge_items[i] for i in indices[0]]
        return results

    def display_knowledge(self):
        """Displays all the knowledge items."""
        for item in self.knowledge_items:
            print(item)
