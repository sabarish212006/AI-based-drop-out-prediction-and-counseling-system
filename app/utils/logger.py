"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: logger.py
Purpose: Centralized logging configuration
Author: Project Team
----------------------------------------------------------
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger instance.

    Parameters:
        name (str): Logger name

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)

    log_file = os.path.join(log_directory, "app.log")

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,      # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger


# Default application logger
app_logger = get_logger("Dropoutdropout_predictionsystem")