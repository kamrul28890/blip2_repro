param(
    [Parameter(Mandatory = $true)]
    [string]$Stage1Checkpoint,
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage2_local_opt350m.yaml").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path,
    [string]$TrainAnnotationPath = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_train_small.json").Path,
    [string]$ValAnnotationPath = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_val_small.json").Path,
    [string]$TestAnnotationPath = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_test_small.json").Path,
    [string]$ImagesRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\images").Path
)

if (-not (Test-Path $Stage1Checkpoint)) {
    throw "Stage-1 checkpoint not found: $Stage1Checkpoint"
}

$Stage1Checkpoint = ((Resolve-Path $Stage1Checkpoint).Path) -replace "\\", "/"
$TrainAnnotation = ((Resolve-Path $TrainAnnotationPath).Path) -replace "\\", "/"
$ValAnnotation = ((Resolve-Path $ValAnnotationPath).Path) -replace "\\", "/"
$TestAnnotation = ((Resolve-Path $TestAnnotationPath).Path) -replace "\\", "/"
$ImagesRoot = ((Resolve-Path $ImagesRoot).Path) -replace "\\", "/"

$Options = @(
    "model.pretrained=$Stage1Checkpoint",
    "datasets.coco_caption.build_info.annotations.train.url=$TrainAnnotation",
    "datasets.coco_caption.build_info.annotations.train.storage=$TrainAnnotation",
    "datasets.coco_caption.build_info.annotations.val.url=$ValAnnotation",
    "datasets.coco_caption.build_info.annotations.val.storage=$ValAnnotation",
    "datasets.coco_caption.build_info.annotations.test.url=$TestAnnotation",
    "datasets.coco_caption.build_info.annotations.test.storage=$TestAnnotation",
    "datasets.coco_caption.build_info.images.storage=$ImagesRoot"
)

Push-Location $LavisRoot
try {
    & $PythonExe train.py --cfg-path $ConfigPath --options $Options
}
finally {
    Pop-Location
}
