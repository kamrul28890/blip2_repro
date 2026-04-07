param(
    [Parameter(Mandatory = $true)]
    [string]$Stage1Checkpoint,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage2_student_100k_opt350m.yaml").Path,
    [string]$ResumeCheckpoint = ""
)

$annotationsRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS\cache\coco\annotations").Path

& "$PSScriptRoot\run_stage2_local.ps1" `
    -ConfigPath $ConfigPath `
    -Stage1Checkpoint $Stage1Checkpoint `
    -ResumeCheckpoint $ResumeCheckpoint `
    -TrainAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_train_student_100k.json") `
    -ValAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_val_student_1k.json") `
    -TestAnnotationPath (Join-Path $annotationsRoot "coco_karpathy_test_student_1k.json")
