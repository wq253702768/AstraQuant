#!/usr/bin/env bash
set -euo pipefail

HOST="${ASTRA_STAGING_HOST:-47.239.90.234}"
GATEWAY_URL="${ASTRA_GATEWAY_URL:-http://${HOST}:8000}"
AUTH_URL="${ASTRA_AUTH_URL:-http://${HOST}:8001}"
LIFECYCLE_URL="${ASTRA_LIFECYCLE_URL:-http://${HOST}:8023}"

check() {
  local name="$1"
  local url="$2"
  echo "[healthcheck] ${name}: ${url}"
  curl --fail --silent --show-error --max-time 10 "${url}" >/tmp/astra_healthcheck.json
  echo "[healthcheck] ${name}: ok"
}

check "api-gateway" "${GATEWAY_URL}/health"
check "auth-service" "${AUTH_URL}/health"
check "strategy-lifecycle-center" "${LIFECYCLE_URL}/health"

echo "[healthcheck] staging environment baseline checks passed"
