param(
    [string]$LavisRoot = (Resolve-Path "$PSScriptRoot\..\..\repo_study\LAVIS").Path
)

$annDir = Join-Path $LavisRoot "cache\coco\annotations"
New-Item -ItemType Directory -Force $annDir | Out-Null

$files = @(
    @{
        Name = "coco_karpathy_train.json"
        Url = "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_train.json"
    },
    @{
        Name = "coco_karpathy_val.json"
        Url = "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_val.json"
    },
    @{
        Name = "coco_karpathy_test.json"
        Url = "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_test.json"
    }
)

foreach ($file in $files) {
    $target = Join-Path $annDir $file.Name
    if (Test-Path $target) {
        Write-Host "Using existing $target"
        continue
    }

    Invoke-WebRequest -Uri $file.Url -OutFile $target
    Write-Host "Downloaded $target"
}
