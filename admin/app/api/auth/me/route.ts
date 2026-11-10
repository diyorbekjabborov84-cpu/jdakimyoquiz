import { NextRequest, NextResponse } from "next/server";
import {
  ADMIN_SESSION_COOKIE,
  ADMIN_SESSION_MAX_AGE_SECONDS,
  getRenderApiUrl,
} from "../../../../lib/auth";

export async function GET(req: NextRequest) {
  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;

  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  try {
    const renderUrl = getRenderApiUrl();
    let response = await fetch(`${renderUrl}/api/admin/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
      signal: AbortSignal.timeout(12000),
    });

    // Eski mock serverlar uchun zaxira (/api/admin/me 404 bo'lsa /api/admin/overview tekshiriladi)
    if (response.status === 404) {
      response = await fetch(`${renderUrl}/api/admin/overview`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        cache: "no-store",
        signal: AbortSignal.timeout(12000),
      });
    }

    if (response.status === 401 || response.status === 403) {
      return NextResponse.json({ ok: false, error: "SESSION_INVALID" }, { status: 401 });
    }

    if (!response.ok) {
      return NextResponse.json({ ok: false, error: "RENDER_UNAVAILABLE" }, { status: 503 });
    }

    const data = await response.json().catch(() => ({}));

    // Tokenni parsing qilish (JWT payload)
    const parts = token.split(".");
    let user: any = data?.user || { id: "admin" };
    if (!data?.user && parts.length === 3) {
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

    const res = NextResponse.json({
      ok: true,
      user,
      renewed: Boolean(data?.renewedToken),
    });

    // Sirpanuvchi (sliding) sessiya: qolgan muddat < 7 kun bo'lsa, 30 kunlik yangi cookie o'rnatiladi
    if (typeof data?.renewedToken === "string" && data.renewedToken) {
      res.cookies.set({
        name: ADMIN_SESSION_COOKIE,
        value: data.renewedToken,
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: ADMIN_SESSION_MAX_AGE_SECONDS,
      });
    }

    res.headers.set("Cache-Control", "no-store");
    return res;
  } catch {
    return NextResponse.json(
      { ok: false, error: "RENDER_CONNECTION_ERROR" },
      { status: 502 }
    );
  }
}
