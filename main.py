from pathlib import Path

from src.parser import PKTParser
from src.formatter import PKTFormatter
from src.writer import PKTWriter
from src.rules import RuleEngine
from src.comparator import PKTComparator


def main():

    # =======================================================
    # Input File
    # =======================================================
    input_file = Path("data/input/8026-1G-LNE.PKT")

    # =======================================================
    # Read PKT File
    # =======================================================
    parser = PKTParser(input_file)
    records = parser.read()

    lna_lines = []
    sach_lines = []

    # =======================================================
    # Process Records
    # =======================================================
    for record in records:

        result = RuleEngine.process(record)

        if result.write_lna:
            lna_lines.append(
                PKTFormatter.replace_label(
                    record,
                    result.lna_label
                )
            )

        if result.write_sach:
            sach_lines.append(
                PKTFormatter.replace_label(
                    record,
                    result.sach_label
                )
            )

    # =======================================================
    # Create Output File Names
    # =======================================================
    output_folder = Path("data/output")

    lna_filename = input_file.name.replace("-LNE.PKT", "-LNA.PKT")
    sach_filename = input_file.name.replace("-LNE.PKT", "-Sach.PKT")

    lna_output = output_folder / lna_filename
    sach_output = output_folder / sach_filename

    # =======================================================
    # Write Output Files
    # =======================================================
    PKTWriter.write(lna_output, lna_lines)
    PKTWriter.write(sach_output, sach_lines)

    # =======================================================
    # Processing Summary
    # =======================================================
    print("\n" + "=" * 60)
    print("              PKT PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Input File     : {input_file.name}")
    print(f"LNA Output     : {lna_output.name}")
    print(f"Sach Output    : {sach_output.name}")
    print("-" * 60)
    print(f"Records Read   : {len(records)}")
    print(f"LNA Records    : {len(lna_lines)}")
    print(f"Sach Records   : {len(sach_lines)}")
    print("=" * 60)

    # =======================================================
    # Compare With Reference Files
    # =======================================================
    reference_folder = Path("data/reference")

    reference_lna = reference_folder / lna_output.name
    reference_sach = reference_folder / sach_output.name

    print("\n")
    print("=" * 60)
    print("             COMPARISON RESULTS")
    print("=" * 60)

    # Compare LNA
    if reference_lna.exists():

        print(f"\nComparing {lna_output.name}")
        PKTComparator.compare(
            reference_lna,
            lna_output
        )

    else:

        print(f"\nReference file not found: {reference_lna}")

    # Compare Sach
    if reference_sach.exists():

        print(f"\nComparing {sach_output.name}")
        PKTComparator.compare(
            reference_sach,
            sach_output
        )

    else:

        print(f"\nReference file not found: {reference_sach}")


if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        print("\nERROR")
        print("=" * 60)
        print(e)
        input("\nPress Enter to exit...")