[CmdletBinding()]
param(
    [string]$Stage1Directory = (Join-Path $PSScriptRoot "..\..\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$directory = (Resolve-Path -LiteralPath $Stage1Directory).Path
$outputFile = Join-Path $directory "checkpoint_0.pth"
$hashFile = Join-Path $directory "checkpoint_0.pth.sha256"
$parts = Get-ChildItem -LiteralPath $directory -Filter "checkpoint_0.pth.part*" | Sort-Object Name

if ($parts.Count -eq 0) {
    throw "No stage-1 checkpoint parts were found in '$directory'."
}

if (-not (Test-Path -LiteralPath $hashFile)) {
    throw "Missing hash manifest '$hashFile'."
}

if ((Test-Path -LiteralPath $outputFile) -and -not $Force) {
    throw "Output file '$outputFile' already exists. Re-run with -Force to overwrite it."
}

if (Test-Path -LiteralPath $outputFile) {
    Remove-Item -LiteralPath $outputFile -Force
}

$outStream = [System.IO.File]::Open($outputFile, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
try {
    foreach ($part in $parts) {
        $bytes = [System.IO.File]::ReadAllBytes($part.FullName)
        $outStream.Write($bytes, 0, $bytes.Length)
    }
}
finally {
    $outStream.Dispose()
}

$expectedHash = (Get-Content -LiteralPath $hashFile | Select-Object -First 1).Trim().Split(" ")[0].ToUpperInvariant()
$actualHash = (Get-FileHash -LiteralPath $outputFile -Algorithm SHA256).Hash.ToUpperInvariant()

if ($actualHash -ne $expectedHash) {
    throw "Hash mismatch for '$outputFile'. Expected $expectedHash but got $actualHash."
}

Write-Host "Reassembled stage-1 checkpoint at $outputFile"
Write-Host "SHA256 verified: $actualHash"
