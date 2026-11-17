#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DRY_RUN=false
SKIP_VERIFY_GITHUB=false
OFFLINE=false
KEEP_TMP=false
COMMIT_MSG=""
STAGE_DIR=""

usage() {
  cat <<'EOF'
Usage: scripts/publish-portfolio.sh [OPTIONS]

Options:
  --dry-run               Build, test, and stage clean /tmp clones without committing or pushing
  -m, --message <msg>     Custom git commit message (default: timestamped UTC chore message)
  --skip-verify-github    Skip live GitHub repository visibility verification (--offline in compiler)
  --offline               Offline mode: skip GitHub verification and remote git/Pages calls (requires --dry-run)
  --keep-tmp              Preserve temporary /tmp staging directory after exit
  -h, --help              Show this help message

Exit codes:
  0  Success
  1  Schema, invariant (VAL-01..VAL-09), hygiene policy, or unit-test failure
  2  Deterministic --check parity drift detected
  3  Live GitHub visibility mismatch detected
  4  Operational, CLI, authentication, git, or GitHub Pages error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -m|--message)
      if [[ -z "${2:-}" ]]; then
        echo "ERROR: $1 requires a non-empty commit message." >&2
        exit 4
      fi
      COMMIT_MSG="$2"
      shift 2
      ;;
    --skip-verify-github)
      SKIP_VERIFY_GITHUB=true
      shift
      ;;
    --offline)
      OFFLINE=true
      SKIP_VERIFY_GITHUB=true
      shift
      ;;
    --keep-tmp)
      KEEP_TMP=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 4
      ;;
  esac
done

if [[ "$OFFLINE" == true && "$DRY_RUN" == false ]]; then
  echo "ERROR: --offline skips all network git/API calls and requires --dry-run (or use --skip-verify-github)." >&2
  exit 4
fi

if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="chore(portfolio): publish SSOT catalog & dual-artifact outputs ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
fi

cleanup() {
  if [[ -n "$STAGE_DIR" && -d "$STAGE_DIR" ]]; then
    if [[ "$KEEP_TMP" == true ]]; then
      echo "==> Preserving staging directory: $STAGE_DIR"
    else
      rm -rf "$STAGE_DIR"
    fi
  fi
}
trap cleanup EXIT

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: Required command not found: $1" >&2
    exit 4
  fi
}

require_cmd python3
require_cmd git
require_cmd rsync

if [[ "$OFFLINE" == false ]]; then
  require_cmd gh
  require_cmd curl
  if ! gh auth status >/dev/null 2>&1; then
    echo "ERROR: GitHub CLI is not authenticated. Run 'gh auth login' first." >&2
    exit 4
  fi
fi

VERIFY_FLAGS=()
if [[ "$SKIP_VERIFY_GITHUB" == true ]]; then
  VERIFY_FLAGS+=(--offline)
else
  VERIFY_FLAGS+=(--verify-github --strict-verification)
fi

run_compiler() {
  local mode="$1"
  set +e
  python3 scripts/build-portfolio.py "$mode" "${VERIFY_FLAGS[@]}" --strict-hygiene
  local rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    echo "ERROR: Compiler failed in $mode mode (exit code $rc)." >&2
    exit "$rc"
  fi
}

echo "==> 1. Build portfolio outputs from SSOT (single-source HygieneScanner active)"
run_compiler --build

echo "==> 2. Verify byte-exact determinism (--check)"
run_compiler --check

echo "==> 3. Run unit, invariant, and architecture tests"
if ! python3 -m unittest discover -s tests -p "test_*.py" -v; then
  echo "ERROR: Test suite failed." >&2
  exit 1
fi

if [[ "$OFFLINE" == true ]]; then
  echo "==> [OFFLINE --dry-run] Local build, check, and tests passed. Remote staging skipped."
  exit 0
fi

echo "==> 4. Stage iCloud-safe /tmp dual-repo clones"
STAGE_DIR="$(mktemp -d /tmp/copur-publish.XXXXXX)"
PROFILE_DIR="$STAGE_DIR/COPUR"
PAGES_DIR="$STAGE_DIR/COPUR.github.io"

gh auth setup-git >/dev/null 2>&1 || true
git clone --depth 1 --branch main https://github.com/COPUR/COPUR.git "$PROFILE_DIR"
git clone --depth 1 --branch main https://github.com/COPUR/COPUR.github.io.git "$PAGES_DIR"

RSYNC_EXCLUDES=(
  --exclude '.git'
  --exclude '.DS_Store'
  --exclude '__pycache__'
  --exclude '*.py[cod]'
  --exclude '.pytest_cache'
  --exclude '.env'
  --exclude '.env.*'
  --exclude '*.log'
  --exclude '*.bak'
)

for dir in catalog scripts tests .github briefs docs; do
  mkdir -p "$PROFILE_DIR/$dir"
  rsync -a --delete "${RSYNC_EXCLUDES[@]}" "$ROOT_DIR/$dir/" "$PROFILE_DIR/$dir/"
