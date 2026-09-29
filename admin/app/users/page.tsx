"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface BotUserItem {
  userId: number | string;
  firstName: string;
  lastName: string | null;
  username: string | null;
  privateChatActive: boolean;
  lastActivity: string;
  updatedAt: string;
}

export default function UsersPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);
  const [users, setUsers] = useState<BotUserItem[]>([]);
  const [totalCount, setTotalCount] = useState<number | null>(null);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);
  const searchSeqRef = useRef<number>(0);
  const isInitialMount = useRef<boolean>(true);

  const fetchUsers = async (query: string, cursor?: string | null) => {
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
      const url = queryString ? `/api/users?${queryString}` : "/api/users";

      const res = await fetch(url, { signal: controller.signal });
      if (currentSeq !== searchSeqRef.current) return;

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (currentSeq !== searchSeqRef.current) return;

      if (res.ok && data.ok) {
        if (cursor) {
          setUsers((prev) => [...prev, ...(data.users || [])]);
        } else {
          setUsers(data.users || []);
        }
        setTotalCount(typeof data.total === "number" ? data.total : null);
        setNextCursor(data.nextCursor || null);
        setHasMore(Boolean(data.hasMore));
        setError(null);
      } else {
        setError(data.message || "Foydalanuvchilar ro'yxatini yuklashda xatolik yuz berdi.");
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

  // Debounced search (300 ms)
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      fetchUsers("", null);
      return;
    }

    const timer = setTimeout(() => {
      setUsers([]);
      setNextCursor(null);
      setHasMore(false);
      fetchUsers(searchTerm, null);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    abortControllerRef.current?.abort();
    searchSeqRef.current++;
    setUsers([]);
    setNextCursor(null);
    setHasMore(false);
    setTotalCount(null);
    setLoadingMore(false);
    setLoading(true);
    setSearchTerm(e.target.value);
  };

  const handleLoadMore = () => {
    if (nextCursor && !loadingMore) {
      fetchUsers(searchTerm, nextCursor);
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
          title="Foydalanuvchilar ro'yxati"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="card-header">
              <div>
                <h3 className="card-title">
                  {searchTerm ? "Qidiruv natijalari" : "Ma'lum Foydalanuvchilar"}
                  {totalCount !== null ? ` (Jami: ${totalCount})` : ` (${users.length}${hasMore ? "+" : ""})`}
                </h3>
                <p style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                  Bot bilan shaxsiy chat boshlagan yoki quizlarda faol ishtirok etgan a&apos;zolar
                </p>
                <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "2px" }}>
                  📌 <i>Bot kuzatuvi yoqilgandan keyin qayd etilgan ma&apos;lumotlar</i>
                </div>
              </div>

              <div className="search-box">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Aniq ID yoki username/ism boshi bo'yicha qidiruv..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="search-input"
                  style={{ minWidth: "310px" }}
                />
              </div>
            </div>

            {error && <div className="alert alert-danger" style={{ margin: "1rem" }}>{error}</div>}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Foydalanuvchi</th>
                    <th>Telegram ID</th>
                    <th>Username</th>
                    <th>Shaxsiy Chat</th>
                    <th>Oxirgi Faollik</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={5} style={{ textAlign: "center", padding: "2rem" }}>
                        ⏳ Yuklanmoqda...
                      </td>
                    </tr>
                  ) : users.length === 0 ? (
                    <tr>
                      <td colSpan={5} style={{ textAlign: "center", padding: "2rem", color: "var(--text-muted)" }}>
                        {searchTerm ? "Qidiruv bo'yicha hech kim topilmadi." : "Hozircha foydalanuvchilar mavjud emas."}
                      </td>
                    </tr>
                  ) : (
                    users.map((u) => (
                      <tr key={String(u.userId)}>
                        <td style={{ fontWeight: 600 }}>
                          {u.firstName} {u.lastName || ""}
                        </td>
                        <td>
                          <code>{u.userId}</code>
                        </td>
                        <td>
                          {u.username ? (
                            <a
                              href={`https://t.me/${u.username}`}
                              target="_blank"
                              rel="noreferrer"
                              style={{ color: "#60a5fa" }}
                            >
                              @{u.username}
                            </a>
                          ) : (
                            <span style={{ color: "var(--text-muted)" }}>—</span>
                          )}
                        </td>
                        <td>
                          {u.privateChatActive ? (
                            <span className="badge badge-success">Faol (Start)</span>
                          ) : (
                            <span className="badge badge-warning">Quiz qatnashchisi</span>
                          )}
                        </td>
                        <td style={{ color: "var(--text-secondary)", fontSize: "0.8rem" }}>
                          {formatDate(u.lastActivity)}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {hasMore && !loading && (
              <div style={{ padding: "1rem", textAlign: "center", borderTop: "1px solid var(--border-color)" }}>
                <button
                  onClick={handleLoadMore}
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
