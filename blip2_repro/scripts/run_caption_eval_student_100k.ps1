param(
    [Parameter(Mandatory = $true)]
    [string]$PredictionFile,
    [string]$OutputPath = (Join-Path (Resolve-Path "$PSScriptRoot\..\..\metrics\blip2").Path "caption_eval_summary_student_100k.json"),
    [string]$ExamplesOutputPath = (Join-Path (Resolve-Path "$PSScriptRoot\..\..\metrics\blip2").Path "caption_eval_examples_student_100k.json")
)

$groundTruth = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_val_student_1k_gt.json").Path

& "$PSScriptRoot\run_caption_eval.ps1" `
    -PredictionFile $PredictionFile `
    -GroundTruthFile $groundTruth `
    -OutputPath $OutputPath `
    -ExamplesOutputPath $ExamplesOutputPath
