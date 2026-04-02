#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 <linux / macos>"
  exit 1
fi

# Start the webform asset server on port 9000 (serves JS/CSS for the
# webform UI at :8080). Set WEBFORM_ASSETS=0 to disable.
if [ "${WEBFORM_ASSETS:-1}" != "0" ]; then
  if [ -f modules/webform/serve_webform_assets.py ]; then
    echo "Starting webform asset server on :9000..."
    python3 modules/webform/serve_webform_assets.py &
    ASSET_PID=$!
    trap "kill $ASSET_PID 2>/dev/null" EXIT
  fi
fi

case "$1" in
  linux)
    echo "Starting Seyoawe Community Edition for Linux..."
    ./seyoawe.linux
    ;;
  macos)
    echo "Starting Seyoawe Community Edition for macOS..."
    ./seyoawe.macos.arm
    ;;
  *)
    echo "Invalid argument. Use 'linux' or 'macos'."
    exit 1
    ;;
esac