#this is just copied for the moment

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import json, time
import re
from copy import deepcopy

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CYAN Config Generator")
        self.step = 0
        self.entries = {}
        self.datapoint_entries = {}
        self.iterators = []
        self.instructions = {}
        self.temp_entries = {}
        self.create_widgets()
    
    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        self.label = ttk.Label(self.frame, text="Welcome to the CYAN Config Generator!")
        self.label.pack(pady=5)
        
        self.next_button = ttk.Button(self.frame, text="Next", command=self.next_step)
        self.next_button.pack()
        
    def next_step(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()  # Using pack_forget() to hide widgets instead of destroying them
        
        if self.step == 0:
            self.temp_entries = {}
            self.label = ttk.Label(self.frame, text="Enter Metadata")
            self.label.pack(pady=5)
            
            metadata_fields = ["cpu_name", "cpu_version", "creator", "date", "cpu_description"]
            for field in metadata_fields:
                row = ttk.Frame(self.frame)
                row.pack(fill='x', padx=10, pady=6)
                label = ttk.Label(row, text=field.capitalize(), width=15)
                label.pack(side='left')
                entry = ttk.Entry(row)
                entry.pack(side='right', fill='x', expand=True)
                self.temp_entries[field] = entry
            
            self.next_button = ttk.Button(self.frame, text="Next", command=self.new_step)
            self.next_button.pack(pady=5)
        
        elif self.step == 1:
            self.label = ttk.Label(self.frame, text="Enter Specs")
            self.label.pack(pady=5)
            self.temp_entries = {}
            specs_fields = [["pipelined","bool"],["address_space","txt"],["word_size","txt"],["simulation_speed","txt"],["rom_size","txt"],["ram_size","txt"]]
            for field in specs_fields:
                row = ttk.Frame(self.frame)
                row.pack(fill='x', padx=10, pady=6)
                label = ttk.Label(row, text=field[0].capitalize(), width=15)
                label.pack(side='left')
                if field[1] == "txt":
                    
                    entry = ttk.Entry(row)
                    entry.pack(side='right', fill='x', expand=True)
                else:
                    entry = tk.BooleanVar()
                    temp = ttk.Checkbutton(row,variable=entry)
                    temp.pack(side='right',fill='x', expand=True)
                self.temp_entries[field[0]] = entry
            
            
            # todo
            self.next_button = ttk.Button(self.frame, text="Next", command=self.new_step)
            self.next_button.pack(pady=5)


        elif self.step==2 and self.entries["pipelined"]:
            self.temp_entries = {}
            self.label = ttk.Label(self.frame, text="Pipeline")
            self.label.pack(pady=5)
            self.label = ttk.Label(self.frame, text="Seperate instructions by newline")
            self.label.pack(pady=5)
            row = ttk.Frame(self.frame)
            row.pack(fill='x', padx=5, pady=6)
            entry = scrolledtext.ScrolledText(self.frame, height=8, width=30, wrap=tk.WORD)
            entry.pack(side='top', fill='x', expand=True)
            self.temp_entries["pipeline"] = entry

            self.next_button = ttk.Button(self.frame, text="Next", command=self.new_step)
            self.next_button.pack(pady=5)

        elif self.step == 2: # skip to step 3
            self.step = 3
            self.next_step()


        elif self.step == 3: # flags
            self.label = ttk.Label(self.frame, text="Flags")
            self.label.pack(pady=5)
            self.temp_entries = {}
            self.label = ttk.Label(self.frame, text="Seperate flag names by newline")
            self.label.pack(pady=5)
            row = ttk.Frame(self.frame)
            row.pack(fill='x', padx=5, pady=6)
            entry = scrolledtext.ScrolledText(self.frame, height=8, width=30, wrap=tk.WORD)
            entry.pack(side='top', fill='x', expand=True)
            self.temp_entries["flags"] = entry

            self.next_button = ttk.Button(self.frame, text="Next", command=self.new_step)
            self.next_button.pack(pady=5)

        elif self.step == 4: # registers
            self.temp_entries = {}
            self.label = ttk.Label(self.frame, text="Registers")
            self.label.pack(pady=5)
            
            # register count
            row = ttk.Frame(self.frame) 
            row.pack(fill='x', padx=10, pady=6)
            label = ttk.Label(row, text="register_count".capitalize(), width=15)
            label.pack(side='left')
            entry = ttk.Entry(row)
            entry.pack(side='right', fill='x', expand=True)
            self.temp_entries["register_count"] = entry

            # special registers
            self.label = ttk.Label(self.frame, text="Special Registers: Seperate reg names by newline")
            self.label.pack(pady=5)
            row = ttk.Frame(self.frame)
            row.pack(fill='x', padx=5, pady=6)
            entry2 = scrolledtext.ScrolledText(self.frame, height=8, width=30, wrap=tk.WORD)
            entry2.pack(side='top', fill='x', expand=True)
            self.temp_entries["special_reg_names"] = entry2

            
            self.next_button = ttk.Button(self.frame, text="Next", command=self.new_step)
            self.next_button.pack(pady=5)
        
        elif self.step == 5: # fix this up using multiple widgets
            
            self.label = ttk.Label(self.frame, text="Special Registers one by one")
            self.label.pack(pady=5)
            if len(self.iterators) > 0:
                self.instruction_label = ttk.Label(self.frame, text=f"Regs Left: {', '.join(self.iterators)}")
                self.instruction_label.pack(pady=5)
                self.instruction_label = ttk.Label(self.frame, text=f"Current: {self.iterators[0]}")
                self.instruction_label.pack(pady=5)
                
                specs_fields = [["description","txt"],["address","txt"],["read_only","bool"],["write_only","bool"],["default_value","txt"],["size","txt"],["accumulates","bool"]]
                for reg_name in self.iterators:
                    self.temp_entries[reg_name] = {"name":reg_name}
                for field in specs_fields:
                    row = ttk.Frame(self.frame)
                    row.pack(fill='x', padx=10, pady=6)
                    label = ttk.Label(row, text=field[0].capitalize(), width=15)
                    label.pack(side='left')
                    if field[1] == "txt":
                        
                        entry = ttk.Entry(row)
                        entry.pack(side='right', fill='x', expand=True)
                    else:
                        entry = tk.BooleanVar()
                        temp = ttk.Checkbutton(row,variable=entry)
                        temp.pack(side='right',fill='x', expand=True)
                    self.temp_entries[self.iterators[0]][field[0]] = entry
                
                self.add_button = ttk.Button(self.frame, text="Add Reg", command=self.port_update)
                self.add_button.pack(pady=5)
            else:
                self.done_button = ttk.Button(self.frame, text="Done", command=self.new_step)
                self.done_button.pack(pady=5)



    def new_step(self): # intermediary function. Just turns everything to normal in case i need values or subdicts
        print(self.temp_entries)
        if self.step == 0 or self.step == 1:
            for field in self.temp_entries:
                self.entries[field] = self.temp_entries[field].get()
            
        elif self.step == 2: #deal with multiline pipeline stages
            for field in self.temp_entries:
                self.entries[field] = []
                for word in self.temp_entries[field].get("1.0",tk.END).split('\n'):
                    if word == '': continue
                    self.entries[field].append(word.strip())

        elif self.step == 3: # deal with multiline flag stages
            for field in self.temp_entries:
                self.entries[field] = {}
                for index, word in enumerate(self.temp_entries[field].get("1.0",tk.END).split('\n')):
                    if word == '': continue
                    self.entries[field][word.strip()] = index

        elif self.step == 4:
            self.entries["register_count"] = self.temp_entries["register_count"].get()
            for word in self.temp_entries["special_reg_names"].get("1.0",tk.END).split('\n'):
                if word == '': continue
                self.iterators.append(word.strip())
        elif self.step == 5:
            self.entries["special_registers"] = []
            for field in self.temp_entries:
                self.entries["special_registers"].append(deepcopy(self.temp_entries[field]))
        self.temp_entries = {}
        print(self.entries)
        self.step += 1
        self.next_step()



    def port_update(self): # update ports and registers
        name = self.iterators[0]
        for field in self.temp_entries[name]:
            if field == "name": continue
            self.temp_entries[name][field] = self.temp_entries[name][field].get()
        print(self.temp_entries)
        self.check_completion()
        self.next_step()



    def check_completion(self):
        # Check if we are done
        if len(self.iterators) != 0:  # If no operations left
            self.iterators.pop(0)



if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()