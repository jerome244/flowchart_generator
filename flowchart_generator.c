#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 256
#define MAX_LINES 1000

// Box-drawing function with ANSI colors per depth level or override
void print_box(FILE *out, const char *content, int depth, const char *override_color) {
    int len = strlen(content);

    const char *colors[] = {
        "\033[94m", // Blue
        "\033[92m", // Green
        "\033[93m", // Yellow
        "\033[91m", // Red
        "\033[95m", // Magenta (Pink)
        "\033[96m", // Cyan
        "\033[33m", // Orange
        "\033[36m", // Teal
        "\033[37m", // Gray
        "\033[41m", // Bg Red
        "\033[42m", // Bg Green
        "\033[43m"  // Bg Yellow
    };

    const char *color = override_color ? override_color : colors[depth % (sizeof(colors)/sizeof(colors[0]))];

    char indent[128] = "";
    for (int i = 0; i < depth; ++i) strcat(indent, "\t");

    // Top border
    fprintf(out, "%s%s\u250C", indent, color);
    for (int i = 0; i < len + 2; ++i) fprintf(out, "\u2500");
    fprintf(out, "\u2510\033[0m\n");

    // Content line — handle empty content correctly
    if (len == 0) {
        fprintf(out, "%s%s\u2502  \u2502\033[0m\n", indent, color);
    } else {
        fprintf(out, "%s%s\u2502 %s \u2502\033[0m\n", indent, color, content);
    }

    // Bottom border
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
    return strstr(line, "/*") || strstr(line, "*") || strstr(line, "*/");
}

int is_variable_declaration(const char *line) {
    const char *types[] = {"int ", "float ", "char ", "double ", "long ", "short ", "unsigned "};
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
    char headed_comment_block[MAX_LINE_LENGTH * 10] = "";

    while (fgets(line, sizeof(line), file)) {
        char *start = line;
        while (*start == ' ' || *start == '\t') start++;
        char *end = start + strlen(start) - 1;
        while (end > start && (*end == '\n' || *end == '\r')) *end-- = '\0';

        if (!headed_comments_done && is_preprocessor(start)) {
            print_box(stdout, start, 0, NULL);
            continue;
        }

        if (!headed_comments_done && is_comment(start)) {
            strcat(headed_comment_block, start);
            strcat(headed_comment_block, "\n");
            in_headed_comments = 1;
            continue;
        } else if (in_headed_comments && !is_comment(start)) {
            print_box(stdout, headed_comment_block, 0, "\033[95m"); // Pink color for comments
            headed_comments_done = 1;
            in_headed_comments = 0;
        }

        if (!headed_comments_done && is_function_declaration(start)) {
            if (strlen(headed_comment_block) > 0) {
                print_box(stdout, headed_comment_block, 0, "\033[95m"); // Pink color for comments
            }
            headed_comments_done = 1;
            is_start_of_function = 1;
        }

        // Print initial variable declarations at depth 0
        if (is_start_of_function && is_variable_declaration(start)) {
            print_box(stdout, start, 0, NULL);
            continue;
        }

        // Control statement without braces
        if (is_control_statement(start)) {
            control_pending = 1;
            print_box(stdout, start, depth, NULL);
            continue;
        }

        // Handle opening brace after control statement
        if (control_pending && strchr(start, '{')) {
            print_box(stdout, start, depth, NULL);
            depth++;
            control_pending = 0;
            continue;
        }

        // Execution line following control without braces
        if (control_pending) {
            print_box(stdout, start, depth + 1, NULL);
            control_pending = 0;
            continue;
        }

        // Opening brace
        if (strchr(start, '{') && !strchr(start, '}')) {
            print_box(stdout, start, depth, NULL);
            depth++;
            continue;
        }

        // Closing brace
        if (strchr(start, '}') && !strchr(start, '{')) {
            depth = depth > 0 ? depth - 1 : 0;
            print_box(stdout, start, depth, NULL);
            continue;
        }

        // Default case
        print_box(stdout, start, depth, NULL);
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

