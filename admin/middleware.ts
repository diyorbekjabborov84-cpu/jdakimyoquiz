import { NextRequest, NextResponse } from "next/server";
import { ADMIN_SESSION_COOKIE } from "./lib/auth";

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Statik fayllar, Next.js ichki yo'llari, API va /login sahifasini o'tkazib yuborish
  if (
    pathname.startsWith("/api/") ||
    pathname.startsWith("/_next/") ||
    pathname.startsWith("/login") ||
    pathname === "/favicon.ico"
  ) {
    return NextResponse.next();
  }

  const sessionToken = req.cookies.get(ADMIN_SESSION_COOKIE)?.value;
  if (!sessionToken || !sessionToken.trim()) {
    const loginUrl = new URL("/login", req.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
