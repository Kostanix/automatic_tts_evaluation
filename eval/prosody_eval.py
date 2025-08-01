import parselmouth
import os
import json

from typing import Dict


def evaluate_prosody(audio_path: str, metadata_path: str) ->Dict[str, float]:
    """
    Extracts prosodic features from an audio file using Parselmouth (Praat).

    Args:
        audio_path (str): Path to the WAV audio file to analyze.
        metadata_path (str): Path to the JSON metadata file containing the reference text under key "text".

    Returns:
        dict: A dictionary containing rounded prosodic feature values:
            {
                "f0_mean": float,
                "f0_std": float,
                "duration": float,
                "speech_rate": float
            }
    """

    # Load metadata (for reference text)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        reference_text = metadata.get("text", "")

    # Load the audio file
    snd = parselmouth.Sound(audio_path)

    # Extract pitch and duration
    pitch = snd.to_pitch()
    duration = snd.get_total_duration()

    # Filter pitch values to exclude unvoiced frames
    f0_values = pitch.selected_array['frequency']
    f0_values = f0_values[f0_values > 0]  # ignore unvoiced parts

    f0_mean = float(f0_values.mean()) if len(f0_values) > 0 else 0.0
    f0_std = float(f0_values.std()) if len(f0_values) > 0 else 0.0

    # Count words in text for speech rate
    word_count = len(reference_text.split())
    speech_rate = word_count / duration if duration > 0 else 0.0

    return {
        "f0_mean": round(f0_mean, 2),
        "f0_std": round(f0_std, 2),
        "duration": round(duration, 2),
        "speech_rate": round(speech_rate, 2),
    }
