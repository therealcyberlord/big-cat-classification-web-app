from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
import os
import requests
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "uploads"
)
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
with open("secrets.json") as f:
    secrets = json.load(f)


def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        file = request.files.get("image")
        if not file or file.filename == "":
            return redirect(request.url)
        if allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("classify", filename=filename))
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/classify/<filename>")
def classify(filename):
    API_URL = "https://api-inference.huggingface.co/models/therealcyberlord/bigcatvit"
    headers = {"Authorization": f"Bearer {secrets['huggingface_key']}"}
    with open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data, json=True)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
