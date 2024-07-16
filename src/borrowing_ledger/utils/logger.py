import logging
import os
from datetime import datetime

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter('[%(asctime)s]%(lineno)d %(name)s -%(levelname)s -%(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)