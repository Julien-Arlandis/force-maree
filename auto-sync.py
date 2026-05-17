#!/usr/bin/env python3
import os
import subprocess
import time

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
POLL_INTERVAL = 2.0


def has_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def run(cmd):
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True)


def auto_commit_and_push():
    run(["git", "add", "-A"])
    message = f"Auto commit {time.strftime('%Y-%m-%d %H:%M:%S')}"
    result = run(["git", "commit", "-m", message])
    if result.returncode != 0:
        return False
    run(["git", "push", "--quiet", "origin", "HEAD"])
    return True


def main():
    print("Auto-sync démarré. Surveillance des modifications...\n")
    while True:
        try:
            if has_changes():
                print("Modifications détectées. Commit + push en cours...")
                auto_commit_and_push()
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("Auto-sync arrêté.")
            break


if __name__ == "__main__":
    main()
