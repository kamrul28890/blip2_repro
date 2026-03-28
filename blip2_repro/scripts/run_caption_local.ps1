param(
    [Parameter(Mandatory = $true)]
    [string]$Stage2Checkpoint,
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\caption_local_opt350m.yaml").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path
)

if (-not (Test-Path $Stage2Checkpoint)) {
    throw "Stage-2 checkpoint not found: $Stage2Checkpoint"
}

$Stage2Checkpoint = ((Resolve-Path $Stage2Checkpoint).Path) -replace "\\", "/"

Push-Location $LavisRoot
try {
    & $PythonExe train.py --cfg-path $ConfigPath --options "model.pretrained=$Stage2Checkpoint"
}
finally {
    Pop-Location
}
