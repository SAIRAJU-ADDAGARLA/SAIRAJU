# setup_daily_task.ps1
# This script registers git_autopush.py with Windows Task Scheduler to run daily.

$ScriptName = "git_autopush.py"
$ScriptPath = Join-Path $PSScriptRoot $ScriptName
$TaskName = "GunaP-Git-AutoPush"

# Verify that python is installed and get its absolute path
$PythonPath = Get-Command python.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source

if (-not $PythonPath) {
    Write-Warning "Python was not found in your system PATH using Get-Command. We will fallback to using 'python', but this may fail in Task Scheduler if the environment variables are not loaded."
    $PythonPath = "python"
} else {
    Write-Host "Found Python at: $PythonPath"
}

Write-Host "Registering task '$TaskName' to run daily at 11:00 PM..."
Write-Host "Script location: $ScriptPath"

# Define the action to execute python with the path of the script
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument """$ScriptPath""" -WorkingDirectory $PSScriptRoot

# Define trigger: daily at 11:00 PM
$Trigger = New-ScheduledTaskTrigger -Daily -At 11:00PM

# Define settings (allow starting on battery, run as soon as possible if missed, etc.)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task for the current user
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Runs git_autopush.py daily to commit and push changes to GitHub" -Force
    Write-Host "Success! The scheduled task '$TaskName' has been registered."
    Write-Host "You can find and manage it in Windows Task Scheduler."
} catch {
    Write-Error "Failed to register scheduled task: $_"
    Write-Host "Please ensure you run this script in a PowerShell window with appropriate permissions."
}
