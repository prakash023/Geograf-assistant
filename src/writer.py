"""
writer.py
---------

Writes PKT files.

The writer only writes lines to disk.
It never changes the content.
"""

from pathlib import Path
from typing import Union


class PKTWriter:

    @staticmethod
    def write(filename: Union[str, Path], lines: list[str]) -> None:
        """
        Write a PKT file.

        Parameters
        ----------
        filename : str | Path
            Output filename.
        lines : list[str]
            Lines to write.
        """

        filename = Path(filename)

        # Create output directory if it doesn't exist
        filename.parent.mkdir(parents=True, exist_ok=True)

        with filename.open("w", encoding="latin-1") as file:
            for line in lines:
                file.write(line + "\n")

        print(f"Written: {filename}")