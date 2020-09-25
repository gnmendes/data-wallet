from flask import Flask

app = Flask(__name__)


@app.route('introduce_data', method=['POST'])
def create_something():
    return None
