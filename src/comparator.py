"""
comparator.py
-------------

Compares two PKT files line by line.
"""

from pathlib import Path


class PKTComparator:

    @staticmethod
    def compare(reference_file, generated_file):

        reference_file = Path(reference_file)
        generated_file = Path(generated_file)

        with reference_file.open("r", encoding="latin-1") as f:
            reference = [line.rstrip("\n") for line in f]

        with generated_file.open("r", encoding="latin-1") as f:
            generated = [line.rstrip("\n") for line in f]

        print("\n" + "=" * 70)
        print("COMPARISON REPORT")
        print("=" * 70)

        print(f"Reference : {reference_file.name}")
        print(f"Generated : {generated_file.name}")
        print()

        print(f"Reference lines : {len(reference)}")
        print(f"Generated lines : {len(generated)}")
        print()

        differences = 0

        for i, (ref, gen) in enumerate(zip(reference, generated), start=1):

            if ref != gen:

                differences += 1

                print("-" * 70)
                print(f"Difference at line {i}")
                print()
                print("Reference:")
                print(ref)
                print()
                print("Generated:")
                print(gen)
                print()

        if len(reference) != len(generated):

            differences += abs(len(reference) - len(generated))

            print("-" * 70)
            print("Files have different number of lines.")

        print("=" * 70)
        print(f"Total differences : {differences}")
        print("=" * 70)

        return differences