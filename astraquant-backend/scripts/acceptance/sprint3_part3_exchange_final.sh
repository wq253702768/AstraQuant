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

echo "[INFO] Sprint 3 Part 3 exchange final acceptance"

LOGIN="$TMP_DIR/login.json"
curl --silent --show-error --max-time 20 -H "Content-Type: application/json" -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" "$GATEWAY_URL/api/auth/login" >"$LOGIN"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

BTC_OI="$TMP_DIR/btc-oi.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/open-interest?symbol=BTC-USDT-SWAP" "$BTC_OI" "$TOKEN"
assert_code "$BTC_OI" SUCCESS "BTC open interest"
[[ -n "$(json_value "$BTC_OI" "data.open_interest")" ]] || { echo "[FAIL] BTC open interest empty"; cat "$BTC_OI"; exit 1; }
echo "[PASS] BTC open interest non-empty"

ETH_OI="$TMP_DIR/eth-oi.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/open-interest?symbol=ETH-USDT-SWAP" "$ETH_OI" "$TOKEN"
assert_code "$ETH_OI" SUCCESS "ETH open interest"
[[ -n "$(json_value "$ETH_OI" "data.open_interest")" ]] || { echo "[FAIL] ETH open interest empty"; cat "$ETH_OI"; exit 1; }
echo "[PASS] ETH open interest non-empty"

BAD_SYMBOL="$TMP_DIR/bad-symbol.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/open-interest?symbol=DOGE-USDT-SWAP" "$BAD_SYMBOL" "$TOKEN"
assert_code "$BAD_SYMBOL" EXCHANGE_SYMBOL_NOT_SUPPORTED "invalid symbol standard error"

BAD_TIMEFRAME="$TMP_DIR/bad-timeframe.json"
request_json GET "$GATEWAY_URL/api/exchange-public/exchanges/OKX/klines?symbol=BTC-USDT-SWAP&timeframe=2m&limit=5" "$BAD_TIMEFRAME" "$TOKEN"
assert_code "$BAD_TIMEFRAME" EXCHANGE_TIMEFRAME_NOT_SUPPORTED "invalid timeframe standard error"

echo "[INFO] Sprint 3 Part 3 exchange final acceptance passed"
