param(
    [string]$ResumeCheckpoint = ""
)

& "$PSScriptRoot\run_stage1_student_100k.ps1" `
    -ConfigPath (Resolve-Path "$PSScriptRoot\..\configs\stage1_student_100k_long.yaml").Path `
    -ResumeCheckpoint $ResumeCheckpoint
