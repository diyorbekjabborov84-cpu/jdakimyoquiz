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

## Quiz Xususiyatlari va Qoidalari

1. **Telegram Quiz Poll formati**: Savollar oddiy matn yoki inline tugma emas, Telegramning rasmiy `type: "quiz"`, `is_anonymous: false` so'rovnomalari ko'rinishida yuboriladi.
2. **21 ta haqiqiy kimyo savoli** («Aminokislotalar — suyuqlanish temperaturasi»):
   - 329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning har biri uchun suyuqlanish temperaturasi bo'yicha savol;
   - Har bir savolda 4 ta turli sonli variant va bitta to'g'ri javob;
   - Har bir savol uchun 20 soniya rasmiy vaqt beriladi;
   - Sistein (178 °C) va Sistin (260 °C) alohida moddalar sifatida kiritilgan;
   - Asparagin kislota va Oksiprolin (ikkalasi 270 °C) nomdan temperaturaga qarab tuzilgan.
3. **Ko'p ishtirokchili baholash va reyting**:
   - Natija 21 tadan hisoblanadi (masalan: `21/21 ball`);
   - Umumiy javob vaqti faqat ishtirokchi bosgan javoblarning vaqtlaridan yig'iladi; javobsiz qolgan savollar vaqtga qo'shilmaydi;
   - Noto'g'ri bosilgan javobning vaqti ham sarflangan vaqtga qo'shiladi;
   - Teng ball to'planganda, qisqaroq umumiy javob vaqti ustunlik qiladi.
4. **Takroriy javoblarni elash (Deduplication)**: Bitta ishtirokchining bir savolga bergan javobi faqat bir marta hisoblanadi.
5. **Multi-group qo'llab-quvvatlash**: Bir nechta guruh bir vaqtning o'zida mustaqil ravishda o'z quizlarini o'tkaza oladi.

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

### 2. Render.com da Blueprint orqali xizmat yaratish
1. [Render Dashboard](https://dashboard.render.com) ga kiring va **New +** -> **Blueprint** ni tanlang. `render.yaml` faqat Blueprint orqali avtomatik qo'llanadi.
2. GitHub repongizni tanlang (**Connect**) va `main` branchidagi `render.yaml` ni ko'rib chiqing.
3. Blueprint quyidagi parametrlarni o'rnatadi:
   - **Name**: `jda-kimyo-quiz` (yoki o'zingiz istagan nom)
   - **Region**: Frankfurt (Yevropa — O'zbekistonga eng yaqin va tez)
   - **Branch**: `main`
   - **Runtime**: `Node`
   - **Build Command**: `npm ci --include=dev && npm run build`
   - **Start Command**: `npm run start`
   - **Instance Type**: `Free` (bepul)

### 3. Muhit o'zgaruvchilarini (Environment Variables) sozlash
Blueprint yaratish bosqichida quyidagilarni kiriting:
- `BOT_TOKEN`: `@BotFather` bergan yangi token; uni README, hisobot yoki chatga yozmang.
- `NODE_ENV`: `production`
- `WEBHOOK_URL`: xizmatning yakuniy `https://...onrender.com` domeni. Domen yaratilgandan keyin ma'lum bo'lsa, Render Environment bo'limida kiriting va xizmatni qayta deploy qiling.
- `WEBHOOK_SECRET`: Render Environment bo‘limida maxfiy qiymat sifatida kiriting. 32–64 ta tasodifiy `A-Z`, `a-z`, `0-9`, `_` yoki `-` belgisidan foydalaning; uni ommaga chiqarmang. Telegram boshqa belgilarni qabul qilmaydi.

### 4. Deploy va Webhook faollashishi
- **Deploy Blueprint** tugmasini bosing.
- Render `npm ci --include=dev && npm run build` bajaradi va `node dist/index.js` ni ishga tushiradi.
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
