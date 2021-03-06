from flask import Flask
from flask import request, redirect, url_for, render_template, jsonify
from pymongo import MongoClient, errors
from bson.json_util import dumps
import json

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.exam_surveillance
try:
    x = dumps(db.statss.find_one())
    print("\n * Database connection successfull\n")
except:
    print("\n -> Database connection failed !!\n")

@app.route('/')
def index():
    return "<h1>INDEX PAGE</h1>"


@app.route('/surveillance', methods=['GET', 'POST', 'PUT'])
def surveillance():
    if request.method == 'GET':
        dataa = dumps(db.statss.find())
        dataa = json.loads(dataa)
        return render_template('index.html', value=dataa)

    if request.method == 'POST':
        # new_record = {
        #     "name": "rohan",
        #     "moved": 233,
        #     "talked": 12
        # }
        # print(request.data)
        new_record = request.json
        foo = db.statss.insert_one(new_record).inserted_id
        return "inserted"

    if request.method == 'PUT':
        mod = dict(request.json)
        key = {"name": mod["name"]}
        mod.pop("name")
        foo = db.statss.update_one(key, {"$set": mod})
        return "updated"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
