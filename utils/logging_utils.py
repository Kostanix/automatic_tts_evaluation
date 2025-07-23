import logging

def setup_logging(level_str):
    """
    Configures Python logging with the given verbosity level.

    Args:
        level_str (str): Logging level as string ("DEBUG", "INFO", "WARNING", "ERROR").

    Returns:
        None
    """
    level = getattr(logging, level_str.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
