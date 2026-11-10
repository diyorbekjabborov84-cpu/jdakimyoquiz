"use client";

import { AdminSessionState } from "@/lib/useAdminSession";

interface SessionWarmupBannerProps {
  sessionState: AdminSessionState;
  retryAttempt: number;
  maxRetries: number;
  onRetry: () => void;
}

export default function SessionWarmupBanner({
  sessionState,
  retryAttempt,
  maxRetries,
  onRetry,
}: SessionWarmupBannerProps) {
  if (sessionState !== "waking" && sessionState !== "unavailable") {
    return null;
  }

  if (sessionState === "waking") {
    return (
      <div
        className="alert alert-info"
        style={{
          marginBottom: "1.25rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "1rem",
          flexWrap: "wrap",
        }}
      >
        <div>
          <div style={{ fontWeight: 600 }}>
            ⏳ Server uyg&apos;onmoqda, biroz kuting…
          </div>
          <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)", marginTop: "2px" }}>
            Render serveri sovuq holatdan ishga tushmoqda. Sessiyangiz saqlangan — avtomatik qayta urinilmoqda ({retryAttempt}/{maxRetries}).
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="alert alert-danger"
      style={{
        marginBottom: "1.25rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "1rem",
        flexWrap: "wrap",
      }}
    >
      <div>
        <div style={{ fontWeight: 600 }}>
          ⚠️ Server hali javob bermadi
        </div>
        <div style={{ fontSize: "0.8rem", marginTop: "2px" }}>
          Server uyg&apos;onishi odatdagidan uzoqroq davom etdi. Cookie va sessiyangiz o&apos;chirilmadi — qayta urinib ko&apos;ring.
        </div>
      </div>
      <button
        type="button"
        onClick={onRetry}
        className="btn btn-primary"
        style={{ fontSize: "0.82rem", padding: "0.45rem 0.9rem" }}
      >
        🔄 Qayta urinish
      </button>
    </div>
  );
}
