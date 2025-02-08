# Dynamic File Organizer

## Overview
The **Dynamic File Organizer** is a Python-based automation tool that organizes files based on their **extensions** or **keywords** in filenames. It provides a **Graphical User Interface (GUI)** for easy folder selection, rule definition, and persistent automation.

## Features
- **Organize by File Extension** – Move files to specific folders based on extensions (e.g., `.pdf`, `.jpg`, `.txt`).
- **Organize by Keyword** – Move files to predefined folders based on keywords in filenames.
- **Multi-Folder Selection** – Users can define multiple source folders for file organization.
- **Custom Rules** – Users can create extension-based and keyword-based rules for organizing files.
- **Persistent Rule Storage** – Custom rules are saved in `extension_rules.json` so they persist across sessions.
- **Graphical User Interface (GUI)** – Built with Tkinter for easy rule setup and execution.
- **Logging System** – Logs file movements and errors for tracking.

## Requirements
- **Python 3.x**
- Required Python libraries:
  ```sh
  pip install tk
  ```

## Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/mayur-salokhe/Dynamic_File_Organizer.git
   cd dynamic-file-organizer
   ```
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the script**:
   ```sh
   python dynamic_file_organizer.py
   ```

## Configuration
### **Keyword-Based Organization**
Create a `config.json` file with the following structure to map keywords to folders:
```json
{
  "folders": {
    "invoice": "C:/Documents/Invoices",
    "report": "C:/Documents/Reports"
  }
}
```

### **Persistent Custom Rules**
- Extension-based rules are stored in `extension_rules.json`.
- These rules are **automatically loaded** upon application startup.

## Usage
### **Running the Application**
1. Launch the script:
   ```sh
   python dynamic_file_organizer.py
   ```
2. The GUI opens with two main tabs:
   - **Extension Organizer** – Add source folders, define extension rules, and select a default destination folder.
   - **Keyword Organizer** – Add source folders and use the `config.json` file for keyword-based sorting.

### **Organizing by File Extension**
- Select multiple source folders.
- Define rules by associating extensions with destination folders.
- Click **"Organize by Extension"** to move files accordingly.

### **Organizing by Keyword**
- Select multiple source folders.
- Choose a `config.json` file mapping keywords to destination folders.
- Click **"Organize by Keyword"** to start sorting.

## Logging
- Log files are stored in `C:/Dyanmic_File_Organizer/` with the format:
  ```
  dynamic_file_orgnanizer_log_YYYY-MM-DD.log
  ```
- Each log entry includes timestamps and details of file movements.

## Troubleshooting
- **Files Not Moving?**
  - Ensure filenames match the specified keywords or extensions.
  - Check the log file for errors.
- **Application Issues?**
  - Verify Python and Tkinter are installed.
  - Ensure required JSON configuration files are available.

## Future Enhancements
- Add scheduling for automated organization.
- Implement drag-and-drop functionality for file selection.
- Provide an option to undo file movements.

## License
This project is licensed under the MIT License.

## Author
Developed by **Mayur Salokhe**

---
_If you like this project, consider giving it a ⭐ on GitHub!_

