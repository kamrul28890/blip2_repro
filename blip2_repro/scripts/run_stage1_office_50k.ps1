param(
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage1_office_50k.yaml").Path
)

$annotationsRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations").Path

& "$PSScriptRoot\run_stage1_local.ps1" `
    -ConfigPath $ConfigPath `
    -TrainAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_train_office_50k.json") `
    -ValAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_val_office_1k.json") `
    -TestAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_test_office_1k.json")
