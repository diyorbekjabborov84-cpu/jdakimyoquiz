import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "../../../../lib/auth";
import { verifyMutationOrigin, handleCsrfError } from "../../../../lib/csrf";

export async function POST(req: NextRequest) {
  const originCheck = verifyMutationOrigin(req);
  if (!originCheck.valid) {
    return handleCsrfError();
  }

  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  try {
    const renderUrl = getRenderApiUrl();
    const response = await fetch(`${renderUrl}/api/admin/kurs/qayta-yuklash`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
      signal: AbortSignal.timeout(20000),
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
