import sys


def read_file():
    filename = sys.argv[1]
    text = open(filename, "r")
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

# def initialization():
#     # initialize
#     print("t")


# def first_pass():
#     # firstpass
#     print("f")


def restart():
    # restart
    print("")


def main_loop():
    # loop
    print("Main Loop")


def write_output_file(filename):
    filename_witout_extension = filename.split(".")[0]
    # create a new file if doesn't exits
    file = open(filename_witout_extension + ".hack", "w")
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
    # convert text iterator to list to make it available after it is consumed
    text = list(text)
    for line in text:
        if line[0] == "(":
            symbol_dict[line[1:-2]] = str(line_number + 1)
        else:
            line_number += 1
    return text, symbol_dict


def second_pass(text, symbol_dict):
    new_text = []
    variable_address = 16

    # print(symbol_dict)
    for line in text:
        if line[0] == "@":
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

    # print(new_text)
    # print(symbol_dict)
    return new_text, symbol_dict


def main():
    value = read_file()
    print("Hello World")
    # for i in value:
    #     print(i)
    filename = sys.argv[1]
    write_output_file(filename)

    # decimal = int(sys.argv[2])
    # print(decimal_to_binary(decimal))

    # `des = sys.argv[2]
    # print(destination_to_bits(des))`

    # print(jump_to_bits("h"))

    # print(initialize_symbol_table())
    new_value, new_dict = first_pass(value, initialize_symbol_table())

    # for i in value:
    #     print(i)
    text, fdict = second_pass(new_value, new_dict)
    for i in text:
        print(i)

    print(fdict)


if __name__ == "__main__":
    main()
