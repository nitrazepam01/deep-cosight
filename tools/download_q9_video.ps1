param(
    [string]$Url = "https://www.youtube.com/watch?v=zNM7OtnJFvU",
    [string]$OutputDir = "task9",
    [int]$Height = 360,
    [switch]$Clip,
    [string]$Section = "*00:32:12-00:33:05"
)

$ErrorActionPreference = "Stop"

function Get-CondaBase {
    try {
        $base = (& conda info --base 2>$null | Select-Object -Last 1).Trim()
        if ($base -and (Test-Path $base)) {
            return $base
        }
    } catch {
        # Fall through to common Windows location.
    }

    $fallback = "D:\Miniconda"
    if (Test-Path $fallback) {
        return $fallback
    }

    throw "Could not find conda base. Install dependencies with: conda install -n base -c conda-forge ffmpeg yt-dlp"
}

function Get-YtDlpCommand {
    param([string]$CondaBase)

    $ytDlpExe = Join-Path $CondaBase "Scripts\yt-dlp.exe"
    if (Test-Path $ytDlpExe) {
        return @($ytDlpExe)
    }

    $pythonExe = Join-Path $CondaBase "python.exe"
    $ytDlpScript = Join-Path $CondaBase "Scripts\yt-dlp-script.py"
    if ((Test-Path $pythonExe) -and (Test-Path $ytDlpScript)) {
        return @($pythonExe, $ytDlpScript)
    }

    if (Test-Path $pythonExe) {
        & $pythonExe -c "import yt_dlp" 2>$null
        if ($LASTEXITCODE -eq 0) {
            return @($pythonExe, "-m", "yt_dlp")
        }
    }

    throw "yt-dlp was not found in conda base. Install it with: conda install -n base -c conda-forge yt-dlp"
}

function Assert-Ffmpeg {
    param([string]$CondaBase)

    $ffmpeg = Join-Path $CondaBase "Library\bin\ffmpeg.exe"
    $ffprobe = Join-Path $CondaBase "Library\bin\ffprobe.exe"
    if ((Test-Path $ffmpeg) -and (Test-Path $ffprobe)) {
        return
    }

    throw "ffmpeg/ffprobe were not found in conda base. Install them with: conda install -n base -c conda-forge ffmpeg"
}

$condaBase = Get-CondaBase
$ytDlp = Get-YtDlpCommand -CondaBase $condaBase
Assert-Ffmpeg -CondaBase $condaBase

$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$repoRoot = (Resolve-Path (Join-Path $scriptRoot "..")).Path
$resolvedOutputDir = if ([System.IO.Path]::IsPathRooted($OutputDir)) {
    $OutputDir
} else {
    Join-Path $repoRoot $OutputDir
}

New-Item -ItemType Directory -Force -Path $resolvedOutputDir | Out-Null

$env:PATH = @(
    (Join-Path $condaBase "Library\bin"),
    (Join-Path $condaBase "Scripts"),
    $condaBase,
    $env:PATH
) -join ";"

$format = "bestvideo[height<=$Height]+bestaudio/best[height<=$Height]/best"
$outputName = if ($Clip) { "q9_level2000_clip.%(ext)s" } else { "q9_full_video.%(ext)s" }
$outputTemplate = Join-Path $resolvedOutputDir $outputName

$argsList = @(
    "--no-playlist",
    "--write-auto-subs",
    "--write-subs",
    "--sub-langs", "en.*",
    "--sub-format", "vtt",
    "-f", $format,
    "--merge-output-format", "mp4",
    "-o", $outputTemplate
)

if ($Clip) {
    $argsList += @("--download-sections", $Section)
}

$argsList += $Url

Write-Host "Conda base: $condaBase"
Write-Host "Repo root:   $repoRoot"
Write-Host "Output dir:  $resolvedOutputDir"
Write-Host "Mode:        $(if ($Clip) { "clip $Section" } else { "full video" })"
Write-Host "Command:     $($ytDlp -join ' ') $($argsList -join ' ')"

$invokeArgs = @()
if ($ytDlp.Count -gt 1) {
    $invokeArgs += $ytDlp[1..($ytDlp.Count - 1)]
}
$invokeArgs += $argsList

& $ytDlp[0] @invokeArgs
if ($LASTEXITCODE -ne 0) {
    throw "yt-dlp failed with exit code $LASTEXITCODE"
}

Write-Host "Done."
