"""Main entry point for the Hack assembler.

This module orchestrates the assembly process, coordinating between the parser,
code generator, and symbol table to convert Hack assembly language into
machine code.

The assembly process consists of:
1. Reading the source file
2. Building the symbol table (two passes)
3. Generating machine code
4. Writing the output file

Usage:
    python -m assembler.main program.asm

The assembler will create program.hack containing the machine code.
"""

import sys

from assembler import Code, Parser, first_pass, initialize_symbol_table, read_file, second_pass, write_output_file


def main() -> None:
    """Main entry fn."""
    file = read_file()
    symbole_dict = initialize_symbol_table()
    symbole_dict = first_pass(file, symbole_dict)
    file, symbole_dict = second_pass(file, symbole_dict, 16)
    parser = Parser(file)
    code = Code()
    output_text = []

    while parser.has_more_lines:
        parser.advance()
        instruction_type = parser.instruction_type()
        # 'A_INSTRUCTION', 'L_INSTRUCTION', 'C_INSTRUCTION'

        if instruction_type == "A_INSTRUCTION":
            symbol = parser.symbol(instruction_type)

            a_bits = code.address(int(symbol))
            output_text.append(a_bits)
        elif instruction_type == "L_INSTRUCTION":
            symbol = parser.symbol(instruction_type)

        else:
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            dest_bits = code.dest(dest)
            comp_bits = code.comp(comp)
            jump_bits = code.jump(jump)
            output_text.append("111" + comp_bits + dest_bits + jump_bits)

    filename = sys.argv[1]
    write_output_file(filename, output_text)


if __name__ == "__main__":
    main()
