"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

interface KursLessonMeta {
  dars: number;
  quizId: string;
  mavzu: string;
  papka?: string;
  testlarSoni: number;
  mashqlarSoni: number;
  updatedAt?: string;
}

export default function KursTestlariPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

  const [darslar, setDarslar] = useState<KursLessonMeta[]>([]);
  const [lastLoadedAt, setLastLoadedAt] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [reloading, setReloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const fetchLessons = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/kurs/darslar", {
        signal: AbortSignal.timeout(15000),
      });
      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        setDarslar(data.darslar || []);
        setLastLoadedAt(data.lastLoadedAt || null);
      } else {
        setError(data.message || "Kurs darslarini yuklashda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setLoading(false);
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

    fetchLessons();
  }, [router]);

  const handleReloadCache = async () => {
    setReloading(true);
    setError(null);
    setSuccessMsg(null);
    try {
      const res = await fetch("/api/kurs/qayta-yuklash", {
        method: "POST",
      });
      if (res.status === 401) {
        router.push("/login");
        return;
      }

      const data = await res.json();
      if (res.ok && data.ok) {
        await fetchLessons();
        setSuccessMsg(
          `Kurs kesh muvaffaqiyatli yangilandi (${data.lessonsCount ?? data.totalLessons ?? 0} ta dars, ${data.quizzesCount ?? data.totalQuestions ?? 0} ta faol test).`
        );
      } else {
        setError(data.message || "Kurs testlarini qayta yuklashda xatolik yuz berdi.");
      }
    } catch {
      setError("Server bilan bog'lanishda xatolik yuz berdi.");
    } finally {
      setReloading(false);
    }
  };

  const formatDate = (isoString?: string | null) => {
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

  const totalQuestions = darslar.reduce(
    (sum, item) => sum + (item.testlarSoni || 0),
    0
  );
  const totalExercises = darslar.reduce(
    (sum, item) => sum + (item.mashqlarSoni || 0),
    0
  );

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Kurs testlari («Kimyo 0 dan»)"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="card-header">
              <div>
                <h3 className="card-title">
                  📚 «Kimyo 0 dan» kursi darslari ({darslar.length} ta dars, {totalQuestions} ta test, {totalExercises} ta mashq)
                </h3>
                <p style={{ fontSize: "0.8rem", color: "var(--text-secondary)", marginTop: "4px" }}>
                  Firestore <code>kurs_darslar</code> kolleksiyasidan yuklangan darslar ro&apos;yxati (faqat o&apos;qish uchun, javoblar maxfiy saqlanadi).
                </p>
                <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "2px" }}>
                  Oxirgi kesh yangilangan vaqt: <b>{formatDate(lastLoadedAt)}</b>
                </div>
              </div>

              <button
                type="button"
                onClick={handleReloadCache}
                disabled={reloading}
                className="btn btn-primary"
              >
                {reloading ? "⏳ Yuklanmoqda..." : "🔄 Qayta yuklash"}
              </button>
            </div>

            {error && <div className="alert alert-danger" style={{ margin: "1rem" }}>{error}</div>}
            {successMsg && <div className="alert alert-success" style={{ margin: "1rem" }}>{successMsg}</div>}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Dars</th>
                    <th>Mavzu</th>
                    <th>Quiz Buyrug&apos;i</th>
                    <th>Testlar Soni</th>
                    <th>Mashqlar Soni</th>
                    <th>Yangilangan Vaqt</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2rem" }}>
                        ⏳ Yuklanmoqda...
                      </td>
                    </tr>
                  ) : darslar.length === 0 ? (
                    <tr>
                      <td colSpan={6} style={{ textAlign: "center", padding: "2.5rem", color: "var(--text-muted)" }}>
                        Firestore bazasida hozircha kurs darslari topilmadi. Lokal muhitda <code>npm run kurs:yukla</code> skriptini ishga tushiring va «Qayta yuklash» tugmasini bosing.
                      </td>
                    </tr>
                  ) : (
                    darslar.map((lesson) => (
                      <tr key={lesson.dars}>
                        <td>
                          <span className="badge badge-next">{lesson.dars}-dars</span>
                        </td>
                        <td>
                          <div style={{ fontWeight: 600 }}>{lesson.mavzu}</div>
                          {lesson.papka && (
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                              📁 {lesson.papka}
                            </div>
                          )}
                        </td>
                        <td>
                          <code>/quiz_{lesson.quizId}</code>
                        </td>
                        <td>
                          <b>{lesson.testlarSoni}</b> ta savol
                        </td>
                        <td>
                          {lesson.mashqlarSoni} ta
                        </td>
                        <td style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                          {formatDate(lesson.updatedAt)}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
