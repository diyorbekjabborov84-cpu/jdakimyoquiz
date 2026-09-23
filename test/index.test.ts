import assert from "node:assert";
import { z } from "zod";
import { createBot } from "../src/bot/bot.js";
import { createApp } from "../src/server/app.js";
import { handleStart } from "../src/bot/handlers/start.js";
import { handleHelp } from "../src/bot/handlers/help.js";
import http from "node:http";

async function runTests() {
  console.log("🧪 1-BOSQICH TESTLARI BOSHLANDI...\n");

  // TEST 1: Konfiguratsiya tekshiruvi (BOT_TOKEN yo'qligi)
  console.log("Test 1: BOT_TOKEN bo'lmaganda Zod xatolik berishi...");
  const envSchema = z.object({
    BOT_TOKEN: z
      .string({ required_error: "BOT_TOKEN ko'rsatilishi shart!" })
      .min(1, "BOT_TOKEN bo'sh bo'lishi mumkin emas!"),
  });
  const invalidResult = envSchema.safeParse({});
  assert.strictEqual(invalidResult.success, false, "BOT_TOKEN bo'lmaganda xato bo'lishi kerak");
  assert.ok(
    invalidResult.error?.issues[0].message.includes("BOT_TOKEN ko'rsatilishi shart"),
    "Tushunarli xato xabari mavjud"
  );
  console.log("✅ Test 1 muvaffaqiyatli o'tdi.\n");

  // TEST 2: Bot instansiyasi yaratilishi va buyruqlarni ro'yxatga olishi
  console.log("Test 2: Bot instansiyasi va buyruqlarning ro'yxatdan o'tishi...");
  const dummyToken = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11";
  const bot = createBot(dummyToken);
  assert.ok(bot, "Bot instansiyasi yaratilishi kerak");
  console.log("✅ Test 2 muvaffaqiyatli o'tdi.\n");

  // TEST 3: /start va /help handlerlari (Mock Context bilan)
  console.log("Test 3: /start va /help handlerlari chaqirilganda xabarlar to'g'ri shakllanishi...");
  let startPrivateMsg = "";
  const mockPrivateCtx: any = {
    chat: { type: "private" },
    from: { first_name: "Aziz" },
    me: { username: "jdakimyoquiz_bot" },
    reply: async (text: string) => {
      startPrivateMsg = text;
    },
  };
  await handleStart(mockPrivateCtx);
  assert.ok(startPrivateMsg.includes("Assalomu alaykum, Aziz"), "Shaxsiy /start salomlashishi kerak");

  let startGroupMsg = "";
  const mockGroupCtx: any = {
    chat: { type: "group" },
    from: { first_name: "Aziz" },
    me: { username: "jdakimyoquiz_bot" },
    reply: async (text: string) => {
      startGroupMsg = text;
    },
  };
  await handleStart(mockGroupCtx);
  assert.ok(startGroupMsg.includes("JDA Kimyo Quiz Boti faol"), "Guruhdagi /start guruh xabarini berishi kerak");

  let helpMsg = "";
  const mockHelpCtx: any = {
    reply: async (text: string) => {
      helpMsg = text;
    },
  };
  await handleHelp(mockHelpCtx);
  assert.ok(helpMsg.includes("Qo'llanma"), "Help yo'riqnomasi mavjud bo'lishi kerak");
  console.log("✅ Test 3 muvaffaqiyatli o'tdi.\n");

  // TEST 4: Express server va /health endpointi
  console.log("Test 4: Express /health va / endpointlari...");
  const testConfig = {
    BOT_TOKEN: dummyToken,
    PORT: 3001,
    NODE_ENV: "test" as const,
    WEBHOOK_URL: "",
    WEBHOOK_SECRET: "",
  };
  const app = createApp(bot, testConfig);

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(3001, resolve));

  const healthRes = await fetch("http://localhost:3001/health");
  assert.strictEqual(healthRes.status, 200, "Health endpoint 200 qaytarishi kerak");
  const healthData = (await healthRes.json()) as any;
  assert.strictEqual(healthData.status, "ok", "Status 'ok' bo'lishi kerak");
  assert.strictEqual(healthData.service, "jda-kimyo-quiz");

  const rootRes = await fetch("http://localhost:3001/");
  assert.strictEqual(rootRes.status, 200, "Root endpoint 200 qaytarishi kerak");
  const rootData = (await rootRes.json()) as any;
  assert.strictEqual(rootData.status, "running", "Root status 'running' bo'lishi kerak");

  server.close();
  console.log("✅ Test 4 muvaffaqiyatli o'tdi.\n");

  console.log("🎉 BARCHA 1-BOSQICH TESTLARI MUVAFFAQIYATLI O'TDI!");
}

runTests().catch((err) => {
  console.error("❌ Testlarda xatolik:", err);
  process.exit(1);
});
