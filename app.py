import json

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World ! "


#
# {"name" : "rakesh",
# "image_id" : "12345"}
#

subscription_key = '3a3dc2d9522241f497a1fe2311f8d16a'

face_api_url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&recognitionModel=recognition_02&returnRecognitionModel=false&detectionModel=detection_01'

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get('name')
    image_id = data.get('image_id')
    print("name : ", name, "  & image_id : ", image_id, " & data : ", data)
    value = {"Status ": 200, "Message ": "Success"}
    return jsonify(value)

@app.route("/journey", methods=["POST"])
def journey():
    data = request.get_json()
    station = data.get('station')
    image_id = data.get('image_id')

    print("station : ", station, "  & image_id : ", image_id, " & data : ", data)
    data = open('pig.jpeg', "rb").read()

    response = requests.post(face_api_url, params=params, headers=headers, data=data)
    print("faceId response", response.text)
    if (response.text == []):
        return "Face not detected", 400
    else:
        face = json.loads(response.text)
        face_Id = face[0]["faceId"]

        face_identify_url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/identify'
        request_data = {
            "personGroupId": "group01",
            "faceIds": [
                face_Id
            ],
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.7
        }

        identify_headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

        identify_response = requests.post(face_identify_url, headers=identify_headers, data=json.dumps(request_data))
        print(identify_response.text)

        identify_face = json.loads(identify_response.text)
        candidate = identify_face[0]["candidates"]
        if (candidate == []):
            return "Existing user not found", 400
        else:
            return "Face detected", 200

    # value = {"Status ": 20000, "Message ": "Station abc"}
    # return jsonify(value)


if __name__ == "__main__":
    app.run(port=2000, debug=True)
