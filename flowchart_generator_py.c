#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 256
#define INDENT_STACK_SIZE 100

void print_box(FILE *out, const char *content, int depth, int force_gray) {
    int only_whitespace = 1;
    for (const char *p = content; *p; ++p) {
        if (!isspace(*p)) {
            only_whitespace = 0;
            break;
        }
    }
    if (only_whitespace) return;

    // Trim content
    char clean[MAX_LINE_LENGTH];
    strcpy(clean, content);
    char *start = clean;
    while (isspace(*start)) start++;
    char *end = start + strlen(start) - 1;
    while (end > start && isspace(*end)) *end-- = '\0';

    int len = strlen(start);
    if (len == 0) len = 1;

    const char *colors[] = {
        "\033[94m", "\033[92m", "\033[93m", "\033[91m",
        "\033[95m", "\033[96m", "\033[33m", "\033[36m",
        "\033[37m", "\033[41m", "\033[42m", "\033[43m"
    };
    const char *color = force_gray ? "\033[90m" : colors[depth % (sizeof(colors)/sizeof(colors[0]))];

    char indent[128] = "";
    for (int i = 0; i < depth; ++i) strcat(indent, "\t");

    fprintf(out, "%s%s\u250C", indent, color);
    for (int i = 0; i < len + 2; ++i) fprintf(out, "\u2500");
    fprintf(out, "\u2510\033[0m\n");

    fprintf(out, "%s%s\u2502 %-*s \u2502\033[0m\n", indent, color, len, start);

    fprintf(out, "%s%s\u2514", indent, color);
    for (int i = 0; i < len + 2; ++i) fprintf(out, "\u2500");
    fprintf(out, "\u2518\033[0m\n");
}

int is_function_declaration(const char *line) {
    return strstr(line, "def ") && strchr(line, '(');
}

int is_comment(const char *line) {
    return line[0] == '#' || strstr(line, "'''") || strstr(line, "\"\"\"");
}

int is_control_statement(const char *line) {
    return strstr(line, "if ") || strstr(line, "for ") ||
           strstr(line, "while ") || strstr(line, "else") ||
           strstr(line, "elif ") || strstr(line, "try") ||
           strstr(line, "except") || strstr(line, "finally");
}

int is_shebang(const char *line) {
    return line[0] == '#' && line[1] == '!';
}

int get_indent_level(const char *line) {
    int count = 0;
    while (*line == ' ') {
        count++;
        line++;
    }
    return count;
}

void process_code(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open file");
        return;
    }

    char line[MAX_LINE_LENGTH];
    int depth = 0;
    int indent_stack[INDENT_STACK_SIZE];
    int stack_top = 0;
    indent_stack[0] = 0;
    int first_line = 1;

    while (fgets(line, sizeof(line), file)) {
        char *start = line;
        while (*start == '\t') start++;  // skip tabs
        while (*start == ' ') start++;   // skip spaces
        char *end = start + strlen(start) - 1;
        while (end > start && (*end == '\n' || *end == '\r')) *end-- = '\0';

        if (first_line && is_shebang(start)) {
            first_line = 0;
            continue;
        }
        first_line = 0;

        if (strlen(start) == 0) continue;

        int current_indent = get_indent_level(line);

        // Adjust nesting based on indentation
        if (current_indent > indent_stack[stack_top]) {
            stack_top++;
            indent_stack[stack_top] = current_indent;
            depth++;
        } else {
            while (stack_top > 0 && current_indent < indent_stack[stack_top]) {
                stack_top--;
                depth--;
                if (depth < 0) depth = 0;
            }
        }

        if (is_comment(start)) {
            print_box(stdout, start, depth, 1);
        } else if (is_function_declaration(start)) {
            print_box(stdout, start, depth, 0);
        } else if (is_control_statement(start)) {
            print_box(stdout, start, depth, 0);
        } else {
            print_box(stdout, start, depth, 0);
        }
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <python_source_file>\n", argv[0]);
        return 1;
    }

    process_code(argv[1]);
    return 0;
}

