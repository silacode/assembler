import sys


def read_file():
    filename = sys.argv[1]
    file = open(filename, "r")
    text = list(file)
    file.close()
    return text


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


def restart():
    # restart
    print("")


def main_loop():
    # loop
    print("Main Loop")


def write_output_file(filename, content):
    filename_witout_extension = filename.split(".")[0]
    # create a new file if doesn't exits
    file = open(filename_witout_extension + ".hack", "w")
    for line in content:
        file.write("%s\n" % line)
    # file.write(content)
    file.close()
    return file


def decimal_to_binary(value):
    """Converts from decimal to binary.

    Args:
      value: decimal value
    """

    def binary_helper(value):
        if value == 0:
            return "0"
        elif value == 1:
            return "1"
        else:
            return binary_helper(value // 2) + str(value % 2)

    return binary_helper(value).zfill(16)


def destination_to_bits(value):
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


def comp_to_bits(val):
    return COMP_DICT.get(val)


def jump_to_bits(val):
    jump_dict = {
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
    return jump_dict.get(val, "000")


def initialize_symbol_table():
    symbol_dict = {}
    for i in range(16):
        symbol_dict["R" + str(i)] = str(i)
    symbol_dict.update(
        {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "SCREEN": "16384",
            "KBD": "24576",
        }
    )

    return symbol_dict


def first_pass(text, symbol_dict):
    line_number = 0
    for line in text:
        line = line.strip()
        if len(line) and line[0] == "(":
            symbol_dict[line[1:-1]] = str(line_number)
        elif len(line) and not line[0] == "/":
            line_number += 1
        else:
            continue
    return symbol_dict


def second_pass(text, symbol_dict):
    new_text = []
    variable_address = 16

    for line in text:
        line = line.strip()
        if len(line) and line[0] == "@":
            symbol = line[1:].strip()
            if not symbol.isnumeric():
                symbol_value = symbol_dict.get(symbol)

                if symbol_value:
                    new_text.append("@" + str(symbol_value))
                else:
                    symbol_dict[symbol] = str(variable_address)
                    new_text.append("@" + str(variable_address))
                    variable_address += 1
            else:
                new_text.append(line)
        else:
            new_text.append(line)

    return new_text, symbol_dict


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
        current_line = self.__file[self.__line_index].strip()

        if not len(current_line) or current_line[0] == "/":
            self.__line_index += 1
            if self.__line_index >= self.__total_lines:
                self.has_more_lines = False
            return self.advance()
        else:
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


def main():
    # construct parser for parsing input file

    # creates an output file

    # use parser and code for c instruction

    # a ins

    file = read_file()
    symbole_dict = initialize_symbol_table()
    symbole_dict = first_pass(file, symbole_dict)
    file, symbole_dict = second_pass(file, symbole_dict)

    parser = Parser(file)
    code = Code()
    output_text = []

    # print(file)
    while parser.has_more_lines:
        parser.advance()
        instruction_type = parser.instruction_type()
        # 'A_INSTRUCTION', 'L_INSTRUCTION', 'C_INSTRUCTION'

        if instruction_type == "A_INSTRUCTION":
            symbol = parser.symbol(instruction_type)

            a_bits = code.address(int(symbol))
            # print(code.address(int(symbol)))
            output_text.append(a_bits)
        elif instruction_type == "L_INSTRUCTION":
            symbol = parser.symbol(instruction_type)
            #  TODO

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
