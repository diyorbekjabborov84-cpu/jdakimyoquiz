import { Router, Request, Response, NextFunction } from "express";
import { EnvConfig } from "../config/env.js";
import {
  verifyTelegramAuth,
  createAdminSessionToken,
  verifyAdminSessionToken,
  TelegramAuthPayload,
  AdminSession,
} from "./adminAuth.js";
import { getOverviewStats, getGroupsList, getUsersList } from "../tracking/tracker.js";
import { verifyGoogleAdmin, ADMIN_GOOGLE_EMAIL } from "./googleAuth.js";
import { executeBroadcast, getBroadcastHistory } from "./broadcastService.js";
import { getQuizResultsList, getSessionLeaderboard } from "./resultsService.js";
import { getAuditLogs, recordAuditLog } from "./auditService.js";

export function createAdminRouter(config: EnvConfig, telegramApi?: any): Router {
  const router = Router();

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
        res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
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
    if (!config.ADMIN_SESSION_SECRET || config.ADMIN_SESSION_SECRET.length < 32) {
      return res.status(503).json({ ok: false, error: "SECRET_NOT_CONFIGURED" });
    }
    const idToken = req.body?.idToken;
    if (typeof idToken !== "string" || !idToken || idToken.length > 10000) {
      return res.status(400).json({ ok: false, error: "INVALID_PAYLOAD" });
    }
    if (!(await verifyGoogleAdmin(idToken))) {
      return res.status(403).json({ ok: false, error: "UNAUTHORIZED_ADMIN", message: "Bu Google akkauntga ruxsat berilmagan yoki kirish tasdig‘i eskirgan." });
    }
    try {
      const adminId = config.ADMIN_TELEGRAM_ID?.trim() || ADMIN_GOOGLE_EMAIL;
      const token = createAdminSessionToken(adminId, ADMIN_GOOGLE_EMAIL, config.ADMIN_SESSION_SECRET);
      return res.json({ ok: true, token, user: { id: adminId, username: ADMIN_GOOGLE_EMAIL, firstName: "Diyorbek" } });
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
    const limit = typeof req.query.limit === "string" ? parseInt(req.query.limit, 10) : 50;
    const cursor = typeof req.query.cursor === "string" ? req.query.cursor : undefined;

    try {
      const result = await getGroupsList({ query: q, limit, cursor });
      return res.status(200).json({
        ok: true,
        groups: result.groups,
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
        message: "Guruhlar ma'lumotini olishda xatolik yuz berdi.",
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
    return res.status(200).json({
      ok: true,
      settings: {
        subscriptionChannels: [
          { username: "@jda_kimyo", title: "JDA Kimyo Asosiy Kanal" },
          { username: "@jdaquizkod", title: "JDA Quiz Kodlari Kanali" },
        ],
        defaultQuestionTimeSeconds: 20,
        botUsername: "jdakimyoquizbot",
        adminGoogleEmail: ADMIN_GOOGLE_EMAIL,
        adminTelegramId: config.ADMIN_TELEGRAM_ID || null,
        environment: config.NODE_ENV,
      },
    });
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
