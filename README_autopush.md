# Git Auto-Push Automation

This repository contains a simple, robust automation setup to automatically commit and push your local workspace changes to GitHub daily on Windows.

## Contents

- [git_autopush.py](file:///c:/Users/saira/Downloads/guna.p/git_autopush.py): The core Python script that checks for local changes, stages them, commits with a timestamped message, and pushes to your remote origin.
- [setup_daily_task.ps1](file:///c:/Users/saira/Downloads/guna.p/setup_daily_task.ps1): A PowerShell utility script that registers the Python script in Windows Task Scheduler to run automatically every day at 11:00 PM.
- `git_autopush.log`: The log file generated automatically by the script to track execution details and debug issues.

---

## Setup Instructions

### 1. Configure Git Authentication (Crucial)
Since the scheduled task runs in the background, Git must be able to push to GitHub without prompting you for a username or password.
- **Recommended (HTTPS)**: Run the following command to enable Windows Credential Manager:
  ```bash
  git config --global credential.helper manager
  ```
  Ensure you have pushed manually once to save your GitHub credentials in the Windows Credential Manager.
- **Alternative (SSH)**: Set up SSH keys and link them to your GitHub account.

### 2. Run the Daily Task Setup
Open PowerShell in this directory and execute:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\setup_daily_task.ps1
```
This registers a task named **`GunaP-Git-AutoPush`** in the Windows Task Scheduler.

---

## Usage

### Manual Execution
You can run the script manually at any time to stage, commit, and push your changes:
```bash
python git_autopush.py
```

### Checking Logs
Every execution (manual or scheduled) is logged to `git_autopush.log` in the same directory.
Example log output:
```text
[2026-06-05 18:15:00] === Git Auto-Push Start ===
[2026-06-05 18:15:01] Using git version 2.45.0.windows.1
[2026-06-05 18:15:01] Remote origin configured: https://github.com/username/repo.git
[2026-06-05 18:15:01] Changes detected:
 M README_autopush.md
 ?? new_file.txt
[2026-06-05 18:15:01] Staging changes...
[2026-06-05 18:15:02] Committing changes with message: 'Auto-commit: Daily update 2026-06-05 18:15:02'
[2026-06-05 18:15:02] Commit successful:
[main a1b2c3d] Auto-commit: Daily update 2026-06-05 18:15:02
 2 files changed, 5 insertions(+)
 create mode 100644 new_file.txt
[2026-06-05 18:15:02] Pushing changes to GitHub...
[2026-06-05 18:15:04] Push successful!
[2026-06-05 18:15:04] === Git Auto-Push Finished ===
```

### Changing Task Settings
To adjust the time or frequency:
1. Press the Windows key, search for **Task Scheduler**, and open it.
2. Select **Task Scheduler Library** from the left panel.
3. Locate **`GunaP-Git-AutoPush`**.
4. Double-click it to modify triggers, settings, or credentials.
