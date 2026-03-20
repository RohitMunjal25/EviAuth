import React from "react";
import "./ResultPage.css";
import jsPDF from "jspdf";

export default function ResultPage({ setPage, file, resultData }) {
  const report = resultData?.report || {};
  const fileName = file?.name || "evidence.jpg";
  const verdictLabel = report.authenticity_status || "Unknown";
  const score = report.manipulation_probability ?? 0;

  const strokeDasharray = `${(score * 3.39).toFixed(0)} 339`;

  const verdictColor = 
    verdictLabel.includes("Authentic") || verdictLabel.includes("Original") ? "#4ade80" : 
    verdictLabel.includes("Fake") || verdictLabel.includes("Tampered") ? "#f87171" : 
    "#fbbf24";

  const downloadPDF = () => {
    const pdf = new jsPDF();

    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(22);
    pdf.text("AI Evidence Forensic Report", 20, 20);

    pdf.setFontSize(12);
    pdf.setFont("helvetica", "normal");
    pdf.text(`File Name: ${fileName}`, 20, 40);
    pdf.text(`Date: ${new Date().toLocaleDateString("en-IN")}`, 20, 50);
    pdf.text(`Authenticity Status: ${verdictLabel}`, 20, 60);
    pdf.text(`Risk Score: ${score}%`, 20, 70);

    pdf.line(20, 75, 190, 75);

    let y = 90;
    pdf.setFont("helvetica", "bold");
    pdf.text("Forensic Summary:", 20, y);
    pdf.setFont("helvetica", "normal");
    y += 10;
    
    const splitSummary = pdf.splitTextToSize(report.forensic_summary || "N/A", 170);
    pdf.text(splitSummary, 20, y);
    y += (splitSummary.length * 7) + 10;

    pdf.setFont("helvetica", "bold");
    pdf.text("Technical Metadata:", 20, y);
    y += 10;

    const addLine = (label, value) => {
      if (y > 280) { pdf.addPage(); y = 20; }
      pdf.setFont("helvetica", "bold");
      pdf.text(label, 20, y);
      pdf.setFont("helvetica", "normal");
      pdf.text(String(value || "N/A"), 70, y);
      y += 10;
    };

    addLine("Camera Source:", report.source_hardware);
    addLine("Metadata Integrity:", report.metadata_integrity);
    addLine("GPS Data:", report.gps_present ? "Available" : "Not Found");
    addLine("Software Used:", report.software || "None (Original)");

    pdf.save(`${fileName.split('.')[0]}_Forensic_Report.pdf`);
  };

  return (
    <div className="result-container">
      <div className="result-topbar">
        <div className="result-file">
          <span style={{ fontSize: 28 }}>🖼️</span>
          <div>
            <div className="result-filename">{fileName}</div>
            <div className="result-filemeta">Analyzed · {new Date().toLocaleDateString("en-IN")}</div>
          </div>
        </div>
        <span className="badge" style={{ background: verdictColor, color: "#000", padding: "6px 16px", borderRadius: "20px", fontWeight: "bold" }}>
          {verdictLabel}
        </span>
      </div>

      <div className="result-grid">
        <div className="score-card card-box">
          <div className="ring-wrap">
            <svg className="ring-svg" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="54" fill="none" stroke="#1e293b" strokeWidth="8" />
              <circle cx="60" cy="60" r="54" fill="none" stroke={score > 50 ? "#f87171" : "#38bdf8"} 
                strokeWidth="8" strokeDasharray={strokeDasharray} strokeLinecap="round" transform="rotate(-90 60 60)" />
            </svg>
            <div className="ring-center">
              <span className="ring-value">{score}%</span>
              <span className="ring-label">Risk</span>
            </div>
          </div>

          <div className="verdict-title">Forensic Verdict</div>
          <div className="verdict-desc">{report.forensic_summary || "Automated analysis complete."}</div>

          <div className="risk-list">
            <RiskItem label="Metadata Integrity" value={report.metadata_integrity === "Preserved" ? 100 : 40} color="#38bdf8" />
            <RiskItem label="AI Generation" value={score} color="#f87171" />
          </div>
        </div>

        <div className="card-box">
          <div className="verdict-title" style={{ marginBottom: '15px' }}>Technical Metadata</div>
          <div className="metadata-container">
            <MetaRow label="Camera Source" value={report.source_hardware || "Unknown"} />
            <MetaRow label="GPS Location" value={report.gps_present ? "Available" : "Not Found"} />
            <MetaRow label="Software Used" value={report.software || "None (Original)"} />
            <MetaRow label="Capture Date" value={report.creation_date || "N/A"} />
          </div>
          
          <div className="result-actions" style={{ marginTop: '30px' }}>
            <button className="btn btn-blue" onClick={() => setPage("upload")}>Analyze Another</button>
            <button className="btn btn-outline" onClick={() => setPage("dashboard")}>Dashboard</button>
            <button className="btn btn-green" onClick={downloadPDF}>Download PDF</button>
          </div>
        </div>
      </div>
    </div>
  );
}

const RiskItem = ({ label, value, color }) => (
  <div className="risk-item">
    <div className="risk-row-meta">
      <span className="meta-key" style={{ fontSize: '11px' }}>{label}</span>
      <span className="meta-val">{value}%</span>
    </div>
    <div className="risk-track">
      <div className="risk-fill" style={{ width: `${value}%`, background: color }}></div>
    </div>
  </div>
);

const MetaRow = ({ label, value }) => (
  <div className="meta-row">
    <span className="meta-key">{label}</span>
    <span className="meta-val">{value}</span>
  </div>
);