import type { Api, Context, NextFunction } from "grammy";
import type { Firestore } from "firebase-admin/firestore";
import { FIRESTORE_COLLECTIONS, getFirestoreDb } from "../firebase/firestore.js";
import { trackGroupEvent } from "./tracker.js";

/** Register groups even when no quiz command is sent. Lifecycle handlers own membership status. */
export async function trackGroupUpdate(ctx: Context, next: NextFunction): Promise<void> {
  const chat = ctx.chat;
  if (chat && (chat.type === "group" || chat.type === "supergroup") && !ctx.myChatMember) {
    await Promise.all([
      trackGroupEvent(chat.id, { title: chat.title, type: chat.type }).catch(() => {}),
      next(),
    ]);
    return;
  }
  await next();
}

type RegistryApi = Pick<Api, "getMe" | "getChat" | "getChatMember" | "getChatMemberCount">;
export interface RestoreGroupsResult {
  discovered: number;
  added: number;
  unresolved: number;
  alreadyCompleted: boolean;
}

/** One-time, repeatable recovery. Existing registry entries always win over historical records. */
export async function restoreHistoricalGroups(
  api: RegistryApi,
  db: Firestore | null = getFirestoreDb(),
): Promise<RestoreGroupsResult> {
  if (!db) throw new Error("DATABASE_NOT_INITIALIZED");
  const marker = db.collection("admin_migrations").doc("group_registry_v1");
  const result: RestoreGroupsResult = { discovered: 0, added: 0, unresolved: 0, alreadyCompleted: false };
  if ((await marker.get()).data()?.completed === true) {
    return { ...result, alreadyCompleted: true };
  }

  const candidates = new Map<number, string>();
  for (const collection of [FIRESTORE_COLLECTIONS.SESSIONS, FIRESTORE_COLLECTIONS.RESULTS]) {
    let after: string | undefined;
    while (true) {
      let query = db.collection(collection).select("chatId", "createdAt", "updatedAt", "savedAt")
        .orderBy("__name__").limit(200);
      if (after) query = query.startAfter(after);
      const page = await query.get();
      for (const doc of page.docs) {
        const data = doc.data();
        const id = Number(data.chatId);
        if (!Number.isSafeInteger(id) || id >= 0) continue;
        let latest = candidates.get(id) || "";
        for (const raw of [data.createdAt, data.updatedAt, data.savedAt]) {
          if (typeof raw !== "string" && typeof raw !== "number") continue;
          const date = new Date(raw);
          if (Number.isFinite(date.getTime())) {
            const iso = date.toISOString();
            if (iso > latest) latest = iso;
          }
        }
        candidates.set(id, latest);
      }
      if (page.docs.length < 200) break;
      after = page.docs[page.docs.length - 1].id;
    }
  }
  result.discovered = candidates.size;

  let botId: number | undefined;
  if (candidates.size) {
    try { botId = (await api.getMe()).id; } catch { /* Keep historical groups visible as unknown. */ }
  }

  for (const [chatId, lastActivity] of candidates) {
    const ref = db.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(chatId));
    if ((await ref.get()).exists) continue;

    let title = `Guruh ${chatId}`;
    let type = "unknown";
    let status: "active" | "left" | "kicked" | "unknown" = "unknown";
    let memberCount: number | null = null;
    try {
      const chat = await api.getChat(chatId);
      if (chat.type !== "group" && chat.type !== "supergroup") continue;
      title = chat.title;
      type = chat.type;
      if (botId !== undefined) {
        const membership = await api.getChatMember(chatId, botId);
        if (membership.status === "left" || membership.status === "kicked") status = membership.status;
        else if (membership.status === "restricted") status = membership.is_member ? "active" : "left";
        else status = "active";
      }
      memberCount = await api.getChatMemberCount(chatId);
    } catch { /* A network/access failure is not evidence that the bot has left. */ }

    const now = new Date().toISOString();
    const added = await db.runTransaction(async (transaction) => {
      // A live event might have registered the group while Telegram calls were in flight.
      if ((await transaction.get(ref)).exists) return false;
      transaction.set(ref, {
        chatId, title, titleLower: title.toLowerCase().trim(), type, status,
        memberCount, lastActivity, updatedAt: now, createdAt: now,
        recoveredFromHistory: true,
        // Historical discovery must not override a subsequent live event.
        eventTimestamp: 0,
      });
      return true;
    });
    if (added) {
      result.added++;
      if (status === "unknown") result.unresolved++;
    }
  }
  await marker.set({ completed: true, completedAt: new Date().toISOString(), ...result });
  return result;
}
