#!/usr/bin/env bash
# Fast sanity checks for Neodoo18Framework on macOS/Linux
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

info() { echo "[INFO] $*"; }
ok() { echo "[ OK ] $*"; }
fail() { echo "[FAIL] $*"; exit 1; }

TMP_BASE="/tmp/neodoo_sanity"
PRJ_NAME="sanity_proj"
MOD_NAME="sanity_mod"
PRJ_PATH="$TMP_BASE/$PRJ_NAME"

info "Listing templates..."
python3 framework/generator/create_project.py --name tmp --list-templates || fail "template listing failed"

info "Doctor (env)..."
python3 framework/cli/neodoo.py doctor || fail "doctor env failed"

info "Creating project... ($PRJ_PATH)"
rm -rf "$PRJ_PATH" || true
python3 framework/cli/neodoo.py create --name "$PRJ_NAME" --base-dir "$TMP_BASE" --module "$MOD_NAME" --template minimal --no-venv || fail "create failed"

info "Doctor (project)..."
python3 framework/cli/neodoo.py doctor --path "$PRJ_PATH" || fail "doctor project failed"

info "Validator strict..."
python3 framework/validator/validate.py "$PRJ_PATH/custom_addons/$MOD_NAME" --strict --auto-fix || fail "validator strict failed"

ok "All sanity checks passed"
