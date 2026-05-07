#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
SYMBOL="${ASTRA_TEST_SYMBOL:-BTC-USDT-SWAP}"
TIMEFRAME="${ASTRA_TEST_TIMEFRAME:-5m}"
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
  local args=(--silent --show-error --max-time 60 -X "$method" -H "Content-Type: application/json")
  [[ -n "$token" ]] && args+=(-H "Authorization: Bearer $token")
  [[ -n "$payload" ]] && args+=(-d "$payload")
  curl "${args[@]}" "$url" >"$output"
}

read START_TIME END_TIME < <(python3 - <<'PY'
from datetime import datetime, timedelta, timezone
end = datetime.now(timezone.utc)
start = end - timedelta(hours=6)
print(start.isoformat().replace("+00:00", "Z"), end.isoformat().replace("+00:00", "Z"))
PY
)

echo "[INFO] Sprint 4 Part 1 market candle acceptance"

LOGIN="$TMP_DIR/login.json"
request_json POST "$GATEWAY_URL/api/auth/login" "$LOGIN" "" "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"
assert_code "$LOGIN" SUCCESS "login"
TOKEN="$(json_value "$LOGIN" "data.access_token")"

HEALTH="$TMP_DIR/health.json"
request_json GET "$GATEWAY_URL/api/market-data/health" "$HEALTH" "$TOKEN"
assert_code "$HEALTH" SUCCESS "market data health"

NO_TOKEN="$TMP_DIR/no-token.json"
request_json GET "$GATEWAY_URL/api/market-data/klines?exchange=OKX&symbol=$SYMBOL&timeframe=$TIMEFRAME&limit=5" "$NO_TOKEN"
assert_code "$NO_TOKEN" UNAUTHORIZED "market data rejects missing token"

CREATE="$TMP_DIR/create.json"
request_json POST "$GATEWAY_URL/api/market-data/sync" "$CREATE" "$TOKEN" "{\"exchange\":\"OKX\",\"symbols\":[\"$SYMBOL\"],\"data_types\":[\"kline\"],\"timeframes\":[\"$TIMEFRAME\"],\"start_time\":\"$START_TIME\",\"end_time\":\"$END_TIME\"}"
assert_code "$CREATE" SUCCESS "create candle sync task"
TASK_ID="$(json_value "$CREATE" "data.sync_task_id")"

RUN1="$TMP_DIR/run1.json"
request_json POST "$GATEWAY_URL/api/market-data/sync/$TASK_ID/run" "$RUN1" "$TOKEN"
assert_code "$RUN1" SUCCESS "run candle sync task"
STATUS="$(json_value "$RUN1" "data.status")"
[[ "$STATUS" == "SUCCESS" ]] || { echo "[FAIL] task status expected SUCCESS got $STATUS"; cat "$RUN1"; exit 1; }

DETAIL="$TMP_DIR/detail.json"
request_json GET "$GATEWAY_URL/api/market-data/sync/$TASK_ID" "$DETAIL" "$TOKEN"
assert_code "$DETAIL" SUCCESS "query sync task detail"

CANDLES="$TMP_DIR/candles.json"
request_json GET "$GATEWAY_URL/api/market-data/klines?exchange=OKX&symbol=$SYMBOL&timeframe=$TIMEFRAME&start_time=$START_TIME&end_time=$END_TIME&limit=100" "$CANDLES" "$TOKEN"
assert_code "$CANDLES" SUCCESS "query stored candles"
COUNT="$(python3 - "$CANDLES" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding='utf-8'))
print(len(data["data"]["items"]))
PY
)"
[[ "$COUNT" -gt 0 ]] || { echo "[FAIL] expected stored candles count > 0"; cat "$CANDLES"; exit 1; }
echo "[PASS] stored candles count > 0 ($COUNT)"

RUN2="$TMP_DIR/run2.json"
request_json POST "$GATEWAY_URL/api/market-data/sync/$TASK_ID/run" "$RUN2" "$TOKEN"
assert_code "$RUN2" SUCCESS "rerun candle sync task idempotently"

echo "[INFO] Sprint 4 Part 1 market candle acceptance passed"
