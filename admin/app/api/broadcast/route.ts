import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "@/lib/auth";
import { verifyMutationOrigin, handleCsrfError } from "@/lib/csrf";

export const maxDuration = 60;

export async function POST(req: NextRequest) {
  // Origin va CSRF tekshiruvi
  const originCheck = verifyMutationOrigin(req);
  if (!originCheck.valid) {
    return handleCsrfError();
  }

  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  try {
    const body = await req.json();
    const renderUrl = getRenderApiUrl();

    const response = await fetch(`${renderUrl}/api/admin/broadcast`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(body),
      cache: "no-store",
      signal: AbortSignal.timeout(55000),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (err: any) {
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
