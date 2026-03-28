param(
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path,
    [int]$TrainLimit = 10000,
    [int]$ValLimit = 1000,
    [int]$TestLimit = 1000,
    [int]$Seed = 42
)

$tool = (Resolve-Path "$PSScriptRoot\..\tools\make_json_subset.py").Path
$annDir = Join-Path $LavisRoot "cache\coco\annotations"

$trainIn = Join-Path $annDir "coco_karpathy_train.json"
$valIn = Join-Path $annDir "coco_karpathy_val.json"
$testIn = Join-Path $annDir "coco_karpathy_test.json"

$trainOut = Join-Path $annDir "coco_karpathy_train_small.json"
$valOut = Join-Path $annDir "coco_karpathy_val_small.json"
$testOut = Join-Path $annDir "coco_karpathy_test_small.json"

$required = @($trainIn, $valIn, $testIn)
foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        throw "Missing annotation file: $path. Run .\\blip2_repro\\scripts\\download_coco_karpathy_annotations.ps1 first."
    }
}

& $PythonExe $tool --input $trainIn --output $trainOut --limit $TrainLimit --seed $Seed --shuffle
& $PythonExe $tool --input $valIn --output $valOut --limit $ValLimit --seed $Seed --shuffle
& $PythonExe $tool --input $testIn --output $testOut --limit $TestLimit --seed $Seed --shuffle

Write-Host "Wrote reduced COCO annotation files to $annDir"
