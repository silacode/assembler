"""Symbol table management for the Hack assembler.

This module handles the creation and management of the symbol table,
which maps symbolic names to numeric addresses in the Hack assembly language.
It includes predefined symbols, label definitions, and variable allocations.
"""

from assembler.constants import A_INSTRUCTION_PATTERN, COMMENT_PATTERN, LABEL_PATTERN, NUMERIC_PATTERN


def initialize_symbol_table() -> dict[str, str]:
    """Initializes the symbol table with predefined symbols for the Hack assembly language.

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


def first_pass(text: list[str], symbol_dict: dict[str, str]) -> dict[str, str]:
    """Performs the first pass of the assembly process.

    Identifying and storing label symbolswith their corresponding line numbers in the symbol table.

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
    text: list[str], symbol_dict: dict[str, str], start_address: int = 16
) -> tuple[list[str], dict[str, str]]:
    """Performs the second pass of the assembly process.

    Resolving variables and symbols to their memory addresses. Also get rid of comments and white spaces.

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
    processed_lines: list[str] = []
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
