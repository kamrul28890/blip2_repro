(.venv) PS D:\Projects\blip2_repro\blip2_repro-1> .\blip2_repro\scripts\run_stage2_office_50k.ps1 -Stage1Checkpoint ".\repo_study\LAVIS\lavis\output\blip2_repro\stage1_office_50k\20260329192\checkpoint_2.pth"
Not using distributed mode
2026-03-30 11:03:34,544 [INFO] 
=====  Running Parameters    =====
2026-03-30 11:03:34,544 [INFO] {
    "accum_grad_iters": 8,
    "amp": true,
    "batch_size_eval": 1,
    "batch_size_train": 1,
    "device": "cuda",
    "dist_url": "env://",
    "distributed": false,
    "evaluate": false,
    "init_lr": 0.0001,
    "lr_sched": "linear_warmup_cosine_lr",
    "max_epoch": 3,
    "min_lr": 1e-05,
    "num_workers": 2,
    "output_dir": "output/blip2_repro/stage2_office_50k_opt350m",
    "resume_ckpt_path": null,
    "seed": 42,
    "task": "image_text_pretrain",
    "test_splits": [],
    "train_splits": [
        "train"
    ],
    "valid_splits": [],
    "warmup_lr": 1e-06,
    "warmup_steps": 50,
    "weight_decay": 0.05,
    "world_size": 1
}
2026-03-30 11:03:34,544 [INFO] 
======  Dataset Attributes  ======
2026-03-30 11:03:34,544 [INFO] 
======== coco_caption =======
2026-03-30 11:03:34,544 [INFO] {
    "build_info": {
        "annotations": {
            "test": {
                "md5": "3ff34b0ef2db02d01c37399f6a2a6cd1",
                "storage": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_office_1k.json",
                "url": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_office_1k.json"
            },
            "train": {
                "md5": "aa31ac474cf6250ebb81d18348a07ed8",
                "storage": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_office_50k.json",
                "url": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_office_50k.json"
            },
            "val": {
                "md5": "b273847456ef5580e33713b1f7de52a0",
                "storage": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_office_1k.json",
                "url": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_office_1k.json"
            }
        },
        "images": {
            "storage": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/images"
        }
    },
    "data_type": "images",
    "dataset_card": "dataset_card/coco_caption.md",
    "text_processor": {
        "eval": {
            "name": "blip_caption"
        },
        "train": {
            "name": "blip_caption"
        }
    },
    "vis_processor": {
        "eval": {
            "image_size": 224,
            "name": "blip_image_eval"
        },
        "train": {
            "image_size": 224,
            "name": "blip2_image_train"
        }
    }
}
2026-03-30 11:03:34,544 [INFO]
======  Model Attributes  ======
2026-03-30 11:03:34,544 [INFO] {
    "arch": "blip2_opt",
    "drop_path_rate": 0,
    "finetuned": "",
    "freeze_vit": true,
    "image_size": 224,
    "load_finetuned": false,
    "load_pretrained": true,
    "model_type": "pretrain_opt2.7b",
    "num_query_token": 32,
    "opt_model": "facebook/opt-350m",
    "pretrained": "D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/lavis/output/blip2_repro/stage1_office_50k/20260329192/checkpoint_2.pth",
    "prompt": "",
    "use_grad_checkpoint": false,
    "vit_model": "clip_L",
    "vit_precision": "fp16"
}
2026-03-30 11:03:34,544 [INFO] Using existing file D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_office_50k.json.
2026-03-30 11:03:34,544 [INFO] Using existing file D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_office_1k.json.
2026-03-30 11:03:34,544 [INFO] Using existing file D:/Projects/blip2_repro/blip2_repro-1/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_office_1k.json.
2026-03-30 11:03:34,544 [INFO] Building datasets...
2026-03-30 11:03:35,770 [WARNING] D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\lavis\models\clip_vit.py:255: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  state_dict = torch.load(cached_file, map_location="cpu")

2026-03-30 11:03:36,028 [INFO] freeze vision encoder
config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 644/644 [00:00<?, ?B/s]
2026-03-30 11:04:07,430 [WARNING] D:\Projects\blip2_repro\blip2_repro-1\.venv\lib\site-packages\huggingface_hub\file_download.py:147: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\Users\Wii-lab-7900x\.cache\huggingface\hub. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to see activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development    
  warnings.warn(message)

merges.txt: 456kB [00:00, 13.7MB/s]
tokenizer_config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 685/685 [00:00<?, ?B/s]
Traceback (most recent call last):
  File "D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\train.py", line 103, in <module>
    main()
  File "D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\train.py", line 94, in main
    model = task.build_model(cfg)
  File "D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\lavis\tasks\base_task.py", line 33, in build_model
    return model_cls.from_config(model_config)
  File "D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\lavis\models\blip2_models\blip2_opt.py", line 413, in from_config
    model = cls(
  File "D:\Projects\blip2_repro\blip2_repro-1\repo_study\LAVIS\lavis\models\blip2_models\blip2_opt.py", line 85, in __init__
    self.opt_tokenizer = AutoTokenizer.from_pretrained(opt_model, use_fast=False)
  File "D:\Projects\blip2_repro\blip2_repro-1\.venv\lib\site-packages\transformers\models\auto\tokenization_auto.py", line 757, in from_pretrained
    return tokenizer_class_py.from_pretrained(pretrained_model_name_or_path, *inputs, **kwargs)
  File "D:\Projects\blip2_repro\blip2_repro-1\.venv\lib\site-packages\transformers\tokenization_utils_base.py", line 1854, in from_pretrained
    return cls._from_pretrained(
  File "D:\Projects\blip2_repro\blip2_repro-1\.venv\lib\site-packages\transformers\tokenization_utils_base.py", line 2017, in _from_pretrained
    tokenizer = cls(*init_inputs, **init_kwargs)
  File "D:\Projects\blip2_repro\blip2_repro-1\.venv\lib\site-packages\transformers\models\gpt2\tokenization_gpt2.py", line 188, in __init__
    with open(vocab_file, encoding="utf-8") as vocab_handle:
TypeError: expected str, bytes or os.PathLike object, not NoneType
(.venv) PS D:\Projects\blip2_repro\blip2_repro-1> 