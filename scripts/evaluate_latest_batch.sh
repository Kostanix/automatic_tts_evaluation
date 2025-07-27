#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

cd ~/automatic_tts_evaluation/data

echo "Searching for latest .tar.gz archive..."
LATEST_ARCHIVE=$(ls -t eval_data_*.tar.gz | head -n 1)

if [[ -z "$LATEST_ARCHIVE" ]]; then
    echo "No archive found. Aborting."
    exit 1
fi

echo "Found archive: $LATEST_ARCHIVE"
echo "Extracting archive..."
tar -xzf "$LATEST_ARCHIVE"

echo "Running evaluation..."
cd ..
python main.py --config config/default.json

echo "Evaluation complete."
