param(
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path,
    [int]$TrainLimit = 100000,
    [int]$ValLimit = 1000,
    [int]$TestLimit = 1000,
    [int]$Seed = 42,
    [int]$Workers = 16
)

$subsetTool = (Resolve-Path "$PSScriptRoot\..\tools\make_json_subset.py").Path
$gtTool = (Resolve-Path "$PSScriptRoot\..\tools\build_coco_gt_from_karpathy_subset.py").Path
$downloadTool = (Resolve-Path "$PSScriptRoot\..\..\scripts\download_coco_subset_images.py").Path

$annDir = Join-Path $LavisRoot "cache\coco\annotations"
$imagesDir = Join-Path $LavisRoot "cache\coco\images"

$trainIn = Join-Path $annDir "coco_karpathy_train.json"
$valIn = Join-Path $annDir "coco_karpathy_val.json"
$testIn = Join-Path $annDir "coco_karpathy_test.json"

$trainOut = Join-Path $annDir "coco_karpathy_train_student_100k.json"
$valOut = Join-Path $annDir "coco_karpathy_val_student_1k.json"
$testOut = Join-Path $annDir "coco_karpathy_test_student_1k.json"
$valGtOut = Join-Path $annDir "coco_karpathy_val_student_1k_gt.json"

$required = @($trainIn, $valIn, $testIn)
foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        throw "Missing annotation file: $path. Run .\blip2_repro\scripts\download_coco_karpathy_annotations.ps1 first."
    }
}

& $PythonExe $subsetTool --input $trainIn --output $trainOut --limit $TrainLimit --seed $Seed --shuffle
& $PythonExe $subsetTool --input $valIn --output $valOut --limit $ValLimit --seed $Seed --shuffle
& $PythonExe $subsetTool --input $testIn --output $testOut --limit $TestLimit --seed $Seed --shuffle
& $PythonExe $gtTool --input-json $valOut --output-json $valGtOut

& $PythonExe $downloadTool `
    --annotations-root $annDir `
    --output-root $imagesDir `
    --annotation-files `
        "coco_karpathy_train_student_100k.json" `
        "coco_karpathy_val_student_1k.json" `
        "coco_karpathy_test_student_1k.json" `
    --workers $Workers

Write-Host "Student-scale 100k run assets are ready:"
Write-Host "  Train subset: $trainOut"
Write-Host "  Val subset:   $valOut"
Write-Host "  Test subset:  $testOut"
Write-Host "  Val GT:       $valGtOut"
