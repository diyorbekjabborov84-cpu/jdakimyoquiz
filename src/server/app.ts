import express, { Express, Request, Response } from "express";
import { Bot, webhookCallback } from "grammy";
import { EnvConfig } from "../config/env.js";
import { checkFirestoreHealth } from "../firebase/firestore.js";
import { checkDatabaseHealth } from "../database/db.js";
import { createAdminRouter } from "./adminRoutes.js";

export function createApp(
  bot: Bot,
  config: EnvConfig,
  customDbHealthCheck?: () => Promise<boolean>
): Express {
  const app = express();

  app.use(express.json());

  // Render yoki tashqi monitoring tizimlari uchun Health Check endpointi
  app.get("/health", async (_req: Request, res: Response) => {
    let dbStatus = "not_configured";

    if (
      config.NODE_ENV === "production" ||
      config.FIREBASE_SERVICE_ACCOUNT_JSON ||
      config.FIREBASE_SERVICE_ACCOUNT_PATH ||
      config.DATABASE_URL
    ) {
      let isDbOk = false;
      if (customDbHealthCheck) {
        isDbOk = await customDbHealthCheck();
      } else {
        const isFirestoreOk = await checkFirestoreHealth();
        if (isFirestoreOk) {
          isDbOk = true;
        } else if (config.DATABASE_URL) {
          isDbOk = await checkDatabaseHealth();
        }
      }

      dbStatus = isDbOk ? "connected" : "disconnected";

      if (!isDbOk && config.NODE_ENV === "production") {
        return res.status(503).json({
          status: "error",
          service: "jda-kimyo-quiz",
          database: "disconnected",
          uptime: Math.floor(process.uptime()),
          timestamp: new Date().toISOString(),
        });
      }
    }

    return res.status(200).json({
      status: "ok",
      service: "jda-kimyo-quiz",
      database: dbStatus,
      uptime: Math.floor(process.uptime()),
      timestamp: new Date().toISOString(),
    });
  });

  // Bosh sahifa
  app.get("/", (_req: Request, res: Response) => {
    res.status(200).json({
      service: "jda-kimyo-quiz",
      status: "running",
      mode: config.NODE_ENV,
      message: "JDA Kimyo Quiz Telegram Boti serveri muvaffaqiyatli ishlamoqda.",
    });
  });

  // Admin panel API routeri
  app.use("/api", createAdminRouter(config));

  // Agar webhook rejimi yoqilgan bo'lsa (Render / production)
  if (config.NODE_ENV === "production" && config.WEBHOOK_URL) {
    const webhookPath = "/webhook";
    console.log(`[Server] Webhook yo'li sozlandi: ${webhookPath}`);
    app.use(
      webhookPath,
      webhookCallback(bot, "express", {
        secretToken: config.WEBHOOK_SECRET,
      })
    );
  }

  return app;
}
