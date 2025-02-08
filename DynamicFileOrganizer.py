import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# ===============================
# Logging Setup
# ===============================
current_date = datetime.now().strftime('%Y-%m-%d')
log_dir = Path("C:/Download_Folder_Automation")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"download_automation_log_{current_date}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===============================
# Rules Persistence Setup
# ===============================
# Determine the file path for the custom rules JSON file.
if '__file__' in globals():
    RULES_FILE = Path(__file__).parent / "extension_rules.json"
else:
    RULES_FILE = Path("extension_rules.json")

# Global variable to store custom rules.
# Each rule is a dictionary: {"extensions": [".pdf", ".doc"], "dest": Path("C:/Some/Folder")}
custom_rules = []

def load_rules():
    """Load custom rules from the RULES_FILE and update the listbox."""
    global custom_rules
    if RULES_FILE.exists():
        try:
            with RULES_FILE.open("r") as f:
                data = json.load(f)
            custom_rules = []
            for rule in data:
                # Ensure the destination is stored as a Path
                custom_rules.append({
                    "extensions": rule.get("extensions", []),
                    "dest": Path(rule.get("dest", ""))
                })
            # Update the listbox if it exists.
            ext_rules_listbox.delete(0, tk.END)
            for rule in custom_rules:
                ext_rules_listbox.insert(tk.END, f"Extensions: {', '.join(rule['extensions'])} -> {rule['dest']}")
        except Exception as e:
            logging.error(f"Error loading rules: {e}")

def save_rules():
    """Save the current custom rules to the RULES_FILE."""
    try:
        data = []
        for rule in custom_rules:
            data.append({
                "extensions": rule["extensions"],
                "dest": str(rule["dest"])
            })
        with RULES_FILE.open("w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving rules: {e}")

# ===============================
# File Moving Functions
# ===============================
def move_to_folder(filepath, destination_folder):
    """
    Moves a file to the specified destination folder.
    If a file with the same name exists, the file is renamed.
    """
    try:
        destination_folder.mkdir(parents=True, exist_ok=True)
        destination_file = destination_folder / filepath.name
        if destination_file.exists():
            new_name = f"{filepath.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}{filepath.suffix}"
            destination_file = destination_folder / new_name
        shutil.move(str(filepath), str(destination_file))
        logging.info(f"Moved {filepath} to {destination_file}")
    except Exception as e:
        logging.error(f"Failed to move {filepath}: {e}")

def move_files_by_custom_rules(source_folder, rules, default_dest=None):
    """
    Recursively moves files from source_folder based on custom rules.
    
    rules: A list of dicts where each dict contains:
           - 'extensions': list of extensions (e.g., ['.pdf', '.doc'])
           - 'dest': destination folder (Path object)
    default_dest: If provided, files not matching any rule will be moved here.
    """
    for root, _, files in os.walk(source_folder):
        for filename in files:
            filepath = Path(root) / filename
            if not filepath.is_file():
                continue
            file_ext = filepath.suffix.lower()
            moved = False
            for rule in rules:
                if file_ext in rule['extensions']:
                    move_to_folder(filepath, rule['dest'])
                    moved = True
                    break
            if not moved:
                if default_dest:
                    move_to_folder(filepath, default_dest)
                else:
                    logging.info(f"No matching rule for {filepath}")

def move_files_by_keyword(source_folder, folders_mapping):
    """
    Recursively moves files from source_folder based on keywords.
    
    folders_mapping: A dictionary mapping a keyword to a destination folder (Path).
    """
    for root, _, files in os.walk(source_folder):
        for filename in files:
            filepath = Path(root) / filename
            if not filepath.is_file():
                continue
            filename_lower = filename.lower()
            moved = False
            for keyword, folder in folders_mapping.items():
                if keyword.lower() in filename_lower:
                    move_to_folder(filepath, folder)
                    moved = True
                    break
            if not moved:
                logging.info(f"No matching keyword for {filename}")

# ===============================
# GUI Setup
# ===============================
root = tk.Tk()
root.title("Dynamic File Organizer")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ===================== Extension Organizer Tab =====================
extension_frame = ttk.Frame(notebook)
notebook.add(extension_frame, text="Extension Organizer")

