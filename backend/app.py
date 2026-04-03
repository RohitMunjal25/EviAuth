import os
import gc
import uuid
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

client = MongoClient(MONGO_URI)
db = client["digital_forensics"]
users_collection = db["users"]
history_collection = db["history"]


@app.route("/health")
def health():
    return {"status": "alive"}, 200


@app.route("/register", methods=["POST"])
def register():
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
    email = request.form.get("email")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    import uuid
    filename = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(path)
        ext = file.filename.split(".")[-1].lower()

        from exiftool import extract_metadata
        metadata = extract_metadata(path)

        from report import generate_report

        # IMAGE ANALYSIS
        if ext in ["jpg", "jpeg", "png"]:
            from models.casiaimage import detect_casia_fake
            from models.cifakeimage import detect_ai_generated

            casia_res = detect_casia_fake(path)
            genai_res = detect_ai_generated(path)

            print("CASIA RAW:", casia_res)
            print("GENAI RAW:", genai_res)

            # FIX: Properly extracting the scores using the correct keys
            casia_score = casia_res.get("casia_score", 0) if isinstance(casia_res, dict) else 0
            genai_score = genai_res.get("genai_score", 0) if isinstance(genai_res, dict) else 0

            report = generate_report(
                metadata=metadata,
                image_forensics={
                    "cnn_score": float(casia_score),
                    "genai_score": float(genai_score),
                    "is_pdf": False
                },
                filename=file.filename
            )

            del detect_casia_fake
            del detect_ai_generated
            gc.collect()

        # DOCUMENT (PDF) ANALYSIS
        elif ext == "pdf":
            from models.midv500 import detect_document_fake
            
            doc_res = detect_document_fake(path)
            print("DOC RAW:", doc_res)
            
            doc_score = doc_res.get("doc_score", 0) if isinstance(doc_res, dict) else 0

            report = generate_report(
                metadata=metadata,
                image_forensics={
                    "cnn_score": float(doc_score),
                    "is_pdf": True
                },
                filename=file.filename
            )

            del detect_document_fake
            gc.collect()

        # AUDIO ANALYSIS
        elif ext in ["mp3", "wav"]:
            from models.audiospoof import detect_audio_spoof

            audio_res = detect_audio_spoof(path)

            report = generate_report(
                metadata=metadata,
                audio_forensics=audio_res,
                filename=file.filename
            )

            del detect_audio_spoof
            gc.collect()

        # VIDEO ANALYSIS
        elif ext in ["mp4", "mov"]:
            from ffmpeg import run_video_forensics

            video_res = run_video_forensics(path)

            report = generate_report(
                metadata=video_res.get("metadata", {}),
                video_forensics=video_res,
                filename=file.filename
            )

            gc.collect()

        else:
            return jsonify({"error": "Unsupported file type"}), 400

        result = {"report": report}

        if history_collection is not None:
            history_collection.insert_one({
                "email": email,
                "file_name": file.filename,
                "result": result,
                "created_at": datetime.now()
            })

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)