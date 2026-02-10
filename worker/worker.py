import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Worker has started and waiting for jobs")

while True:
    time.sleep(10)
