import assert from "node:assert/strict";
import { verifyGoogleAdmin, ADMIN_GOOGLE_EMAIL } from "../src/server/googleAuth.js";

async function main() {
  const claims = { email: ADMIN_GOOGLE_EMAIL, email_verified: true, auth_time: Math.floor(Date.now() / 1000), firebase: { sign_in_provider: "google.com" } };
  const verify = (value: any) => async (_token: string): Promise<any> => value;
  assert.equal(await verifyGoogleAdmin("signed", verify(claims)), true);
  for (const patch of [
    { email: "someone@gmail.com" }, { email: undefined }, { email_verified: false },
    { firebase: { sign_in_provider: "password" } }, { auth_time: 0 },
    { auth_time: Math.floor(Date.now() / 1000) + 120 },
  ]) assert.equal(await verifyGoogleAdmin("signed", verify({ ...claims, ...patch })), false);
  assert.equal(await verifyGoogleAdmin("forged", async () => { throw new Error("invalid signature"); }), false);
  console.log("Google auth: allowed email, provider, verified email, freshness and invalid token checks passed");
}
main().catch(e => { console.error(e); process.exitCode = 1; });
