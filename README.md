<p align="center">
  <img src="https://github.com/your-username/flowchart-converter/blob/main/screenshots/banner.png?raw=true" alt="Flowchart Converter Banner">
</p>

# 🧠 Flowchart Converter

> Turn your C code into structured, visual flowcharts.  
> Perfect for students, developers, and anyone looking to understand program logic at a glance.

---

## 📌 Table of Contents

- [📝 Introduction](#-introduction)
- [⚙️ Features](#️-features)
- [💻 Usage](#-usage)
- [🖼️ Screenshots](#-screenshots)
- [📁 Project Structure](#-project-structure)
- [🌐 Web Version](#-web-version)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

## 📝 Introduction

**Flowchart Converter** is a simple tool that takes a C source file and transforms its logic into a clear, structured flowchart using Unicode box drawing.  
It visually separates conditional and looping branches, and highlights nesting levels with indentation and color coding.

---

## ⚙️ Features

- ✅ Supports conditionals (`if`, `else`, `switch`) and loops (`while`, `for`, `do-while`)
- ✅ Braces (`{}`) are optional — works with one-liners
- ✅ Indented, color-coded flowcharts using Unicode
- ✅ Runs via Python script or compiled C binary
- ✅ Control flow branches are visually offset to the right
- 🌐 Web version in progress!

---

## 💻 Usage

### 🔧 Requirements

- Python 3 installed  
_OR_  
- GCC for C version

### ▶️ Run the Python version

```bash
python3 flowchart_generator.py yourCfile.c
```

### ⚙️ Compile and run the C version

```bash
gcc flowchart_generator.c -o flowchart_generator
./flowchart_generator yourCfile.c
```

> Replace `yourCfile.c` with your own C source file.

---

## 🖼️ Screenshots

<p align="center">
  <b>📄 Input C Code</b><br>
  <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/cSnippetExample.png" width="400">
</p>

<p align="center">
  <b>🧱 Output - C Version</b><br>
  <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/c_version.png" width="400">
</p>

<p align="center">
  <b>🐍 Output - Python Version</b><br>
  <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/python_version.png" width="400">
</p>

---

## 📁 Project Structure

| File/Folder | Description |
|-------------|-------------|
| `flowchart_generator.py` | Python version of the flowchart generator |
| `flowchart_generator.c` | C version of the flowchart generator |
| `screenshots/` | Contains images used in this README |
| `README.md` | Project documentation |
| `LICENSE` | License file (MIT recommended) |

---

## 🌐 Web Version

The **Web Flowchart Generator** is under development!  
You’ll soon be able to paste or upload your C code directly into a browser and see the flowchart instantly.

> 🌍 Stay tuned for a live demo!

---

## 👨‍💻 Author

**Your Name**  
🔗 GitHub: [@your-username](https://github.com/your-username)

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---


