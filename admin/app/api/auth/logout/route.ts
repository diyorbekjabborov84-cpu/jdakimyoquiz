import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE } from "@/lib/auth";
import { verifyMutationOrigin, handleCsrfError } from "@/lib/csrf";

export async function POST(req: NextRequest) {
  const originCheck = verifyMutationOrigin(req);
  if (!originCheck.valid) {
    return handleCsrfError();
  }

  const res = NextResponse.json({ ok: true, message: "Muvaffaqiyatli chiqildi" });

  res.cookies.set({
    name: ADMIN_SESSION_COOKIE,
    value: "",
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 0,
  });

  return res;
}
