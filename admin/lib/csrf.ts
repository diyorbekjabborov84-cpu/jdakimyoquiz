import { NextRequest, NextResponse } from "next/server";

/**
 * Mutatsiya so'rovlari (POST, PUT, DELETE) uchun Origin va CSRF tekshiruvi.
 * Brauzerdan yuborilgan so'rovning Origin sarlavhasi o'z domeni yoki
 * ruxsat etilgan admin domeniga to'liq mos kelishini talab qiladi.
 */
export function verifyMutationOrigin(req: NextRequest): { valid: boolean; error?: string } {
  // Fetch metadata tekshiruvi: Agar cross-site bo'lsa darhol rad etiladi
  const secFetchSite = req.headers.get("sec-fetch-site");
  if (secFetchSite === "cross-site") {
    return { valid: false, error: "CROSS_SITE_MUTATION_FORBIDDEN" };
  }

  const origin = req.headers.get("origin");
  const host = req.headers.get("host");

  if (!origin) {
    // Origin bo'lmasa faqat tekshiriladigan Referer bilan davom etamiz.
    const referer = req.headers.get("referer");
    if (!referer || !host) {
      return { valid: false, error: "ORIGIN_REQUIRED" };
    }
    try {
      const refUrl = new URL(referer);
      if (refUrl.host !== host || refUrl.origin !== req.nextUrl.origin) {
        return { valid: false, error: "REFERER_ORIGIN_MISMATCH" };
      }
    } catch {
      return { valid: false, error: "INVALID_REFERER" };
    }
    return { valid: true };
  }

  try {
    const originUrl = new URL(origin);

    // 1. Same-origin tekshiruvi (request host bilan solishtirish)
    if (host && originUrl.host === host) {
      return { valid: true };
    }

    // 2. NextURL origin bilan solishtirish
    if (originUrl.origin === req.nextUrl.origin) {
      return { valid: true };
    }

    // 3. Konfiguratsiyalangan ruxsatli domen (agar bor bo'lsa)
    const allowedOrigin = process.env.ADMIN_ALLOWED_ORIGIN?.trim();
    if (allowedOrigin && originUrl.origin === allowedOrigin) {
      return { valid: true };
    }

    return { valid: false, error: "CSRF_ORIGIN_MISMATCH" };
  } catch {
    return { valid: false, error: "MALFORMED_ORIGIN" };
  }
}

export function handleCsrfError(): NextResponse {
  return NextResponse.json(
    {
      ok: false,
      error: "CSRF_FORBIDDEN",
      message: "So'rov manbasi (Origin) tasdiqlanmadi. Ruxsatsiz cross-site murojaat.",
    },
    { status: 403 }
  );
}
