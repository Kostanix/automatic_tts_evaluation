import os
import csv
import json

from eval.intelligibility_eval import evaluate_intelligibility
from eval.speaker_similarity_eval import evaluate_speaker_similarity
from eval.prosody_eval import evaluate_prosody
from eval.mos_eval import evaluate_mos

DATA_DIR = "data"
RESULTS_FILE = "results.csv"

sample_dirs = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

all_metadata_keys = set()
results_rows = []

for sample_id in sample_dirs:
    base_path = os.path.join(DATA_DIR, sample_id)
    metadata_path = os.path.join(base_path, "metadata.json")

    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            all_metadata_keys.update(metadata.keys())

eval_keys = ["sample_id", "wer", "cer", "similarity", "f0_mean", "f0_std", "duration", "speech_rate", "mos_score"]
header = ["sample_id"] + sorted(all_metadata_keys) + eval_keys[1:]  # sample_id nicht doppeln

with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()

    for sample_id in sample_dirs:
        print(f"Processing {sample_id}...")
        row = {"sample_id": sample_id}

        try:
            base_path = os.path.join(DATA_DIR, sample_id)
            audio_path = os.path.join(base_path, "audio.wav")
            metadata_path = os.path.join(base_path, "metadata.json")
            reference_path = os.path.join(base_path, "reference.wav")

            # Load metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    row.update(meta)

            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                reference_text = metadata["text"]

            # Evaluations
            try:
                row.update(evaluate_intelligibility(audio_path, reference_text))
            except Exception as e:
                print(f"  [WARN] intelligibility failed: {e}")

            try:
                row.update(evaluate_speaker_similarity(audio_path, reference_path))
            except Exception as e:
                print(f"  [WARN] similarity failed: {e}")

            try:
                row.update(evaluate_prosody(audio_path, metadata_path))
            except Exception as e:
                print(f"  [WARN] prosody failed: {e}")

            try:
                row.update(evaluate_mos(audio_path))
            except Exception as e:
                print(f"  [WARN] mos failed: {e}")

        except Exception as e:
            print(f"[ERROR] Skipping {sample_id}: {e}")

        # Ensure all columns are present
        for key in header:
            row.setdefault(key, None)

        writer.writerow(row)
