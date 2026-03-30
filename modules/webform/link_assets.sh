#!/bin/bash
# Links the compiled webform assets (JS/CSS/configs) from build/dist/ into
# the webform module root so serve_webform_assets.py can serve them on :9000.
#
# Run once after cloning or after rebuilding the webform frontend:
#   cd modules/webform && ./link_assets.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST="$SCRIPT_DIR/build/dist"

if [ ! -d "$DIST" ]; then
  echo "Error: $DIST not found. Build the webform frontend first."
  exit 1
fi

cd "$SCRIPT_DIR"

for item in webform_bundle.js webform_bundle.css custom.css configs; do
  if [ -e "$DIST/$item" ]; then
    ln -sfn "$DIST/$item" "$item" 2>/dev/null || cp -r "$DIST/$item" "$item"
    echo "Linked $item"
  fi
done

echo "Webform assets linked. serve_webform_assets.py can now serve from :9000."
