import os
import json
import logging

from eval.intelligibility_eval import evaluate_intelligibility
from eval.speaker_similarity_eval import evaluate_speaker_similarity
from eval.prosody_eval import evaluate_prosody
from eval.mos_eval import evaluate_mos


def run_evaluations(sample_id, base_path, enabled_metrics, whisper_model):
    """
    Runs all enabled evaluation metrics for a given sample folder.

    Args:
        sample_id (str): The sample identifier.
        base_path (str): Path to the sample folder.
        enabled_metrics (set): Set of enabled metric names.
        whisper_model

    Returns:
        dict: Dictionary containing metric results.
    """
    result = {}

    audio_path = os.path.join(base_path, "audio.wav")
    metadata_path = os.path.join(base_path, "metadata.json")
    reference_path = os.path.join(base_path, "reference.wav")

    reference_text = ""
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                reference_text = metadata.get("text", "")
        except Exception as e:
            logging.warning(f"[{sample_id}] Failed to load metadata text: {e}")

    metric_dispatch = {
        "intelligibility": lambda: evaluate_intelligibility(
            audio_path,
            reference_text,
            whisper_model,
            metadata.get("language") if 'metadata' in locals() else None
        ),
        "prosody": lambda: evaluate_prosody(audio_path, metadata_path),
        "similarity": lambda: evaluate_speaker_similarity(audio_path, reference_path)
        if os.path.exists(reference_path)
        else (_log_missing_reference(sample_id), {}),
        "mos": lambda: evaluate_mos(audio_path)
    }

    for metric in enabled_metrics:
        if metric not in metric_dispatch:
            logging.warning(f"[{sample_id}] Unknown metric '{metric}' – skipping.")
            continue

        try:
            result.update(metric_dispatch[metric]())
        except Exception as e:
            logging.warning(f"[{sample_id}] {metric} failed: {e}")

    return result


def _log_missing_reference(sample_id):
    """
    Logs a warning if reference.wav is missing for speaker similarity evaluation.

    Args:
        sample_id (str): The sample identifier.

    Returns:
        None
    """
    logging.warning(f"[{sample_id}] reference.wav missing – skipping similarity.")
