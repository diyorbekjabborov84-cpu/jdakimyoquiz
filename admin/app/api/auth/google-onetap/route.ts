import { NextRequest, NextResponse } from "next/server";
import {
  ADMIN_SESSION_COOKIE,
  ADMIN_SESSION_MAX_AGE_SECONDS,
  getRenderApiUrl,
} from "../../../../lib/auth";
import { verifyMutationOrigin, handleCsrfError } from "../../../../lib/csrf";

export async function POST(req: NextRequest) {
  // Origin va CSRF tekshiruvi
  const originCheck = verifyMutationOrigin(req);
  if (!originCheck.valid) {
    return handleCsrfError();
  }

  try {
    const body = await req.json();
    const renderUrl = getRenderApiUrl();

    const response = await fetch(`${renderUrl}/api/auth/google-onetap`, {
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

    res.cookies.set({
      name: ADMIN_SESSION_COOKIE,
      value: data.token,
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: ADMIN_SESSION_MAX_AGE_SECONDS, // 30 kun
    });
    res.headers.set("Cache-Control", "no-store");

    return res;
  } catch {
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
