from flask import Flask, render_template, url_for, redirect, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World ! "

#
# {"name" : "rakesh",
# "image_id" : "12345"}
#


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get('name')
    image_id = data.get('image_id')

    print("name : ", name, "  & image_id : ", image_id, " & data : ", data)
    value = {"Status ": 200, "Message ": "Success"}
    return jsonify(value)


if __name__ == "__main__":
    app.run(port=2000, debug=True)
