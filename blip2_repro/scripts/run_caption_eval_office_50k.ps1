param(
    [Parameter(Mandatory = $true)]
    [string]$PredictionFile
)

$groundTruth = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations\coco_karpathy_val_office_1k_gt.json").Path

& "$PSScriptRoot\run_caption_eval.ps1" `
    -PredictionFile $PredictionFile `
    -GroundTruthFile $groundTruth
