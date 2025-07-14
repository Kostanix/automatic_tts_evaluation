import json
import os
import csv

from eval.intelligibility_eval import evaluate_intelligibility
from eval.mos_eval import evaluate_mos
from eval.speaker_similarity_eval import evaluate_speaker_similarity
from eval.prosody_eval import evaluate_prosody

DATA_DIR = "data"
RESULTS_FILE = "results.csv"

HEADER = ["sample_id", "wer", "cer", "similarity", "f0_mean", "f0_std", "duration", "speech_rate", "mos_score"]

sample_dirs = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=HEADER)
    writer.writeheader()

    for sample_id in sample_dirs:
        print(f"Processing {sample_id}...")
        row = {"sample_id": sample_id}

        try:
            base_path = os.path.join(DATA_DIR, sample_id)
            audio_path = os.path.join(base_path, "audio.wav")
            metadata_path = os.path.join(base_path, "metadata.json")
            reference_path = os.path.join(base_path, "reference.wav")

            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                reference_text = metadata["text"]

            # Evaluate intelligibility
            try:
                row.update(evaluate_intelligibility(audio_path, reference_text))
            except Exception as e:
                print(f"  [WARN] intelligibility failed: {e}")

            # Evaluate speaker similarity
            try:
                row.update(evaluate_speaker_similarity(audio_path, reference_path))
            except Exception as e:
                print(f"  [WARN] similarity failed: {e}")

            # Evaluate prosody
            try:
                row.update(evaluate_prosody(audio_path, metadata_path))
            except Exception as e:
                print(f"  [WARN] prosody failed: {e}")

            # Evaluate MOS
            try:
                mos_score = evaluate_mos(audio_path)
                row["mos_score"] = round(mos_score["mos_score"], 2)
            except Exception as e:
                print(f"  [WARN] mos failed: {e}")
                row["mos"] = None

        except Exception as e:
            print(f"[ERROR] Skipping {sample_id} due to: {e}")

        # Ensure all columns exist
        for key in HEADER:
            row.setdefault(key, None)

        writer.writerow(row)
