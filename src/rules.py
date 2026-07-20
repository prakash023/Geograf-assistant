"""
rules.py
--------

Business logic for splitting LNE labels into
LNA and Sach labels.
"""

import re
from dataclasses import dataclass


@dataclass
class RuleResult:
    write_lna: bool
    write_sach: bool

    lna_label: str
    sach_label: str


class RuleEngine:

    NUMBER_PATTERN = re.compile(r'^[+-]?\d+(\.\d+)?$')

    @staticmethod
    def is_numeric(token: str) -> bool:
        """
        True for:
            77
            0.24
            11.50
            -5
            +3
        """
        return bool(RuleEngine.NUMBER_PATTERN.fullmatch(token))

    @staticmethod
    def process(record) -> RuleResult:

        # Preserve original width inside the quotation marks
        original_width = len(record.label)

        # Remove leading/trailing spaces only for analysis
        label = record.label.strip()

        # Empty label
        if label == "":
            return RuleResult(
                False,
                False,
                "",
                ""
            )

        numeric_tokens = []
        text_tokens = []

        for token in label.split():

            if RuleEngine.is_numeric(token):
                numeric_tokens.append(token)
            else:
                text_tokens.append(token)

        lna = " ".join(numeric_tokens)
        sach = " ".join(text_tokens)

        # Keep original label width
        if lna:
            lna = lna.ljust(original_width)

        if sach:
            sach = sach.ljust(original_width)

        return RuleResult(
            write_lna=bool(lna.strip()),
            write_sach=bool(sach.strip()),
            lna_label=lna,
            sach_label=sach
        )