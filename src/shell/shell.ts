import { Context } from "grammy";
import { getFirestoreDb, FIRESTORE_COLLECTIONS } from "../firebase/firestore.js";
import {
  getBotSettings,
  GroupShellMode,
  isValidGroupMode,
  getAdminContactUrl,
} from "../settings/botSettings.js";

export type ShellResolution =
  | { shell: "asosiy" }
  | { shell: "kurs"; context: "group" | "private" }
  | {
      shell: "yopiq";
      reason: "group_disabled" | "not_participant" | "blocked" | "check_error";
    };

export interface KursParticipantRecord {
  userId: number;
  ism: string;
  qoshilgan: string;
  qoshgan: string;
  bloklangan: boolean;
  updatedAt?: string;
}

const GROUP_MODE_CACHE_TTL_MS = 60_000; // 60 soniya
const PARTICIPANT_CACHE_TTL_MS = 10 * 60_000; // 10 daqiqa
const CHECK_ERROR_CACHE_TTL_MS = 30_000; // 30 soniya (vaqtinchalik xatolar uchun)

const groupModeCache = new Map<number, { mode: GroupShellMode; expiresAt: number }>();
const participantCache = new Map<
  number,
  { status: "participant" | "not_participant" | "blocked" | "check_error"; expiresAt: number }
>();

// Guruh o'chirilgan (ochiq_emas) bo'lganda faqat bir marta ogohlantirish yuborish uchun
const disabledNoticeSentGroups = new Set<number>();
// Ishlamaydigan (o'lik) kurs guruhlarini logga faqat bir marta yozish uchun
const loggedDeadKursGroups = new Set<number>();

// Lokal/test muhiti uchun xotiradagi zaxira
const memoryGroupModes = new Map<number, GroupShellMode>();
const memoryParticipants = new Map<number, KursParticipantRecord>();

export function invalidateGroupModeCache(chatId?: number): void {
  if (chatId !== undefined) {
    groupModeCache.delete(chatId);
    disabledNoticeSentGroups.delete(chatId);
    loggedDeadKursGroups.delete(chatId);
  } else {
    groupModeCache.clear();
    disabledNoticeSentGroups.clear();
    loggedDeadKursGroups.clear();
  }
  // Guruh rejimi o'zgarganda kurs guruhlari ro'yxati o'zgarishi mumkin, shuning uchun ishtirokchi keshini ham tozalaymiz
  participantCache.clear();
}

export function invalidateParticipantCache(userId?: number): void {
  if (userId !== undefined) {
    participantCache.delete(userId);
  } else {
    participantCache.clear();
  }
}

export function resetShellStateForTest(): void {
  groupModeCache.clear();
  participantCache.clear();
  disabledNoticeSentGroups.clear();
  loggedDeadKursGroups.clear();
  memoryGroupModes.clear();
  memoryParticipants.clear();
}

export async function getGroupShellMode(chatId: number): Promise<GroupShellMode> {
  const now = Date.now();
  const cached = groupModeCache.get(chatId);
  if (cached && now < cached.expiresAt) {
    return cached.mode;
  }

  const db = getFirestoreDb();
  if (!db) {
    const memMode = memoryGroupModes.get(chatId);
    if (memMode) {
      groupModeCache.set(chatId, { mode: memMode, expiresAt: now + GROUP_MODE_CACHE_TTL_MS });
      return memMode;
    }
    const settings = await getBotSettings();
    const fallbackMode: GroupShellMode = settings.defaultGroupMode || "asosiy";
    groupModeCache.set(chatId, { mode: fallbackMode, expiresAt: now + GROUP_MODE_CACHE_TTL_MS });
    return fallbackMode;
  }

  const docSnap = await db.collection(FIRESTORE_COLLECTIONS.GROUPS).doc(String(chatId)).get();
  if (!docSnap.exists) {
    const settings = await getBotSettings();
    const defaultMode: GroupShellMode = settings.defaultGroupMode || "asosiy";
    groupModeCache.set(chatId, { mode: defaultMode, expiresAt: now + GROUP_MODE_CACHE_TTL_MS });
    return defaultMode;
  }

  const data = docSnap.data() || {};
  const mode: GroupShellMode = isValidGroupMode(data.mode) ? data.mode : "asosiy";
  groupModeCache.set(chatId, { mode, expiresAt: now + GROUP_MODE_CACHE_TTL_MS });
  return mode;
}

