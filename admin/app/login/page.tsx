"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const widgetContainerRef = useRef<HTMLDivElement>(null);

  const botUsername =
    process.env.NEXT_PUBLIC_BOT_USERNAME || "jdakimyoquizbot";

  const handleTelegramAuth = async (user: any) => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
      });

      const data = await res.json();

      if (!res.ok || !data.ok) {
        let msg = "Kirishda xatolik yuz berdi.";
        if (data.error === "UNAUTHORIZED_ADMIN") {
          msg =
            "⛔ Ushbu Telegram hisobi admin panelga kirish huquqiga ega emas. Faqat belgilangan loyiha administratori kirishi mumkin.";
        } else if (data.error === "ADMIN_NOT_CONFIGURED") {
          msg =
            "⚠️ Serverda ADMIN_TELEGRAM_ID hali sozlanmagan. Tizim xavfsizlik talabiga binoan yopiq holatda (fail-closed).";
        } else if (data.error === "EXPIRED_AUTH" || data.error === "INVALID_HASH") {
          msg = "❌ Telegram autentifikatsiyasi tekshiruvdan o'tmadi yoki eskirgan.";
        } else if (data.message) {
          msg = data.message;
        }
        setError(msg);
        setLoading(false);
        return;
      }

      // Muvaffaqiyatli kirish
      router.push("/");
    } catch (err: any) {
      setError("Tarmoq yoki server bilan bog'lanishda xatolik yuz berdi.");
      setLoading(false);
    }
  };

  useEffect(() => {
    // Global callback yaratish
    (window as any).onTelegramAuth = (user: any) => {
      handleTelegramAuth(user);
    };

    // Telegram widget scriptini yuklash
    if (widgetContainerRef.current) {
      widgetContainerRef.current.innerHTML = "";
      const script = document.createElement("script");
      script.src = "https://telegram.org/js/telegram-widget.js?22";
      script.setAttribute("data-telegram-login", botUsername);
      script.setAttribute("data-size", "large");
      script.setAttribute("data-radius", "8");
      script.setAttribute("data-onauth", "onTelegramAuth(user)");
      script.async = true;
      widgetContainerRef.current.appendChild(script);
    }

    return () => {
      delete (window as any).onTelegramAuth;
    };
  }, [botUsername]);

  return (
    <div className="login-screen">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">⚗️</div>
          <h1>JDA Kimyo Quiz</h1>
          <p>Yagona admin boshqaruv paneli</p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div style={{ textAlign: "center", marginBottom: "1rem" }}>
          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}>
            Tizimga kirish uchun quyidagi rasmiy Telegram tugmasini bosing:
          </p>
        </div>

        <div className="widget-container" ref={widgetContainerRef}>
          {loading ? (
            <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
              ⏳ Autentifikatsiya tekshirilmoqda...
            </p>
          ) : (
            <p style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>
              Telegram Login vidjeti yuklanmoqda...
            </p>
          )}
        </div>

        <div className="alert alert-info" style={{ marginTop: "1.5rem", fontSize: "0.775rem" }}>
          ℹ️ <b>Eslatma:</b> Telegram Login vidjeti ishlashi uchun bot domenini
          BotFather&apos;da <code>/setdomain</code> buyrug&apos;i orqali ulash kerak.
        </div>
      </div>
    </div>
  );
}
