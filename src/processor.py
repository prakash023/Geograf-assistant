from pathlib import Path

from src.parser import PKTParser
from src.writer import PKTWriter
from src.rules import RuleEngine
from src.comparator import PKTComparator


class PKTProcessor:

    def log(self, message, logger):

        if logger:
            logger(message)
        else:
            print(message)

    # --------------------------------------------------

    @staticmethod
    def replace_label(record, new_label):
        """
        Replace ONLY the text inside the quotation marks.
        Everything else remains untouched.
        """

        return (
            record.raw_line[:record.quote_start + 1]
            + new_label
            + record.raw_line[record.quote_end:]
        )

    # --------------------------------------------------

    def process(
        self,
        input_file,
        output_folder,
        logger=None,
        compare_reference=True
    ):

        input_file = Path(input_file)
        output_folder = Path(output_folder)

        self.log(f"Input File : {input_file}", logger)
        self.log(f"Output Folder : {output_folder}", logger)

        self.log("Reading PKT...", logger)

        parser = PKTParser(input_file)
        records = parser.read()

        lna_lines = []
        sach_lines = []

        self.log("Applying rules...", logger)

        for record in records:

            result = RuleEngine.process(record)

            if result.write_lna:

                lna_lines.append(
                    self.replace_label(
                        record,
                        result.lna_label
                    )
                )

            if result.write_sach:

                sach_lines.append(
                    self.replace_label(
                        record,
                        result.sach_label
                    )
                )

        stem = input_file.stem

        if stem.endswith("-LNE"):

            base = stem[:-4]

            lna_filename = f"{base}-LNA.PKT"
            sach_filename = f"{base}-Sach.PKT"

        else:

            lna_filename = f"{stem}-LNA.PKT"
            sach_filename = f"{stem}-Sach.PKT"

        lna_output = output_folder / lna_filename
        sach_output = output_folder / sach_filename

        self.log(f"LNA Output : {lna_output}", logger)
        self.log(f"Sach Output: {sach_output}", logger)

        self.log("Writing LNA...", logger)

        PKTWriter.write(
            lna_output,
            lna_lines
        )

        self.log("Writing Sach...", logger)

        PKTWriter.write(
            sach_output,
            sach_lines
        )

        if compare_reference:

            reference_folder = Path("data/reference")

            reference_lna = reference_folder / lna_output.name
            reference_sach = reference_folder / sach_output.name

            if reference_lna.exists():

                self.log("Comparing LNA...", logger)

                PKTComparator.compare(
                    reference_lna,
                    lna_output
                )

            if reference_sach.exists():

                self.log("Comparing Sach...", logger)

                PKTComparator.compare(
                    reference_sach,
                    sach_output
                )

        self.log("Finished.", logger)

        return {

            "records": len(records),

            "lna": len(lna_lines),

            "sach": len(sach_lines),

            "lna_output": lna_output,

            "sach_output": sach_output

        }