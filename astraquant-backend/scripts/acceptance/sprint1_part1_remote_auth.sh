#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234:8000}"
FRONTEND_URL="${ASTRA_FRONTEND_URL:-http://47.239.90.234:5173}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
: "${ASTRA_TEST_PASSWORD:?Set ASTRA_TEST_PASSWORD for the staging admin account}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

LOGIN_JSON="$TMP_DIR/login.json"
ME_JSON="$TMP_DIR/me.json"
REFRESH_JSON="$TMP_DIR/refresh.json"
UNAUTH_JSON="$TMP_DIR/unauth.json"

pass() {
  echo "[PASS] $1"
}

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

json_value() {
  python3 - "$1" "$2" <<'PY'
import json
import sys

path, expr = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
for part in expr.split("."):
    data = data[part]
print(data)
PY
}

assert_code_success() {
  local file="$1"
  local name="$2"
  local code
  code="$(json_value "$file" "code")"
  [[ "$code" == "SUCCESS" ]] || fail "$name returned code=$code"
  pass "$name returned SUCCESS"
}

echo "[INFO] Sprint 1 Part 1 remote acceptance"
echo "[INFO] Gateway:  $GATEWAY_URL"
echo "[INFO] Frontend: $FRONTEND_URL"

curl --fail --silent --show-error --max-time 10 "$GATEWAY_URL/health" >/dev/null
pass "Gateway health"

curl --fail --silent --show-error --max-time 10 "$FRONTEND_URL/" >/dev/null
pass "Frontend page"

curl --silent --show-error --max-time 10 \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$ASTRA_TEST_PASSWORD\"}" \
  "$GATEWAY_URL/api/auth/login" >"$LOGIN_JSON"
assert_code_success "$LOGIN_JSON" "Login"

ACCESS_TOKEN="$(json_value "$LOGIN_JSON" "data.access_token")"
REFRESH_TOKEN="$(json_value "$LOGIN_JSON" "data.refresh_token")"
[[ -n "$ACCESS_TOKEN" ]] || fail "missing access token"
[[ -n "$REFRESH_TOKEN" ]] || fail "missing refresh token"
pass "Login returned access and refresh tokens"

curl --silent --show-error --max-time 10 \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  "$GATEWAY_URL/api/auth/me" >"$ME_JSON"
assert_code_success "$ME_JSON" "Current user"

ME_USERNAME="$(json_value "$ME_JSON" "data.username")"
[[ "$ME_USERNAME" == "$USERNAME" ]] || fail "expected username=$USERNAME got $ME_USERNAME"
pass "Current user matches login user"

curl --silent --show-error --max-time 10 \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}" \
  "$GATEWAY_URL/api/auth/refresh" >"$REFRESH_JSON"
assert_code_success "$REFRESH_JSON" "Refresh token"

NEW_ACCESS_TOKEN="$(json_value "$REFRESH_JSON" "data.access_token")"
[[ -n "$NEW_ACCESS_TOKEN" ]] || fail "missing refreshed access token"
pass "Refresh returned new access token"

HTTP_STATUS="$(curl --silent --show-error --max-time 10 -o "$UNAUTH_JSON" -w "%{http_code}" "$GATEWAY_URL/api/dashboard/overview")"
[[ "$HTTP_STATUS" == "401" ]] || fail "expected unauthenticated dashboard status 401 got $HTTP_STATUS"
pass "Protected API rejects missing token"

echo "[INFO] Sprint 1 Part 1 remote acceptance passed"
