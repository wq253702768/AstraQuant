#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

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
  --exclude "frontend/dist" \
  --exclude "astraquant-backend/.venv" \
  -e "ssh ${SSH_OPTS[*]}" \
  "$REPO_ROOT/" "$REMOTE:$ASTRA_STAGING_APP_DIR/"

echo "==> Checking staging env file"
ssh "${SSH_OPTS[@]}" "$REMOTE" "test -f '$ASTRA_STAGING_ENV_FILE'"

COMPOSE="docker compose --env-file '$ASTRA_STAGING_ENV_FILE' -f deploy/staging/docker-compose.sprint2-part1.yml"

echo "==> Building and starting Sprint 2 Part 1 stack"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR/astraquant-backend' && $COMPOSE up -d --build"

echo "==> Running migrations"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR/astraquant-backend' && $COMPOSE run --rm auth-service alembic upgrade head"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR/astraquant-backend' && $COMPOSE run --rm strategy-service alembic upgrade head"

echo "==> Seeding admin user and strategy templates"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR/astraquant-backend' && $COMPOSE run --rm -v '$ASTRA_STAGING_APP_DIR/astraquant-backend/scripts:/scripts:ro' auth-service python /scripts/create_admin_user.py || true"
ssh "${SSH_OPTS[@]}" "$REMOTE" "cd '$ASTRA_STAGING_APP_DIR/astraquant-backend' && $COMPOSE run --rm -v '$ASTRA_STAGING_APP_DIR/astraquant-backend/scripts:/scripts:ro' strategy-service python /scripts/seed_strategy_templates.py"

echo "==> Sprint 2 Part 1 deployment finished"
