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
  - Barcha fayllar va `render.yaml` `main` branchiga to'liq yuklandi.
  - `.env` va boshqa maxfiy fayllar Git tarixiga kirmaganligi qat'iy tekshirildi.
- **Lokal bot holati**: **To'xtatildi** (`task-477` o'chirildi). Lokal jarayon to'xtatilib, Render'dagi webhook ishlashi uchun yo'l bo'shatildi.
- **Render Web Service URL’i**: [Foydalanuvchi Render hisobida xizmatni yaratgach aniqlanadi]
- **Render deploy holati**: **Kutilmoqda / Foydalanuvchi harakati zarur** (Deploy to'liq tugadi deb belgilanmadi).
- **Sabab**: Tizimda Render CLI yoki `RENDER_API_KEY` mavjud emasligi sababli agent to'g'ridan-to'g'ri Render hisobiga kira olmaydi.

### Foydalanuvchi Render'da bajarishi kerak bo‘lgan aniq qadamlar:

1. **Render'ga kirish**: Brauzerda [dashboard.render.com](https://dashboard.render.com) ga kiring.
2. **Yangi Web Service ochish**:
   - **New +** tugmasini bosing va **Web Service** ni tanlang;
   - `diyorbekjabborov84-cpu/jdakimyoquiz` GitHub omborini tanlang (**Connect**).
3. **Sozlamalarni tekshirish** (loyihadagi `render.yaml` tufayli avtomatik to'ldiriladi):
   - **Name**: `jda-kimyo-quiz`
   - **Region**: `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Runtime**: `Node`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm run start`
   - **Plan**: `Free`
4. **Environment Variables (Muhit o'zgaruvchilari)**:
   - `BOT_TOKEN`: Telegram botingiz tokeni (masalan: `<BOT_TOKEN>`)
   - `NODE_ENV`: `production`
   - `WEBHOOK_URL`: `https://<render-bergan-nom>.onrender.com` (Render sahifasi yuqorisida ko'rsatilgan xizmat domeni)
   - `WEBHOOK_SECRET`: ixtiyoriy sirli so'z (masalan: `jda_quiz_super_secret_2026`)
5. **Deploy qilish**:
   - **Deploy Web Service** tugmasini bosing.
   - Render build va start jarayonini boshlaydi.
   - Xizmat ishga tushgach, sahifaning yuqorisidagi Render URL manzilini oling (masalan, `https://jda-kimyo-quiz.onrender.com`).

---

## 4. Xulosa va keyingi qadam

- **2-bosqich**: **To'liq yakunlandi.**
- **GitHub ombori**: **Muvaffaqiyatli yaratildi va push qilindi.**
- **Lokal bot**: **To'xtatildi.**
- **Render deploy holati**: **Foydalanuvchi Render Dashboard'da Web Service yaratishi kutilmoqda.**
- **Keyingi qadam**: Render xizmati ishga tushgach, foydalanuvchi o'zining Render URL manzilini taqdim etadi. Agent darhol `https://<render-url>/health` va Telegram webhook statusini tekshiradi hamda guruhdagi yakuniy sinovni tasdiqlaydi.
