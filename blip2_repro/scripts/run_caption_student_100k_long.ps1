param(
    [Parameter(Mandatory = $true)]
    [string]$Stage2Checkpoint,
    [string]$ResumeCheckpoint = ""
)

& "$PSScriptRoot\run_caption_student_100k.ps1" `
    -Stage2Checkpoint $Stage2Checkpoint `
    -ConfigPath (Resolve-Path "$PSScriptRoot\..\configs\caption_student_100k_opt350m_long.yaml").Path `
    -ResumeCheckpoint $ResumeCheckpoint
