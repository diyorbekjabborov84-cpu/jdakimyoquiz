"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export default function QuizzesPage() {
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
          title="Quizlar va testlar"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="placeholder-box">
              <div className="placeholder-icon">🧪</div>
              <h2 className="placeholder-title">Quizlar va testlar muharriri</h2>
              <span className="badge badge-next" style={{ fontSize: "0.85rem", padding: "0.35rem 0.85rem" }}>
                Keyingi bosqichda (2-bosqich)
              </span>
              <p className="placeholder-desc">
                Ushbu bo&apos;lim 2-bosqichda amalga oshiriladi. Unda admin paneldan turib yangi quizlar yaratish,
                mavjud savollarni tahrirlash, variantlarni o&apos;zgartirish va botga dinamik tarzda kiritish imkoniyati bo&apos;ladi.
              </p>
              <div className="alert alert-info" style={{ maxWidth: "480px", textAlign: "left" }}>
                ℹ️ Hozirgi bosqichda barcha quizlar kod ichidagi <code>src/quiz/questions.ts</code> faylida
                ishonchli va xavfsiz holda saqlanmoqda.
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
