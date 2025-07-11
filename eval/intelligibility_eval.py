import os

import whisper
from jiwer import wer, cer

model = whisper.load_model("base")

def evaluate_intelligibility(audio_path, reference_text):
    try:
        print(f"📄 Transkription von: {audio_path}")
        print("📁 Existiert Datei?", os.path.exists(audio_path))
        # Whisper-transcription
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
        print(f"[ERROR] intelligibility_eval failed: {e}")
        return {
            "wer": None,
            "cer": None
        }