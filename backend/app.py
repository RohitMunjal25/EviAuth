import os
import gc
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from flask_bcrypt import Bcrypt
from backendstore import UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

load_dotenv()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MONGO_URI = os.getenv("MONGO_URL")

if not MONGO_URI:
    raise Exception("MONGO_URL not set")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.server_info()
    print("MongoDB Connected")

    db = client["digital_forensics"]
    users_collection = db["users"]
    history_collection = db["history"]

except Exception as e:
    print("MongoDB Connection Failed:", e)
    users_collection = None
    history_collection = None

@app.route("/health")
def health():
    return {"status": "alive"}, 200

@app.route("/register", methods=["POST"])
def register():
    if users_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()

    password = data.get("pass") or data.get("password")

    if users_collection.find_one({"email": data['email']}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

    users_collection.insert_one({
        "name": data['name'],
        "email": data['email'],
        "password": hashed_pass,
        "created_at": datetime.now()
    })

    return jsonify({"message": "Account created"}), 201

@app.route("/login", methods=["POST"])
def login():
    if users_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()

    email = data.get("email")
    password = data.get("pass") or data.get("password")

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.check_password_hash(user['password'], password):
        return jsonify({
            "name": user['name'],
            "email": user['email']
        }), 200

    return jsonify({"error": "Invalid password"}), 401

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        file.save(path)
        ext = file.filename.split(".")[-1].lower()

        result = {}

        if ext in ["jpg", "jpeg", "png"]:
            from models.casiaimage import detect_casia_fake
            from models.cifakeimage import detect_ai_generated

            casia_res = detect_casia_fake(path)
            genai_res = detect_ai_generated(path)

            score = max(
                casia_res.get("fake_probability", 0),
                genai_res.get("genai_score", 0)
            )

            result = {
                "report": {
                    "authenticity_status": "Fake" if score > 0.5 else "Real",
                    "manipulation_probability": score
                }
            }

            del detect_casia_fake
            del detect_ai_generated
            gc.collect()

        elif ext in ["mp3", "wav"]:
            from models.audiospoof import detect_audio_spoof

            audio_res = detect_audio_spoof(path)

            result = {
                "report": {
                    "authenticity_status": audio_res.get("label", "Unknown"),
                    "manipulation_probability": audio_res.get("score", 0)
                }
            }

            del detect_audio_spoof
            gc.collect()

        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)