"""
Logging configuration for the security platform
Place this in: backend/app/logging_config.py
"""

import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Setup logging configuration"""
    logger = logging.getLogger("security_platform")
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Threat-specific logger
threat_logger = logging.getLogger("threats")
threat_handler = logging.handlers.RotatingFileHandler(
    LOGS_DIR / "threats.log",
    maxBytes=10485760,
    backupCount=20
)
threat_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
threat_logger.addHandler(threat_handler)

# Detection-specific logger
detection_logger = logging.getLogger("detection")
detection_handler = logging.handlers.RotatingFileHandler(
    LOGS_DIR / "detection.log",
    maxBytes=10485760,
    backupCount=20
)
detection_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
detection_logger.addHandler(detection_handler)
