import re
import html  # Import the html module to escape HTML entities

MAX_LINE_WIDTH = 100

# Define colors for different nesting levels (for text and box borders)
HTML_NESTING_COLORS = {
    0: '#1E90FF', 1: '#32CD32', 2: '#FFD700', 3: '#FF4500',
    4: '#8A2BE2', 5: '#00CED1', 6: '#FFA500', 7: '#20B2AA',
    8: '#D3D3D3', 9: '#A9A9A9', 'default': '#FFFFFF', 'comment': '#A9A9A9'
}

# Dark background for the flowchart boxes (matching website dark theme)
BOX_BACKGROUND_COLOR = "#1e1e1e"  # Dark gray for the boxes

def escape_html(text):
    """Escapes HTML special characters in the input text."""
    return html.escape(text)

def html_box(flowchart, stmt, depth, current_width, color):
    stmt = escape_html(stmt)  # Escape any HTML special characters
    indent = "&nbsp;" * (depth * 4)
    box_width = len(stmt) + 6

    # Color for the text and border based on nesting depth
    text_color = color  # Text color based on nesting depth
    
    if current_width + box_width > MAX_LINE_WIDTH:
        flowchart.append("<br>")
        current_width = 0

    border = f"{indent}<span style='background-color:{BOX_BACKGROUND_COLOR}; color:{text_color};'>+{'-' * box_width}+</span><br>"
    content = f"{indent}<span style='background-color:{BOX_BACKGROUND_COLOR}; color:{text_color};'>|  {stmt.ljust(box_width - 6)}  |</span><br>"

    flowchart.extend([border, content, border])
    return current_width + box_width

# -------------------- C CODE PARSER --------------------
def generate_flowchart_from_c_code(code: str) -> str:
    lines = code.strip().splitlines()
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
    increment_next = False

    for line in lines:
        line = line.strip()
        if not line:
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
        elif line.startswith("//"):
            comments.append(line)
        elif line.startswith("#include"):
            includes.append(line)
        elif re.match(r"\w+\s+\w+\s*\(.*\)\s*;", line) and not re.match(r".*=\s*malloc.*", line):
            functions.append(line)
        elif re.match(r"(\w+\s+\**\w+\s*=.*|\w+\s+\**\w+)", line) and not re.match(r"^(if|for|while|else|else\s+if|switch)\b", line):
            declarations.append(line)
        else:
            code_lines.append(line)

    # Header comments
    if comments:
        flowchart.append("<b>Comments:</b><br>")
        for comment in comments:
            current_width = html_box(flowchart, comment, nesting_depth, current_width, HTML_NESTING_COLORS['comment'])
        flowchart.append("<br>")

    # Preprocessor
    if includes:
        flowchart.append("<b>Preprocessor Directives:</b><br>")
        for include in includes:
            current_width = html_box(flowchart, include, nesting_depth, current_width, HTML_NESTING_COLORS.get(nesting_depth))
        flowchart.append("<br>")

    # Declarations
    if declarations:
        flowchart.append("<b>Function Declaration:</b><br>")
        current_width = html_box(flowchart, declarations[0], 0, current_width, HTML_NESTING_COLORS.get(0))
        flowchart.append("<br><b>Variable Declarations:</b><br>")
        for declaration in declarations[1:]:
            current_width = html_box(flowchart, declaration, 1, current_width, HTML_NESTING_COLORS.get(1))
        flowchart.append("<br>")

    # Functions
    if functions:
        flowchart.append("<b>Function Declarations:</b><br>")
        for func in functions:
            current_width = html_box(flowchart, func, 0, current_width, HTML_NESTING_COLORS.get(0))
        flowchart.append("<br>")

    # Function logic
    flowchart.append("<b>Function Logic Starts:</b><br>")
    nesting_depth = 1
    i = 0
    while i < len(code_lines):
        line = code_lines[i].strip()

        if re.match(r"^switch\b", line):
            current_width = html_box(flowchart, line, nesting_depth, current_width, HTML_NESTING_COLORS.get(nesting_depth))
            brace_stack.append("{")
            nesting_depth += 1
            i += 1
            continue

        elif re.match(r"^case\b", line) or re.match(r"^default\b", line):
            current_width = html_box(flowchart, line, nesting_depth + 1, current_width, HTML_NESTING_COLORS.get(nesting_depth + 1))
            i += 1
            continue

        elif re.match(r"^(if|for|while|else if|else)\b", line):
            current_width = html_box(flowchart, line, nesting_depth, current_width, HTML_NESTING_COLORS.get(nesting_depth))
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
            current_width = html_box(flowchart, code_lines[i].strip(), nesting_depth + 1, current_width, HTML_NESTING_COLORS.get(nesting_depth + 1))
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

        # Regular statement
        current_width = html_box(flowchart, line, nesting_depth, current_width, HTML_NESTING_COLORS.get(nesting_depth))
        i += 1

    return "<pre style='font-family: monospace'>" + "".join(flowchart) + "</pre>"

# -------------------- PYTHON CODE PARSER --------------------
def get_indent_level(line: str) -> int:
    return len(line) - len(line.lstrip(' '))

def generate_flowchart_from_python(code: str) -> str:
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
        indent = get_indent_level(raw_line)

        if inside_multiline_comment:
            current_width = html_box(flowchart, stripped, depth, current_width, HTML_NESTING_COLORS['comment'])
            if '"""' in stripped or "'''" in stripped:
                inside_multiline_comment = False
            continue

        if stripped.startswith(("'''", '"""')):
            inside_multiline_comment = not inside_multiline_comment
            current_width = html_box(flowchart, stripped, depth, current_width, HTML_NESTING_COLORS['comment'])
            continue

        if stripped.startswith("#"):
            current_width = html_box(flowchart, stripped, depth, current_width, HTML_NESTING_COLORS['comment'])
            continue

        while indent < indent_stack[-1]:
            indent_stack.pop()
            depth -= 1

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            depth += 1

        color = HTML_NESTING_COLORS.get(depth, HTML_NESTING_COLORS['default'])
        current_width = html_box(flowchart, stripped, depth, current_width, color)

    return "<pre style='font-family: monospace'>" + "".join(flowchart) + "</pre>"

