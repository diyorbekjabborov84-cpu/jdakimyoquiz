import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";
import { trackGroupEvent } from "../tracking/tracker.js";
import { recordAuditLog } from "./auditService.js";

export interface BroadcastButton {
  text: string;
  url: string;
}

export interface BroadcastRequest {
  target: "all_groups" | "private_users" | "selected_groups";
  selectedChatIds?: (number | string)[];
  message: string;
  imageUrl?: string;
  buttons?: BroadcastButton[];
  adminUser?: string;
}

export interface BroadcastHistoryItem {
  id: string;
  target: string;
  message: string;
  imageUrl?: string;
  buttons?: BroadcastButton[];
  totalTargets: number;
  successful: number;
  failed: number;
  admin: string;
  sentAt: string;
  createdAt: number;
}

// In-memory zaxira tarix
const inMemoryHistory: BroadcastHistoryItem[] = [];

/**
 * Telegram tugma havolasini xavfsiz tozalash va tekshirish
 */
function sanitizeButtonUrl(rawUrl: string): string | null {
  let url = (rawUrl || "").trim();
  if (!url) return null;
  if (!/^https?:\/\//i.test(url) && !/^tg:\/\//i.test(url)) {
    if (url.startsWith("t.me/")) {
      url = "https://" + url;
    } else if (url.startsWith("@")) {
      url = "https://t.me/" + url.slice(1);
    } else {
      url = "https://" + url;
    }
  }
  try {
    new URL(url);
    return url;
  } catch {
    return null;
  }
}

/**
 * Xabar tarqatish uchun maqsadli chat ID larini Firestore'dan yuklash
 */
export async function resolveBroadcastTargets(
  target: "all_groups" | "private_users" | "selected_groups",
  selectedChatIds?: (number | string)[]
): Promise<number[]> {
  if (target === "selected_groups" && selectedChatIds && selectedChatIds.length > 0) {
    return Array.from(
      new Set(
        selectedChatIds
          .map((id) => Number(id))
          .filter((id) => !isNaN(id) && id !== 0)
      )
    );
  }

  const db = getFirestoreDb();
  if (!db) {
    if (target === "selected_groups" && selectedChatIds) {
      return Array.from(new Set(selectedChatIds.map(Number).filter((id) => !isNaN(id) && id !== 0)));
    }
    return [];
  }

  const targets: number[] = [];

  if (target === "all_groups") {
    // Faol guruhlar
    const snap = await db
      .collection(FIRESTORE_COLLECTIONS.GROUPS)
      .where("status", "==", "active")
      .limit(500)
      .get();

    for (const doc of snap.docs) {
      const data = doc.data();
      const chatId = Number(data.chatId);
      if (!isNaN(chatId)) targets.push(chatId);
    }
  } else if (target === "private_users") {
    // Shaxsiy botda faol foydalanuvchilar
    const snap = await db
      .collection(FIRESTORE_COLLECTIONS.USERS)
      .where("privateChatActive", "==", true)
      .limit(1000)
      .get();

    for (const doc of snap.docs) {
      const data = doc.data();
      const userId = Number(data.userId);
      if (!isNaN(userId)) targets.push(userId);
    }
  }

  return Array.from(new Set(targets));
}

/**
 * Telegram API orqali xavfsiz va navbatli broadcast bajarish
 */
