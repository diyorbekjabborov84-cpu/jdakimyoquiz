"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  getGoogleIdToken,
  checkExistingSessionAndRedirect,
  shouldSkipOneTapAutoLogin,
  LOGOUT_SESSION_FLAG,
} from "@/lib/google-login";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const widgetContainerRef = useRef<HTMLDivElement>(null);
  const oneTapAttemptedRef = useRef(false);

  const handleOneTapCredential = async (credential: string) => {
    if (!credential || loading) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/auth/google-onetap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credential }),
      });
      const data = await response.json();
      if (!response.ok || !data.ok) {
        throw new Error(data.message || "Bu hisobga ruxsat yo'q");
      }
      try {
        sessionStorage.removeItem(LOGOUT_SESSION_FLAG);
      } catch {
        // ignore
      }
      router.replace("/");
    } catch (err: any) {
      setError(err?.message || "Bu hisobga ruxsat yo'q");
      setLoading(false);
    }
  };

  const handleGoogleAuth = async () => {
    if (loading) return;
    setLoading(true);
    setError(null);
    try {
      try {
        sessionStorage.removeItem(LOGOUT_SESSION_FLAG);
      } catch {
        // ignore
      }
      const idToken = await getGoogleIdToken();
      const response = await fetch("/api/auth/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken }),
      });
      const data = await response.json();
      if (!response.ok || !data.ok) {
        throw new Error(data.message || "Bu hisobga ruxsat yo'q");
      }
      router.replace("/");
    } catch (err: any) {
      if (
        err.code === "auth/popup-closed-by-user" ||
        err.code === "auth/cancelled-popup-request"
      ) {
        setError(null);
      } else if (err.code === "auth/popup-blocked") {
        setError("Brauzerda ochiluvchi oynaga ruxsat bering va qayta urinib ko‘ring.");
      } else if (err.message === "GOOGLE_NOT_CONFIGURED") {
        setError("Google orqali kirish hali sozlanmagan.");
      } else {
        setError(
          err.code
            ? "Google orqali kirishda xatolik yuz berdi. Qayta urinib ko‘ring."
            : err.message
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const botUsername = process.env.NEXT_PUBLIC_BOT_USERNAME || "jdakimyoquizbot";

  const handleTelegramAuth = async (user: any) => {
    setLoading(true);
    setError(null);

    try {
      try {
        sessionStorage.removeItem(LOGOUT_SESSION_FLAG);
      } catch {
        // ignore
      }
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

      router.replace("/");
    } catch {
      setError("Tarmoq yoki server bilan bog'lanishda xatolik yuz berdi.");
      setLoading(false);
    }
  };

  useEffect(() => {
    let active = true;

    const initSessionAndOneTap = async () => {
      // 1. Mavjud yaroqli sessiya bo'lsa, darhol "/" ga o'tkazish
      const redirected = await checkExistingSessionAndRedirect(fetch, (p) => router.replace(p));
      if (!active || redirected) return;
      setCheckingSession(false);

      // 2. Agar foydalanuvchi "Chiqish" bosgan bo'lsa, avtomatik One Tap ishga tushmasin
      if (shouldSkipOneTapAutoLogin()) {
        try {
          (window as any).google?.accounts?.id?.disableAutoSelect?.();
        } catch {
          // ignore
        }
        return;
      }

      if (oneTapAttemptedRef.current) return;
      oneTapAttemptedRef.current = true;

      try {
        const cfgRes = await fetch("/api/auth/google/config", { cache: "no-store" });
        if (!cfgRes.ok) return;
        const cfg = await cfgRes.json();
        const clientId = typeof cfg?.googleClientId === "string" ? cfg.googleClientId.trim() : "";
        if (!clientId || !active) return;

        const startOneTap = () => {
          if (!active) return;
          const gsi = (window as any).google?.accounts?.id;
          if (!gsi) return;
          gsi.initialize({
            client_id: clientId,
            callback: (resp: { credential?: string }) => {
              if (resp?.credential) {
                void handleOneTapCredential(resp.credential);
              }
            },
            auto_select: true,
            use_fedcm_for_prompt: true,
            cancel_on_tap_outside: false,
          });
          gsi.prompt();
        };

        if ((window as any).google?.accounts?.id) {
          startOneTap();
        } else {
          const existingScript = document.querySelector(
            'script[src="https://accounts.google.com/gsi/client"]'
          ) as HTMLScriptElement | null;
          if (existingScript) {
            existingScript.addEventListener("load", startOneTap, { once: true });
          } else {
            const gsiScript = document.createElement("script");
            gsiScript.src = "https://accounts.google.com/gsi/client";
            gsiScript.async = true;
            gsiScript.defer = true;
            gsiScript.onload = startOneTap;
            document.head.appendChild(gsiScript);
          }
        }
      } catch {
        // One Tap ixtiyoriy; zaxira tugmalar ishlayveradi
      }
    };

    void initSessionAndOneTap();

    return () => {
      active = false;
    };
  }, [router]);

  useEffect(() => {
    (window as any).onTelegramAuth = (user: any) => {
      handleTelegramAuth(user);
    };

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
            {checkingSession
              ? "Mavjud sessiya tekshirilmoqda..."
              : "Google yoki Telegram akkauntingiz orqali kiring."}
          </p>
        </div>

        <button
          type="button"
          className="btn btn-primary"
          disabled={loading}
          onClick={handleGoogleAuth}
          style={{
            width: "100%",
            marginBottom: "1.25rem",
            padding: "0.85rem 1.25rem",
            fontSize: "0.95rem",
            fontWeight: 600,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.6rem",
            cursor: loading ? "wait" : "pointer",
            background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
            boxShadow: "0 4px 12px rgba(37, 99, 235, 0.25)",
            border: "none",
            borderRadius: "8px",
            color: "#ffffff",
          }}
        >
          <span>🔐</span>
          <span>
            {loading ? "Kirish tekshirilmoqda…" : "Google orqali to'g'ridan-to'g'ri kirish"}
          </span>
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
