#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
SUFFIX="$(date +%s)"
CODE="s2_publish_${SUFFIX}"
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

assert_not_success() {
  local file="$1"; local name="$2"; local code
  code="$(json_value "$file" "code")"
  [[ "$code" != "SUCCESS" ]] || { echo "[FAIL] $name expected failure got SUCCESS"; cat "$file"; exit 1; }
  echo "[PASS] $name ($code)"
}

request_json() {
  local method="$1"; local url="$2"; local output="$3"; local payload="${4:-}"; local token="${5:-}"
  local args=(--silent --show-error --max-time 20 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  [[ -n "$payload" ]] && args+=(-d "$payload")
  curl "${args[@]}" "$url" >"$output"
}

echo "[INFO] Sprint 2 Part 3 strategy publish acceptance"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

TEMPLATES="$TMP_DIR/templates.json"
request_json GET "$GATEWAY_URL/api/strategy-templates" "$TEMPLATES" "" "$TOKEN"
TEMPLATE_ID="$(json_value "$TEMPLATES" "data.items.0.id")"

CREATE="$TMP_DIR/create.json"
request_json POST "$GATEWAY_URL/api/strategies" "$CREATE" "{\"template_id\":\"$TEMPLATE_ID\",\"name\":\"Sprint2 发布验收策略\",\"code\":\"$CODE\",\"strategy_type\":\"CONFIG\"}" "$TOKEN"
assert_code "$CREATE" SUCCESS "create strategy"
STRATEGY_ID="$(json_value "$CREATE" "data.strategy_id")"

VERSIONS="$TMP_DIR/versions.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions" "$VERSIONS" "" "$TOKEN"
VERSION_ID="$(json_value "$VERSIONS" "data.items.0.id")"

PUBLISH="$TMP_DIR/publish.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$VERSION_ID/publish" "$PUBLISH" "{\"publish_note\":\"Sprint2 Part3 发布验收\"}" "$TOKEN"
assert_code "$PUBLISH" SUCCESS "publish draft version"
STATUS="$(json_value "$PUBLISH" "data.status")"
[[ "$STATUS" == "PUBLISHED" ]] || { echo "[FAIL] publish status expected PUBLISHED got $STATUS"; cat "$PUBLISH"; exit 1; }
CONFIG_HASH="$(json_value "$PUBLISH" "data.config_hash")"
[[ -n "$CONFIG_HASH" && "$CONFIG_HASH" != "null" ]] || { echo "[FAIL] config_hash missing"; cat "$PUBLISH"; exit 1; }
echo "[PASS] published version has config hash"

DETAIL="$TMP_DIR/detail.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$VERSION_ID" "$DETAIL" "" "$TOKEN"
assert_code "$DETAIL" SUCCESS "query published version detail"
[[ "$(json_value "$DETAIL" "data.status")" == "PUBLISHED" ]] || { echo "[FAIL] detail status is not PUBLISHED"; cat "$DETAIL"; exit 1; }

STRATEGY="$TMP_DIR/strategy.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID" "$STRATEGY" "" "$TOKEN"
assert_code "$STRATEGY" SUCCESS "query strategy after publish"
[[ "$(json_value "$STRATEGY" "data.latest_version_id")" == "$VERSION_ID" ]] || { echo "[FAIL] strategy latest_version_id not updated"; cat "$STRATEGY"; exit 1; }
echo "[PASS] strategy latest_version_id updated"

PARAMS="$(json_value "$DETAIL" "data.params_json")"
RISK="$(json_value "$DETAIL" "data.risk_params_json")"
EDIT_PUBLISHED="$TMP_DIR/edit-published.json"
request_json PUT "$GATEWAY_URL/api/strategy-versions/$VERSION_ID/params" "$EDIT_PUBLISHED" "{\"params_json\":$PARAMS,\"risk_params_json\":$RISK}" "$TOKEN"
assert_not_success "$EDIT_PUBLISHED" "published version rejects params update"

COPY="$TMP_DIR/copy.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$VERSION_ID/copy" "$COPY" "{\"change_reason\":\"复制已发布版本为新草稿\"}" "$TOKEN"
assert_code "$COPY" SUCCESS "copy published version as draft"
NEW_VERSION_ID="$(json_value "$COPY" "data.strategy_version_id")"

NEW_DETAIL="$TMP_DIR/new-detail.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$NEW_VERSION_ID" "$NEW_DETAIL" "" "$TOKEN"
assert_code "$NEW_DETAIL" SUCCESS "query copied draft version"
[[ "$(json_value "$NEW_DETAIL" "data.status")" == "DRAFT" ]] || { echo "[FAIL] copied version is not DRAFT"; cat "$NEW_DETAIL"; exit 1; }
echo "[PASS] copied version is draft"

echo "[INFO] Sprint 2 Part 3 strategy publish acceptance passed"
