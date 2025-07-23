import json

def load_config(path):
    """
    Loads a JSON configuration file from the given path.

    Args:
        path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def merge_args_with_config(args, config):
    """
    Merges CLI arguments with values from the configuration file.
    CLI arguments override config values if provided.

    Args:
        args (argparse.Namespace): Parsed CLI arguments.
        config (dict): Configuration loaded from file.

    Returns:
        dict: Merged configuration dictionary.
    """
    merged = config.copy()
    if args.data_dir:
        merged["data_dir"] = args.data_dir
    if args.results_file:
        merged["results_file"] = args.results_file
    if args.enable:
        merged["enable"] = args.enable
    if args.use_gpu is not None:
        merged["use_gpu"] = args.use_gpu
    if args.log_level:
        merged["log_level"] = args.log_level
    return merged
