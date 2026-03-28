import argparse
import json
import random
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a deterministic subset from a JSON list file."
    )
    parser.add_argument("--input", required=True, help="Path to the source JSON file.")
    parser.add_argument("--output", required=True, help="Path to the subset JSON file.")
    parser.add_argument(
        "--limit",
        required=True,
        type=int,
        help="Maximum number of records to keep.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used when shuffling.",
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Shuffle before truncating.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8") as infile:
        payload = json.load(infile)

    if not isinstance(payload, list):
        raise ValueError(f"Expected a JSON list in {input_path}")

    rows = list(payload)
    if args.shuffle:
        rng = random.Random(args.seed)
        rng.shuffle(rows)

    subset = rows[: args.limit]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as outfile:
        json.dump(subset, outfile, indent=2)

    print(
        f"Wrote {len(subset)} of {len(rows)} records from {input_path} to {output_path}"
    )


if __name__ == "__main__":
    main()
