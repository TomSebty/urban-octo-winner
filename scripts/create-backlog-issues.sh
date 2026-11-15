#!/usr/bin/env bash
# Create all BrandVoice backlog issues via GitHub CLI
set -euo pipefail
REPO="${GITHUB_REPOSITORY:-TomSebty/urban-octo-winner}"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo 'Creating labels (ignore errors if they exist)...'
for lb in wave-0-foundation wave-1-core wave-2-mvp wave-3-polish \
  layer-db layer-backend layer-ai layer-frontend layer-qa layer-devops bonus; do
  gh label create "$lb" --repo "$REPO" --force 2>/dev/null || true
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON="$SCRIPT_DIR/backlog_issues.json"
if ! command -v jq &>/dev/null; then
  echo "jq is required. Install jq or use: python3 scripts/generate_backlog.py"
  exit 1
fi
COUNT=$(jq length "$JSON")
echo "Creating $COUNT issues in $REPO ..."
for i in $(seq 0 $((COUNT - 1))); do
  TITLE=$(jq -r ".[$i].title" "$JSON")
  BODY=$(jq -r ".[$i].body" "$JSON")
  LABELS=$(jq -r ".[$i].labels | join(",")" "$JSON")
  gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY" --label "$LABELS"
  echo "Created: $TITLE"
done
echo "Done. Open GitHub Projects and add these issues to the board."
