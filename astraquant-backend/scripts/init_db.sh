#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../services/auth-service"
alembic upgrade head
