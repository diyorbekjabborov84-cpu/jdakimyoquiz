import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "@/lib/auth";
import { verifyMutationOrigin, handleCsrfError } from "@/lib/csrf";

export async function POST(req: NextRequest) {
  // Origin va CSRF tekshiruvi
  const originCheck = verifyMutationOrigin(req);
  if (!originCheck.valid) {
    return handleCsrfError();
  }

  try {
    const body = await req.json();
    const renderUrl = getRenderApiUrl();

    const response = await fetch(`${renderUrl}/api/auth/google`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      cache: "no-store",
      signal: AbortSignal.timeout(20000),
    });

    const data = await response.json();

    if (!response.ok || !data.ok) {
      return NextResponse.json(data, { status: response.status || 401 });
    }

    const res = NextResponse.json({
      ok: true,
      user: data.user,
    });

    // HttpOnly, Secure, SameSite: "lax" xavfsiz cookie Vercel domenida o'rnatiladi
    res.cookies.set({
      name: ADMIN_SESSION_COOKIE,
      value: data.token,
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 7 * 86400, // 7 kun
    });
    res.headers.set("Cache-Control", "no-store");

    return res;
  } catch (error: any) {
    return NextResponse.json(
      {
        ok: false,
        error: "RENDER_CONNECTION_ERROR",
        message: "Render serveri bilan bog'lanishda xatolik yuz berdi.",
      },
      { status: 502 }
    );
  }
}
