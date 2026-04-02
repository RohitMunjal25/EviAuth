# 🔍 EviAuth – Advanced Multi-Modal Digital Forensics & AI Authenticity Suite

> **"In the era of synthetic media, verify every byte." 🔐**

EviAuth is a high-integrity forensic ecosystem designed to detect sophisticated digital forgeries. By combining **10+ state-of-the-art Deep Learning models**, the platform provides a powerful defense against **deepfakes, AI-generated media, and document tampering**.

---

## 🚀 Core Capabilities

### 🧠 Neural Ensemble Detection

* **Deepfake Mitigation**
  Detects high-fidelity face-swaps and GAN-generated video content.

* **Audio Spoofing Protection**
  Identifies synthetic voice clones and replay attacks using ASVspoof protocols.

* **Document Integrity Verification**
  Validates ID cards and legal documents using MIDV-500 standards.

* **Image Forgery Localization**
  Detects splicing, cloning, and resampling artifacts using CASIA & CIFAKE models.

---

## 🔬 Forensic Tool Integration

* **Metadata Forensics**
  Deep header inspection using ExifTool to detect:

  * GPS spoofing
  * Editing software traces

* **Signal Processing**

  * Frame-level video decomposition using FFmpeg
  * Audio frequency analysis using Librosa

---

## 🏗️ Technical Architecture

### 📊 Integrated Models & Technologies

| Domain      | Technologies                              |
| ----------- | ----------------------------------------- |
| 🖼️ Image   | CASIA (Splicing), CIFAKE (Gen-AI), OpenCV |
| 🎥 Video    | FaceForensics++, DFDC, FFmpeg             |
| 🔊 Audio    | ASVspoof LA & PA                          |
| 📄 Document | MIDV-500, PyMuPDF                         |

---

## ⚙️ Tech Stack

* **Backend:** Flask (Python)
* **AI Engine:** TensorFlow, Keras, PyTorch
* **Forensics Tools:** ExifTool, FFmpeg, Librosa

---

## ⚙️ Deployment & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RohitMunjal25/EviAuth.git
cd EviAuth
```

### 2️⃣ Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python app.py
```

---

## ⚡ Zero-Config "Plug & Play"

On first run, EviAuth automatically:

* 📥 Downloads optimized model weights (H5/PTH)
* ⚡ Detects hardware acceleration (CUDA/OpenCL)
* 🔧 Configures forensic tools and binaries

---

## 🛠️ Future Roadmap

* [ ] 📊 Interactive Dashboard (React-based visualization)
* [ ] 🎥 Real-time Stream Analysis
* [ ] 🌐 REST API for enterprise integration

---

## 👨‍💻 Authors

* **Rohit Munjal**
* **Yogita Gupta**

---

## 🎯 Purpose

Developed for advancing **Information Security**, **Digital Forensics**, and **Trust in AI-generated content**.

---
