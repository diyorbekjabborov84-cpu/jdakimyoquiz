import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "@/lib/auth";

export async function GET(req: NextRequest) {
  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;

  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  try {
    const renderUrl = getRenderApiUrl();
    const response = await fetch(`${renderUrl}/api/admin/overview`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      // Keshni cheklash uchun no-store
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
