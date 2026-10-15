import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE, getRenderApiUrl } from "@/lib/auth";

export async function GET(req: NextRequest) {
  const token = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;
  if (!token) {
    return NextResponse.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const quizId = searchParams.get("quizId") || "";
  const chatId = searchParams.get("chatId") || "";
  const limit = searchParams.get("limit") || "50";

  try {
    const renderUrl = getRenderApiUrl();
    const params = new URLSearchParams({ limit });
    if (quizId) params.set("quizId", quizId);
    if (chatId) params.set("chatId", chatId);

    const response = await fetch(`${renderUrl}/api/admin/results?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
      signal: AbortSignal.timeout(15000),
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
