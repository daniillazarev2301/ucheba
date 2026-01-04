#!/usr/bin/env bash
set -euo pipefail

PAGES_URL=${PAGES_URL:-https://example.github.io/ucheba}
ARCHIVE_NAME=${ARCHIVE_NAME:-ucheba.tar.gz}
PROJECT_DIR=${PROJECT_DIR:-/opt/ucheba}

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)."
  exit 1
fi

mkdir -p "$PROJECT_DIR"

curl -fsSL "$PAGES_URL/$ARCHIVE_NAME" -o /tmp/ucheba.tar.gz

rm -rf "$PROJECT_DIR"/*

tar -xzf /tmp/ucheba.tar.gz -C "$PROJECT_DIR" --strip-components=1

bash "$PROJECT_DIR/scripts/install_vds.sh"
