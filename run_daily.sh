#!/bin/bash
# run_daily.sh - Trigger daily paper pipeline via Claude Code
set -euo pipefail

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="$HOME/PaperVault"
LOG_DIR="$VAULT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

echo "=== Daily Paper Run: $(date) ===" >> "$LOG_FILE"

# Load all skill files into the system prompt
SKILLS=""
for f in "$PROJ_DIR"/.claude/skills/*/skill.md; do
  SKILLS="$SKILLS
$(cat "$f")
---
"
done

cd "$PROJ_DIR"

claude -p "Run the daily paper pipeline now. Follow the daily-paper skill instructions exactly step by step." \
  --permission-mode bypassPermissions \
  --append-system-prompt "$SKILLS" \
  --add-dir "$PROJ_DIR" \
  --add-dir "$VAULT_DIR" \
  >> "$LOG_FILE" 2>&1

echo "=== Completed: $(date) ===" >> "$LOG_FILE"
