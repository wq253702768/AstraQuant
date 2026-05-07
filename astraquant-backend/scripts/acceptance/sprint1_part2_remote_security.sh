#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://47.239.90.234}"
USERNAME="${ASTRA_TEST_USERNAME:-admin}"
OLD_PASSWORD="${ASTRA_TEST_PASSWORD:-password}"
NEW_PASSWORD="${ASTRA_TEST_NEW_PASSWORD:-NewPassword@123}"
ASTRA_STAGING_HOST="${ASTRA_STAGING_HOST:-47.239.90.234}"
ASTRA_STAGING_USER="${ASTRA_STAGING_USER:-deploy}"
ASTRA_STAGING_SSH_KEY="${ASTRA_STAGING_SSH_KEY:-}"

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

post_json() {
  local url="$1"
  local payload="$2"
  local output="$3"
  local auth="${4:-}"
  if [[ -n "$auth" ]]; then
    curl --silent --show-error --max-time 15 -H "Content-Type: application/json" -H "Authorization: Bearer $auth" -d "$payload" "$url" >"$output"
  else
    curl --silent --show-error --max-time 15 -H "Content-Type: application/json" -d "$payload" "$url" >"$output"
  fi
}

put_json() {
  local url="$1"
  local payload="$2"
  local output="$3"
  local auth="$4"
  curl --silent --show-error --max-time 15 -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $auth" -d "$payload" "$url" >"$output"
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

reset_password_directly() {
  if [[ -z "$ASTRA_STAGING_SSH_KEY" ]]; then
    return 1
  fi
  ssh -i "$ASTRA_STAGING_SSH_KEY" "$ASTRA_STAGING_USER@$ASTRA_STAGING_HOST" \
    "export ASTRA_TEST_USERNAME='$USERNAME' ASTRA_TEST_PASSWORD='$OLD_PASSWORD'; cd /opt/astraquant/app/astraquant-backend && docker compose --env-file /opt/astraquant/env/.env.staging -f deploy/staging/docker-compose.sprint1-part1.yml run --rm -e ASTRA_TEST_USERNAME -e ASTRA_TEST_PASSWORD -v /opt/astraquant/app/astraquant-backend/scripts:/scripts:ro auth-service python - <<'PY'
import asyncio
import os
from astra_common.security import hash_password
from sqlalchemy import update
from app.infrastructure.db.models import UserAccountModel
from app.infrastructure.db.session import SessionLocal

async def main():
    async with SessionLocal() as session:
        await session.execute(
            update(UserAccountModel)
            .where(UserAccountModel.username == os.environ['ASTRA_TEST_USERNAME'])
            .values(password_hash=hash_password(os.environ['ASTRA_TEST_PASSWORD']))
        )
        await session.commit()

asyncio.run(main())
PY" \
    >/dev/null
}

echo "[INFO] Sprint 1 Part 2 remote security acceptance"
echo "[INFO] Gateway: $GATEWAY_URL"

LOGIN1="$TMP_DIR/login1.json"
post_json "$GATEWAY_URL/api/auth/login" "{\"username\":\"$USERNAME\",\"password\":\"$OLD_PASSWORD\"}" "$LOGIN1"
assert_code "$LOGIN1" "SUCCESS" "login with current password"
ACCESS1="$(json_value "$LOGIN1" "data.access_token")"
REFRESH1="$(json_value "$LOGIN1" "data.refresh_token")"

REFRESH_OK="$TMP_DIR/refresh-ok.json"
post_json "$GATEWAY_URL/api/auth/refresh" "{\"refresh_token\":\"$REFRESH1\"}" "$REFRESH_OK"
assert_code "$REFRESH_OK" "SUCCESS" "refresh token rotation succeeds"
ACCESS2="$(json_value "$REFRESH_OK" "data.access_token")"
REFRESH2="$(json_value "$REFRESH_OK" "data.refresh_token")"

REFRESH_OLD="$TMP_DIR/refresh-old.json"
post_json "$GATEWAY_URL/api/auth/refresh" "{\"refresh_token\":\"$REFRESH1\"}" "$REFRESH_OLD"
assert_code "$REFRESH_OLD" "UNAUTHORIZED" "old refresh token is revoked"

LOGOUT="$TMP_DIR/logout.json"
post_json "$GATEWAY_URL/api/auth/logout" "{\"refresh_token\":\"$REFRESH2\"}" "$LOGOUT" "$ACCESS2"
assert_code "$LOGOUT" "SUCCESS" "logout succeeds"

ME_AFTER_LOGOUT="$TMP_DIR/me-after-logout.json"
curl --silent --show-error --max-time 15 -H "Authorization: Bearer $ACCESS2" "$GATEWAY_URL/api/auth/me" >"$ME_AFTER_LOGOUT"
assert_code "$ME_AFTER_LOGOUT" "UNAUTHORIZED" "access token rejected after logout"

REFRESH_AFTER_LOGOUT="$TMP_DIR/refresh-after-logout.json"
post_json "$GATEWAY_URL/api/auth/refresh" "{\"refresh_token\":\"$REFRESH2\"}" "$REFRESH_AFTER_LOGOUT"
assert_code "$REFRESH_AFTER_LOGOUT" "UNAUTHORIZED" "refresh token rejected after logout"

LOGIN2="$TMP_DIR/login2.json"
post_json "$GATEWAY_URL/api/auth/login" "{\"username\":\"$USERNAME\",\"password\":\"$OLD_PASSWORD\"}" "$LOGIN2"
assert_code "$LOGIN2" "SUCCESS" "login before password change"
ACCESS3="$(json_value "$LOGIN2" "data.access_token")"
REFRESH3="$(json_value "$LOGIN2" "data.refresh_token")"

CHANGE="$TMP_DIR/change.json"
put_json "$GATEWAY_URL/api/auth/password" "{\"old_password\":\"$OLD_PASSWORD\",\"new_password\":\"$NEW_PASSWORD\"}" "$CHANGE" "$ACCESS3"
assert_code "$CHANGE" "SUCCESS" "change password succeeds"

OLD_LOGIN="$TMP_DIR/old-login.json"
post_json "$GATEWAY_URL/api/auth/login" "{\"username\":\"$USERNAME\",\"password\":\"$OLD_PASSWORD\"}" "$OLD_LOGIN"
assert_code "$OLD_LOGIN" "AUTH_INVALID_CREDENTIALS" "old password rejected"

REFRESH_AFTER_CHANGE="$TMP_DIR/refresh-after-change.json"
post_json "$GATEWAY_URL/api/auth/refresh" "{\"refresh_token\":\"$REFRESH3\"}" "$REFRESH_AFTER_CHANGE"
assert_code "$REFRESH_AFTER_CHANGE" "UNAUTHORIZED" "old refresh rejected after password change"

NEW_LOGIN="$TMP_DIR/new-login.json"
post_json "$GATEWAY_URL/api/auth/login" "{\"username\":\"$USERNAME\",\"password\":\"$NEW_PASSWORD\"}" "$NEW_LOGIN"
assert_code "$NEW_LOGIN" "SUCCESS" "new password login succeeds"
ACCESS4="$(json_value "$NEW_LOGIN" "data.access_token")"

RESTORE="$TMP_DIR/restore.json"
put_json "$GATEWAY_URL/api/auth/password" "{\"old_password\":\"$NEW_PASSWORD\",\"new_password\":\"$OLD_PASSWORD\"}" "$RESTORE" "$ACCESS4"
if [[ "$(json_value "$RESTORE" "code")" == "SUCCESS" ]]; then
  echo "[PASS] restore original password"
else
  echo "[INFO] restore via API failed, attempting staging cleanup reset"
  reset_password_directly || { echo "[FAIL] could not restore original password"; cat "$RESTORE"; exit 1; }
  RESTORE_LOGIN="$TMP_DIR/restore-login.json"
  post_json "$GATEWAY_URL/api/auth/login" "{\"username\":\"$USERNAME\",\"password\":\"$OLD_PASSWORD\"}" "$RESTORE_LOGIN"
  assert_code "$RESTORE_LOGIN" "SUCCESS" "restore original password via staging cleanup"
fi

echo "[INFO] Sprint 1 Part 2 remote security acceptance passed"
