import argparse
import json
import re
from pathlib import Path


IMAGE_ID_PATTERN = re.compile(r"_(\d+)\.[^.]+$")


def extract_image_id(image_path: str) -> int:
    match = IMAGE_ID_PATTERN.search(Path(image_path).name)
    if not match:
        raise ValueError(f"Could not extract COCO image id from: {image_path}")
    return int(match.group(1))


def build_gt(records):
    coco_gt = {"annotations": [], "images": []}
    seen_images = set()
    ann_id = 0

    for record in records:
        image_id = extract_image_id(record["image"])
        if image_id not in seen_images:
            coco_gt["images"].append({"id": image_id})
            seen_images.add(image_id)

        captions = record["caption"]
        if isinstance(captions, str):
            captions = [captions]

        for caption in captions:
            coco_gt["annotations"].append(
                {
                    "image_id": image_id,
                    "caption": caption,
                    "id": ann_id,
                }
            )
            ann_id += 1

    return coco_gt


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Karpathy-style COCO subset JSON into COCO caption-eval ground truth."
    )
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_json)
    output_path = Path(args.output_json)

    records = json.loads(input_path.read_text(encoding="utf-8"))
    coco_gt = build_gt(records)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(coco_gt), encoding="utf-8")

    print(f"wrote {len(coco_gt['images'])} images and {len(coco_gt['annotations'])} annotations to {output_path}")


if __name__ == "__main__":
    main()
