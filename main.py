import os
import csv
import argparse
import logging
import torch
import whisper

from utils.config_utils import load_config, merge_args_with_config
from utils.logging_utils import setup_logging
from utils.evaluation_utils import run_evaluations

DEFAULT_CONFIG_PATH = "config/default.json"

def main() -> None:
    """
    Main entry point for the evaluation pipeline.

    - Parses command-line arguments.
    - Loads and merges configuration settings.
    - Discovers sample folders and metadata.
    - Runs selected evaluation metrics (WER, MOS, prosody, similarity) for each sample.
    - Aggregates results and writes them to a CSV file.

    CLI arguments override config file settings if provided.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Automated evaluation of TTS systems")
    parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH, help="Path to configuration file")
    parser.add_argument("--data_dir", type=str, help="Path to input sample directory")
    parser.add_argument("--results_file", type=str, help="Path to output results CSV")
    parser.add_argument("--enable", nargs="+", help="List of metrics to enable (e.g., intelligibility prosody)")
    parser.add_argument("--use_gpu", type=bool, help="Force GPU usage (true/false)")
    parser.add_argument("--log_level", type=str, help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    parser.add_argument(
        "--whisper_model", type=str,help="Whisper model size to use (tiny, base, small, medium, large, turbo)"
    )

    args = parser.parse_args()

    config = load_config(args.config)

    if args.whisper_model:
        config["whisper_model"] = args.whisper_model

    cfg = merge_args_with_config(args, config)

    # Setup logging
    setup_logging(cfg.get("log_level", "INFO"))

    data_dir = cfg["data_dir"]
    results_file = cfg["results_file"]
    enabled_metrics = set(cfg["enable"])

    logging.info(f"Enabled metrics: {enabled_metrics}")
    logging.info(f"Loading samples from '{data_dir}'...")

    # Whisper model initialization
    device = "cuda" if torch.cuda.is_available() else "cpu"
    whisper_model = whisper.load_model(config.get("whisper_model", "medium"), device=device)
    logging.info(f"Whisper model loaded on device: {device}")

    # Discover sample folders
    sample_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    all_metadata_keys = set()

    # Collect all metadata fields across samples
    for sample_id in sample_dirs:
        metadata_path = os.path.join(data_dir, sample_id, "metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = f.read()
                    all_metadata_keys.update(eval(metadata).keys())  # safer: use json.load() if unsure
            except Exception as e:
                logging.warning(f"[{sample_id}] Failed to read metadata: {e}")

    # Build CSV header
    eval_keys = ["sample_id", "wer", "cer", "similarity", "f0_mean", "f0_std", "duration", "speech_rate", "mos_score"]
    header = ["sample_id"] + sorted(all_metadata_keys) + eval_keys[1:]  # avoid duplicate sample_id

    # Evaluate and write results
    with open(results_file, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()

        for sample_id in sample_dirs:
            logging.info(f"Processing sample: {sample_id}")
            base_path = os.path.join(data_dir, sample_id)
            row = {"sample_id": sample_id}

            # Load metadata into row
            metadata_path = os.path.join(base_path, "metadata.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        metadata = f.read()
                        row.update(eval(metadata))  # or use json.load() if stored as JSON
                except Exception as e:
                    logging.warning(f"[{sample_id}] Metadata loading failed: {e}")

            # Run all enabled evaluations for this sample
            eval_results = run_evaluations(sample_id, base_path, enabled_metrics, whisper_model)
            row.update(eval_results)

            # Fill in missing fields (optional but safe)
            for key in header:
                row.setdefault(key, None)

            writer.writerow(row)

    logging.info(f"Evaluation complete. Results saved to '{results_file}'.")

# === Entry point ===
if __name__ == "__main__":
    main()
