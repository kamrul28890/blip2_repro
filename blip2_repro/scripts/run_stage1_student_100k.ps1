param(
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage1_student_100k.yaml").Path,
    [string]$ResumeCheckpoint = ""
)

$annotationsRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations").Path

& "$PSScriptRoot\run_stage1_local.ps1" `
    -ConfigPath $ConfigPath `
    -ResumeCheckpoint $ResumeCheckpoint `
    -TrainAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_train_student_100k.json") `
    -ValAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_val_student_1k.json") `
    -TestAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_test_student_1k.json")
