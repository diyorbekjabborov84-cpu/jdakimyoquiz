import dotenv from "dotenv";
import { z } from "zod";

// .env faylini o'qish
dotenv.config();

const envSchema = z.object({
  BOT_TOKEN: z
    .string({ required_error: "BOT_TOKEN ko'rsatilishi shart!" })
    .min(1, "BOT_TOKEN bo'sh bo'lishi mumkin emas!"),
  PORT: z
    .string()
    .default("3000")
    .transform((val) => parseInt(val, 10))
    .refine((val) => !isNaN(val) && val > 0 && val <= 65535, {
      message: "PORT 1 va 65535 orasidagi son bo'lishi kerak!",
    }),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  WEBHOOK_URL: z.string().url("WEBHOOK_URL to'g'ri URL bo'lishi kerak!").optional().or(z.literal("")),
  WEBHOOK_SECRET: z.string().optional(),
  DATABASE_URL: z.string().optional(),
  FIREBASE_SERVICE_ACCOUNT_JSON: z.string().optional(),
  FIREBASE_SERVICE_ACCOUNT_PATH: z.string().optional(),
}).superRefine((data, ctx) => {
  if (data.NODE_ENV === "production") {
    const fs = require("node:fs");
    const renderSecretExists = fs.existsSync("/etc/secrets/firebase-service-account.json");
    const customPathExists = Boolean(data.FIREBASE_SERVICE_ACCOUNT_PATH && fs.existsSync(data.FIREBASE_SERVICE_ACCOUNT_PATH));
    const envJsonExists = Boolean(data.FIREBASE_SERVICE_ACCOUNT_JSON && data.FIREBASE_SERVICE_ACCOUNT_JSON.trim());

    if (!renderSecretExists && !customPathExists && !envJsonExists) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["FIREBASE_SERVICE_ACCOUNT_JSON"],
        message:
          "Production muhitida Firebase sozlanishi shart! (/etc/secrets/firebase-service-account.json fayli yoki FIREBASE_SERVICE_ACCOUNT_JSON muhit o'zgaruvchisi talab qilinadi)",
      });
    }
  }
});

export type EnvConfig = z.infer<typeof envSchema>;

let configCache: EnvConfig | null = null;

export function resetConfigCache(): void {
  configCache = null;
}

export function loadConfig(): EnvConfig {
  if (configCache) {
    return configCache;
  }

  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error("\n❌ =================== KONFIGURATSIYA XATOLIGI ===================");
    console.error("Muhit o'zgaruvchilari (.env) to'g'ri sozlanmagan:\n");
    for (const issue of result.error.issues) {
      console.error(` • [${issue.path.join(".")}] : ${issue.message}`);
    }
    console.error("\nIltimos, .env.example faylidan nusxa olib, .env faylini to'ldiring:");
    console.error("  cp .env.example .env (yoki .env fayli yaratib BOT_TOKEN va FIREBASE_SERVICE_ACCOUNT_JSON ni kiriting)");
    console.error("=================================================================\n");
    throw new Error("Konfiguratsiya xatosi: zarur muhit o'zgaruvchilari topilmadi.");
  }

  configCache = result.data;
  return configCache;
}

// Global config instance
export const config = {
  get current(): EnvConfig {
    return loadConfig();
  },
};
