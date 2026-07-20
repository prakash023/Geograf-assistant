"""
rules.py
--------

Contains the business logic for splitting LNE labels into
LNA and Sach labels.
"""

from dataclasses import dataclass


@dataclass
class RuleResult:
    """
    Result returned by the rule engine.
    """

    write_lna: bool
    write_sach: bool

    lna_label: str
    sach_label: str


class RuleEngine:

    @staticmethod
    def process(record) -> RuleResult:
        """
        Process one PKT record.

        Current rules:

        R001  Empty label -> Ignore
        R002  Point type 90 + Empty label -> Ignore
        R003  Numbers only -> LNA
        R004  Letters only -> Sach
        R005  Number + Text -> Split
        """

        label = record.label.strip()
        point_type = record.point_type

        # -------------------------------------------------
        # R001
        # Empty label -> Ignore
        # -------------------------------------------------

        if label == "":
            return RuleResult(
                False,
                False,
                "",
                ""
            )

        # -------------------------------------------------
        # R002
        # Point type 90 + Empty label -> Ignore
        # (Explicit business rule)
        # -------------------------------------------------

        if point_type == 90 and label == "":
            return RuleResult(
                False,
                False,
                "",
                ""
            )

        # -------------------------------------------------
        # R003
        # Numbers only -> LNA
        # -------------------------------------------------

        if label.isdigit():
            return RuleResult(
                True,
                False,
                label,
                ""
            )

        # -------------------------------------------------
        # R004
        # Letters only -> Sach
        # -------------------------------------------------

        if label.isalpha():
            return RuleResult(
                False,
                True,
                "",
                label
            )

        # -------------------------------------------------
        # R005
        # Number + Text
        # -------------------------------------------------

        parts = label.split()

        if len(parts) == 2:

            left, right = parts

            if left.isdigit():

                return RuleResult(
                    True,
                    True,
                    left,
                    right
                )

            if right.isdigit():

                return RuleResult(
                    True,
                    True,
                    right,
                    left
                )

        # -------------------------------------------------
        # Unknown pattern
        # -------------------------------------------------

        return RuleResult(
            False,
            False,
            "",
            ""
        )