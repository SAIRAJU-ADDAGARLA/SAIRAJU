import os
import subprocess
import sys
from datetime import datetime

# Setup log file path relative to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "git_autopush.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def run_git_cmd(args):
    try:
        # Run command, capture stdout and stderr
        result = subprocess.run(
            ["git"] + args,
            cwd=SCRIPT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return True, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip(), e.stderr.strip()
    except FileNotFoundError:
        return False, "", "Git executable not found. Please ensure Git is installed and in your PATH."

def main():
    log("=== Git Auto-Push Start ===")
    
    # 1. Check if git is installed
    ok, stdout, stderr = run_git_cmd(["--version"])
    if not ok:
        log(f"CRITICAL: Git is not installed or not in PATH. Details: {stderr}")
        sys.exit(1)
    
    log(f"Using {stdout}")

    # 2. Check if directory is a git repository
    # If .git folder doesn't exist, initialize it
    git_dir = os.path.join(SCRIPT_DIR, ".git")
    if not os.path.exists(git_dir):
        log("No git repository detected. Initializing git...")
        ok, stdout, stderr = run_git_cmd(["init"])
        if not ok:
            log(f"ERROR: Failed to initialize git repository: {stderr}")
            sys.exit(1)
        log("Initialized empty Git repository.")
        
    # Check if remote origin is configured
    ok, stdout, stderr = run_git_cmd(["remote", "get-url", "origin"])
    if not ok:
        log("WARNING: No remote 'origin' configured. You must set a remote to push changes.")
        log("Example command to set origin: git remote add origin <your-github-repo-url>")
        has_remote = False
    else:
        log(f"Remote origin configured: {stdout}")
        has_remote = True

    # 3. Check for changes
    # git status --porcelain shows modified, untracked, deleted files in a clean machine-readable format
    ok, stdout, stderr = run_git_cmd(["status", "--porcelain"])
    if not ok:
        log(f"ERROR: Failed to check git status: {stderr}")
        sys.exit(1)
        
    if not stdout:
        log("No changes detected. Nothing to commit.")
        log("=== Git Auto-Push Finished ===")
        sys.exit(0)
        
    log("Changes detected:\n" + stdout)

    # 4. Staging changes
    log("Staging changes...")
    ok, stdout, stderr = run_git_cmd(["add", "-A"])
    if not ok:
        log(f"ERROR: Failed to stage changes: {stderr}")
        sys.exit(1)

    # 5. Committing changes
    commit_msg = f"Auto-commit: Daily update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    log(f"Committing changes with message: '{commit_msg}'")
    ok, stdout, stderr = run_git_cmd(["commit", "-m", commit_msg])
    if not ok:
        log(f"ERROR: Failed to commit changes: {stderr}")
        sys.exit(1)
    log(f"Commit successful:\n{stdout}")

    # 6. Pushing changes
    if not has_remote:
        log("Skipping push because remote origin is not configured. Local changes committed.")
        log("=== Git Auto-Push Finished ===")
        sys.exit(0)

    log("Pushing changes to GitHub...")
    # Get current branch
    ok, current_branch, stderr = run_git_cmd(["branch", "--show-current"])
    if not ok or not current_branch:
        current_branch = "main"
    
    # Try to push current branch to origin
    ok, stdout, stderr = run_git_cmd(["push", "origin", current_branch])
    if not ok:
        log(f"ERROR: Failed to push to remote: {stderr}")
        log("Please verify remote credentials (SSH keys or Git Credential Manager) and network connectivity.")
        sys.exit(1)
        
    log("Push successful!")
    if stdout:
        log(stdout)
    log("=== Git Auto-Push Finished ===")

if __name__ == "__main__":
    main()
