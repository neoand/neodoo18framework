#!/usr/bin/env bash
# Fast snapshot of project health for LLM agents
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_PATH="${1:-}"
if [[ -z "$PROJECT_PATH" ]]; then
  echo "Usage: ./scripts/dev/export_agent_brief.sh /absolute/path/to/project" >&2
  exit 1
fi

PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_PATH")"
DOCTOR_CMD_STR="NEODOO_SKIP_PAUSE=1 $ROOT_DIR/neodoo doctor --path $PROJECT_PATH"
VALIDATOR_TARGET="${PROJECT_PATH}/custom_addons"
if [[ ! -d "$VALIDATOR_TARGET" ]]; then
  VALIDATOR_TARGET="$PROJECT_PATH"
fi
VALIDATOR_CMD_STR="python3 $ROOT_DIR/framework/validator/validate.py $VALIDATOR_TARGET --strict --auto-fix"
CORP_CMD_STR="python3 $ROOT_DIR/framework/validator/validate.py $VALIDATOR_TARGET --plugins-dir $ROOT_DIR/corporate_plugins --strict"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

DOCTOR_LOG_RAW="$TMP_DIR/doctor-raw.log"
VALIDATOR_LOG_RAW="$TMP_DIR/validator-raw.log"
CORP_LOG_RAW="$TMP_DIR/corporate-raw.log"
DOCTOR_LOG="$TMP_DIR/doctor.log"
VALIDATOR_LOG="$TMP_DIR/validator.log"
CORP_LOG="$TMP_DIR/corporate.log"

printf "[INFO] Running %s\n" "$DOCTOR_CMD_STR"
NEODOO_SKIP_PAUSE=1 "$ROOT_DIR/neodoo" doctor --path "$PROJECT_PATH" >"$DOCTOR_LOG_RAW" 2>&1 || true

printf "[INFO] Running %s\n" "$VALIDATOR_CMD_STR"
python3 "$ROOT_DIR/framework/validator/validate.py" "$VALIDATOR_TARGET" --strict --auto-fix >"$VALIDATOR_LOG_RAW" 2>&1 || true

CORP_AVAILABLE=false
if [[ -d "$ROOT_DIR/corporate_plugins" ]]; then
  CORP_AVAILABLE=true
  printf "[INFO] Running %s\n" "$CORP_CMD_STR"
  python3 "$ROOT_DIR/framework/validator/validate.py" "$VALIDATOR_TARGET" --plugins-dir "$ROOT_DIR/corporate_plugins" --strict >"$CORP_LOG_RAW" 2>&1 || true
fi

# Strip ANSI sequences for readability
perl -pe 's/\e\[[0-9;]*[A-Za-z]//g' "$DOCTOR_LOG_RAW" > "$DOCTOR_LOG"
perl -pe 's/\e\[[0-9;]*[A-Za-z]//g' "$VALIDATOR_LOG_RAW" > "$VALIDATOR_LOG"
if [[ "$CORP_AVAILABLE" == true ]]; then
  perl -pe 's/\e\[[0-9;]*[A-Za-z]//g' "$CORP_LOG_RAW" > "$CORP_LOG"
fi

BRIEF_FILE="$ROOT_DIR/docs/agent-brief.md"
mkdir -p "$(dirname "$BRIEF_FILE")"

NOW="$(date '+%Y-%m-%d %H:%M:%S %Z')"
{
  echo "# Agent Brief"
  echo
  echo "_Gerado em ${NOW}_"
  echo
  echo "## Projeto"
  echo "- Nome: $PROJECT_NAME"
  echo "- Caminho: $PROJECT_PATH"
  echo "- Target validator: $VALIDATOR_TARGET"
  echo
  echo "## Comandos Executados"
  echo "- \`$DOCTOR_CMD_STR\`"
  echo "- \`$VALIDATOR_CMD_STR\`"
  if [[ "$CORP_AVAILABLE" == true ]]; then
    echo "- \`$CORP_CMD_STR\`"
  fi
  echo
  echo "## Resumo Doctor"
  echo '```'
  tail -n 40 "$DOCTOR_LOG"
  echo '```'
  echo
  echo "## Resumo Validator"
  echo '```'
  tail -n 40 "$VALIDATOR_LOG"
  echo '```'
  if [[ "$CORP_AVAILABLE" == true ]]; then
    echo
    echo "## Resumo Corporate Plugins"
    echo '```'
    tail -n 40 "$CORP_LOG"
    echo '```'
  fi
  echo
  echo "> Atualize este arquivo sempre que novos problemas ou correções forem relevantes para agentes."
} >"$BRIEF_FILE"

printf "[OK] Snapshot salvo em %s\n" "$BRIEF_FILE"
