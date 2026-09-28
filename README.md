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

- `/start` — Shaxsiy chatda kanal obunasini tekshiradi. Quiz havolasi shaxsiy chatda ochilsa, guruhga o'tish tugmasini beradi; guruhda obuna tekshirilmaydi.
- `/help` — Yo'riqnoma va buyruqlar ro'yxatini ko'rish.
- `/quiz` — Asosiy quiz kodlarini olish xabari va `@jdaquizkod` kanaliga o'tish tugmasi (guruhda ham, shaxsiyda ham erkin ishlaydi, hech kimdan obuna talab qilinmaydi).
- `/quiz_<ID>` yoki `/start_<ID>` — Tanlangan quizni guruhda istalgan guruh a'zosi boshlaydi (masalan: `/start_R1` yoki `/quiz_KK1_1`). Shaxsiy chatda guruhga o'tish tugmasi chiqadi.
- `/resume` — To'xtatilgan (pauzadagi) yoki server qayta ishga tushgach tiklangan quizni aynan keyingi savoldan davom ettiradi (istalgan guruh a'zosi yubora oladi).
- `/stop` yoki `/stopquiz` — Guruhdagi faol quizni faqat guruh admini to'xtata oladi. Stop bosilganda savol va taymer to'xtaydi, yakuniy natija yuborilmaydi.

---

## Majburiy Kanal Obunasi (Faqat Shaxsiy Chatlar Uchun)

