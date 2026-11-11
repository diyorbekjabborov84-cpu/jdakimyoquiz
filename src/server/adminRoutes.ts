import { Router, Request, Response, NextFunction } from "express";
import { EnvConfig } from "../config/env.js";
import {
  verifyTelegramAuth,
  createAdminSessionToken,
  verifyAdminSessionToken,
  shouldRenewAdminSession,
  MAX_ADMIN_SESSION_SECONDS,
  TelegramAuthPayload,
  AdminSession,
} from "./adminAuth.js";
import { getOverviewStats, getGroupsList, getUsersList } from "../tracking/tracker.js";
import {
  verifyGoogleAdmin,
  verifyGoogleOneTapToken,
  ADMIN_GOOGLE_EMAIL,
} from "./googleAuth.js";
import { executeBroadcast, getBroadcastHistory } from "./broadcastService.js";
import { getQuizResultsList, getSessionLeaderboard } from "./resultsService.js";
import { getAuditLogs, recordAuditLog } from "./auditService.js";
import {
  getBotSettings,
  updateBotSettings,
  isValidGroupMode,
  isValidDefaultGroupMode,
  isValidKursQuestionTimeSeconds,
  normalizeAdminContact,
} from "../settings/botSettings.js";
import {
  setGroupShellMode,
  listKursParticipants,
  addKursParticipant,
  updateKursParticipantBlockStatus,
  deleteKursParticipant,
} from "../shell/shell.js";
import {
  getKursDarslarAdminMeta,
  reloadKursDarslar,
} from "../kurs/kursRepository.js";

/**
 * Render kabi reverse proxy ortida mijozning haqiqiy IP manzilini xavfsiz olish:
 * Mijoz X-Forwarded-For boshiga soxta IP qo'shib yuborsa ham, ishonchli proxy
 * eng oxiriga haqiqiy IP ni yozadi (yoki trust proxy=1 bo'lganda req.ip shu qiymatni oladi).
 */
export function extractClientIpForRateLimit(req: Request): string {
  const xff = req.headers["x-forwarded-for"];
  if (typeof xff === "string" && xff.trim()) {
    const parts = xff
      .split(",")
      .map((p) => p.trim())
      .filter(Boolean);
    if (parts.length > 0) {
      return parts[parts.length - 1];
    }
  } else if (Array.isArray(xff) && xff.length > 0) {
    const lastHeader = xff[xff.length - 1];
    const parts = String(lastHeader)
      .split(",")
      .map((p) => p.trim())
      .filter(Boolean);
    if (parts.length > 0) {
      return parts[parts.length - 1];
    }
  }

  return String(req.ip || req.socket?.remoteAddress || "local").trim();
}

