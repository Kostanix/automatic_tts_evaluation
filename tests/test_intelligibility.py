from eval.intelligibility_eval import evaluate_intelligibility
import json
import os

# sample_001
sample_id = "sample_001"
sample_dir = os.path.join("../data", sample_id)
audio_path = os.path.join(sample_dir, "audio.wav")
metadata_path = os.path.join(sample_dir, "metadata.json")

# load reference text
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

reference_text = metadata["text"]

# do evaluation
result = evaluate_intelligibility(audio_path, reference_text)

print(f"Sample: {sample_id}")
print(f"Referenztext: {reference_text}")
print(f"WER: {result['wer']}")
print(f"CER: {result['cer']}")
