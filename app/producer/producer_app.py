from flask import Flask, render_template, jsonify
import redis
from config.settings import REDIS_HOST, REDIS_PORT, setup_logger

app = Flask(__name__)
logger = setup_logger()

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Stream names as defined in producer.py
STREAM_NAMES = {
    'starters': 'stream:starters',
    'mains': 'stream:mains',
    'desserts': 'stream:desserts'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_dishes')
def get_dishes():
    dishes = []
    # Fetch last 10 entries from each stream
    for name, stream in STREAM_NAMES.items():
        last_entries = redis_client.xrevrange(stream, count=10)
        for entry in last_entries:
            dish_info = entry[1]  # entry[1] contains the field-value pairs
            dish_name = dish_info.get(b'name', b'').decode('utf-8')
            prep_time = dish_info.get(b'prep_time', b'').decode('utf-8')
            dishes.append(f"{dish_name} ({prep_time} seconds)")
            #logger.info(f"Retrieved dish: {dish_name} ({prep_time} seconds)")
    return jsonify(dishes)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