# --- Multi-Source Folders ---
tk.Label(extension_frame, text="Source Folders:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ext_source_listbox = tk.Listbox(extension_frame, width=60, height=5)
ext_source_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

def add_ext_source():
    folder = filedialog.askdirectory(title="Select Source Folder")
    if folder:
        ext_source_listbox.insert(tk.END, folder)

def remove_ext_source():
    selected = ext_source_listbox.curselection()
    for index in reversed(selected):
        ext_source_listbox.delete(index)

tk.Button(extension_frame, text="Add Source Folder", command=add_ext_source).grid(row=2, column=0, padx=5, pady=5)
tk.Button(extension_frame, text="Remove Selected", command=remove_ext_source).grid(row=2, column=1, padx=5, pady=5)

# --- Custom Rules ---
tk.Label(extension_frame, text="Custom Rules (Extensions -> Destination Folder):").grid(row=3, column=0, padx=5, pady=5, sticky="w")

tk.Label(extension_frame, text="Extensions (comma-separated):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
rule_extensions_entry = tk.Entry(extension_frame, width=30)
rule_extensions_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

tk.Label(extension_frame, text="Destination Folder:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
rule_dest_var = tk.StringVar()
rule_dest_entry = tk.Entry(extension_frame, textvariable=rule_dest_var, width=30)
rule_dest_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

def browse_rule_dest():
    folder = filedialog.askdirectory(title="Select Destination Folder for Rule")
    if folder:
        rule_dest_var.set(folder)

tk.Button(extension_frame, text="Browse", command=browse_rule_dest).grid(row=5, column=2, padx=5, pady=5)

# Listbox to show added rules
tk.Label(extension_frame, text="Added Rules:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
ext_rules_listbox = tk.Listbox(extension_frame, width=60, height=5)
ext_rules_listbox.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky="w")

def add_rule():
    exts = rule_extensions_entry.get().strip()
    dest = rule_dest_var.get().strip()
    if not exts or not dest:
        messagebox.showerror("Error", "Please enter both extensions and destination folder for the rule.")
        return
    # Process the extensions (split by comma, remove whitespace, lower-case them)
    ext_list = [e.strip().lower() for e in exts.split(',') if e.strip()]
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    rule = {'extensions': ext_list, 'dest': dest_path}
    custom_rules.append(rule)
    ext_rules_listbox.insert(tk.END, f"Extensions: {', '.join(ext_list)} -> {dest}")
    # Clear the entries
    rule_extensions_entry.delete(0, tk.END)
    rule_dest_var.set("")
    save_rules()

def remove_rule():
    selected = ext_rules_listbox.curselection()
    for index in reversed(selected):
        ext_rules_listbox.delete(index)
        del custom_rules[index]
    save_rules()

tk.Button(extension_frame, text="Add Rule", command=add_rule).grid(row=8, column=0, padx=5, pady=5)
tk.Button(extension_frame, text="Remove Selected Rule", command=remove_rule).grid(row=8, column=1, padx=5, pady=5)

# --- Default Destination Folder ---
tk.Label(extension_frame, text="Default Destination Folder (if no rule matches):").grid(row=9, column=0, padx=5, pady=5, sticky="e")
default_dest_var = tk.StringVar()
default_dest_entry = tk.Entry(extension_frame, textvariable=default_dest_var, width=30)
default_dest_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

def browse_default_dest():
    folder = filedialog.askdirectory(title="Select Default Destination Folder")
    if folder:
        default_dest_var.set(folder)

tk.Button(extension_frame, text="Browse", command=browse_default_dest).grid(row=9, column=2, padx=5, pady=5)

def organize_by_extension():
    # Get all source folders from the listbox
    sources = ext_source_listbox.get(0, tk.END)
    if not sources:
        messagebox.showerror("Error", "Please add at least one source folder.")
        return
    # Get the default destination folder if specified
    default_dest = default_dest_var.get().strip()
    default_dest_path = Path(default_dest) if default_dest else None

    for src in sources:
        src_path = Path(src)
        if src_path.exists():
            move_files_by_custom_rules(src_path, custom_rules, default_dest_path)
        else:
            logging.error(f"Source folder does not exist: {src}")
    logging.info("Extension-based organization completed.")
    messagebox.showinfo("Success", "Files organized by extension successfully!")

tk.Button(extension_frame, text="Organize by Extension", command=organize_by_extension).grid(row=10, column=0, columnspan=3, pady=10)

# ===================== Keyword Organizer Tab =====================
keyword_frame = ttk.Frame(notebook)
notebook.add(keyword_frame, text="Keyword Organizer")

# --- Multi-Source Folders ---
tk.Label(keyword_frame, text="Source Folders:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
keyword_source_listbox = tk.Listbox(keyword_frame, width=60, height=5)
keyword_source_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

def add_keyword_source():
    folder = filedialog.askdirectory(title="Select Source Folder")
    if folder:
        keyword_source_listbox.insert(tk.END, folder)

def remove_keyword_source():
    selected = keyword_source_listbox.curselection()
    for index in reversed(selected):
        keyword_source_listbox.delete(index)

tk.Button(keyword_frame, text="Add Source Folder", command=add_keyword_source).grid(row=2, column=0, padx=5, pady=5)
tk.Button(keyword_frame, text="Remove Selected", command=remove_keyword_source).grid(row=2, column=1, padx=5, pady=5)

# --- Config File for Keyword Rules ---
tk.Label(keyword_frame, text="Config File (for keyword rules):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
keyword_config_var = tk.StringVar()
keyword_config_entry = tk.Entry(keyword_frame, textvariable=keyword_config_var, width=40)
keyword_config_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

def browse_keyword_config():
    file = filedialog.askopenfilename(title="Select Config File", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file:
        keyword_config_var.set(file)

tk.Button(keyword_frame, text="Browse", command=browse_keyword_config).grid(row=3, column=2, padx=5, pady=5)

def organize_by_keyword():
    sources = keyword_source_listbox.get(0, tk.END)
    if not sources:
        messagebox.showerror("Error", "Please add at least one source folder.")
        return
    config_path = keyword_config_var.get().strip()
    if not config_path:
        messagebox.showerror("Error", "Please select a config file.")
        return

    try:
        config_path_obj = Path(config_path)
        with config_path_obj.open('r') as f:
            config_data = json.load(f)
        if 'folders' not in config_data:
            messagebox.showerror("Error", "Config file is missing the 'folders' key.")
            return

        folders_mapping = {key: Path(value) for key, value in config_data['folders'].items()}
        for folder in folders_mapping.values():
            folder.mkdir(parents=True, exist_ok=True)

        for src in sources:
            src_path = Path(src)
            if src_path.exists():
                move_files_by_keyword(src_path, folders_mapping)
            else:
                logging.error(f"Source folder does not exist: {src}")
        logging.info("Keyword-based organization completed.")
        messagebox.showinfo("Success", "Files organized by keyword successfully!")
    except Exception as e:
        logging.error(f"Error in organizing by keyword: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

tk.Button(keyword_frame, text="Organize by Keyword", command=organize_by_keyword).grid(row=4, column=0, columnspan=3, pady=10)

# ===============================
# Load persisted extension rules (if any) before starting the GUI loop.
load_rules()

# ===============================
# Start the GUI Event Loop
# ===============================
root.mainloop()
