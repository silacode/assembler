# Hack Assembler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

A Python implementation of an assembler for the Hack computer platform, converting Hack assembly language into machine code. This assembler is part of the [Nand to Tetris](https://www.nand2tetris.org/) course.

## 🚀 Features

- ✨ Full support for Hack assembly language syntax
- 🏷️ Symbol handling (variables and labels)
- 🔄 Two-pass assembly process
- 🎯 Clean, modular code structure
- 📝 Detailed error messages
- 🧪 Comprehensive testing suite

## 📋 Requirements

- Python 3.9 or higher
- No external dependencies required

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hack-assembler.git
cd hack-assembler
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 💻 Usage

### Command Line

Run the assembler from the command line:

```bash
python -m assembler.main your_program.asm
```

This will create `your_program.hack` containing the machine code.

### As a Module

```python
from assembler import Parser, Code
from assembler.file_handler import read_file, write_output_file
from assembler.symbol_table import initialize_symbol_table, first_pass, second_pass

# Read assembly file
assembly_code = read_file()

# Process symbols
symbol_table = initialize_symbol_table()
symbol_table = first_pass(assembly_code, symbol_table)
processed_code, symbol_table = second_pass(assembly_code, symbol_table)

# Generate machine code
parser = Parser(processed_code)
code_generator = Code()
machine_code = []

while parser.has_more_lines:
    parser.advance()
    # Process instructions...
```

## 📁 Project Structure

```
assembler/
│
├── __init__.py          # Package initialization
├── main.py             # Main entry point
├── constants.py        # Constants and patterns
├── code.py            # Binary code generation
├── parser.py          # Instruction parsing
├── symbol_table.py    # Symbol management
└── file_handler.py    # File I/O operations
```

## 🔍 Example

### Input (program.asm):
```assembly
// Adds 1 + 2
@1
D=A
@2
D=D+A
@3
M=D
```

### Output (program.hack):
```binary
0000000000000001
1110110000010000
0000000000000010
1110000010010000
0000000000000011
1110001100001000
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📝 Assembly Language Specification

The Hack assembly language supports three types of instructions:

1. A-instructions: `@value`
   - Load a value or symbol into the A register
   - Example: `@100`, `@LOOP`

2. C-instructions: `dest=comp;jump`
   - Compute a value and store it
   - Example: `D=M+1`, `0;JMP`

3. Labels: `(LABEL)`
   - Define a symbol for jumps
   - Example: `(LOOP)`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on the [Nand to Tetris](https://www.nand2tetris.org/) course
- Thanks to Noam Nisan and Shimon Schocken for the course materials
- All contributors and testers

## 📞 Contact

Siladitya Samaddar - [@silacode](https://github.com/silacode)

Project Link: [https://github.com/silacode/assembler](https://github.com/silacode/assembler)