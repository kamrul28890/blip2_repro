param(
    [Parameter(Mandatory = $true)]
    [string]$Stage1Checkpoint,
    [string]$ResumeCheckpoint = ""
)

& "$PSScriptRoot\run_stage2_student_100k.ps1" `
    -Stage1Checkpoint $Stage1Checkpoint `
    -ConfigPath (Resolve-Path "$PSScriptRoot\..\configs\stage2_student_100k_opt350m_long.yaml").Path `
    -ResumeCheckpoint $ResumeCheckpoint
