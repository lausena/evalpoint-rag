import logging
import os

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger("researchengine_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler('logs/researchengine.log', mode='a')
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(file_handler)