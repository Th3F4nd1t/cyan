#this is just copied for the moment

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import json
import re

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CYAN Config Generator")
        self.step = 0
        self.entries = {}
        self.datapoint_entries = {}
        self.operations = []
        self.instructions = {}
        self.create_widgets()
    
    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.label = ttk.Label(self.frame, text="Welcome to the CYAN Config Generator!")
        self.label.pack(pady=5)
        
        self.next_button = ttk.Button(self.frame, text="Next", command=self.next_step)
        self.next_button.pack()
        
    def next_step(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()  # Using pack_forget() to hide widgets instead of destroying them
        
        if self.step == 0:
            self.label = ttk.Label(self.frame, text="Step 1: Enter Metadata")
            self.label.pack(pady=5)
            
            metadata_fields = ["cpu_name", "cpu_version", "creator", "date", "cpu_description"]
            for field in metadata_fields:
                row = ttk.Frame(self.frame)
                row.pack(fill='x', padx=5, pady=2)
                label = ttk.Label(row, text=field.capitalize(), width=15)
                label.pack(side='left')
                entry = ttk.Entry(row)
                entry.pack(side='right', fill='x', expand=True)
                self.entries[field] = entry
            
            self.next_button = ttk.Button(self.frame, text="Next", command=self.next_step)
            self.next_button.pack(pady=5)

        elif self.step == 1:
            self.label = ttk.Label(self.frame, text="Step 2: Enter Specs")
            self.label.pack(pady=5)
            
            # todo
            self.next_button = ttk.Button(self.frame, text="Next", command=self.next_step)
            self.next_button.pack(pady=5)

        self.step += 1
    
    
                
    
    def update_done_button_state(self):
        # Enable "Done" button if all operations have been added
        if not self.operations:  # If no operations left
            self.done_button.config(state=tk.NORMAL)
        else:
            self.done_button.config(state=tk.DISABLED)

    def check_completion(self):
        # Check if we are done
        if not self.operations:  # If no operations left
            self.step += 1
            self.done_button.config(state=tk.NORMAL)
            self.next_step()  # Go to next step if finished
        else:
            # If operations still remain, disable "Done"
            self.done_button.config(state=tk.DISABLED)



if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()