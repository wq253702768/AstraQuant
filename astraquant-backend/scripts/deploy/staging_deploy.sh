#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

: "${ASTRA_STAGING_HOST:?Set ASTRA_STAGING_HOST, for example 47.239.90.234}"
: "${ASTRA_STAGING_USER:=deploy}"
: "${ASTRA_STAGING_APP_DIR:=/opt/astraquant/app}"
: "${ASTRA_STAGING_ENV_FILE:=/opt/astraquant/env/.env.staging}"

SSH_OPTS=()
if [[ -n "${ASTRA_STAGING_SSH_KEY:-}" ]]; then
  SSH_OPTS=(-i "$ASTRA_STAGING_SSH_KEY")
fi

REMOTE="${ASTRA_STAGING_USER}@${ASTRA_STAGING_HOST}"

echo "==> Preparing remote directories on ${REMOTE}"
ssh "${SSH_OPTS[@]}" "$REMOTE" "mkdir -p '$ASTRA_STAGING_APP_DIR'"

echo "==> Syncing repository files"
rsync -az --delete \
  --exclude ".git" \
  --exclude "**/.pytest_cache" \
  --exclude "**/__pycache__" \
  --exclude "frontend/node_modules" \
  --exclude "astraquant-backend/.venv" \
  -e "ssh ${SSH_OPTS[*]}" \
  "$ROOT_DIR/" "$REMOTE:$ASTRA_STAGING_APP_DIR/"

echo "==> Checking staging env file"
ssh "${SSH_OPTS[@]}" "$REMOTE" "test -f '$ASTRA_STAGING_ENV_FILE' || (echo 'Missing $ASTRA_STAGING_ENV_FILE on server. Copy deploy/staging/.env.staging.example there and fill secrets.' >&2; exit 2)"

echo "==> Building and starting staging stack"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR' && docker compose --env-file '$ASTRA_STAGING_ENV_FILE' -f docker-compose.yml -f deploy/staging/docker-compose.staging.yml up -d --build"

echo "==> Running database migrations"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR' && docker compose --env-file '$ASTRA_STAGING_ENV_FILE' -f docker-compose.yml -f deploy/staging/docker-compose.staging.yml run --rm auth-service alembic upgrade head"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR' && docker compose --env-file '$ASTRA_STAGING_ENV_FILE' -f docker-compose.yml -f deploy/staging/docker-compose.staging.yml run --rm strategy-lifecycle-center alembic upgrade head"

echo "==> Seeding admin user"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR' && docker compose --env-file '$ASTRA_STAGING_ENV_FILE' -f docker-compose.yml -f deploy/staging/docker-compose.staging.yml run --rm -v '$ASTRA_STAGING_APP_DIR/scripts:/scripts:ro' auth-service python /scripts/create_admin_user.py || true"

echo "==> Deployment command finished"
echo "Run scripts/deploy/staging_healthcheck.sh to verify public endpoints."
