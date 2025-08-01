import logging
from typing import Optional, Dict

from jiwer import wer, cer

# Will be set from outside
WHISPER_MODEL_NAME = "medium"

def evaluate_intelligibility(audio_path: str, reference_text: str, model, language: Optional[str] = None) -> Dict[str, Optional[float]]:
    """
    Evaluates the intelligibility of a synthetic speech sample using automatic transcription.

    Args:
        audio_path (str): Path to the audio file to be evaluated.
        reference_text (str): The original reference text corresponding to the audio.
        model: The Whisper model instance used for transcription (e.g. whisper.load_model()).
        language (Optional[str]): ISO 639-1 language code (e.g., 'en' for English). If None, auto-detection is used.

    Returns:
        dict: Dictionary containing the rounded WER and CER scores.
              Returns {"wer": None, "cer": None} if an error occurs.
    """
    try:
        try:
            result = model.transcribe(audio_path, language=language)
        except ValueError as lang_error:
            logging.warning(f"Invalid language '{language}' – falling back to auto-detection. Error: {lang_error}")
            result = model.transcribe(audio_path)

        recognized_text = result["text"]

        # WER & CER calculation
        wer_score = wer(reference_text, recognized_text)
        cer_score = cer(reference_text, recognized_text)

        return {
            "wer": round(wer_score, 3),
            "cer": round(cer_score, 3)
        }

    except Exception as e:
        logging.error(f"intelligibility_eval failed: {e}")
        return {
            "wer": None,
            "cer": None
        }
