"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { getGoogleIdToken } from "@/lib/google-login";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const widgetContainerRef = useRef<HTMLDivElement>(null);

  const handleGoogleAuth = async () => {
    if (loading) return;
    setLoading(true);
    setError(null);
    try {
      const idToken = await getGoogleIdToken();
      const response = await fetch("/api/auth/google", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken }),
      });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.message || "Google akkauntingizga kirish ruxsati berilmagan.");
      router.replace("/");
    } catch (err: any) {
      if (err.code === "auth/popup-closed-by-user" || err.code === "auth/cancelled-popup-request") setError(null);
      else if (err.code === "auth/popup-blocked") setError("Brauzerda ochiluvchi oynaga ruxsat bering va qayta urinib ko‘ring.");
      else if (err.message === "GOOGLE_NOT_CONFIGURED") setError("Google orqali kirish hali sozlanmagan.");
      else setError(err.code ? "Google orqali kirishda xatolik yuz berdi. Qayta urinib ko‘ring." : err.message);
    } finally { setLoading(false); }
  };

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
            Google yoki Telegram akkauntingiz orqali kiring.
          </p>
        </div>

        <button type="button" className="btn btn-primary" disabled={loading} onClick={handleGoogleAuth}
          style={{ width: "100%", marginBottom: "1rem", padding: "0.8rem", cursor: loading ? "wait" : "pointer" }}>
          {loading ? "Kirish tekshirilmoqda…" : "Google orqali kirish"}
        </button>
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
          Faqat loyiha administratorining akkauntlariga ruxsat beriladi.
        </div>
      </div>
    </div>
  );
}
