<<<<<<< HEAD:srcs/frontend/src/App.tsx
// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <section id="center">
//         <div className="hero">
//           <img src={heroImg} className="base" width="170" height="179" alt="" />
//           <img src={reactLogo} className="framework" alt="React logo" />
//           <img src={viteLogo} className="vite" alt="Vite logo" />
//         </div>
//         <div>
//           <h1>Get started</h1>
//           <p>
//             Edit <code>src/App.tsx</code> and save to test <code>HMR</code>
//           </p>
//         </div>
//         <button
//           type="button"
//           className="counter"
//           onClick={() => setCount((count) => count + 1)}
//         >
//           Count is {count}
//         </button>
//       </section>

//       <div className="ticks"></div>

//       <section id="next-steps">
//         <div id="docs">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#documentation-icon"></use>
//           </svg>
//           <h2>Documentation</h2>
//           <p>Your questions, answered</p>
//           <ul>
//             <li>
//               <a href="https://vite.dev/" target="_blank">
//                 <img className="logo" src={viteLogo} alt="" />
//                 Explore Vite
//               </a>
//             </li>
//             <li>
//               <a href="https://react.dev/" target="_blank">
//                 <img className="button-icon" src={reactLogo} alt="" />
//                 Learn more
//               </a>
//             </li>
//           </ul>
//         </div>
//         <div id="social">
//           <svg className="icon" role="presentation" aria-hidden="true">
//             <use href="/icons.svg#social-icon"></use>
//           </svg>
//           <h2>Connect with us</h2>
//           <p>Join the Vite community</p>
//           <ul>
//             <li>
//               <a href="https://github.com/vitejs/vite" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#github-icon"></use>
//                 </svg>
//                 GitHub
//               </a>
//             </li>
//             <li>
//               <a href="https://chat.vite.dev/" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#discord-icon"></use>
//                 </svg>
//                 Discord
//               </a>
//             </li>
//             <li>
//               <a href="https://x.com/vite_js" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#x-icon"></use>
//                 </svg>
//                 X.com
//               </a>
//             </li>
//             <li>
//               <a href="https://bsky.app/profile/vite.dev" target="_blank">
//                 <svg
//                   className="button-icon"
//                   role="presentation"
//                   aria-hidden="true"
//                 >
//                   <use href="/icons.svg#bluesky-icon"></use>
//                 </svg>
//                 Bluesky
//               </a>
//             </li>
//           </ul>
//         </div>
//       </section>

//       <div className="ticks"></div>
//       <section id="spacer"></section>
//     </>
//   )
// }

// export default App


import { useState, useEffect } from "react";
import './index.css'

