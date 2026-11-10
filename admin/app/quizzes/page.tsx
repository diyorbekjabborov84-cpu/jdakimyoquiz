"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import SessionWarmupBanner from "@/components/SessionWarmupBanner";
import { useAdminSession } from "@/lib/useAdminSession";

export default function QuizzesPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const {
    adminUser,
    sessionState,
    retryAttempt,
    maxRetries,
    retrySession,
  } = useAdminSession();

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
          <SessionWarmupBanner
            sessionState={sessionState}
            retryAttempt={retryAttempt}
            maxRetries={maxRetries}
            onRetry={retrySession}
          />
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
