#!/bin/bash
set -euo pipefail

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_DIR="${PAPERVAULT_DIR:-$HOME/PaperVault}"
PLIST_NAME="com.papertracker.daily"

echo "=== Paper Tracker Installer ==="
echo ""

# Check prerequisites
echo "[1/5] Checking prerequisites..."

if ! command -v claude &>/dev/null; then
  echo "  ERROR: Claude Code CLI not found. Install from https://docs.anthropic.com/en/docs/claude-code"
  exit 1
fi
echo "  ✓ Claude Code CLI"

if ! command -v python3 &>/dev/null; then
  echo "  ERROR: Python 3 not found."
  exit 1
fi
echo "  ✓ Python 3 ($(python3 --version 2>&1 | cut -d' ' -f2))"

# Create vault
echo ""
echo "[2/5] Creating Obsidian vault at $VAULT_DIR..."
mkdir -p "$VAULT_DIR"/{Daily,Papers,assets/images,logs}
echo "  ✓ Vault directories created"

# Copy skills to .claude/skills for runtime
echo ""
echo "[3/5] Setting up Claude Code skills..."
mkdir -p "$PROJ_DIR/.claude/skills"
for skill_dir in "$PROJ_DIR"/skills/*/; do
  skill_name="$(basename "$skill_dir")"
  mkdir -p "$PROJ_DIR/.claude/skills/$skill_name"
  cp "$skill_dir"skill.md "$PROJ_DIR/.claude/skills/$skill_name/skill.md"
done
echo "  ✓ Skills copied to .claude/skills/"

# Set up launchd (macOS) or cron (Linux)
echo ""
echo "[4/5] Setting up daily schedule (8:00 AM)..."

if [[ "$(uname)" == "Darwin" ]]; then
  PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

  # Unload existing if present
  launchctl unload "$PLIST_PATH" 2>/dev/null || true

  cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PROJ_DIR/run_daily.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$VAULT_DIR/logs/launchd-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$VAULT_DIR/logs/launchd-stderr.log</string>
</dict>
</plist>
PLIST

  launchctl load "$PLIST_PATH"
  echo "  ✓ launchd agent installed and loaded"
else
  # Linux: add cron job
  CRON_LINE="0 8 * * * $PROJ_DIR/run_daily.sh"
  (crontab -l 2>/dev/null | grep -v "run_daily.sh"; echo "$CRON_LINE") | crontab -
  echo "  ✓ cron job added"
fi

# Run tests
echo ""
echo "[5/5] Running tests..."
cd "$PROJ_DIR"
if python3 -m pytest tests/ -v 2>&1; then
  echo "  ✓ All tests passed"
else
  echo "  WARNING: Some tests failed. The pipeline may still work."
fi

echo ""
echo "=== Installation complete ==="
echo ""
echo "  Vault:    $VAULT_DIR (open this in Obsidian)"
echo "  Schedule: Daily at 8:00 AM"
echo "  Manual:   $PROJ_DIR/run_daily.sh"
echo "  Logs:     $VAULT_DIR/logs/"
echo ""
echo "To uninstall:"
if [[ "$(uname)" == "Darwin" ]]; then
  echo "  launchctl unload ~/Library/LaunchAgents/$PLIST_NAME.plist"
  echo "  rm ~/Library/LaunchAgents/$PLIST_NAME.plist"
else
  echo "  crontab -e  # remove the paper-tracker line"
fi
