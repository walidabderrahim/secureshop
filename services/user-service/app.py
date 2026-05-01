from flask import Flask, request, jsonify
import sqlite3, bcrypt, jwt, os
from datetime import datetime, timedelta

app = Flask(__name__)
JWT_SECRET = os.environ.get("JWT_SECRET", "changeme_in_production")

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            role     TEXT    DEFAULT 'user'
        )
    """)
    conn.commit()
    return conn

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password required"}), 400
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
    try:
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (data["username"], hashed))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    return jsonify({"message": "User created"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "username and password required"}), 400
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?",
                      (data["username"],)).fetchone()
    if user and bcrypt.checkpw(data["password"].encode(), user[2]):
        token = jwt.encode({
            "user_id": user[0],
            "username": user[1],
            "role": user[3],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/profile/<int:user_id>")
def profile(user_id):
    db = get_db()
    user = db.execute("SELECT id, username, role FROM users WHERE id = ?",
                      (user_id,)).fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user[0], "username": user[1], "role": user[2]})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "user-service"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
