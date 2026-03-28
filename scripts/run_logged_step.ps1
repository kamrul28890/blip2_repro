param(
    [Parameter(Mandatory = $true)]
    [string]$Stage,

    [Parameter(Mandatory = $true)]
    [string]$Step,

    [Parameter(Mandatory = $true)]
    [string]$WorkingDirectory,

    [Parameter(Mandatory = $true)]
    [string]$Command
)

$ErrorActionPreference = "Continue"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedWorkingDirectory = (Resolve-Path $WorkingDirectory).Path
$safeStage = ($Stage -replace '[^A-Za-z0-9._-]', '_')
$safeStep = ($Step -replace '[^A-Za-z0-9._-]', '_')
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$logDir = Join-Path $repoRoot "logs\blip2\$safeStage"
New-Item -ItemType Directory -Force $logDir | Out-Null

$logPath = Join-Path $logDir "${timestamp}_${safeStep}.log"
$metricsPath = Join-Path $repoRoot "metrics\blip2\install_attempts.jsonl"

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$exitCode = 0

$machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathSegments = @()

foreach ($segment in @($machinePath, $userPath, $env:Path) -split ';') {
    if (-not [string]::IsNullOrWhiteSpace($segment) -and ($pathSegments -notcontains $segment)) {
        $pathSegments += $segment
    }
}

$env:Path = ($pathSegments -join ';')

Push-Location $resolvedWorkingDirectory
try {
    @(
        "timestamp=$timestamp"
        "stage=$Stage"
        "step=$Step"
        "working_directory=$resolvedWorkingDirectory"
        "command=$Command"
        ""
    ) | Tee-Object -FilePath $logPath -Append | Out-Null

    & cmd.exe /d /s /c $Command 2>&1 |
        Tee-Object -FilePath $logPath -Append

    if ($null -ne $LASTEXITCODE) {
        $exitCode = [int]$LASTEXITCODE
    }
}
catch {
    $_ | Tee-Object -FilePath $logPath -Append
    $exitCode = 1
}
finally {
    Pop-Location
    $stopwatch.Stop()
}

$result = if ($exitCode -eq 0) { "success" } else { "failure" }
$entry = [ordered]@{
    timestamp = (Get-Date).ToString("o")
    stage = $Stage
    step = $Step
    working_directory = $resolvedWorkingDirectory
    command = $Command
    exit_code = $exitCode
    duration_seconds = [math]::Round($stopwatch.Elapsed.TotalSeconds, 3)
    result = $result
    log_path = $logPath
}

$entry | ConvertTo-Json -Compress | Add-Content -Path $metricsPath

exit $exitCode
