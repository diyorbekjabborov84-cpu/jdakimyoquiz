"use client";

import { useEffect, useState } from "react";

interface HealthState {
  loading: boolean;
  status: "healthy" | "unhealthy" | "unreachable" | "unknown";
  latencyMs?: number;
  uptime?: number;
}

export default function HealthBadge() {
  const [health, setHealth] = useState<HealthState>({
    loading: true,
    status: "unknown",
  });

  const checkHealth = async () => {
    setHealth((prev) => ({ ...prev, loading: true }));
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (res.ok && data.ok) {
        setHealth({
          loading: false,
          status: "healthy",
          latencyMs: data.latencyMs,
          uptime: data.render?.uptime,
        });
      } else {
        setHealth({
          loading: false,
          status: data.status === "unhealthy" ? "unhealthy" : "unreachable",
          latencyMs: data.latencyMs,
        });
      }
    } catch {
      setHealth({
        loading: false,
        status: "unreachable",
      });
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30s interval
    return () => clearInterval(interval);
  }, []);

  const getStatusBadge = () => {
    if (health.loading && health.status === "unknown") {
      return <span className="badge badge-warning">⏳ Tekshirilmoqda...</span>;
    }
    if (health.status === "healthy") {
      return (
        <span className="badge badge-success">
          🟢 Render faol {health.latencyMs !== undefined && `(${health.latencyMs}ms)`}
        </span>
      );
    }
    if (health.status === "unhealthy") {
      return <span className="badge badge-warning">🟡 Xizmat nosoz</span>;
    }
    return <span className="badge badge-danger">🔴 Server uzilgan</span>;
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
      {getStatusBadge()}
      <button
        onClick={checkHealth}
        className="btn btn-outline"
        style={{ padding: "0.2rem 0.5rem", fontSize: "0.75rem" }}
        title="Qayta tekshirish"
        disabled={health.loading}
      >
        🔄
      </button>
    </div>
  );
}
