#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> 1. Secret, PII & excluded-metadata hygiene check"
if grep -rniE '(AIza[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z]{20,}|gho_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z]{20,}|JForce|Ümit|Ayşe|16\+?\s*Years?|16-year|steerf[0o]cus)' README.md PROJECTS.md docs/index.html; then
  echo "ERROR: Potential sensitive or excluded data detected. Aborting."
  exit 1
fi

echo "==> 2. Verify all public COPUR GitHub links resolve"
PUBLIC_REPOS="$(gh repo list COPUR --limit 200 --visibility public --json name -q '.[].name')"
URLS="$(grep -rhoE 'https://github\.com/COPUR/[A-Za-z0-9_.-]+' README.md PROJECTS.md docs/index.html | sort -u)"

for url in $URLS; do
  repo="${url#https://github.com/COPUR/}"
  if ! printf '%s\n' "$PUBLIC_REPOS" | grep -qx "$repo"; then
    echo "ERROR: Link points to non-public or missing repo: $url"
    exit 1
  fi
done
echo "All $(printf '%s\n' "$URLS" | wc -l | tr -d ' ') repository links verified PUBLIC."

echo "==> 3. Commit and push changes if any"
git add README.md PROJECTS.md docs/index.html scripts/publish-portfolio.sh
if ! git diff --cached --quiet; then
  git commit -m "chore: update enterprise portfolio, Agentic AI suite, and remove experience years"
  git push origin main
else
  echo "No new changes to commit."
fi

echo "==> 4. Ensure GitHub Pages is enabled (main /docs)"
if gh api repos/COPUR/COPUR/pages >/dev/null 2>&1; then
  echo "GitHub Pages already configured."
else
  gh api --method POST repos/COPUR/COPUR/pages \
    -f "build_type=legacy" \
    -F "source[branch]=main" \
    -F "source[path]=/docs" >/dev/null
  echo "GitHub Pages enabled on main:/docs."
fi

echo "==> Done! Profile: https://github.com/COPUR | Pages: https://copur.github.io/COPUR/"
