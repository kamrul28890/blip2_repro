import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider


def load_ground_truth(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    for ann in data["annotations"]:
        grouped[int(ann["image_id"])].append(ann["caption"])
    return grouped


def load_predictions(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped = {}
    for item in data:
        grouped[int(item["image_id"])] = [item["caption"]]
    return grouped


def compute_scores(gts, res):
    bleu_scorer = Bleu(4)
    bleu_score, _ = bleu_scorer.compute_score(gts, res)

    cider_scorer = Cider()
    cider_score, _ = cider_scorer.compute_score(gts, res)

    return {
        "Bleu_1": float(bleu_score[0]),
        "Bleu_2": float(bleu_score[1]),
        "Bleu_3": float(bleu_score[2]),
        "Bleu_4": float(bleu_score[3]),
        "CIDEr": float(cider_score),
    }


def compute_diversity(res):
    captions = [v[0] for _, v in sorted(res.items())]
    counts = Counter(captions)
    top = counts.most_common(10)
    return {
        "prediction_count": len(captions),
        "unique_caption_count": len(counts),
        "most_common_caption": top[0][0] if top else "",
        "most_common_caption_count": int(top[0][1]) if top else 0,
        "top_5_caption_coverage": int(sum(count for _, count in top[:5])),
        "top_10_caption_coverage": int(sum(count for _, count in top[:10])),
        "top_captions": [
            {"caption": caption, "count": int(count)} for caption, count in top
        ],
    }


def build_examples(gts, res, example_ids):
    examples = []
    for image_id in example_ids:
        if image_id not in gts or image_id not in res:
            continue
        examples.append(
            {
                "image_id": image_id,
                "references": gts[image_id],
                "prediction": res[image_id][0],
            }
        )
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt", required=True, type=Path)
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--examples-output", type=Path)
    parser.add_argument(
        "--example-ids",
        type=int,
        nargs="*",
        default=[91500, 511622, 341113, 407403, 353027, 31240],
    )
    args = parser.parse_args()

    gts = load_ground_truth(args.gt)
    res = load_predictions(args.pred)

    gt_ids = set(gts.keys())
    pred_ids = set(res.keys())
    common_ids = sorted(gt_ids & pred_ids)
    aligned_gts = {image_id: gts[image_id] for image_id in common_ids}
    aligned_res = {image_id: res[image_id] for image_id in common_ids}

    scores = compute_scores(aligned_gts, aligned_res)
    diversity = compute_diversity(aligned_res)

    summary = {
        "ground_truth_path": str(args.gt.resolve()),
        "prediction_path": str(args.pred.resolve()),
        "aligned_image_count": len(common_ids),
        "missing_in_predictions": len(gt_ids - pred_ids),
        "extra_predictions": len(pred_ids - gt_ids),
        "metrics": scores,
        "diversity": diversity,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if args.examples_output:
        examples = build_examples(aligned_gts, aligned_res, args.example_ids)
        args.examples_output.parent.mkdir(parents=True, exist_ok=True)
        args.examples_output.write_text(
            json.dumps(examples, indent=2), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
