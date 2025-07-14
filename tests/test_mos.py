import os
from eval.mos_eval import evaluate_mos

sample_id = "sample_001"
sample_dir = os.path.join("../data", sample_id)

audio_path = os.path.join(sample_dir, "audio.wav")

result = evaluate_mos(audio_path)
print(f"MOS Score for {sample_id}: {result['mos_score']:.2f}")
