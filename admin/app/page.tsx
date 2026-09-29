"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import StatCard from "@/components/StatCard";
import HealthBadge from "@/components/HealthBadge";

interface DashboardData {
  stats: {
    groupsCount: number;
    usersCount: number;
    quizzesCount: number;
    resultsCount: number;
    cached: boolean;
  };
  health?: any;
}

export default function DashboardPage() {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminUser, setAdminUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Sessiyani va ma'lumotlarni yuklash
    const loadDashboard = async () => {
      try {
        // 1. Foydalanuvchi sessiyasini tekshirish
        const meRes = await fetch("/api/auth/me");
        if (!meRes.ok) {
          router.push("/login");
          return;
        }
        const meData = await meRes.json();
        setAdminUser(meData.user);

        // 2. Overview ma'lumotlarini yuklash
        const overviewRes = await fetch("/api/overview");
        if (overviewRes.ok) {
          const overviewData = await overviewRes.json();
          setData(overviewData);
        } else {
          setError("Statistika ma'lumotlarini yuklashda xatolik.");
        }
      } catch (err: any) {
        setError("Server bilan bog'lanishda xatolik yuz berdi.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [router]);

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        <Header
          title="Bosh sahifa"
          adminUser={adminUser}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="page-container">
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "1.5rem",
              flexWrap: "wrap",
              gap: "1rem",
            }}
          >
            <div>
              <h1 style={{ fontSize: "1.5rem", fontWeight: 700 }}>
                Xush kelibsiz{adminUser?.username ? `, @${adminUser.username}` : ""}!
              </h1>
              <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
                JDA Kimyo Quiz Telegram botining real vaqtdagi boshqaruv markazi
              </p>
              <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "4px" }}>
                📌 <i>Qayd etilgan guruhlar va foydalanuvchilar ko&apos;rsatilmoqda. Eski quiz yozuvlaridagi guruhlar ham tiklanadi.</i>
              </div>
            </div>

            <HealthBadge />
          </div>

          {error && <div className="alert alert-danger">{error}</div>}

          {loading ? (
            <div style={{ textAlign: "center", padding: "3rem", color: "var(--text-secondary)" }}>
              ⏳ Ma&apos;lumotlar yuklanmoqda...
            </div>
          ) : (
            <>
              {/* Asosiy KPI ko'rsatkichlari */}
              <div className="grid-cards">
                <StatCard
                  title="Faol Guruhlar"
                  value={data?.stats.groupsCount ?? 0}
                  icon="👥"
                  description="Bot hozir faol bo'lgan guruhlar (kuzatuv davomida)"
                />
                <StatCard
                  title="Ma'lum Foydalanuvchilar"
                  value={data?.stats.usersCount ?? 0}
                  icon="👤"
                  description="Shaxsiy chat ochgan va quiz yechgan a'zolar"
                />
                <StatCard
                  title="Mavjud Testlar"
                  value={data?.stats.quizzesCount ?? 0}
                  icon="🧪"
                  description="Koddagi faol quiz to'plamlari"
                />
                <StatCard
                  title="O'tkazilgan Quizlar"
                  value={data?.stats.resultsCount ?? 0}
                  icon="🏆"
                  description="Guruhlarda yakunlangan sessiyalar"
                />
              </div>

              {/* Tezkor havolalar va holat */}
              <div className="content-card">
                <div className="card-header">
                  <h3 className="card-title">1-bosqich: Mavjud Boshqaruv Bo&apos;limlari</h3>
                </div>
                <div style={{ padding: "1.25rem", display: "flex", gap: "1rem", flexWrap: "wrap" }}>
                  <Link href="/groups" className="btn btn-primary">
                    👥 Guruhlar ro&apos;yxati
                  </Link>
                  <Link href="/users" className="btn btn-outline">
                    👤 Foydalanuvchilar ro&apos;yxati
                  </Link>
                </div>
              </div>

              {/* Keyingi bosqichlar rejasi */}
              <div className="content-card">
                <div className="card-header">
                  <h3 className="card-title">Keyingi bosqichlarda qo&apos;shiladigan modullar</h3>
                  <span className="badge badge-next">Rejada</span>
                </div>
                <div style={{ padding: "1.25rem", fontSize: "0.875rem", color: "var(--text-secondary)" }}>
                  <ul style={{ paddingLeft: "1.25rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                    <li>
                      <b>2-bosqich:</b> Test muharriri — yangi savollar yaratish, tahrirlash va botga dinamik yuklash
                    </li>
                    <li>
                      <b>3-bosqich:</b> Natijalar va reyting tahlili — guruhlar bo&apos;yicha ishtirokchilar reytingi, xatoliklar statistikasi
                    </li>
                    <li>
                      <b>4-bosqich:</b> Xabarnoma yuborish (Broadcast) va botning dinamik sozlamalarini boshqarish
                    </li>
                  </ul>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
