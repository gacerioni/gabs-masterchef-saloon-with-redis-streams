import os
import redis
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from app.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, setup_logger

logger = setup_logger()
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
consumer_name = os.getenv("CONSUMER_NAME")
if not consumer_name:
    logger.error("CONSUMER_NAME environment variable not set.")
    exit(1)  # Exit if no consumer name is specified

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
GROUP_NAME = "waiters"


@app.route('/')
def index():
    return render_template('index.html', consumer_name=consumer_name)


@app.route('/messages')
def messages():
    messages = get_consumer_messages(consumer_name)
    logger.info(f"Consumer {consumer_name} fetched {len(messages)} messages")
    return jsonify(messages)


def get_consumer_messages(consumer_name):
    # Fetch messages specifically for this consumer from Redis
    messages = []
    for stream in ['stream:starters', 'stream:mains', 'stream:desserts']:
        try:
            entries = redis_client.xreadgroup(GROUP_NAME, consumer_name, {stream: '>'}, count=10, block=1000)
            for entry in entries:
                for message_id, message in entry[1]:
                    message_data = {
                        'id': message_id,
                        'dish': message[b'name'].decode('utf-8'),
                        'prep_time': message[b'prep_time'].decode('utf-8')
                    }
                    messages.append(message_data)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis error: {e}")
    return messages


if __name__ == '__main__':
    app.run(debug=True, port=5001)
