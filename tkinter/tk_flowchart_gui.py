import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re

# ---------- Config ----------
MAX_LINE_WIDTH = 100
RESET = '\033[0m'

NESTING_COLORS = {
    0: '\033[94m', 1: '\033[92m', 2: '\033[93m', 3: '\033[91m',
    4: '\033[95m', 5: '\033[96m', 6: '\033[33m', 7: '\033[36m',
    8: '\033[37m', 9: '\033[41m', 10: '\033[42m', 11: '\033[43m',
    12: '\033[44m', 'default': '\033[97m'
}

ANSI_COLORS = {
    '\033[94m': 'blue',
    '\033[92m': 'green',
    '\033[93m': 'yellow',
    '\033[91m': 'red',
    '\033[95m': 'magenta',
    '\033[96m': 'cyan',
    '\033[33m': 'orange',
    '\033[36m': 'teal',
    '\033[37m': 'gray',
    '\033[41m': 'white_on_red',
    '\033[42m': 'white_on_green',
    '\033[43m': 'white_on_yellow',
    '\033[44m': 'white_on_blue',
    '\033[97m': 'white',
    '\033[0m': 'reset',
}

# ---------- Flowchart Rendering ----------
def get_arrow_color_for_depth(depth):
    return NESTING_COLORS.get(depth % len(NESTING_COLORS), RESET)

def print_box(flowchart, stmt, depth, current_width, color):
    indent = " " * (depth * 4)
    lines = stmt.split("\n")
    max_line = max(len(line) for line in lines)
    box_width = max_line + 6

    if current_width + box_width > MAX_LINE_WIDTH:
        flowchart.append("")
        current_width = 0

    flowchart.append(f"{indent}{color}+{'-' * box_width}+{RESET}")
    for line in lines:
        flowchart.append(f"{indent}{color}|  {line.ljust(box_width - 4)}  |{RESET}")
    flowchart.append(f"{indent}{color}+{'-' * box_width}+{RESET}")

    return current_width + box_width

# ---------- Python Parser ----------
def get_indent_level(line):
    return len(line) - len(line.lstrip(' '))

def is_control_statement(line):
    return re.match(r'^\s*(if|elif|else|for|while|try|except|finally)\b', line)

def generate_flowchart_from_python(code):
    lines = code.strip().splitlines()
    flowchart = []
    indent_stack = [0]
    depth = 0
    current_width = 0
    inside_multiline_comment = False
    last_was_control = False

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        indent = get_indent_level(line)

        if inside_multiline_comment:
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            if '"""' in stripped or "'''" in stripped:
                inside_multiline_comment = False
            continue

        if stripped.startswith(("'''", '\"\"\"')):
            inside_multiline_comment = not inside_multiline_comment
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            continue

        if stripped.startswith("#"):
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            continue

        while indent < indent_stack[-1]:
            indent_stack.pop()
            depth -= 1

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            depth += 1

        color = get_arrow_color_for_depth(depth)
        current_width = print_box(flowchart, stripped, depth, current_width, color)
        last_was_control = is_control_statement(stripped)

    return "\n".join(flowchart)

# ---------- C Parser ----------
def process_code_line(flowchart, stmt, nesting_depth, current_width, color):
    shift = " " * (nesting_depth * 4)
    lines = stmt.split("\n")
    max_line = max(len(line) for line in lines)
    box_width = max_line + 6

    if current_width + box_width > MAX_LINE_WIDTH:
        flowchart.append("")
        current_width = 0

    flowchart.append(f"{shift}{color}+{'-' * box_width}+{RESET}")
    for line in lines:
        flowchart.append(f"{shift}{color}|  {line.ljust(box_width - 4)}  |{RESET}")
    flowchart.append(f"{shift}{color}+{'-' * box_width}+{RESET}")

    return current_width + box_width

