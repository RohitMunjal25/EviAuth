🔍EviAuth
Advanced Multi-Modal Digital Forensics & AI-Authenticity Suite
EviAuth is a high-integrity forensic ecosystem designed to detect sophisticated digital forgeries. By synthesizing 10+ state-of-the-art Deep Learning models, the platform provides a robust defense against Deepfakes, AI-generated media, and document tampering.

"In the era of synthetic media, verify every byte." 🔐


🚀 Core Capabilities
🧠 Neural Ensemble Detection
Deepfake Mitigation: Detects high-fidelity face-swaps and GAN-generated video content.
Audio Spoofing Protection: Identifies synthetic voice clones and replayed speech using ASVspoof protocols.
Document Integrity: Validates ID cards and legal certificates using the MIDV-500 dataset standards.
Image Forgery Localization: Detects splicing, cloning, and resampling artifacts via CASIA/CIFAKE models.


🔬 Forensic Tool Integration
Metadata Forensics: Deep-header inspection using ExifTool to uncover GPS-spoofing and software-edit traces.
Signal Processing: Frame-level decomposition and audio frequency analysis using FFmpeg and Librosa.


🏗️ Technical ArchitectureDomainIntegrated Models & Technologies

🖼️ Image                  CASIA (Splicing), CIFAKE (Gen-AI), OpenCV
🎥 Video                  FaceForensics++, DFDC (Deepfakes), FFmpeg
🔊 Audio                  ASVspoof LA (Logical Access), ASVspoof PA (Physical Access)
📄 Document               MIDV-500 (Forgery Detection), PyMuPDF


The Tech Stack
Backend: Flask (Python)
AI Engine: TensorFlow, Keras, PyTorch
Forensics: ExifTool, FFmpeg, Librosa


⚙️ Deployment & Setup
1️⃣ Clone the Infrastructure
Bash
git clone https://github.com/RohitMunjal25/EviAuth.git
cd EviAuth
2️⃣ Environment Configuration
Bash
# Initialize virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3️⃣ Execution
Bash
python app.py


⚡ Zero-Config "Plug & Play"
EviAuth is engineered for immediate deployment. On the First Run, the system autonomously:
Retrieves optimized model weights (H5/PTH) from secure repositories.
Validates hardware acceleration (CUDA/OpenCL).
Initializes forensic binary paths automatically.


🛠️ Future Roadmap
[ ] Interactive Dashboard: React-based forensic report visualization.
[ ] Real-time Stream Analysis: Live video feed authenticity checking.
[ ] API Access: RESTful endpoints for enterprise security workflows.

👨‍💻 Authors
Rohit Munjal & Yogita Gupta

Developed for the advancement of Information Security and Digital Trust.
