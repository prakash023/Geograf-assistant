"""
parser.py
----------

Reads a Geograf PKT file without changing its formatting.

The parser NEVER modifies a line.
It only extracts information that will later be used by the rule engine.

Author: Geograf Assistant
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


# ==========================================================
# PKT Record
# ==========================================================

@dataclass
class PKTRecord:
    """Represents one record of a PKT file."""

    line_number: int

    raw_line: str

    point_number: str
    point_type: str

    x: str
    y: str

    label: str

    quote_start: int
    quote_end: int


# ==========================================================
# Parser
# ==========================================================

class PKTParser:

    def __init__(self, filename: str):

        self.filename = Path(filename)

        if not self.filename.exists():
            raise FileNotFoundError(f"File not found:\n{self.filename}")

    # ------------------------------------------------------

    def read(self) -> List[PKTRecord]:
        """
        Reads the complete PKT file.
        """

        records: List[PKTRecord] = []

        with open(self.filename, "r", encoding="latin-1") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.rstrip("\n")

                record = self.parse_line(line_number, line)

                if record is not None:
                    records.append(record)
                else:
                    print(f"Warning: Could not parse line {line_number}") 

        return records

    # ------------------------------------------------------

    def parse_line(
        self,
        line_number: int,
        line: str
    ) -> Optional[PKTRecord]:
        """
        Parses one PKT line.

        Returns None if the line cannot be parsed.
        """

        first_quote = line.find('"')
        last_quote = line.rfind('"')

        if first_quote == -1:
            return None

        if last_quote == -1:
            return None

        if first_quote == last_quote:
            return None

        label = line[first_quote + 1:last_quote]

        left = line[:first_quote].split()

        if len(left) < 4:
            return None

        return PKTRecord(

            line_number=line_number,

            raw_line=line,

            point_number=left[0],
            #point_type=left[1],
            point_type=int(left[1]),

            x=left[2],
            y=left[3],

            label=label,

            quote_start=first_quote,
            quote_end=last_quote
        )

    # ------------------------------------------------------

    @staticmethod
    def replace_label(
        record: PKTRecord,
        new_label: str
    ) -> str:
        """
        Replaces ONLY the text inside the quotation marks.

        Everything else remains untouched.
        """

        return (
            record.raw_line[:record.quote_start + 1]
            + new_label
            + record.raw_line[record.quote_end:]
        )