export async function setGroupShellMode(
  chatId: number,
  mode: GroupShellMode
): Promise<{ chatId: number; mode: GroupShellMode; updatedAt: string }> {
  if (!isValidGroupMode(mode)) {
    throw new Error("Noto'g'ri mode qiymati. Ruxsat etilgan: 'asosiy' | 'kurs' | 'ochiq_emas'.");
  }

  const updatedAt = new Date().toISOString();
  const db = getFirestoreDb();
  if (db) {
    await db
      .collection(FIRESTORE_COLLECTIONS.GROUPS)
      .doc(String(chatId))
      .set(
        {
          chatId,
          mode,
          updatedAt,
        },
        { merge: true }
      );
  } else {
    memoryGroupModes.set(chatId, mode);
  }

  invalidateGroupModeCache(chatId);
  groupModeCache.set(chatId, { mode, expiresAt: Date.now() + GROUP_MODE_CACHE_TTL_MS });
  return { chatId, mode, updatedAt };
}

function isActiveChatMemberStatus(member: any): boolean {
  if (!member || typeof member.status !== "string") return false;
  if (
    member.status === "creator" ||
    member.status === "administrator" ||
    member.status === "member"
  ) {
    return true;
  }
  if (member.status === "restricted" && member.is_member !== false) {
    return true;
  }
  return false;
}

function classifyDeadGroupError(err: any): "kicked" | "left" | "unknown" | null {
  const desc = String(err?.description || err?.message || "").toLowerCase();
  if (desc.includes("bot was kicked")) {
    return "kicked";
  }
  if (desc.includes("bot is not a member")) {
    return "left";
  }
  if (
    desc.includes("chat not found") ||
    desc.includes("group chat was upgraded to a supergroup")
  ) {
    return "unknown";
  }
  return null;
}

async function getKursGroupChatIds(): Promise<number[]> {
  const db = getFirestoreDb();
  if (!db) {
    const ids: number[] = [];
    for (const [chatId, mode] of memoryGroupModes.entries()) {
      if (mode === "kurs") ids.push(chatId);
    }
    return ids;
  }

  const snap = await db
    .collection(FIRESTORE_COLLECTIONS.GROUPS)
    .where("mode", "==", "kurs")
    .get();

  const ids: number[] = [];
  for (const doc of snap.docs) {
    const data = doc.data() || {};
    if (data.status === "kicked" || data.status === "left" || data.status === "unknown") {
      continue;
    }
    const id = Number(data.chatId ?? doc.id);
    if (Number.isFinite(id) && id < 0) {
      ids.push(id);
    }
  }
  return ids;
}

