import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger that writes to file and console."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
