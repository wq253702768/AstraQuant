#!/usr/bin/env bash
set -euo pipefail
"$(dirname "$0")/init_db.sh"
cd "$(dirname "$0")/../services/strategy-service"
alembic upgrade head
