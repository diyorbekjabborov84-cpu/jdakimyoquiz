"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface GroupItem {
  chatId: number | string;
  title: string;
  type: string;
  status: "active" | "left" | "kicked" | "unknown";
  memberCount: number | null;
  lastActivity: string;
  updatedAt: string;
}

export default function GroupsPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);
  const [groups, setGroups] = useState<GroupItem[]>([]);
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

  const fetchGroups = async (query: string, cursor?: string | null) => {
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
      const url = queryString ? `/api/groups?${queryString}` : "/api/groups";

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
          setGroups((prev) => [...prev, ...(data.groups || [])]);
        } else {
          setGroups(data.groups || []);
        }
        setTotalCount(typeof data.total === "number" ? data.total : null);
        setNextCursor(data.nextCursor || null);
        setHasMore(Boolean(data.hasMore));
        setError(null);
      } else {
        setError(data.message || "Guruhlar ro'yxatini yuklashda xatolik yuz berdi.");
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
      fetchGroups("", null);
      return;
    }

    const timer = setTimeout(() => {
      setGroups([]);
      setNextCursor(null);
      setHasMore(false);
      fetchGroups(searchTerm, null);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    abortControllerRef.current?.abort();
    searchSeqRef.current++;
    setGroups([]);
    setNextCursor(null);
    setHasMore(false);
    setTotalCount(null);
    setLoadingMore(false);
    setLoading(true);
    setSearchTerm(e.target.value);
  };

  const handleLoadMore = () => {
    if (nextCursor && !loadingMore) {
      fetchGroups(searchTerm, nextCursor);
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
          title="Guruhlar ro'yxati"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="card-header">
              <div>
                <h3 className="card-title">
                  {searchTerm ? "Qidiruv natijalari" : "Mavjud Guruhlar"}
                  {totalCount !== null ? ` (Jami: ${totalCount})` : ` (${groups.length}${hasMore ? "+" : ""})`}
                </h3>
                <p style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                  Bot qo&apos;shilgan, faoliyat yuritayotgan yoki tark etgan Telegram guruhlari
                </p>
                <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "2px" }}>
                  📌 <i>Bot qayd etgan va eski quiz yozuvlaridan tiklangan guruhlar. Bazada izi yo&apos;q eski guruhlar botga hodisa kelganda qo&apos;shiladi.</i>
                </div>
              </div>

              <div className="search-box">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Aniq ID yoki nomining boshi bo'yicha qidiruv..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="search-input"
                  style={{ minWidth: "290px" }}
                />
              </div>
            </div>

            {error && <div className="alert alert-danger" style={{ margin: "1rem" }}>{error}</div>}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Guruh Nomi</th>
                    <th>Chat ID</th>
                    <th>Turi</th>
                    <th>Bot Holati</th>
                    <th>A&apos;zolar Soni</th>
                    <th>Oxirgi Faollik</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2rem" }}>
                        ⏳ Yuklanmoqda...
                      </td>
                    </tr>
                  ) : groups.length === 0 ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2rem", color: "var(--text-muted)" }}>
                        {searchTerm ? "Qidiruv bo'yicha hech qanday guruh topilmadi." : "Hozircha guruhlar mavjud emas."}
                      </td>
                    </tr>
                  ) : (
                    groups.map((group) => (
                      <tr key={String(group.chatId)}>
                        <td style={{ fontWeight: 600 }}>{group.title}</td>
                        <td>
                          <code>{group.chatId}</code>
                        </td>
                        <td>
                          <span style={{ textTransform: "capitalize", color: "var(--text-secondary)" }}>
                            {group.type === "unknown" ? "Noma’lum" : group.type}
                          </span>
                        </td>
                        <td>
                          {group.status === "active" ? (
                            <span className="badge badge-success">Faol</span>
                          ) : group.status === "kicked" ? (
                            <span className="badge badge-danger">Haydalgan</span>
                          ) : group.status === "unknown" ? (
                            <span className="badge badge-warning">A’zoligi aniqlanmagan</span>
                          ) : (
                            <span className="badge badge-warning">Chiqib ketgan</span>
                          )}
                        </td>
                        <td>
                          {group.memberCount !== null && group.memberCount !== undefined ? (
                            group.memberCount
                          ) : (
                            <span style={{ color: "var(--text-muted)", fontStyle: "italic" }}>
                              noma&apos;lum
                            </span>
                          )}
                        </td>
                        <td style={{ color: "var(--text-secondary)", fontSize: "0.8rem" }}>
                          {formatDate(group.lastActivity)}
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
