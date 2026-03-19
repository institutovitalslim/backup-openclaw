param(
    [string]$TaskName = "OpenClawDailyBackup",
    [string]$Time = "03:00"
)

$ErrorActionPreference = "Stop"

$backupScript = Join-Path $PSScriptRoot "backup-codex-windows.ps1"
$powershellExe = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"

if (-not (Test-Path -LiteralPath $backupScript)) {
    throw "Script de backup nao encontrado em $backupScript"
}

$action = New-ScheduledTaskAction -Execute $powershellExe -Argument "-ExecutionPolicy Bypass -File `"$backupScript`""
$trigger = New-ScheduledTaskTrigger -Daily -At ([DateTime]::ParseExact($Time, "HH:mm", $null))
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue | Out-Null
} catch {
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings | Out-Null

Write-Host "Tarefa registrada: $TaskName as $Time"
