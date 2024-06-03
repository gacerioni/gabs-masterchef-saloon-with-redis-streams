import redis
import sys
import os
import random
from time import sleep
# This computes the absolute path to the root of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from app.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, setup_logger

# Setup logger
logger = setup_logger()

# Environment variables for group and stream names
GROUP_NAME = os.getenv('REDIS_GROUP_NAME', 'waiters')
STREAM_NAMES = {
    'starters': 'stream:starters',
    'mains': 'stream:mains',
    'desserts': 'stream:desserts'
}


def process_message(stream, message_id, message):
    # Decode byte strings to UTF-8 (or your preferred encoding)
    dish_name = message[b'name'].decode('utf-8')
    prep_time = message[b'prep_time'].decode('utf-8')

    # Now you can log or use these as normal strings
    logger.info(f"Processing dish {dish_name} from {stream} with ID {message_id} and prep time {prep_time} seconds")


class Waiter:
    def __init__(self, consumer_name):
        self.consumer_name = consumer_name
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        self.ensure_groups_exist()

    def ensure_groups_exist(self):
        for stream in STREAM_NAMES.values():
            try:
                self.client.xgroup_create(stream, GROUP_NAME, '$', mkstream=True)
            except redis.exceptions.ResponseError:
                logger.info(f"Group {GROUP_NAME} already exists for stream {stream}")

    def run(self):
        while True:
            try:
                streams = {stream: '>' for stream in STREAM_NAMES.values()}
                results = self.client.xreadgroup(GROUP_NAME, self.consumer_name, streams, count=1, block=1000)
                if results:
                    for stream, messages in results:
                        for message_id, message in messages:
                            # Simulate processing delay
                            delay = random.uniform(0.1, 2)
                            sleep(delay)
                            process_message(stream, message_id, message)
                            # Decide randomly whether to acknowledge the message
                            if random.random() < 0.9:
                                self.client.xack(stream, GROUP_NAME, message_id)
                                logger.info(f"Message {message_id} acknowledged.")
                            else:
                                logger.warning(f"Forgot to acknowledge message {message_id} from {stream}")
            except redis.exceptions.ConnectionError:
                logger.error("Connection error encountered, trying to reconnect...")
                sleep(5)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        waiter = Waiter(consumer_name=sys.argv[1])
        waiter.run()
    else:
        logger.error("Consumer name not provided. Please restart with a consumer name.")
        sys.exit(1)
