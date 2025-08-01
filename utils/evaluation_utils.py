import os
import json
import logging
from typing import Dict, Set, Any


from eval.intelligibility_eval import evaluate_intelligibility
from eval.speaker_similarity_eval import evaluate_speaker_similarity
from eval.prosody_eval import evaluate_prosody
from eval.mos_eval import evaluate_mos


def run_evaluations(
    sample_id: str,
    base_path: str,
    enabled_metrics: Set[str],
    whisper_model: Any
) -> Dict[str, Any]:
    """
    Runs all enabled evaluation metrics for a given sample folder.

    Args:
        sample_id (str): Unique identifier for the sample (used in logging).
        base_path (str): Path to the sample directory containing 'audio.wav', 'metadata.json', and optionally 'reference.wav'.
        enabled_metrics (Set[str]): Set of metric names to run (e.g., {"intelligibility", "mos"}).
        whisper_model (Any): A preloaded Whisper model instance for transcription-based evaluations.

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


def _log_missing_reference(sample_id: str) -> None:
    """
    Logs a warning if 'reference.wav' is missing for speaker similarity evaluation.

    Args:
        sample_id (str): The sample identifier (used for logging).
    """
    """
    Logs a warning if reference.wav is missing for speaker similarity evaluation.

    Args:
        sample_id (str): The sample identifier.

    Returns:
        None
    """
    logging.warning(f"[{sample_id}] reference.wav missing – skipping similarity.")
