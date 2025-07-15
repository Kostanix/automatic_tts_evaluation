import warnings

# Suppress specific deprecation warning from torch
warnings.filterwarnings(
    "ignore",
    message="`torch.nn.utils.weight_norm` is deprecated",
    category=FutureWarning
)

import torch
import torchaudio

def evaluate_mos(audio_path: str) -> dict:
    """
    Predict MOS (speech quality score) using UTMOS model via SpeechMOS (torch.hub).
    """

    # Load pretrained UTMOS model once via torch.hub
    model = torch.hub.load("tarepan/SpeechMOS", "utmos22_strong", trust_repo=True)

    # Load and resample audio
    wav, sr = torchaudio.load(audio_path)

    # Ensure mono
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)

    # Run model prediction
    with torch.no_grad():
        score = model(wav, sr=sr)[0].item()

    return {"mos_score": score}
