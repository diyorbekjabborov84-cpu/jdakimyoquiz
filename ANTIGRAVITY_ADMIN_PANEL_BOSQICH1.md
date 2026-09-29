# Antigravityga topshiriq — JDA Kimyo admin paneli, 1-bosqich

## Kontekst va ish chegarasi

Foydalanuvchi admin panel ishini boshlashni so'radi. To'liq mahsulot talablari `ADMIN_PANEL_TALABLARI.md` da. Panel **Vercel** da, bot va himoyalangan API **Render** da, doimiy ma'lumotlar **mavjud Cloud Firestore** da qoladi. Vercel loyihasi `diyorbekjabborov84@gmail.com` hisobida bo'ladi. Hozircha yagona admin — loyiha egasi. Bu faylni 1-bosqich uchun bajar; keyingi bosqichlarni hozircha yozma va deploy qilma.

Vercel hisob tekshiruvi: brauzerda `diyorbekjabborov84@gmail.com` **Verified Primary** ko'rindi; tanlangan jamoa `jda-group`. Vercel loyihasini keyin shu jamoada yarating, repo importida Root Directory `admin` bo'lsin. Hozircha Vercel loyihasi yaratilmagan va panel deploy qilinmagan.

Repo holatiga e'tibor ber: KK3 quizlari `599ee7b` commitida alohida saqlandi. Mavjud quiz savollari va ularning IDlariga tegma. `ADMIN_PANEL_TALABLARI.md` va ushbu topshiriq faylidagi mahalliy o'zgarishlarni saqla; boshqa aloqasiz untracked fayllarni commitga tasodifan qo'shma. O'z o'zgarishlaringni aniq fayllar bo'yicha ajrat. Render yoki Vercel'ga deploy qilma; Codex ko'rib chiqadi.

## Hozirgi koddagi aniq holat

- Bot TypeScript + grammY + Express. `src/server/app.ts` hozir `/health`, `/` va `/webhook` ga ega.
- Firestore mavjud. `src/firebase/firestore.ts` da `quiz_sessions`, `quiz_results`, `groups`, `bot_users`, `quizzes` kolleksiya nomlari bor, lekin `groups` va `bot_users` ni faol yozadigan kod topilmadi. Dashboard ularni bo'sh deb noto'g'ri talqin qilmasin.
- Quizlar hozir koddagi `src/quiz/questions.ts` registridan ishlaydi. 1-bosqichda test muharriri yoki migratsiya qilinmaydi.
- Yagona adminning Telegram raqamli IDsi repoda yo'q. Username yoki emailni Telegram ID sifatida qabul qilma. `ADMIN_TELEGRAM_ID` majburiy server env bo'lsin; qiymat topilmaguncha admin kirishi yopiq bo'lsin.
- Vercel hisobidagi Google email faqat hosting egaligini bildiradi. Panel loginini shu emailga bog'lash haqida kelishilmagan; `ADMIN_PANEL_TALABLARI.md` dagidek tasdiqlangan Telegram raqamli ID bilan kirish kerak.

## 1-bosqichda yetkaziladigan natija

1. Repo ichida alohida `admin/` Next.js + TypeScript loyihasi yarating. Vercel monorepo importida Root Directory `admin` bo'lishi mumkin. Telefon va kompyuterda ishlaydigan sodda, qulay o'zbekcha login, sidebar va bosh sahifa tayyorlang. Bo'sh yoki hali mavjud bo'lmagan bo'limlarni ishga tayyordek ko'rsatmang; `Keyingi bosqichda` deb aniq belgilang.
2. Telegram Login orqali kelgan ma'lumotlarni **Render serverida** Bot API tokeni yordamida rasmiy HMAC tekshiruvdan o'tkazing; `auth_date` yangiligini tekshiring; `id` ni aynan `ADMIN_TELEGRAM_ID` bilan solishtiring. Frontendga bot tokeni yoki Firebase service account chiqmasin. Token yoki boshqa maxfiy qiymatni repo, test fixture, log, URL query yoki foydalanuvchiga ko'rinadigan xatoga yozmang. Login domenini BotFather'da ulash uchun kerakli deploydan keyingi ko'rsatmani hisobotga yozing.
3. Kirishdan keyingi sessiya HttpOnly, Secure, SameSite cookie orqali Vercel domenida ishlasin. Brauzer Render API'ga admin tokenini bevosita yubormasin; Vercel server route/BFF vositachi bo'lsin. Render har admin API so'rovida imzolangan sessiyani va admin IDni qayta tekshirsin. Sessiya muddati va chiqish (`logout`) ishlasin. Mutatsiya endpointlarida CSRF/Origin himoyasi bo'lsin. Login xato yoki env yo'q bo'lsa fail-closed.
4. Bot guruhga qo'shilishi/chiqishi va `/start` kabi mos keladigan hodisalarda `groups` ma'lumotini ehtiyotkor upsert qiling: chat ID, nom, bot holati, oxirgi faollik. Bot bilan shaxsiy chat boshlagan va quiz javob bergan ma'lum foydalanuvchilar uchun `bot_users` ga ID, ko'rinadigan ism/username, oxirgi faollik, shaxsiy chat holati yozilsin. Telegram bermaydigan barcha guruh a'zolarini mavjud deb ko'rsatmang. Mavjud guruh quiz oqimini yoki `poll_answer` tezligini sezilarli sekinlashtirmang; Firestore xatosi quizni yiqitmasin, ammo kuzatuv xatosi logda ko'rinsin. Dublikat hujjatlar bo'lmasin.
5. Panel bosh sahifasida Render `/health` holati hamda real Firestore sonlari: bot borligi ma'lum guruhlar, ma'lum foydalanuvchilar, kodda mavjud testlar, o'tkazilgan quizlar. Raqamlarni olish qimmat to'liq skan bilan har sahifa yuklanishida bajarmang; zarur bo'lsa cache/aggregation. `groups` va `bot_users` dan kamida o'qish ro'yxati bo'lsin: qidirish, nom/ID, oxirgi faollik, bot holati. Guruh a'zolari soni noma'lum bo'lsa `noma'lum` deb yozilsin.
6. `admin/.env.example` va Render uchun env namunalarini faqat **nom va izoh** bilan bering. Haqiqiy tokenlar va Firebase kalitlarini nusxalamang. Build, test, lokal run va Vercel `admin` Root Directory sozlashni `admin/README.md` ga yozing.

## Qabul mezonlari va tekshiruv

- `admin` va bot TypeScript buildlari o'tadi. Relevant unit/integration testlar: Telegram HMAC to'g'ri/xato/eskirgan; ruxsatli va boshqa ID; sessiya yo'q/muddati o'tgan; himoyalangan API rad javobi; guruh/foydalanuvchi upsert; botning eski quiz oqimi buzilmagan.
- Auth va dashboard API uchun Render endpointlari autentifikatsiyasiz oshkor bo'lmaydi. `/health` va Telegram webhook avvalgidek ishlaydi.
- Haqiqiy tashqi servisga tegmaydigan testlarda Firestore mock/emulator ishlatilsin; production ma'lumotlarini o'zgartirmang.
- Hisobotda o'zgargan fayllar, arxitektura, test natijalari, hali qo'lda kerak bo'ladigan env qiymatlar (`ADMIN_TELEGRAM_ID`, sessiya siri, Vercel domeni) va deploy qilinmaganligi yozilsin.
- Yakunda menga `1-bosqich tugadi, Codex tekshirsin` deb xabar ber. Keyingi bosqichlar: shaxsiy blok; test muharriri va botga dinamik nashr; natijalar va umumiy xabarlar. Ularni hozircha boshlama.
