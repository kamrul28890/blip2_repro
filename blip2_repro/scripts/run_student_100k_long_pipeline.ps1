param(
    [switch]$PrepareData,
    [string]$Stage1Checkpoint = "",
    [string]$Stage2Checkpoint = "",
    [string]$Stage1ResumeCheckpoint = "",
    [string]$Stage2ResumeCheckpoint = "",
    [string]$CaptionResumeCheckpoint = "",
    [switch]$EvaluateAllCaptionEpochs = $true
)

$repoRoot = (Resolve-Path "$PSScriptRoot\..\..").Path
$outputRoot = Join-Path $repoRoot "repo_study\LAVIS\lavis\output\blip2_repro"
$metricsRoot = Join-Path $repoRoot "metrics\blip2"

function Resolve-OptionalPath {
    param([string]$PathValue)

    if (-not $PathValue) {
        return ""
    }

    if (-not (Test-Path $PathValue)) {
        throw "Path not found: $PathValue"
    }

    return (Resolve-Path $PathValue).Path
}

function Get-LatestRunDirectory {
    param([string]$StageOutputRoot)

    if (-not (Test-Path $StageOutputRoot)) {
        throw "Stage output root not found: $StageOutputRoot"
    }

    $latest = Get-ChildItem -Path $StageOutputRoot -Directory |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if (-not $latest) {
        throw "No run directory found under $StageOutputRoot"
    }

    return $latest.FullName
}

function Get-HighestEpochCheckpoint {
    param([string]$RunDirectory)

    $checkpoints = Get-ChildItem -Path $RunDirectory -File -Filter "checkpoint_*.pth" |
        Where-Object { $_.BaseName -match '^checkpoint_(\d+)$' } |
        Sort-Object { [int]($_.BaseName -replace 'checkpoint_', '') } -Descending

    if (-not $checkpoints) {
        throw "No numbered checkpoint files found under $RunDirectory"
    }

    return $checkpoints[0].FullName
}

function Get-HighestEpochPrediction {
    param([string]$ResultDirectory)

    if (-not (Test-Path $ResultDirectory)) {
        throw "Caption result directory not found: $ResultDirectory"
    }

    $predictions = Get-ChildItem -Path $ResultDirectory -File -Filter "val_epoch*.json" |
        Where-Object { $_.BaseName -match '^val_epoch(\d+)$' } |
        Sort-Object { [int]($_.BaseName -replace 'val_epoch', '') } -Descending

    if (-not $predictions) {
        throw "No val_epoch*.json files found under $ResultDirectory"
    }

    return $predictions[0].FullName
}

function Get-EpochPredictions {
    param([string]$ResultDirectory)

    if (-not (Test-Path $ResultDirectory)) {
        throw "Caption result directory not found: $ResultDirectory"
    }

    return Get-ChildItem -Path $ResultDirectory -File -Filter "val_epoch*.json" |
        Where-Object { $_.BaseName -match '^val_epoch(\d+)$' } |
        Sort-Object { [int]($_.BaseName -replace 'val_epoch', '') }
}

$Stage1Checkpoint = Resolve-OptionalPath $Stage1Checkpoint
$Stage2Checkpoint = Resolve-OptionalPath $Stage2Checkpoint
$Stage1ResumeCheckpoint = Resolve-OptionalPath $Stage1ResumeCheckpoint
$Stage2ResumeCheckpoint = Resolve-OptionalPath $Stage2ResumeCheckpoint
$CaptionResumeCheckpoint = Resolve-OptionalPath $CaptionResumeCheckpoint

if ($PrepareData) {
    & "$PSScriptRoot\prepare_student_100k_run.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "prepare_student_100k_run.ps1 failed with exit code $LASTEXITCODE"
    }
}

