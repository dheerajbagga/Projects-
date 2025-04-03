import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import ollama
import time
import subprocess
import requests

class CodeAssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Code Assistant")

        # Check Ollama server and model
        """
        if not self.check_ollama_server():
            return  # Exit if the server is not running
        if not self.check_codellama_model():
            return  # Exit if the model is not downloaded
        """

        # Prompt Label and Text Area
        self.prompt_label = tk.Label(master, text="Enter your Prompt:")
        self.prompt_label.pack(pady=(20, 15))

        # Use tk.Text instead of tk.Entry
        self.prompt_entry = tk.Text(master, width=150, height=5)  # Increased height to 5 lines
        self.prompt_entry.pack(pady=(0, 10))

        # Generate Button
        self.generate_button = tk.Button(master, text="Submit your Prompt", command=self.generate_code_thread)
        self.generate_button.pack(pady=(0, 5))

        # Stop Button
        self.stop_button = tk.Button(master, text="Stop Generation", command=self.stop_generation)
        self.stop_button.pack(pady=(0, 10))
        self.stop_button.config(state=tk.DISABLED)  # Initially disabled

        # Response Label
        self.response_label = tk.Label(master, text="Generated Response:")
        self.response_label.pack()

        # Response Text Area (ScrolledText)
        self.response_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=150, height=40)
        self.response_text.pack(pady=(0, 10))
        self.response_text.config(state=tk.DISABLED)  # Make it read-only

        # Status Label
        self.status_label = tk.Label(master, text="Ready")
        self.status_label.pack(pady=(5, 10))

        self.generation_thread = None  # To store the thread object
        self.stop_event = threading.Event()  # To signal the thread to stop

    def check_ollama_server(self):
        """Checks if the Ollama server is running."""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                return True
            else:
                messagebox.showerror("Ollama Server Error", "Ollama server is not running. Please start it with 'ollama serve' in your terminal.")
                return False
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Ollama Server Error", "Ollama server is not running. Please start it with 'ollama serve' in your terminal.")
            return False

    def check_codellama_model(self):
        """Checks if the codellama model is downloaded."""
        try:
            models_data = ollama.list()
            print("ollama.list() output:", models_data)  # Debugging: Print the output

            if 'models' not in models_data:
                print("Error: 'models' key not found in ollama.list() output.")
                raise ValueError("Invalid ollama.list() output format")

            models = models_data['models']
            if not models:
                print("No models found in ollama.list() output.")
            
            model_found = False
            for model in models:
                print("Model details:", model)  # Debugging: Print each model's details
                if 'name' in model and model['name'] in ('codellama:latest', 'codellama'):
                    model_found = True
                    break

            if model_found:
                return True
            else:
                if messagebox.askyesno("Model Not Found", "The codellama model is not downloaded. Do you want to download it now?"):
                    self.set_status("Downloading codellama model...")
                    ollama.pull('codellama')
                    self.set_status("codellama model downloaded.")
                    return True
                else:
                    messagebox.showerror("Model Not Found", "The codellama model is required. Please download it using 'ollama pull codellama' in your terminal.")
                    return False
        except Exception as e:
            messagebox.showerror("Ollama Error", f"An error occurred while checking for the codellama model: {e}")
            return False


    def generate_code_thread(self):
        """Starts the code generation in a separate thread."""
        self.stop_event.clear()  # Clear the stop event before starting a new generation
        self.generation_thread = threading.Thread(target=self.generate_code)
        self.generation_thread.start()

    def generate_code(self):
        """Generates code based on the user's prompt."""
        self.set_status("Generating code...")
        self.disable_input()
        self.clear_response()
        self.stop_button.config(state=tk.NORMAL) #enable stop button

        # Get the prompt from the tk.Text widget
        prompt = self.prompt_entry.get("1.0", tk.END).strip()  # Get all text from start to end, remove leading/trailing whitespace
        if not prompt:
            self.set_status("Prompt cannot be empty.")
            self.enable_input()
            return

        try:
            response_stream = ollama.generate(model='codellama', prompt=prompt, stream=True)
            full_response = ""
            for response_part in response_stream:
                if self.stop_event.is_set():
                    self.set_status("Generation stopped by user.")
                    break  # Exit the loop if the stop event is set
                if 'response' in response_part:
                    chunk = response_part['response']
                    full_response += chunk
                    self.append_response(chunk)
            if not self.stop_event.is_set():
                self.set_status("Code generation complete.")
        except Exception as e:
            self.set_status(f"Error: {e}")
        finally:
            self.enable_input()
            self.stop_button.config(state=tk.DISABLED) #disable stop button

    def stop_generation(self):
        """Stops the code generation."""
        self.stop_event.set()  # Set the stop event to signal the thread to stop
        self.set_status("Stopping generation...")
        # No need to explicitly join the thread here, as it will eventually exit on its own

    def append_response(self, text):
        """Appends text to the response text area."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.insert(tk.END, text)
        self.response_text.config(state=tk.DISABLED)
        self.response_text.see(tk.END)  # Scroll to the end

    def clear_response(self):
        """Clears the response text area."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state=tk.DISABLED)

    def set_status(self, message):
        """Updates the status label."""
        self.status_label.config(text=message)
        self.master.update_idletasks()  # Force update

    def disable_input(self):
        """Disables the input field and button."""
        self.prompt_entry.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.DISABLED)

    def enable_input(self):
        """Enables the input field and button."""
        self.prompt_entry.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    gui = CodeAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
