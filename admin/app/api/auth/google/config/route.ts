import { NextResponse } from "next/server";
export const dynamic = "force-dynamic";
export function GET() {
  return NextResponse.json({
    // Firebase web configuration is public; authorization is enforced on Render.
    apiKey: "AIzaSyD7Xp5Se4QMr72OBjx36OI16HkvnEAd6rA",
    authDomain: "jda-kimyo-quiz.firebaseapp.com",
    projectId: "jda-kimyo-quiz",
    appId: "1:116732620330:web:f9a0c4af464f70a5de5d53",
  }, { headers: { "Cache-Control": "no-store" } });
}
