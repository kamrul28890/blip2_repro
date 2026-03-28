# Data Layout

## Expected COCO Layout

The working layout is:

```text
repo_study/LAVIS/cache/coco/
  annotations/
    coco_karpathy_train.json
    coco_karpathy_val.json
    coco_karpathy_test.json
    coco_karpathy_train_small.json
    coco_karpathy_val_small.json
    coco_karpathy_test_small.json
  images/
    train2014/
    val2014/
```

## Current Verified State

- Annotation root exists: `repo_study/LAVIS/cache/coco/annotations`
- Reduced subset counts:
  - `coco_karpathy_train_small.json`: `10000`
  - `coco_karpathy_val_small.json`: `1000`
  - `coco_karpathy_test_small.json`: `1000`
- Image root exists: `repo_study/LAVIS/cache/coco/images`
- Image folder counts:
  - `train2014`: `7066`
  - `val2014`: `4605`
  - total unique images staged: `11671`
- Image folder sizes:
  - `train2014`: `1,148,062,726` bytes
  - `val2014`: `754,048,201` bytes
- Sample path from the reduced training subset:
  - `val2014/COCO_val2014_000000293244.jpg`
- Recovered retry path:
  - `val2014/COCO_val2014_000000091349.jpg`

## Verification Target

After image staging, this exact file must exist and load successfully:

```text
repo_study/LAVIS/cache/coco/images/val2014/COCO_val2014_000000293244.jpg
```

## Verified Load Checks

- `repo_study/LAVIS/cache/coco/images/val2014/COCO_val2014_000000293244.jpg` exists
- The sample image loads successfully
- Sample image resolution: `640 x 480`
- The previously missing retry target now also exists

## Path Resolution Notes

- The local BLIP configs now use absolute annotation and image paths
- This is necessary because stock LAVIS resolves relative dataset storage through its default cache root, which points to `/export/home/.cache/lavis` in this repo clone

## Image Staging Policy

- Keep the BLIP-2 configs pointed at the standard LAVIS cache layout
- Prefer staging images into `repo_study/LAVIS/cache/coco/images`
- Do not change local BLIP-2 configs to an external image path unless a later decision makes that necessary
