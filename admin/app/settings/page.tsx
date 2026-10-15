"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface AuditLogItem {
  id?: string;
  admin: string;
  action: string;
  details?: Record<string, any>;
  ip?: string;
  timestamp: string;
}

interface BotSettings {
  subscriptionChannels: Array<{ username: string; title: string }>;
  defaultQuestionTimeSeconds: number;
  botUsername: string;
  adminGoogleEmail: string;
  adminTelegramId: string | null;
  environment: string;
}

export default function SettingsPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

  const [settings, setSettings] = useState<BotSettings | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

    fetchSettingsAndLogs();
  }, [router]);

  const fetchSettingsAndLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const [settingsRes, logsRes] = await Promise.all([
        fetch("/api/settings", { signal: AbortSignal.timeout(10000) }),
        fetch("/api/audit-logs", { signal: AbortSignal.timeout(10000) }),
      ]);

      const settingsData = await settingsRes.json();
      const logsData = await logsRes.json();

      if (settingsRes.ok && settingsData.ok) {
        setSettings(settingsData.settings);
      }
      if (logsRes.ok && logsData.ok) {
        setAuditLogs(logsData.logs || []);
      }
    } catch {
      setError("Sozlamalar va audit loglarini yuklashda xatolik yuz berdi.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Sozlamalar & Audit Tarixi"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div style={{ marginBottom: "1.5rem" }}>
            <h1 style={{ fontSize: "1.5rem", fontWeight: 700 }}>⚙️ Bot Sozlamalari & Audit Jurnali</h1>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
              Bot konfiguratsiyasi, majburiy kanallar va admin harakatlari xavfsizlik tarixi
            </p>
          </div>

          {error && <div className="alert alert-danger" style={{ marginBottom: "1.5rem" }}>{error}</div>}

          {/* 1. Bot konfiguratsiyasi kartochkalari */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "1.5rem", marginBottom: "1.5rem" }}>
            {/* Majburiy kanallar */}
            <div className="content-card" style={{ marginBottom: 0 }}>
              <div className="card-header">
                <h3 className="card-title">📢 Majburiy Obuna Kanallari</h3>
                <span className="badge badge-success">Faol</span>
              </div>
              <div style={{ padding: "1.25rem" }}>
                <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
                  Faqat bot bilan shaxsiy chat ochgan a&apos;zolarga tegishli (guruhlardagi quizlarda talab qilinmaydi):
                </p>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {settings?.subscriptionChannels.map((ch, idx) => (
                    <div
                      key={idx}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        background: "var(--bg-card)",
                        padding: "0.75rem 1rem",
                        borderRadius: "var(--radius-sm)",
                        border: "1px solid var(--border-color)",
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: 600, fontSize: "0.9rem" }}>{ch.title}</div>
                        <div style={{ fontSize: "0.8rem", color: "var(--primary)" }}>{ch.username}</div>
                      </div>
                      <a
                        href={`https://t.me/${ch.username.replace("@", "")}`}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-outline"
                        style={{ fontSize: "0.75rem", padding: "0.3rem 0.65rem" }}
                      >
                        Ochish ↗
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Asosiy parametrlar */}
            <div className="content-card" style={{ marginBottom: 0 }}>
              <div className="card-header">
                <h3 className="card-title">⚡ Asosiy Parametrlar & Xavfsizlik</h3>
              </div>
              <div style={{ padding: "1.25rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "0.5rem 0", borderBottom: "1px solid var(--border-color)" }}>
                  <span style={{ color: "var(--text-secondary)", fontSize: "0.85rem" }}>Standart savol taymeri:</span>
                  <b style={{ color: "#38bdf8" }}>{settings?.defaultQuestionTimeSeconds ?? 20} soniya</b>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "0.5rem 0", borderBottom: "1px solid var(--border-color)" }}>
                  <span style={{ color: "var(--text-secondary)", fontSize: "0.85rem" }}>Telegram Bot Username:</span>
                  <b>@{settings?.botUsername ?? "jdakimyoquizbot"}</b>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "0.5rem 0", borderBottom: "1px solid var(--border-color)" }}>
                  <span style={{ color: "var(--text-secondary)", fontSize: "0.85rem" }}>Asosiy Admin Google:</span>
                  <b style={{ color: "#34d399" }}>{settings?.adminGoogleEmail ?? "diyorbekjabborov84@gmail.com"}</b>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "0.5rem 0" }}>
                  <span style={{ color: "var(--text-secondary)", fontSize: "0.85rem" }}>Tizim Muhiti:</span>
                  <span className="badge badge-next">{settings?.environment || "production"}</span>
                </div>
              </div>
            </div>
          </div>

          {/* 2. Admin harakatlari jurnali (Audit Logs) */}
          <div className="content-card">
            <div className="card-header">
              <h3 className="card-title">🛡️ Admin Harakatlari Jurnali (Audit Log)</h3>
              <button
                type="button"
                onClick={fetchSettingsAndLogs}
                className="btn btn-outline"
                style={{ fontSize: "0.8rem", padding: "0.35rem 0.75rem" }}
              >
                🔄 Yangilash
              </button>
            </div>
            <div className="table-responsive">
              {loading ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
                  ⏳ Loglar yuklanmoqda...
                </div>
              ) : auditLogs.length === 0 ? (
                <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-muted)" }}>
                  Hozircha hech qanday admin amallari qayd etilmagan.
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Vaqt</th>
                      <th>Admin</th>
                      <th>Amal (Action)</th>
                      <th>Tafsilotlar</th>
                    </tr>
                  </thead>
                  <tbody>
                    {auditLogs.map((log, idx) => (
                      <tr key={log.id || idx}>
                        <td style={{ fontSize: "0.8rem", whiteSpace: "nowrap" }}>
                          {new Date(log.timestamp).toLocaleString("uz-UZ")}
                        </td>
                        <td>
                          <b>{log.admin}</b>
                        </td>
                        <td>
                          <span
                            className={
                              log.action.includes("BROADCAST")
                                ? "badge badge-success"
                                : log.action.includes("SETTINGS")
                                ? "badge badge-warning"
                                : "badge badge-next"
                            }
                            style={{ fontSize: "0.725rem" }}
                          >
                            {log.action}
                          </span>
                        </td>
                        <td style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                          {log.details ? (
                            <span>
                              {Object.entries(log.details)
                                .map(([k, v]) => `${k}: ${v}`)
                                .join(" | ")}
                            </span>
                          ) : (
                            "—"
                          )}
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
    </div>
  );
}
