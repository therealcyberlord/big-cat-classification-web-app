from flask import Flask

app = Flask(__main__)


@app.route("/")
def home():
    return "Hello world"


if __name__ == "__main__":
    app.run()
