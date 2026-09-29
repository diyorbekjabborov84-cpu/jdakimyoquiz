"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export default function SettingsPage() {
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
          title="Sozlamalar"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="placeholder-box">
              <div className="placeholder-icon">⚙️</div>
              <h2 className="placeholder-title">Bot va panel sozlamalari</h2>
              <span className="badge badge-next" style={{ fontSize: "0.85rem", padding: "0.35rem 0.85rem" }}>
                Keyingi bosqichda (4-bosqich)
              </span>
              <p className="placeholder-desc">
                Kanal obunasi majburiyligi, kanallar ro&apos;yxati, test taymerlari standart vaqti,
                admin hisoblari va audit loglarini boshqarish sozlamalari.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
