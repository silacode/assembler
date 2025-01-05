Hack Assembly Compiler
A Python-based compiler that translates Hack assembly language into machine code.

Features - 
Converts Hack assembly (.asm) files to binary (.hack) files
Two-pass compilation for handling symbols and variables
Supports all standard Hack assembly instructions
Comprehensive error handling
Built-in symbol table with predefined symbols

Installation -
Clone the repository
Ensure Python 3.6+ is installed
No additional dependencies required

Usage-
bash
python main.py <input_file.asm>
The compiler will generate a .hack file with the same base name as the input file.

Project Structure-
text
project/
├── src/
│   ├── __init__.py
│   ├── constants.py      # Instruction dictionaries and patterns
│   ├── parser.py         # Parser class for instruction processing
│   ├── code.py          # Code class for binary conversion
│   ├── file_handler.py   # File I/O operations
│   └── main.py          # Main program logic
├── tests/
└── README.md

Supported Instructions -
A-instructions: @value
C-instructions: dest=comp;jump
Labels: (LABEL)
Comments: // comment

Error Handling -
The compiler handles various error cases:
Missing input files
Invalid file permissions
Duplicate label definitions
Invalid instruction formats
File I/O errors

Contributing -
Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a Pull Request

License -
[MIT]
Author -
[Siladitya Samaddar]
