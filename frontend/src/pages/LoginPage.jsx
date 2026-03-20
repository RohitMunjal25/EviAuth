import React, { useState } from "react";
import "./LoginPage.css";

export default function LoginPage({ onLogin }) {
  const [name, setName] = useState(""); 
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [isRegister, setIsRegister] = useState(false);

  const handleRegister = () => {
    if (!name || !email || !pass) return alert("Please fill all fields!");

    const users = JSON.parse(localStorage.getItem("users") || "[]");
    if (users.find(u => u.email === email)) return alert("User already exists!");

    users.push({ name, email, pass, history: [] });
    localStorage.setItem("users", JSON.stringify(users));
    alert("Account Created Successfully! Now login.");
    
    setIsRegister(false);
    setPass("");
  };

  const handleLogin = () => {
    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const user = users.find(u => u.email === email && u.pass === pass);
    if (!user) return alert("Invalid credentials");

    localStorage.setItem("currentUser", email);
    localStorage.setItem("currentUserName", user.name || "User");
    onLogin("user");
  };

  const handleGuest = () => {
    localStorage.removeItem("currentUser");
    localStorage.removeItem("currentUserName");
    onLogin("guest");
  };

  return (
    <div className="login-wrapper">
      
      <div className="login-left">
        <div className="login-brand">
          <div className="login-logo">⚡</div>
          <h1><span>Evi</span>Auth</h1>
          <p>AI Powered Evidence Authentication Platform</p>

          <div className="login-features">
            <div className="login-feature">
              <div className="login-feature-icon">🔍</div>
              Detect deepfakes instantly
            </div>
            <div className="login-feature">
              <div className="login-feature-icon">📊</div>
              Generate forensic reports
            </div>
            <div className="login-feature">
              <div className="login-feature-icon">🔒</div>
              Secure evidence storage
            </div>
          </div>
        </div>
      </div>

      <div className="login-right">
        <div className="login-box">
          <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>
          <p className="login-sub">
            {isRegister ? "Register to start analyzing evidence" : "Login to continue"}
          </p>

          {isRegister && (
            <input
              type="text"
              className="input-field"
              placeholder="Full Name"
              value={name}
              onChange={e => setName(e.target.value)}
            />
          )}

          <input
            type="email"
            className="input-field"
            placeholder="Email Address"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />

          <input
            type="password"
            className="input-field"
            placeholder="Password"
            value={pass}
            onChange={e => setPass(e.target.value)}
          />

          {isRegister ? (
            <button className="btn btn-blue" onClick={handleRegister}>
              Create Account
            </button>
          ) : (
            <button className="btn btn-blue" onClick={handleLogin}>
              Login
            </button>
          )}

          <div className="login-divider">or</div>

          <button className="btn btn-outline" onClick={handleGuest}>
            Continue as Guest
          </button>

          <div className="auth-switch">
            {isRegister ? (
              <>Already have an account? <span onClick={() => { setIsRegister(false); setName(""); }}>Login</span></>
            ) : (
              <>New here? <span onClick={() => setIsRegister(true)}>Create account</span></>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}