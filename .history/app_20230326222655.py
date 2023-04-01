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

with open("secrets.json") as f:
    secrets = json.load(f)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("classify", filename=filename))
    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/classify/<filename>")
def classify(filename):
    # Perform image classification here
  

    API_URL = "https://api-inference.huggingface.co/models/therealcyberlord/bigcatvit"
    headers = {"Authorization": f"Bearer {}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("cats.jpg")


if __name__ == "__main__":
    app.run(debug=True)