=======
import { useState, useEffect } from "react";
>>>>>>> fd6ff79 (feat(auth): add login and register pages):src/App.jsx

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  .app {
    min-height: 100vh;
    background: #08080a;
    color: #e2dfda;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
  }
  .syne { font-family: 'Syne', sans-serif; }

  .auth-wrap { min-height: 100vh; display: grid; grid-template-columns: 1fr 1fr; }
  .auth-left {
    background: #0c0c10;
    border-right: 1px solid #1a1a22;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 3rem;
  }
  .auth-right { display: flex; align-items: center; justify-content: center; padding: 3rem; }
  .auth-form-box { width: 100%; max-width: 360px; }

  .dash-wrap { display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }
  .sidebar {
    background: #0b0b0e;
    border-right: 1px solid #18181e;
    display: flex;
    flex-direction: column;
    padding: 2rem 0;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
  }
  .main { padding: 2.5rem 3rem; overflow-y: auto; }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 24px;
    color: #787891;
    cursor: pointer;
    transition: color 0.15s;
    border-left: 2px solid transparent;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    user-select: none;
  }
  .nav-item:hover { color: #908ca0; }
  .nav-item.active { color: #aaef5a; border-left-color: #aaef5a; }

  .field {
    width: 100%;
    background: #101014;
    border: 1px solid #20202a;
    color: #e2dfda;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    padding: 10px 14px;
    outline: none;
    transition: border-color 0.15s;
    border-radius: 0;
    -webkit-appearance: none;
  }
  .field:focus { border-color: #aaef5a; }
  .field::placeholder { color: #35333e; }

  .btn-primary {
    background: #aaef5a;
    color: #081400;
    border: none;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 12px 28px;
    cursor: pointer;
    transition: opacity 0.15s;
    border-radius: 0;
  }
  .btn-primary:hover { opacity: 0.82; }
  .btn-primary:active { opacity: 0.7; }

  .btn-ghost {
    background: transparent;
    border: 1px solid #20202a;
    color: #787891;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.06em;
    padding: 10px 20px;
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
    border-radius: 0;
  }
  .btn-ghost:hover { border-color: #aaef5a; color: #aaef5a; }

  .review-card {
    background: #0d0d11;
    border: 1px solid #18181e;
    padding: 18px 22px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 16px;
    margin-bottom: 10px;
  }
  .review-card:hover { border-color: #2a2a36; background: #0f0f14; }

  .score { font-size: 22px; font-weight: 700; font-family: 'Syne', sans-serif; }
  .score.high { color: #aaef5a; }
  .score.mid  { color: #f8c354; }
  .score.low  { color: #f87171; }

  .tag {
    display: inline-block;
    background: #18181e;
    color: #787891;
    font-size: 9px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 8px;
    margin-right: 6px;
  }

  .code-block {
    background: #060608;
    border: 1px solid #18181e;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #90d860;
    white-space: pre;
    overflow-x: auto;
    line-height: 1.8;
    text-align: left;
  }

  .readme-wrap {
    background: #0d0d11;
    border: 1px solid #18181e;
    padding: 28px 32px;
  }
  .readme-h1 { 
    font-family: 'Syne', sans-serif; 
    font-size: 20px; 
    font-weight: 800; 
    color: #f0ede5; 
    margin-bottom: 6px; 
    text-align: center; 
  }
  .readme-h2 {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #c0bcb5;
    margin: 28px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #20202a;
    text-align: center;
  }
  .readme-h3 {
    font-size: 10px;
    font-weight: 500;
    color: #aaef5a;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 18px 0 10px;
    text-align: left;
  }
  .readme-p { 
    color: #787891; 
    font-size: 12px; 
    line-height: 1.8; 
    margin-bottom: 10px; 
    text-align: left;
  }
  .readme-li {
    color: #787891;
    font-size: 12px;
    line-height: 1.75;
    padding-left: 16px;
    position: relative;
    margin-bottom: 6px;
    text-align: left;
  }
  .readme-li::before { content: '–'; position: absolute; left: 0; color: #aaef5a; }
  .readme-score {
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
    background: #13130f;
    border: 1px solid #2a2a1e;
    padding: 6px 14px;
    margin-bottom: 12px;
    text-align: left;
  }

  .divider { height: 1px; background: #18181e; margin: 1.5rem 0; }
  .mono-label {
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #787891;
    display: block;
    margin-bottom: 8px;
  }
  select.field {
    -webkit-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='11' height='11' viewBox='0 0 24 24' fill='none' stroke='%2350505e' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 14px center;
    padding-right: 38px;
    cursor: pointer;
  }
.loading-wrap {
  min-height: 100vh;
  background: #08080a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0;
}
.loading-message {
  font-size: 13px;
  color: #e2dfda;
  text-align: center;
  min-height: 24px;
  transition: opacity 0.3s ease;
}
.loading-message.fade { opacity: 0; }
.loading-bar-track {
  width: 280px;
  height: 1px;
  background: #18181e;
  margin-top: 32px;
  position: relative;
  overflow: hidden;
}
.loading-bar-fill {
  position: absolute;
  top: 0; left: 0;
  height: 100%;
  background: #aaef5a;
  transition: width 0.5s ease;
}
.loading-pulse {
  width: 8px; height: 8px;
  background: #aaef5a;
  border-radius: 50%;
  margin-bottom: 32px;
  animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.3; transform: scale(0.6); }
}
  textarea.field { resize: vertical; line-height: 1.65; }
`;

const reviews = [
  { id: 1, file: "auth_middleware.py", lang: "Python",     date: "May 10, 2026", score: 87, agentCount: 2 },
  { id: 2, file: "api_routes.js",      lang: "JavaScript", date: "May  9, 2026", score: 62, agentCount: 2 },
  { id: 3, file: "database.go",        lang: "Go",         date: "May  8, 2026", score: 94, agentCount: 2 },
  { id: 4, file: "user_service.ts",    lang: "TypeScript", date: "May  7, 2026", score: 78, agentCount: 2 },
];

const reviewResult = {
  revisedCode:
`from typing import Optional
import bcrypt
import os
from db import get_connection

SECRET_KEY = os.environ.get("SECRET_KEY")

def get_user(user_id: int) -> Optional[dict]:
    """
    Fetch a single user record by primary key.

    Args:
        user_id: The user's integer primary key.

    Returns:
        A dict of user fields, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.fetchone()

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def get_users_bulk(user_ids: list[int]) -> dict[int, dict]:
    """Batch-fetch users by a list of IDs. Avoids N+1 queries."""
    if not user_ids:
        return {}
    placeholders = ",".join(["%s"] * len(user_ids))
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM users WHERE id IN ({placeholders})",
            tuple(user_ids),
        )
        return {row["id"]: row for row in cursor.fetchall()}`,

  agentReports: [
    {
      label: "Agent A",
      originalScore: 54,
      identified: [
        "SQL injection vulnerability — raw user input interpolated directly into query strings.",
        "Hardcoded SECRET_KEY in source rather than being read from the environment.",
        "MD5 used for password hashing — cryptographically broken for this use case.",
      ],
      changed: [
        "Replaced f-string query interpolation with parameterised queries (%s placeholders).",
        "Moved SECRET_KEY to os.environ.get() — no secrets in source.",
        "Replaced MD5 with bcrypt via a verify_password() helper.",
      ],
    },
    {
      label: "Agent B",
      originalScore: 61,
      identified: [
        "N+1 query pattern — a DB call was executed per iteration inside a loop.",
        "No connection management — connections were opened but not guaranteed to close.",
        "Missing type annotations on all function signatures.",
        "No docstrings on any public method.",
      ],
      changed: [
        "Added get_users_bulk() — fetches a list of users in a single batch query.",
        "Wrapped all DB calls in a context manager (with get_connection()) to guarantee cleanup.",
        "Added full type hints to all function signatures.",
        "Added docstrings to all public functions describing args and return values.",
      ],
    },
  ],
};

const loadingSteps = [
  "Parsing your code structure…",
  "Our security agent is reviewing for vulnerabilities…",
  "Our performance agent is analysing efficiency…",
  "Our quality agent is checking maintainability…",
  "Agents are cross-referencing findings…",
  "Compiling the revised output…",
];

<<<<<<< HEAD:srcs/frontend/src/App.tsx
function getScoreClass(n: number) { return n >= 80 ? "high" : n >= 60 ? "mid" : "low"; }
=======
function getScoreClass(n) { return n >= 80 ? "high" : n >= 60 ? "mid" : "low"; }
>>>>>>> fd6ff79 (feat(auth): add login and register pages):src/App.jsx

function Dot() {
  return <div style={{ width: 8, height: 8, background: "#aaef5a", borderRadius: "50%", flexShrink: 0 }} />;
}
<<<<<<< HEAD:srcs/frontend/src/App.tsx
function Logo({ small }: { small?: boolean }) {
=======
function Logo({ small }) {
>>>>>>> fd6ff79 (feat(auth): add login and register pages):src/App.jsx
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
      <Dot />
      <span className="syne" style={{ fontSize: small ? 12 : 14, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" }}>
        Multigent
      </span>
    </div>
  );
}

export default function App() {
  const [screen,         setScreen]         = useState("auth");
  const [authMode,       setAuthMode]       = useState("login");
  const [activeNav,      setActiveNav]      = useState("dashboard");
<<<<<<< HEAD:srcs/frontend/src/App.tsx
  const [selectedReview, setSelectedReview] = useState<typeof reviews[0] | null>(null);
=======
  const [selectedReview, setSelectedReview] = useState(null);
>>>>>>> fd6ff79 (feat(auth): add login and register pages):src/App.jsx
  const [detailTab,      setDetailTab]      = useState("code");
  const [isLoading,    setIsLoading]    = useState(false);
  const [loadingStep,  setLoadingStep]  = useState(0);
  const [msgVisible,   setMsgVisible]   = useState(true);

<<<<<<< HEAD:srcs/frontend/src/App.tsx
  function goTo(nav: string) { setActiveNav(nav); setSelectedReview(null); }
  function openReview(r: typeof reviews[0]) { setSelectedReview(r); setDetailTab("code"); setActiveNav("dashboard"); }
=======
  function goTo(nav) { setActiveNav(nav); setSelectedReview(null); }
  function openReview(r) { setSelectedReview(r); setDetailTab("code"); setActiveNav("dashboard"); }
>>>>>>> fd6ff79 (feat(auth): add login and register pages):src/App.jsx

  useEffect(() => {
    if (!isLoading) return;

    setMsgVisible(true);

    const showTimer = setTimeout(() => {
      setMsgVisible(false);

      const advanceTimer = setTimeout(() => {
        if (loadingStep < loadingSteps.length - 1) {
          setLoadingStep(s => s + 1);
        } else {
          setIsLoading(false);
          setLoadingStep(0);
          openReview(reviews[0]);
        }
      }, 350);

      return () => clearTimeout(advanceTimer);
    }, 1200);

    return () => clearTimeout(showTimer);
  }, [isLoading, loadingStep]);

  /*AUTH*/
  if (screen === "auth") {
    return (
      <div className="app">
        <style>{css}</style>
        <div className="auth-wrap">
          <div className="auth-left">
            <div>
              <div style={{ marginBottom: 52 }}><Logo /></div>
              <h1 className="syne" style={{ fontSize: 44, fontWeight: 800, lineHeight: 1.08, color: "#f0ede5", marginBottom: 22 }}>
                Code reviewed<br />by a council<br />of agents.
              </h1>
              <p style={{ color: "#787891", lineHeight: 1.85, maxWidth: 310, fontSize: 12 }}>
                Paste any snippet. Multiple AI agents audit it for security, performance,
                and quality — then produce a single revised output together.
              </p>
            </div>
            <div>
              <div className="divider" />
              {[
                "Security & vulnerability analysis",
                "Performance & efficiency review",
                "Code quality & maintainability",
                "Unified revised output + agent README",
              ].map(t => (
                <div key={t} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 13 }}>
                  <div style={{ width: 4, height: 4, background: "#aaef5a", borderRadius: "50%", flexShrink: 0 }} />
                  <span style={{ color: "#787891", fontSize: 11 }}>{t}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="auth-right">
            <div className="auth-form-box">
              <div style={{ marginBottom: 32 }}>
                <h2 className="syne" style={{ fontSize: 26, fontWeight: 700, color: "#f0ede5", marginBottom: 6 }}>
                  {authMode === "login" ? "Sign in" : "Create account"}
                </h2>
                <p style={{ color: "#787891", fontSize: 12 }}>
                  {authMode === "login" ? "Welcome back." : "Start reviewing code in seconds."}
                </p>
              </div>

              {authMode === "register" && (
                <div style={{ marginBottom: 14 }}>
                  <label className="mono-label">Username</label>
                  <input className="field" type="text" placeholder="User123" />
                </div>
              )}
              <div style={{ marginBottom: 14 }}>
                <label className="mono-label">Email</label>
                <input className="field" type="email" placeholder="example@email.com" />
              </div>
              <div style={{ marginBottom: authMode === "register" ? 14 : 24 }}>
                <label className="mono-label">Password</label>
                <input className="field" type="password" placeholder="••••••••" />
              </div>
              {authMode === "register" && (
                <div style={{ marginBottom: 24 }}>
                  <label className="mono-label">Confirm password</label>
                  <input className="field" type="password" placeholder="••••••••" />
                </div>
              )}

              <button className="btn-primary" style={{ width: "100%" }}
                onClick={() => { setScreen("dashboard"); goTo("dashboard"); }}>
                →&nbsp;&nbsp;{authMode === "login" ? "Sign in" : "Create account"}
              </button>
              <div className="divider" />
              <p style={{ color: "#787891", fontSize: 11, textAlign: "center" }}>
                {authMode === "login" ? "No account yet? " : "Already have one? "}
                <span style={{ color: "#aaef5a", cursor: "pointer" }}
                  onClick={() => setAuthMode(authMode === "login" ? "register" : "login")}>
                  {authMode === "login" ? "Register" : "Sign in"}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /*DASHBOARD SHELL*/
  const navItems = [
    { id: "dashboard",  label: "Reviews",    icon: "▦" },
    { id: "new-review", label: "New review", icon: "+" },
    { id: "settings",   label: "Settings",   icon: "⊙" },
  ];

  if (isLoading) {
    const progress = ((loadingStep + 1) / loadingSteps.length) * 100;
    return (
      <div className="app">
        <style>{css}</style>
        <div className="loading-wrap">
          <Logo />
          <div style={{ marginTop: 48 }} />
          <div className="loading-pulse" />
          <p className={`loading-message ${msgVisible ? "" : "fade"}`}>
            {loadingSteps[loadingStep]}
          </p>
          <div className="loading-bar-track">
            <div className="loading-bar-fill" style={{ width: `${progress}%` }} />
          </div>
          <p style={{ marginTop: 16, fontSize: 10, color: "#30303e", letterSpacing: "0.08em" }}>
            {loadingStep + 1} / {loadingSteps.length}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <style>{css}</style>
      <div className="dash-wrap">

        <div className="sidebar">
          <div style={{ padding: "0 24px", marginBottom: 44 }}><Logo small /></div>
          <nav style={{ flex: 1 }}>
            {navItems.map(item => (
              <div key={item.id}
                className={`nav-item ${activeNav === item.id ? "active" : ""}`}
                onClick={() => goTo(item.id)}>
                <span style={{ fontSize: 13 }}>{item.icon}</span>
                {item.label}
              </div>
            ))}
          </nav>
          <div>
            <div className="divider" style={{ margin: "0 24px 14px" }} />
            <div style={{ padding: "0 24px", marginBottom: 8 }}>
              <div style={{ fontSize: 9, color: "#787891", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 4 }}>Signed in as</div>
              <div style={{ color: "#787891", fontSize: 11 }}>example@email.com</div>
            </div>
            <div className="nav-item" style={{ marginTop: 6 }} onClick={() => setScreen("auth")}>
              <span>↖</span> Sign out
            </div>
          </div>
        </div>

        <div className="main">

          {/*REVIEWS LIST*/}
          {activeNav === "dashboard" && !selectedReview && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 32 }}>
                <div>
                  <h1 className="syne" style={{ fontSize: 30, fontWeight: 800, color: "#f0ede5", marginBottom: 4 }}>Code Reviews</h1>
                  <p style={{ color: "#787891", fontSize: 11 }}>4 reviews this week · 2 agents per review</p>
                </div>
                <button className="btn-ghost" onClick={() => goTo("new-review")}>+ New review</button>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10, marginBottom: 32 }}>
                {[
                  { label: "Avg. score", value: "80", unit: "/100"      },
                  { label: "Reviews",    value: "4",  unit: "this week" },
                  { label: "Agents",     value: "2",  unit: "per review"},
                ].map(s => (
                  <div key={s.label} style={{ background: "#0d0d11", border: "1px solid #18181e", padding: "16px 20px" }}>
                    <div className="mono-label" style={{ marginBottom: 10 }}>{s.label}</div>
                    <div style={{ display: "flex", alignItems: "baseline", gap: 5 }}>
                      <span className="syne" style={{ fontSize: 30, fontWeight: 800, color: "#f0ede5" }}>{s.value}</span>
                      <span style={{ color: "#787891", fontSize: 11 }}>{s.unit}</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mono-label" style={{ marginBottom: 14 }}>Recent reviews</div>
              {reviews.map(r => (
                <div key={r.id} className="review-card" onClick={() => openReview(r)}>
                  <div>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                      <span style={{ color: "#f0ede5", fontSize: 14, fontWeight: 500 }}>{r.file}</span>
                      <span className="tag">{r.lang}</span>
                    </div>
                    <div style={{ color: "#787891", fontSize: 11 }}>{r.date} · {r.agentCount} agents</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div className={`score ${getScoreClass(r.score)}`}>{r.score}</div>
                    <div style={{ fontSize: 9, color: "#787891", textTransform: "uppercase", letterSpacing: "0.08em" }}>score</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/*REVIEW DETAIL*/}
          {activeNav === "dashboard" && selectedReview && (
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 32 }}>
                <span style={{ color: "#787891", cursor: "pointer", fontSize: 11 }}
                  onClick={() => setSelectedReview(null)}>← Back</span>
                <span style={{ color: "#28282e" }}>/</span>
                <span style={{ color: "#f0ede5", fontSize: 13 }}>{selectedReview.file}</span>
                <span className="tag">{selectedReview.lang}</span>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
                <div>
                  <h1 className="syne" style={{ fontSize: 26, fontWeight: 800, color: "#f0ede5", marginBottom: 4 }}>Review Output</h1>
                  <p style={{ color: "#787891", fontSize: 11 }}>{selectedReview.date} · {selectedReview.agentCount} agents</p>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ display: "flex", alignItems: "baseline", gap: 5 }}>
                    <span className={`score ${getScoreClass(selectedReview.score)}`} style={{ fontSize: 40 }}>
                      {selectedReview.score}
                    </span>
                    <span style={{ color: "#787891", fontSize: 13 }}>/100</span>
                  </div>
                  <div style={{ fontSize: 9, color: "#787891", textTransform: "uppercase", letterSpacing: "0.08em" }}>final score</div>
                </div>
              </div>

              <div style={{ display: "flex", borderBottom: "1px solid #18181e", marginBottom: 28, gap: 2 }}>
                {[{ id: "code", label: "Revised code" }, { id: "readme", label: "Agent README" }].map(t => (
                  <div key={t.id}
                    style={{
                      padding: "8px 20px",
                      borderBottom: `2px solid ${detailTab === t.id ? "#aaef5a" : "transparent"}`,
                      cursor: "pointer",
                      color: detailTab === t.id ? "#aaef5a" : "#787891",
                      fontSize: 11,
                      letterSpacing: "0.06em",
                      transition: "color 0.15s, border-color 0.15s",
                      userSelect: "none",
                    }}
                    onClick={() => setDetailTab(t.id)}>
                    {t.label}
                  </div>
                ))}
              </div>

              {detailTab === "code" && (
                <div>
                  <div className="mono-label" style={{ marginBottom: 10 }}>
                    Final output — revised by {selectedReview.agentCount} agents
                  </div>
                  <div className="code-block">{reviewResult.revisedCode}</div>
                </div>
              )}

              {detailTab === "readme" && (
                <div className="readme-wrap">
                  <div className="readme-h1">{selectedReview.file}</div>
                  <p className="readme-p" style={{ marginTop: 6 }}>
                    Reviewed by {selectedReview.agentCount} agents.
                    Each agent's findings, original score, and changes are documented below.
                  </p>

                  {reviewResult.agentReports.map((agent, idx) => (
                    <div key={idx}>
                      <div className="readme-h2">{agent.label}</div>

                      <div className="readme-score">
                        <span style={{ fontSize: 9, color: "#60603e", letterSpacing: "0.08em", textTransform: "uppercase" }}>
                          Original score
                        </span>
                        <span className={`score ${getScoreClass(agent.originalScore)}`}
                          style={{ fontSize: 20 }}>
                          {agent.originalScore}
                        </span>
                        <span style={{ color: "#40403e", fontSize: 11 }}>/100</span>
                      </div>

                      <div className="readme-h3">What was identified</div>
                      {agent.identified.map((item, i) => (
                        <div key={i} className="readme-li">{item}</div>
                      ))}

                      <div className="readme-h3">What was changed</div>
                      {agent.changed.map((item, i) => (
                        <div key={i} className="readme-li">{item}</div>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/*NEW REVIEW*/}
          {activeNav === "new-review" && (
            <div style={{ maxWidth: 700 }}>
              <div style={{ marginBottom: 32 }}>
                <h1 className="syne" style={{ fontSize: 30, fontWeight: 800, color: "#f0ede5", marginBottom: 4 }}>New Review</h1>
                <p style={{ color: "#787891", fontSize: 11 }}>
                  Paste your code below. All agents will review it simultaneously and produce a unified revised output.
                </p>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
                <div>
                  <label className="mono-label">Language</label>
                  <select className="field">
                    {["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++", "Other"].map(l => (
                      <option key={l}>{l}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="mono-label">Review focus</label>
                  <select className="field">
                    {["All checks", "Security only", "Performance only", "Code quality only"].map(l => (
                      <option key={l}>{l}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div style={{ marginBottom: 28 }}>
                <label className="mono-label">Code snippet</label>
                <textarea className="field" style={{ height: 360, fontSize: 12 }}
                  placeholder={"# Paste your code here…\n\ndef example():\n    pass"} />
              </div>

              <div className="divider" />

              <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
                <button className="btn-primary" onClick={() => { setIsLoading(true); setLoadingStep(0); setMsgVisible(true); }}>
                  →&nbsp;&nbsp;Submit for review
                </button>
                <span style={{ color: "#30303e", fontSize: 11 }}>2 agents · ~30 s</span>
              </div>
            </div>
          )}

          {/*SETTINGS*/}
          {activeNav === "settings" && (
            <div style={{ maxWidth: 520 }}>
              <div style={{ marginBottom: 32 }}>
                <h1 className="syne" style={{ fontSize: 30, fontWeight: 800, color: "#f0ede5", marginBottom: 4 }}>Settings</h1>
              </div>
              {[
                { section: "Account",     fields: [{ label: "Username", val: "User123" }, { label: "Email", val: "jane@company.com" }] },
                { section: "Preferences", fields: [{ label: "Default language", val: "Python" }, { label: "Default review focus", val: "All checks" }] },
              ].map(group => (
                <div key={group.section} style={{ marginBottom: 32 }}>
                  <div className="mono-label" style={{ marginBottom: 14 }}>{group.section}</div>
                  {group.fields.map(f => (
                    <div key={f.label} style={{ marginBottom: 14 }}>
                      <label className="mono-label">{f.label}</label>
                      <input className="field" defaultValue={f.val} />
                    </div>
                  ))}
                </div>
              ))}
              <div className="divider" />
              <button className="btn-primary">Save changes</button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}