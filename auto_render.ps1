# Pull the daily batch from GitHub, render MP4s for new scripts only, write caption files.
# Run by hand:   powershell -ExecutionPolicy Bypass -File auto_render.ps1
# Or schedule it (see README "Automatic rendering").
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$log = Join-Path $PSScriptRoot "work\auto_render.log"
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
Start-Transcript -Path $log -Append | Out-Null
try {
    Write-Host "=== $(Get-Date -Format s) ==="
    git pull --ff-only
    python render.py --new
    python publish/captions.py
    Write-Host "Done. MP4s and captions are in out/"
} finally {
    Stop-Transcript | Out-Null
}
