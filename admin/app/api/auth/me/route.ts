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
    });

    if (!response.ok) {
      return NextResponse.json({ ok: false, error: "SESSION_INVALID" }, { status: 401 });
    }

    // Tokenni parsing qilish (JWT payload)
    const parts = token.split(".");
    let user: any = { id: "admin" };
    if (parts.length === 3) {
      try {
        const payload = JSON.parse(Buffer.from(parts[1], "base64url").toString("utf-8"));
        user = {
          id: payload.adminId,
          username: payload.username,
        };
      } catch {
        // fallback
      }
    }

    return NextResponse.json({ ok: true, user });
  } catch (err) {
    return NextResponse.json(
      { ok: false, error: "RENDER_CONNECTION_ERROR" },
      { status: 502 }
    );
  }
}
