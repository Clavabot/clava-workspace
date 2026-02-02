#!/bin/bash
# Auto-backup memory to git
# Run via cron or manually

cd /home/azureuser/.openclaw/workspace

# Add all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Commit with timestamp
DATE=$(date +%Y-%m-%d_%H:%M)
git commit -m "Auto-backup: $DATE"

# Push to remote
git push origin main 2>&1 || echo "Push failed - will retry later"

echo "Backup complete: $DATE"
