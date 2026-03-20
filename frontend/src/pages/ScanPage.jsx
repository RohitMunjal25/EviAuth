import React, { useState, useEffect, useRef } from "react"; // useRef add kiya
import "./ScanPage.css";

const STEPS = [
  { label: "File Validation", desc: "Verifying file integrity", duration: 1000 },
  { label: "Metadata Extraction", desc: "Reading EXIF and file properties", duration: 1500 },
  { label: "Deepfake Detection", desc: "Running AI neural model", duration: 2500 },
  { label: "Tamper Analysis", desc: "Checking for editing artifacts", duration: 1500 },
  { label: "Report Generation", desc: "Calculating confidence score", duration: 800 },
];

const LOGS = [
  "> File checksum verified — SHA256 OK",
  "> Loading ExifTool 12.6...",
  "> TensorFlow deepfake model ready",
  "> 248 frames sampled for analysis",
  "> Deepfake probability: 0.06 (LOW)",
  "> Metadata: all fields consistent",
  "> No tamper artifacts detected",
  "> Confidence score: 94%",
  "> Generating report...",
];

export default function ScanPage({ setPage, file }) {
  const [progress, setProgress] = useState(0);
  const [stepIndex, setStepIndex] = useState(0);
  const [logs, setLogs] = useState(["> Initializing forensic engine..."]);
  const logEndRef = useRef(null); 

  const total = STEPS.reduce((a, s) => a + s.duration, 0);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  useEffect(() => {
    let elapsed = 0;
    let logI = 0;
    let logTimer = 0;

    const tick = setInterval(() => {
      elapsed += 100;
      logTimer += 100;

      setProgress(Math.min(100, Math.round((elapsed / total) * 100)));

      let cumul = 0;
      for (let i = 0; i < STEPS.length; i++) {
        cumul += STEPS[i].duration;
        if (elapsed < cumul) {
          setStepIndex(i);
          break;
        }
        if (i === STEPS.length - 1) setStepIndex(STEPS.length);
      }

      if (logTimer >= 700 && logI < LOGS.length) {
        setLogs((prev) => [...prev, LOGS[logI]]);
        logI++;
        logTimer = 0;
      }

      if (elapsed >= total) {
        clearInterval(tick);
        setTimeout(() => setPage("result"), 500);
      }
    }, 100);

    return () => clearInterval(tick);
  }, [total, setPage]);

  const fileName = file?.name || "evidence_file.jpg";
  const fileSize = file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : "2.4 MB";

  return (
    <div className="scan-page">
      <div className="scan-box">
        <div className="scan-header">
          <div className="scan-icon">🔍</div>
          <h2>Analyzing Evidence</h2>
          <p>{fileName} · {fileSize}</p>
        </div>

        <div className="card scan-bar-card card-box">
          <div className="bar-outer">
            <div className="bar-inner" style={{ width: `${progress}%` }} />
          </div>
          <div className="bar-meta">
            <span>{stepIndex < STEPS.length ? STEPS[stepIndex].label : "Complete!"}</span>
            <span className="bar-pct">{progress}%</span>
          </div>
        </div>

        <div className="card card-box">
          {STEPS.map((s, i) => {
            const status = i < stepIndex ? "done" : i === stepIndex ? "running" : "waiting";
            return (
              <div key={i} className={`scan-step ${status}`}>
                <div className={`step-dot ${status}`}>
                  {status === "done" ? "✓" : status === "running" ? "●" : i + 1}
                </div>
                <div className="step-info">
                  <span className="step-name">{s.label}</span>
                  <span className="step-desc">
                    {status === "done" ? "Completed" : status === "running" ? s.desc : "Waiting..."}
                  </span>
                </div>
                <span className="step-mark">
                  {status === "done" ? "✅" : status === "running" ? "⏳" : "—"}
                </span>
              </div>
            );
          })}
        </div>

        <div className="scan-log">
          {logs.map((line, i) => (
            <div key={i} className="log-line">{line}</div>
          ))}
          <div ref={logEndRef} /> 
          <span className="log-cursor">█</span>
        </div>
      </div>
    </div>
  );
}