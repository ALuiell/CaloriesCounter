#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/caloriescounter/app}"
SHARED_DIR="${SHARED_DIR:-/opt/caloriescounter/shared}"
VENV_DIR="${VENV_DIR:-$APP_DIR/.venv}"
SERVICE_NAME="${SERVICE_NAME:-caloriescounter}"
BRANCH="${BRANCH:-master}"

echo "Deploying CaloriesCounter from branch: $BRANCH"
echo "App dir: $APP_DIR"
echo "Shared dir: $SHARED_DIR"

cd "$APP_DIR"

if [ ! -f "$SHARED_DIR/.env" ]; then
  echo "Missing $SHARED_DIR/.env"
  echo "Create it first, for example from .env.example"
  exit 1
fi

git fetch origin
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

mkdir -p "$SHARED_DIR/data"

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl restart "$SERVICE_NAME"
  sudo systemctl status "$SERVICE_NAME" --no-pager
else
  echo "systemctl not found; restart the bot process manually."
fi

echo "Deploy finished."