export function createAdminRouter(
  config: EnvConfig,
  telegramApi?: any,
  oneTapVerifyOptions?: Parameters<typeof verifyGoogleOneTapToken>[2]
): Router {
  const router = Router();
  const loginAttempts = new Map<string, { count: number; resetAt: number }>();

  const checkLoginRateLimit = (req: Request, res: Response): boolean => {
    const ip = extractClientIpForRateLimit(req);
    const now = Date.now();
    const entry = loginAttempts.get(ip);
    if (!entry || now >= entry.resetAt) {
      loginAttempts.set(ip, { count: 1, resetAt: now + 60_000 });
      return true;
    }
    entry.count += 1;
    if (entry.count > 25) {
      res.status(429).json({
        ok: false,
        error: "TOO_MANY_ATTEMPTS",
        message: "Juda ko'p kirish urinishlari. Birozdan so'ng qayta urinib ko'ring.",
      });
      return false;
    }
    return true;
  };

  // Qat'iy CORS middleware
  router.use((req: Request, res: Response, next: NextFunction) => {
    const origin = req.headers.origin;
    const allowedOrigin = config.ADMIN_CORS_ORIGIN?.trim();

    if (origin) {
      let isAllowed = false;

      if (config.NODE_ENV === "production") {
        // Productionda: Faqat va faqat aniq konfiguratsiya qilingan origin!
        // Wildcard '*', substring yoki blanket *.vercel.app domenlari mutlaqo taqiqlanadi!
        if (allowedOrigin && allowedOrigin !== "*" && origin === allowedOrigin) {
          isAllowed = true;
        }
      } else {
        // Development yoki test muhitida:
        if (allowedOrigin && (allowedOrigin === "*" || origin === allowedOrigin)) {
          isAllowed = true;
        } else if (
          origin === "http://localhost:3000" ||
          origin === "http://localhost:3001" ||
          origin === "http://127.0.0.1:3000" ||
          origin === "http://127.0.0.1:3001"
        ) {
          isAllowed = true;
        }
      }

      if (isAllowed) {
        res.setHeader("Access-Control-Allow-Origin", origin);
        res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS");
        res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With");
      }
    }

    if (req.method === "OPTIONS") {
      return res.status(204).end();
    }
    next();
  });

  // 1. Telegram Login Widget orqali autentifikatsiya
  router.post("/auth/telegram", async (req: Request, res: Response) => {
    const body: TelegramAuthPayload = req.body;

    if (!body || !body.id || !body.hash || !body.auth_date) {
      return res.status(400).json({
        ok: false,
        error: "MISSING_FIELDS",
        message: "Telegram login ma'lumotlari to'liq emas.",
      });
    }

    const verification = verifyTelegramAuth(body, config.BOT_TOKEN, config.ADMIN_TELEGRAM_ID);

    if (!verification.success) {
      const status =
        verification.error === "ADMIN_NOT_CONFIGURED" ||
        verification.error === "BOT_TOKEN_NOT_CONFIGURED"
          ? 503
          : 403;
      return res.status(status).json({
        ok: false,
        error: verification.error,
        message:
          verification.error === "ADMIN_NOT_CONFIGURED"
            ? "Serverda admin hisobi (ADMIN_TELEGRAM_ID) hali sozlanmagan."
            : verification.error === "UNAUTHORIZED_ADMIN"
            ? "Ushbu Telegram akkaunt admin paneliga kirish huquqiga ega emas."
            : "Telegram ma'lumotlari tekshiruvdan o'tmadi yoki eskirgan.",
      });
    }

    // Muvaffaqiyatli: xavfsiz sessiya tokeni yaratiladi
    try {
      const token = createAdminSessionToken(
        verification.user.id,
        verification.user.username || undefined,
        config.ADMIN_SESSION_SECRET
      );

      return res.status(200).json({
        ok: true,
        token,
        user: verification.user,
      });
    } catch (err: any) {
      return res.status(503).json({
        ok: false,
        error: "SECRET_NOT_CONFIGURED",
        message: "Serverda admin sessiyasi siri (ADMIN_SESSION_SECRET) to'g'ri sozlanmagan.",
      });
    }
  });

  router.post("/auth/google", async (req: Request, res: Response) => {
    res.setHeader("Cache-Control", "no-store");
    if (!checkLoginRateLimit(req, res)) return;
    if (!config.ADMIN_SESSION_SECRET || config.ADMIN_SESSION_SECRET.length < 32) {
      return res.status(503).json({ ok: false, error: "SECRET_NOT_CONFIGURED" });
    }
    const idToken = req.body?.idToken;
    if (typeof idToken !== "string" || !idToken || idToken.length > 10000) {
      return res.status(400).json({ ok: false, error: "INVALID_PAYLOAD" });
    }
    if (!(await verifyGoogleAdmin(idToken))) {
      return res.status(403).json({
        ok: false,
        error: "UNAUTHORIZED_ADMIN",
        message: "Bu hisobga ruxsat yo'q",
      });
    }
    try {
      const adminId = config.ADMIN_TELEGRAM_ID?.trim() || ADMIN_GOOGLE_EMAIL;
      const token = createAdminSessionToken(
        adminId,
        ADMIN_GOOGLE_EMAIL,
        config.ADMIN_SESSION_SECRET,
        MAX_ADMIN_SESSION_SECONDS
      );
      return res.json({
        ok: true,
        token,
        user: { id: adminId, username: ADMIN_GOOGLE_EMAIL, firstName: "Diyorbek" },
      });
    } catch {
      return res.status(503).json({ ok: false, error: "SECRET_NOT_CONFIGURED" });
    }
  });

  // 1.2. Google Identity Services (One Tap / FedCM) ID tokeni orqali avtomatik kirish (4.1)
  router.post("/auth/google-onetap", async (req: Request, res: Response) => {
    res.setHeader("Cache-Control", "no-store");
    if (!checkLoginRateLimit(req, res)) return;
    if (!config.ADMIN_SESSION_SECRET || config.ADMIN_SESSION_SECRET.length < 32) {
      return res.status(503).json({ ok: false, error: "SECRET_NOT_CONFIGURED" });
    }

    const credential = req.body?.credential || req.body?.idToken;
    if (typeof credential !== "string" || !credential || credential.length > 10000) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_PAYLOAD",
        message: "Google ID token yuborilmadi.",
      });
    }

    const clientId = config.GOOGLE_OAUTH_CLIENT_ID || process.env.GOOGLE_OAUTH_CLIENT_ID;
    const verifyRes = await verifyGoogleOneTapToken(credential, clientId, oneTapVerifyOptions);

    if (!verifyRes.valid) {
      const status =
        verifyRes.error === "CLIENT_ID_NOT_CONFIGURED"
          ? 503
          : verifyRes.error === "UNAUTHORIZED_EMAIL"
          ? 403
          : 401;
      return res.status(status).json({
        ok: false,
        error: verifyRes.error === "UNAUTHORIZED_EMAIL" ? "UNAUTHORIZED_ADMIN" : verifyRes.error,
        message:
          verifyRes.error === "UNAUTHORIZED_EMAIL"
            ? "Bu hisobga ruxsat yo'q"
            : verifyRes.message || "Google One Tap tekshiruvidan o'tmadi.",
      });
    }

    try {
      const adminId = config.ADMIN_TELEGRAM_ID?.trim() || ADMIN_GOOGLE_EMAIL;
      const token = createAdminSessionToken(
        adminId,
        ADMIN_GOOGLE_EMAIL,
        config.ADMIN_SESSION_SECRET,
        MAX_ADMIN_SESSION_SECONDS
      );
      return res.status(200).json({
        ok: true,
        token,
        user: { id: adminId, username: ADMIN_GOOGLE_EMAIL, firstName: "Diyorbek" },
      });
    } catch {
      return res.status(503).json({ ok: false, error: "SECRET_NOT_CONFIGURED" });
    }
  });

  // Autentifikatsiyani tekshiruvchi middleware
  const requireAdminAuth = (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({
        ok: false,
        error: "AUTH_REQUIRED",
        message: "Avtorizatsiya talab qilinadi.",
      });
    }

    const token = authHeader.substring(7).trim();
    const result = verifyAdminSessionToken(
      token,
      config.ADMIN_TELEGRAM_ID,
      config.ADMIN_SESSION_SECRET
    );

    if (!result.valid || !result.session) {
      const status = result.error === "ADMIN_NOT_CONFIGURED" || result.error === "SECRET_NOT_CONFIGURED" ? 503 : 401;
      return res.status(status).json({
        ok: false,
        error: result.error || "INVALID_SESSION",
        message: "Sessiya yaroqsiz yoki muddati o'tgan.",
      });
    }

    (req as any).adminSession = result.session as AdminSession;
    next();
  };

  // 1.3. Sessiyani tekshirish va sirpanuvchi (sliding) yangilash (30 kun, < 7 kun qolganda yangilanadi)
  router.get("/admin/me", requireAdminAuth, (req: Request, res: Response) => {
    res.setHeader("Cache-Control", "no-store");
    const session = (req as any).adminSession as AdminSession;
    let renewedToken: string | undefined;

    if (shouldRenewAdminSession(session)) {
      try {
        renewedToken = createAdminSessionToken(
          session.adminId,
          session.username,
          config.ADMIN_SESSION_SECRET,
          MAX_ADMIN_SESSION_SECONDS
        );
      } catch {
        // ignore renewal failure
      }
    }

    return res.status(200).json({
      ok: true,
      user: {
        id: session.adminId,
        username: session.username,
      },
      exp: session.exp,
      ...(renewedToken ? { renewedToken } : {}),
    });
  });

  // 2. Bosh sahifa (Overview / KPI)
  router.get("/admin/overview", requireAdminAuth, async (_req: Request, res: Response) => {
    try {
      const stats = await getOverviewStats();
      return res.status(200).json({
        ok: true,
        stats,
        health: {
          service: "jda-kimyo-quiz",
          status: "ok",
          uptime: Math.floor(process.uptime()),
          timestamp: new Date().toISOString(),
        },
      });
    } catch (err: any) {
      return res.status(503).json({
        ok: false,
        error: "DATABASE_UNAVAILABLE",
        message: "Ma'lumotlar bazasi bilan bog'lanishda xatolik yuz berdi.",
      });
    }
  });

  // 3. Guruhlar ro'yxati
  router.get("/admin/groups", requireAdminAuth, async (req: Request, res: Response) => {
    const q = typeof req.query.q === "string" ? req.query.q : undefined;
    const mode = typeof req.query.mode === "string" && isValidGroupMode(req.query.mode)
      ? req.query.mode
      : undefined;
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;
    const cursor = typeof req.query.cursor === "string" ? req.query.cursor : undefined;

    try {
      const result = await getGroupsList({ query: q, mode, limit, cursor });
      return res.status(200).json({
        ok: true,
        groups: result.groups,
        nextCursor: result.nextCursor,
        hasMore: result.hasMore,
        total: result.total,
        modeCounts: result.modeCounts,
      });
    } catch (err: any) {
      if (err.name === "InvalidCursorError" || err.message?.includes("INVALID_CURSOR")) {
        return res.status(400).json({
          ok: false,
          error: "INVALID_CURSOR",
          message: "Cursor parametri yaroqsiz yoki noto'g'ri formatda.",
        });
      }
      return res.status(503).json({
        ok: false,
        error: "DATABASE_UNAVAILABLE",
        message: "Guruhlar ma'lumotini olishda xatolik yuz berdi.",
      });
    }
  });

  // 3.1. Guruh qobig'i rejimini o'zgartirish (asosiy | kurs | ochiq_emas)
  router.patch("/admin/groups/:chatId/mode", requireAdminAuth, async (req: Request, res: Response) => {
    const rawChatId = String(req.params.chatId || "").trim();
    const chatId = Number(rawChatId);
    if (!rawChatId || !Number.isInteger(chatId)) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_CHAT_ID",
        message: "Guruh chatId butun son bo'lishi kerak.",
      });
    }

    const mode = req.body?.mode;
    if (!isValidGroupMode(mode)) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_GROUP_MODE",
        message: "mode faqat 'asosiy', 'kurs' yoki 'ochiq_emas' bo'lishi mumkin.",
      });
    }

    try {
      const updated = await setGroupShellMode(chatId, mode);
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      await recordAuditLog({
        admin: adminName,
        action: "GROUP_MODE_CHANGE",
        details: { chatId, mode },
      });
      return res.status(200).json({ ok: true, ...updated });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "GROUP_MODE_UPDATE_FAILED",
        message: err?.message || "Guruh rejimini yangilashda xatolik yuz berdi.",
      });
    }
  });

  // 4. Foydalanuvchilar ro'yxati
  router.get("/admin/users", requireAdminAuth, async (req: Request, res: Response) => {
    const q = typeof req.query.q === "string" ? req.query.q : undefined;
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;
    const cursor = typeof req.query.cursor === "string" ? req.query.cursor : undefined;

    try {
      const result = await getUsersList({ query: q, limit, cursor });
      return res.status(200).json({
        ok: true,
        users: result.users,
        nextCursor: result.nextCursor,
        hasMore: result.hasMore,
        total: result.total,
      });
    } catch (err: any) {
      if (err.name === "InvalidCursorError" || err.message?.includes("INVALID_CURSOR")) {
        return res.status(400).json({
          ok: false,
          error: "INVALID_CURSOR",
          message: "Cursor parametri yaroqsiz yoki noto'g'ri formatda.",
        });
      }
      return res.status(503).json({
        ok: false,
        error: "DATABASE_UNAVAILABLE",
        message: "Foydalanuvchilar ma'lumotini olishda xatolik yuz berdi.",
      });
    }
  });

  // 5. Umumiy xabarnoma (Broadcast) yuborish
  router.post("/admin/broadcast", requireAdminAuth, async (req: Request, res: Response) => {
    const body = req.body;
    if (!body || !body.message || typeof body.message !== "string" || !body.message.trim()) {
      return res.status(400).json({
        ok: false,
        error: "MESSAGE_REQUIRED",
        message: "Xabar matni kiritilishi shart.",
      });
    }

    if (!["all_groups", "private_users", "selected_groups"].includes(body.target)) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_TARGET",
        message: "Auditoriya turi noto'g'ri tanlangan.",
      });
    }

    try {
      const adminSession = (req as any).adminSession;
      const adminUser = adminSession?.username || adminSession?.adminId || "admin";

      const result = await executeBroadcast(
        {
          target: body.target,
          selectedChatIds: body.selectedChatIds,
          message: body.message.trim(),
          imageUrl: body.imageUrl,
          buttons: body.buttons,
          adminUser,
        },
        telegramApi
      );

      return res.status(200).json({ ok: true, result });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "BROADCAST_FAILED",
        message: err?.message || "Xabar yuborishda kutilmagan xatolik yuz berdi.",
      });
    }
  });

  // 6. Xabarnomalar tarixi
  router.get("/admin/broadcast/history", requireAdminAuth, async (_req: Request, res: Response) => {
    try {
      const history = await getBroadcastHistory(30);
      return res.status(200).json({ ok: true, history });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "HISTORY_FETCH_FAILED",
        message: "Xabarnomalar tarixini olishda xatolik yuz berdi.",
      });
    }
  });

  // 7. O'tkazilgan quizlar natijalari ro'yxati
  router.get("/admin/results", requireAdminAuth, async (req: Request, res: Response) => {
    const quizId = typeof req.query.quizId === "string" ? req.query.quizId : undefined;
    const chatId = typeof req.query.chatId === "string" ? parseInt(req.query.chatId, 10) : undefined;
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;

    try {
      const data = await getQuizResultsList({ quizId, chatId, limit });
      return res.status(200).json({ ok: true, ...data });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "RESULTS_FETCH_FAILED",
        message: "Quiz natijalarini olishda xatolik yuz berdi.",
      });
    }
  });

  // 8. Muayyan sessiya reyting jadvali (Leaderboard)
  router.get("/admin/results/:sessionId", requireAdminAuth, async (req: Request, res: Response) => {
    const sessionId = typeof req.params.sessionId === "string" ? req.params.sessionId : String(req.params.sessionId || "");
    if (!sessionId) {
      return res.status(400).json({
        ok: false,
        error: "SESSION_ID_REQUIRED",
        message: "Sessiya ID ko'rsatilishi shart.",
      });
    }

    try {
      const data = await getSessionLeaderboard(sessionId);
      return res.status(200).json({ ok: true, ...data });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "SESSION_LEADERBOARD_FAILED",
        message: "Sessiya reytingini olishda xatolik yuz berdi.",
      });
    }
  });

  // 9. Sozlamalar
  router.get("/admin/settings", requireAdminAuth, async (_req: Request, res: Response) => {
    try {
      const botSettings = await getBotSettings();
      return res.status(200).json({
        ok: true,
        settings: {
          adminContact: botSettings.adminContact,
          defaultGroupMode: botSettings.defaultGroupMode,
          kursQuestionTimeSeconds: botSettings.kursQuestionTimeSeconds,
          updatedAt: botSettings.updatedAt || null,
          defaultQuestionTimeSeconds: 20,
          botUsername: "jdakimyoquizbot",
          adminGoogleEmail: ADMIN_GOOGLE_EMAIL,
          adminTelegramId: config.ADMIN_TELEGRAM_ID || null,
          environment: config.NODE_ENV,
        },
      });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "SETTINGS_FETCH_FAILED",
        message: "Sozlamalarni olishda xatolik yuz berdi.",
      });
    }
  });

  router.patch("/admin/settings", requireAdminAuth, async (req: Request, res: Response) => {
    const body = req.body || {};
    const patch: {
      adminContact?: string;
      defaultGroupMode?: "asosiy" | "ochiq_emas";
      kursQuestionTimeSeconds?: number;
    } = {};

    if (body.adminContact !== undefined) {
      const normalized = normalizeAdminContact(body.adminContact);
      if (!normalized) {
        return res.status(400).json({
          ok: false,
          error: "INVALID_ADMIN_CONTACT",
          message: "adminContact to'g'ri Telegram username bo'lishi kerak (masalan: @diyorbek_jabborov).",
        });
      }
      patch.adminContact = normalized;
    }

    if (body.defaultGroupMode !== undefined) {
      if (!isValidDefaultGroupMode(body.defaultGroupMode)) {
        return res.status(400).json({
          ok: false,
          error: "INVALID_DEFAULT_GROUP_MODE",
          message: "defaultGroupMode faqat 'asosiy' yoki 'ochiq_emas' bo'lishi mumkin.",
        });
      }
      patch.defaultGroupMode = body.defaultGroupMode;
    }

    if (body.kursQuestionTimeSeconds !== undefined) {
      const parsedTime =
        typeof body.kursQuestionTimeSeconds === "number"
          ? body.kursQuestionTimeSeconds
          : typeof body.kursQuestionTimeSeconds === "string" &&
            body.kursQuestionTimeSeconds.trim() !== ""
          ? Number(body.kursQuestionTimeSeconds)
          : NaN;
      if (!isValidKursQuestionTimeSeconds(parsedTime)) {
        return res.status(400).json({
          ok: false,
          error: "INVALID_KURS_QUESTION_TIME",
          message: "kursQuestionTimeSeconds 20 dan 25 gacha butun son bo'lishi kerak.",
        });
      }
      patch.kursQuestionTimeSeconds = parsedTime;
    }

    try {
      const updated = await updateBotSettings(patch);
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      await recordAuditLog({
        admin: adminName,
        action: "BOT_SETTINGS_UPDATE",
        details: patch,
      });

      return res.status(200).json({
        ok: true,
        settings: {
          ...updated,
          defaultQuestionTimeSeconds: 20,
          botUsername: "jdakimyoquizbot",
          adminGoogleEmail: ADMIN_GOOGLE_EMAIL,
          adminTelegramId: config.ADMIN_TELEGRAM_ID || null,
          environment: config.NODE_ENV,
        },
      });
    } catch (err: any) {
      return res.status(400).json({
        ok: false,
        error: "SETTINGS_UPDATE_FAILED",
        message: err?.message || "Sozlamalarni yangilashda xatolik yuz berdi.",
      });
    }
  });

  // 9.1. Kurs ishtirokchilari CRUD
  router.get("/admin/kurs/ishtirokchilar", requireAdminAuth, async (req: Request, res: Response) => {
    const search = typeof req.query.q === "string"
      ? req.query.q
      : typeof req.query.search === "string"
      ? req.query.search
      : undefined;
    const page = typeof req.query.page === "string" ? parseInt(req.query.page, 10) : 1;
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;

    try {
      const data = await listKursParticipants({ search, page, limit });
      return res.status(200).json({ ok: true, ...data });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "KURS_PARTICIPANTS_FETCH_FAILED",
        message: "Kurs ishtirokchilarini olishda xatolik yuz berdi.",
      });
    }
  });

  router.post("/admin/kurs/ishtirokchilar", requireAdminAuth, async (req: Request, res: Response) => {
    const rawUserId = req.body?.userId;
    const userId = Number(rawUserId);
    if (!Number.isInteger(userId) || userId <= 0) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_USER_ID",
        message: "userId musbat butun son bo'lishi kerak.",
      });
    }

    const ism = typeof req.body?.ism === "string" ? req.body.ism.trim() : "";

    try {
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      const participant = await addKursParticipant({
        userId,
        ism,
        qoshgan: "admin",
      });
      await recordAuditLog({
        admin: adminName,
        action: "KURS_PARTICIPANT_ADD",
        details: { userId, ism },
      });
      return res.status(200).json({ ok: true, participant });
    } catch (err: any) {
      return res.status(400).json({
        ok: false,
        error: "KURS_PARTICIPANT_ADD_FAILED",
        message: err?.message || "Ishtirokchini qo'shishda xatolik yuz berdi.",
      });
    }
  });

  router.patch("/admin/kurs/ishtirokchilar/:userId", requireAdminAuth, async (req: Request, res: Response) => {
    const userId = Number(req.params.userId);
    if (!Number.isInteger(userId) || userId <= 0) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_USER_ID",
        message: "userId musbat butun son bo'lishi kerak.",
      });
    }

    if (typeof req.body?.bloklangan !== "boolean") {
      return res.status(400).json({
        ok: false,
        error: "INVALID_BLOKLANGAN",
        message: "bloklangan boolean (true yoki false) bo'lishi shart.",
      });
    }

    try {
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      const participant = await updateKursParticipantBlockStatus(userId, req.body.bloklangan);
      await recordAuditLog({
        admin: adminName,
        action: "KURS_PARTICIPANT_BLOCK_TOGGLE",
        details: { userId, bloklangan: req.body.bloklangan },
      });
      return res.status(200).json({ ok: true, participant });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "KURS_PARTICIPANT_UPDATE_FAILED",
        message: err?.message || "Ishtirokchi holatini yangilashda xatolik yuz berdi.",
      });
    }
  });

  router.delete("/admin/kurs/ishtirokchilar/:userId", requireAdminAuth, async (req: Request, res: Response) => {
    const userId = Number(req.params.userId);
    if (!Number.isInteger(userId) || userId <= 0) {
      return res.status(400).json({
        ok: false,
        error: "INVALID_USER_ID",
        message: "userId musbat butun son bo'lishi kerak.",
      });
    }

    try {
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      await deleteKursParticipant(userId);
      await recordAuditLog({
        admin: adminName,
        action: "KURS_PARTICIPANT_DELETE",
        details: { userId },
      });
      return res.status(200).json({ ok: true, userId });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "KURS_PARTICIPANT_DELETE_FAILED",
        message: err?.message || "Ishtirokchini o'chirishda xatolik yuz berdi.",
      });
    }
  });

  // 9.2. Kurs darslar ro'yxati (javob kalitlari aslo qaytarilmaydi!) va qayta yuklash
  router.get("/admin/kurs/darslar", requireAdminAuth, async (_req: Request, res: Response) => {
    try {
      const meta = await getKursDarslarAdminMeta();
      return res.status(200).json({ ok: true, ...meta });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "KURS_LESSONS_FETCH_FAILED",
        message: "Kurs darslarini olishda xatolik yuz berdi.",
      });
    }
  });

  router.post("/admin/kurs/qayta-yuklash", requireAdminAuth, async (req: Request, res: Response) => {
    try {
      const adminSession = (req as any).adminSession;
      const adminName = adminSession?.username || adminSession?.adminId || "admin";
      const result = await reloadKursDarslar();
      await recordAuditLog({
        admin: adminName,
        action: "KURS_LESSONS_RELOAD",
        details: result,
      });
      return res.status(200).json({ ok: true, ...result });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "KURS_RELOAD_FAILED",
        message: err?.message || "Kurs darslarini qayta yuklashda xatolik yuz berdi.",
      });
    }
  });

  // 10. Audit loglari
  router.get("/admin/audit-logs", requireAdminAuth, async (req: Request, res: Response) => {
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;
    try {
      const logs = await getAuditLogs(limit);
      return res.status(200).json({ ok: true, logs });
    } catch (err: any) {
      return res.status(500).json({
        ok: false,
        error: "LOGS_FETCH_FAILED",
        message: "Audit loglarini olishda xatolik yuz berdi.",
      });
    }
  });

  return router;
}
