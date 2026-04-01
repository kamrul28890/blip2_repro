import argparse
import concurrent.futures
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


BASE_URL = "http://images.cocodataset.org/"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download the unique COCO images referenced by reduced annotation files."
    )
    parser.add_argument(
        "--annotations-root",
        required=True,
        help="Directory containing the reduced COCO annotation JSON files.",
    )
    parser.add_argument(
        "--output-root",
        required=True,
        help="Directory that will become repo_study/LAVIS/cache/coco/images.",
    )
    parser.add_argument(
        "--annotation-files",
        nargs="+",
        default=[
            "coco_karpathy_train_small.json",
            "coco_karpathy_val_small.json",
            "coco_karpathy_test_small.json",
        ],
        help="Annotation JSON filenames under --annotations-root to scan for image paths.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=16,
        help="Number of concurrent download workers.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retries for transient download failures.",
    )
    parser.add_argument(
        "--retry-delay-seconds",
        type=float,
        default=1.5,
        help="Delay between retry attempts for transient download failures.",
    )
    return parser.parse_args()


def collect_unique_images(
    annotations_root: Path, annotation_files: list[str]
) -> list[str]:
    unique_images = set()
    for name in annotation_files:
        payload = json.loads((annotations_root / name).read_text(encoding="utf-8"))
        for row in payload:
            unique_images.add(row["image"])
    return sorted(unique_images)


def download_one(
    relative_path: str, output_root: Path, retries: int, retry_delay_seconds: float
) -> tuple[str, str]:
    destination = output_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        return relative_path, "exists"

    url = BASE_URL + relative_path.replace("\\", "/")
    attempts = max(1, retries + 1)

    for attempt in range(1, attempts + 1):
        try:
            urllib.request.urlretrieve(url, destination)
            return relative_path, "downloaded"
        except urllib.error.HTTPError as exc:
            if attempt < attempts and exc.code in {429, 500, 502, 503, 504}:
                time.sleep(retry_delay_seconds)
                continue
            return relative_path, f"http_error:{exc.code}"
        except urllib.error.URLError as exc:
            if attempt < attempts:
                time.sleep(retry_delay_seconds)
                continue
            return relative_path, f"url_error:{exc.reason}"
        except Exception as exc:  # pragma: no cover - defensive logging
            if attempt < attempts:
                time.sleep(retry_delay_seconds)
                continue
            return relative_path, f"error:{exc}"


def main():
    args = parse_args()
    annotations_root = Path(args.annotations_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    images = collect_unique_images(annotations_root, args.annotation_files)
    print(f"unique_images={len(images)}")

    counters = {
        "downloaded": 0,
        "exists": 0,
        "failed": 0,
    }
    failures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                download_one,
                image_path,
                output_root,
                args.retries,
                args.retry_delay_seconds,
            ): image_path
            for image_path in images
        }
        for index, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            image_path, status = future.result()
            if status == "downloaded":
                counters["downloaded"] += 1
            elif status == "exists":
                counters["exists"] += 1
            else:
                counters["failed"] += 1
                failures.append((image_path, status))

            if index % 200 == 0 or index == len(images):
                print(
                    f"progress={index}/{len(images)} "
                    f"downloaded={counters['downloaded']} "
                    f"exists={counters['exists']} "
                    f"failed={counters['failed']}"
                )
                sys.stdout.flush()

    print("summary")
    print(json.dumps(counters, indent=2))

    if failures:
        print("failures")
        for image_path, status in failures[:50]:
            print(f"{image_path} -> {status}")
        sys.exit(1)


if __name__ == "__main__":
    main()
