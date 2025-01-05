"""Binary code generation for the Hack assembly language.

This module provides the Code class which handles conversion of assembly language
components (dest, comp, jump) into their binary representations according to
the Hack machine language specification.
"""

from assembler.constants import COMP_DICT, JUMP_DICT


class Code:
    """code generation class."""

    def __init__(self) -> None:
        """Constructor."""
        self.dict = {}

    def address(self, value: int) -> str:
        """Address generation."""

        def binary_helper(value: int) -> str:
            """Recursion helper."""
            if value == 0:
                return "0"
            if value == 1:
                return "1"
            return binary_helper(value // 2) + str(value % 2)

        return binary_helper(value).zfill(16)

    def dest(self, value: str) -> str:
        """Convert destination value to 3-bit binary representation.

        Args:
            value (str): Destination string containing 'M', 'D', and/or 'A' characters.
                None is treated as no destination.

        Returns:
            str: A 3-bit binary string where:
                - Bit 0 (rightmost): M register
                - Bit 1: D register
                - Bit 2 (leftmost): A register
        """
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

    def comp(self, value: str) -> str:
        """Comp generation."""
        return COMP_DICT.get(value)

    def jump(self, value: str) -> str:
        """Jump generation."""
        return JUMP_DICT.get(value, "000")
