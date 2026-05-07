#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
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
  local method="$1"; local url="$2"; local output="$3"; local token="${4:-}"; local payload="${5:-}"
  local args=(--silent --show-error --max-time 30 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  [[ -n "$payload" ]] && args+=(-d "$payload")
  curl "${args[@]}" "$url" >"$output"
}

echo "[INFO] Sprint 3 Part 2 exchange metadata acceptance"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

SYNC="$TMP_DIR/sync.json"
request_json POST "$GATEWAY_URL/api/exchange-public/instruments/sync" "$SYNC" "$TOKEN" '{"exchange":"OKX","inst_type":"SWAP"}'
assert_code "$SYNC" SUCCESS "sync instruments"

INSTRUMENTS="$TMP_DIR/instruments.json"
request_json GET "$GATEWAY_URL/api/exchange-public/instruments?exchange=OKX&inst_type=SWAP" "$INSTRUMENTS" "$TOKEN"
assert_code "$INSTRUMENTS" SUCCESS "query stored instruments"
python3 - "$INSTRUMENTS" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
symbols = {item["internal_symbol"] for item in data["data"]["items"]}
missing = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"} - symbols
if missing:
    raise SystemExit(f"missing symbols: {missing}")
print("[PASS] stored BTC/ETH instruments present")
PY

DETAIL="$TMP_DIR/detail.json"
request_json GET "$GATEWAY_URL/api/exchange-public/instruments/BTC-USDT-SWAP?exchange=OKX" "$DETAIL" "$TOKEN"
assert_code "$DETAIL" SUCCESS "query stored instrument detail"

MAPPINGS="$TMP_DIR/mappings.json"
request_json GET "$GATEWAY_URL/api/exchange-public/symbol-mappings?exchange=OKX" "$MAPPINGS" "$TOKEN"
assert_code "$MAPPINGS" SUCCESS "query symbol mappings"
python3 - "$MAPPINGS" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
symbols = {item["internal_symbol"] for item in data["data"]["items"]}
if "BTC-USDT-SWAP" not in symbols or "ETH-USDT-SWAP" not in symbols:
    raise SystemExit("BTC/ETH mappings missing")
print("[PASS] BTC/ETH symbol mappings present")
PY

KLINES="$TMP_DIR/klines.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=5m&limit=5" "$KLINES" "$TOKEN"
assert_code "$KLINES" SUCCESS "valid klines"

BAD_TIMEFRAME="$TMP_DIR/bad-timeframe.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=2m&limit=5" "$BAD_TIMEFRAME" "$TOKEN"
assert_not_success "$BAD_TIMEFRAME" "invalid timeframe rejected"

BAD_LIMIT="$TMP_DIR/bad-limit.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=5m&limit=999" "$BAD_LIMIT" "$TOKEN"
assert_not_success "$BAD_LIMIT" "kline limit rejected"

FUNDING="$TMP_DIR/funding-history.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/funding-rate-history?symbol=BTC-USDT-SWAP&limit=5" "$FUNDING" "$TOKEN"
assert_code "$FUNDING" SUCCESS "valid funding history"

BAD_FUNDING_LIMIT="$TMP_DIR/bad-funding-limit.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/funding-rate-history?symbol=BTC-USDT-SWAP&limit=999" "$BAD_FUNDING_LIMIT" "$TOKEN"
assert_not_success "$BAD_FUNDING_LIMIT" "funding history limit rejected"

echo "[INFO] Sprint 3 Part 2 exchange metadata acceptance passed"
