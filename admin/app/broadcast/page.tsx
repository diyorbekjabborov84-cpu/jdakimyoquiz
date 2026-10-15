"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface BroadcastButton {
  text: string;
  url: string;
}

interface BroadcastHistoryItem {
  id: string;
  target: string;
  message: string;
  imageUrl?: string;
  buttons?: BroadcastButton[];
  totalTargets: number;
  successful: number;
  failed: number;
  admin: string;
  sentAt: string;
}

function formatTelegramPreviewHtml(text: string): string {
  if (!text) return "";
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return escaped
    .replace(/&lt;(\/?(?:b|strong|i|em|u|ins|s|strike|del|code|pre))&gt;/gi, "<$1>")
    .replace(/&lt;a\s+href=&quot;(.*?)&quot;&gt;/gi, '<a href="$1" target="_blank" rel="noreferrer" style="color: #64b5f6; text-decoration: underline;">')
    .replace(/&lt;a\s+href=&#39;(.*?)&#39;&gt;/gi, '<a href="$1" target="_blank" rel="noreferrer" style="color: #64b5f6; text-decoration: underline;">')
    .replace(/&lt;\/a&gt;/gi, "</a>")
    .replace(/\n/g, "<br/>");
}

export default function BroadcastPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

  // Form holati
  const [target, setTarget] = useState<"all_groups" | "private_users" | "selected_groups">("all_groups");
  const [selectedChatIdsInput, setSelectedChatIdsInput] = useState("");
  const [messageText, setMessageText] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [buttons, setButtons] = useState<BroadcastButton[]>([]);
  const [newBtnText, setNewBtnText] = useState("");
  const [newBtnUrl, setNewBtnUrl] = useState("");

  // Amallar va xatoliklar
  const [sending, setSending] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [sendResult, setSendResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Tarix
  const [history, setHistory] = useState<BroadcastHistoryItem[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  // Auth va tarixni yuklash
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

    fetchHistory();
  }, [router]);

  const fetchHistory = async () => {
    try {
      setLoadingHistory(true);
      const res = await fetch("/api/broadcast/history", {
        signal: AbortSignal.timeout(10000),
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        setHistory(data.history || []);
      }
    } catch {
      // Tarix yuklanmasa ham forma ishlaydi
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleAddButton = () => {
    if (!newBtnText.trim() || !newBtnUrl.trim()) return;
    setButtons([...buttons, { text: newBtnText.trim(), url: newBtnUrl.trim() }]);
    setNewBtnText("");
    setNewBtnUrl("");
  };

  const handleRemoveButton = (index: number) => {
    setButtons(buttons.filter((_, i) => i !== index));
  };

  const handleSendBroadcast = async () => {
    setShowConfirmModal(false);
    setSending(true);
    setError(null);
    setSendResult(null);

    let selectedChatIds: number[] | undefined;
    if (target === "selected_groups") {
      selectedChatIds = selectedChatIdsInput
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !isNaN(n) && n !== 0);

      if (!selectedChatIds.length) {
        setError("Kamida bitta yaroqli guruh IDsi kiritilishi shart.");
        setSending(false);
        return;
      }
    }

    try {
      const res = await fetch("/api/broadcast", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: AbortSignal.timeout(60000),
        body: JSON.stringify({
          target,
          selectedChatIds,
          message: messageText,
          imageUrl: imageUrl.trim() || undefined,
          buttons: buttons.length ? buttons : undefined,
        }),
      });

      const data = await res.json();
      if (res.ok && data.ok) {
        setSendResult(data.result);
        setMessageText("");
        setImageUrl("");
        setButtons([]);
        fetchHistory();
      } else {
        setError(data.message || "Xabar tarqatishda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Umumiy xabarnoma (Broadcast)"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div style={{ marginBottom: "1.5rem" }}>
            <h1 style={{ fontSize: "1.5rem", fontWeight: 700 }}>📢 Umumiy Xabarnoma Yuborish</h1>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
              Bot a&apos;zo bo&apos;lgan barcha guruhlarga yoki shaxsiy foydalanuvchilarga xavfsiz va tezkor e&apos;lon tarqatish
            </p>
          </div>

          {error && <div className="alert alert-danger" style={{ marginBottom: "1.5rem" }}>{error}</div>}

          {sendResult && (
            <div className="alert alert-info" style={{ marginBottom: "1.5rem", background: "rgba(16, 185, 129, 0.15)", border: "1px solid #10b981" }}>
              <div style={{ fontWeight: 600, color: "#34d399", marginBottom: "4px" }}>
                ✅ Xabarnoma muvaffaqiyatli tarqatildi!
              </div>
              <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                Jami manzillar: <b>{sendResult.totalTargets}</b> | Muvaffaqiyatli: <b style={{ color: "#34d399" }}>{sendResult.successful}</b> | Xatolik: <b style={{ color: "#f87171" }}>{sendResult.failed}</b>
              </div>
            </div>
          )}

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "1.5rem", marginBottom: "2rem" }}>
            {/* 1. Xabar tuzish formasi */}
            <div className="content-card" style={{ marginBottom: 0 }}>
              <div className="card-header">
                <h3 className="card-title">📝 Xabar Parametrlari</h3>
              </div>
              <div style={{ padding: "1.25rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
                {/* Auditoriya */}
                <div>
                  <label style={{ display: "block", fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.4rem", color: "var(--text-secondary)" }}>
                    Auditoriya:
                  </label>
                  <select
                    value={target}
                    onChange={(e: any) => setTarget(e.target.value)}
                    style={{
                      width: "100%",
                      padding: "0.55rem 0.85rem",
                      background: "var(--bg-card)",
                      border: "1px solid var(--border-color)",
                      color: "var(--text-primary)",
                      borderRadius: "var(--radius-sm)",
                      fontSize: "0.875rem",
                    }}
                  >
                    <option value="all_groups">👥 Barcha faol guruhlar</option>
                    <option value="private_users">👤 Shaxsiy bot ochgan foydalanuvchilar</option>
                    <option value="selected_groups">🎯 Tanlangan aniq guruhlar (ID bo&apos;yicha)</option>
                  </select>
                </div>

                {target === "selected_groups" && (
                  <div>
                    <label style={{ display: "block", fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.4rem", color: "var(--text-secondary)" }}>
                      Guruh ID lari (vergul bilan ajrating):
                    </label>
                    <input
                      type="text"
                      placeholder="-1001234567890, -1009876543210"
                      value={selectedChatIdsInput}
                      onChange={(e) => setSelectedChatIdsInput(e.target.value)}
                      style={{
                        width: "100%",
                        padding: "0.55rem 0.85rem",
                        background: "var(--bg-card)",
                        border: "1px solid var(--border-color)",
                        color: "var(--text-primary)",
                        borderRadius: "var(--radius-sm)",
                        fontSize: "0.875rem",
                      }}
                    />
                  </div>
                )}

                {/* Xabar matni */}
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.4rem" }}>
                    <label style={{ fontSize: "0.85rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                      Xabar matni (HTML ruxsat etilgan):
                    </label>
                    <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>{messageText.length} belgi</span>
                  </div>
                  <textarea
                    rows={6}
                    placeholder="Masalan: 🧪 <b>Yangi Kimyo Quizi e'lon qilindi!</b>&#10;&#10;Barcha guruh a'zolari /quiz_KK5_1 buyrug'i orqali qatnashishlari mumkin."
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    style={{
                      width: "100%",
                      padding: "0.65rem 0.85rem",
                      background: "var(--bg-card)",
                      border: "1px solid var(--border-color)",
                      color: "var(--text-primary)",
                      borderRadius: "var(--radius-sm)",
                      fontSize: "0.875rem",
                      fontFamily: "inherit",
                    }}
                  />
                  <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginTop: "4px" }}>
                    Teglar: <code>&lt;b&gt;qalin&lt;/b&gt;</code>, <code>&lt;i&gt;kursiv&lt;/i&gt;</code>, <code>&lt;code&gt;kod&lt;/code&gt;</code>, <code>&lt;a href=&quot;...&quot;&gt;havola&lt;/a&gt;</code>
                  </div>
                </div>

                {/* Rasm URL */}
                <div>
                  <label style={{ display: "block", fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.4rem", color: "var(--text-secondary)" }}>
                    Rasm URL (ixtiyoriy poster/infografika):
                  </label>
                  <input
                    type="url"
                    placeholder="https://example.com/poster.jpg"
                    value={imageUrl}
                    onChange={(e) => setImageUrl(e.target.value)}
                    style={{
                      width: "100%",
                      padding: "0.55rem 0.85rem",
                      background: "var(--bg-card)",
                      border: "1px solid var(--border-color)",
                      color: "var(--text-primary)",
                      borderRadius: "var(--radius-sm)",
                      fontSize: "0.875rem",
                    }}
                  />
                </div>

                {/* Inline tugmalar */}
                <div>
                  <label style={{ display: "block", fontSize: "0.85rem", fontWeight: 600, marginBottom: "0.4rem", color: "var(--text-secondary)" }}>
                    Inline Tugmalar (ixtiyoriy havolalar):
                  </label>
                  <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
                    <input
                      type="text"
                      placeholder="Tugma matni (masalan: 🧪 Testni boshlash)"
                      value={newBtnText}
                      onChange={(e) => setNewBtnText(e.target.value)}
                      style={{
                        flex: 1,
                        padding: "0.45rem 0.65rem",
                        background: "var(--bg-card)",
                        border: "1px solid var(--border-color)",
                        color: "var(--text-primary)",
                        borderRadius: "var(--radius-sm)",
                        fontSize: "0.8rem",
                      }}
                    />
                    <input
                      type="url"
                      placeholder="https://t.me/..."
                      value={newBtnUrl}
                      onChange={(e) => setNewBtnUrl(e.target.value)}
                      style={{
                        flex: 1,
                        padding: "0.45rem 0.65rem",
                        background: "var(--bg-card)",
                        border: "1px solid var(--border-color)",
                        color: "var(--text-primary)",
                        borderRadius: "var(--radius-sm)",
                        fontSize: "0.8rem",
                      }}
                    />
                    <button type="button" onClick={handleAddButton} className="btn btn-outline" style={{ padding: "0.45rem 0.8rem", fontSize: "0.8rem" }}>
                      ➕ Qo&apos;shish
                    </button>
                  </div>

                  {buttons.length > 0 && (
                    <div style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
                      {buttons.map((b, idx) => (
                        <div key={idx} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "var(--bg-card)", padding: "0.4rem 0.75rem", borderRadius: "var(--radius-sm)", fontSize: "0.8rem" }}>
                          <span>🔘 <b>{b.text}</b> ➔ <span style={{ color: "var(--primary)" }}>{b.url}</span></span>
                          <button type="button" onClick={() => handleRemoveButton(idx)} style={{ background: "none", border: "none", color: "#f87171", cursor: "pointer", fontSize: "0.9rem" }}>✕</button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Yuborish tugmasi */}
                <button
                  type="button"
                  disabled={sending || !messageText.trim()}
                  onClick={() => setShowConfirmModal(true)}
                  className="btn btn-primary"
                  style={{
                    padding: "0.75rem",
                    fontSize: "0.95rem",
                    fontWeight: 600,
                    marginTop: "0.5rem",
                    cursor: sending || !messageText.trim() ? "not-allowed" : "pointer",
                    background: "linear-gradient(135deg, #3b82f6, #2563eb)",
                  }}
                >
                  {sending ? "⏳ Xabar yuborilmoqda..." : "🚀 Xabarnomani Yuborish"}
                </button>
              </div>
            </div>

            {/* 2. Jonli Telegram Ko'rinishi (Live Preview) */}
            <div className="content-card" style={{ marginBottom: 0 }}>
              <div className="card-header">
                <h3 className="card-title">📱 Telegramda Ko&apos;rinishi (Jonli Preview)</h3>
              </div>
              <div style={{ padding: "1.25rem", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "360px", background: "#0e1621" }}>
                <div style={{ maxWidth: "340px", width: "100%", background: "#182533", borderRadius: "12px", overflow: "hidden", boxShadow: "0 6px 16px rgba(0,0,0,0.4)" }}>
                  {/* Bot sarlavhasi */}
                  <div style={{ padding: "10px 14px", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", alignItems: "center", gap: "8px" }}>
                    <div style={{ width: "32px", height: "32px", borderRadius: "50%", background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "16px" }}>
                      ⚗️
                    </div>
                    <div>
                      <div style={{ fontSize: "0.85rem", fontWeight: 600, color: "#fff" }}>JDA Kimyo Quiz Boti</div>
                      <div style={{ fontSize: "0.7rem", color: "#6c7883" }}>bot</div>
                    </div>
                  </div>

                  {/* Rasm mavjud bo'lsa */}
                  {imageUrl && (
                    <div style={{ width: "100%", maxHeight: "200px", overflow: "hidden", background: "#111b24", display: "flex", alignItems: "center", justifyContent: "center" }}>
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        src={imageUrl}
                        alt="Poster preview"
                        style={{ width: "100%", height: "auto", objectFit: "cover" }}
                        onError={(e: any) => { e.target.style.display = "none"; }}
                      />
                    </div>
                  )}

                  {/* Matn */}
                  <div style={{ padding: "12px 14px", fontSize: "0.85rem", color: "#e4ecf2", whiteSpace: "pre-wrap", lineHeight: 1.45 }}>
                    {messageText ? (
                      <div dangerouslySetInnerHTML={{ __html: formatTelegramPreviewHtml(messageText) }} />
                    ) : (
                      <span style={{ color: "#6c7883", fontStyle: "italic" }}>Xabar matni bu yerda ko&apos;rinadi...</span>
                    )}
                  </div>

                  {/* Inline tugmalar */}
                  {buttons.length > 0 && (
                    <div style={{ padding: "6px 10px 12px", display: "flex", flexDirection: "column", gap: "4px" }}>
                      {buttons.map((btn, idx) => (
                        <div
                          key={idx}
                          style={{
                            background: "rgba(255,255,255,0.08)",
                            color: "#64b5f6",
                            textAlign: "center",
                            padding: "7px 10px",
                            borderRadius: "6px",
                            fontSize: "0.8rem",
                            fontWeight: 500,
                          }}
                        >
                          {btn.text} ↗
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* 3. Yuborilgan xabarlar tarixi jadvali */}
          <div className="content-card">
            <div className="card-header">
              <h3 className="card-title">📜 Oxirgi Xabarnomalar Tarixi</h3>
            </div>
            <div className="table-responsive">
              {loadingHistory ? (
                <div style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)" }}>Yuklanmoqda...</div>
              ) : history.length === 0 ? (
                <div style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)" }}>Hozircha hech qanday xabarnoma yuborilmagan.</div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Sana va Vaqt</th>
                      <th>Auditoriya</th>
                      <th>Xabar mazmuni</th>
                      <th>Yetib bordi / Xato</th>
                      <th>Yuboruvchi</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((item) => (
                      <tr key={item.id}>
                        <td style={{ fontSize: "0.8rem", whiteSpace: "nowrap" }}>
                          {new Date(item.sentAt).toLocaleString("uz-UZ")}
                        </td>
                        <td>
                          <span className="badge badge-success" style={{ fontSize: "0.7rem" }}>
                            {item.target === "all_groups" ? "👥 Barcha guruhlar" : item.target === "private_users" ? "👤 Shaxsiy a'zolar" : "🎯 Tanlangan"}
                          </span>
                        </td>
                        <td style={{ maxWidth: "300px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                          {item.message}
                        </td>
                        <td>
                          <b style={{ color: "#34d399" }}>{item.successful}</b> / <span style={{ color: item.failed > 0 ? "#f87171" : "var(--text-muted)" }}>{item.failed}</span>
                        </td>
                        <td style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                          {item.admin}
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

      {/* Tasdiqlash modali */}
      {showConfirmModal && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: "1rem" }}>
          <div style={{ background: "var(--bg-secondary)", border: "1px solid var(--border-color)", borderRadius: "var(--radius-md)", maxWidth: "440px", width: "100%", padding: "1.5rem", boxShadow: "0 10px 25px rgba(0,0,0,0.5)" }}>
            <h3 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: "0.75rem" }}>⚠️ Xabarni yuborishni tasdiqlaysizmi?</h3>
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem", lineHeight: 1.5, marginBottom: "1.25rem" }}>
              Ushbu xabar <b>{target === "all_groups" ? "barcha faol guruhlar" : target === "private_users" ? "barcha shaxsiy foydalanuvchilar" : "tanlangan guruhlar"}</b>ga navbatma-navbat yuboriladi. Tasdiqlangach, jarayonni to&apos;xtatib bo&apos;lmaydi.
            </p>
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.75rem" }}>
              <button type="button" onClick={() => setShowConfirmModal(false)} className="btn btn-outline">
                Bekor qilish
              </button>
              <button type="button" onClick={handleSendBroadcast} className="btn btn-primary" style={{ background: "#ef4444" }}>
                Ha, Yuborilsin
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
