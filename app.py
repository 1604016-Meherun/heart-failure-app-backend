from flask import Flask
from flask.globals import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import joblib, sklearn
import pandas as pd
import requests
import json

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config["MONGO_URI"] = "mongodb://localhost:27017/heartfailureapp"
mongo = PyMongo(app)

@app.route('/predict',methods=['POST'])
def predict():
    _json = request.json
    _age = _json['age']
    _anaemia = _json['anaemia']
    _ejection_fraction = _json['ejection_fraction']
    _high_blood_pressure = _json['high_blood_pressure']
    _platelets = _json['platelets']
    _serum_creatinine = _json['serum_creatinine']
    _serum_sodium = _json['serum_sodium']
    _sex = _json['sex']
    _smoking = _json['smoking']
    _time = _json['time']
    print("hello")
    _token = _json['token']


    if request.method == "POST":
        #predicting from model
        infile = open('finalizes_model.pkl','rb')
        model = joblib.load(infile)
        # _json = request.json
        query_df = pd.DataFrame([[_age,_anaemia,_ejection_fraction,_high_blood_pressure,_platelets,_serum_creatinine,_serum_sodium,_sex,_smoking,_time]])
        _prediction = int(model.predict(query_df))
        infile.close()

        #Integrating with fcm
        post_data = {
        "to": _token,
        "priority": "high",
        "data": {
                "experienceId": "@naimur978/heart-failure-prediction",
                "title": "Recieved_Meherun!",
                "message": "Prediction Generated!",
                "data_message": {
                    "status": True,
                    "prediction": '1'
                }
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "key=AAAAUEDzIwk:APA91bHLlCwtuw3c7AvWH6vlnbUnVT7pGqaPSU5fGLitH-xE8ECqzDLQoGjfYAiEsPVYj7CKPwifFkl5Gd1vwEQCsZ1cm8szlW12ZtFxHylBq_j_e4Z3K3cAzSh8YgMz6M0z5MlUIs44"
        }
        _r = requests.post('https://fcm.googleapis.com/fcm/send',
                        data=json.dumps(post_data), headers=headers)
        

        #saving in Mongodb
        id = mongo.db.model_prediction.insert({'age':_age,'anaemia':_anaemia,'ejection_fraction':_ejection_fraction,'high_blood_pressure':_high_blood_pressure,'platelets':_platelets,'serum_creatinine':_serum_creatinine,'serum_sodium':_serum_sodium,'sex':_sex,'smoking':_smoking,'time':_time,'token':_token, 'prediction':_prediction})
        #Collecting from db
        s = mongo.db.model_prediction.find_one({'_id': id })
        output =[]
        output = {'age':s['age'],'anaemia':s['anaemia'],'ejection_fraction':s['ejection_fraction'],'high_blood_pressure':s['high_blood_pressure'],'platelets':s['platelets'],'serum_creatinine':s['serum_creatinine'],'serum_sodium':s['serum_sodium'],'sex':s['sex'],'smoking':s['smoking'],'time':s['time'],'token':s['token'],'prediction':s['prediction']}

        
        #showing result
        return jsonify({'result' : output})
        # resp.status_code = 200
    else:
        return not_found()

        
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404
    return resp



if __name__ == '__main__':
    app.run(debug=True)

