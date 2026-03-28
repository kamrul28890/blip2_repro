param(
    [Parameter(Mandatory = $true)]
    [string]$Stage1Checkpoint,
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage2_local_opt350m.yaml").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path
)

if (-not (Test-Path $Stage1Checkpoint)) {
    throw "Stage-1 checkpoint not found: $Stage1Checkpoint"
}

$Stage1Checkpoint = ((Resolve-Path $Stage1Checkpoint).Path) -replace "\\", "/"

Push-Location $LavisRoot
try {
    & $PythonExe train.py --cfg-path $ConfigPath --options "model.pretrained=$Stage1Checkpoint"
}
finally {
    Pop-Location
}