- **Majburiy kanallar**: [@jdaquizkod](https://t.me/jdaquizkod) va [@jdakimyouz](https://t.me/jdakimyouz).
- **Qayerda tekshiriladi**: Faqat shaxsiy chatda (`private`) oddiy `/start` va eski obunani tekshirish tugmasi orqali. Guruhda obuna talab qilinmaydi.
- **Obunasiz holatda**: Oddiy `/start` da foydalanuvchiga ikkala kanalga a'zo bo'lish havolalari va «✅ A’zo bo‘ldim — tekshirish» tugmasi ko'rsatiladi.
- **Obunadan so'ng**: Oddiy `/start` tekshiruvida botdan foydalanish xabari chiqadi. Quizlar shaxsiy chatda boshlanmaydi; quiz havolasi guruhga o'tish tugmasini beradi.
- **Xatolik xavfsizligi**: Telegram `getChatMember` API xatolik berganda foydalanuvchini noto'g'ri "a'zo emas" deb ko'rsatmaydi; tushunarli vaqtinchalik xato xabarini beradi.
- **Guruhlarda obuna talab qilinmaydi**: Guruhda quiz boshlashda va javob berishda hech qanday kanal obunasi so'ralmaydi; istalgan a'zo boshlaydi, qatnashchilar javob beradi va reyting hisoblanadi.

---

## Ko'p Quizli Tizim va Qoidalar

1. **O'zgarmas va Takrorlanmas IDlar**: Har bir quiz koddagi stabil, doimiy IDga ega:
   - `amino_acids`: «Aminokislotalar — suyuqlanish temperaturasi» (21 ta savol, 20s/savol)
   - `kimyo_asoslari`: «Kimyo asoslari — namuna» (5 ta savol, 20s/savol)
   - `KK1_1`: «Kolloid kimyo — 1-qism (KK1_1)» (01–20-savollar: Kolloid kimyo asoslari, dispers sistemalar, 20s/savol)
   - `KK1_2`: «Kolloid kimyo — 2-qism (KK1_2)» (21–40-savollar: Sirt energiyasi, adsorbsiya, 20s/savol)
   - `KK1_3`: «Kolloid kimyo — 3-qism (KK1_3)» (41–60-savollar: Zol va gellar, optik va kinetik xossalar, 20s/savol)
   - `KK2_1`: «Kolloid kimyo — 2-mavzu 1-qism (KK2_1)» (01–20-savollar: Dispers sistema va asosiy turlari, buyruq: `/quiz_KK2_1` yoki `/start_KK2_1`, 20s/savol)
   - `KK2_2`: «Kolloid kimyo — 2-mavzu 2-qism (KK2_2)» (21–40-savollar: Fazalar, barqarorlik va tasnif, buyruq: `/quiz_KK2_2` yoki `/start_KK2_2`, 20s/savol)
   - `KK2_3`: «Kolloid kimyo — 2-mavzu 3-qism (KK2_3)» (41–60-savollar: Olinish va tozalash usullari, buyruq: `/quiz_KK2_3` yoki `/start_KK2_3`, 20s/savol)
   - `I3_1`: «Alkanlar — 1-qism (I3_1)» (01–20-savollar: Tuzilish, nomlanish va izomeriya, buyruq: `/quiz_I3_1` yoki `/start_I3_1`, 20s/savol)
   - `I3_2`: «Alkanlar — 2-qism (I3_2)» (21–40-savollar: Tabiiy manbalar, fizik xossalar va olinish, buyruq: `/quiz_I3_2` yoki `/start_I3_2`, 20s/savol)
   - `I3_3`: «Alkanlar — 3-qism (I3_3)» (41–60-savollar: Kimyoviy xossalar va termik o'zgarishlar, buyruq: `/quiz_I3_3` yoki `/start_I3_3`, 20s/savol)
   - `R1`: «Rus tili va adabiyoti — 1-qism (1–50)» (1–50-savollar, buyruq: `/start_R1` yoki `/quiz_R1`, 20s/savol)
   - `R2`: «Rus tili va adabiyoti — 2-qism (51–100)» (51–100-savollar, buyruq: `/start_R2` yoki `/quiz_R2`, 20s/savol)
   - `R3`: «Rus tili va adabiyoti — 3-qism (101–150)» (101–150-savollar, buyruq: `/start_R3` yoki `/quiz_R3`, 20s/savol)
   - `R4`: «Rus tili va adabiyoti — 4-qism (151–200)» (151–200-savollar, buyruq: `/start_R4` yoki `/quiz_R4`, 20s/savol)
   - `R5`: «Rus tili va adabiyoti — 5-qism (201–250)» (201–250-savollar, buyruq: `/start_R5` yoki `/quiz_R5`, 20s/savol)
   - `R6`: «Rus tili va adabiyoti — 6-qism (251–300)» (251–298-savollar + 5-to'plamdan 2 ta to'ldiruvchi savol, jami 50 ta savol, buyruq: `/start_R6` yoki `/quiz_R6`, 20s/savol)
2. **Guruh Havolalari (Deep Linking)**:
   - **Shaxsiy chatda ochilgan eski havola**: `https://t.me/<bot_username>?start=quiz_<ID>` — test boshlanmaydi, guruhga o'tish tugmasi chiqadi.
   - **Guruhga qo'shish va to'g'ridan-to'g'ri boshlash uchun**: `https://t.me/<bot_username>?startgroup=quiz_<ID>` yoki `?startgroup=start_<ID>`
     - *KK2_1*: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK2_1` (yoki `?startgroup=start_KK2_1`)
     - *KK2_2*: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK2_2` (yoki `?startgroup=start_KK2_2`)
     - *KK2_3*: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK2_3` (yoki `?startgroup=start_KK2_3`)
     - *I3_1*: `https://t.me/jdakimyoquizbot?startgroup=quiz_I3_1` (yoki `?startgroup=start_I3_1`)
     - *I3_2*: `https://t.me/jdakimyoquizbot?startgroup=quiz_I3_2` (yoki `?startgroup=start_I3_2`)
     - *I3_3*: `https://t.me/jdakimyoquizbot?startgroup=quiz_I3_3` (yoki `?startgroup=start_I3_3`)
     - *R1*: `https://t.me/jdakimyoquizbot?startgroup=start_R1` (yoki `?startgroup=R1`)
     - *R2*: `https://t.me/jdakimyoquizbot?startgroup=start_R2` (yoki `?startgroup=R2`)
     - *R3*: `https://t.me/jdakimyoquizbot?startgroup=start_R3` (yoki `?startgroup=R3`)
     - *R4*: `https://t.me/jdakimyoquizbot?startgroup=start_R4` (yoki `?startgroup=R4`)
     - *R5*: `https://t.me/jdakimyoquizbot?startgroup=start_R5` (yoki `?startgroup=R5`)
     - *R6*: `https://t.me/jdakimyoquizbot?startgroup=start_R6` (yoki `?startgroup=R6`)
3. **Dinamik Aralashtirish (Dynamic Shuffling)**:
   - Barcha yangi quizlar boshlangan har safar savollar ketma-ketligi va har bir savolning 4 ta javob varianti mustaqil tasodifiy aralashtiriladi.
   - 1-ustundagi to'g'ri javob yangi tartibga mos ravishda to'g'ri qayta indekslanadi va baholanadi.
   - Bitta quiz ichida savol takrorlanmaydi; parallel guruhlardagi testlar bir-biriga aslo ta'sir qilmaydi.
4. **Faqat Guruh Cheklovi (`groupOnly`)**:
   - Barcha quizlar faqat Telegram guruhlarida o'tkaziladi. Shaxsiy chatda quiz buyrug'i yoki havolasi yuborilsa, bot guruhga qo'shish tugmasini chiqaradi.
5. **Telegram Quiz Poll formati**: Savollar oddiy matn yoki inline tugma emas, Telegramning rasmiy `type: "quiz"`, `is_anonymous: false` so'rovnomalari ko'rinishida yuboriladi.
6. **Chat Sessiyalari Izolyatsiyasi**:
   - Har bir guruh boshqa guruhlardan mutlaqo mustaqil o'z sessiyasiga, savollar holatiga, vaqt va ballar hisobiga ega.
   - Bitta chatda faol quiz davom etayotganda ikkinchi quiz boshlanishi bloklanadi. Konkurent bosishlarda poyga holati (race condition) bloklangan.
7. **Ko'p ishtirokchili baholash va reyting**:
   - Natija savollar sonidan hisoblanadi (masalan: `20/20 ball` yoki `21/21 ball`);
   - Umumiy javob vaqti faqat ishtirokchi bosgan javoblarning vaqtlaridan yig'iladi; javobsiz qolgan savollar vaqtga qo'shilmaydi;
   - Noto'g'ri bosilgan javobning vaqti ham sarflangan vaqtga qo'shiladi;
   - Teng ball to'planganda, qisqaroq umumiy javob vaqti ustunlik qiladi.
8. **Takroriy javoblarni elash (Deduplication)**: Bitta ishtirokchining bir savolga bergan javobi faqat bir marta hisoblanadi.
9. **Bot Guruhga Qo‘shilgandagi Yo‘riqnoma**:
   - Bot guruhga yangi qo'shilganda maxsus yo'riqnoma xabari va «📢 Test kodlari» tugmasi yuboriladi.
   - Adminlik huquqi o'zgarganda yoki oddiy `/start` da bu xabar qayta chiqmaydi.
10. **Aqlli Pauza (Smart Pause)**:
   - Guruhda ketma-ket 3 ta savolga hech kim javob bermasa, test avtomatik tarzda to'xtatiladi.
   - Guruhga «▶️ Qolgan joyidan davom ettirish» tugmasi chiqariladi (guruhning istalgan a'zosi bosa oladi).
   - Bitta odam noto'g'ri javob bersa ham hisoblagich darhol 0 ga qaytadi.
   - Davom ettirilganda test qayta aralashmasdan aynan keyingi savoldan boshlanadi va barcha to'plangan ballar/vaqtlar saqlanadi.
   - Pauza tugmasi sessiya identifikatori (`sessionId`) bilan bog'langan; eski/tugagan sessiya tugmasi yangi sessiyaga ta'sir qilmaydi.
11. **Doimiy Saqlash va Tashqi Baza Arxitekturasi (Durable Persistence)**:
   - **Lokal Fayl Tizimi**: `data/sessions.json` faqat lokal ishlab chiqish (development) va testlar uchun ishlatiladi.
   - **Render Cheklovi**: Render Free tarifida konteyner fayl tizimi efemer (ephemeral) hisoblanadi; yangi versiya deploy qilinganda, spin-down yoki restart paytida diskdagi fayllar o'chib ketadi.
   - **Cloud Firestore Integratsiyasi**: Doimiy saqlash uchun Google Cloud Firestore (`jda-kimyo-quiz`, Frankfurt `europe-west3`) ishlatiladi. Barcha sessiyalar va natijalar `quiz_sessions` va `quiz_results` kolleksiyalarida har bir savol, javob va yakunlash holatida real vaqtda yangilanadi.
   - **Restartdan keyin tiklanish**: Server qayta ishga tushganda barcha guruhlardagi to'xtab qolgan quizlar avtomatik `paused` holatida tiklanadi, guruhlarga yangi `[▶️ Qolgan joyidan davom ettirish]` tugmali xabar yuboriladi va `/resume` buyrug'i faol bo'ladi.
   - **Xatoliklarda sessiya yo'qolmasligi**: Telegram API vaqtinchalik `429 Too Many Requests` yoki tarmoq xatosi berganda sessiya o'chirilmaydi; savol indeksi saqlanib, xavfsiz pauzaga o'tkaziladi.

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

Lokal development va oddiy unit testlar sessiyalarni faylda saqlaydi, hatto `.env`da Firebase kaliti bo'lsa ham. `npm test` test jarayonida `FIRESTORE_LOCAL_ENABLED` ni o'chiradi. Lokal botni ataylab Firestore bilan ishlatish kerak bo'lsa, `FIRESTORE_LOCAL_ENABLED=true` qo'ying. `test/firestore.test.ts` alohida `test_*` kolleksiyalarida jonli integratsiya sinovi o'tkazadi; bu sinov uchun Firebase ulanishi talab qilinadi.

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

### 3. Muhit o'zgaruvchilarini (Environment Variables) va Maxfiy Fayllarni sozlash
Render Dashboard -> Environment bo'limida:
- `BOT_TOKEN`: `@BotFather` bergan token (maxfiy, hech qayerga oshkor qilinmasin).
- `NODE_ENV`: `production` (productionda Firebase xizmat akkaunti talab qilinadi).
- `NODE_VERSION`: `22.13.0` (`firebase-admin` uchun Node.js 22+ talab etiladi).
- `WEBHOOK_URL`: Xizmatning yakuniy `https://...onrender.com` domeni.
- `WEBHOOK_SECRET`: 32–64 ta tasodifiy belgidan iborat maxfiy kalit.
- `DATABASE_URL`: (Ixtiyoriy) Tashqi PostgreSQL ulanishi.

Render Dashboard -> **Secret Files** bo'limida:
- Fayl nomi: `firebase-service-account.json`
- Fayl yo'li (runtime): `/etc/secrets/firebase-service-account.json`
- Mazmuni: Firebase Service Account JSON (maxfiy hisob ma'lumotlari).

### 4. Deploy va Webhook faollashishi
- **Deploy Blueprint** tugmasini bosing.
- Render `npm ci --include=dev && npm run build` bajaradi va `node dist/index.js` ni ishga tushiradi.
- Server ishga tushishdan oldin Cloud Firestore ulanishi va sessiyalarni bazadan yuklashni tekshiradi; agar baza ulanmasa yoki hisob ma'lumotlari bo'lmasa, server xatolik bilan to'xtaydi (soxta ishlayotganlik e'lon qilinmaydi, webhook ochilmaydi).
- Cloud Firestore sog'lom bo'lganda `src/index.ts` Telegram API'ga avtomatik ravishda HTTPS Webhook'ni (`${WEBHOOK_URL}/webhook`) o'rnatadi.
- Render **Logs** bo'limida quyidagi yozuvlar chiqadi:
  ```
  ✅ [Firebase] Cloud Firestore muvaffaqiyatli ulandi.
  ✅ [HTTP Server] http://localhost:10000 da tinglamoqda
  🩺 [Health Check] http://localhost:10000/health (baza uzilsa 503 qaytaradi)
  🌐 [Bot] Production Webhook rejimida ishlamoqda: https://.../webhook
  ✅ [Bot] Telegram Webhook muvaffaqiyatli o'rnatildi.
  ```

### 6. Botni yangilash va kuzatish
- **Loglarni ko'rish**: Render Dashboard -> Web Service -> **Logs** oynasida har bir savol, javoblar va reyting jarayoni real vaqtda ko'rinadi.
- **Botni yangilash**: Loyihada o'zgarish qilib, GitHub'ga `git push` qilishingiz bilan Render avtomatik yangi versiyani quradi va deploy qiladi (Auto-Deploy yoqilgan bo'lsa).
- **Bepul tarif va uyg'onish kechikishi**: Bepul Render Web Service 15 daqiqa faoliyatsizlikdan keyin uyqu rejimiga (spin down) o'tadi. Birinchi yangi so'rov yoki buyruq kelganda server taxminan 30–50 soniyada uyg'onadi. Doimiy kechikishsiz ishlashi uchun [cron-job.org](https://cron-job.org) yoki [UptimeRobot](https://uptimerobot.com) orqali `https://<service>.onrender.com/health` manziliga har 10 daqiqada bepul ping yuborishni sozlash mumkin.
