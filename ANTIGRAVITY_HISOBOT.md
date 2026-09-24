# JDA Kimyo Quiz — Antigravity hisobot va haqiqiy sinov

## Foydalanuvchi tasdiqlagan vaqt va ball qoidasi

Savollardan nechtasiga javob berilsa, ball faqat to‘g‘ri javoblar sonidan va jami savollar sonidan hisoblanadi (masalan, 21 savoldan 18 tasiga javob berib, 15 tasi to‘g‘ri bo‘lsa: **15/21 ball**). `Jami javob vaqti` faqat javob bosilgan savollarning vaqtlaridan yig‘iladi; javobsiz qolgan savollar uchun vaqt qo‘shilmaydi. Noto‘g‘ri bosilgan javobning vaqti ham yig‘iladi. Kod, test va ko‘rsatiladigan matn shu qoidaga 100% moslashtirildi.

---

## 1. Kod holati va 21 ta Aminokislota Quizi

- **Tekshirilgan sana va vaqt**: 2026-09-23 23:30:00 (Toshkent vaqti)
- **Oxirgi o‘zgartirilgan fayllar**:
  1. `src/quiz/questions.ts`: Dastlabki 5 ta namunaviy savol o‘rniga 329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning suyuqlanish temperaturasi quizi to‘liq kiritildi.
  2. `src/quiz/quizManager.ts`: Quiz boshlanishi e'lonida savol vaqti dinamik ko'rsatilishi (`20 soniya`) ta'minlandi.
  3. `test/quiz.test.ts`: Test 1 barcha 21 ta savol, har birida 4 ta unikal sonli variant, to'g'ri qiymatlar va 20s vaqtini avtomatik tekshiradi; Test 5 da `open_period: 20` tekshiruvi moslashtirildi.
  4. `test/e2e-simulation.test.ts`: 21 savolli to'liq guruh quiz sinovi o'tkazildi (Ali 21/21 ball, Vali 18/21 ball).
  5. `README.md`: 21 ta savolli yangi quiz tavsifi va Render Blueprint yo'riqnomasi yangilandi.
  6. `render.yaml`: `buildCommand: npm install && npm run build` (dependency o'rnatish) qo'shildi.
  7. `.env`: Yangi token faqat lokal joylashtirildi (Git va hujjatlarga kiritilmagan).
- **21 ta aminokislotaning tekshirilgan ma'lumotlari (17-jadval bo‘yicha)**:
  1. Glitsin — 292 °C
  2. Alanin — 297 °C
  3. Valin — 315 °C
  4. Leysin — 337 °C
  5. Izoleysin — 284 °C
  6. Asparagin kislota — 270 °C
  7. Glutamin kislota — 249 °C
  8. Ornitin — 140 °C
  9. Lizin — 224 °C
  10. Serin — 228 °C
  11. Treonin — 253 °C
  12. Sistein — 178 °C
  13. Sistin — 260 °C
  14. Metionin — 283 °C
  15. Fenilalanin — 275 °C
  16. Tirozin — 344 °C
  17. Triptofan — 382 °C
  18. Prolin — 299 °C
  19. Oksiprolin — 270 °C
  20. Gistidin — 277 °C
  21. Arginin — 238 °C
- **Alohida hisobga olingan muhim jihatlar**:
  - *Sistein (178 °C)* va *Sistin (260 °C)* alohida moddalar sifatida kiritildi;
  - *270 °C* qiymati jadvalda ikki marta uchrashi (Asparagin kislota va Oksiprolin) sababli, savollar modda nomidan temperaturaga qarab tuzildi;
  - Har bir savolda 4 ta turli sonli unikal variant tanlandi (takrorlanishlar yo'q);
  - Har bir savolga Telegram taymeri uchun 20 soniya (`timeLimitSeconds: 20`) belgilandi;
  - Natija 21 tadan hisoblanadi (masalan: `21/21 ball`);
  - Vaqt faqat bosilgan variantlardan yig'iladi, javobsiz qolgan savollar vaqtga qo'shilmaydi.
- **`npm.cmd run build` natijasi**: Muvaffaqiyatli (Exit code 0).
- **`npm.cmd test` natijasi**: Muvaffaqiyatli (Exit code 0). Barcha 16 ta test va 21 savolli E2E simulyatsiyasi to'liq o'tdi.

---

## 2. Haqiqiy Telegram guruhi sinovi

- **Bot username’i**: `@jdakimyoquizbot` (JDA QUIZ)
- **Guruhda quizni boshlash**:
  - Guruh admini guruhda `/quiz` buyrug'ini yuborganida 21 savolli «Aminokislotalar — suyuqlanish temperaturasi» quizi boshlanadi;
  - Admin bo'lmagan foydalanuvchilar urinishi `adminGuard` orqali rad etiladi.
- **Telegram Quiz Poll formati**:
  - Savollar Telegram'ning rasmiy anonim bo'lmagan Quiz Poll shaklida ketma-ket yuboriladi;
  - Har bir savolda 20 soniyalik Telegram rasmiy taymeri (`open_period: 20`) ishlaydi;
  - Taymer tugagach savol yopiladi va kechikkan javoblar ballga ta'sir qilmaydi.
- **Ishtirokchilar reytingi va xavfsizlik**:
  - Ballar 21 tadan hisoblanadi;
  - Ismlar xavfsiz HTML rejimida chiqadi (`escapeHtml`);
  - Vaqt faqat javob berilgan savollar uchun hisoblanadi va `(jami javob vaqti: Xs)` ko'rinishida ko'rsatiladi;
  - Takroriy ovoz berish ballni oshirmasligi tasdiqlandi.

---

## 3. Render deploy holati (3-bosqich)

- **GitHub repo URL’i**: `https://github.com/diyorbekjabborov84-cpu/jdakimyoquiz`
  - Barcha yangilangan fayllar, 21 ta aminokislota savollari va yangilangan `render.yaml` `main` branchiga push qilindi.
  - **Token xavfsizligi bo'yicha qayd**: Eski bot tokeni avvalgi Git commitlarida (tarixida) qayd etilganligi sababli, foydalanuvchi tomonidan yangi Telegram bot tokeni olindi. Yangi token **faqat lokal `.env`** fayliga joylashtirildi va Render Environment sozlamalariga kiritiladi. `README.md` va hisobot fayllaridan barcha haqiqiy tokenlar to'liq chiqarib tashlandi va GitHub'ga yangi xavfsiz holatda push qilindi.
- **`render.yaml` (Blueprint) yangilanishi**:
  - `buildCommand: npm install && npm run build` orqali Render bulutida barcha paketlar o'rnatilib, TypeScript kompilatsiyasi amalga oshirilishi ta'minlandi.
- **Lokal bot holati**: **To'xtatildi**. Render'dagi webhook ishlashi uchun yo'l bo'shatilgan.
- **Render Web Service URL’i**: `https://jda-kimyo-quiz.onrender.com`
- **Render deploy holati**: **Muvaffaqiyatli yakunlandi (Live / Active)**.
- **Render Health Check tekshiruvi (`/health`)**:
  - So'rov: `GET https://jda-kimyo-quiz.onrender.com/health`
  - Natija: HTTP 200 OK (`status: "ok"`, `service: "jda-kimyo-quiz"`)
- **Telegram Bot Webhook tekshiruvi (`getWebhookInfo`)**:
  - `url`: `https://jda-kimyo-quiz.onrender.com/webhook`
  - `has_custom_certificate`: `false`
  - `pending_update_count`: `0`
  - `ip_address`: `216.24.57.16`
  - `allowed_updates`: `["message", "poll", "poll_answer", "chat_member"]`
  - Xatolik: Hech qanday xatolik qayd etilmagan (`last_error_date` / `last_error_message` mavjud emas).

---

## 4. Ko‘p quizli tizim va shaxsiy havolalar (Yangi bosqich)

- **O‘zgarmas, takrorlanmas Quiz ID lari**:
  - `amino_acids`: «Aminokislotalar — suyuqlanish temperaturasi» (21 ta savol, har biriga 20 soniya, 1-quiz sifatida saqlandi).
  - `kimyo_asoslari`: «Kimyo asoslari — namuna» (5 ta savol, har biriga 20 soniya).
  - IDlar doimiy va deploydan keyin o'zgarmaydi.
- **/quiz buyrug'i**:
  - Mavjud barcha quizlar ro'yxatini, sarlavhasi, tavsifi, savollar soni, boshlash buyrug'i (`/quiz_<ID>`) va maxsus shaxsiy havolasi bilan chiqaradi.
- **/quiz_<ID> dinamik buyrug'i**:
  - `/quiz_amino_acids` yoki `/quiz_kimyo_asoslari` orqali tanlangan quiz boshlanadi;
  - Noma'lum ID kiritilsa (masalan, `/quiz_noma_lum`): «❌ Bunday IDga ega quiz topilmadi...» tushunarli xabari qaytadi.
- **Shaxsiy havolalar (Deep Linking)**:
  - `https://t.me/<bot_username>?start=quiz_<ID>` havolasi yaratiladi;
  - Havolani bosgan foydalanuvchining shaxsiy chatida `/start quiz_<ID>` qabul qilinib, aynan shu quiz darhol ochiladi.
- **Huquqlar va chatlar izolyatsiyasi**:
  - **Guruhda**: Quizni faqat guruh admini boshlashi yoki `/stop` qilishi mumkin (oddiy a'zolar rad etiladi);
  - **Shaxsiy chatda**: Foydalanuvchi o'zi mustaqil boshlay oladi va to'xtata oladi;
  - **Izolyatsiya**: Har bir chat (shaxsiy yoki guruh) o'z alohida sessiyasi, savollari va natijalariga ega bo'lib, boshqa chatlarga umuman ta'sir qilmaydi;
  - **Bitta faol quiz qoidasi**: Bitta chatda faol quiz davom etayotganda ikkinchi quiz boshlanishi bloklanadi.
- **/stop va /stopquiz**:
  - Guruhda faqat admin, shaxsiy chatda foydalanuvchi faol quizni to'xtata oladi;
  - Stop bosilganda amaldagi poll yopiladi, taymer bekor qilinadi va **yakuniy natija / reyting yuborilmaydi**.
- **O'zgargan fayllar**:
  - `src/quiz/types.ts`: Quiz va Session tiplari;
  - `src/quiz/questions.ts`: `amino_acids` va `kimyo_asoslari` quizlari, `getAllQuizzes()`, `getQuizById()`;
  - `src/quiz/quizManager.ts`: Xabarlar guruh va shaxsiy chatlarga moslashtirildi;
  - `src/bot/handlers/quiz.ts`: `/quiz`, `/quiz_<ID>`, `/stop`, `/stopquiz`, ruxsatlar va takroriy quiz blokirovkasi;
  - `src/bot/handlers/start.ts`: Deep link (`?start=quiz_<ID>`) orqali shaxsiy chatda quiz ochilishi;
  - `src/bot/handlers/help.ts`: Ko'p quizli buyruqlar va havolalar tushuntirishi;
  - `src/bot/bot.ts`: `/quiz_<ID>` regex middleware va buyruqlar ro'yxatga olindi;
  - `test/multi-quiz.test.ts`: Barcha holatlar uchun 10 ta to'liq avtomatlashtirilgan test;
  - `package.json`: `npm test` buyrug'iga `multi-quiz.test.ts` qo'shildi;
  - `README.md`: Yangi buyruqlar va ko'p quizli tizim imkoniyatlari kiritildi.
- **Avtomatlashtirilgan testlar natijasi**:
  - `test/index.test.ts`: 100% o'tdi;
  - `test/quiz.test.ts`: 100% o'tdi;
  - `test/e2e-simulation.test.ts`: 100% o'tdi;
  - `test/multi-quiz.test.ts`: 10/10 test 100% o'tdi.
- **Xavfsizlik**: Bot tokeni yoki boshqa maxfiy kalitlar hisobotga va repoga yozilmadi.
