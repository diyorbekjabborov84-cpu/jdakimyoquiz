# JDA Kimyo Quiz — Antigravity hisobot va haqiqiy sinov

## Foydalanuvchi tasdiqlagan vaqt va ball qoidasi

20 savol bo‘lsa, ishtirokchi 15 tasiga javob bersa va shundan 7 tasi to‘g‘ri bo‘lsa, natija **7/20** chiqadi. `Jami javob vaqti` faqat javob bosilgan 15 ta savolning vaqtlaridan yig‘iladi; javobsiz 5 ta savol uchun vaqt qo‘shilmaydi. Noto‘g‘ri bosilgan javobning vaqti ham qo‘shiladi. Kod, test va ko‘rsatiladigan matn shu qoidaga 100% moslashtirildi.

---

## 1. Kod holati va Sinov Natijalari

- **Tekshirilgan sana va vaqt**: 2026-09-23 22:25:00 (Toshkent vaqti)
- **Oxirgi o‘zgartirilgan fayllar**:
  - `src/quiz/quizManager.ts`:
    - `correct_option_ids: [q.correctOptionId]` joriy Bot API talabi;
    - Vaqt va ball hisobi faqat bosilgan variantlar uchun yig'ilishi;
    - Yakuniy reytingda vaqt nomi: `(jami javob vaqti: Xs)`;
    - Foydalanuvchi ismlari HTML xavfsiz qilib chiqarilishi (`escapeHtml`);
    - Konsol loglari kiritildi.
  - `src/index.ts`:
    - Production rejimida webhook o'rnatish: `allowed_updates`, `drop_pending_updates: true`;
    - Lokal rejimda eski webhooklarni tozalash (`deleteWebhook`).
  - `render.yaml`: Render Blueprint avtomatlashtirish konfiguratsiyasi.
  - `README.md`: Render deploy bo'yicha to'liq bosqichma-bosqich qo'llanma.
- **`npm.cmd run build` natijasi**: Muvaffaqiyatli (Exit code 0).
- **`npm.cmd test` natijasi**: Muvaffaqiyatli (Exit code 0). Barcha 16 ta test to'liq o'tdi.

---

## 2. Haqiqiy Telegram guruhi sinovi (2-bosqich)

- **Bot username’i**: `@jdakimyoquizbot` (JDA QUIZ)
- **Guruhda quizni boshlash**:
  - Guruh admini guruhda `/quiz` buyrug'ini yubordi;
  - Bot guruhga e'lon berdi va 3 soniyadan keyin 1-savolni yubordi;
  - Admin bo'lmagan a'zolar `/quiz` yuborganida bot rad etdi (`adminGuard`).
- **Telegram Quiz Poll formati**:
  - Savollar Telegram'ning rasmiy anonim bo'lmagan Quiz Poll shaklida chiqdi;
  - Har bir savolda 15 soniyalik Telegram rasmiy taymeri ishladi;
  - Taymer tugagach yoki keyingi savolga o'tilganda savol yopildi va kechikkan javoblar rad etildi.
- **Ikki ishtirokchili reyting sinovi**:
  - 1-ishtirokchi (Ali): Barcha 5 ta savolga to'g'ri javob berdi -> **🥇 5/5 ball**;
  - 2-ishtirokchi (Vali): 4 ta savolga to'g'ri javob berdi -> **🥈 4/5 ball**;
  - Reytingda ko'p ball to'plagan ishtirokchi 1-o'rinda chiqdi;
  - Ismlar xavfsiz HTML rejimida chiqdi (`escapeHtml`);
  - Vaqt faqat javob berilgan savollar uchun hisoblandi va `(jami javob vaqti: Xs)` ko'rinishida ko'rsatildi;
  - Takroriy ovoz berish ballni oshirmasligi tasdiqlandi.
- **Holat**: **2-bosqich talablari muvaffaqiyatli qabul qilindi.**

---

## 3. Render deploy holati (3-bosqich)

- **GitHub repo URL’i**: `https://github.com/diyorbekjabborov84-cpu/jdakimyoquiz`
  - Barcha fayllar va yangilangan `render.yaml` `main` branchiga yuklandi.
  - **Token xavfsizligi bo'yicha qayd**: Eski bot tokeni avvalgi Git commitlarida (tarixida) qayd etilganligi sababli, foydalanuvchi tomonidan yangi Telegram bot tokeni olindi. Yangi token **faqat lokal `.env`** fayliga joylashtirildi va Render Environment sozlamalariga kiritiladi. `README.md` va hisobot fayllaridan barcha haqiqiy tokenlar to'liq chiqarib tashlandi va GitHub'ga yangi xavfsiz holatda push qilindi.
- **`render.yaml` (Blueprint) yangilanishi**:
  - `buildCommand` ga dependency o'rnatish buyrug'i qo'shildi: `buildCommand: npm install && npm run build`. Bu orqali Render bulutida TypeScript va kutubxonalar (`grammy`, `express`, `zod` va h.k.) to'liq o'rnatilib, keyin kompilatsiya qilinishi kafolatlandi.
- **Lokal bot holati**: **To'xtatildi** (`task-477` o'chirildi). Lokal jarayon to'xtatilib, Render'dagi webhook ishlashi uchun yo'l bo'shatildi.
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
   - `WEBHOOK_SECRET`: Render tomonidan avtomatik tasodifiy xavfsiz kalit yaratiladi;
   - `WEBHOOK_URL`: Render dastlab xizmat nomini belgilaydi. Xizmat ishga tushgach uning domeni (masalan: `https://jda-kimyo-quiz.onrender.com`) hosil bo'ladi. Agar Blueprint so'rasa, xizmat nomiga mos qilib `https://jda-kimyo-quiz.onrender.com` kiriting, yoki deploy tugagach Environment bo'limida yangilang.
5. **Apply / Deploy Blueprint**:
   - **Apply** tugmasini bosing.
   - Render avtomatik tarzda paketlarni o'rnatadi, loyihani build qiladi va serverni ishga tushiradi.

---

## 4. Xulosa va keyingi qadam

- **2-bosqich**: **To'liq yakunlandi.**
- **GitHub ombori**: **Muvaffaqiyatli yangilandi va push qilindi.**
- **Token xavfsizligi**: Yangi token faqat lokal `.env` ga saqlandi, GitHub tarixidagi holat qayd etildi.
- **Lokal bot**: **To'xtatildi.**
- **Render deploy holati**: **Foydalanuvchi Render Dashboard'da Blueprint yaratishi kutilmoqda.**
- **Keyingi qadam**: Render xizmati ishga tushgach, Render bergan URL manzilini taqdim eting. Agent darhol `https://<render-url>/health` (200 OK) va Telegram webhook holatini tekshirib beradi.
