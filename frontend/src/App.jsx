import React, { useState, useEffect } from 'react';
import './App.css';
import LoginPage    from './pages/LoginPage';
import Dashboard    from './pages/Dashboard';
import UploadPage   from './pages/UploadPage';
import ScanPage     from './pages/ScanPage';
import ResultPage   from './pages/ResultPage';
import HistoryPage  from './pages/HistoryPage';

export default function App() {
  const [page, setPage] = useState('login');
  const [file, setFile] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [userType, setUserType] = useState(null); 

  useEffect(() => {
    const currentUser = localStorage.getItem("currentUser");
    if (currentUser) {
      setUserType('user');  
      setPage('dashboard'); 
    }
  }, []);

  const goScan = (selectedFile, resultFromServer) => {
    setFile(selectedFile);
    setAnalysisData(resultFromServer); 
    setPage('scan'); 
  };

  const handleLogout = () => {
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserName"); 
    setUserType(null);
    setPage('login'); 
  };

  if (page === 'login') {
    return (
      <LoginPage 
        onLogin={(type) => {
          setUserType(type);   
          setPage('dashboard');
        }} 
      />
    );
  }

  return (
    <div className="layout">
      <aside className={`sidebar ${menuOpen ? 'open' : ''}`}>
        <div className="logo">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">AI Evidence</span>
        </div>

        <nav>
          {[
            { id: 'dashboard', icon: '📊', label: 'Dashboard'  },
            { id: 'upload',    icon: '📤', label: 'Upload'     },
            { id: 'history',   icon: '📁', label: 'History'    },
          ].map(item => (
            <button
              key={item.id}
              className={`nav-btn ${page === item.id ? 'active' : ''}`}
              onClick={() => { 
                setPage(item.id); 
                setMenuOpen(false);
                if (item.id !== 'result') setAnalysisData(null); 
              }}
            >
              <span>{item.icon}</span> {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            
            <div className="avatar">
              {userType === 'guest' 
                ? 'G' 
                : (localStorage.getItem("currentUserName") 
                    ? localStorage.getItem("currentUserName")[0].toUpperCase() 
                    : 'U')
              }
            </div>

            <div>
              
              <div className="user-name">
                {userType === 'guest' 
                  ? 'Guest User' 
                  : (localStorage.getItem("currentUserName") || "User")}
              </div>
              
              <div className="user-role">
                {userType === 'guest' 
                  ? 'Demo Mode' 
                  : (localStorage.getItem("currentUser") || 'Registered User')}
              </div>
            </div>
          </div>
          
          <button className="logout-btn" onClick={handleLogout}>
            Logout →
          </button>
        </div>
      </aside>

      {menuOpen && <div className="overlay" onClick={() => setMenuOpen(false)} />}

      <main className="main">
        <div className="topbar">
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}>☰</button>
          <span className="page-title">
            {{ dashboard:'Dashboard', upload:'Upload Evidence', scan:'Scanning...', result:'Report', history:'History' }[page]}
          </span>
          <span className="status-indicator">● Online</span>
        </div>

        <div className="content">
          {page === 'dashboard' && <Dashboard setPage={setPage} />}
          {page === 'upload'    && <UploadPage goScan={goScan} />}
          {page === 'scan'      && <ScanPage setPage={setPage} file={file} />}
          {page === 'result'    && <ResultPage setPage={setPage} file={file} resultData={analysisData} />}
          {page === 'history'   && <HistoryPage setPage={setPage} />}
        </div>
      </main>
    </div>
  );
}