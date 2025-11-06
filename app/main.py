from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello from OpenShift CI/CD Pipeline!"


if __name__ == "_main_":
    app.run(host="0.0.0.0", port=8080)

