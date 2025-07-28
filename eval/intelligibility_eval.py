import torch
import logging
import whisper
from jiwer import wer, cer

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)
logging.info(f"Whisper model loaded on device: {device}")

def evaluate_intelligibility(audio_path, reference_text, language=None):
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
