# util_helpers.py

import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger.

    Parameters:
        name (str): Name of the logger.
        log_file (str): File to write logs to.
        level (int): Logging level.
    
    Returns:
        logging.Logger: Configured logger.
    """
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger
