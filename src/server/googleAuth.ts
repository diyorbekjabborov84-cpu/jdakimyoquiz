import { getAuth } from "firebase-admin/auth";

export const ADMIN_GOOGLE_EMAIL = "diyorbekjabborov84@gmail.com";

export async function verifyGoogleAdmin(
  idToken: string,
  verify = (token: string) => getAuth().verifyIdToken(token, true)
): Promise<boolean> {
  try {
    const claims = await verify(idToken);
    return claims.email_verified === true &&
      claims.email?.toLowerCase() === ADMIN_GOOGLE_EMAIL &&
      claims.firebase?.sign_in_provider === "google.com" &&
      Number.isFinite(claims.auth_time) &&
      Math.floor(Date.now() / 1000) - claims.auth_time <= 300 &&
      claims.auth_time <= Math.floor(Date.now() / 1000) + 60;
  } catch {
    return false;
  }
}
