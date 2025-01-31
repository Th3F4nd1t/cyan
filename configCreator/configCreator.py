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
            
            metadata_fields = ["name", "cyan_version", "creator", "date", "description"]
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
            self.label = ttk.Label(self.frame, text="Step 2: Enter Datapoints")
            self.label.pack(pady=5)
            
            datapoint_fields = ["prom", "registers", "word_size", "opcode_size", "operand_count", "operand_size"]
            for field in datapoint_fields:
                row = ttk.Frame(self.frame)
                row.pack(fill='x', padx=5, pady=2)
                label = ttk.Label(row, text=field.capitalize(), width=15)
                label.pack(side='left')
                entry = ttk.Entry(row)
                entry.pack(side='right', fill='x', expand=True)
                self.datapoint_entries[field] = entry
            
            self.next_button = ttk.Button(self.frame, text="Next", command=self.next_step)
            self.next_button.pack(pady=5)
            
        elif self.step == 2:
            self.label = ttk.Label(self.frame, text="Step 3: Enter Operations (one per line)")
            self.label.pack(pady=5)
            
            self.operations_text = scrolledtext.ScrolledText(self.frame, height=5)
            self.operations_text.insert("1.0", "Enter operation names here, one per line...")
            self.operations_text.pack(fill='x', padx=5, pady=5)
            
            self.store_operations_button = ttk.Button(self.frame, text="Save Operations and Proceed", command=self.store_operations)
            self.store_operations_button.pack()
            return
        
        elif self.step == 3:
            self.label = ttk.Label(self.frame, text="Step 4: Write Instructions One by One")
            self.label.pack(pady=5)
            
            self.instruction_label = ttk.Label(self.frame, text=f"Available operations: {', '.join(self.operations)}")
            self.instruction_label.pack(pady=5)
            
            self.instruction_entry = scrolledtext.ScrolledText(self.frame, height=5)
            self.instruction_entry.pack(fill='x', padx=5, pady=5)
            
            self.add_instruction_button = ttk.Button(self.frame, text="Add Instruction", command=self.add_instruction)
            self.add_instruction_button.pack(pady=5)
            
            self.done_button = ttk.Button(self.frame, text="Done", command=self.check_completion, state=tk.DISABLED)
            self.done_button.pack(pady=5)
            return
        
        elif self.step == 4:
            self.label = ttk.Label(self.frame, text="Step 5: Save Config and Instructions")
            self.label.pack(pady=5)
            
            save_config_button = ttk.Button(self.frame, text="Save Config", command=self.save_config)
            save_config_button.pack(pady=5)
            
            save_instructions_button = ttk.Button(self.frame, text="Save Instructions", command=self.save_instructions)
            save_instructions_button.pack(pady=5)
        
        self.step += 1
    
    def store_operations(self):
        self.operations = self.operations_text.get("1.0", tk.END).strip().split("\n")
        self.operations = [op.strip() for op in self.operations if op.strip() and not op.startswith("Enter operation names here")]
        self.instructions = {op: None for op in self.operations}
        self.step += 1
        self.next_step()
    
    def add_instruction(self):
        instruction_code = self.instruction_entry.get("1.0", tk.END).strip()
        if instruction_code:
            match = re.search(r'class\s+(\w+):', instruction_code)
            if match:
                class_name = match.group(1)
                if class_name in self.instructions:
                    self.instructions[class_name] = instruction_code
                    self.operations.remove(class_name)
                
            else:
                messagebox.showerror("Error", "Class name not found.")
                    
            self.instruction_entry.delete("1.0", tk.END)
            self.instruction_label.config(text=f"Available operations: {', '.join(self.operations)}")
            
            # After adding instruction, update the "Done" button state
            self.update_done_button_state()
    
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
    
    def save_config(self):
        config_data = {
            "metadata": {field: self.entries[field].get() for field in self.entries},
            "datapoints": {
                field: int(self.datapoint_entries[field].get()) 
                for field in self.datapoint_entries
                if self.datapoint_entries[field].get().isdigit() and self.datapoint_entries[field].get()
            },
            "operations": list(self.instructions.keys())
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(config_data, file, indent=4)
    
    def save_instructions(self):
        # Remove any entries with None or empty instructions (including just spaces)
        valid_instructions = {class_name: instruction for class_name, instruction in self.instructions.items() if instruction and instruction.strip()}
        
        if not valid_instructions:  # If no valid instructions
            messagebox.showerror("Error", "No instructions to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                for class_name, instruction in valid_instructions.items():
                    file.write(f"\n\n# {class_name}\n{instruction}")



if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()