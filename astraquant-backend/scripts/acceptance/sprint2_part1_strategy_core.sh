#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
SUFFIX="$(date +%s)"
CODE="s2_core_${SUFFIX}"
COPY_CODE="${CODE}_copy"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

json_value() {
  python3 - "$1" "$2" <<'PY'
import json, sys
path, expr = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
for part in expr.split("."):
    if part.isdigit():
        data = data[int(part)]
    else:
        data = data[part]
print(data)
PY
}

assert_code() {
  local file="$1"
  local expected="$2"
  local name="$3"
  local code
  code="$(json_value "$file" "code")"
  [[ "$code" == "$expected" ]] || { echo "[FAIL] $name expected $expected got $code"; cat "$file"; exit 1; }
  echo "[PASS] $name"
}

request_json() {
  local method="$1"; local url="$2"; local output="$3"; local payload="${4:-}"; local token="${5:-}"
  local args=(--silent --show-error --max-time 20 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  [[ -n "$payload" ]] && args+=(-d "$payload")
  curl "${args[@]}" "$url" >"$output"
}

echo "[INFO] Sprint 2 Part 1 strategy core acceptance"
echo "[INFO] Gateway: $GATEWAY_URL"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

NO_TOKEN="$TMP_DIR/no-token.json"
curl --silent --show-error --max-time 20 "$GATEWAY_URL/api/strategies" >"$NO_TOKEN"
assert_code "$NO_TOKEN" UNAUTHORIZED "strategy list rejects missing token"

TEMPLATES="$TMP_DIR/templates.json"
request_json GET "$GATEWAY_URL/api/strategy-templates" "$TEMPLATES" "" "$TOKEN"
assert_code "$TEMPLATES" SUCCESS "list strategy templates"
TEMPLATE_ID="$(json_value "$TEMPLATES" "data.items.0.id")"

CREATE="$TMP_DIR/create.json"
request_json POST "$GATEWAY_URL/api/strategies" "$CREATE" "{\"template_id\":\"$TEMPLATE_ID\",\"name\":\"Sprint2 核心验收策略\",\"code\":\"$CODE\",\"description\":\"真实地址验收创建\",\"strategy_type\":\"CONFIG\",\"tags\":[\"Sprint2\",\"验收\"]}" "$TOKEN"
assert_code "$CREATE" SUCCESS "create strategy"
STRATEGY_ID="$(json_value "$CREATE" "data.strategy_id")"

DUP="$TMP_DIR/duplicate.json"
request_json POST "$GATEWAY_URL/api/strategies" "$DUP" "{\"template_id\":\"$TEMPLATE_ID\",\"name\":\"重复策略\",\"code\":\"$CODE\",\"strategy_type\":\"CONFIG\"}" "$TOKEN"
assert_code "$DUP" STRATEGY_CODE_ALREADY_EXISTS "duplicate strategy code rejected"

LIST="$TMP_DIR/list.json"
request_json GET "$GATEWAY_URL/api/strategies?keyword=$CODE" "$LIST" "" "$TOKEN"
assert_code "$LIST" SUCCESS "query strategy list"

DETAIL="$TMP_DIR/detail.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID" "$DETAIL" "" "$TOKEN"
assert_code "$DETAIL" SUCCESS "query strategy detail"

UPDATE="$TMP_DIR/update.json"
request_json PUT "$GATEWAY_URL/api/strategies/$STRATEGY_ID" "$UPDATE" "{\"description\":\"已更新的策略描述\",\"tags\":[\"Sprint2\",\"已更新\"]}" "$TOKEN"
assert_code "$UPDATE" SUCCESS "update strategy"

COPY="$TMP_DIR/copy.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/copy" "$COPY" "{\"name\":\"Sprint2 核心验收策略 - 副本\",\"code\":\"$COPY_CODE\"}" "$TOKEN"
assert_code "$COPY" SUCCESS "copy strategy"

ARCHIVE="$TMP_DIR/archive.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/archive" "$ARCHIVE" "{\"reason\":\"Sprint2 Part1 验收归档\"}" "$TOKEN"
assert_code "$ARCHIVE" SUCCESS "archive strategy"

ARCHIVED="$TMP_DIR/archived.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID" "$ARCHIVED" "" "$TOKEN"
assert_code "$ARCHIVED" SUCCESS "query archived strategy"
STATUS="$(json_value "$ARCHIVED" "data.status")"
[[ "$STATUS" == "ARCHIVED" ]] || { echo "[FAIL] archived strategy status expected ARCHIVED got $STATUS"; cat "$ARCHIVED"; exit 1; }
echo "[PASS] archived strategy status confirmed"

echo "[INFO] Sprint 2 Part 1 strategy core acceptance passed"
