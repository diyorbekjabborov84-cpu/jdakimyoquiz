"use client";

import { useRouter } from "next/navigation";

interface HeaderProps {
  title: string;
  adminUser?: { id: string | number; username?: string } | null;
  onMenuToggle: () => void;
}

export default function Header({ title, adminUser, onMenuToggle }: HeaderProps) {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
    } catch {
      // ignore
    }
    router.push("/login");
  };

  return (
    <header className="top-header">
      <div className="header-left">
        <button className="menu-toggle" onClick={onMenuToggle} aria-label="Menyu">
          ☰
        </button>
        <h2 style={{ fontSize: "1.15rem", fontWeight: 600 }}>{title}</h2>
      </div>

      <div className="header-right">
        {adminUser && (
          <div className="admin-badge">
            <div className="admin-avatar">
              {adminUser.username ? adminUser.username[0].toUpperCase() : "A"}
            </div>
            <span>
              {adminUser.username ? `@${adminUser.username}` : `ID: ${adminUser.id}`}
            </span>
          </div>
        )}

        <button className="btn btn-outline" onClick={handleLogout} title="Chiqish">
          🚪 Chiqish
        </button>
      </div>
    </header>
  );
}