export async function checkPrivateKursParticipation(
  ctx: Context,
  userId: number
): Promise<"participant" | "not_participant" | "blocked" | "check_error"> {
  const now = Date.now();
  const cached = participantCache.get(userId);
  if (cached && now < cached.expiresAt) {
    return cached.status;
  }

  const db = getFirestoreDb();
  if (!db && process.env.NODE_ENV === "production") {
    participantCache.set(userId, {
      status: "check_error",
      expiresAt: now + CHECK_ERROR_CACHE_TTL_MS,
    });
    return "check_error";
  }

  // 1-qadam: kurs_ishtirokchilari/{userId} ni tekshirish (bloklangan: true ustunlik qiladi!)
  try {
    let record: KursParticipantRecord | undefined;
    if (db) {
      const docSnap = await db
        .collection(FIRESTORE_COLLECTIONS.KURS_PARTICIPANTS)
        .doc(String(userId))
        .get();
      if (docSnap.exists) {
        const d = docSnap.data() || {};
        if (!d.deleted) {
          record = {
            userId: Number(d.userId ?? userId),
            ism: typeof d.ism === "string" ? d.ism : "",
            qoshilgan: typeof d.qoshilgan === "string" ? d.qoshilgan : "",
            qoshgan: typeof d.qoshgan === "string" ? d.qoshgan : "admin",
            bloklangan: Boolean(d.bloklangan),
          };
        }
      }
    } else {
      record = memoryParticipants.get(userId);
    }

    if (record) {
      if (record.bloklangan) {
        participantCache.set(userId, {
          status: "blocked",
          expiresAt: now + PARTICIPANT_CACHE_TTL_MS,
        });
        return "blocked";
      }
      participantCache.set(userId, {
        status: "participant",
        expiresAt: now + PARTICIPANT_CACHE_TTL_MS,
      });
      return "participant";
    }
  } catch (err) {
    console.error(`[Shell] kurs_ishtirokchilari tekshirishda xatolik (userId: ${userId}):`, err);
    participantCache.set(userId, {
      status: "check_error",
      expiresAt: now + CHECK_ERROR_CACHE_TTL_MS,
    });
    return "check_error";
  }

  // 2-qadam: mode === "kurs" bo'lgan guruhlarda getChatMember orqali a'zolikni tekshirish
  let kursGroupIds: number[] = [];
  try {
    kursGroupIds = await getKursGroupChatIds();
  } catch (err) {
    console.error(`[Shell] Kurs guruhlarini olishda xatolik (userId: ${userId}):`, err);
    participantCache.set(userId, {
      status: "check_error",
      expiresAt: now + CHECK_ERROR_CACHE_TTL_MS,
    });
    return "check_error";
  }

  if (kursGroupIds.length === 0) {
    participantCache.set(userId, {
      status: "not_participant",
      expiresAt: now + PARTICIPANT_CACHE_TTL_MS,
    });
    return "not_participant";
  }

  let hadApiError = false;
  for (const groupChatId of kursGroupIds) {
    try {
      if (typeof ctx.api?.getChatMember !== "function") {
        hadApiError = true;
        continue;
      }
      const member = await ctx.api.getChatMember(groupChatId, userId);
      if (isActiveChatMemberStatus(member)) {
        participantCache.set(userId, {
          status: "participant",
          expiresAt: now + PARTICIPANT_CACHE_TTL_MS,
        });
        return "participant";
      }
    } catch (err: any) {
      // Agar foydalanuvchi guruhda umuman bo'lmagan bo'lsa (user not found / participant not found), bu oddiy a'zo emaslik
      const desc = String(err?.description || err?.message || "").toLowerCase();
      if (desc.includes("user not found") || desc.includes("participant_id_invalid")) {
        continue;
      }

      // Guruhga oid doimiy xatolar: bot guruhda yo'q, chiqarilgan yoki guruh o'chgan/ko'chgan
      const deadStatus = classifyDeadGroupError(err);
      if (deadStatus) {
        if (!loggedDeadKursGroups.has(groupChatId)) {
          loggedDeadKursGroups.add(groupChatId);
          console.warn(
            `[Shell] Kurs guruhi (${groupChatId}) faol emas (${deadStatus}): ${err?.description || err?.message || err}`
          );
        }
        if (db) {
          const nowIso = new Date().toISOString();
          await db
            .collection(FIRESTORE_COLLECTIONS.GROUPS)
            .doc(String(groupChatId))
            .set(
              {
                status: deadStatus,
                statusUpdatedAt: nowIso,
                updatedAt: nowIso,
              },
              { merge: true }
            )
            .catch((updateErr) => {
              console.warn(`[Shell] Guruh (${groupChatId}) statusini yangilashda xatolik:`, updateErr);
            });
        }
        continue;
      }

      console.error(
        `[Shell] getChatMember xatoligi (group: ${groupChatId}, user: ${userId}):`,
        err
      );
      hadApiError = true;
    }
  }

  if (hadApiError) {
    participantCache.set(userId, {
      status: "check_error",
      expiresAt: now + CHECK_ERROR_CACHE_TTL_MS,
    });
    return "check_error";
  }

  participantCache.set(userId, {
    status: "not_participant",
    expiresAt: now + PARTICIPANT_CACHE_TTL_MS,
  });
  return "not_participant";
}

/**
 * Inline query uchun (ctx.chat bo'lmaganda) foydalanuvchi kurs kartochkalarini
 * ko'ra olishini tekshirish. Fail-closed: xatolik bo'lsa false qaytaradi.
 */
export async function canUserAccessKursInInlineQuery(
  ctx: Context,
  userId?: number,
  adminTelegramId?: string
): Promise<boolean> {
  if (!userId || !Number.isInteger(userId) || userId <= 0) {
    return false;
  }

  const configuredAdminId = (adminTelegramId ?? process.env.ADMIN_TELEGRAM_ID ?? "").trim();
  if (configuredAdminId && String(userId) === configuredAdminId) {
    return true;
  }

  try {
    const status = await checkPrivateKursParticipation(ctx, userId);
    return status === "participant";
  } catch (err) {
    console.error(`[Shell] Inline query ruxsat tekshiruvida xatolik (userId: ${userId}):`, err);
    return false;
  }
}

/**
 * Har qanday buyruq yoki callback kelganda qobiqni (shell) aniqlash:
 * - Guruhda: guruhning mode qiymatiga qarab ("asosiy" | "kurs" | "ochiq_emas")
 * - Shaxsiy chatda: foydalanuvchining kurs ishtirokchisi ekanligiga qarab
 */
