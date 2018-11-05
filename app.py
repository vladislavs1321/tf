import time
import tensorflow as tf
import redis
from flask import Flask, request, jsonify

from pprint import pprint




app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    foo = tf.VERSION
    return format(foo)

@app.route('/api', methods=['GET'])
def api():

    input_data = request.json
    output_data = []
    response = jsonify(pprint(locals()))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)