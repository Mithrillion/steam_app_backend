from flask import Flask
from flask.json import jsonify
import numpy as np
from sklearn.neighbors import BallTree
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={"/query/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return "Nothing Here!"


@app.route('/query/<app_id>')
def query(app_id):
    try:
        loc = id_to_loc[int(app_id)]
    except KeyError:
        return jsonify([])
    dist, ind = tree.query([codes[loc]], k=40)
    dist = np.ravel(dist)
    ind = np.ravel(ind)
    results = pd.DataFrame({"distance": dist, "loc": ind, "app_id": ids[ind].astype(np.int64)})
    joined = pd.merge(left=results, right=ratings, on="app_id").sort_values("distance")
    return joined.to_json(orient='records')


if __name__ == '__main__':
    ids = np.ravel(np.load("./server_data/ids_arr.npy"))
    id_to_loc = {int(i): l for i, l in zip(ids, range(len(ids)))}
    codes = np.load("./server_data/codes_arr.npy")
    ratings = pd.read_csv("./server_data/ratings.csv")
    tree = BallTree(codes)
    app.run()
