#!/usr/bin/env bash
set -euo pipefail

if ! command -v git >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y git
fi

if ! command -v curl >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y curl
fi

if ! command -v rsync >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y rsync
fi

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sudo sh
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin is not available after Docker installation." >&2
  exit 1
fi

sudo mkdir -p /opt/astraquant/app /opt/astraquant/env /opt/astraquant/logs /opt/astraquant/backups
sudo chown -R "$USER":"$USER" /opt/astraquant

echo "AstraQuant staging bootstrap completed."
