import os
import sys
from dotenv import load_dotenv
import subprocess
from model_downloader import ensure_models_exist

def install_requirements():
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        except:
            pass

install_requirements()
load_dotenv()
ensure_models_exist()

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import time

from models.casiaimage import detect_casia_fake  
from models.cifakeimage import detect_ai_generated 
from models.midv500 import detect_document_fake
from ffmpeg import run_video_forensics
from exiftool import extract_metadata
from report import generate_report
from pydub import AudioSegment
from models.audiospoof import detect_audio_spoof
from backendstore import UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017/forensics_db")

db = None
collection = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client["digital_forensics"]
    collection = db["history"]
except:
    pass

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    video_result = None
    image_result = None  
    audio_result = None  
    metadata = {}
    report = {}

    try:
        file.save(path)
        ext = file.filename.split(".")[-1].lower()

        if ext == "pdf":
            print(" Running Document Forensics (MIDV-500 + ELA)...")
            metadata = extract_metadata(path)
            doc_result = detect_document_fake(path)
            
            image_result = {
                "cnn_score": doc_result.get("doc_score", 0),
                "total_pages": doc_result.get("total_pages", 1),
                "is_pdf": True
            }
            report = generate_report(metadata, image_forensics=image_result, filename=file.filename)

        elif ext in ["jpg", "jpeg", "png", "tiff", "bmp"]:
            print("Running Hybrid Image Forensics (CASIA + GenAI)...")
            metadata = extract_metadata(path)
            
            try:
                casia_res = detect_casia_fake(path)
                tampering_score = casia_res.get("fake_probability", casia_res.get("score", casia_res.get("doc_score", 0)))
            except Exception as e:
                print(f" CASIA Error: {e}")
                tampering_score = 0

            try:
                genai_res = detect_ai_generated(path)
                genai_score = genai_res.get("genai_score", 0)
            except Exception as e:
                print(f"cifake Error: {e}")
                genai_score = 0
            
            image_result = {
                "cnn_score": tampering_score,
                "genai_score": genai_score,
                "is_pdf": False
            }
            report = generate_report(metadata, image_forensics=image_result, filename=file.filename)

        elif ext in ["mp4", "mov", "avi", "mkv"]:
            print("🎥 Running Video Forensics...")
            video_result = run_video_forensics(path)
            metadata = video_result.get("metadata", {})
            report = generate_report(metadata, video_forensics=video_result, filename=file.filename)
        
        elif ext in ["mp3", "wav", "m4a", "flac", "ogg", "aac"]:
            print(f"🎙️ Processing Audio File: {file.filename}")
            
            wav_filename = f"{file.filename.split('.')[0]}_converted.wav"
            wav_path = os.path.join(UPLOAD_FOLDER, wav_filename)
            
            try:
                audio = AudioSegment.from_file(path)
                audio = audio.set_frame_rate(16000).set_channels(1)
                audio.export(wav_path, format="wav")
                print(f"Converted to WAV: {wav_filename}")
            except Exception as e:
                return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 400

            metadata = extract_metadata(path)
            audio_result = detect_audio_spoof(wav_path)
            
            report = generate_report(metadata, audio_forensics=audio_result, filename=file.filename)
            
            if os.path.exists(wav_path): os.remove(wav_path)

        else:
            return jsonify({"error": "Unsupported file type"}), 400

        data = {
            "filename": file.filename,
            "time": datetime.now(),
            "metadata": make_json_safe(metadata),
            "video_forensics": video_result,
            "image_forensics": image_result,
            "audio_forensics": audio_result,  
            "report": report
        }
        
        inserted_id = "not_saved_to_db"
        if collection is not None:
            inserted = collection.insert_one(data)
            inserted_id = str(inserted.inserted_id)
            
        return jsonify({"id": inserted_id, "report": report})

    except Exception as e:
        print(f" Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(path): os.remove(path)

@app.route("/report/<id>", methods=["GET"])
def get_report(id):
    if collection is None:
        return jsonify({"error": "Database not connected"}), 503
    try:
        data = collection.find_one({"_id": ObjectId(id)})
        if data:
            data["_id"] = str(data["_id"])
            return jsonify(data)
        return jsonify({"error": "Report not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route("/history", methods=["GET"])
def history():
    if collection is None:
        return jsonify([])
    data = list(collection.find())
    for d in data:
        d["_id"] = str(d["_id"])
    return jsonify(data)

@app.route("/health")
def health():
    return {"status": "alive", "message": "Backend is running "}, 200

def make_json_safe(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_dict[str(k)] = make_json_safe(v)
        return new_dict
    elif isinstance(data, list):
        return [make_json_safe(v) for v in data]
    elif isinstance(data, (int, float, str, bool)) or data is None:
        return data
    else:
        return str(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)