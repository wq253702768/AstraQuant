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

request_json() {
  local method="$1"; local url="$2"; local output="$3"; local token="${4:-}"
  local args=(--silent --show-error --max-time 30 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  curl "${args[@]}" "$url" >"$output"
}

echo "[INFO] Sprint 3 Part 1 exchange public acceptance"

LOGIN="$TMP_DIR/login.json"
curl --silent --show-error --max-time 20 -H "Content-Type: application/json" -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" "$GATEWAY_URL/api/auth/login" >"$LOGIN"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

NO_TOKEN="$TMP_DIR/no-token.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/time" "$NO_TOKEN"
assert_code "$NO_TOKEN" UNAUTHORIZED "exchange public rejects missing token"

HEALTH="$TMP_DIR/health.json"
request_json GET "$GATEWAY_URL/api/exchange-public/health" "$HEALTH" "$TOKEN"
assert_code "$HEALTH" SUCCESS "exchange public health"

TIME="$TMP_DIR/time.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/time" "$TIME" "$TOKEN"
assert_code "$TIME" SUCCESS "okx time"

INSTRUMENTS="$TMP_DIR/instruments.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/instruments?contract_type=swap" "$INSTRUMENTS" "$TOKEN"
assert_code "$INSTRUMENTS" SUCCESS "okx instruments"
python3 - "$INSTRUMENTS" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
symbols = {item["internal_symbol"] for item in data["data"]["items"]}
missing = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"} - symbols
if missing:
    raise SystemExit(f"missing symbols: {missing}")
print("[PASS] BTC/ETH instruments present")
PY

TICKER="$TMP_DIR/ticker.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/ticker?symbol=BTC-USDT-SWAP" "$TICKER" "$TOKEN"
assert_code "$TICKER" SUCCESS "okx ticker"
[[ -n "$(json_value "$TICKER" "data.last_price")" ]] || { echo "[FAIL] ticker missing last price"; cat "$TICKER"; exit 1; }
echo "[PASS] ticker has last price"

MARK="$TMP_DIR/mark.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/mark-price?symbol=BTC-USDT-SWAP" "$MARK" "$TOKEN"
assert_code "$MARK" SUCCESS "okx mark price"

FUNDING="$TMP_DIR/funding.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/funding-rate?symbol=BTC-USDT-SWAP" "$FUNDING" "$TOKEN"
assert_code "$FUNDING" SUCCESS "okx funding rate"

KLINES="$TMP_DIR/klines.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=5m&limit=5" "$KLINES" "$TOKEN"
assert_code "$KLINES" SUCCESS "okx klines"

HISTORY_FUNDING="$TMP_DIR/funding-history.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/funding-rate-history?symbol=BTC-USDT-SWAP&limit=5" "$HISTORY_FUNDING" "$TOKEN"
assert_code "$HISTORY_FUNDING" SUCCESS "okx funding history"

echo "[INFO] Sprint 3 Part 1 exchange public acceptance passed"
