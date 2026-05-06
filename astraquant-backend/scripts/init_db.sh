#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT/services/auth-service"
alembic upgrade head

cd "$ROOT/services/strategy-service"
alembic upgrade head
