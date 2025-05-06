# Flowchart Generator

A **Python-based application** for generating **flowcharts** from `.c` and `.py` code files. This app is built with **Tkinter** and allows for **zooming** in/out of flowchart visualizations, **grouped header comments** for C functions, and a **dark mode** theme.

## Features

- **Supports `.py` and `.c` code files** for flowchart generation.
- **Dark mode GUI** for better readability.
- **Zoom In/Out functionality** for increasing/decreasing the flowchart font size.
- **Grouped header comments** in C code are displayed as one block instead of individual lines.
- **Color-coded flowchart** with customized colors for different code sections and structures (e.g., keywords, comments, variables).

## Requirements

The application requires **Python 3** and the following libraries:

- **Tkinter** (for the GUI)
- **re** (for regular expressions)
- **scrolledtext** (for the scrollable text widget)

These are included in most Python installations, but you can install Tkinter manually if missing:

### On Linux:
```bash
sudo apt install python3-tk
### On Windows/macOS:
Tkinter is generally bundled with the standard Python installation. If you're missing it, install the latest version from python.org.

## Installation
Clone the repository or download the script:
Download tk_flowchart_gui.py to your local machine.

Install required dependencies:
If Tkinter or other dependencies are missing, you can install them via pip:

bash
pip install tk
### Usage
Run the Python script:
Execute the script with Python:

bash
python tk_flowchart_gui.py
Open .py or .c files:

Use the "Open .py or .c File" button to choose a Python or C source code file.

The flowchart will be generated and displayed in a scrollable window with zoomable text.

Zoom In / Zoom Out:

Use the Zoom In and Zoom Out buttons located at the bottom left of the window to adjust the flowchart's font size.

### Packaging as Executable
If you want to distribute the app as a standalone executable (e.g., .exe for Windows), use PyInstaller.

Step 1: Install PyInstaller
bash
pip install pyinstaller
Step 2: Create the Executable
Run the following command to generate a standalone .exe file:

bash
pyinstaller --noconsole --onefile tk_flowchart_gui.py
This will create the executable in the dist/ folder.

Step 3: Running the Executable
Simply double-click the .exe file from the dist/ folder to run the app.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

yaml

---

### How to Use:

1. **Save the file** as `README.md` in your project folder.
2. **Follow the instructions** inside to install dependencies, run the Python script, or package it as an executable.
  
Let me know if you need any more modifications!
