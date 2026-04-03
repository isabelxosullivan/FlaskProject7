from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Dog API App</h1>
    <p><a href="/dog">See dog image</a></p>
    <p><a href="/health">Health check</a></p>
    """

@app.route("/dog")
def get_dog():
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {
        "x-api-key": os.getenv("API_KEY")
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    image_url = data[0]["url"]

    return f"""
    <h1>Random Dog</h1>
    <img src="{image_url}" style="max-width:500px;">
    <p><a href="/dog">Another dog</a></p>
    """

@app.route("/health")
def health():
    return jsonify({"status": "ok"})