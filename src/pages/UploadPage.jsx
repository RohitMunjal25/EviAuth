import React, { useState, useRef } from "react";
import "./UploadPage.css";

export default function UploadPage({ goScan }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef();

  const getFileEmoji = (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase();
    if (['mp4', 'mov', 'avi'].includes(ext)) return "🎥";
    if (['mp3', 'wav', 'm4a'].includes(ext)) return "🎙️";
    if (['pdf'].includes(ext)) return "📄";
    return "🖼️";
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) setFile(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://13.61.105.7:10000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Server error");
      const data = await response.json();

      const currentUser = localStorage.getItem("currentUser");
      if (currentUser) {
        const users = JSON.parse(localStorage.getItem("users") || "[]");
        const index = users.findIndex(u => u.email === currentUser);
        if (index !== -1) {
          users[index].history.push({
            name: file.name,
            date: new Date().toLocaleDateString("en-IN"),
            verdict: data?.report?.authenticity_status || "Unknown",
            score: data?.report?.manipulation_probability ?? 0
          });
          localStorage.setItem("users", JSON.stringify(users));
        }
      }

      goScan(file, data);
    } catch (err) {
      alert("Backend connection failed! Check if AWS server is running.");
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-grid">
      {/* LEFT COLUMN: UPLOAD ZONE */}
      <div className="upload-main card-box">
        <div 
          className={`dropzone ${file ? 'file-active' : ''}`} 
          onClick={() => fileRef.current.click()}
          style={{ minHeight: '220px' }} // Thoda bada kar diya clean look ke liye
        >
          <input type="file" ref={fileRef} hidden onChange={handleFileChange} 
            accept="image/*,video/*,audio/*,.pdf" />

          {!file ? (
            <div className="drop-empty">
              <div className="drop-icon">📤</div>
              <h3>Click or Drag Evidence Here</h3>
              <p>Supports Images, Videos, Audio, and PDFs (Max 50MB)</p>
              <div className="format-list">
                {['JPG', 'PNG', 'MP4', 'WAV', 'PDF'].map(tag => (
                  <span key={tag} className="format-tag">{tag}</span>
                ))}
              </div>
            </div>
          ) : (
            <div className="file-selected">
              <div className="file-emoji">{getFileEmoji(file.name)}</div>
              <div className="file-info">
                <div className="file-name">{file.name}</div>
                <div className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB</div>
              </div>
              <button className="remove-btn" onClick={(e) => {
                e.stopPropagation();
                setFile(null);
              }}>✕</button>
            </div>
          )}
        </div>

        <button className="btn btn-blue" onClick={handleAnalyze} disabled={!file || loading}
          style={{ width: '100%', marginTop: '30px', height: '50px', fontSize: '16px', fontWeight: 'bold' }}>
          {loading ? "⏳ Processing AI Models..." : "🔍 Start Forensic Analysis"}
        </button>
      </div>

      {/* RIGHT COLUMN: SIDEBAR INFO */}
      <div className="upload-sidebar card-box">
        <h4 style={{ fontSize: '14px', marginBottom: '16px' }}>System Info</h4>
        <div className="info-rows">
          <div className="info-row"><span className="meta-key">Server Status</span><span className="text-green">● Online</span></div>
          <div className="info-row"><span className="meta-key">AI Engine</span><span>v3.2-Flash</span></div>
          <div className="info-row"><span className="meta-key">Storage</span><span>Encrypted</span></div>
        </div>

        <hr style={{ border: '0.5px solid #1e293b', margin: '20px 0' }} />

        <h4 style={{ fontSize: '14px', marginBottom: '16px' }}>How it works?</h4>
        {[
          { num: "1", text: "Upload the digital file for forensic verification." },
          { num: "2", text: "System runs ELA, Metadata, and CNN models." },
          { num: "3", text: "Download the verified authenticity report." }
        ].map(step => (
          <div key={step.num} className="how-row">
            <div className="how-num">{step.num}</div>
            <p className="opt-desc" style={{ margin: 0 }}>{step.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}