def generate_flowchart_from_c_code(code):
    lines = code.strip().splitlines()
    flowchart = []
    nesting_depth = 0
    brace_stack = []
    current_width = 0
    increment_next = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Grouped headed comment block
        if line.startswith("/*") and not line.endswith("*/"):
            comment_block = [line]
            i += 1
            while i < len(lines):
                line = lines[i].strip()
                comment_block.append(line)
                if line.endswith("*/"):
                    break
                i += 1
            grouped_comment = "\n".join(comment_block)
            current_width = process_code_line(flowchart, grouped_comment, nesting_depth, current_width, NESTING_COLORS[8])
            i += 1
            continue

        # One-line comment block
        elif line.startswith("/*") and line.endswith("*/"):
            current_width = process_code_line(flowchart, line, nesting_depth, current_width, NESTING_COLORS[8])
            i += 1
            continue

        if not line:
            i += 1
            continue

        if re.match(r"^(if|for|while|else if|else)\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth, current_width, get_arrow_color_for_depth(nesting_depth))
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if next_line == "{":
                brace_stack.append("{")
                nesting_depth += 1
                i += 1
                continue
            elif not next_line.startswith("{"):
                increment_next = True
            i += 1
            continue

        if increment_next:
            current_width = process_code_line(flowchart, line, nesting_depth + 1, current_width, get_arrow_color_for_depth(nesting_depth + 1))
            increment_next = False
            i += 1
            continue

        if line == "{":
            brace_stack.append("{")
            nesting_depth += 1
            i += 1
            continue
        elif line == "}":
            if brace_stack:
                brace_stack.pop()
                nesting_depth -= 1
            i += 1
            continue

        current_width = process_code_line(flowchart, line, nesting_depth, current_width, get_arrow_color_for_depth(nesting_depth))
        i += 1

    return "\n".join(flowchart)

# ---------- ANSI Rendering in Tkinter ----------
def setup_tags(widget):
    widget.tag_config('blue', foreground='#82AAFF')             # keywords/includes
    widget.tag_config('green', foreground='#C3E88D')            # declarations
    widget.tag_config('yellow', foreground='#FFCB6B')           # conditions
    widget.tag_config('red', foreground='#F07178')              # errors
    widget.tag_config('magenta', foreground='#C792EA')          # types
    widget.tag_config('cyan', foreground='#89DDFF')             # flow
    widget.tag_config('orange', foreground='#F78C6C')           # constants
    widget.tag_config('teal', foreground='#6FC1FF')             # return
    widget.tag_config('gray', foreground='#888888')             # comments
    widget.tag_config('white_on_red', foreground='white', background='#B00020')
    widget.tag_config('white_on_green', foreground='black', background='#00C853')
    widget.tag_config('white_on_yellow', foreground='black', background='#FFD600')
    widget.tag_config('white_on_blue', foreground='white', background='#2962FF')
    widget.tag_config('white', foreground='white')
    widget.tag_config('reset', foreground='white')

def insert_ansi_text(widget, ansi_text):
    ansi_regex = re.compile(r'(\033\[\d+m)')
    parts = ansi_regex.split(ansi_text)

    current_tag = None
    for part in parts:
        if part in ANSI_COLORS:
            current_tag = ANSI_COLORS[part]
        else:
            widget.insert(tk.END, part, current_tag)

# ---------- File Handling ----------
def detect_language(path):
    if path.endswith('.py'):
        return 'python'
    elif path.endswith('.c'):
        return 'c'
    return None

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Code Files", "*.py *.c")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as f:
            code = f.read()

        lang = detect_language(file_path)
        if lang == 'python':
            result = generate_flowchart_from_python(code)
        elif lang == 'c':
            result = generate_flowchart_from_c_code(code)
        else:
            messagebox.showerror("Unsupported file", "Only .py and .c files are supported.")
            return

        output_text.delete(1.0, tk.END)
        insert_ansi_text(output_text, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Zoom Functionality ----------
zoom_level = 10  # Default zoom level for the font size
def zoom_in():
    global zoom_level
    zoom_level += 2
    output_text.config(font=("Courier New", zoom_level))

def zoom_out():
    global zoom_level
    zoom_level = max(6, zoom_level - 2)  # Prevent too small font size
    output_text.config(font=("Courier New", zoom_level))

# ---------- GUI ----------
root = tk.Tk()
root.title("Flowchart Generator (.c / .py)")
root.configure(bg="#1e1e1e")

frame = tk.Frame(root, bg="#1e1e1e", padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

btn = tk.Button(frame, text="Open .py or .c File", command=open_file, bg="#333", fg="white")
btn.pack(pady=(0, 10))

output_text = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    width=100,
    height=40,
    font=("Courier New", zoom_level),
    bg="#121212",
    fg="white",
    insertbackground="white"
)
output_text.pack(fill=tk.BOTH, expand=True)

# Zoom buttons
zoom_frame = tk.Frame(root, bg="#1e1e1e")
zoom_frame.pack(pady=10, anchor="w")

zoom_in_btn = tk.Button(zoom_frame, text="Zoom In", command=zoom_in, bg="#333", fg="white")
zoom_in_btn.pack(side=tk.LEFT, padx=5)

zoom_out_btn = tk.Button(zoom_frame, text="Zoom Out", command=zoom_out, bg="#333", fg="white")
zoom_out_btn.pack(side=tk.LEFT, padx=5)

setup_tags(output_text)
root.mainloop()

