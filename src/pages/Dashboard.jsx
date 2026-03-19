import React, { useEffect, useState } from "react";
import "./Dashboard.css";

export default function Dashboard({ setPage }) {
  const currentUser = localStorage.getItem("currentUser");
  const isGuest = !currentUser;

  const [stats, setStats] = useState({
    total: 0,
    authentic: 0,
    suspicious: 0,
    tampered: 0,
  });

  const [recent, setRecent] = useState([]);

  useEffect(() => {
    if (!currentUser) return;

    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const user = users.find(u => u.email === currentUser);

    if (!user) return;

    const history = user.history || [];

    const total = history.length;
    const authentic = history.filter(h => h.verdict.includes("Original") || h.verdict.includes("Authentic")).length;
    const tampered = history.filter(h => h.verdict.includes("Edited") || h.verdict.includes("Tampered")).length;
    const suspicious = total - authentic - tampered;

    setStats({ total, authentic, suspicious, tampered });
    setRecent(history.slice(-5).reverse());
  }, [currentUser]);

  const statCards = [
    { label: "Total Analyzed", value: stats.total, color: "#38bdf8", icon: "📊" },
    { label: "Authentic", value: stats.authentic, color: "#4ade80", icon: "✅" },
    { label: "Suspicious", value: stats.suspicious, color: "#fbbf24", icon: "⚠️" },
    { label: "Tampered", value: stats.tampered, color: "#f87171", icon: "❌" },
  ];

  // Helper to color code the verdict in the table
  const getVerdictStyle = (verdict) => {
    if (verdict.includes("Original") || verdict.includes("Authentic")) return { color: "#4ade80", fontWeight: "bold" };
    if (verdict.includes("Edited") || verdict.includes("Tampered")) return { color: "#f87171", fontWeight: "bold" };
    return { color: "#fbbf24", fontWeight: "bold" };
  };

  return (
    <div className="dashboard-container">
      <div className="page-header">
        <h1 style={{ marginBottom: "8px" }}>Forensic Dashboard</h1>
        <p style={{ color: "#94a3b8" }}>Overview of your evidence analysis activity</p>
      </div>

      {/* --- STATS GRID --- */}
      <div className="stat-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '30px' }}>
        {statCards.map((s, i) => (
          <div className="stat-card card-box" key={i} style={{ textAlign: 'center', padding: '25px', background: '#111827', borderRadius: '12px', borderTop: `3px solid ${s.color}` }}>
            <div className="stat-icon" style={{ fontSize: '32px', marginBottom: '10px' }}>{s.icon}</div>
            <div className="stat-value" style={{ color: s.color, fontSize: '36px', fontWeight: 'bold' }}>{s.value}</div>
            <div className="stat-label" style={{ color: '#94a3b8', fontSize: '14px', marginTop: '5px' }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* --- QUICK ACTIONS --- */}
      <div className="quick-actions" style={{ display: 'flex', gap: '15px', marginBottom: '30px' }}>
        <button className="btn btn-blue" onClick={() => setPage("upload")} style={{ flex: 1, padding: '15px', fontSize: '16px' }}>
          <span style={{ marginRight: '8px' }}>📤</span> Upload New Evidence
        </button>
        <button className="btn btn-outline" onClick={() => setPage("history")} style={{ flex: 1, padding: '15px', fontSize: '16px' }}>
          <span style={{ marginRight: '8px' }}>📁</span> View Full History
        </button>
      </div>

      {/* --- RECENT ANALYSES --- */}
      <div className="recent-analyses card-box" style={{ background: '#111827', padding: '25px', borderRadius: '12px' }}>
        <h3 style={{ marginBottom: '20px', fontSize: '18px', borderBottom: '1px solid #1e293b', paddingBottom: '10px' }}>Recent Analyses</h3>

        {isGuest ? (
          <div style={{ textAlign: 'center', padding: '40px 20px' }}>
            <span style={{ fontSize: '40px' }}>🔒</span>
            <h4 style={{ margin: '15px 0 5px', color: '#cbd5e1' }}>Guest Mode Active</h4>
            <p style={{ color: '#64748b' }}>Please login to save and view your forensic analysis history.</p>
          </div>
        ) : recent.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 20px' }}>
            <span style={{ fontSize: '40px' }}>📭</span>
            <h4 style={{ margin: '15px 0 5px', color: '#cbd5e1' }}>No Analyses Yet</h4>
            <p style={{ color: '#64748b', marginBottom: '20px' }}>Upload your first digital evidence to start building your history.</p>
            <button className="btn btn-blue" onClick={() => setPage("upload")}>Upload Now</button>
          </div>
        ) : (
          <div className="table-wrap">
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ color: '#94a3b8', borderBottom: '2px solid #1e293b' }}>
                  <th style={{ padding: '12px 10px' }}>File Name</th>
                  <th style={{ padding: '12px 10px' }}>Verdict</th>
                  <th style={{ padding: '12px 10px' }}>Date</th>
                </tr>
              </thead>
              <tbody>
                {recent.map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: '15px 10px', color: '#e2e8f0' }}>{row.name}</td>
                    <td style={{ padding: '15px 10px' }}>
                      <span style={{ ...getVerdictStyle(row.verdict), background: '#0f172a', padding: '5px 10px', borderRadius: '6px' }}>
                        {row.verdict}
                      </span>
                    </td>
                    <td style={{ padding: '15px 10px', color: '#94a3b8' }}>{row.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}