export async function resolveShell(ctx: Context): Promise<ShellResolution> {
  const chatType = ctx.chat?.type;
  const chatId = ctx.chat?.id;

  if (chatType === "group" || chatType === "supergroup") {
    if (!chatId) {
      return { shell: "asosiy" };
    }
    try {
      const mode = await getGroupShellMode(chatId);
      if (mode === "kurs") {
        return { shell: "kurs", context: "group" };
      }
      if (mode === "ochiq_emas") {
        return { shell: "yopiq", reason: "group_disabled" };
      }
      return { shell: "asosiy" };
    } catch (err) {
      console.error(`[Shell] Guruh rejimini aniqlashda xatolik (chatId: ${chatId}):`, err);
      return { shell: "yopiq", reason: "check_error" };
    }
  }

  if (chatType === "private") {
    const userId = ctx.from?.id;
    if (!userId) {
      return { shell: "yopiq", reason: "not_participant" };
    }
    const status = await checkPrivateKursParticipation(ctx, userId);
    if (status === "participant") {
      return { shell: "kurs", context: "private" };
    }
    return { shell: "yopiq", reason: status };
  }

  return { shell: "yopiq", reason: "not_participant" };
}

/**
 * mode === "ochiq_emas" bo'lgan guruhda spam qilmasdan bir marta ogohlantirish xabarini yuborish
 */
export async function replyGroupDisabledOnce(ctx: Context): Promise<void> {
  const chatId = ctx.chat?.id;
  const settings = await getBotSettings();
  const msg = `⚠️ Bu guruhda bot faol emas. Adminga murojaat: ${settings.adminContact}`;

  if (ctx.callbackQuery) {
    try {
      await ctx.answerCallbackQuery({ text: msg, show_alert: true });
    } catch {
      // ignore
    }
    return;
  }

  if (chatId !== undefined) {
    if (disabledNoticeSentGroups.has(chatId)) {
      return;
    }
    disabledNoticeSentGroups.add(chatId);
  }

  await ctx.reply(msg);
}

/**
 * Shaxsiy chatda kurs a'zosi bo'lmagan yoki bloklangan foydalanuvchiga javob
 */
export async function replyPrivateNotParticipant(
  ctx: Context,
  reason: "not_participant" | "blocked" | "check_error"
): Promise<void> {
  if (reason === "check_error") {
    const errText = "⚠️ Hozir tekshirib bo‘lmadi, birozdan so‘ng urinib ko‘ring.";
    if (ctx.callbackQuery) {
      try {
        await ctx.answerCallbackQuery({ text: errText, show_alert: true });
      } catch {
        // ignore
      }
      return;
    }
    await ctx.reply(errText);
    return;
  }

  const settings = await getBotSettings();
  const adminContact = settings.adminContact;
  const adminUrl = getAdminContactUrl(adminContact);

  if (ctx.callbackQuery) {
    try {
      await ctx.answerCallbackQuery({
        text: `Bu bot shaxsiy chatda faqat «Kimyo 0 dan» kursi ishtirokchilari uchun ishlaydi. Murojaat: ${adminContact}`,
        show_alert: true,
      });
    } catch {
      // ignore
    }
    return;
  }

  const firstName = ctx.from?.first_name ? `, ${ctx.from.first_name}` : "";
  const text =
    `👋 Assalomu alaykum${firstName}!\n` +
    `Bu bot shaxsiy chatda faqat «Kimyo 0 dan» kursi ishtirokchilari uchun ishlaydi.\n` +
    `Kursga qo‘shilish yoki savollar bo‘yicha adminga murojaat qiling: ${adminContact}`;

  await ctx.reply(text, {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "✉️ Adminga yozish",
            url: adminUrl,
          },
        ],
      ],
    },
  });
}

// ============================================================================
// Kurs ishtirokchilari CRUD (Admin API va testlar uchun)
// ============================================================================

