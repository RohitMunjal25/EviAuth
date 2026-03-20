import React, { useState, useEffect } from "react";
import "./HistoryPage.css";
import jsPDF from "jspdf"; 
function getVerdict(score) {
  if (score <= 20) return { label: "Authentic", cls: "badge-green", pill: "pill-green" };
  if (score <= 60) return { label: "Suspicious", cls: "badge-yellow", pill: "pill-yellow" };
  return { label: "Tampered", cls: "badge-red", pill: "pill-red" };
}

export default function HistoryPage({ setPage }) {
  const currentUser = localStorage.getItem("currentUser");

  const [records, setRecords] = useState([]);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (!currentUser) return;
    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const user = users.find(u => u.email === currentUser);

    if (!user) return;

    const formatted = (user.history || []).map((h, i) => ({
      id: i, 
      name: h.name,
      date: h.date,
      score: h.score !== undefined ? h.score : (h.verdict.includes("Authentic") ? 0 : 80),
      verdictText: h.verdict
    }));

    setRecords(formatted.reverse());
  }, [currentUser]);

  const handleDelete = (idToDelete) => {
    if (!window.confirm("Are you sure you want to delete this record?")) return;

    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const userIndex = users.findIndex(u => u.email === currentUser);
    
    if (userIndex !== -1) {
      users[userIndex].history = users[userIndex].history.filter((_, i) => i !== idToDelete);
      localStorage.setItem("users", JSON.stringify(users));
      
      setRecords(prev => prev.filter(r => r.id !== idToDelete));
    }
  };

  const downloadRowPDF = (row) => {
    const pdf = new jsPDF();
    pdf.setFont("helvetica", "bold");
    pdf.setFontSize(22);
    pdf.text("AI Evidence Forensic Report", 20, 20);

    pdf.setFontSize(12);
    pdf.setFont("helvetica", "normal");
    pdf.text(`File Name: ${row.name}`, 20, 40);
    pdf.text(`Date Analyzed: ${row.date}`, 20, 50);
    pdf.text(`Authenticity Status: ${row.verdictText}`, 20, 60);
    pdf.text(`Risk Score: ${row.score}%`, 20, 70);

    pdf.line(20, 75, 190, 75);
    pdf.setFontSize(10);
    pdf.text("Note: This is a historical summary. Full metadata is available for new scans.", 20, 90);

    pdf.save(`${row.name.split('.')[0]}_Report.pdf`);
  };

  const handleView = (row) => {
    alert(`File: ${row.name}\nVerdict: ${row.verdictText}\nScore: ${row.score}%\n\nPlease download the PDF for the summary report.`);
  };

  const filteredRecords = records.filter(r => {
    const v = getVerdict(r.score);
    const matchFilter = filter === "all" || v.label.toLowerCase() === filter;
    const matchSearch = r.name.toLowerCase().includes(search.toLowerCase());
    return matchFilter && matchSearch;
  });

  return (
    <div>
      <div className="page-header">
        <h1>Evidence History</h1>
        <p>{records.length} total records · {filteredRecords.length} shown</p>
      </div>

      
      <div style={{ display:'flex', gap:10, flexWrap:'wrap', marginBottom:16, alignItems:'center' }}>
        {[
          { id:'all', label:'All' },
          { id:'authentic', label:'✅ Authentic' },
          { id:'suspicious', label:'⚠️ Suspicious' },
          { id:'tampered', label:'❌ Tampered' },
        ].map(f => (
          <button key={f.id} onClick={() => setFilter(f.id)}
            style={{
              padding:'6px 16px', borderRadius:50, fontSize:13, fontWeight:600,
              background: filter === f.id ? 'rgba(56,189,248,0.15)' : '#1e293b',
              border: filter === f.id ? '1px solid #38bdf8' : '1px solid #334155',
              color: filter === f.id ? '#38bdf8' : '#94a3b8',
              cursor:'pointer'
            }}>
            {f.label}
          </button>
        ))}

        <div style={{ marginLeft:'auto', display:'flex', alignItems:'center', gap:8, background:'#1e293b', border:'1px solid #334155', borderRadius:50, padding:'6px 14px' }}>
          🔍
          <input
            placeholder="Search file..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ background:'none', border:'none', outline:'none', color:'#e2e8f0' }}
          />
        </div>
      </div>

      <div className="card" style={{ padding:0, overflow:'hidden' }}>
        <div className="table-wrap">
          {filteredRecords.length === 0 ? (
            <div style={{ textAlign:'center', padding:40, color:'#64748b' }}>
              <p>No records found.</p>
              <button className="btn btn-blue" onClick={() => setPage("upload")} style={{ marginTop: '10px' }}>
                Upload Evidence
              </button>
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #1e293b', color: '#94a3b8' }}>
                  <th style={{ padding: '15px' }}>File Name</th>
                  <th>Date</th>
                  <th>Risk Score</th>
                  <th>Verdict</th>
                  <th style={{ textAlign: 'center' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredRecords.map(row => {
                  const v = getVerdict(row.score);
                  return (
                    <tr key={row.id} style={{ borderBottom: '1px solid #1e293b' }}>
                      <td style={{ padding: '15px', color: '#e2e8f0', fontWeight: '500' }}>{row.name}</td>
                      <td style={{ color: '#94a3b8' }}>{row.date}</td>
                      <td><span className={`pill ${v.pill}`}>{row.score}%</span></td>
                      <td><span className={`badge ${v.cls}`}>{v.label}</span></td>
                      
                      <td style={{ display: 'flex', gap: '8px', justifyContent: 'center', padding: '10px' }}>
                        <button 
                          className="btn btn-blue btn-sm" 
                          onClick={() => handleView(row)}
                          title="View Details"
                          style={{ padding: '6px 10px', fontSize: '12px' }}>
                          👁️ View
                        </button>
                        
                        <button 
                          className="btn btn-green btn-sm" 
                          onClick={() => downloadRowPDF(row)}
                          title="Download PDF"
                          style={{ padding: '6px 10px', fontSize: '12px' }}>
                          📥 PDF
                        </button>

                        <button
                          className="btn btn-red btn-sm"
                          onClick={() => handleDelete(row.id)}
                          title="Delete Record"
                          style={{ padding: '6px 10px', fontSize: '12px' }}>
                          🗑️
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div style={{ marginTop:10, fontSize:12, color:'#475569', textAlign: 'right' }}>
        Showing {filteredRecords.length} of {records.length} records
      </div>
    </div>
  );
}