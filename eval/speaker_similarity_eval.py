from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine

def evaluate_speaker_similarity(sample_path: str, reference_path: str) -> dict:
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