done
cp -f "$ROOT_DIR/README.md" "$PROFILE_DIR/README.md"
cp -f "$ROOT_DIR/PROJECTS.md" "$PROFILE_DIR/PROJECTS.md"
cp -f "$ROOT_DIR/.gitignore" "$PROFILE_DIR/.gitignore"
if [[ -f "$ROOT_DIR/BACKLOG.md" ]]; then
  cp -f "$ROOT_DIR/BACKLOG.md" "$PROFILE_DIR/BACKLOG.md"
fi
if [[ -f "$ROOT_DIR/TOGAF_ADM_PLAN.md" ]]; then
  cp -f "$ROOT_DIR/TOGAF_ADM_PLAN.md" "$PROFILE_DIR/TOGAF_ADM_PLAN.md"
fi

# Mirror static web artifacts into COPUR/COPUR.github.io root /
cp -f "$ROOT_DIR/docs/index.html" "$PAGES_DIR/index.html"
cp -f "$ROOT_DIR/docs/.nojekyll" "$PAGES_DIR/.nojekyll"
cp -f "$ROOT_DIR/.gitignore" "$PAGES_DIR/.gitignore"
mkdir -p "$PAGES_DIR/briefs"
rsync -a --delete --exclude '.DS_Store' "$ROOT_DIR/docs/briefs/" "$PAGES_DIR/briefs/"

# Pre-commit sanity guard for Pages mirror
if [[ ! -s "$PAGES_DIR/index.html" || ! -f "$PAGES_DIR/.nojekyll" ]]; then
  echo "ERROR: Missing required root Pages artifacts in $PAGES_DIR." >&2
  exit 4
fi
if ! find "$PAGES_DIR/briefs" -maxdepth 1 -name '*.html' -print -quit | grep -q .; then
  echo "ERROR: No HTML proof briefs found in $PAGES_DIR/briefs/." >&2
  exit 4
fi

sync_repo() {
  local repo_dir="$1"
  local repo_label="$2"

  git -C "$repo_dir" add -A
  if git -C "$repo_dir" diff --cached --quiet; then
    echo "[$repo_label] No changes to commit."
    return 0
  fi

  echo "[$repo_label] Staged diff summary:"
  git -C "$repo_dir" diff --cached --stat

  if [[ "$DRY_RUN" == true ]]; then
    echo "[DRY-RUN][$repo_label] Skipping commit and push. Message would be: $COMMIT_MSG"
    return 0
  fi

  git -C "$repo_dir" commit -m "$COMMIT_MSG"
  git -C "$repo_dir" push origin main
}

echo "==> 5. Commit & push COPUR/COPUR first (SSOT), then COPUR/COPUR.github.io (Pages)"
sync_repo "$PROFILE_DIR" "COPUR/COPUR"
sync_repo "$PAGES_DIR" "COPUR/COPUR.github.io"

if [[ "$DRY_RUN" == true ]]; then
  echo "==> [DRY-RUN] Validation and /tmp staging preview complete. No remote state was mutated."
  exit 0
fi

echo "==> 6. Ensure COPUR/COPUR.github.io Pages is configured (main /)"
if ! gh api repos/COPUR/COPUR.github.io/pages >/dev/null 2>&1; then
  gh api --method POST repos/COPUR/COPUR.github.io/pages \
    -f "build_type=legacy" \
    -F "source[branch]=main" \
    -F "source[path]=/" >/dev/null
  echo "Enabled GitHub Pages on COPUR/COPUR.github.io (main:/)."
fi

TARGET_SHA="$(git -C "$PAGES_DIR" rev-parse HEAD)"
echo "==> 7. Verify GitHub Pages build for commit $TARGET_SHA"
BUILT=false
for attempt in $(seq 1 12); do
  BUILD_JSON="$(gh api repos/COPUR/COPUR.github.io/pages/builds/latest 2>/dev/null || true)"
  BUILD_STATUS="$(python3 -c 'import json,sys; d=json.loads(sys.stdin.read() or "{}"); print(d.get("status",""))' <<<"$BUILD_JSON")"
  BUILD_SHA="$(python3 -c 'import json,sys; d=json.loads(sys.stdin.read() or "{}"); print(d.get("commit",""))' <<<"$BUILD_JSON")"
  if [[ "$BUILD_STATUS" == "errored" ]]; then
    echo "ERROR: GitHub Pages build errored for commit $BUILD_SHA." >&2
    exit 4
  fi
  if [[ "$BUILD_STATUS" == "built" && "$BUILD_SHA" == "$TARGET_SHA" ]]; then
    BUILT=true
    break
  fi
  sleep 5
done

if [[ "$BUILT" != true ]]; then
  echo "WARNING: Pages build did not finish matching $TARGET_SHA within 60s; check GitHub Pages tab." >&2
  exit 4
fi

echo "==> 8. Live endpoint smoke check"
SMOKE_OK=false
for attempt in $(seq 1 5); do
  BODY="$(curl -fsSL "https://copur.github.io/" 2>/dev/null || true)"
  if grep -qi "10 Canonical Suites" <<<"$BODY"; then
    SMOKE_OK=true
    break
  fi
  sleep 3
done
if [[ "$SMOKE_OK" != true ]]; then
  echo "ERROR: Live smoke check failed on https://copur.github.io/." >&2
  exit 4
fi

echo "==> Done! Profile: https://github.com/COPUR | Showcase: https://copur.github.io/"
