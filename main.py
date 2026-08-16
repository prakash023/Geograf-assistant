from pathlib import Path

from src.processor import PKTProcessor


def main():

    processor = PKTProcessor()

    summary = processor.process(
        input_file=Path("data/input/8026-1G-LNE.PKT"),
        output_folder=Path("data/output"),
        logger=print,
        compare_reference=True
    )

    print("\n" + "=" * 60)
    print("              PKT PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Records Read : {summary['records']}")
    print(f"LNA Records  : {summary['lna']}")
    print(f"Sach Records : {summary['sach']}")
    print("=" * 60)


if __name__ == "__main__":

    try:
        main()

    except Exception as e:

        print("\nERROR")
        print("=" * 60)
        print(e)
        input("\nPress Enter to exit...")
        