import sys
import re

MAX_LINE_WIDTH = 100

HTML_NESTING_COLORS = {
    0: '#1E90FF',  # Bright Dodger Blue
    1: '#32CD32',  # Bright Lime Green
    2: '#FFD700',  # Bright Gold
    3: '#FF4500',  # Bright Orange Red
    4: '#8A2BE2',  # Bright Blue Violet
    5: '#00CED1',  # Dark Turquoise
    6: '#FFA500',  # Bright Orange
    7: '#20B2AA',  # Light Sea Green
    8: '#D3D3D3',  # Light Gray
    9: '#A9A9A9',  # Dark Gray
    'default': '#FFFFFF',  # Default White
    'comment': '#D3D3D3'  # Light Gray for comments
}

def process_code_line(flowchart, stmt, depth, current_width, is_comment=False):
    color = HTML_NESTING_COLORS['comment'] if is_comment else HTML_NESTING_COLORS.get(depth, HTML_NESTING_COLORS['default'])
    shift = "&nbsp;" * (depth * 4)
    stmt_length = len(stmt) + 6

    if current_width + stmt_length > MAX_LINE_WIDTH:
        flowchart.append("<br>")
        current_width = 0

    border = f"{shift}<span style='color:{color}'>+{'-' * stmt_length}+</span><br>"
    content = f"{shift}<span style='color:{color}'>|  {stmt.ljust(stmt_length - 6)}  |  </span><br>"  # Added 2 spaces after the bar

    flowchart.extend([border, content, border])
    return current_width + stmt_length

def process_multiple_statements_on_same_line(flowchart, line, depth, current_width):
    statements = line.split(";")
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            current_width = process_code_line(flowchart, stmt, depth, current_width)
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
        elif re.match(r"(\w+\s+\**\w+\s*=.*|\w+\s+\**\w+)", line) and not re.match(r"^(if|for|while|else|else\s+if|switch)\b", line):
            declarations.append(line)
        else:
            code_lines.append(line)

    # Handling Comments (display in light gray)
    if comments:
        flowchart.append("<b>Comments:</b><br>")
        for comment in comments:
            current_width = process_code_line(flowchart, comment, nesting_depth, current_width, is_comment=True)
            line_number += 1
        flowchart.append("<br>")

    # Handling Preprocessor Directives
    if includes:
        flowchart.append("<b>Preprocessor Directives:</b><br>")
        for include in includes:
            current_width = process_code_line(flowchart, include, nesting_depth, current_width)
            line_number += 1
        flowchart.append("<br>")

    # Handling Declarations
    if declarations:
        flowchart.append("<b>Function Declaration:</b><br>")
        current_width = process_code_line(flowchart, declarations[0], 0, current_width)
        flowchart.append("<br><b>Variable Declarations:</b><br>")
        for declaration in declarations[1:]:
            current_width = process_code_line(flowchart, declaration, 1, current_width)
            line_number += 1
        flowchart.append("<br>")

    # Handling Function Declarations
    if functions:
        flowchart.append("<b>Function Declarations:</b><br>")
        for func in functions:
            current_width = process_code_line(flowchart, func, 0, current_width)
            line_number += 1
        flowchart.append("<br>")

    flowchart.append("<b>Function Logic Starts:</b><br>")
    nesting_depth = 1

    i = 0
    while i < len(code_lines):
        line = code_lines[i].strip()

        # Handling switch statement
        if re.match(r"^switch\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth, current_width)
            brace_stack.append("{")
            nesting_depth += 1
            i += 1
            continue
        
        # Handling case statements within a switch
        elif re.match(r"^case\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth + 1, current_width)
            i += 1
            continue

        # Handling default case within a switch
        elif re.match(r"^default\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth + 1, current_width)
            i += 1
            continue

        # Handling other conditionals (if, for, while, else, etc.)
        elif re.match(r"^(if|for|while|else if|else)\b", line):
            current_width = process_code_line(flowchart, line, nesting_depth, current_width)
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

        # Continue processing other logic as per the previous code...
        # Skipping the logic for if/else/while since it's already in your current code

        if increment_next:
            current_width = process_code_line(flowchart, code_lines[i].strip(), nesting_depth + 1, current_width)
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

        current_width = process_multiple_statements_on_same_line(flowchart, line, nesting_depth, current_width)
        i += 1

    return "<pre style='font-family: monospace'>" + "".join(flowchart) + "</pre>"

def main():
    if len(sys.argv) != 2:
        print("Usage: python flowchart_generator.py <C file path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            code = file.read()
            flowchart = generate_flowchart_from_c_code(code)
            print(flowchart)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

