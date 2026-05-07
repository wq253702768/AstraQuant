#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
SUFFIX="$(date +%s)"
CODE="s25_ux_${SUFFIX}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

json_value() {
  python3 - "$1" "$2" <<'PY'
import json, sys
path, expr = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
for part in expr.split("."):
    data = data[int(part)] if part.isdigit() else data[part]
print(json.dumps(data, ensure_ascii=False) if isinstance(data, (dict, list)) else data)
PY
}

assert_code() {
  local file="$1"; local expected="$2"; local name="$3"; local code
  code="$(json_value "$file" "code")"
  [[ "$code" == "$expected" ]] || { echo "[FAIL] $name expected $expected got $code"; cat "$file"; exit 1; }
  echo "[PASS] $name"
}

request_json() {
  local method="$1"; local url="$2"; local output="$3"; local token="${4:-}"; local payload="${5:-}"
  local args=(--silent --show-error --max-time 20 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  [[ -n "$payload" ]] && args+=(-d "$payload")
  curl "${args[@]}" "$url" >"$output"
}

echo "[INFO] Sprint 2.5 strategy UX acceptance"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

TEMPLATES="$TMP_DIR/templates.json"
request_json GET "$GATEWAY_URL/api/strategy-templates" "$TEMPLATES" "$TOKEN"
assert_code "$TEMPLATES" SUCCESS "list templates"
TEMPLATE_ID="$(json_value "$TEMPLATES" "data.items.0.id")"

TEMPLATE_DETAIL="$TMP_DIR/template-detail.json"
request_json GET "$GATEWAY_URL/api/strategy-templates/$TEMPLATE_ID" "$TEMPLATE_DETAIL" "$TOKEN"
assert_code "$TEMPLATE_DETAIL" SUCCESS "template detail"
json_value "$TEMPLATE_DETAIL" "data.default_config" >/dev/null
json_value "$TEMPLATE_DETAIL" "data.param_schema" >/dev/null
json_value "$TEMPLATE_DETAIL" "data.risk_schema" >/dev/null
echo "[PASS] template detail includes default_config/schema"

CREATE="$TMP_DIR/create.json"
request_json POST "$GATEWAY_URL/api/strategies" "$CREATE" "$TOKEN" "{\"template_id\":\"$TEMPLATE_ID\",\"name\":\"Sprint2.5 UX 验收策略\",\"code\":\"$CODE\",\"strategy_type\":\"CONFIG\",\"tags\":[\"UX\"]}"
assert_code "$CREATE" SUCCESS "create strategy"
STRATEGY_ID="$(json_value "$CREATE" "data.strategy_id")"

UPDATE="$TMP_DIR/update.json"
request_json PUT "$GATEWAY_URL/api/strategies/$STRATEGY_ID" "$UPDATE" "$TOKEN" '{"description":"UX确认框验收更新","tags":["UX","确认"]}'
assert_code "$UPDATE" SUCCESS "update strategy"

COPY="$TMP_DIR/copy.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/copy" "$COPY" "$TOKEN" "{\"name\":\"Sprint2.5 UX 验收策略 - 副本\",\"code\":\"${CODE}_copy\"}"
assert_code "$COPY" SUCCESS "copy strategy"

VERSIONS="$TMP_DIR/versions.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions" "$VERSIONS" "$TOKEN"
assert_code "$VERSIONS" SUCCESS "list versions"
VERSION_ID="$(json_value "$VERSIONS" "data.items.0.id")"

VERSION_DETAIL="$TMP_DIR/version-detail.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$VERSION_ID" "$VERSION_DETAIL" "$TOKEN"
assert_code "$VERSION_DETAIL" SUCCESS "version detail"

ARCHIVE="$TMP_DIR/archive.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/archive" "$ARCHIVE" "$TOKEN" '{"reason":"Sprint2.5 UX 验收归档"}'
assert_code "$ARCHIVE" SUCCESS "archive strategy"

echo "[INFO] Sprint 2.5 strategy UX acceptance passed"
