"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

type GroupMode = "asosiy" | "kurs" | "ochiq_emas";

interface GroupItem {
  chatId: number | string;
  title: string;
  type: string;
  status: "active" | "left" | "kicked" | "unknown";
  mode?: GroupMode;
  memberCount: number | null;
  lastActivity: string;
  updatedAt: string;
}

interface ModeCounts {
  asosiy: number;
  kurs: number;
  ochiq_emas: number;
}

const MODE_LABELS: Record<GroupMode, string> = {
  asosiy: "🟢 Asosiy (6 bo'limli menyu)",
  kurs: "🔵 Kurs («Kimyo 0 dan»)",
  ochiq_emas: "⚪ O'chirilgan (javob bermaydi)",
};

export default function GroupsPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);
  const [groups, setGroups] = useState<GroupItem[]>([]);
  const [totalCount, setTotalCount] = useState<number | null>(null);
  const [modeCounts, setModeCounts] = useState<ModeCounts | null>(null);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [modeFilter, setModeFilter] = useState<"" | GroupMode>("");
  const [updatingChatId, setUpdatingChatId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);
  const searchSeqRef = useRef<number>(0);
  const isInitialMount = useRef<boolean>(true);

  const fetchGroups = async (
    query: string,
    selectedMode: "" | GroupMode,
    cursor?: string | null
  ) => {
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
      if (selectedMode) params.set("mode", selectedMode);
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
        if (data.modeCounts) {
          setModeCounts(data.modeCounts);
        }
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

  // Debounced search va rejim filtri (300 ms)
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      fetchGroups("", "", null);
      return;
    }

    const timer = setTimeout(() => {
      setGroups([]);
      setNextCursor(null);
      setHasMore(false);
      fetchGroups(searchTerm, modeFilter, null);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, modeFilter]);

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

  const handleModeFilterChange = (newMode: "" | GroupMode) => {
    if (newMode === modeFilter) return;
    abortControllerRef.current?.abort();
    searchSeqRef.current++;
    setGroups([]);
    setNextCursor(null);
    setHasMore(false);
    setTotalCount(null);
    setLoadingMore(false);
    setLoading(true);
    setModeFilter(newMode);
  };

  const handleGroupModeChange = async (group: GroupItem, nextMode: GroupMode) => {
    const currentMode: GroupMode = group.mode || "asosiy";
    if (nextMode === currentMode) return;

    const confirmed = window.confirm(
      `«${group.title}» (${group.chatId}) guruhining rejimini "${MODE_LABELS[nextMode]}" ga o'zgartirishni tasdiqlaysizmi?`
    );
    if (!confirmed) return;

    const chatIdKey = String(group.chatId);
    setUpdatingChatId(chatIdKey);
    setError(null);
    setSuccessMsg(null);

    try {
      const res = await fetch(
        `/api/groups/${encodeURIComponent(chatIdKey)}/mode`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ mode: nextMode }),
        }
      );

      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        setGroups((prev) =>
          prev
            .map((item) =>
              String(item.chatId) === chatIdKey ? { ...item, mode: nextMode } : item
            )
            .filter((item) => !modeFilter || (item.mode || "asosiy") === modeFilter)
        );
        setModeCounts((prev) => {
          if (!prev) return prev;
          return {
            ...prev,
            [currentMode]: Math.max(0, (prev[currentMode] || 0) - 1),
            [nextMode]: (prev[nextMode] || 0) + 1,
          };
        });
        setSuccessMsg(
          `«${group.title}» guruhi rejimi "${MODE_LABELS[nextMode]}" ga o'zgartirildi.`
        );
      } else {
        setError(data.message || "Guruh rejimini o'zgartirishda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setUpdatingChatId(null);
    }
  };

  const handleLoadMore = () => {
    if (nextCursor && !loadingMore) {
      fetchGroups(searchTerm, modeFilter, nextCursor);
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

  const allModesTotal = modeCounts
    ? modeCounts.asosiy + modeCounts.kurs + modeCounts.ochiq_emas
    : null;

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
                  Bot qo&apos;shilgan, faoliyat yuritayotgan yoki tark etgan Telegram guruhlari va ularning qobiq rejimi
                </p>
                <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "2px" }}>
                  📌 <i>Har bir guruh uchun «Asosiy», «Kurs» yoki «O&apos;chirilgan» rejimini tanlashingiz mumkin.</i>
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

            {/* Rejim filtri tablari */}
            <div
              style={{
                padding: "0.75rem 1.25rem",
                borderBottom: "1px solid var(--border-color)",
                display: "flex",
                gap: "0.5rem",
                flexWrap: "wrap",
                alignItems: "center",
              }}
            >
              <span style={{ fontSize: "0.8rem", color: "var(--text-secondary)", marginRight: "0.25rem" }}>
                Rejim bo&apos;yicha filtr:
              </span>
              <button
                type="button"
                onClick={() => handleModeFilterChange("")}
                className={`btn ${modeFilter === "" ? "btn-primary" : "btn-outline"}`}
                style={{ fontSize: "0.78rem", padding: "0.35rem 0.75rem" }}
              >
                Barchasi{allModesTotal !== null ? ` (${allModesTotal})` : ""}
              </button>
              <button
                type="button"
                onClick={() => handleModeFilterChange("asosiy")}
                className={`btn ${modeFilter === "asosiy" ? "btn-primary" : "btn-outline"}`}
                style={{ fontSize: "0.78rem", padding: "0.35rem 0.75rem" }}
              >
                🟢 Asosiy{modeCounts ? ` (${modeCounts.asosiy})` : ""}
              </button>
              <button
                type="button"
                onClick={() => handleModeFilterChange("kurs")}
                className={`btn ${modeFilter === "kurs" ? "btn-primary" : "btn-outline"}`}
                style={{ fontSize: "0.78rem", padding: "0.35rem 0.75rem" }}
              >
                🔵 Kurs{modeCounts ? ` (${modeCounts.kurs})` : ""}
              </button>
              <button
                type="button"
                onClick={() => handleModeFilterChange("ochiq_emas")}
                className={`btn ${modeFilter === "ochiq_emas" ? "btn-primary" : "btn-outline"}`}
                style={{ fontSize: "0.78rem", padding: "0.35rem 0.75rem" }}
              >
                ⚪ O&apos;chirilgan{modeCounts ? ` (${modeCounts.ochiq_emas})` : ""}
              </button>
            </div>

            {error && <div className="alert alert-danger" style={{ margin: "1rem" }}>{error}</div>}
            {successMsg && <div className="alert alert-success" style={{ margin: "1rem" }}>{successMsg}</div>}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Guruh Nomi</th>
                    <th>Chat ID</th>
                    <th>Qobiq Rejimi (Mode)</th>
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
                        {searchTerm || modeFilter
                          ? "Tanlangan filtr bo'yicha hech qanday guruh topilmadi."
                          : "Hozircha guruhlar mavjud emas."}
                      </td>
                    </tr>
                  ) : (
                    groups.map((group) => {
                      const currentMode: GroupMode = group.mode || "asosiy";
                      const isUpdating = updatingChatId === String(group.chatId);
                      return (
                        <tr key={String(group.chatId)}>
                          <td>
                            <div style={{ fontWeight: 600 }}>{group.title}</div>
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "capitalize" }}>
                              {group.type === "unknown" ? "Noma’lum" : group.type}
                            </div>
                          </td>
                          <td>
                            <code>{group.chatId}</code>
                          </td>
                          <td>
                            <select
                              value={currentMode}
                              disabled={isUpdating}
                              onChange={(e) =>
                                handleGroupModeChange(group, e.target.value as GroupMode)
                              }
                              className="form-input"
                              style={{
                                padding: "0.35rem 0.6rem",
                                fontSize: "0.8rem",
                                width: "auto",
                                minWidth: "215px",
                              }}
                            >
                              <option value="asosiy">🟢 Asosiy (6 bo&apos;limli menyu)</option>
                              <option value="kurs">🔵 Kurs («Kimyo 0 dan»)</option>
                              <option value="ochiq_emas">⚪ O&apos;chirilgan (javob bermaydi)</option>
                            </select>
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
                      );
                    })
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
