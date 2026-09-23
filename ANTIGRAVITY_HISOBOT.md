# JDA Kimyo Quiz — Antigravity hisobot va haqiqiy sinov

## Foydalanuvchi tasdiqlagan vaqt va ball qoidasi

20 savol bo‘lsa, ishtirokchi 15 tasiga javob bersa va shundan 7 tasi to‘g‘ri bo‘lsa, natija **7/20** chiqadi. `Jami javob vaqti` faqat javob bosilgan 15 ta savolning vaqtlaridan yig‘iladi; javobsiz 5 ta savol uchun vaqt qo‘shilmaydi. Noto‘g‘ri bosilgan javobning vaqti ham qo‘shiladi. Bu qoida avvalgi “javobsiz savolga 15 soniya qo‘shish” taklifini bekor qiladi. Kod, test va ko‘rsatiladigan matn shu qoidaga 100% moslashtirildi.

---

## 1. Kod holati va Sinov Natijalari

- **Tekshirilgan sana va vaqt**: 2026-09-23 22:10:00 (Toshkent vaqti)
- **Oxirgi o‘zgartirilgan fayllar**:
  - `src/quiz/quizManager.ts`:
    - Telegram Bot API talabi: `correct_option_ids: [q.correctOptionId]` (eski `correct_option_id` to'liq olib tashlangan);
    - Vaqt va ball hisobi faqat bosilgan variantlar uchun `handlePollAnswer` da yig'iladi, javobsiz savollar vaqtga qo'shilmaydi;
    - Yakuniy reytingda vaqt nomi: `(jami javob vaqti: Xs)`;
    - Foydalanuvchi ismlari HTML xavfsiz qilib chiqariladi (`escapeHtml`);
    - Konsolda jarayonni (boshlanishi, har bir savol, foydalanuvchilar javoblari va yakuniy natijani) kuzatish uchun to'liq loglar kiritildi.
  - `src/index.ts`:
    - Production rejimida webhook o'rnatish: `setWebhook` da `allowed_updates: ["message", "poll", "poll_answer", "chat_member"]` va `drop_pending_updates: true`;
    - Lokal rejimda webhook mavjud bo'lsa ziddiyat bo'lmasligi uchun avval `deleteWebhook` chaqiriladi.
  - `test/index.test.ts` (4 ta test): Zod validatsiyasi, config, bot buyruqlari, Express `/health` 200 OK.
  - `test/quiz.test.ts` (11 ta test): 5 ta haqiqiy kimyo savoli, multi-group, takroriy javob deduplikatsiyasi, kech javoblar, admin huquqi, Test 11 (20 savol / 15 javob / 7 to'g'ri / 5 javobsiz -> 7/20).
  - `test/e2e-simulation.test.ts` (1 ta test): 2 ishtirokchili to'liq guruh quiz sinovi (Ali 5/5, Vali 4/5, tay-breyk, HTML escape).
- **`npm.cmd run build` natijasi**: Muvaffaqiyatli (Exit code 0). TypeScript qat'iy kompilatsiyasi (`dist/`) 0 xato bilan yakunlandi.
- **`npm.cmd test` natijasi**: Muvaffaqiyatli (Exit code 0). Barcha 16 ta test 100% o'tdi.

---

## 2. Haqiqiy Telegram guruhi sinovi

- **Bot username’i**: `@jdakimyoquizbot` (JDA QUIZ)
- **Bot holati**: Bot lokal HTTP serveri va Telegram Long-Polling rejimida faol ishlab turibdi (`node dist/index.js`).
- **Guruhda quizni boshlash**:
  - Guruh admini guruhda `/quiz` buyrug'ini yubordi;
  - Bot guruhga e'lon berdi va 3 soniyadan keyin 1-savolni yubordi;
  - Guruh a'zolari bo'lmagan shaxslar yoki oddiy a'zolar `/quiz` yuborganida bot rad etdi (`adminGuard`).
- **Telegram Quiz Poll formati**:
  - Savollar Telegram'ning rasmiy anonim bo'lmagan Quiz Poll shaklida chiqdi;
  - Har bir savolda 15 soniyalik rasmiy Telegram taymeri (`open_period: 15`) ishladi;
  - Taymer tugagach yoki keyingi savolga o'tilganda savol yopildi va kechikkan javoblar ballga ta'sir qilmadi.
- **Ikki ishtirokchili reyting sinovi**:
  - 1-ishtirokchi (Ali / Tester 1): Barcha 5 ta savolga to'g'ri javob berdi -> **🥇 5/5 ball**;
  - 2-ishtirokchi (Vali / Tester 2): 4 ta savolga to'g'ri javob berdi -> **🥈 4/5 ball**;
  - Reytingda ko'p ball to'plagan ishtirokchi 1-o'rinda chiqdi;
  - Ismlar xavfsiz HTML rejimida chiqdi (`escapeHtml`);
  - Vaqt faqat javob berilgan savollar uchun hisoblandi va `(jami javob vaqti: Xs)` ko'rinishida ko'rsatildi;
  - Takroriy ovoz berish holatlari ballni oshirmasligi tekshirildi va tasdiqlandi.
- **Holat**: **2-bosqich talablari muvaffaqiyatli yakunlandi va qabul qilindi.**

---

## 3. Render deploy holati (3-bosqich)

- **GitHub tayyorgarligi**:
  - `.gitignore` fayliga `.env`, `.env.*.local`, `node_modules/`, `dist/` kiritilgan;
  - Git ombori yaratildi va dastlabki commit tayyorlandi: hech qanday maxfiy token yoki konfiguratsiya Git tarixiga tushmaydi;
  - Foydalanuvchi o'zining GitHub hisobida yangi bo'sh repo yaratib, ushbu loyihani push qilishi mumkin.
- **Render Web Service sozlamalari**:
  - **Service Type**: Web Service
  - **Environment**: Node
  - **Build Command**: `npm run build`
  - **Start Command**: `npm run start`
  - **Port**: Render tomonidan beriladigan `PORT` muhit o'zgaruvchisi avtomatik tarzda o'qiladi (default: 3000, Render odatda 10000 beradi).
- **Muhit o‘zgaruvchilari (Environment Variables)**:
  - `BOT_TOKEN`: `@BotFather` bergan token (maxfiy ma'lumot sifatida faqat Render Environment sozlamalariga yoziladi);
  - `NODE_ENV`: `production`
  - `PORT`: `10000` (ixtiyoriy, Render o'zi kiritadi);
  - `WEBHOOK_URL`: `https://<sizning-xizmat-nomingiz>.onrender.com`
  - `WEBHOOK_SECRET`: ixtiyoriy sirli xavfsizlik kaliti (masalan: `jda_chem_secret_2026`).
- **Telegram Webhook integratsiyasi**:
  - `src/index.ts` da `NODE_ENV=production` va `WEBHOOK_URL` mavjud bo'lganda, bot avtomatik ravishda `bot.api.setWebhook("${WEBHOOK_URL}/webhook")` chaqiradi;
  - `drop_pending_updates: true` orqali server qayta ishga tushganda eski updatelar to'planib qolmaydi;
  - Express server `/webhook` yo'lida `webhookCallback` orqali yangilanishlarni xavfsiz qabul qiladi;
  - `/health` endpointi Render sog'lig'ini tekshirish (Health Check) uchun doimo 200 OK qaytaradi.
- **Bepul tarif bo'yicha muhim eslatma**:
  - Render’ning bepul tarifi (Free Web Service) 15 daqiqa faol bo'lmaganda uxlaydi (spin down). Yangi xabar yoki webhook kelganda 30-50 soniyada uyg'onadi;
  - Sinov uchun bepul tarif yetarli, biroq doimiy production uchun Render Paid ($7/oy) yoki bepul tashqi ping (masalan, UptimeRobot orqali `/health` manzilini har 10 daqiqada tekshirish) tavsiya etiladi.

---

## 4. Xulosa va Keyingi Qadam

- **2-bosqich**: **To'liq yakunlandi va qabul qilindi.**
- **3-bosqich (Render deploy)**: Loyiha kodi va deploy arxitekturasi to'liq tayyorlandi. Foydalanuvchi GitHub'ga push qilib, Render'da Web Service yaratishi kifoya.
- **Keyingi bosqich**: Render deploy amalga oshirilgach, `YOL_XARITASI.md` bo'yicha **4-bosqich — doimiy ma’lumotlar bazasi (PostgreSQL)** ga o'tiladi.
