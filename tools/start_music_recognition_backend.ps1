param(
    [switch]$Install,
    [switch]$Background
)

$ErrorActionPreference = "Stop"

$ToolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ServiceDir = Join-Path $ToolsDir "media\ncm-recognize-api"
$PackageJson = Join-Path $ServiceDir "package.json"
$NodeModules = Join-Path $ServiceDir "node_modules"

if (-not (Test-Path -LiteralPath $PackageJson)) {
    throw "ncm-recognize-api is not installed. Clone it into $ServiceDir first."
}

if ($Install -or -not (Test-Path -LiteralPath $NodeModules)) {
    Push-Location $ServiceDir
    try {
        npm install
    }
    finally {
        Pop-Location
    }
}

if ($Background) {
    Start-Process -FilePath "node" -ArgumentList "server.js" -WorkingDirectory $ServiceDir -WindowStyle Hidden
    Write-Host "ncm-recognize-api started in background at http://127.0.0.1:12400"
    return
}

Write-Host "Starting ncm-recognize-api at http://127.0.0.1:12400"
Push-Location $ServiceDir
try {
    node server.js
}
finally {
    Pop-Location
}