export async function listKursParticipants(options?: {
  search?: string;
  page?: number;
  limit?: number;
}): Promise<{
  items: KursParticipantRecord[];
  total: number;
  page: number;
  limit: number;
}> {
  const page = Math.max(1, Number(options?.page) || 1);
  const limit = Math.min(200, Math.max(1, Number(options?.limit) || 50));
  const search = (options?.search || "").trim().toLowerCase();

  const db = getFirestoreDb();
  let all: KursParticipantRecord[] = [];

  if (db) {
    const snap = await db.collection(FIRESTORE_COLLECTIONS.KURS_PARTICIPANTS).get();
    all = snap.docs
      .filter((doc) => {
        const d = doc.data() || {};
        return !d.deleted;
      })
      .map((doc) => {
        const d = doc.data() || {};
        return {
          userId: Number(d.userId ?? doc.id),
          ism: typeof d.ism === "string" ? d.ism : "",
          qoshilgan: typeof d.qoshilgan === "string" ? d.qoshilgan : "",
          qoshgan: typeof d.qoshgan === "string" ? d.qoshgan : "admin",
          bloklangan: Boolean(d.bloklangan),
          updatedAt: typeof d.updatedAt === "string" ? d.updatedAt : undefined,
        };
      });
  } else {
    all = Array.from(memoryParticipants.values()).map((r) => ({ ...r }));
  }

  all.sort((a, b) => (b.qoshilgan || "").localeCompare(a.qoshilgan || ""));

  const filtered = search
    ? all.filter(
        (item) =>
          String(item.userId).includes(search) ||
          (item.ism || "").toLowerCase().includes(search)
      )
    : all;

  const total = filtered.length;
  const start = (page - 1) * limit;
  const items = filtered.slice(start, start + limit);

  return { items, total, page, limit };
}

export async function addKursParticipant(params: {
  userId: number;
  ism?: string;
  qoshgan?: string;
}): Promise<KursParticipantRecord> {
  const userId = Number(params.userId);
  if (!Number.isInteger(userId) || userId <= 0) {
    throw new Error("userId musbat butun son bo'lishi shart.");
  }

  const ism = typeof params.ism === "string" ? params.ism.trim().slice(0, 120) : "";
  const nowIso = new Date().toISOString();

  const record: KursParticipantRecord = {
    userId,
    ism,
    qoshilgan: nowIso,
    qoshgan: params.qoshgan || "admin",
    bloklangan: false,
    updatedAt: nowIso,
  };

  const db = getFirestoreDb();
  if (db) {
    await db
      .collection(FIRESTORE_COLLECTIONS.KURS_PARTICIPANTS)
      .doc(String(userId))
      .set(record, { merge: true });
  } else {
    memoryParticipants.set(userId, record);
  }

  invalidateParticipantCache(userId);
  return { ...record };
}

export async function updateKursParticipantBlockStatus(
  userId: number,
  bloklangan: boolean
): Promise<KursParticipantRecord> {
  const numId = Number(userId);
  if (!Number.isInteger(numId) || numId <= 0) {
    throw new Error("userId musbat butun son bo'lishi shart.");
  }

  const nowIso = new Date().toISOString();
  const db = getFirestoreDb();

  if (db) {
    const docRef = db.collection(FIRESTORE_COLLECTIONS.KURS_PARTICIPANTS).doc(String(numId));
    const snap = await docRef.get();
    const existing = snap.exists ? snap.data() || {} : {};
    const record: KursParticipantRecord = {
      userId: numId,
      ism: typeof existing.ism === "string" ? existing.ism : "",
      qoshilgan: typeof existing.qoshilgan === "string" ? existing.qoshilgan : nowIso,
      qoshgan: typeof existing.qoshgan === "string" ? existing.qoshgan : "admin",
      bloklangan: Boolean(bloklangan),
      updatedAt: nowIso,
    };
    await docRef.set(record, { merge: true });
    invalidateParticipantCache(numId);
    return record;
  }

  const existing = memoryParticipants.get(numId);
  const record: KursParticipantRecord = {
    userId: numId,
    ism: existing?.ism || "",
    qoshilgan: existing?.qoshilgan || nowIso,
    qoshgan: existing?.qoshgan || "admin",
    bloklangan: Boolean(bloklangan),
    updatedAt: nowIso,
  };
  memoryParticipants.set(numId, record);
  invalidateParticipantCache(numId);
  return { ...record };
}

export async function deleteKursParticipant(userId: number): Promise<boolean> {
  const numId = Number(userId);
  if (!Number.isInteger(numId) || numId <= 0) {
    throw new Error("userId musbat butun son bo'lishi shart.");
  }

  const db = getFirestoreDb();
  if (db) {
    const docRef = db.collection(FIRESTORE_COLLECTIONS.KURS_PARTICIPANTS).doc(String(numId));
    if (typeof (docRef as any).delete === "function") {
      await (docRef as any).delete();
    } else {
      await docRef.set({ deleted: true, bloklangan: false }, { merge: false });
    }
  } else {
    memoryParticipants.delete(numId);
  }

  invalidateParticipantCache(numId);
  return true;
}
