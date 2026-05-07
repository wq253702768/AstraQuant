#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
BAD_PASSWORD="${ASTRA_TEST_BAD_PASSWORD:-wrong-password}"
FAILED_LIMIT="${ASTRA_LOGIN_FAILED_LIMIT:-5}"
ASTRA_STAGING_HOST="${ASTRA_STAGING_HOST:-47.239.90.234}"
ASTRA_STAGING_USER="${ASTRA_STAGING_USER:-deploy}"
: "${ASTRA_STAGING_SSH_KEY:?Set ASTRA_STAGING_SSH_KEY so the script can clean Redis lock keys after the test}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

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

login() {
  local password="$1"
  local output="$2"
  curl --silent --show-error --max-time 15 \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$USERNAME\",\"password\":\"$password\"}" \
    "$GATEWAY_URL/api/auth/login" >"$output"
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

clear_login_protection() {
  ssh -i "$ASTRA_STAGING_SSH_KEY" "$ASTRA_STAGING_USER@$ASTRA_STAGING_HOST" \
    "cd /opt/astraquant/app/astraquant-backend && docker compose --env-file /opt/astraquant/env/.env.staging -f deploy/staging/docker-compose.sprint1-part1.yml exec -T redis redis-cli DEL auth:login_failed:${USERNAME,,} auth:login_locked:${USERNAME,,}" >/dev/null
}

echo "[INFO] Sprint 1 Part 3 login protection acceptance"
echo "[INFO] Gateway: $GATEWAY_URL"

clear_login_protection

for i in $(seq 1 "$FAILED_LIMIT"); do
  OUT="$TMP_DIR/bad-$i.json"
  login "$BAD_PASSWORD" "$OUT"
  if [[ "$i" -lt "$FAILED_LIMIT" ]]; then
    assert_code "$OUT" "AUTH_INVALID_CREDENTIALS" "bad password attempt $i rejected"
  else
    assert_code "$OUT" "AUTH_USER_LOCKED" "bad password attempt $i locks account"
  fi
done

LOCKED_GOOD="$TMP_DIR/locked-good.json"
login "$PASSWORD" "$LOCKED_GOOD"
assert_code "$LOCKED_GOOD" "AUTH_USER_LOCKED" "correct password rejected while locked"

clear_login_protection

LOGIN_OK="$TMP_DIR/login-ok.json"
login "$PASSWORD" "$LOGIN_OK"
assert_code "$LOGIN_OK" "SUCCESS" "login succeeds after clearing lock"

echo "[INFO] Sprint 1 Part 3 login protection acceptance passed"
