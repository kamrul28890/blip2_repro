param(
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path,
    [string]$ConfigPath = (Resolve-Path "$PSScriptRoot\..\configs\stage1_local.yaml").Path,
    [string]$PythonExe = (Resolve-Path "$PSScriptRoot\..\..\.venv\Scripts\python.exe").Path
)

Push-Location $LavisRoot
try {
    & $PythonExe train.py --cfg-path $ConfigPath
}
finally {
    Pop-Location
}
