import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "../../../lib/auth";

export async function GET(req: NextRequest) {
  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;

  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q") || "";
  const limit = searchParams.get("limit") || "50";
  const cursor = searchParams.get("cursor");

  try {
    const renderUrl = getRenderApiUrl();
    const params = new URLSearchParams({ q, limit });
    if (cursor) params.set("cursor", cursor);
    const queryStr = params.toString();
    const response = await fetch(`${renderUrl}/api/admin/users?${queryStr}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (err: any) {
    return NextResponse.json(
      {
        ok: false,
        error: "RENDER_CONNECTION_ERROR",
        message: "Render serveri bilan bog'lanib bo'lmadi.",
      },
      { status: 502 }
    );
  }
}
