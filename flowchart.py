import sys

# Limit the maximum width before wrapping to a new "column"
MAX_LINE_WIDTH = 100  # Adjust this to your preferred limit

# Define colors for different nesting depths (only for the arrows)
NESTING_COLORS = {
    0: '\033[94m',  # Blue
    1: '\033[92m',  # Green
    2: '\033[93m',  # Yellow
    3: '\033[91m',  # Red
    4: '\033[95m',  # Magenta
    5: '\033[96m',  # Cyan
}

# Function to get the color for the arrows based on nesting depth
def get_arrow_color_for_depth(depth):
    return NESTING_COLORS.get(depth, '\033[0m')  # Default to no color if depth exceeds predefined levels

def process_code_line(flowchart, stmt, nesting_depth, line_number, current_width):
    """
    This function processes a single code line (statement or condition) and applies horizontal shifts (nesting depth).
    It also adds line numbers to the flowchart with wrapping behavior.
    """
    shift = " " * (nesting_depth * 10)  # Horizontal shift for nesting depth
    stmt_length = len(stmt) + 12  # Adding extra space for separators

    # If the current width exceeds the limit, start a new column (wrap)
    if current_width + stmt_length > MAX_LINE_WIDTH:
        flowchart.append("")  # Add an empty line to simulate the wrap
        current_width = 0  # Reset width for the new line

    # Add the flowchart components (rectangles for the statements)
    flowchart.append(f"{shift}+{'-' * stmt_length}+")
    flowchart.append(f"{shift}| {stmt.ljust(len(stmt) + 8)} |  Line {line_number}")
    flowchart.append(f"{shift}+{'-' * stmt_length}+")
    flowchart.append(f"{shift}                    |")

    # Color the arrow based on nesting depth and add nesting depth number
    arrow_color = get_arrow_color_for_depth(nesting_depth)
    arrow_with_depth = f"{shift}{arrow_color}                    v {nesting_depth}\033[0m"  # Colored arrow with depth number
    flowchart.append(arrow_with_depth)

    current_width += stmt_length  # Update the width after adding the statement

    return current_width

def generate_flowchart_from_c_code(code: str) -> str:
    """
    This function generates the flowchart for C code by processing its structure,
    respecting nesting depth (horizontal indentation).
    """
    # Grouping all variable declarations at the beginning
    lines = code.strip().split('\n')
    flowchart = []
    nesting_depth = 0  # Start at the root nesting level
    inside_comment = False
    comment_block = []
    skip_next_line = False  # Flag to skip the next line if it's a single-line block
    brace_stack = []  # Stack to track braces
    line_number = 1  # Initialize line number counter
    current_width = 0  # Track the current line width

    for line in lines:
        line = line.strip()

        # Skip empty lines or lines that contain only whitespace
        if not line:
            line_number += 1
            continue

        # Handle the start of a comment block
        if line.startswith("/*"):
            inside_comment = True
            comment_block.append(line)
            line_number += 1
            continue

        # Handle the end of a comment block
        if inside_comment:
            comment_block.append(line)
            if line.endswith("*/"):
                # Once the comment block ends, group the entire comment block as a single flowchart entry
                current_width = process_code_line(flowchart, "\n".join(comment_block), nesting_depth, line_number, current_width)
                inside_comment = False
                comment_block = []  # Clear comment block
            line_number += 1
            continue

        # Handle the beginning of control structures (if, while, for, etc.)
        if line.startswith("while") or line.startswith("for") or line.startswith("if") or line.startswith("else if") or line.startswith("else"):
            # Process the condition (start of block)
            current_width = process_code_line(flowchart, line, nesting_depth, line_number, current_width)

            # Only increment nesting depth if it's not a single-line control structure
            if not line.endswith(";"):  # Handle multi-line control structures (e.g., if, while)
                nesting_depth += 1  # Increment depth for entering the block
                flowchart.append(f"{' ' * (nesting_depth * 10)}   |")
                flowchart.append(f"{' ' * (nesting_depth * 10)}   v")  # Arrow to indicate flow to the next block

            skip_next_line = True  # We need to process the next line separately after this control structure
            line_number += 1
            continue  # Skip the brace processing for multi-line control structures

        # Handle the opening brace
        elif line == "{":
            brace_stack.append("{")  # Push to stack
            nesting_depth += 1  # Increase nesting depth
            line_number += 1
            continue

        # Handle closing braces
        elif line == "}":
            if brace_stack:
                brace_stack.pop()  # Pop from stack when a closing brace is found
            else:
                print("Error: Unmatched closing brace found.")
                continue
            nesting_depth = max(0, nesting_depth - 1)  # Decrease nesting depth but not below 0
            line_number += 1
            continue

        # Process regular statements
        if skip_next_line:
            # This is the next line after a single-line control structure
            current_width = process_code_line(flowchart, line, nesting_depth, line_number, current_width)
            skip_next_line = False  # Reset the flag
            # Decrease nesting depth after the line executes
            nesting_depth -= 1
        else:
            current_width = process_code_line(flowchart, line, nesting_depth, line_number, current_width)

        line_number += 1

    return "\n".join(flowchart)

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

if __name__ == "__main__":
    main()

