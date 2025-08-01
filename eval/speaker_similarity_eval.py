from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine
from typing import Dict, Optional


def evaluate_speaker_similarity(sample_path: str, reference_path: str) -> Dict[str, Optional[float]]:
    """
    Evaluates speaker similarity between a synthetic sample and a reference audio
    using speaker embeddings and cosine similarity.
    Args:
        sample_path (str): Path to the synthetic or test audio file (WAV format).
        reference_path (str): Path to the reference audio file representing the target voice.

    Returns:
        dict: Dictionary containing the cosine similarity between the embeddings under the key "similarity".
              Returns {"similarity": None} if the evaluation fails.
              Example: {"similarity": 0.8723}
    """
    try:
        # Load and preprocess the sample and reference audio files
        wav_sample = preprocess_wav(sample_path)
        wav_reference = preprocess_wav(reference_path)

        # Generate speaker embeddings
        encoder = VoiceEncoder()
        emb_sample = encoder.embed_utterance(wav_sample)
        emb_reference = encoder.embed_utterance(wav_reference)

        # Compute cosine similarity (1 - distance)
        similarity = 1 - cosine(emb_sample, emb_reference)

        return {
            "similarity": round(similarity, 4)
        }

    except Exception as e:
        print(f"[ERROR] Speaker similarity evaluation failed: {e}")
        return {"similarity": None}
