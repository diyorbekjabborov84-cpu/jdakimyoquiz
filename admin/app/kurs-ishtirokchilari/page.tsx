"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface KursParticipant {
  userId: number | string;
  ism: string;
  username?: string;
  qoshgan?: string;
  manba?: "guruh" | "admin";
  bloklangan: boolean;
  qoshilgan?: string;
  qoshilganVaqt?: string;
}

export default function KursIshtirokchilariPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

  const [participants, setParticipants] = useState<KursParticipant[]>([]);
  const [totalCount, setTotalCount] = useState<number | null>(null);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  // Qo'shish formasi
  const [newUserId, setNewUserId] = useState("");
  const [newIsm, setNewIsm] = useState("");
  const [adding, setAdding] = useState(false);
  const [actionUserId, setActionUserId] = useState<string | null>(null);

  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);
  const searchSeqRef = useRef<number>(0);
  const isInitialMount = useRef<boolean>(true);

  const fetchParticipants = async (query: string, cursor?: string | null) => {
    if (cursor) {
      setLoadingMore(true);
    } else {
      setLoading(true);
      setError(null);
    }

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    const currentSeq = ++searchSeqRef.current;

    try {
      const params = new URLSearchParams();
      if (query.trim()) params.set("q", query.trim());
      if (cursor) params.set("cursor", cursor);
      const queryString = params.toString();
      const url = queryString
        ? `/api/kurs/ishtirokchilar?${queryString}`
        : "/api/kurs/ishtirokchilar";

      const res = await fetch(url, { signal: controller.signal });
      if (currentSeq !== searchSeqRef.current) return;

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (currentSeq !== searchSeqRef.current) return;

      if (res.ok && data.ok) {
        const list = data.items || data.ishtirokchilar || [];
        if (cursor) {
          setParticipants((prev) => [...prev, ...list]);
        } else {
          setParticipants(list);
        }
        setTotalCount(typeof data.total === "number" ? data.total : null);
        setNextCursor(data.nextCursor || null);
        setHasMore(Boolean(data.hasMore));
        setError(null);
      } else {
        setError(data.message || "Ishtirokchilar ro'yxatini yuklashda xatolik yuz berdi.");
      }
    } catch (err: any) {
      if (err.name === "AbortError") return;
      if (currentSeq === searchSeqRef.current) {
        setError("Server bilan bog'lanishda xatolik yuz berdi.");
      }
    } finally {
      if (currentSeq === searchSeqRef.current) {
        setLoading(false);
        setLoadingMore(false);
      }
    }
  };

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
  }, [router]);

  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      fetchParticipants("", null);
      return;
    }

    const timer = setTimeout(() => {
      setParticipants([]);
      setNextCursor(null);
      setHasMore(false);
      fetchParticipants(searchTerm, null);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    abortControllerRef.current?.abort();
    searchSeqRef.current++;
    setParticipants([]);
    setNextCursor(null);
    setHasMore(false);
    setTotalCount(null);
    setLoadingMore(false);
    setLoading(true);
    setSearchTerm(e.target.value);
  };

  const handleAddParticipant = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedId = newUserId.trim();
    if (!/^\d+$/.test(trimmedId)) {
      setError("Telegram User ID faqat musbat raqamlardan iborat bo'lishi kerak.");
      return;
    }

    setAdding(true);
    setError(null);
    setSuccessMsg(null);

    try {
      const res = await fetch("/api/kurs/ishtirokchilar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: trimmedId,
          ism: newIsm.trim() || undefined,
        }),
      });

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        setNewUserId("");
        setNewIsm("");
        setSuccessMsg(`Ishtirokchi (${trimmedId}) muvaffaqiyatli qo'shildi.`);
        fetchParticipants(searchTerm, null);
      } else {
        setError(data.message || "Ishtirokchini qo'shishda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setAdding(false);
    }
  };

  const handleToggleBlock = async (item: KursParticipant) => {
    const nextBlocked = !item.bloklangan;
    const actionLabel = nextBlocked ? "bloklashni" : "blokdan chiqarishni";
    const confirmed = window.confirm(
      `${item.ism || item.userId} (${item.userId}) foydalanuvchisini ${actionLabel} tasdiqlaysizmi?`
    );
    if (!confirmed) return;

    const userIdStr = String(item.userId);
    setActionUserId(userIdStr);
    setError(null);
    setSuccessMsg(null);

    try {
      const res = await fetch(
        `/api/kurs/ishtirokchilar/${encodeURIComponent(userIdStr)}`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ bloklangan: nextBlocked }),
        }
      );

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        setParticipants((prev) =>
          prev.map((p) =>
            String(p.userId) === userIdStr ? { ...p, bloklangan: nextBlocked } : p
          )
        );
        setSuccessMsg(
          `Foydalanuvchi (${userIdStr}) ${nextBlocked ? "bloklandi" : "blokdan chiqarildi"}.`
        );
      } else {
        setError(data.message || "Holatni o'zgartirishda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setActionUserId(null);
    }
  };

  const handleDeleteParticipant = async (item: KursParticipant) => {
    const userIdStr = String(item.userId);
    const confirmed = window.confirm(
      `${item.ism || userIdStr} (${userIdStr}) foydalanuvchisini kurs ishtirokchilari ro'yxatidan o'chirishni tasdiqlaysizmi?`
    );
    if (!confirmed) return;

    setActionUserId(userIdStr);
    setError(null);
    setSuccessMsg(null);

    try {
      const res = await fetch(
        `/api/kurs/ishtirokchilar/${encodeURIComponent(userIdStr)}`,
        {
          method: "DELETE",
        }
      );

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        setParticipants((prev) => prev.filter((p) => String(p.userId) !== userIdStr));
        setTotalCount((prev) => (typeof prev === "number" ? Math.max(0, prev - 1) : prev));
        setSuccessMsg(`Ishtirokchi (${userIdStr}) ro'yxatdan o'chirildi.`);
      } else {
        setError(data.message || "Ishtirokchini o'chirishda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setActionUserId(null);
    }
  };

  const formatDate = (isoString?: string) => {
    if (!isoString) return "—";
    try {
      const d = new Date(isoString);
      return d.toLocaleString("uz-UZ", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Kurs ishtirokchilari"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          {/* Izoh va qo'shish formasi */}
          <div className="content-card" style={{ marginBottom: "1.5rem" }}>
            <div className="card-header">
              <div>
                <h3 className="card-title">🎓 Qo&apos;shimcha ishtirokchi qo&apos;shish</h3>
                <p style={{ fontSize: "0.82rem", color: "var(--text-secondary)", marginTop: "4px" }}>
                  ℹ️ <b>Izoh:</b> Kurs guruhining a&apos;zolari avtomatik ruxsat oladi, bu ro&apos;yxat qo&apos;shimcha va istisnolar uchun.
                </p>
              </div>
            </div>

            <form
              onSubmit={handleAddParticipant}
              style={{
                padding: "1.25rem",
                display: "flex",
                gap: "0.75rem",
                flexWrap: "wrap",
                alignItems: "flex-end",
              }}
            >
              <div style={{ flex: "1 1 220px" }}>
                <label className="form-label" htmlFor="newUserId">
                  Telegram User ID *
                </label>
                <input
                  id="newUserId"
                  type="text"
                  className="form-input"
                  placeholder="Masalan: 123456789"
                  value={newUserId}
                  onChange={(e) => setNewUserId(e.target.value)}
                  required
                />
              </div>

              <div style={{ flex: "1 1 260px" }}>
                <label className="form-label" htmlFor="newIsm">
                  Ism / Izoh (ixtiyoriy)
                </label>
                <input
                  id="newIsm"
                  type="text"
                  className="form-input"
                  placeholder="Masalan: Alisher Karimov"
                  value={newIsm}
                  onChange={(e) => setNewIsm(e.target.value)}
                />
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={adding}
                style={{ height: "42px" }}
              >
                {adding ? "⏳ Qo'shilmoqda..." : "➕ Ro'yxatga qo'shish"}
              </button>
            </form>
          </div>

          {error && <div className="alert alert-danger" style={{ marginBottom: "1rem" }}>{error}</div>}
          {successMsg && <div className="alert alert-success" style={{ marginBottom: "1rem" }}>{successMsg}</div>}

          {/* Ro'yxat */}
          <div className="content-card">
            <div className="card-header">
              <div>
                <h3 className="card-title">
                  Qo&apos;shimcha va istisno ishtirokchilar
                  {totalCount !== null ? ` (Jami: ${totalCount})` : ` (${participants.length}${hasMore ? "+" : ""})`}
                </h3>
                <p style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                  Admin tomonidan qo&apos;shilgan yoki shaxsiy chatdan bloklangan foydalanuvchilar
                </p>
              </div>

              <div className="search-box">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Telegram ID bo'yicha qidiruv..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="search-input"
                  style={{ minWidth: "250px" }}
                />
              </div>
            </div>

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Ism</th>
                    <th>Telegram ID</th>
                    <th>Manba</th>
                    <th>Holati</th>
                    <th>Qo&apos;shilgan vaqt</th>
                    <th>Amallar</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2rem" }}>
                        ⏳ Yuklanmoqda...
                      </td>
                    </tr>
                  ) : participants.length === 0 ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2.5rem", color: "var(--text-muted)" }}>
                        {searchTerm
                          ? "Qidiruv bo'yicha hech qanday ishtirokchi topilmadi."
                          : "Qo'shimcha ishtirokchilar ro'yxati hozircha bo'sh. Kurs guruhi a'zolari shaxsiy chatdan avtomatik foydalana oladi."}
                      </td>
                    </tr>
                  ) : (
                    participants.map((item) => {
                      const isBusy = actionUserId === String(item.userId);
                      const sourceLabel = item.qoshgan || item.manba || "admin";
                      const addedAt = item.qoshilgan || item.qoshilganVaqt;
                      return (
                        <tr key={String(item.userId)}>
                          <td>
                            <div style={{ fontWeight: 600 }}>{item.ism || "Ismsiz"}</div>
                            {item.username && (
                              <div style={{ fontSize: "0.75rem", color: "var(--primary)" }}>
                                @{item.username.replace(/^@/, "")}
                              </div>
                            )}
                          </td>
                          <td>
                            <code>{item.userId}</code>
                          </td>
                          <td>
                            <span className="badge badge-next">
                              {sourceLabel === "admin" ? "Admin" : sourceLabel}
                            </span>
                          </td>
                          <td>
                            {item.bloklangan ? (
                              <span className="badge badge-danger">🚫 Bloklangan</span>
                            ) : (
                              <span className="badge badge-success">✅ Ruxsat berilgan</span>
                            )}
                          </td>
                          <td style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                            {formatDate(addedAt)}
                          </td>
                          <td>
                            <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                              <button
                                type="button"
                                onClick={() => handleToggleBlock(item)}
                                disabled={isBusy}
                                className="btn btn-outline"
                                style={{ fontSize: "0.75rem", padding: "0.3rem 0.65rem" }}
                              >
                                {item.bloklangan ? "🔓 Blokdan chiqarish" : "🚫 Bloklash"}
                              </button>
                              <button
                                type="button"
                                onClick={() => handleDeleteParticipant(item)}
                                disabled={isBusy}
                                className="btn btn-outline"
                                style={{
                                  fontSize: "0.75rem",
                                  padding: "0.3rem 0.65rem",
                                  borderColor: "var(--danger)",
                                  color: "var(--danger)",
                                }}
                              >
                                🗑️ O&apos;chirish
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>

            {hasMore && !loading && (
              <div style={{ padding: "1rem", textAlign: "center", borderTop: "1px solid var(--border-color)" }}>
                <button
                  onClick={() => nextCursor && fetchParticipants(searchTerm, nextCursor)}
                  className="btn btn-outline"
                  disabled={loadingMore}
                >
                  {loadingMore ? "⏳ Yuklanmoqda..." : "Keyingi sahifani yuklash ⬇️"}
                </button>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
