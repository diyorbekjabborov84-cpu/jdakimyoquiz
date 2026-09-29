import { getApps, initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, inMemoryPersistence, setPersistence, signInWithPopup, signOut } from "firebase/auth";

export async function getGoogleIdToken() {
  const config = await fetch("/api/auth/google/config", { cache: "no-store" }).then(r => r.json());
  if (!config.apiKey) throw new Error("GOOGLE_NOT_CONFIGURED");
  const app = getApps()[0] || initializeApp(config);
  const auth = getAuth(app);
  await setPersistence(auth, inMemoryPersistence);
  const provider = new GoogleAuthProvider();
  provider.setCustomParameters({ prompt: "select_account" });
  try {
    const result = await signInWithPopup(auth, provider);
    return await result.user.getIdToken();
  } finally {
    await signOut(auth);
  }
}
