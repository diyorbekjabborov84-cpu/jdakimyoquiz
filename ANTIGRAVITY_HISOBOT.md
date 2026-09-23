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
- **Render Web Service URL’i**: [Foydalanuvchi Render hisobida Blueprint yaratgach aniqlanadi]
- **Render deploy holati**: **Kutilmoqda / Foydalanuvchi harakati zarur** (Deploy to'liq tugadi deb belgilanmadi).
- **Sabab**: Tizimda Render CLI yoki `RENDER_API_KEY` mavjud emasligi sababli agent to'g'ridan-to'g'ri Render hisobiga kira olmaydi.

### Render uchun to‘g‘ri Blueprint yo‘riqnomasi:

1. **Render Dashboard'ga kirish**: Brauzerda [dashboard.render.com](https://dashboard.render.com) ga kiring.
2. **Yangi Blueprint ochish**:
   - Yuqori o'ng burchakdagi **New +** tugmasini bosing va **Blueprint** ni tanlang (Eslatma: `render.yaml` aynan Blueprint orqali avtomatik o'qiladi);
   - `diyorbekjabborov84-cpu/jdakimyoquiz` GitHub omborini tanlang (**Connect**).
3. **Sozlamalarni tasdiqlash**:
   - Render avtomatik tarzda `render.yaml` faylini aniqlaydi va quyidagi parametrlarni o'rnatadi:
     - Service: `jda-kimyo-quiz` (Web Service, Node)
     - Plan: `Free`
     - Region: `Frankfurt`
     - Build Command: `npm install && npm run build`
     - Start Command: `npm run start`
     - Health Check Path: `/health`
4. **Environment Variables (Muhit o'zgaruvchilarini kiritish)**:
   - `BOT_TOKEN`: `@BotFather` bergan yangi tokeningizni kiriting (faqat Render'da saqlanadi);
   - `NODE_ENV`: `production` (avtomatik);
   - `WEBHOOK_SECRET`: Render avtomatik tasodifiy xavfsiz kalit yaratadi;
   - `WEBHOOK_URL`: Render dastlab xizmat nomini belgilaydi. Xizmat ishga tushgach uning domeni (masalan: `https://jda-kimyo-quiz.onrender.com`) hosil bo'ladi. Agar Blueprint so'rasa, xizmat nomiga mos qilib `https://jda-kimyo-quiz.onrender.com` kiriting, yoki deploy tugagach Environment bo'limida yangilang.
5. **Apply / Deploy Blueprint**:
   - **Apply** tugmasini bosing.
   - Render avtomatik tarzda paketlarni o'rnatadi, loyihani build qiladi va serverni ishga tushiradi.

---

## 4. Xulosa va keyingi qadam

- **21 ta savolli kimyo quizi**: **To'liq yaratildi, 21 ta savol va 4 ta unikal variant tekshirildi va barcha testlar muvaffaqiyatli o'tdi.**
- **GitHub ombori**: **Barcha o'zgarishlar GitHub'ga push qilindi.**
- **Token xavfsizligi**: Yangi token faqat lokal `.env` ga saqlandi, GitHub tarixidagi holat qayd etildi.
- **Lokal bot**: **To'xtatildi.**
- **Render deploy holati**: **Foydalanuvchi Render Dashboard'da Blueprint yaratishi kutilmoqda.**
- **Keyingi qadam**: Render xizmati ishga tushgach, Render bergan URL manzilini taqdim eting. Agent darhol `https://<render-url>/health` (200 OK) va Telegram webhook holatini tekshirib beradi.
