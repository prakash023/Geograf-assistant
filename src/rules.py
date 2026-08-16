"""
rules.py
--------

Business logic for splitting LNE labels into
LNA and Sach labels.

Confirmed rules:

R000  AA2014... point -> Ignore completely
R001  Empty label -> Ignore
R002  Integer only -> LNA
R003  Text only -> Sach
R004  Integer + Decimal -> Split
R005  Decimal measurement -> Sach
R006  Text + Integer -> Split
R999  Unknown pattern -> Sach

Important:
- AA2014... records are excluded from both outputs.
- Empty labels are excluded from both outputs.
- Integer + decimal:
      Integer -> LNA
      Decimal -> Sach
- Decimal-containing descriptive labels remain in Sach.
- Original spacing inside quotation marks is preserved.
"""


import re
from dataclasses import dataclass


# ==========================================================
# Result
# ==========================================================

@dataclass
class RuleResult:

    write_lna: bool
    write_sach: bool

    lna_label: str
    sach_label: str


# ==========================================================
# Rule Engine
# ==========================================================

class RuleEngine:

    INTEGER = re.compile(
        r"^[+-]?\d+$"
    )

    DECIMAL = re.compile(
        r"^[+-]?\d+\.\d+$"
    )

    # ======================================================
    # Number checks
    # ======================================================

    @staticmethod
    def is_integer(token: str) -> bool:

        return bool(
            RuleEngine.INTEGER.fullmatch(token)
        )

    # ------------------------------------------------------

    @staticmethod
    def is_decimal(token: str) -> bool:

        return bool(
            RuleEngine.DECIMAL.fullmatch(token)
        )

    # ======================================================
    # R000
    # AA2014... point
    # ======================================================

    @staticmethod
    def rule_ignore_aa2014(record):
        """
        Ignore points beginning with AA2014.

        Examples:

            AA201437 ... "Bst    "
            AA201433 ... "Bst -0.1   "

        These records must be written to neither
        LNA nor Sach.
        """

        point_number = record.point_number

        if point_number.startswith("AA2014"):

            return RuleResult(
                write_lna=False,
                write_sach=False,
                lna_label="",
                sach_label=""
            )

        return None

    # ======================================================
    # R001
    # Empty label
    # ======================================================

    @staticmethod
    def rule_empty(label):
        """
        Empty label -> Ignore completely.
        """

        if label.strip() == "":

            return RuleResult(
                write_lna=False,
                write_sach=False,
                lna_label="",
                sach_label=""
            )

        return None

    # ======================================================
    # R002
    # Integer only
    # ======================================================

    @staticmethod
    def rule_integer_only(label):
        """
        Integer-only label -> LNA.

        Example:

            "76    "
        """

        if RuleEngine.is_integer(label.strip()):

            return RuleResult(
                write_lna=True,
                write_sach=False,
                lna_label=label,
                sach_label=""
            )

        return None

    # ======================================================
    # R003
    # Text only
    # ======================================================

    @staticmethod
    def rule_text_only(label):
        """
        Text-only label -> Sach.

        Examples:

            "BP    "
            "Bst   "
            "WASSERSCHIEBER"
        """

        tokens = label.split()

        if len(tokens) != 1:
            return None

        token = tokens[0]

        if (
            not RuleEngine.is_integer(token)
            and
            not RuleEngine.is_decimal(token)
        ):

            return RuleResult(
                write_lna=False,
                write_sach=True,
                lna_label="",
                sach_label=label
            )

        return None

    # ======================================================
    # R004
    # Integer + Decimal
    # ======================================================

    @staticmethod
    def rule_integer_decimal(label):
        """
        Integer followed by a decimal measurement.

        Examples:

            "15 0.280   "
            "25 0.280   "
            "76 0.280   "
            "2516 0.280   "

        Result:

            LNA:
                integer

            Sach:
                decimal
        """

        match = re.fullmatch(
            r"\s*"
            r"([+-]?\d+)"
            r"(\s+)"
            r"([+-]?\d+\.\d+)"
            r"(\s*)",
            label
        )

        if not match:
            return None

        integer_part = match.group(1)
        decimal_part = match.group(3)
        trailing_spaces = match.group(4)

        # Integer is the line identifier.
        lna = integer_part + "    "

        # Decimal measurement remains in Sach.
        sach = decimal_part + trailing_spaces

        return RuleResult(
            write_lna=True,
            write_sach=True,
            lna_label=lna,
            sach_label=sach
        )

    # ======================================================
    # R005
    # Decimal measurement
    # ======================================================

    @staticmethod
    def rule_decimal_measurement(label):
        """
        Any decimal-containing label that was not
        handled by R004 remains completely in Sach.

        Examples:

            "0.280   "
            "0.250   "
            "L 0.400 4.000 einst mmig"
            "FI 1.000 7.000 einst mmig"
            "Bst -0.1   "
        """

        for token in label.split():

            if RuleEngine.is_decimal(token):

                return RuleResult(
                    write_lna=False,
                    write_sach=True,
                    lna_label="",
                    sach_label=label
                )

        return None

    # ======================================================
    # R006
    # Text + Integer
    # ======================================================

    @staticmethod
    def rule_integer_identifier(label):
        """
        Text followed by an integer identifier.

        Example:

            "METALL.GEGENFAHRSCHUTZ 71   "

        Result:

            LNA:
                "71   "

            Sach:
                "METALL.GEGENFAHRSCHUTZ    "
        """

        match = re.fullmatch(
            r"^(.*?)(\s+)([+-]?\d+)(\s*)$",
            label
        )

        if not match:
            return None

        text_part = match.group(1)
        separator = match.group(2)
        integer_part = match.group(3)
        trailing_spaces = match.group(4)

        if text_part.strip() == "":
            return None

        # Decimal-containing text belongs entirely
        # to Sach.
        for token in text_part.split():

            if RuleEngine.is_decimal(token):
                return None

        # Integer -> LNA
        lna = (
            integer_part
            + trailing_spaces
        )

        # Text -> Sach
        sach = (
            text_part
            + separator
            + trailing_spaces
        )

        return RuleResult(
            write_lna=True,
            write_sach=True,
            lna_label=lna,
            sach_label=sach
        )

    # ======================================================
    # R999
    # Unknown pattern
    # ======================================================

    @staticmethod
    def rule_default(label):

        return RuleResult(
            write_lna=False,
            write_sach=True,
            lna_label="",
            sach_label=label
        )

    # ======================================================
    # Main
    # ======================================================

    @staticmethod
    def process(record):

        # --------------------------------------------------
        # R000
        # AA2014... -> Ignore
        # --------------------------------------------------

        result = RuleEngine.rule_ignore_aa2014(record)

        if result is not None:
            return result

        # --------------------------------------------------
        # Original label
        # --------------------------------------------------

        label = record.label

        # --------------------------------------------------
        # R001
        # Empty -> Ignore
        # --------------------------------------------------

        result = RuleEngine.rule_empty(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R002
        # Integer only -> LNA
        # --------------------------------------------------

        result = RuleEngine.rule_integer_only(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R003
        # Text only -> Sach
        # --------------------------------------------------

        result = RuleEngine.rule_text_only(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R004
        # Integer + Decimal -> Split
        # --------------------------------------------------

        result = RuleEngine.rule_integer_decimal(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R005
        # Decimal -> Sach
        # --------------------------------------------------

        result = RuleEngine.rule_decimal_measurement(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R006
        # Text + Integer -> Split
        # --------------------------------------------------

        result = RuleEngine.rule_integer_identifier(label)

        if result is not None:
            return result

        # --------------------------------------------------
        # R999
        # Unknown -> Sach
        # --------------------------------------------------

        return RuleEngine.rule_default(label)