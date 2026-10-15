"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface QuizSessionItem {
  sessionId: string;
  chatId: number;
  groupTitle?: string;
  quizId: string;
  quizTitle: string;
  totalQuestions: number;
  participantsCount: number;
  winner?: {
    name: string;
    username: string | null;
    score: number;
  } | null;
  status: string;
  createdAt: string;
}

interface LeaderboardEntry {
  rank: number;
  userId: number;
  name: string;
  username: string | null;
  score: number;
  totalQuestions: number;
  totalTimeSeconds: number;
  accuracy: number;
}

export default function ResultsPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

  // Ma'lumotlar
  const [sessions, setSessions] = useState<QuizSessionItem[]>([]);
  const [quizzes, setQuizzes] = useState<Array<{ id: string; title: string }>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filtrlar
  const [selectedQuizId, setSelectedQuizId] = useState("all");
  const [chatIdFilter, setChatIdFilter] = useState("");

  // Sessiya reytingi modali
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [selectedSessionTitle, setSelectedSessionTitle] = useState<string>("");
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loadingLeaderboard, setLoadingLeaderboard] = useState(false);

  useEffect(() => {
    fetch("/api/auth/me")
      .then((res) => {
        if (!res.ok) router.push("/login");
        return res.json();
      })
      .then((data) => {
        if (data.ok) setAdminUser(data.user);
      })
      .catch(() => router.push("/login"));

    fetchResults();
  }, [router]);

  const fetchResults = async (quizFilter?: string, chatFilter?: string) => {
    setLoading(true);
    setError(null);
    try {
      const q = quizFilter !== undefined ? quizFilter : selectedQuizId;
      const c = chatFilter !== undefined ? chatFilter : chatIdFilter;

      const params = new URLSearchParams();
      if (q && q !== "all") params.set("quizId", q);
      if (c && c.trim()) params.set("chatId", c.trim());

      const res = await fetch(`/api/results?${params.toString()}`, {
        signal: AbortSignal.timeout(15000),
      });
      const data = await res.json();

      if (res.ok && data.ok) {
        setSessions(data.sessions || []);
        if (data.quizzes && data.quizzes.length > 0) {
          setQuizzes(data.quizzes);
        }
      } else {
        setError(data.message || "Natijalarni yuklashda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setLoading(false);
    }
  };

  const handleOpenLeaderboard = async (session: QuizSessionItem) => {
    setSelectedSessionId(session.sessionId);
    setSelectedSessionTitle(`${session.groupTitle || `Guruh ${session.chatId}`} — ${session.quizTitle}`);
    setLeaderboard([]);
    setLoadingLeaderboard(true);

    try {
      const res = await fetch(`/api/results/${encodeURIComponent(session.sessionId)}`, {
        signal: AbortSignal.timeout(12000),
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        setLeaderboard(data.leaderboard || []);
      }
    } catch {
      // xato holati
    } finally {
      setLoadingLeaderboard(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Natijalar & Reyting Tahlili"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div style={{ marginBottom: "1.5rem" }}>
            <h1 style={{ fontSize: "1.5rem", fontWeight: 700 }}>🏆 O&apos;tkazilgan Quizlar & Natijalar</h1>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
              Telegram guruhlarida o&apos;tkazilgan testlar, qatnashuvchilar ballari va reyting jadvali
            </p>
          </div>

          {error && <div className="alert alert-danger" style={{ marginBottom: "1.5rem" }}>{error}</div>}

          {/* Filtrlar paneli */}
          <div className="content-card">
            <div className="card-header">
              <h3 className="card-title">🔍 Filtrlash va Qidiruv</h3>
              <button
                type="button"
                onClick={() => fetchResults()}
                className="btn btn-outline"
                style={{ fontSize: "0.8rem", padding: "0.35rem 0.75rem" }}
              >
                🔄 Yangilash
              </button>
            </div>
            <div style={{ padding: "1.25rem", display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center" }}>
              {/* Test bo'yicha filter */}
              <div style={{ minWidth: "220px", flex: 1 }}>
                <label style={{ display: "block", fontSize: "0.8rem", color: "var(--text-muted)", marginBottom: "4px" }}>
                  Test bo&apos;yicha:
                </label>
                <select
                  value={selectedQuizId}
                  onChange={(e) => {
                    setSelectedQuizId(e.target.value);
                    fetchResults(e.target.value, chatIdFilter);
                  }}
                  style={{
                    width: "100%",
                    padding: "0.5rem 0.85rem",
                    background: "var(--bg-card)",
                    border: "1px solid var(--border-color)",
                    color: "var(--text-primary)",
                    borderRadius: "var(--radius-sm)",
                    fontSize: "0.875rem",
                  }}
                >
                  <option value="all">Barcha testlar (32 ta to&apos;plam)</option>
                  {quizzes.map((q) => (
                    <option key={q.id} value={q.id}>
                      {q.id}: {q.title}
                    </option>
                  ))}
                </select>
              </div>

              {/* Chat ID bo'yicha filter */}
              <div style={{ minWidth: "200px", flex: 1 }}>
                <label style={{ display: "block", fontSize: "0.8rem", color: "var(--text-muted)", marginBottom: "4px" }}>
                  Guruh Chat ID:
                </label>
                <input
                  type="text"
                  placeholder="Masalan: -100123456789"
                  value={chatIdFilter}
                  onChange={(e) => setChatIdFilter(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") fetchResults(selectedQuizId, chatIdFilter);
                  }}
                  style={{
                    width: "100%",
                    padding: "0.5rem 0.85rem",
                    background: "var(--bg-card)",
                    border: "1px solid var(--border-color)",
                    color: "var(--text-primary)",
                    borderRadius: "var(--radius-sm)",
                    fontSize: "0.875rem",
                  }}
                />
              </div>

              <div style={{ alignSelf: "flex-end" }}>
                <button
                  type="button"
                  onClick={() => fetchResults(selectedQuizId, chatIdFilter)}
                  className="btn btn-primary"
                  style={{ padding: "0.5rem 1rem" }}
                >
                  Qidirish
                </button>
              </div>
            </div>
          </div>

          {/* O'tkazilgan quizlar ro'yxati */}
          <div className="content-card">
            <div className="card-header">
              <h3 className="card-title">📊 O&apos;tkazilgan Sessiyalar Ro&apos;yxati ({sessions.length})</h3>
            </div>
            <div className="table-responsive">
              {loading ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
                  ⏳ Natijalar yuklanmoqda...
                </div>
              ) : sessions.length === 0 ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
                  Hech qanday quiz sessiyalari topilmadi.
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Sana va Vaqt</th>
                      <th>Guruh</th>
                      <th>Quiz Nomi</th>
                      <th>Savollar</th>
                      <th>Qatnashuvchilar</th>
                      <th>1-o&apos;rin G&apos;olibi</th>
                      <th>Harakat</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sessions.map((sess) => (
                      <tr key={sess.sessionId}>
                        <td style={{ fontSize: "0.8rem", whiteSpace: "nowrap" }}>
                          {new Date(sess.createdAt).toLocaleString("uz-UZ")}
                        </td>
                        <td>
                          <div style={{ fontWeight: 600 }}>{sess.groupTitle || `Guruh ${sess.chatId}`}</div>
                          <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>ID: {sess.chatId}</div>
                        </td>
                        <td>
                          <span className="badge badge-next" style={{ fontSize: "0.72rem", marginBottom: "2px" }}>
                            {sess.quizId}
                          </span>
                          <div style={{ fontSize: "0.8rem" }}>{sess.quizTitle}</div>
                        </td>
                        <td>{sess.totalQuestions} ta</td>
                        <td>
                          <b style={{ color: "#38bdf8" }}>{sess.participantsCount}</b> nafar
                        </td>
                        <td>
                          {sess.winner ? (
                            <div>
                              <span>🥇 <b>{sess.winner.name}</b></span>{" "}
                              <span style={{ color: "var(--success)", fontWeight: 600 }}>
                                ({sess.winner.score} ball)
                              </span>
                            </div>
                          ) : (
                            <span style={{ color: "var(--text-muted)" }}>—</span>
                          )}
                        </td>
                        <td>
                          <button
                            type="button"
                            onClick={() => handleOpenLeaderboard(sess)}
                            className="btn btn-outline"
                            style={{ padding: "0.35rem 0.75rem", fontSize: "0.8rem" }}
                          >
                            📈 Reyting
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Sessiya reytingi modali */}
      {selectedSessionId && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: "1rem" }}>
          <div style={{ background: "var(--bg-secondary)", border: "1px solid var(--border-color)", borderRadius: "var(--radius-md)", maxWidth: "680px", width: "100%", maxHeight: "90vh", display: "flex", flexDirection: "column", boxShadow: "0 10px 25px rgba(0,0,0,0.6)" }}>
            <div style={{ padding: "1.25rem 1.5rem", borderBottom: "1px solid var(--border-color)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 700 }}>🏆 Sessiya Reyting Jadvali</h3>
                <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>{selectedSessionTitle}</div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedSessionId(null)}
                style={{ background: "none", border: "none", color: "var(--text-secondary)", fontSize: "1.2rem", cursor: "pointer" }}
              >
                ✕
              </button>
            </div>

            <div style={{ padding: "1.25rem", overflowY: "auto", flex: 1 }}>
              {loadingLeaderboard ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>Yuklanmoqda...</div>
              ) : leaderboard.length === 0 ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
                  Ushbu sessiya bo&apos;yicha hali natijalar mavjud emas.
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th style={{ width: "60px" }}>O&apos;rin</th>
                      <th>Ishtirokchi</th>
                      <th>Ball</th>
                      <th>Sof Vaqt</th>
                      <th>Aniqlik</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map((entry) => (
                      <tr key={entry.userId}>
                        <td style={{ fontWeight: 700 }}>
                          {entry.rank === 1 ? "🥇 1" : entry.rank === 2 ? "🥈 2" : entry.rank === 3 ? "🥉 3" : entry.rank}
                        </td>
                        <td>
                          <div style={{ fontWeight: 600 }}>{entry.name}</div>
                          {entry.username && (
                            <div style={{ fontSize: "0.75rem", color: "var(--primary)" }}>@{entry.username}</div>
                          )}
                        </td>
                        <td>
                          <b style={{ color: "#34d399" }}>{entry.score}</b> / {entry.totalQuestions}
                        </td>
                        <td style={{ fontSize: "0.85rem" }}>
                          ⏱️ {entry.totalTimeSeconds}s
                        </td>
                        <td>
                          <span
                            className={entry.accuracy >= 80 ? "badge badge-success" : entry.accuracy >= 50 ? "badge badge-warning" : "badge badge-danger"}
                            style={{ fontSize: "0.75rem" }}
                          >
                            {entry.accuracy}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            <div style={{ padding: "1rem 1.5rem", borderTop: "1px solid var(--border-color)", display: "flex", justifyContent: "flex-end" }}>
              <button type="button" onClick={() => setSelectedSessionId(null)} className="btn btn-outline">
                Yopish
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
