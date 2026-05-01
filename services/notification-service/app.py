from flask import Flask, jsonify, request
from datetime import datetime
app = Flask(__name__)
notifications = []

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    if not data or not data.get("to") or not data.get("subject"):
        return jsonify({"error": "to and subject required"}), 400
    notif = {
        "id": len(notifications) + 1, "to": data.get("to"),
        "subject": data.get("subject"), "body": data.get("body", ""),
        "type": data.get("type", "email"), "status": "sent",
        "created_at": datetime.utcnow().isoformat()
    }
    notifications.append(notif)
    return jsonify(notif), 201

@app.route("/notifications")
def list_notifications():
    return jsonify(notifications)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "notification-service"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8005)
