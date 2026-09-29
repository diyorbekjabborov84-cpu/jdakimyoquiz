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

export function createAdminRouter(config: EnvConfig): Router {
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

  return router;
}
