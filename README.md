# Dynamic_File_Organizer

## Overview
The **Dynamic File Organizer** is a Python-based application that helps users organize files either by **file extensions** or **keywords** found in filenames. It provides a **GUI interface** using Tkinter, making it easy for users to select folders and organize files efficiently. Logging is enabled to keep track of file movements.

## Features
- **Organize by File Extension:** Move files to a specified folder based on their extensions.
- **Organize by Keyword:** Move files to predefined folders based on keywords in filenames (configured via a JSON file).
- **Graphical User Interface (GUI):** Allows easy folder and config selection.
- **Logging:** Records file movements and errors.

## Requirements
- Python 3.x
- Required libraries: `tkinter`, `shutil`, `os`, `json`, `pathlib`, `datetime`, `logging`

## Installation
1. Ensure Python is installed.
2. Install required dependencies (Tkinter is included in standard Python installations):
   ```sh
   pip install tk
   ```
3. Save the `dynamic_file_organizer.py` script and ensure the `config.json` file is available in the same directory (if using keyword-based organization).

## Configuration
For **keyword-based organization**, create a `config.json` file in the same directory as the script with the following structure:
```json
{
  "folders": {
    "invoice": "C:/Documents/Invoices",
    "report": "C:/Documents/Reports"
  }
}
```

## Usage
### Running the Application
1. Open a terminal or command prompt and run:
   ```sh
   python dynamic_file_organizer.py
   ```
2. The GUI will open with two tabs:
   - **Extension Organizer:** Choose a source folder, specify file extensions, and select a destination folder.
   - **Keyword Organizer:** Choose a source folder and select a config file with keyword-folder mappings.

### Organizing by File Extension
1. Select the **source folder** (default is Downloads).
2. Select the **destination folder** where matched files should be moved.
3. Enter **file extensions** (comma-separated, e.g., `.pdf, .jpg, .txt`).
4. Click **Organize by Extension**.

### Organizing by Keyword
1. Select the **source folder** (default is Downloads).
2. Select the **config file** (JSON format).
3. Click **Organize by Keyword**.

## Logging
- Log files are stored in `C:/Download_Folder_Automation/` with filenames like:
  ```
  download_automation_log_YYYY-MM-DD.log
  ```
- Each log entry contains timestamps, file movements, and errors (if any).

## Troubleshooting
- If a file isn’t moving:
  - Ensure the filename matches the specified keyword (for keyword-based organization).
  - Check the file extension format (for extension-based organization).
  - Look at the log file for errors.
- If the application doesn’t start:
  - Ensure Python and Tkinter are installed.
  - Check for missing dependencies.

## Future Enhancements
- Support for scheduling automated file organization.
- Add a feature to revert moved files.
- Allow drag-and-drop file selection in the GUI.

## License
This project is open-source and available for modification and distribution.

---

**Author:** Mayur Salokhe  
**Last Updated:** 2025-02-07

