import { loadConfig } from "./config/env.js";
import { createBot } from "./bot/bot.js";
import { createApp } from "./server/app.js";

async function bootstrap() {
  console.log("🚀 JDA Kimyo Quiz boti ishga tushirilmoqda...");

  // 1. Konfiguratsiyani o'qish va tekshirish
  const config = loadConfig();
  console.log(`[Config] Muhit: ${config.NODE_ENV}, Port: ${config.PORT}`);

  // 2. Telegram Botni yaratish
  const bot = createBot(config.BOT_TOKEN);

  // 3. HTTP Serverni yaratish va ishga tushirish
  const app = createApp(bot, config);
  const server = app.listen(config.PORT, () => {
    console.log(`✅ [HTTP Server] http://localhost:${config.PORT} da tinglamoqda`);
    console.log(`🩺 [Health Check] http://localhost:${config.PORT}/health`);
  });

  // 4. Bot update'larini qabul qilish (poll_answer yangilanishlarini olish uchun allowed_updates shart)
  const allowedUpdates = [
    "message",
    "poll",
    "poll_answer",
    "chat_member",
  ] as const;

  if (config.NODE_ENV === "production" && config.WEBHOOK_URL) {
    console.log(`🌐 [Bot] Production Webhook rejimida ishlamoqda: ${config.WEBHOOK_URL}/webhook`);
    // Webhook URL'ni Telegram API'ga o'rnatish
    await bot.api.setWebhook(`${config.WEBHOOK_URL}/webhook`, {
      secret_token: config.WEBHOOK_SECRET,
      allowed_updates: [...allowedUpdates],
      drop_pending_updates: true,
    });
    console.log("✅ [Bot] Telegram Webhook muvaffaqiyatli o'rnatildi.");
  } else {
    // Lokal pollingda eski webhook mavjud bo'lsa, uni tozalash
    try {
      await bot.api.deleteWebhook({ drop_pending_updates: false });
    } catch (e) {
      // e'tiborsiz qoldiramiz
    }
    console.log("📡 [Bot] Lokal Long-Polling rejimida ishga tushirilmoqda...");
    bot.start({
      allowed_updates: [...allowedUpdates],
      onStart: (botInfo) => {
        console.log(`✅ [Bot] @${botInfo.username} sifatida muvaffaqiyatli ishga tushdi!`);
      },
    });
  }

  // Graceful shutdown
  const handleShutdown = async (signal: string) => {
    console.log(`\n🛑 [Shutdown] ${signal} qabul qilindi. Server va bot to'xtatilmoqda...`);
    server.close(() => {
      console.log("🔒 [HTTP Server] To'xtatildi.");
    });
    if (bot.isInited()) {
      await bot.stop();
      console.log("🔒 [Bot] To'xtatildi.");
    }
    process.exit(0);
  };

  process.on("SIGINT", () => handleShutdown("SIGINT"));
  process.on("SIGTERM", () => handleShutdown("SIGTERM"));
}

bootstrap().catch((err) => {
  console.error("💥 Kutilmagan kritik xatolik:", err);
  process.exit(1);
});
