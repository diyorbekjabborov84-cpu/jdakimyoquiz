export const ADMIN_SESSION_COOKIE = "admin_session";

export function getRenderApiUrl(): string {
  const url = process.env.RENDER_API_URL?.trim();

  if (process.env.NODE_ENV === "production") {
    if (!url) {
      throw new Error("RENDER_API_URL_NOT_CONFIGURED: Production muhitida RENDER_API_URL sozlanmagan!");
    }
    return url.replace(/\/+$/, "");
  }

  // Development yoki test muhitida fallback ruxsat etiladi
  return (url || "http://localhost:3000").replace(/\/+$/, "");
}
