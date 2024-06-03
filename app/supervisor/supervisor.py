import os
import sys

import redis
import time
# This computes the absolute path to the root of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from app.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, setup_logger

# Setup logger
logger = setup_logger()

# Environment variables for group and stream names
GROUP_NAME = 'waiters'
STREAM_NAMES = {
    'starters': 'stream:starters',
    'mains': 'stream:mains',
    'desserts': 'stream:desserts'
}


class Supervisor:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def claim_stale_messages(self, min_idle_time):
        """Claim messages that have not been acknowledged yet."""
        for stream in STREAM_NAMES.values():
            try:
                # Get the pending messages for the consumer group
                pending_messages = self.client.xpending_range(stream, GROUP_NAME, '-', '+', count=10)
                print(pending_messages)
            except Exception as e:
                logger.error(f"Error claiming messages: {e}")

    def run(self):
        while True:
            # Check every 10 seconds for messages idle for more than 6 seconds (6000 milliseconds)
            self.claim_stale_messages(6000)
            time.sleep(10)


if __name__ == "__main__":
    supervisor = Supervisor()
    supervisor.run()
