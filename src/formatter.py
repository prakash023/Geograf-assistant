from src.parser import PKTRecord


class PKTFormatter:
    """
    Responsible only for rebuilding a PKT line.
    It never decides WHAT the label should be.
    """

    @staticmethod
    def replace_label(record: PKTRecord, new_label: str) -> str:
        """
        Replace only the text inside the quotation marks.
        """

        return (
            record.raw_line[:record.quote_start + 1]
            + new_label
            + record.raw_line[record.quote_end:]
        )

    @staticmethod
    def keep_original(record: PKTRecord) -> str:
        """
        Return the original line unchanged.
        """

        return record.raw_line