if (-not $Stage1Checkpoint) {
    $stage1Args = @{}
    if ($Stage1ResumeCheckpoint) {
        $stage1Args.ResumeCheckpoint = $Stage1ResumeCheckpoint
    }

    & "$PSScriptRoot\run_stage1_student_100k_long.ps1" @stage1Args
    if ($LASTEXITCODE -ne 0) {
        throw "run_stage1_student_100k_long.ps1 failed with exit code $LASTEXITCODE"
    }

    $stage1RunDir = Get-LatestRunDirectory (Join-Path $outputRoot "stage1_student_100k_long")
    $Stage1Checkpoint = Get-HighestEpochCheckpoint $stage1RunDir
}

if (-not $Stage2Checkpoint) {
    $stage2Args = @{
        Stage1Checkpoint = $Stage1Checkpoint
    }
    if ($Stage2ResumeCheckpoint) {
        $stage2Args.ResumeCheckpoint = $Stage2ResumeCheckpoint
    }

    & "$PSScriptRoot\run_stage2_student_100k_long.ps1" @stage2Args
    if ($LASTEXITCODE -ne 0) {
        throw "run_stage2_student_100k_long.ps1 failed with exit code $LASTEXITCODE"
    }

    $stage2RunDir = Get-LatestRunDirectory (Join-Path $outputRoot "stage2_student_100k_opt350m_long")
    $Stage2Checkpoint = Get-HighestEpochCheckpoint $stage2RunDir
}

$captionArgs = @{
    Stage2Checkpoint = $Stage2Checkpoint
}
if ($CaptionResumeCheckpoint) {
    $captionArgs.ResumeCheckpoint = $CaptionResumeCheckpoint
}

& "$PSScriptRoot\run_caption_student_100k_long.ps1" @captionArgs
if ($LASTEXITCODE -ne 0) {
    throw "run_caption_student_100k_long.ps1 failed with exit code $LASTEXITCODE"
}

$captionRunDir = Get-LatestRunDirectory (Join-Path $outputRoot "caption_student_100k_opt350m_long")
$captionResultDir = Join-Path $captionRunDir "result"

if ($EvaluateAllCaptionEpochs) {
    $bestEpoch = $null
    $bestCider = -1.0

    foreach ($prediction in Get-EpochPredictions $captionResultDir) {
        $epochSuffix = $prediction.BaseName -replace '^val_', ''
        $summaryPath = Join-Path $metricsRoot "caption_eval_summary_student_100k_long_${epochSuffix}.json"
        $examplesPath = Join-Path $metricsRoot "caption_eval_examples_student_100k_long_${epochSuffix}.json"

        & "$PSScriptRoot\run_caption_eval_student_100k.ps1" `
            -PredictionFile $prediction.FullName `
            -OutputPath $summaryPath `
            -ExamplesOutputPath $examplesPath

        if ($LASTEXITCODE -ne 0) {
            throw "run_caption_eval_student_100k.ps1 failed for $($prediction.FullName) with exit code $LASTEXITCODE"
        }

        $summary = Get-Content $summaryPath -Raw | ConvertFrom-Json
        $cider = [double]$summary.metrics.CIDEr
        if ($cider -gt $bestCider) {
            $bestCider = $cider
            $bestEpoch = $epochSuffix
        }
    }

    if ($bestEpoch) {
        Write-Host "Best evaluated caption epoch by CIDEr: $bestEpoch (CIDEr=$bestCider)"
    }
}
else {
    $latestPrediction = Get-HighestEpochPrediction $captionResultDir
    & "$PSScriptRoot\run_caption_eval_student_100k.ps1" -PredictionFile $latestPrediction
    if ($LASTEXITCODE -ne 0) {
        throw "run_caption_eval_student_100k.ps1 failed with exit code $LASTEXITCODE"
    }
}

Write-Host "Pipeline complete."
Write-Host "Stage 1 checkpoint: $Stage1Checkpoint"
Write-Host "Stage 2 checkpoint: $Stage2Checkpoint"
Write-Host "Caption run directory: $captionRunDir"
