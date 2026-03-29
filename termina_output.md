(.venv) PS D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper> .\blip2_repro\scripts\run_caption_local.ps1 -Stage2Checkpoint "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\stage2_local_opt350m\20260328150\checkpoint_0.pth"
Not using distributed mode
2026-03-28 18:32:23,574 [INFO] 
=====  Running Parameters    =====
2026-03-28 18:32:23,574 [INFO] {
    "accum_grad_iters": 16,
    "amp": true,
    "annotation_file": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_small_gt.json",
    "batch_size_eval": 1,
    "batch_size_train": 1,
    "device": "cuda",
    "dist_url": "env://",
    "distributed": false,
    "evaluate": false,
    "init_lr": 1e-05,
    "lr_sched": "linear_warmup_cosine_lr",
    "max_epoch": 1,
    "max_len": 30,
    "min_len": 8,
    "min_lr": 0,
    "num_beams": 3,
    "num_workers": 2,
    "output_dir": "output/blip2_repro/caption_local_opt350m",
    "resume_ckpt_path": null,
    "seed": 42,
    "task": "captioning",
    "test_splits": [],
    "train_splits": [
        "train"
    ],
    "valid_splits": [
        "val"
    ],
    "warmup_lr": 1e-08,
    "warmup_steps": 50,
    "weight_decay": 0.05,
    "world_size": 1
}
2026-03-28 18:32:23,574 [INFO]
======  Dataset Attributes  ======
2026-03-28 18:32:23,574 [INFO]
======== coco_caption =======
2026-03-28 18:32:23,575 [INFO] {
    "build_info": {
        "annotations": {
            "test": {
                "md5": "3ff34b0ef2db02d01c37399f6a2a6cd1",
                "storage": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_small.json",
                "url": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_small.json"
            },
            "train": {
                "md5": "aa31ac474cf6250ebb81d18348a07ed8",
                "storage": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_small.json",
                "url": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_small.json"
            },
            "val": {
                "md5": "b273847456ef5580e33713b1f7de52a0",
                "storage": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_small.json",
                "url": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_small.json"
            }
        },
        "images": {
            "storage": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/images"
        }
    },
    "data_type": "images",
    "dataset_card": "dataset_card/coco_caption.md",
    "text_processor": {
        "eval": {
            "name": "blip_caption"
        },
        "train": {
            "name": "blip_caption",
            "prompt": "a photo of "
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
2026-03-28 18:32:23,575 [INFO]
======  Model Attributes  ======
2026-03-28 18:32:23,575 [INFO] {
    "arch": "blip2_opt",
    "drop_path_rate": 0,
    "finetuned": "https://storage.googleapis.com/sfr-vision-language-research/LAVIS/models/BLIP2/blip2_caption_opt2.7b.pth",
    "freeze_vit": true,
    "image_size": 224,
    "load_finetuned": false,
    "load_pretrained": true,
    "model_type": "caption_coco_opt2.7b",
    "num_query_token": 32,
    "opt_model": "facebook/opt-350m",
    "pretrained": "D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/checkpoint_0.pth",
    "prompt": "a photo of",
    "use_grad_checkpoint": false,
    "vit_model": "clip_L",
    "vit_precision": "fp16"
}
2026-03-28 18:32:23,576 [INFO] Using existing file D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_small.json.
2026-03-28 18:32:23,576 [INFO] Using existing file D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_small.json.
2026-03-28 18:32:23,576 [INFO] Using existing file D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_small.json.
2026-03-28 18:32:23,576 [INFO] Building datasets...
2026-03-28 18:32:24,826 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\models\clip_vit.py:255: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  state_dict = torch.load(cached_file, map_location="cpu")

2026-03-28 18:32:25,377 [INFO] freeze vision encoder
2026-03-28 18:32:27,470 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\transformers\modeling_utils.py:488: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  return torch.load(checkpoint_file, map_location=map_location)

2026-03-28 18:32:31,119 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\models\blip2_models\blip2.py:92: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  checkpoint = torch.load(url_or_filename, map_location="cpu")

2026-03-28 18:32:31,790 [INFO] load checkpoint from D:/Purdue/Courses/04. Spring 2026 ECE 59500-073 LEC/Term Paper/repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/checkpoint_0.pth
2026-03-28 18:32:31,794 [INFO] Start training
2026-03-28 18:32:32,429 [INFO] dataset_ratios not specified, datasets will be concatenated (map-style datasets) or chained (webdataset.DataPipeline).
2026-03-28 18:32:32,429 [INFO] Loaded 10000 records for train split from the dataset.
2026-03-28 18:32:32,429 [INFO] Loaded 1000 records for val split from the dataset.
2026-03-28 18:32:32,429 [INFO] Loaded 1000 records for test split from the dataset.
2026-03-28 18:32:32,435 [INFO] number of trainable parameters: 102019072
2026-03-28 18:32:32,437 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\runners\runner_base.py:129: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  self._scaler = torch.cuda.amp.GradScaler()

2026-03-28 18:32:32,437 [INFO] Start training epoch 0, 10000 iters per inner epoch.
2026-03-28 18:32:44,599 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\tasks\base_task.py:225: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  with torch.cuda.amp.autocast(enabled=use_amp):

2026-03-28 18:32:44,602 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\models\blip2_models\blip2.py:42: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  return torch.cuda.amp.autocast(dtype=dtype)

2026-03-28 18:32:44,960 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\torch\nn\functional.py:5560: UserWarning: 1Torch was not compiled with flash attention. (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\builder\windows\pytorch\aten\src\ATen\native\transformers\cuda\sdp_utils.cpp:555.)
  attn_output = scaled_dot_product_attention(q, k, v, attn_mask, dropout_p, is_causal)

Train: data epoch: [0]  [    0/10000]  eta: 1 day, 12:16:51  lr: 0.000000  loss: 0.4781  time: 13.0612  data: 0.0000  max mem: 2136
Train: data epoch: [0]  [   50/10000]  eta: 1:01:58  lr: 0.000010  loss: 0.2413  time: 0.1205  data: 0.0000  max mem: 2446
Train: data epoch: [0]  [  100/10000]  eta: 0:40:58  lr: 0.000010  loss: 0.2956  time: 0.1181  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  150/10000]  eta: 0:33:47  lr: 0.000010  loss: 0.2522  time: 0.1204  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  200/10000]  eta: 0:30:09  lr: 0.000010  loss: 0.2381  time: 0.1221  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  250/10000]  eta: 0:27:54  lr: 0.000010  loss: 0.1912  time: 0.1176  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  300/10000]  eta: 0:26:29  lr: 0.000010  loss: 0.2166  time: 0.1314  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  350/10000]  eta: 0:25:31  lr: 0.000010  loss: 0.1834  time: 0.1204  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  400/10000]  eta: 0:24:39  lr: 0.000010  loss: 0.2645  time: 0.1254  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  450/10000]  eta: 0:23:57  lr: 0.000010  loss: 0.2099  time: 0.1211  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  500/10000]  eta: 0:23:20  lr: 0.000010  loss: 0.2198  time: 0.1208  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  550/10000]  eta: 0:22:52  lr: 0.000010  loss: 0.2394  time: 0.1235  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  600/10000]  eta: 0:22:25  lr: 0.000010  loss: 0.2562  time: 0.1201  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  650/10000]  eta: 0:22:01  lr: 0.000010  loss: 0.1881  time: 0.1180  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  700/10000]  eta: 0:21:39  lr: 0.000010  loss: 0.2582  time: 0.1199  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  750/10000]  eta: 0:21:19  lr: 0.000010  loss: 0.2000  time: 0.1199  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  800/10000]  eta: 0:21:13  lr: 0.000010  loss: 0.2048  time: 0.1673  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  850/10000]  eta: 0:21:02  lr: 0.000010  loss: 0.2194  time: 0.1201  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  900/10000]  eta: 0:20:46  lr: 0.000010  loss: 0.2968  time: 0.1178  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [  950/10000]  eta: 0:20:31  lr: 0.000010  loss: 0.2057  time: 0.1186  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1000/10000]  eta: 0:20:16  lr: 0.000010  loss: 0.2620  time: 0.1177  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1050/10000]  eta: 0:20:02  lr: 0.000010  loss: 0.3191  time: 0.1199  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1100/10000]  eta: 0:19:49  lr: 0.000010  loss: 0.2440  time: 0.1183  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1150/10000]  eta: 0:19:37  lr: 0.000010  loss: 0.2119  time: 0.1197  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1200/10000]  eta: 0:19:27  lr: 0.000010  loss: 0.3411  time: 0.1238  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1250/10000]  eta: 0:19:16  lr: 0.000010  loss: 0.1883  time: 0.1241  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1300/10000]  eta: 0:19:13  lr: 0.000010  loss: 0.1980  time: 0.1440  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1350/10000]  eta: 0:19:03  lr: 0.000010  loss: 0.2678  time: 0.1199  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1400/10000]  eta: 0:18:53  lr: 0.000010  loss: 0.2758  time: 0.1202  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1450/10000]  eta: 0:18:43  lr: 0.000010  loss: 0.1873  time: 0.1198  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1500/10000]  eta: 0:18:33  lr: 0.000010  loss: 0.2126  time: 0.1192  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1550/10000]  eta: 0:18:24  lr: 0.000010  loss: 0.2011  time: 0.1199  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1600/10000]  eta: 0:18:15  lr: 0.000010  loss: 0.3518  time: 0.1200  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1650/10000]  eta: 0:18:05  lr: 0.000010  loss: 0.1835  time: 0.1200  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1700/10000]  eta: 0:17:56  lr: 0.000010  loss: 0.2641  time: 0.1164  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1750/10000]  eta: 0:17:49  lr: 0.000010  loss: 0.2556  time: 0.1306  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1800/10000]  eta: 0:17:45  lr: 0.000010  loss: 0.2800  time: 0.1289  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1850/10000]  eta: 0:17:39  lr: 0.000010  loss: 0.1976  time: 0.1370  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1900/10000]  eta: 0:17:36  lr: 0.000010  loss: 0.2174  time: 0.1500  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 1950/10000]  eta: 0:17:32  lr: 0.000010  loss: 0.3074  time: 0.1316  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2000/10000]  eta: 0:17:22  lr: 0.000010  loss: 0.2755  time: 0.1039  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2050/10000]  eta: 0:17:10  lr: 0.000010  loss: 0.1871  time: 0.1035  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2100/10000]  eta: 0:16:58  lr: 0.000010  loss: 0.2005  time: 0.0993  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2150/10000]  eta: 0:16:46  lr: 0.000010  loss: 0.2992  time: 0.0991  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2200/10000]  eta: 0:16:36  lr: 0.000010  loss: 0.2215  time: 0.1051  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2250/10000]  eta: 0:16:25  lr: 0.000010  loss: 0.1982  time: 0.1034  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2300/10000]  eta: 0:16:18  lr: 0.000010  loss: 0.2804  time: 0.1197  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2350/10000]  eta: 0:16:07  lr: 0.000010  loss: 0.2353  time: 0.1018  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2400/10000]  eta: 0:15:57  lr: 0.000010  loss: 0.1778  time: 0.1030  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2450/10000]  eta: 0:15:48  lr: 0.000010  loss: 0.2454  time: 0.1045  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2500/10000]  eta: 0:15:37  lr: 0.000010  loss: 0.2917  time: 0.1008  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2550/10000]  eta: 0:15:28  lr: 0.000010  loss: 0.2901  time: 0.1078  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2600/10000]  eta: 0:15:19  lr: 0.000010  loss: 0.1665  time: 0.0995  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2650/10000]  eta: 0:15:10  lr: 0.000010  loss: 0.3108  time: 0.1042  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2700/10000]  eta: 0:15:01  lr: 0.000010  loss: 0.1829  time: 0.1045  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2750/10000]  eta: 0:14:52  lr: 0.000010  loss: 0.2408  time: 0.1009  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2800/10000]  eta: 0:14:43  lr: 0.000010  loss: 0.2110  time: 0.1017  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2850/10000]  eta: 0:14:36  lr: 0.000010  loss: 0.1774  time: 0.1243  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2900/10000]  eta: 0:14:29  lr: 0.000010  loss: 0.2056  time: 0.1030  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 2950/10000]  eta: 0:14:20  lr: 0.000010  loss: 0.1743  time: 0.1017  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3000/10000]  eta: 0:14:12  lr: 0.000010  loss: 0.1646  time: 0.1027  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3050/10000]  eta: 0:14:05  lr: 0.000010  loss: 0.1637  time: 0.1095  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3100/10000]  eta: 0:13:56  lr: 0.000010  loss: 0.2036  time: 0.1014  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3150/10000]  eta: 0:13:48  lr: 0.000010  loss: 0.2247  time: 0.1028  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3200/10000]  eta: 0:13:41  lr: 0.000010  loss: 0.1941  time: 0.1081  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3250/10000]  eta: 0:13:33  lr: 0.000010  loss: 0.2512  time: 0.1039  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3300/10000]  eta: 0:13:25  lr: 0.000010  loss: 0.1676  time: 0.1049  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3350/10000]  eta: 0:13:18  lr: 0.000010  loss: 0.2001  time: 0.1144  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3400/10000]  eta: 0:13:11  lr: 0.000010  loss: 0.2975  time: 0.1049  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3450/10000]  eta: 0:13:05  lr: 0.000010  loss: 0.1920  time: 0.1053  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3500/10000]  eta: 0:12:58  lr: 0.000010  loss: 0.1996  time: 0.1024  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3550/10000]  eta: 0:12:51  lr: 0.000010  loss: 0.1949  time: 0.1125  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3600/10000]  eta: 0:12:44  lr: 0.000010  loss: 0.1644  time: 0.1032  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3650/10000]  eta: 0:12:37  lr: 0.000010  loss: 0.2300  time: 0.1075  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3700/10000]  eta: 0:12:30  lr: 0.000010  loss: 0.2755  time: 0.1133  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3750/10000]  eta: 0:12:22  lr: 0.000010  loss: 0.1952  time: 0.1029  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3800/10000]  eta: 0:12:15  lr: 0.000010  loss: 0.2891  time: 0.1010  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3850/10000]  eta: 0:12:08  lr: 0.000010  loss: 0.2611  time: 0.1019  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3900/10000]  eta: 0:12:01  lr: 0.000010  loss: 0.2300  time: 0.1011  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 3950/10000]  eta: 0:11:54  lr: 0.000010  loss: 0.2315  time: 0.1111  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4000/10000]  eta: 0:11:48  lr: 0.000010  loss: 0.3303  time: 0.1186  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4050/10000]  eta: 0:11:42  lr: 0.000010  loss: 0.1846  time: 0.1235  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4100/10000]  eta: 0:11:35  lr: 0.000010  loss: 0.2229  time: 0.1028  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4150/10000]  eta: 0:11:28  lr: 0.000010  loss: 0.2038  time: 0.1023  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4200/10000]  eta: 0:11:21  lr: 0.000010  loss: 0.2243  time: 0.1018  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4250/10000]  eta: 0:11:14  lr: 0.000010  loss: 0.2047  time: 0.1028  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4300/10000]  eta: 0:11:07  lr: 0.000010  loss: 0.1857  time: 0.1011  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4350/10000]  eta: 0:11:01  lr: 0.000010  loss: 0.2268  time: 0.1089  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4400/10000]  eta: 0:10:54  lr: 0.000010  loss: 0.2487  time: 0.1035  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4450/10000]  eta: 0:10:47  lr: 0.000010  loss: 0.2020  time: 0.1032  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4500/10000]  eta: 0:10:41  lr: 0.000010  loss: 0.2584  time: 0.1032  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4550/10000]  eta: 0:10:35  lr: 0.000010  loss: 0.2245  time: 0.1395  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4600/10000]  eta: 0:10:29  lr: 0.000010  loss: 0.2416  time: 0.1037  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4650/10000]  eta: 0:10:22  lr: 0.000010  loss: 0.1967  time: 0.1071  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4700/10000]  eta: 0:10:16  lr: 0.000010  loss: 0.2495  time: 0.1031  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4750/10000]  eta: 0:10:09  lr: 0.000010  loss: 0.2042  time: 0.1041  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4800/10000]  eta: 0:10:03  lr: 0.000010  loss: 0.3142  time: 0.1049  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4850/10000]  eta: 0:09:56  lr: 0.000010  loss: 0.2410  time: 0.1044  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4900/10000]  eta: 0:09:50  lr: 0.000010  loss: 0.1891  time: 0.1018  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 4950/10000]  eta: 0:09:45  lr: 0.000010  loss: 0.1866  time: 0.1486  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5000/10000]  eta: 0:09:40  lr: 0.000010  loss: 0.2521  time: 0.1302  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5050/10000]  eta: 0:09:36  lr: 0.000010  loss: 0.1519  time: 0.1373  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5100/10000]  eta: 0:09:31  lr: 0.000010  loss: 0.2400  time: 0.1352  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5150/10000]  eta: 0:09:26  lr: 0.000010  loss: 0.2048  time: 0.1424  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5200/10000]  eta: 0:09:22  lr: 0.000010  loss: 0.2731  time: 0.1400  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5250/10000]  eta: 0:09:16  lr: 0.000010  loss: 0.2408  time: 0.1290  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5300/10000]  eta: 0:09:11  lr: 0.000010  loss: 0.2190  time: 0.1285  data: 0.0000  max mem: 3309
.0000  max mem: 3309
Train: data epoch: [0]  [ 5800/10000]  eta: 0:08:20  lr: 0.000010  loss: 0.2205  time: 0.1380  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5850/10000]  eta: 0:08:15  lr: 0.000010  loss: 0.2903  time: 0.1502  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5900/10000]  eta: 0:08:10  lr: 0.000010  loss: 0.1484  time: 0.1413  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 5950/10000]  eta: 0:08:05  lr: 0.000010  loss: 0.2583  time: 0.1598  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6000/10000]  eta: 0:07:59  lr: 0.000010  loss: 0.1710  time: 0.1194  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6050/10000]  eta: 0:07:54  lr: 0.000010  loss: 0.2435  time: 0.1415  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6100/10000]  eta: 0:07:49  lr: 0.000010  loss: 0.3083  time: 0.1413  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6150/10000]  eta: 0:07:44  lr: 0.000010  loss: 0.1635  time: 0.1300  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6200/10000]  eta: 0:07:38  lr: 0.000010  loss: 0.1810  time: 0.1402  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6250/10000]  eta: 0:07:33  lr: 0.000010  loss: 0.1897  time: 0.1328  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6300/10000]  eta: 0:07:27  lr: 0.000010  loss: 0.1887  time: 0.1430  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6350/10000]  eta: 0:07:22  lr: 0.000010  loss: 0.2242  time: 0.1462  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6400/10000]  eta: 0:07:17  lr: 0.000010  loss: 0.2700  time: 0.1355  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6450/10000]  eta: 0:07:11  lr: 0.000010  loss: 0.2315  time: 0.1421  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6500/10000]  eta: 0:07:05  lr: 0.000010  loss: 0.2612  time: 0.1268  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6550/10000]  eta: 0:06:59  lr: 0.000010  loss: 0.2093  time: 0.1325  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6600/10000]  eta: 0:06:54  lr: 0.000010  loss: 0.1841  time: 0.1368  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6650/10000]  eta: 0:06:48  lr: 0.000010  loss: 0.2018  time: 0.1389  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6700/10000]  eta: 0:06:42  lr: 0.000010  loss: 0.2348  time: 0.1259  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6750/10000]  eta: 0:06:36  lr: 0.000010  loss: 0.2182  time: 0.1355  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6800/10000]  eta: 0:06:30  lr: 0.000010  loss: 0.2146  time: 0.1426  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6850/10000]  eta: 0:06:25  lr: 0.000010  loss: 0.1695  time: 0.1361  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6900/10000]  eta: 0:06:19  lr: 0.000010  loss: 0.2021  time: 0.1381  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 6950/10000]  eta: 0:06:13  lr: 0.000010  loss: 0.1887  time: 0.1277  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7000/10000]  eta: 0:06:07  lr: 0.000010  loss: 0.2145  time: 0.1298  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7050/10000]  eta: 0:06:01  lr: 0.000010  loss: 0.2959  time: 0.1287  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7100/10000]  eta: 0:05:55  lr: 0.000010  loss: 0.2502  time: 0.1341  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7150/10000]  eta: 0:05:49  lr: 0.000010  loss: 0.1520  time: 0.1372  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7200/10000]  eta: 0:05:43  lr: 0.000010  loss: 0.2543  time: 0.1332  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7250/10000]  eta: 0:05:37  lr: 0.000010  loss: 0.1976  time: 0.1407  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7300/10000]  eta: 0:05:31  lr: 0.000010  loss: 0.2652  time: 0.1369  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7350/10000]  eta: 0:05:25  lr: 0.000010  loss: 0.2966  time: 0.1341  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7400/10000]  eta: 0:05:20  lr: 0.000010  loss: 0.1867  time: 0.1352  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7450/10000]  eta: 0:05:14  lr: 0.000010  loss: 0.2215  time: 0.1301  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7500/10000]  eta: 0:05:08  lr: 0.000010  loss: 0.2092  time: 0.1401  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7550/10000]  eta: 0:05:02  lr: 0.000010  loss: 0.1868  time: 0.1375  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7600/10000]  eta: 0:04:56  lr: 0.000010  loss: 0.3531  time: 0.1373  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7650/10000]  eta: 0:04:50  lr: 0.000010  loss: 0.2628  time: 0.1413  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7700/10000]  eta: 0:04:44  lr: 0.000010  loss: 0.1848  time: 0.1501  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7750/10000]  eta: 0:04:38  lr: 0.000010  loss: 0.1894  time: 0.1411  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7800/10000]  eta: 0:04:32  lr: 0.000010  loss: 0.2833  time: 0.1365  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7850/10000]  eta: 0:04:26  lr: 0.000010  loss: 0.1946  time: 0.1374  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7900/10000]  eta: 0:04:20  lr: 0.000010  loss: 0.2013  time: 0.1339  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 7950/10000]  eta: 0:04:14  lr: 0.000010  loss: 0.1669  time: 0.1323  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8000/10000]  eta: 0:04:08  lr: 0.000010  loss: 0.3344  time: 0.1292  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8050/10000]  eta: 0:04:02  lr: 0.000010  loss: 0.1921  time: 0.1392  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8100/10000]  eta: 0:03:56  lr: 0.000010  loss: 0.1897  time: 0.1306  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8150/10000]  eta: 0:03:50  lr: 0.000010  loss: 0.2308  time: 0.1601  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8200/10000]  eta: 0:03:44  lr: 0.000010  loss: 0.2484  time: 0.1352  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8250/10000]  eta: 0:03:38  lr: 0.000010  loss: 0.2169  time: 0.1359  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8300/10000]  eta: 0:03:32  lr: 0.000010  loss: 0.1701  time: 0.1353  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8350/10000]  eta: 0:03:26  lr: 0.000010  loss: 0.3020  time: 0.1328  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8400/10000]  eta: 0:03:20  lr: 0.000010  loss: 0.2238  time: 0.1350  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8450/10000]  eta: 0:03:13  lr: 0.000010  loss: 0.2564  time: 0.1331  data: 0.0001  max mem: 3309
Train: data epoch: [0]  [ 8500/10000]  eta: 0:03:07  lr: 0.000010  loss: 0.1320  time: 0.1359  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8550/10000]  eta: 0:03:01  lr: 0.000010  loss: 0.1894  time: 0.1614  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8600/10000]  eta: 0:02:55  lr: 0.000010  loss: 0.1787  time: 0.1518  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8650/10000]  eta: 0:02:49  lr: 0.000010  loss: 0.1952  time: 0.1452  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8700/10000]  eta: 0:02:43  lr: 0.000010  loss: 0.1395  time: 0.1328  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8750/10000]  eta: 0:02:37  lr: 0.000010  loss: 0.2118  time: 0.1388  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8800/10000]  eta: 0:02:30  lr: 0.000010  loss: 0.1477  time: 0.1314  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8850/10000]  eta: 0:02:24  lr: 0.000010  loss: 0.2231  time: 0.1396  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8900/10000]  eta: 0:02:18  lr: 0.000010  loss: 0.1855  time: 0.1489  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 8950/10000]  eta: 0:02:12  lr: 0.000010  loss: 0.1944  time: 0.1455  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9000/10000]  eta: 0:02:06  lr: 0.000010  loss: 0.2300  time: 0.1320  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9050/10000]  eta: 0:01:59  lr: 0.000010  loss: 0.2620  time: 0.1490  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9100/10000]  eta: 0:01:53  lr: 0.000010  loss: 0.1414  time: 0.1371  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9150/10000]  eta: 0:01:47  lr: 0.000010  loss: 0.3309  time: 0.1313  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9200/10000]  eta: 0:01:41  lr: 0.000010  loss: 0.3681  time: 0.1369  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9250/10000]  eta: 0:01:34  lr: 0.000010  loss: 0.2033  time: 0.1424  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9300/10000]  eta: 0:01:28  lr: 0.000010  loss: 0.2331  time: 0.1330  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9350/10000]  eta: 0:01:22  lr: 0.000010  loss: 0.2281  time: 0.1295  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9400/10000]  eta: 0:01:16  lr: 0.000010  loss: 0.1634  time: 0.1608  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9450/10000]  eta: 0:01:09  lr: 0.000010  loss: 0.2439  time: 0.1309  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9500/10000]  eta: 0:01:03  lr: 0.000010  loss: 0.1757  time: 0.1373  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9550/10000]  eta: 0:00:57  lr: 0.000010  loss: 0.2217  time: 0.1413  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9600/10000]  eta: 0:00:50  lr: 0.000010  loss: 0.1815  time: 0.1305  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9650/10000]  eta: 0:00:44  lr: 0.000010  loss: 0.1776  time: 0.1379  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9700/10000]  eta: 0:00:38  lr: 0.000010  loss: 0.1501  time: 0.1293  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9750/10000]  eta: 0:00:31  lr: 0.000010  loss: 0.2488  time: 0.1372  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9800/10000]  eta: 0:00:25  lr: 0.000010  loss: 0.1806  time: 0.1296  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9850/10000]  eta: 0:00:19  lr: 0.000010  loss: 0.1474  time: 0.1484  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9900/10000]  eta: 0:00:12  lr: 0.000010  loss: 0.2628  time: 0.1294  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9950/10000]  eta: 0:00:06  lr: 0.000010  loss: 0.1711  time: 0.1341  data: 0.0000  max mem: 3309
Train: data epoch: [0]  [ 9999/10000]  eta: 0:00:00  lr: 0.000010  loss: 0.1327  time: 0.2022  data: 0.0000  max mem: 3309
Train: data epoch: [0] Total time: 0:21:15 (0.1275 s / it)
2026-03-28 18:53:47,479 [INFO] Averaged stats: lr: 0.0000  loss: 0.2267
2026-03-28 18:53:47,480 [INFO] Evaluating on val.
2026-03-28 18:54:00,169 [WARNING] D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\transformers\generation\configuration_utils.py:367: UserWarning: `do_sample` is set to `False`. However, `top_p` is set to `0.9` -- this flag is only used in sample-based generation modes. You should set `do_sample=True` or unset `top_p`.
  warnings.warn(

Evaluation  [   0/1000]  eta: 3:37:59    time: 13.0795  data: 12.4871  max mem: 3309
Evaluation  [  10/1000]  eta: 0:25:12    time: 1.5282  data: 1.1358  max mem: 3309
Evaluation  [  20/1000]  eta: 0:15:40    time: 0.3538  data: 0.0006  max mem: 3309
Evaluation  [  30/1000]  eta: 0:12:15    time: 0.3349  data: 0.0005  max mem: 3309
Evaluation  [  40/1000]  eta: 0:10:31    time: 0.3415  data: 0.0005  max mem: 3309
Evaluation  [  50/1000]  eta: 0:09:28    time: 0.3496  data: 0.0006  max mem: 3309
Evaluation  [  60/1000]  eta: 0:08:39    time: 0.3374  data: 0.0006  max mem: 3309
Evaluation  [  70/1000]  eta: 0:08:22    time: 0.3947  data: 0.0005  max mem: 3309
Evaluation  [  80/1000]  eta: 0:08:04    time: 0.4445  data: 0.0003  max mem: 3309
Evaluation  [  90/1000]  eta: 0:07:37    time: 0.3686  data: 0.0003  max mem: 3309
Evaluation  [ 100/1000]  eta: 0:07:17    time: 0.3209  data: 0.0006  max mem: 3309
Evaluation  [ 110/1000]  eta: 0:07:01    time: 0.3431  data: 0.0006  max mem: 3309
Evaluation  [ 120/1000]  eta: 0:06:46    time: 0.3402  data: 0.0006  max mem: 3309
Evaluation  [ 130/1000]  eta: 0:06:37    time: 0.3580  data: 0.0005  max mem: 3309
Evaluation  [ 140/1000]  eta: 0:06:27    time: 0.3883  data: 0.0004  max mem: 3309
Evaluation  [ 150/1000]  eta: 0:06:17    time: 0.3627  data: 0.0005  max mem: 3309
Evaluation  [ 160/1000]  eta: 0:06:08    time: 0.3478  data: 0.0004  max mem: 3309
Evaluation  [ 170/1000]  eta: 0:05:59    time: 0.3517  data: 0.0004  max mem: 3309
Evaluation  [ 180/1000]  eta: 0:05:52    time: 0.3610  data: 0.0005  max mem: 3309
Evaluation  [ 190/1000]  eta: 0:05:45    time: 0.3676  data: 0.0005  max mem: 3309
Evaluation  [ 200/1000]  eta: 0:05:39    time: 0.3755  data: 0.0005  max mem: 3309
Evaluation  [ 210/1000]  eta: 0:05:34    time: 0.3946  data: 0.0005  max mem: 3309
Evaluation  [ 220/1000]  eta: 0:05:27    time: 0.3750  data: 0.0004  max mem: 3309
Evaluation  [ 230/1000]  eta: 0:05:21    time: 0.3543  data: 0.0004  max mem: 3309
Evaluation  [ 240/1000]  eta: 0:05:16    time: 0.3775  data: 0.0005  max mem: 3309
Evaluation  [ 250/1000]  eta: 0:05:10    time: 0.3744  data: 0.0005  max mem: 3309
Evaluation  [ 260/1000]  eta: 0:05:04    time: 0.3540  data: 0.0005  max mem: 3309
Evaluation  [ 270/1000]  eta: 0:04:59    time: 0.3556  data: 0.0007  max mem: 3309
Evaluation  [ 280/1000]  eta: 0:04:53    time: 0.3647  data: 0.0005  max mem: 3309
Evaluation  [ 290/1000]  eta: 0:04:47    time: 0.3512  data: 0.0003  max mem: 3309
Evaluation  [ 300/1000]  eta: 0:04:42    time: 0.3300  data: 0.0005  max mem: 3309
Evaluation  [ 310/1000]  eta: 0:04:36    time: 0.3312  data: 0.0004  max mem: 3309
Evaluation  [ 320/1000]  eta: 0:04:31    time: 0.3517  data: 0.0003  max mem: 3309
Evaluation  [ 330/1000]  eta: 0:04:27    time: 0.3670  data: 0.0003  max mem: 3309
Evaluation  [ 340/1000]  eta: 0:04:21    time: 0.3481  data: 0.0006  max mem: 3309
Evaluation  [ 350/1000]  eta: 0:04:17    time: 0.3409  data: 0.0008  max mem: 3309
Evaluation  [ 360/1000]  eta: 0:04:12    time: 0.3656  data: 0.0003  max mem: 3309
Evaluation  [ 370/1000]  eta: 0:04:08    time: 0.3677  data: 0.0004  max mem: 3309
Evaluation  [ 380/1000]  eta: 0:04:04    time: 0.3779  data: 0.0005  max mem: 3309
Evaluation  [ 390/1000]  eta: 0:03:59    time: 0.3760  data: 0.0003  max mem: 3309
Evaluation  [ 400/1000]  eta: 0:03:56    time: 0.3999  data: 0.0004  max mem: 3309
Evaluation  [ 410/1000]  eta: 0:03:51    time: 0.3852  data: 0.0005  max mem: 3309
Evaluation  [ 420/1000]  eta: 0:03:46    time: 0.3086  data: 0.0005  max mem: 3309
Evaluation  [ 430/1000]  eta: 0:03:41    time: 0.3136  data: 0.0005  max mem: 3309
Evaluation  [ 440/1000]  eta: 0:03:37    time: 0.3439  data: 0.0007  max mem: 3309
Evaluation  [ 450/1000]  eta: 0:03:33    time: 0.3725  data: 0.0006  max mem: 3309
Evaluation  [ 460/1000]  eta: 0:03:29    time: 0.3935  data: 0.0004  max mem: 3309
Evaluation  [ 470/1000]  eta: 0:03:25    time: 0.3719  data: 0.0004  max mem: 3309
Evaluation  [ 480/1000]  eta: 0:03:21    time: 0.3524  data: 0.0004  max mem: 3309
Evaluation  [ 490/1000]  eta: 0:03:16    time: 0.3545  data: 0.0004  max mem: 3309
Evaluation  [ 500/1000]  eta: 0:03:12    time: 0.3380  data: 0.0005  max mem: 3309
Evaluation  [ 510/1000]  eta: 0:03:08    time: 0.3691  data: 0.0004  max mem: 3309
Evaluation  [ 520/1000]  eta: 0:03:04    time: 0.3838  data: 0.0003  max mem: 3309
Evaluation  [ 530/1000]  eta: 0:03:00    time: 0.3582  data: 0.0003  max mem: 3309
Evaluation  [ 540/1000]  eta: 0:02:56    time: 0.3754  data: 0.0006  max mem: 3309
Evaluation  [ 550/1000]  eta: 0:02:52    time: 0.3594  data: 0.0006  max mem: 3309
Evaluation  [ 560/1000]  eta: 0:02:48    time: 0.3299  data: 0.0006  max mem: 3309
Evaluation  [ 570/1000]  eta: 0:02:44    time: 0.3792  data: 0.0006  max mem: 3309
Evaluation  [ 580/1000]  eta: 0:02:40    time: 0.3999  data: 0.0006  max mem: 3309
Evaluation  [ 590/1000]  eta: 0:02:37    time: 0.3881  data: 0.0006  max mem: 3309
Evaluation  [ 600/1000]  eta: 0:02:33    time: 0.3741  data: 0.0006  max mem: 3309
Evaluation  [ 610/1000]  eta: 0:02:29    time: 0.3556  data: 0.0005  max mem: 3309
Evaluation  [ 620/1000]  eta: 0:02:25    time: 0.3866  data: 0.0005  max mem: 3309
Evaluation  [ 630/1000]  eta: 0:02:21    time: 0.3643  data: 0.0006  max mem: 3309
Evaluation  [ 640/1000]  eta: 0:02:17    time: 0.3383  data: 0.0005  max mem: 3309
Evaluation  [ 650/1000]  eta: 0:02:13    time: 0.3362  data: 0.0004  max mem: 3309
Evaluation  [ 660/1000]  eta: 0:02:09    time: 0.3837  data: 0.0003  max mem: 3309
Evaluation  [ 670/1000]  eta: 0:02:05    time: 0.3891  data: 0.0004  max mem: 3309
Evaluation  [ 680/1000]  eta: 0:02:01    time: 0.3337  data: 0.0004  max mem: 3309
Evaluation  [ 690/1000]  eta: 0:01:57    time: 0.3324  data: 0.0002  max mem: 3309
Evaluation  [ 700/1000]  eta: 0:01:53    time: 0.3327  data: 0.0004  max mem: 3309
Evaluation  [ 710/1000]  eta: 0:01:49    time: 0.3296  data: 0.0005  max mem: 3309
Evaluation  [ 720/1000]  eta: 0:01:45    time: 0.3393  data: 0.0005  max mem: 3309
Evaluation  [ 730/1000]  eta: 0:01:42    time: 0.3742  data: 0.0005  max mem: 3309
Evaluation  [ 740/1000]  eta: 0:01:38    time: 0.3998  data: 0.0005  max mem: 3309
Evaluation  [ 750/1000]  eta: 0:01:34    time: 0.3649  data: 0.0006  max mem: 3309
Evaluation  [ 760/1000]  eta: 0:01:30    time: 0.3429  data: 0.0008  max mem: 3309
Evaluation  [ 770/1000]  eta: 0:01:26    time: 0.3504  data: 0.0008  max mem: 3309
Evaluation  [ 780/1000]  eta: 0:01:22    time: 0.3439  data: 0.0003  max mem: 3309
Evaluation  [ 790/1000]  eta: 0:01:19    time: 0.3470  data: 0.0002  max mem: 3309
Evaluation  [ 800/1000]  eta: 0:01:15    time: 0.3487  data: 0.0004  max mem: 3309
Evaluation  [ 810/1000]  eta: 0:01:11    time: 0.3419  data: 0.0004  max mem: 3309
Evaluation  [ 820/1000]  eta: 0:01:07    time: 0.3291  data: 0.0005  max mem: 3309
Evaluation  [ 830/1000]  eta: 0:01:03    time: 0.3501  data: 0.0006  max mem: 3309
Evaluation  [ 840/1000]  eta: 0:00:59    time: 0.3505  data: 0.0003  max mem: 3309
Evaluation  [ 850/1000]  eta: 0:00:56    time: 0.3381  data: 0.0003  max mem: 3309
Evaluation  [ 860/1000]  eta: 0:00:52    time: 0.3517  data: 0.0004  max mem: 3309
Evaluation  [ 870/1000]  eta: 0:00:48    time: 0.3658  data: 0.0008  max mem: 3309
Evaluation  [ 880/1000]  eta: 0:00:44    time: 0.3978  data: 0.0006  max mem: 3309
Evaluation  [ 890/1000]  eta: 0:00:41    time: 0.4006  data: 0.0002  max mem: 3309
Evaluation  [ 900/1000]  eta: 0:00:37    time: 0.3606  data: 0.0004  max mem: 3309
Evaluation  [ 910/1000]  eta: 0:00:33    time: 0.3614  data: 0.0004  max mem: 3309
Evaluation  [ 920/1000]  eta: 0:00:29    time: 0.3772  data: 0.0004  max mem: 3309
Evaluation  [ 930/1000]  eta: 0:00:26    time: 0.3680  data: 0.0004  max mem: 3309
Evaluation  [ 940/1000]  eta: 0:00:22    time: 0.3294  data: 0.0004  max mem: 3309
Evaluation  [ 950/1000]  eta: 0:00:18    time: 0.3197  data: 0.0005  max mem: 3309
Evaluation  [ 960/1000]  eta: 0:00:14    time: 0.3412  data: 0.0004  max mem: 3309
Evaluation  [ 970/1000]  eta: 0:00:11    time: 0.3290  data: 0.0004  max mem: 3309
Evaluation  [ 980/1000]  eta: 0:00:07    time: 0.3354  data: 0.0005  max mem: 3309
Evaluation  [ 990/1000]  eta: 0:00:03    time: 0.3532  data: 0.0004  max mem: 3309
Evaluation  [ 999/1000]  eta: 0:00:00    time: 0.4128  data: 0.0686  max mem: 3309
Evaluation Total time: 0:06:12 (0.3725 s / it)
2026-03-28 18:59:59,993 [WARNING] rank 0 starts merging results.
result file saved to D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\caption_local_opt350m\20260328183\result\val_epoch0.json
loading annotations into memory...
Done (t=0.00s)
creating index...
index created!
Loading and preparing results...
DONE (t=0.01s)
creating index...
index created!
tokenization...
PTBTokenizer tokenized 61513 tokens at 764298.05 tokens per second.
PTBTokenizer tokenized 9338 tokens at 188230.46 tokens per second.
setting up scorers...
computing Bleu score...
{'testlen': 8278, 'reflen': 8726, 'guess': [8278, 7278, 6278, 5278], 'correct': [3077, 378, 40, 11]}
ratio: 0.948659179463563
Bleu_1: 0.352
Bleu_2: 0.132
Bleu_3: 0.047
Bleu_4: 0.021
computing METEOR score...
Traceback (most recent call last):
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\train.py", line 103, in <module>
    main()
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\train.py", line 99, in main
    runner.train()
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\runners\runner_base.py", line 393, in train
    val_log = self.eval_epoch(
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\torch\utils\_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\runners\runner_base.py", line 494, in eval_epoch
    return self.task.after_evaluation(
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\tasks\captioning.py", line 134, in after_evaluation
    metrics = self._report_metrics(
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\common\dist_utils.py", line 112, in wrapper
    return func(*args, **kwargs)
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\tasks\captioning.py", line 150, in _report_metrics
    coco_val = coco_caption_eval(None, eval_result_file, split_name, annotation_file=self.annotation_file, img_ids=self.img_ids)
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\tasks\captioning.py", line 254, in coco_caption_eval
    coco_eval.evaluate()
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\pycocoevalcap\eval.py", line 53, in evaluate
    score, scores = scorer.compute_score(gts, res)
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\pycocoevalcap\meteor\meteor.py", line 37, in compute_score
    stat = self._stat(res[i][0], gts[i])
  File "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\lib\site-packages\pycocoevalcap\meteor\meteor.py", line 57, in _stat
    self.meteor_p.stdin.flush()
OSError: [Errno 22] Invalid argument
