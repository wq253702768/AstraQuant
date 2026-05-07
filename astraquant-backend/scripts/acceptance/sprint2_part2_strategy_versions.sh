#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
SUFFIX="$(date +%s)"
CODE="s2_version_${SUFFIX}"
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

echo "[INFO] Sprint 2 Part 2 strategy version acceptance"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

TEMPLATES="$TMP_DIR/templates.json"
request_json GET "$GATEWAY_URL/api/strategy-templates" "$TEMPLATES" "" "$TOKEN"
assert_code "$TEMPLATES" SUCCESS "list strategy templates"
TEMPLATE_ID="$(json_value "$TEMPLATES" "data.items.0.id")"

CREATE="$TMP_DIR/create.json"
request_json POST "$GATEWAY_URL/api/strategies" "$CREATE" "{\"template_id\":\"$TEMPLATE_ID\",\"name\":\"Sprint2 版本验收策略\",\"code\":\"$CODE\",\"description\":\"版本验收\",\"strategy_type\":\"CONFIG\",\"tags\":[\"Sprint2\",\"版本\"]}" "$TOKEN"
assert_code "$CREATE" SUCCESS "create strategy"
STRATEGY_ID="$(json_value "$CREATE" "data.strategy_id")"

LIST1="$TMP_DIR/list1.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions" "$LIST1" "" "$TOKEN"
assert_code "$LIST1" SUCCESS "list initial versions"
SOURCE_ID="$(json_value "$LIST1" "data.items.0.id")"

CREATE_VERSION="$TMP_DIR/create-version.json"
request_json POST "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions" "$CREATE_VERSION" "{\"change_reason\":\"创建 Part2 验收草稿版本\"}" "$TOKEN"
assert_code "$CREATE_VERSION" SUCCESS "create draft version without explicit source"
VERSION_ID="$(json_value "$CREATE_VERSION" "data.strategy_version_id")"

DETAIL="$TMP_DIR/detail.json"
request_json GET "$GATEWAY_URL/api/strategies/$STRATEGY_ID/versions/$VERSION_ID" "$DETAIL" "" "$TOKEN"
assert_code "$DETAIL" SUCCESS "query version detail"
PARAMS="$(json_value "$DETAIL" "data.params_json")"
RISK="$(json_value "$DETAIL" "data.risk_params_json")"

VALID_PAYLOAD="$TMP_DIR/valid-payload.json"
python3 - "$PARAMS" "$RISK" >"$VALID_PAYLOAD" <<'PY'
import json, sys
params = json.loads(sys.argv[1])
risk = json.loads(sys.argv[2])
params["timeframe"] = "15m"
print(json.dumps({"params_json": params, "risk_params_json": risk}, ensure_ascii=False))
PY
VALID="$TMP_DIR/valid.json"
request_json PUT "$GATEWAY_URL/api/strategy-versions/$VERSION_ID/params" "$VALID" "$(cat "$VALID_PAYLOAD")" "$TOKEN"
assert_code "$VALID" SUCCESS "update draft version with valid config"

INVALID_SYMBOL_PAYLOAD="$TMP_DIR/invalid-symbol-payload.json"
python3 - "$PARAMS" "$RISK" >"$INVALID_SYMBOL_PAYLOAD" <<'PY'
import json, sys
params = json.loads(sys.argv[1])
risk = json.loads(sys.argv[2])
params["symbols"] = ["DOGE-USDT-SWAP"]
print(json.dumps({"params_json": params, "risk_params_json": risk}, ensure_ascii=False))
PY
INVALID_SYMBOL="$TMP_DIR/invalid-symbol.json"
request_json PUT "$GATEWAY_URL/api/strategy-versions/$VERSION_ID/params" "$INVALID_SYMBOL" "$(cat "$INVALID_SYMBOL_PAYLOAD")" "$TOKEN"
assert_not_success "$INVALID_SYMBOL" "invalid symbol rejected"

INVALID_RISK_PAYLOAD="$TMP_DIR/invalid-risk-payload.json"
python3 - "$PARAMS" "$RISK" >"$INVALID_RISK_PAYLOAD" <<'PY'
import json, sys
params = json.loads(sys.argv[1])
risk = json.loads(sys.argv[2])
risk["max_leverage"] = 100
print(json.dumps({"params_json": params, "risk_params_json": risk}, ensure_ascii=False))
PY
INVALID_RISK="$TMP_DIR/invalid-risk.json"
request_json PUT "$GATEWAY_URL/api/strategy-versions/$VERSION_ID/params" "$INVALID_RISK" "$(cat "$INVALID_RISK_PAYLOAD")" "$TOKEN"
assert_not_success "$INVALID_RISK" "invalid risk config rejected"

echo "[INFO] Sprint 2 Part 2 strategy version acceptance passed"
