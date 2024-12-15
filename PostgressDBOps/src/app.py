from flask import Flask, request, jsonify
from pymongo import MongoClient
from src.routes import api_routes
from urllib.parse import quote

app = Flask(__name__)

# Register routes
app.register_blueprint(api_routes)

@app.route('/')
def home():
    return "Welcome to the Flask REST API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)