"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navItems = [
  { href: "/", label: "Bosh sahifa", icon: "📊", available: true },
  { href: "/groups", label: "Guruhlar", icon: "👥", available: true },
  { href: "/users", label: "Foydalanuvchilar", icon: "👤", available: true },
  { href: "/quizzes", label: "Quizlar va testlar", icon: "🧪", available: false },
  { href: "/results", label: "Natijalar & Reyting", icon: "🏆", available: false },
  { href: "/broadcast", label: "Xabarnoma yuborish", icon: "📢", available: false },
  { href: "/settings", label: "Sozlamalar", icon: "⚙️", available: false },
];

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {isOpen && <div className="sidebar-backdrop" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="logo-badge">⚗️</div>
          <div className="logo-text">
            <h1>JDA Kimyo Quiz</h1>
            <span>Admin Panel v1.0</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`nav-link ${isActive ? "active" : ""}`}
                onClick={onClose}
              >
                <div className="nav-item-left">
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </div>
                {!item.available && (
                  <span className="badge badge-next">Keyingi bosqichda</span>
                )}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div>Loyiha: JDA Kimyo Quiz</div>
          <div style={{ marginTop: "4px" }}>Vercel &bull; Render &bull; Firestore</div>
        </div>
      </aside>
    </>
  );
}
