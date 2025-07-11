from eval.prosody_eval import evaluate_prosody
import os

# Define which sample to analyze
sample_id = "sample_001"
sample_dir = os.path.join("../data", sample_id)

# Define paths to audio and metadata
audio_path = os.path.join(sample_dir, "audio.wav")
metadata_path = os.path.join(sample_dir, "metadata.json")

# Run evaluation
result = evaluate_prosody(audio_path, metadata_path)

# Display results
print(f"Sample ID: {sample_id}")
print(f"F0 Mean: {result['f0_mean']} Hz")
print(f"F0 Std: {result['f0_std']} Hz")
print(f"Duration: {result['duration']} seconds")
print(f"Speech Rate: {result['speech_rate']} words/second")
