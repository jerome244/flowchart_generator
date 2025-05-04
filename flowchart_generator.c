#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 256
#define MAX_LINES 1000

void print_box(FILE *out, const char *content, int depth, int force_gray) {
    // Skip empty or whitespace-only content
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
    return strstr(line, "(") && strstr(line, ")") && strchr(line, '{');
}

int is_preprocessor(const char *line) {
    return line[0] == '#';
}

int is_comment(const char *line) {
    return strstr(line, "/*") || strstr(line, "*") || strstr(line, "//") || strstr(line, "*/");
}

int is_variable_declaration(const char *line) {
    const char *types[] = {
        "int ", "float ", "char ", "double ", "long ", "short ", "unsigned ",
        "size_t", "void*", "FILE*", "struct "
    };
    for (int i = 0; i < sizeof(types) / sizeof(types[0]); i++) {
        if (strstr(line, types[i]) && strchr(line, ';')) {
            return 1;
        }
    }
    return 0;
}

int is_control_statement(const char *line) {
    return (strstr(line, "if") || strstr(line, "for") ||
            strstr(line, "while") || strstr(line, "else")) &&
           !strchr(line, '{');
}

int is_switch_statement(const char *line) {
    return strstr(line, "switch") != NULL;
}

int is_case_or_default(const char *line) {
    return strstr(line, "case ") || strstr(line, "default");
}

void process_code(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open file");
        return;
    }

    char line[MAX_LINE_LENGTH];
    int depth = 0;
    int in_headed_comments = 0;
    int headed_comments_done = 0;
    int control_pending = 0;
    int is_start_of_function = 0;
    int in_switch = 0;
    char headed_comment_block[MAX_LINE_LENGTH * 10] = "";

    while (fgets(line, sizeof(line), file)) {
        char *start = line;
        while (*start == ' ' || *start == '\t') start++;
        char *end = start + strlen(start) - 1;
        while (end > start && (*end == '\n' || *end == '\r')) *end-- = '\0';

        // Preprocessor
        if (!headed_comments_done && is_preprocessor(start)) {
            print_box(stdout, start, 0, 0);
            continue;
        }

        // Headed comment block
        if (!headed_comments_done && is_comment(start)) {
            strcat(headed_comment_block, start);
            strcat(headed_comment_block, "\n");
            in_headed_comments = 1;
            continue;
        } else if (in_headed_comments && !is_comment(start)) {
            print_box(stdout, headed_comment_block, 0, 0);
            headed_comments_done = 1;
            in_headed_comments = 0;
        }

        // Function header
        if (!headed_comments_done && is_function_declaration(start)) {
            if (strlen(headed_comment_block) > 0) {
                print_box(stdout, headed_comment_block, 0, 0);
            }
            headed_comments_done = 1;
            is_start_of_function = 1;
        }

        // Variable declarations at root
        if (is_start_of_function && is_variable_declaration(start)) {
            print_box(stdout, start, 0, 0);
            continue;
        }

        // Switch header
        if (is_switch_statement(start)) {
            print_box(stdout, start, depth, 0);
            in_switch = 1;
            if (strchr(start, '{')) depth++;
            continue;
        }

        // Case/default in switch
        if (in_switch && is_case_or_default(start)) {
            print_box(stdout, start, depth, 0);
            continue;
        }

        // Control block headers (without braces), using original color
        if (strstr(start, "if") && !strchr(start, ';')) {
            print_box(stdout, start, depth, 0); // Keep original color
            control_pending = 1;
            continue;
        } else if ((strstr(start, "for") || strstr(start, "while")) && !strchr(start, ';')) {
            print_box(stdout, start, depth, 0); // Keep original color
            control_pending = 1;
            continue;
        } else if (strstr(start, "else") && !strchr(start, ';')) {
            print_box(stdout, start, depth, 0); // Keep original color
            control_pending = 1;
            continue;
        }

        // Opening brace after control
        if (control_pending && strchr(start, '{')) {
            depth++;
            control_pending = 0;
            continue;
        }

        // Single-line execution after control
        if (control_pending) {
            print_box(stdout, start, depth + 1, 0);
            control_pending = 0;
            continue;
        }

        // Opening brace (skip braces in output)
        if (strchr(start, '{') && !strchr(start, '}')) {
            depth++;
            continue;
        }

        // Closing brace (skip braces in output)
        if (strchr(start, '}') && !strchr(start, '{')) {
            depth = depth > 0 ? depth - 1 : 0;
            continue;
        }

        // Other lines
        print_box(stdout, start, depth, 0);
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <c_source_file>\n", argv[0]);
        return 1;
    }

    process_code(argv[1]);
    return 0;
}

