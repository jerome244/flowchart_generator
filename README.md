Welcome to my own made flowchart converter program

This program convert a given c code into a flowchart.

For executing this program, you need a c code file.

For launching it you can type in your bash command-line:

            python3 flowchart.py YourCfile.c

This will display you a flowchart in this style:

+-----------------------------+
| #include "main.h"         |  Line 1
+-----------------------------+
                    |
                    v 0

+---------------------------------------------------------------------------------------------+
| /*
* array_cleaner - function to free array
* @array: array needed to be freed
*/         |  Line 5
+---------------------------------------------------------------------------------------------+
                    |
                    v 0

+--------------------------------------------+
| void array_cleaner(char **array)         |  Line 6
+--------------------------------------------+
                    |
                    v 0
          +----------------------+
          | int i = 0;         |  Line 8
          +----------------------+
                              |
                              v 1
          +----------------------------+
          | while (array[i])         |  Line 10
          +----------------------------+
                              |
                              v 1
                       |
                       v

                              +---------------------------+
                              | free(array[i]);         |  Line 12
                              +---------------------------+
                                                  |
                                                  v 3
                    +----------------+
                    | i++;         |  Line 13
                    +----------------+
                                        |
                                        v 2
          +------------------------+
          | free(array);         |  Line 15
          +------------------------+
                              |
                              v 1



