"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export default function ResultsPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);

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

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Natijalar & Reyting"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="placeholder-box">
              <div className="placeholder-icon">🏆</div>
              <h2 className="placeholder-title">Natijalar va reyting tahlili</h2>
              <span className="badge badge-next" style={{ fontSize: "0.85rem", padding: "0.35rem 0.85rem" }}>
                Keyingi bosqichda (3-bosqich)
              </span>
              <p className="placeholder-desc">
                Ushbu bo&apos;limda guruhlar kesimida o&apos;tkazilgan quizlar ro&apos;yxati, ishtirokchilar ballari,
                eng qiyin savollar tahlili va umumiy reyting jadvallari ko&apos;rsatiladi.
              </p>
              <div className="alert alert-info" style={{ maxWidth: "480px", textAlign: "left" }}>
                ℹ️ Hozirda har bir o&apos;tkazilgan quiz natijasi Cloud Firestore&apos;ning <code>quiz_results</code> kolleksiyasiga
                muvaffaqiyatli yozib borilmoqda.
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
