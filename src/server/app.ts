import express, { Express, Request, Response } from "express";
import { Bot, webhookCallback } from "grammy";
import { EnvConfig } from "../config/env.js";

export function createApp(bot: Bot, config: EnvConfig): Express {
  const app = express();

  app.use(express.json());

  // Render yoki tashqi monitoring tizimlari uchun Health Check endpointi
  app.get("/health", (_req: Request, res: Response) => {
    res.status(200).json({
      status: "ok",
      service: "jda-kimyo-quiz",
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
