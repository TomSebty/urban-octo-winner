#!/usr/bin/env bash
# Add all repo issues whose title starts with "[Wave" to a GitHub Project v2 board.
# Usage:
#   export GH_PROJECT_NUMBER=1   # from: gh project list --owner TomSebty
#   bash scripts/add-issues-to-project.sh
set -euo pipefail
REPO="${GITHUB_REPOSITORY:-TomSebty/urban-octo-winner}"
OWNER="${GITHUB_PROJECT_OWNER:-TomSebty}"
PROJECT="${GH_PROJECT_NUMBER:?Set GH_PROJECT_NUMBER (gh project list --owner TomSebty)}"

echo "Linking BrandVoice backlog issues to project #$PROJECT for $OWNER ..."
gh project link "$PROJECT" --owner "$OWNER" --repo "$REPO" 2>/dev/null || true

mapfile -t URLS < <(gh issue list --repo "$REPO" --state open --limit 500 \
  --json url,title --jq '.[] | select(.title | startswith("[Wave")) | .url')

echo "Found ${#URLS[@]} backlog issues."
for url in "${URLS[@]}"; do
  gh project item-add "$PROJECT" --owner "$OWNER" --url "$url" || echo "Skip/fail: $url"
done
echo "Done. Open: gh project view $PROJECT --owner $OWNER --web"