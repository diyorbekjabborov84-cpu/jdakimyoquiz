"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export default function BroadcastPage() {
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
          title="Xabarnoma yuborish"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div className="content-card">
            <div className="placeholder-box">
              <div className="placeholder-icon">📢</div>
              <h2 className="placeholder-title">Xabarnoma yuborish (Broadcast)</h2>
              <span className="badge badge-next" style={{ fontSize: "0.85rem", padding: "0.35rem 0.85rem" }}>
                Keyingi bosqichda (4-bosqich)
              </span>
              <p className="placeholder-desc">
                Bot qo&apos;shilgan barcha guruhlarga yoki shaxsiy chat ochgan faol foydalanuvchilarga xabarlar,
                yangiliklar va yangi test e&apos;lonlarini xavfsiz va navbatli (rate-limited) tarzda tarqatish moduli.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
