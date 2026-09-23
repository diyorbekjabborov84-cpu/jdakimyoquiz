# JDA Kimyo Quiz — Telegram Boti

Telegram guruhlarida kimyo fanidan interaktiv, ko'p savolli quiz musobaqalarini o'tkazadigan rasmiy bot loyihasi.

## Texnologik Stack va Tanlov Asosi

- **Dasturlash tili va muhit**: Node.js (v20+) + TypeScript
- **Telegram Bot Framework**: [grammY](https://grammy.dev/)
  - *Nega grammY tanlandi?*
    1. **TypeScript-first**: grammY boshidanoq TypeScript'da yozilgan, tiplar to'liq va xatosiz ishlaydi.
    2. **Quiz Polls**: Telegramning rasmiy `quiz` turidagi poll-lari va `poll_answer` update-larini qayta ishlash uchun juda qulay va moslashuvchan.
    3. **Webhook va Polling**: Mahalliy muhitda `bot.start()` (long-polling) bilan, Render serverida esa `webhookCallback` (Express) orqali yagona va toza arxitekturada ishlaydi.
    4. **Tezlik va Xavfsizlik**: Middleware arxitekturasi va xatolarni boshqarish tizimi (`bot.catch`) eng yuqori darajada.
- **Veb Server**: Express (Health check endpointi va Webhook qabul qilish uchun)
- **Validatsiya**: Zod (muhit o'zgaruvchilari xavfsizligini ta'minlash uchun)

---

## Mavjud Buyruqlar

- `/start` — Botni ishga tushirish (shaxsiy va guruh chatlariga moslashgan).
- `/help` — Yo'riqnoma va qoidalar bilan tanishish.
- `/quiz` — Guruhda kimyo quizini boshlash (faqat guruh adminlari uchun).
- `/stopquiz` — Faol quizni to'xtatish (faqat guruh adminlari uchun).

---

## Quiz Xususiyatlari va Qoidalari (2-bosqich)

1. **Telegram Quiz Poll formati**: Savollar oddiy matn yoki inline tugma emas, Telegramning rasmiy `type: "quiz"`, `is_anonymous: false` so'rovnomalari ko'rinishida yuboriladi.
2. **5 ta haqiqiy kimyo savoli** (`JDA Kimyo — namuna`):
   - Molar massa (H₂O)
   - Elementning davriy jadvaldagi o'rni (Uglerod)
   - Mineral va moddalar formulalari (NaCl)
   - Atmosfera havosi tarkibi (Azot N₂)
   - Kimyoviy indikatorlar (Lakmus kislotada)
3. **Avtomatik taymer**: Har bir savol uchun 15 soniya vaqt beriladi. Telegramning rasmiy taymeri bilan birga ichki nazorat taymeri ishlaydi.
4. **Ko'p ishtirokchili baholash**: Guruhdagi har bir a'zoning javobi qabul qilinadi.
5. **Takroriy javoblarni elash (Deduplication)**: Bitta ishtirokchining bir savolga bergan javobi faqat bir marta hisoblanadi (takroriy Telegram update-lar ballni oshirmaydi).
6. **Reyting va Tay-breyk (Tie-breaking)**:
   - 1-mezon: To'g'ri javoblar soni bo'yicha kamayish tartibida;
   - 2-mezon: Teng ball to'plangan taqdirda, javob berishga sarflangan umumiy vaqt (ms) bo'yicha o'sish tartibida (tezroq javob bergan ishtirokchi yuqorida turadi).
7. **Multi-group qo'llab-quvvatlash**: Bir nechta guruh bir vaqtning o'zida mustaqil ravishda o'z quizlarini o'tkaza oladi.

---

## Loyiha Tuzilishi

```
.
├── src/
│   ├── bot/
│   │   ├── guards/
│   │   │   └── adminGuard.ts # Guruh admini huquqini tekshirish
│   │   ├── handlers/
│   │   │   ├── start.ts      # /start buyrug'i
│   │   │   ├── help.ts       # /help buyrug'i
│   │   │   ├── quiz.ts       # /quiz va /stopquiz buyruqlari
│   │   │   └── pollAnswer.ts # poll_answer update'i
│   │   └── bot.ts            # grammY bot obyekti va hodisalar
│   ├── config/
│   │   └── env.ts            # Zod bilan muhit o'zgaruvchilarini tekshirish
│   ├── quiz/
│   │   ├── types.ts          # Quiz, Question, Session tiplari
│   │   ├── questions.ts      # "JDA Kimyo — namuna" savollar to'plami
│   │   └── quizManager.ts    # Sessiyalar, taymerlar va reyting
│   ├── server/
│   │   └── app.ts            # Express server va /health endpointi
│   └── index.ts              # Asosiy kirish nuqtasi
├── test/
│   ├── index.test.ts         # 1-bosqich testlari (config, health, bot)
│   └── quiz.test.ts          # 2-bosqich testlari (quiz, dedup, rating, admin)
├── .env.example              # Namunaviy muhit o'zgaruvchilari
├── package.json
├── tsconfig.json
├── YOL_XARITASI.md           # Bosqichma-bosqich reja
└── README.md
```

---

## O'rnatish va Ishga Tushirish

### 1. Bog'liqliklarni o'rnatish
```bash
npm install
```

### 2. Muhit o'zgaruvchilarini sozlash
`.env.example` faylidan nusxa olib, `.env` faylini yarating:
```bash
cp .env.example .env
```
`.env` faylida quyidagi parametrlarni to'ldiring:
- `BOT_TOKEN`: Telegram `@BotFather` orqali olingan bot tokeni (majburiy).
- `PORT`: Server porti (default: `3000`).
- `NODE_ENV`: `development` yoki `production`.

### 3. Loyihani build qilish (TypeScript -> JavaScript)
```bash
npm run build
```

### 4. Dasturni ishga tushirish

**Ishlab chiqish rejimida (avtomatik qayta yuklash bilan):**
```bash
npm run dev
```

**Production rejimida:**
```bash
npm run start
```

### 5. Sog'liqni tekshirish (Health Check)
Server ishga tushgach, quyidagi manzil orqali tekshirish mumkin:
```bash
curl http://localhost:3000/health
```

---

## Testlarni ishga tushirish
Avtomatlashtirilgan testlarni tekshirish (Windows muhitida `npm.cmd test`):
```bash
npm test
```

---

## 3-bosqich: Render Web Service Deploy Yo'riqnomasi

Loyihani [Render.com](https://render.com) bulutli platformasiga joylash tartibi:

### 1. GitHub omboriga yuklash
1. GitHub hisobingizda yangi bo'sh ombor (masalan, `jdakimyoquiz`) yarating.
2. Lokal loyihangizni GitHub'ga yuboring:
```bash
git remote add origin https://github.com/<sizning-username>/jdakimyoquiz.git
git branch -M main
git push -u origin main
```
*(Eslatma: `.env` fayli `.gitignore` orqali himoyalangan, u repoga kirmaydi).*

### 2. Render.com da Web Service yaratish
1. [Render Dashboard](https://dashboard.render.com) ga kiring va **New +** -> **Web Service** tugmasini bosing.
2. Yuqorida ochilgan GitHub repongizni tanlang (**Connect**).
3. Asosiy parametrlarni to'ldiring:
   - **Name**: `jda-kimyo-quiz` (yoki o'zingiz istagan nom)
   - **Region**: Frankfurt (Yevropa — O'zbekistonga eng yaqin va tez)
   - **Branch**: `main`
   - **Runtime**: `Node`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm run start`
   - **Instance Type**: `Free` (bepul)

### 3. Muhit o'zgaruvchilarini (Environment Variables) sozlash
Render Web Service sahifasidagi **Environment Variables** bo'limida quyidagilarni kiriting:
- `BOT_TOKEN`: `@BotFather` bergan token (masalan: `8771542358:AAFS9GXzFrBVpP6v6gQoMb0rzpo2rFwlSW4`)
- `NODE_ENV`: `production`
- `WEBHOOK_URL`: `https://<sizning-xizmat-nomingiz>.onrender.com` (Render taqdim etgan to'liq domen)
- `WEBHOOK_SECRET`: ixtiyoriy maxfiy kalit (masalan: `jda_quiz_secret_secure_key`)

### 4. Deploy va Webhook faollashishi
- **Deploy Web Service** tugmasini bosing.
- Render avtomatik ravishda `npm install`, so'ng `npm run build` bajaradi va `node dist/index.js` ni ishga tushiradi.
- Server ishga tushishi bilan `src/index.ts` Telegram API'ga avtomatik ravishda HTTPS Webhook'ni (`${WEBHOOK_URL}/webhook`) o'rnatadi.
- Render **Logs** bo'limida quyidagi yozuvlar chiqadi:
  ```
  ✅ [HTTP Server] http://localhost:10000 da tinglamoqda
  🩺 [Health Check] http://localhost:10000/health
  🌐 [Bot] Production Webhook rejimida ishlamoqda: https://.../webhook
  ✅ [Bot] Telegram Webhook muvaffaqiyatli o'rnatildi.
  ```

### 5. Botni yangilash va kuzatish
- **Loglarni ko'rish**: Render Dashboard -> Web Service -> **Logs** oynasida har bir savol, javoblar va reyting jarayoni real vaqtda ko'rinadi.
- **Botni yangilash**: Loyihada o'zgarish qilib, GitHub'ga `git push` qilishingiz bilan Render avtomatik yangi versiyani quradi va deploy qiladi (Auto-Deploy yoqilgan bo'lsa).
- **Bepul tarif va uyg'onish kechikishi**: Bepul Render Web Service 15 daqiqa faoliyatsizlikdan keyin uyqu rejimiga (spin down) o'tadi. Birinchi yangi so'rov yoki buyruq kelganda server taxminan 30–50 soniyada uyg'onadi. Doimiy kechikishsiz ishlashi uchun [cron-job.org](https://cron-job.org) yoki [UptimeRobot](https://uptimerobot.com) orqali `https://<service>.onrender.com/health` manziliga har 10 daqiqada bepul ping yuborishni sozlash mumkin.

