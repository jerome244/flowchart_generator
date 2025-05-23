import sys
import re
import os

# Limit the maximum width before wrapping to a new "column"
MAX_LINE_WIDTH = 100  # Adjust this to your preferred limit

# Define colors for different nesting depths (extend this list as needed)
NESTING_COLORS = {
    0: '\033[94m',  # Blue
    1: '\033[92m',  # Green
    2: '\033[93m',  # Yellow
    3: '\033[91m',  # Red
    4: '\033[95m',  # Magenta (Pink)
    5: '\033[96m',  # Cyan
    6: '\033[33m',  # Orange
    7: '\033[36m',  # Teal
    8: '\033[37m',  # Gray
    9: '\033[41m',  # Background Red
    10: '\033[42m', # Background Green
    11: '\033[43m', # Background Yellow
    12: '\033[44m', # Background Blue
    'default': '\033[97m',  # White for default
}

RESET = '\033[0m'

def get_arrow_color_for_depth(depth):
    max_depth = len(NESTING_COLORS)
    return NESTING_COLORS.get(depth % max_depth, '\033[0m')


# Python-specific flowchart generator functions
def get_indent_level(line: str) -> int:
    return len(line) - len(line.lstrip(' '))

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


# C-specific flowchart generator functions
def process_code_line(flowchart, stmt, nesting_depth, current_width, color, include_line_number=True):
    shift = " " * (nesting_depth * 10)
    stmt_length = len(stmt) + 12  # Account for padding inside the box

    if current_width + stmt_length > MAX_LINE_WIDTH:
        flowchart.append("")
        current_width = 0

    flowchart.append(f"{shift}{color}+{'-' * stmt_length}+{RESET}")
    flowchart.append(f"{shift}{color}|  {stmt.ljust(len(stmt) + 8)}   |{RESET}")  # 1 space removed here
    flowchart.append(f"{shift}{color}+{'-' * stmt_length}+{RESET}")

    current_width += stmt_length
    return current_width

def process_multiple_statements_on_same_line(flowchart, line, nesting_depth, current_width, color):
    statements = line.split(";")
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            current_width = process_code_line(flowchart, stmt, nesting_depth, current_width, color)
    return current_width

def generate_flowchart_from_c_code(code: str) -> str:
    lines = code.strip().split('\n')
    flowchart = []
    nesting_depth = 0
    inside_comment = False
    comment_block = []
    brace_stack = []
    current_width = 0

    comments = []
    includes = []
    functions = []
    declarations = []
    code_lines = []

    line_number = 1
    increment_next = False

    for line in lines:
        line = line.strip()

        if not line:
            line_number += 1
            continue

        if line.startswith("/*"):
            inside_comment = True
            comment_block.append(line)
        elif inside_comment:
            comment_block.append(line)
            if line.endswith("*/"):
                comments.append("\n".join(comment_block))
                inside_comment = False
                comment_block = []
        elif line.startswith("#include"):
            includes.append(line)
        elif re.match(r"\w+\s+\w+\s*\(.*\)\s*;", line) and not re.match(r".*=\s*malloc.*", line):
            functions.append(line)
        elif re.match(r"(\w+\s+\**\w+\s*=.*|\w+\s+\**\w+)", line):
            declarations.append(line)
        else:
            code_lines.append(line)

    # Colorized comments section (Gray), no '|' in comments
    if comments:
        flowchart.append("Comments:")
        for comment in comments:
            current_width = process_code_line(flowchart, comment, nesting_depth, current_width, NESTING_COLORS[8], include_line_number=False)
            line_number += 1
        flowchart.append("")

    # Colorized preprocessor directives (Blue)
    if includes:
        flowchart.append("Preprocessor Directives:")
        for include in includes:
            current_width = process_code_line(flowchart, include, nesting_depth, current_width, NESTING_COLORS[0], include_line_number=False)
            line_number += 1
        flowchart.append("")

    # Variable Declarations Section
    if declarations:
        flowchart.append("Function Declaration:")

        # First declaration: pink, depth 0
        current_width = process_code_line(flowchart, declarations[0], 0, current_width, NESTING_COLORS[4], include_line_number=False)
        flowchart.append("")  # Newline after first declaration
        flowchart.append("Variable Declarations:")

        # Remaining declarations: gray, depth 1
        for declaration in declarations[1:]:
            current_width = process_code_line(flowchart, declaration, 1, current_width, NESTING_COLORS[8], include_line_number=False)
            line_number += 1
        flowchart.append("")

    # Function declarations (Blue)
    if functions:
        flowchart.append("Function Declarations:")
        for func in functions:
            current_width = process_code_line(flowchart, func, 0, current_width, NESTING_COLORS[0])
            line_number += 1
        flowchart.append("")

    flowchart.append("Function Logic Starts:")

    nesting_depth = 1  # Start logic at depth 1

    i = 0
    while i < len(code_lines):
        line = code_lines[i].strip()

        if re.match(r"^(if|for|while|else if|else)\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth, current_width, NESTING_COLORS.get(nesting_depth, '\033[0m'))
            next_line = code_lines[i + 1].strip() if i + 1 < len(code_lines) else ""
            if next_line == "{":
                brace_stack.append("{")
                nesting_depth += 1
                i += 1
                continue
            if not next_line.startswith("{"):
                increment_next = True
            i += 1
            continue

        if increment_next:
            current_width = process_code_line(flowchart, code_lines[i].strip(), nesting_depth + 1, current_width, NESTING_COLORS.get(nesting_depth + 1, '\033[0m'))
            increment_next = False
            i += 1
            continue

        if line == "{":
            i += 1
            continue
        elif line == "}":
            if brace_stack:
                brace_stack.pop()
                nesting_depth -= 1
            i += 1
            continue

        current_width = process_multiple_statements_on_same_line(flowchart, line, nesting_depth, current_width, NESTING_COLORS.get(nesting_depth, '\033[0m'))
        i += 1

    return "\n".join(flowchart)


# Unified entry point
def main():
    if len(sys.argv) != 2:
        print("Usage: python flowchart_generator.py <file path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as file:
            code = file.read()

            if file_path.endswith(".py"):
                flowchart = generate_flowchart_from_python(code)
            elif file_path.endswith(".c"):
                flowchart = generate_flowchart_from_c_code(code)
            else:
                print("Unsupported file type. Please provide a Python (.py) or C (.c) file.")
                sys.exit(1)

            print(flowchart)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

