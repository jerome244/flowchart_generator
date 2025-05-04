<p align="center">
  <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/banner.png?raw=true" alt="Flowchart Converter Banner">
</p>

# 🧠 Code Reading/ Diagram Understand Helper

> Turn your C code into structured, visual flowcharts.  
> Perfect for students, developers, and anyone looking to understand program logic at a glance.
> More of a diagram/flowchart helper-maker and understanding tool, designed to help visualize C code logic in a clear, structured way.
---

## 📌 Table of Contents

- [📝 Introduction](#-introduction)
- [⚙️ Features](#️-features)
- [💻 Usage](#-usage)
- [🖼️ Screenshots](#-screenshots)
- [📁 Project Structure](#-project-structure)
- [🌐 Web Version](#-web-version)
- [📖 How to Use/Read this Flowchart](#how-to-use-read-this-flowchart)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

## 📝 Introduction

**Code Reading/ Diagram Understand Helper** is a simple tool that takes a C source file and transforms its logic into a clear, structured code using Unicode box drawing.  
It visually separates conditional and looping branches, and highlights nesting levels with indentation and color coding for an easier and fast understanding.

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

<p align="center"> <b>🌐 Web Preview - 1</b><br> <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/homepage.png?raw=true" width="400"> </p> 

<p align="center"> <b>🌐 Web Preview - 2</b><br> <img src="https://github.com/jerome244/flowchart_generator/blob/main/screenshots/generation.png?raw=true" width="400"> </p>
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

The Web Flowchart Generator is now live!

To use the web version, simply run the following command in your terminal:

bash
Copy code
python3 flowchart_server.py
Then, navigate to http://localhost:YOUR_PORT in your browser, where you can upload your C code, generate the flowchart, and enjoy the interactive features!

🌍 More features are on the way!

---

## 📖 How to Use/Read this Flowchart
This flowchart is designed to visually represent the control flow and structure of your C program. Here's how to read it:

1. Main Flow
The main flow of the program runs from top to bottom.

Each function or statement is shown as a box (e.g., a function call or variable assignment).

The main flow proceeds in a straight line unless a control flow structure (like an if or loop) alters it.

2. Control Statements
Conditionals (if, else, switch):

These are shown as blocks branching to the right of the main flow, indicating where decisions are made in the code.

For example, an if statement will have two branches: one for the condition being true, and another for it being false.

Loops (for, while, do-while):

Loops are represented by boxes that loop back to previous parts of the flow, indicating repetition.

For example, a for loop will show a box that cycles back to the loop’s condition check.

3. Indentation and Nesting
The flowchart uses indentation (tabs/spaces) to represent nesting levels, showing how deep the control flow is.

The more deeply indented a block is, the more nested it is within other structures (like a loop or if statement).

4. Colors
The flowchart uses different colors to indicate nesting depth, helping visualize how deep you are in the program’s logic.

Light colors: Shallow nesting.

Darker colors: Deeper nesting.

5. Input and Output
Boxes with labels like input() or output() represent where the program takes inputs (e.g., user input) or produces outputs (e.g., printing to the console).

By following the structure of the flowchart, you can easily trace how the program flows, see the control structures, and understand the overall logic of the code.

---

## 👨‍💻 Author

**Your Name**  
🔗 GitHub: [@jerome244](https://github.com/jerome244)

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---


