import sys
import re

MAX_LINE_WIDTH = 100

NESTING_COLORS = {
    0: '\033[94m', 1: '\033[92m', 2: '\033[93m', 3: '\033[91m',
    4: '\033[95m', 5: '\033[96m', 6: '\033[33m', 7: '\033[36m',
    8: '\033[37m', 9: '\033[41m', 10: '\033[42m', 11: '\033[43m',
    12: '\033[44m', 'default': '\033[97m'
}

RESET = '\033[0m'

def get_indent_level(line: str) -> int:
    return len(line) - len(line.lstrip(' '))

def get_arrow_color_for_depth(depth):
    return NESTING_COLORS.get(depth % len(NESTING_COLORS), RESET)

def print_box(flowchart, stmt, depth, current_width, color):
    indent = " " * (depth * 4)
    box_width = len(stmt) + 6

    if current_width + box_width > MAX_LINE_WIDTH:
        flowchart.append("")
        current_width = 0

    flowchart.append(f"{indent}{color}+{'-' * box_width}+{RESET}")
    flowchart.append(f"{indent}{color}|  {stmt.ljust(box_width - 4)}  |{RESET}")
    flowchart.append(f"{indent}{color}+{'-' * box_width}+{RESET}")

    return current_width + box_width

def is_control_statement(line):
    return re.match(r'^\s*(if|elif|else|for|while|try|except|finally)\b', line)

def generate_flowchart_from_python(code: str) -> str:
    lines = code.strip().splitlines()
    flowchart = []
    indent_stack = [0]
    depth = 0
    current_width = 0
    inside_multiline_comment = False
    last_indent = 0
    last_was_control = False

    for i, raw_line in enumerate(lines):
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if line.startswith("#!") and len(flowchart) == 0:
            continue  # Skip shebang

        stripped = line.strip()
        indent = get_indent_level(line)

        # Multiline comment block handling
        if inside_multiline_comment:
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            if '"""' in stripped or "'''" in stripped:
                inside_multiline_comment = False
            continue

        if stripped.startswith(("'''", '\"\"\"')):
            inside_multiline_comment = not inside_multiline_comment
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            continue

        # Decrement depth if comment follows control block or dedentation
        if stripped.startswith("#"):
            if indent < indent_stack[-1] or last_was_control:
                while indent < indent_stack[-1]:
                    indent_stack.pop()
                    depth -= 1
                last_was_control = False
            current_width = print_box(flowchart, stripped, depth, current_width, NESTING_COLORS[8])
            last_indent = indent
            continue

        # Indentation-based depth adjustment
        while indent < indent_stack[-1]:
            indent_stack.pop()
            depth -= 1

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            depth += 1

        color = get_arrow_color_for_depth(depth)
        current_width = print_box(flowchart, stripped, depth, current_width, color)

        last_was_control = is_control_statement(stripped)
        last_indent = indent

    return "\n".join(flowchart)

def main():
    if len(sys.argv) != 2:
        print("Usage: python flowchart_generator_for_python.py <python_file.py>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            code = file.read()
            flowchart = generate_flowchart_from_python(code)
            print(flowchart)
            print(RESET)  # Ensure terminal color resets at the end
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(RESET)

if __name__ == "__main__":
    main()

