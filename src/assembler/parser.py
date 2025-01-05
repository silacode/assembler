"""Parser for Hack assembly language instructions.

This module provides the Parser class which reads and parses assembly language
instructions, breaking them down into their constituent components according
to the instruction type (A-instruction, C-instruction, or L-instruction/label).
"""


class Parser:
    """Parser class."""

    def __init__(self, file: list) -> None:
        """Constructor."""
        self.__file = file
        self.__line_index = 0
        self.has_more_lines = bool(len(file))
        self.current_instruction: str = None
        self.__total_lines = len(file)

    def advance(self) -> None:
        """Advance method."""
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

    def instruction_type(self) -> str:
        """Instruction type check method."""
        # Return the type of current_instruction
        # A - @xxx
        # C - dest=comp;jump
        # L - (xxx)  # noqa: ERA001

        first_char = self.current_instruction[0]

        if first_char == "@":
            return "A_INSTRUCTION"
        if first_char == "(":
            return "L_INSTRUCTION"
        return "C_INSTRUCTION"

    def symbol(self, ins_type: str) -> str:
        """Symbol parser method."""
        # get the symbol from A or L instruction
        # should be called if instruction type is A or L
        if ins_type == "A_INSTRUCTION":
            return self.current_instruction[1:]
        return self.current_instruction[1:-1]

    def dest(self) -> str:
        """Dest parser method."""
        # Returns dest part of the current c instruction
        # should be called if instruction type is C

        if "=" in self.current_instruction:
            return self.current_instruction.split("=")[0]
        return None

    def comp(self) -> str:
        """Comp parser method."""
        # Returns the symbolic comp part of the current C instruction
        # should be called if instruction type is C
        result = self.current_instruction
        if "=" in result:
            result = result.split("=")[1]
        if ";" in result:
            result = result.split(";")[0]
        return result

    def jump(self) -> str:
        """Jump parser method."""
        # Returns the symbolic jump part of the current C instruction
        # should be called if instruction type is C
        if ";" in self.current_instruction:
            return self.current_instruction.split(";")[1]
        return None
