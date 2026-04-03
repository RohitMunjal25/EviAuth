import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from flask_bcrypt import Bcrypt
from backendstore import UPLOAD_FOLDER
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

load_dotenv()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MONGO_URI = os.getenv("MONGO_URL")

if not MONGO_URI:
    raise Exception(" MONGO_URL not set")

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

casia_model = None
genai_model = None
audio_model = None

def load_models_if_needed():
    global casia_model, genai_model, audio_model
    from model_downloader import ensure_models_exist
    ensure_models_exist()

    if casia_model is None:
        from models.casiaimage import detect_casia_fake
        casia_model = detect_casia_fake

    if genai_model is None:
        from models.cifakeimage import detect_ai_generated
        genai_model = detect_ai_generated

    if audio_model is None:
        from models.audiospoof import detect_audio_spoof
        audio_model = detect_audio_spoof
@app.route("/health")
def health():
    return {"status": "alive", "message": "Backend is running"}, 200

@app.route("/register", methods=["POST"])
def register():
    if users_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    password = data.get("pass") or data.get("password")

    if not password:
        return jsonify({"error": "Password missing"}), 400

    if users_collection.find_one({"email": data['email']}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

    users_collection.insert_one({
        "name": data['name'],
        "email": data['email'],
        "password": hashed_pass
    })

    return jsonify({"message": "Account created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    if users_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("pass") or data.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password missing"}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.check_password_hash(user['password'], password):
        return jsonify({
            "name": user['name'],
            "email": user['email'],
            "status": "success"
        }), 200

    return jsonify({"error": "Invalid password"}), 401

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    user_email = request.form.get("email")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        file.save(path)
        ext = file.filename.split(".")[-1].lower()

        load_models_if_needed()

        result = {}

        if ext in ["jpg", "jpeg", "png"]:
            casia_res = casia_model(path)
            genai_res = genai_model(path)

            result = {
                "cnn_score": casia_res.get("fake_probability", 0),
                "genai_score": genai_res.get("genai_score", 0)
            }

        elif ext in ["mp3", "wav"]:
            audio_res = audio_model(path)
            result = audio_res

        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