export async function executeBroadcast(
  req: BroadcastRequest,
  telegramApi: any
): Promise<BroadcastHistoryItem> {
  const admin = req.adminUser || "admin";
  const now = Date.now();
  const sentAt = new Date(now).toISOString();

  // 1. Manzillarni aniqlash va takrorlanishdan tozalash
  const chatIds = await resolveBroadcastTargets(req.target, req.selectedChatIds);

  let successful = 0;
  let failed = 0;

  // 2. Inline klaviatura tayyorlash (yaroqsiz yoki xavfli URL larni filtrlaymiz)
  const validButtons = (req.buttons || [])
    .map((b) => {
      const cleanUrl = sanitizeButtonUrl(b.url);
      return cleanUrl ? { text: b.text.trim(), url: cleanUrl } : null;
    })
    .filter((b): b is { text: string; url: string } => Boolean(b && b.text));

  const replyMarkup =
    validButtons.length > 0
      ? {
          inline_keyboard: validButtons.map((b) => [{ text: b.text, url: b.url }]),
        }
      : undefined;

  // 3. Ketma-ket, tezlik chegarasiga mos yuborish (rate limit: ~20 ta/sekund)
  if (telegramApi && chatIds.length > 0) {
    for (const chatId of chatIds) {
      try {
        if (req.imageUrl && req.imageUrl.trim()) {
          await telegramApi.sendPhoto(chatId, req.imageUrl.trim(), {
            caption: req.message,
            parse_mode: "HTML",
            reply_markup: replyMarkup,
          });
        } else {
          await telegramApi.sendMessage(chatId, req.message, {
            parse_mode: "HTML",
            reply_markup: replyMarkup,
          });
        }
        successful++;
      } catch (err: any) {
        const desc = String(err?.description || err?.message || "");

        // Agar HTML teglarida xatolik bo'lsa (masalan unclosed tag), plain text rejimida qayta urinish
        if (desc.includes("can't parse entities") || desc.includes("parsing error")) {
          try {
            if (req.imageUrl && req.imageUrl.trim()) {
              await telegramApi.sendPhoto(chatId, req.imageUrl.trim(), {
                caption: req.message,
                reply_markup: replyMarkup,
              });
            } else {
              await telegramApi.sendMessage(chatId, req.message, {
                reply_markup: replyMarkup,
              });
            }
            successful++;
            await new Promise((r) => setTimeout(r, 45));
            continue;
          } catch {
            // plain text ham xato bersa quyiga o'tadi
          }
        }

        failed++;
        console.warn(`[Broadcast] Chat ${chatId} ga yuborishda xatolik:`, desc);

        // Agar bot guruhdan chiqarilgan yoki bloklangan bo'lsa, holatni yangilaymiz
        if (
          desc.includes("kicked") ||
          desc.includes("chat not found") ||
          desc.includes("bot was blocked")
        ) {
          trackGroupEvent(chatId, { status: "kicked" }).catch(() => {});
        }

        // Agar Telegram 429 flood wait bersa
        if (err?.parameters?.retry_after) {
          const waitSec = Math.min(Number(err.parameters.retry_after) || 1, 30);
          await new Promise((r) => setTimeout(r, (waitSec + 1) * 1000));
        }
      }

      // Xavfsiz oraliq (Telegram 30 msgs/sec cheklovidan past)
      await new Promise((r) => setTimeout(r, 45));
    }
  } else if (!telegramApi) {
    // Mock rejim (testlarda yoki api bo'lmaganda)
    successful = chatIds.length;
  }

  // 4. Tarixga yozish
  const historyItem: BroadcastHistoryItem = {
    id: `bc_${now}_${Math.random().toString(36).substring(2, 7)}`,
    target: req.target,
    message: req.message,
    imageUrl: req.imageUrl || undefined,
    buttons: req.buttons || [],
    totalTargets: chatIds.length,
    successful,
    failed,
    admin,
    sentAt,
    createdAt: now,
  };

  inMemoryHistory.unshift(historyItem);
  if (inMemoryHistory.length > 100) inMemoryHistory.pop();

  const db = getFirestoreDb();
  if (db) {
    try {
      await db.collection(FIRESTORE_COLLECTIONS.BROADCASTS).doc(historyItem.id).set(historyItem);
    } catch (e: any) {
      console.error("[Broadcast] Tarixni Firestore'ga saqlashda xatolik:", e?.message || e);
    }
  }

  // 5. Audit log
  await recordAuditLog({
    admin,
    action: "BROADCAST_SENT",
    details: {
      target: req.target,
      totalTargets: chatIds.length,
      successful,
      failed,
      hasImage: Boolean(req.imageUrl),
    },
  });

  return historyItem;
}

/**
 * Xabarnomalar tarixini olish
 */
export async function getBroadcastHistory(limitCount = 30): Promise<BroadcastHistoryItem[]> {
  const db = getFirestoreDb();
  if (!db) {
    return inMemoryHistory.slice(0, limitCount);
  }

  try {
    const snap = await db
      .collection(FIRESTORE_COLLECTIONS.BROADCASTS)
      .orderBy("createdAt", "desc")
      .limit(limitCount)
      .get();

    if (snap.empty) {
      return inMemoryHistory.slice(0, limitCount);
    }

    return snap.docs.map((d) => d.data() as BroadcastHistoryItem);
  } catch (err: any) {
    console.warn("[Broadcast] Firestore tarixini o'qishda xatolik, in-memory qaytarilmoqda:", err?.message || err);
    return inMemoryHistory.slice(0, limitCount);
  }
}
