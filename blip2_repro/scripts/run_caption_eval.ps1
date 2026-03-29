param(
    [Parameter(Mandatory = $true)]
    [string]$PredictionFile,
    [string]$GroundTruthFile = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_val_small_gt.json").Path,
    [string]$OutputPath = (Join-Path (Resolve-Path "$PSScriptRoot\..\..\metrics\blip2").Path "caption_eval_summary.json"),
    [string]$ExamplesOutputPath = (Join-Path (Resolve-Path "$PSScriptRoot\..\..\metrics\blip2").Path "caption_eval_examples.json"),
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path
)

if (-not (Test-Path $PredictionFile)) {
    throw "Prediction file not found: $PredictionFile"
}

if (-not (Test-Path $GroundTruthFile)) {
    throw "Ground-truth file not found: $GroundTruthFile"
}

& $PythonExe `
    "$PSScriptRoot\..\tools\evaluate_caption_subset.py" `
    --gt ((Resolve-Path $GroundTruthFile).Path) `
    --pred ((Resolve-Path $PredictionFile).Path) `
    --output $OutputPath `
    --examples-output $ExamplesOutputPath
