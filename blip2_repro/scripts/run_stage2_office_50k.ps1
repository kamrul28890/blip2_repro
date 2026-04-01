param(
    [Parameter(Mandatory = $true)]
    [string]$Stage1Checkpoint,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage2_office_50k_opt350m.yaml").Path
)

$annotationsRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations").Path

& "$PSScriptRoot\run_stage2_local.ps1" `
    -ConfigPath $ConfigPath `
    -Stage1Checkpoint $Stage1Checkpoint `
    -TrainAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_train_office_50k.json") `
    -ValAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_val_office_1k.json") `
    -TestAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_test_office_1k.json")
