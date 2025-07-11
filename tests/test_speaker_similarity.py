from eval.speaker_similarity_eval import evaluate_speaker_similarity
import os

sample_id = "sample_001"

sample_dir = os.path.join("../data", sample_id)
audio_path = os.path.join(sample_dir, "audio.wav")
reference_path = os.path.join(sample_dir, "reference.wav")

result = evaluate_speaker_similarity(audio_path, reference_path)

print(f"Sample ID: {sample_id}")
print(f"Speaker similarity to reference: {result['similarity']}")
