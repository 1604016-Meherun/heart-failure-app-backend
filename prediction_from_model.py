from flask import Flask
from flask.globals import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import joblib, sklearn
import pandas as pd



app = Flask(__name__)
app.secret_key = 'secretkey'
app.config["MONGO_URI"] = "mongodb://localhost:27017/heartfailureapp"
mongo = PyMongo(app)


@app.route('/verify',methods=['POST'])
def prediction():
    infile = open('finalizes_model.pkl','rb')
    model = joblib.load(infile)
    json_ = request.json
    query_df = pd.DataFrame([json_])
    prediction = str(model.predict(query_df))
    infile.close()
    return jsonify(prediction)


if __name__ == '__main__':
    app.run(debug=True)


