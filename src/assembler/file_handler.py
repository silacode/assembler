"""File I/O operations for the Hack assembler.

This module handles reading assembly language source files and writing
the resulting machine code to output files. It includes error handling
for common file operations and input validation.

Functions:
    read_file: Reads and preprocesses assembly source files
    write_output_file: Writes assembled machine code to .hack files
"""

import sys
from pathlib import Path
from typing import TextIO


def read_file() -> list[str]:
    """Reads content from a file specified as the first command-line argument.

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
            raise IndexError("No input file specified. Usage: python main.py <filename>")

        filename = Path(sys.argv[1])
        if not filename.exists():
            raise FileNotFoundError(f"File not found: {filename}")

        # Use context manager to handle file operations
        with filename.open("r", encoding="utf-8") as file:
            # Read all lines at once and strip whitespace
            return [line.strip() for line in file]
    except IndexError as e:
        raise IndexError(str(e))
    except (FileNotFoundError, PermissionError) as e:
        raise type(e)(f"Error reading file {filename}: {str(e)}")  # noqa: B904
    except Exception as e:
        raise Exception(f"Unexpected error reading file {filename}:{str(e)}")


def write_output_file(filename: str, content: list[str]) -> TextIO:
    """Writes content to a .hack file, creating it if it doesn't exist.

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
    file = Path.open(f"{base_filename}.hack", "w")
    for line in content:
        file.write(f"{line}\n")
    file.close()
    return file
