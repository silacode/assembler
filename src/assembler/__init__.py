"""Hack Assembly Language Assembler.

This package provides functionality to convert Hack assembly language
into machine code.
"""

from .code import Code
from .file_handler import read_file, write_output_file
from .parser import Parser
from .symbol_table import first_pass, initialize_symbol_table, second_pass

__version__ = "1.0.0"
__author__ = "Siladitya Samaddar"

# Export public interfaces
__all__ = [
    "Code",
    "Parser",
    "first_pass",
    "initialize_symbol_table",
    "read_file",
    "second_pass",
    "write_output_file",
]
