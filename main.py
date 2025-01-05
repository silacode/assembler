from email.parser import Parser
import sys
from typing import Dict, List, Tuple


from pathlib import Path
import sys
from typing import List, TextIO
import re


COMP_DICT = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

JUMP_DICT = {
    None: "000",
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

LABEL_PATTERN = re.compile(r"^\((.*)\)$")
COMMENT_PATTERN = re.compile(r"^(//.*)")
A_INSTRUCTION_PATTERN = re.compile(r"^@([\w.$_]+|\d+)$")
NUMERIC_PATTERN = re.compile(r"^\d+$")


class Code:
    def __init__(self):
        self.dict = {}

    def address(self, value):
        def binary_helper(value):
            if value == 0:
                return "0"
            elif value == 1:
                return "1"
            else:
                return binary_helper(value // 2) + str(value % 2)

        return binary_helper(value).zfill(16)

    def dest(self, value):
        # return 3 bits
        if value is None:
            return "000"
        bits = 0
        if "M" in value:
            bits |= 1
        if "D" in value:
            bits |= 2
        if "A" in value:
            bits |= 4
        return f"{bits:03b}"

    def comp(self, value):
        # return 7 bits
        return COMP_DICT.get(value)

    def jump(self, value):
        # return 3 bits
        return JUMP_DICT.get(value, "000")


def read_file() -> List[str]:
    """
    Reads content from a file specified as the first command-line argument.

    Returns:
        List[str]: List of strings, each representing a line from the file

    Raises:
        IndexError: If no command-line argument is provided
        FileNotFoundError: If the specified file doesn't exist
        PermissionError: If the program lacks permission to read the file

    Example:
        # Running script: python input.py test.asm
        >>> lines = read_file()
        >>> print(lines)  # ['line1', 'line2', ...]

    Note:
        - Strips trailing whitespace and newlines from each line
        - Expects the filename as the first command-line argument
    """
    try:
        if len(sys.argv) < 2:
            raise IndexError(
                "No input file specified. Usage: python main.py <filename>"
            )

        filename = Path(sys.argv[1])
        if not filename.exists():
            raise FileNotFoundError(f"File not found: {filename}")

        # Use context manager to handle file operations
        with open(filename, "r", encoding="utf-8") as file:
            # Read all lines at once and strip whitespace
            return [line.strip() for line in file]
    except IndexError as e:
        raise IndexError(str(e))
    except (FileNotFoundError, PermissionError) as e:
        raise type(e)(f"Error reading file {filename}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error reading file {filename}:{str(e)}")


def write_output_file(filename: str, content: List[str]) -> TextIO:
    """
    Writes content to a .hack file, creating it if it doesn't exist.

    Args:
        filename (str): The input filename (with or without extension)
        content (List[str]): List of strings to write to the file, each representing a line

    Returns:
        TextIO: The file object of the written file

    Raises:
        OSError: If there are permission issues or disk is full

    Example:
        >>> content = ["line1", "line2", "line3"]
        >>> file = write_output_file("test.asm", content)
    """

    base_filename = filename.split(".")[0]
    file = open(base_filename + ".hack", "w")
    for line in content:
        file.write("%s\n" % line)
    file.close()
    return file


class Parser:
    def __init__(self, file: list):
        self.__file = file
        self.__line_index = 0
        self.has_more_lines = bool(len(file))
        self.current_instruction: str = None
        self.__total_lines = len(file)

    def advance(self):
        # skips over white space and comments
        # reads next instruction and make it current_instruction
        # should be called if has_more_lines is true
        # initially current_instruction is none

        if not self.has_more_lines:
            return
        current_line = self.__file[self.__line_index]
        self.current_instruction = current_line
        self.__line_index += 1
        if self.__line_index >= self.__total_lines:
            self.has_more_lines = False
        return

    def instruction_type(self):
        # Return the type of current_instruction
        # A - @xxx
        # C - dest=comp;jump
        # L - (xxx)
        first_char = self.current_instruction[0]

        if first_char == "@":
            return "A_INSTRUCTION"
        elif first_char == "(":
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"

    def symbol(self, type):
        # get the symbol from A or L instruction
        # should be called if instruction type is A or L
        if type == "A_INSTRUCTION":
            return self.current_instruction[1:]
        else:
            return self.current_instruction[1:-1]

    def dest(self):
        # Returns dest part of the current c instruction
        # should be called if instruction type is C

        if "=" in self.current_instruction:
            return self.current_instruction.split("=")[0]

    def comp(self):
        # Returns the symbolic comp part of the current C instruction
        # should be called if instruction type is C
        result = self.current_instruction
        if "=" in result:
            result = result.split("=")[1]
        if ";" in result:
            result = result.split(";")[0]
        return result

    def jump(self):
        # Returns the symbolic jump part of the current C instruction
        # should be called if instruction type is C
        if ";" in self.current_instruction:
            return self.current_instruction.split(";")[1]


def initialize_symbol_table() -> Dict[str, str]:
    """
    Initializes the symbol table with predefined symbols for the Hack assembly language.

    Returns:
        Dict[str, str]: A dictionary mapping symbolic names to their memory addresses
                       as strings. Includes:
                       - R0-R15 registers (0-15)
                       - Predefined symbols (SP, LCL, ARG, THIS, THAT)
                       - Memory mapped I/O (SCREEN, KBD)

    Example:
        >>> symbol_table = initialize_symbol_table()
        >>> print(symbol_table['R0'])  # '0'
        >>> print(symbol_table['SCREEN'])  # '16384'

    Note:
        All values are stored as strings to maintain consistency with
        the Hack assembly language specification.
    """
    return {
        **{f"R{i}": str(i) for i in range(16)},
        "SP": "0",
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4",
        "SCREEN": "16384",
        "KBD": "24576",
    }


def first_pass(text: List[str], symbol_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Performs the first pass of the assembly process, identifying and storing label symbols
    with their corresponding line numbers in the symbol table.

    Args:
        text (List[str]): List of pre-stripped assembly code lines
        symbol_dict (Dict[str, str]): Existing symbol dictionary to update

    Returns:
        Dict[str, str]: Updated symbol dictionary with label definitions
    """
    line_number = 0
    try:
        for line in text:
            if not line:
                continue
            if COMMENT_PATTERN.match(line):
                continue
            if label_match := LABEL_PATTERN.match(line):
                label_name = label_match.group(1)
                if label_name in symbol_dict:
                    raise ValueError(f"Duplicate label definition: {label_name}")
                symbol_dict[label_name] = str(line_number)
                continue

            line_number += 1

        return symbol_dict

    except Exception as e:
        raise Exception(f"Error during first pass at line {line_number}: {str(e)}")


def second_pass(
    text: List[str], symbol_dict: Dict[str, str], start_address: int = 16
) -> Tuple[List[str], Dict[str, str]]:
    """
    Performs the second pass of the assembly process, resolving variables and symbols
    to their memory addresses. Also get rid of comments and white spaces.

    Args:
        text (List[str]): Pre-stripped assembly code lines
        symbol_dict (Dict[str, str]): Symbol table with predefined symbols and labels
        start_address (int, optional): Starting address for variables. Defaults to 16

    Returns:
        Tuple[List[str], Dict[str, str]]:
            - List of processed assembly lines with resolved symbols
            - Updated symbol dictionary including new variables

    Example:
        >>> text = ["@counter", "@5", "@LOOP"]
        >>> symbols = {"LOOP": "10"}
        >>> lines, symbols = second_pass(text, symbols)
        >>> print(lines)  # ['@16', '@5', '@10']
        >>> print(symbols["counter"])  # '16'

    Note:
        - Variables are allocated from address 16 onwards
        - Numeric addresses (@123) are preserved as-is
        - Pre-defined symbols and labels are resolved using symbol_dict
    """

    processed_lines: List[str] = []
    variable_address = start_address

    for line in text:
        # Get rid of comments and white spaces
        if not line or line.startswith("//"):
            continue
        if a_match := A_INSTRUCTION_PATTERN.match(line):
            symbol = a_match.group(1)

            if NUMERIC_PATTERN.match(symbol):
                processed_lines.append(line)
                continue

            # Use existing symbol or allocate new address
            address = symbol_dict.get(symbol)

            if address:
                processed_lines.append(f"@{address}")
            else:
                symbol_dict[symbol] = str(variable_address)
                processed_lines.append(f"@{variable_address}")
                variable_address += 1
        else:
            processed_lines.append(line)
    return processed_lines, symbol_dict


def main():
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
