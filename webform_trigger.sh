#!/bin/bash
# Triggers the approval_demo workflow and sets up the webform assets for the new UUID.
# Usage: ./webform_trigger.sh [workflow_name]
# Default workflow: approval_demo

WORKFLOW="${1:-approval_demo}"
SERVER="localhost:8080"
CUSTOMER="default"
DIST="modules/webform/build/dist"

echo "Triggering $WORKFLOW..."
curl -s -X POST "http://$SERVER/api/$CUSTOMER/$WORKFLOW" \
  -H "Content-Type: application/json" \
  -d '{"action": "run"}' | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'Engine response: {r}')"

echo "Waiting for approval link..."
sleep 2

LINK=$(grep "Approval link:" logs/command_module.log | tail -1 | grep -oP 'http://[^\s'"'"']+')
if [ -z "$LINK" ]; then
  echo "[ERROR] No approval link found in logs. Is the engine running?"
  exit 1
fi

UUID=$(echo "$LINK" | cut -d'/' -f5)
STEP=$(echo "$LINK" | cut -d'/' -f6)

echo "UUID: $UUID"
echo "Step: $STEP"

mkdir -p "$DIST/webform/$UUID/$STEP"
ln -sfn "$(pwd)/$DIST/configs" "$DIST/webform/$UUID/$STEP/configs"

echo ""
echo "Open this link in your browser:"
echo "$LINK"
