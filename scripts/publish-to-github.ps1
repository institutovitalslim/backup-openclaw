param(
    [string]$RemoteUrl = "https://github.com/institutovitalslim/backup-openclaw.git",
    [string]$Branch = "main",
    [string]$CommitMessage = "Update OpenClaw workplace backup"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git nao esta instalado neste ambiente."
}

$repoRoot = Split-Path -Parent $PSScriptRoot

Push-Location $repoRoot
try {
    $insideGitRepo = $false

    try {
        git rev-parse --is-inside-work-tree | Out-Null
        $insideGitRepo = $true
    } catch {
        $insideGitRepo = $false
    }

    if (-not $insideGitRepo) {
        git init | Out-Null
    }

    $remoteExists = $false
    try {
        git remote get-url origin | Out-Null
        $remoteExists = $true
    } catch {
        $remoteExists = $false
    }

    if (-not $remoteExists) {
        git remote add origin $RemoteUrl
    }

    git checkout -B $Branch | Out-Null
    git add .
    git commit -m $CommitMessage
    git push -u origin $Branch
} finally {
    Pop-Location
}
