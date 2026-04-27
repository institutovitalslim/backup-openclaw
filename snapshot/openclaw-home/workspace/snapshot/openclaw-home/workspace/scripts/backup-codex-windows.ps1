param(
    [string]$CodexHome = "C:\Users\tiaro\.codex"
)

$ErrorActionPreference = "Stop"

function Reset-Directory {
    param([string]$Path)

    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }

    New-Item -ItemType Directory -Path $Path | Out-Null
}

function Should-ExcludePath {
    param([string]$RelativePath)

    $normalized = $RelativePath.Replace("\", "/")
    $topLevel = ($normalized -split "/")[0]

    return $topLevel -in @(
        ".sandbox",
        ".sandbox-bin",
        ".sandbox-secrets",
        "sessions",
        "sqlite",
        "tmp",
        "vendor_imports"
    )
}

function Should-ExcludeFile {
    param([string]$Name)

    return $Name -in @(
        "auth.json",
        "cap_sid",
        "models_cache.json",
        "session_index.jsonl",
        ".codex-global-state.json"
    )
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$snapshotRoot = Join-Path $repoRoot "snapshot\codex-home"
$metadataRoot = Join-Path $repoRoot "snapshot\metadata"

if (-not (Test-Path -LiteralPath $CodexHome)) {
    throw "Diretorio CODEX_HOME nao encontrado: $CodexHome"
}

Reset-Directory -Path $snapshotRoot
Reset-Directory -Path $metadataRoot

$sourceItems = Get-ChildItem -LiteralPath $CodexHome -Recurse -Force -ErrorAction SilentlyContinue

foreach ($item in $sourceItems) {
    $relativePath = $item.FullName.Substring($CodexHome.Length).TrimStart('\')

    if ([string]::IsNullOrWhiteSpace($relativePath)) {
        continue
    }

    if (Should-ExcludePath -RelativePath $relativePath) {
        continue
    }

    if ($item.PSIsContainer) {
        $targetDir = Join-Path $snapshotRoot $relativePath
        if (-not (Test-Path -LiteralPath $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        continue
    }

    if (Should-ExcludeFile -Name $item.Name) {
        continue
    }

    if ($item.Name -like "logs_*.sqlite*" -or $item.Name -like "state_*.sqlite*") {
        continue
    }

    $targetFile = Join-Path $snapshotRoot $relativePath
    $targetParent = Split-Path -Parent $targetFile

    if (-not (Test-Path -LiteralPath $targetParent)) {
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
    }

    Copy-Item -LiteralPath $item.FullName -Destination $targetFile -Force
}

$inventory = Get-ChildItem -LiteralPath $snapshotRoot -Recurse -Force |
    Select-Object FullName, Name, Length, LastWriteTimeUtc

$inventory | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $metadataRoot "inventory.json") -Encoding UTF8
$inventory | Format-Table -AutoSize | Out-String -Width 220 | Set-Content -LiteralPath (Join-Path $metadataRoot "inventory.txt") -Encoding UTF8

$summary = [pscustomobject]@{
    generated_at_utc = [DateTime]::UtcNow.ToString("o")
    codex_home = $CodexHome
    snapshot_root = $snapshotRoot
    restored_with = ".\scripts\restore-codex-windows.ps1"
}

$summary | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $metadataRoot "summary.json") -Encoding UTF8

Write-Host "Backup concluido em $snapshotRoot"
