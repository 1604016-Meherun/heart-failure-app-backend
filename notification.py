from flask import Flask
from flask.globals import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, json
import joblib, sklearn
import pandas as pd
import requests
import json


app = Flask(__name__)

@app.route('/notification',methods=['POST'])
def send_fcm_with_rest():
    _json = request.json
    token = _json['token']
    post_data = {
        "to": token,
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
    print("response : ",type(_r))
    result = []
    result={'output':_r}
    rs = _r.text.encode('utf8')
    print(rs)
    print(type(rs))
    jd = json.loads(rs)
    print(jd)
    return jd
 
#   return Response(result)

# @app.route('/notification',methods=['POST'])
# def rest():
#     _json = request.json
#     _token = 'faIvvs3oR56QG7eI53HM0S:APA91bH51njCUJPe_IEMz23LFwr1tEkGPNlTO0ald6vzK78BK5qS9O-Alvvw__Ccf_6l4bPWHiG73oqwJFfkYHKihA3aaHUOdXcl0MrDMEnbJlGXUnHzHRWsVuFMM0PvylB1Zh2tIdST'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'key=AAAAUEDzIwk:APA91bHLlCwtuw3c7AvWH6vlnbUnVT7pGqaPSU5fGLitH-xE8ECqzDLQoGjfYAiEsPVYj7CKPwifFkl5Gd1vwEQCsZ1cm8szlW12ZtFxHylBq_j_e4Z3K3cAzSh8YgMz6M0z5MlUIs44',
#         'Content-Type': 'application/json'
#     }
#     url = 'https://fcm.googleapis.com/fcm/send'
#     if type(_token) is list:
#         payload = {
#             "registration_ids": _token,
#             "collapse_key": "type_a",
#             "data": {
#                         "status": True,
#                         "prediction": '1'
#                     }
#         }
#     else:
#         payload = {
#             "to": _token,
#             "collapse_key": "type_a",
#             "data": {
#                         "status": True,
#                         "prediction": '1'
#                     }
#         }
#     #print(json.dumps(payload))
#     resp = requests.post(url, headers=headers, data=json.dumps(payload))

#     #print(resp.text.encode('utf8'), flush=True)
#     return jsonify('ok')




if __name__ == '__main__':
    app.run(debug=True)

