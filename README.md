# 🔍 EviAuth

**AI-Based Digital Evidence Authenticity Platform 🚀**

---

## 📌 Project Overview

EviAuth is an AI-powered digital forensics platform designed to detect manipulation and forgery in **images, videos, audio, and documents**.

The system integrates multiple machine learning models and forensic tools to analyze media authenticity and provide reliable results.

> "Trust your data. Verify your evidence." 🔐

---

## ⚡ Key Features

### 🧠 Multi-Modal Detection

* Supports **Image, Video, Audio, and Document analysis**
* Uses **10+ trained ML models** for high accuracy detection

---

### 🔐 Forensic Analysis

* Metadata extraction using **ExifTool**
* Media processing using **FFmpeg**
* Deep inspection of file authenticity

---

### ⚙️ Auto Model Setup (Plug & Play)

* No manual setup required
* On first run, the system automatically:

  * Downloads required models
  * Sets up dependencies
  * Configures environment

👉 Just run one command and everything is ready

---

## 🧠 Models Used

### 🖼️ Image Models

* CASIA
* CIFAKE
* ExifTool (metadata analysis)

---

### 📄 Document Model

* MIDV-500

---

### 🎥 Video Models

* FaceForensics++
* DFDC
* FFmpeg (frame extraction & processing)
* ExifTool

---

### 🔊 Audio Models

* ASVspoof LA
* ASVspoof PA

---

## 🛠️ Tech Stack

| Layer      | Technology           |
| ---------- | -------------------- |
| Backend    | Python (Flask)       |
| ML Models  | Deep Learning Models |
| Processing | FFmpeg, ExifTool     |
| Database   | (Optional if used)   |


## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```id="eviauth2"
git clone https://github.com/yourusername/EviAuth.git
cd EviAuth
```

---

### 2️⃣ Install Dependencies

```id="eviauth3"
pip install -r requirements.txt
```

---

### 3️⃣ Run Application

```id="eviauth4"
python app.py
```

---

## 🚀 First Run Behavior

* Models will be **automatically downloaded**
* Required tools will be initialized
* System will configure itself

👉 No manual model setup required

---

## 📊 Capabilities

* Detect deepfake media
* Analyze metadata for tampering
* Identify forged documents
* Validate audio authenticity

---

## 📌 Future Improvements

* Web dashboard for detailed reports
* Real-time analysis pipeline
* Model accuracy improvements

---

## 👨‍💻 Author

Rohit Munjal & Yogita Gupta
