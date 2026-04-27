param(
    [string]$TargetCodexHome = "C:\Users\tiaro\.codex"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$snapshotRoot = Join-Path $repoRoot "snapshot\codex-home"

if (-not (Test-Path -LiteralPath $snapshotRoot)) {
    throw "Snapshot nao encontrado em $snapshotRoot"
}

if (-not (Test-Path -LiteralPath $TargetCodexHome)) {
    New-Item -ItemType Directory -Path $TargetCodexHome -Force | Out-Null
}

$items = Get-ChildItem -LiteralPath $snapshotRoot -Recurse -Force

foreach ($item in $items) {
    $relativePath = $item.FullName.Substring($snapshotRoot.Length).TrimStart('\')

    if ([string]::IsNullOrWhiteSpace($relativePath)) {
        continue
    }

    $targetPath = Join-Path $TargetCodexHome $relativePath

    if ($item.PSIsContainer) {
        if (-not (Test-Path -LiteralPath $targetPath)) {
            New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
        }
        continue
    }

    $targetParent = Split-Path -Parent $targetPath
    if (-not (Test-Path -LiteralPath $targetParent)) {
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
    }

    Copy-Item -LiteralPath $item.FullName -Destination $targetPath -Force
}

Write-Host "Restore concluido em $TargetCodexHome"
Write-Host "Autenticacoes e segredos devem ser refeitos manualmente."
