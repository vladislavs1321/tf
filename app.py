import time

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

import redis
from flask import Flask, request, jsonify, Response, render_template

from pprint import pprint

import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



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

    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    train_images.shape          

    foo = len(train_labels)

    plt.figure()
    plt.imshow(train_images[0])
    plt.colorbar()
    plt.grid(False)

    return format(foo)

@app.route('/api', methods=['GET'])
def api():

    input_data = request.json
    output_data = []
    response = jsonify(pprint(locals()))
    return response

@app.route('/plot', methods=['GET'])
def plot():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("static/plot.png")
    
    return render_template('/plot.html', url = '/static/plot.png')
 


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)