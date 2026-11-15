#!/usr/bin/env bash
# Create all BrandVoice backlog issues via GitHub CLI
set -euo pipefail
REPO="${GITHUB_REPOSITORY:-TomSebty/urban-octo-winner}"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo 'Creating labels (requires repo admin token; skips if unavailable)...'
LABELS_OK=1
for lb in wave-0-foundation wave-1-core wave-2-mvp wave-3-polish \
  layer-db layer-backend layer-ai layer-frontend layer-qa layer-devops bonus; do
  gh label create "$lb" --repo "$REPO" --force 2>/dev/null || LABELS_OK=0
done
if [[ "$LABELS_OK" == 1 ]]; then
  echo "Labels ready."
else
  echo "Label create skipped or failed; issues will include suggested labels in the body."
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON="$SCRIPT_DIR/backlog_issues.json"
if ! command -v jq &>/dev/null; then
  echo "jq is required. Install jq or use: python3 scripts/generate_backlog.py"
  exit 1
fi
COUNT=$(jq length "$JSON")
EXISTING=$(gh issue list --repo "$REPO" --state open --limit 500 \
  --json title --jq '[.[] | select(.title | startswith("[Wave"))] | length')
if [[ "$EXISTING" -ge "$COUNT" ]]; then
  echo "Already have $EXISTING/[Wave] issues (expected $COUNT). Skipping create."
  echo "To add to a board: GH_PROJECT_NUMBER=<n> bash scripts/add-issues-to-project.sh"
  exit 0
fi
echo "Creating $COUNT issues in $REPO (${EXISTING} already exist) ..."
for i in $(seq 0 $((COUNT - 1))); do
  TITLE=$(jq -r --argjson i "$i" '.[$i].title' "$JSON")
  if [[ "$LABELS_OK" == 1 ]]; then
    BODY=$(jq -r --argjson i "$i" '.[$i].body' "$JSON")
    LABELS=$(jq -r --argjson i "$i" '.[$i].labels | join(",")' "$JSON")
    gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY" --label "$LABELS"
  else
    BODY_FILE=$(mktemp)
    jq -r --argjson i "$i" \
      '.[$i].body + "\n\n## Suggested labels\n" + (.[$i].labels | map("`" + . + "`") | join(", "))' \
      "$JSON" >"$BODY_FILE"
    gh issue create --repo "$REPO" --title "$TITLE" --body-file "$BODY_FILE"
    rm -f "$BODY_FILE"
  fi
  echo "Created: $TITLE"
done
echo "Done. Open GitHub Projects and add these issues to the board."
