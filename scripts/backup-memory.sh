#!/bin/bash
# Auto-backup memory: local snapshot + git push
# Runs hourly via OpenClaw cron

set -e
WORKSPACE="/home/azureuser/.openclaw/workspace"
BACKUP_DIR="/home/azureuser/backups"
DATE=$(date +%Y-%m-%d_%H%M)

cd "$WORKSPACE"

# 1. Local backup (tarball)
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/workspace-$DATE.tar.gz" \
    --exclude='.git' \
    --exclude='logs' \
    --exclude='*.tar.gz' \
    .

# Keep only last 24 hourly backups
ls -t "$BACKUP_DIR"/workspace-*.tar.gz 2>/dev/null | tail -n +25 | xargs -r rm

echo "✓ Local backup: $BACKUP_DIR/workspace-$DATE.tar.gz"

# 2. Git push
git add -A

if git diff --cached --quiet; then
    echo "✓ Git: no changes"
else
    git commit -m "Auto-backup: $DATE"
    git push origin main 2>&1
    echo "✓ Git: pushed to GitHub"
fi

echo "Backup complete: $DATE"
