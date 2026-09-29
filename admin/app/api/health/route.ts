import { NextResponse } from "next/server";
import { getRenderApiUrl } from "@/lib/auth";

export async function GET() {
  const start = Date.now();
  try {
    const renderUrl = getRenderApiUrl();
    const response = await fetch(`${renderUrl}/health`, {
      cache: "no-store",
    });
    const latency = Date.now() - start;

    if (!response.ok) {
      return NextResponse.json({
        ok: false,
        status: "unhealthy",
        httpStatus: response.status,
        latencyMs: latency,
      });
    }

    const data = await response.json();
    return NextResponse.json({
      ok: true,
      status: "healthy",
      latencyMs: latency,
      render: data,
    });
  } catch (err: any) {
    const latency = Date.now() - start;
    return NextResponse.json({
      ok: false,
      status: "unreachable",
      latencyMs: latency,
      error: err?.message || "Failed to reach Render",
    });
  }
}
