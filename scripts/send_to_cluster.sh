#!/bin/bash

set -e

# === Configuration ===
REMOTE_USER="kg068"
REMOTE_HOST="deeplearn.mi.hdm-stuttgart.de"
REMOTE_DIR="automatic_tts_evaluation"
REMOTE_PATH="$REMOTE_USER@$REMOTE_HOST:~/$REMOTE_DIR/data"
PACKAGE_NAME="eval_data_$(date +%Y%m%d_%H%M%S).tar.gz"

echo "-- Step 1: Checking local data folder"
if [[ ! -d "data" ]]; then
    echo "ERROR: 'data/' folder is missing in $(pwd)"
    exit 1
fi
echo "Found 'data/' folder"

echo "-- Step 2: Creating archive"
tar -czf "$PACKAGE_NAME" data
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to create archive"
    exit 1
fi
echo "Archive created: $PACKAGE_NAME"

echo "-- Step 3: Uploading to cluster"
echo "Target: $REMOTE_PATH"
scp "$PACKAGE_NAME" "$REMOTE_PATH"
if [[ $? -ne 0 ]]; then
    echo "ERROR: Upload failed"
    exit 1
fi
echo "Upload complete"

echo "-- Cleaning up local archive"
rm "$PACKAGE_NAME"

echo "=== Done ==="
