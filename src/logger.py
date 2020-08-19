import sys
import logging

from settings import DEBUG

def setup_logger():
    logger = logging.getLogger('social_credit')
    stdout_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(stdout_handler)
    level = logging.DEBUG if DEBUG else logging.INFO
    logger.setLevel(level)