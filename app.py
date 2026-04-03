import os
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DOG_API_KEY = os.getenv("DOG_API_KEY")
DOG_API_URL = "https://api.thedogapi.com/v1/images/search"

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE")
    )
    return conn

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dog/view")
def dog_view():
    fresh_dog = None
    try:
        headers = {"x-api-key": DOG_API_KEY}
        response = requests.get(DOG_API_URL, headers=headers)
        data = response.json()
        if data:
            fresh_dog = data[0]["url"]
    except Exception:
        fresh_dog = None

    dogs = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT image_url, created_at FROM dogs ORDER BY created_at DESC")
        dogs = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        pass

    return render_template("dog.html", dogs=dogs, fresh_dog=fresh_dog)

@app.route("/dogs")
def dogs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT image_url, created_at FROM dogs ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("saved_dogs.html", dogs=rows)
    except Exception as e:
        return render_template("saved_dogs.html", dogs=[]), 200

@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        db_status = "ok"
        return render_template("health.html", db_status=db_status), 200
    except Exception as e:
        return render_template("health.html", db_status=str(e)), 500
@app.route("/status")
def status():
    db_status = "unknown"
    dog_count = 0
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM dogs;")
        dog_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = str(e)
    return render_template("status.html", db_status=db_status, dog_count=dog_count)

from flask import Flask, render_template, request, jsonify, redirect, url_for

@app.route("/dog/save", methods=["POST"])
def dog_save():
    try:
        image_url = request.form.get("image_url")
        if not image_url:
            return jsonify({"error": "No image_url provided"}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO dogs (image_url) VALUES (%s);", (image_url,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("dogs"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)

