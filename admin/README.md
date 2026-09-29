# JDA Kimyo Quiz — Admin Panel (1-bosqich)

Ushbu loyiha **JDA Kimyo Quiz** Telegram botining rasmiy veb boshqaruv paneli hisoblanadi.

- **Frontend & BFF**: Next.js 14 (App Router) + TypeScript
- **Hosting platformasi**: Vercel (Jamoa: `jda-group`, Hisob: `diyorbekjabborov84@gmail.com`)
- **Backend API & Bot**: Render (Express + grammY)
- **Doimiy ma'lumotlar bazasi**: Google Cloud Firestore (`groups`, `bot_users`, `quizzes`, `quiz_results`)

---

## 1. Mahalliy muhitda ishga tushirish (Local Development)

### 1-qadam: Bog'liqliklarni o'rnatish
```bash
cd admin
npm install
```

### 2-qadam: Muhit o'zgaruvchilarini sozlash
`admin/.env.local` faylini yarating va quyidagi qiymatlarni kiriting:
```env
RENDER_API_URL=http://localhost:3000
NEXT_PUBLIC_BOT_USERNAME=jdakimyoquizbot
```

### 3-qadam: Loyihani ishga tushirish
```bash
npm run dev
```
Panel brauzerda `http://localhost:3000` (yoki Next.js avtomatik tanlagan port, masalan `http://localhost:3001`) manzilida ochiladi.

### 4-qadam: Ishchi buildni tekshirish
```bash
npm run build
```

---

## 2. Vercel'da joylashtirish (Vercel Deployment)

Loyiha monorepo tarkibida joylashganligi sababli Vercel importida quyidagi sozlamalarni to'g'ri ko'rsatish zarur:

1. **Vercel Dashboard**ga kiring (`jda-group` jamoasi tanlangan bo'lsin).
2. **Add New... -> Project** tugmasini bosing va `jdakimyoquiz` repozitoriyasini import qiling.
3. **Project Settings**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `admin` *(MUHIM: `Edit` tugmasini bosib `admin` papkasini tanlang!)*
   - **Build Command**: `next build` (avtomatik)
   - **Output Directory**: `.next` (avtomatik)
   - **Install Command**: `npm install` (avtomatik)
4. **Environment Variables**:
   - `RENDER_API_URL`: Render'dagi backend xizmati manzili (masalan: `https://jda-kimyo-quiz.onrender.com`).
   - `NEXT_PUBLIC_BOT_USERNAME`: `jdakimyoquizbot`
5. **Deploy** tugmasini bosing.

---

## 3. BotFather orqali Telegram Login domenini ulash

Telegram Login Widget ishlashi uchun Vercel'da berilgan domen Telegram Botiga bog'langan bo'lishi shart:

1. Telegram'da [@BotFather](https://t.me/BotFather) botiga kiring.
2. `/setdomain` buyrug'ini yuboring.
3. Botlar ro'yxatidan `@jdakimyoquizbot` ni tanlang.
4. Vercel tomonidan berilgan domenni kiriting (masalan: `jda-kimyo-quiz-admin.vercel.app`).
   *(DIQQAT: `https://` yoki oxirida `/` qo'ymasdan, faqat toza domen yuboriladi).*
5. BotFather `Success! Domain linked.` deb tasdiqlaydi.

---

## 4. Xavfsizlik va Arxitektura

- **Yagona Admin & Fail-Closed**: Faqat Render serveridagi `ADMIN_TELEGRAM_ID` ga teng raqamli ID egasi tizimga kira oladi. Ushbu o'zgaruvchi o'rnatilmagan bo'lsa, tizim 503 xatosi bilan barcha kirishlarni bloklaydi.
- **Telegram HMAC-SHA256**: Autentifikatsiya faqat Render serverida bot tokeni orqali hisoblangan HMAC imzosi bilan tasdiqlanadi. Brauzerga bot tokeni yoki Firebase service account kalitlari HECH QACHON chiqmaydi.
- **Stateless Imzolangan Sessiya**: Muvaffaqiyatli kirishdan so'ng Vercel domenida `HttpOnly`, `Secure`, `SameSite: lax` cookie (`admin_session`) o'rnatiladi.
- **BFF (Backend-For-Frontend)**: Brauzer Render API'ga to'g'ridan-to'g'ri maxfiy token bilan murojaat qilmaydi; Next.js server route'lari orqali xavfsiz proksi qilinadi.
- **Asinxron Firestore Kuzatuvi**: Botning guruhlar va foydalanuvchilar faolligini qayd etish jarayoni quizlar oqimi va `poll_answer` tezligiga mutlaqo to'sqinlik qilmaydi.

## 5. Guruhlar ro'yxatini to'ldirish

- Botga yetib kelgan guruh xabarlari, buyruqlar va tugma hodisalari guruhni qayd etadi; quiz boshlash shart emas. `my_chat_member` hodisasi qo'shilish/chiqish holatini yangilaydi.
- Production ishga tushganda `quiz_sessions` va `quiz_results` yozuvlaridagi guruh IDlari 200 yozuvli sahifalarda o'qiladi. Takrorlar olib tashlanadi, Telegram orqali nomi va botning a'zoligi tekshiriladi, faqat registrda yo'q guruhlar qo'shiladi. HTTP server bu ish tugashini kutmaydi.
- Mavjud guruhlar, shu jumladan tiklash paytida jonli hodisadan yaratilgan yozuvlar ustidan yozilmaydi. Telegramga ulanish xatosi `left` yoki `active` deb taxmin qilinmaydi: `unknown` holati panelda “A'zoligi aniqlanmagan” bo'lib chiqadi.
- Muvaffaqiyatli tiklash `admin_migrations/group_registry_v1` hujjatida qayd etiladi. Baza xatosida bu belgi yozilmaydi va keyingi ishga tushishda qayta uriniladi. Qayta urinish takroriy guruh yaratmaydi.
- Webhook yangilanganda kutilayotgan hodisalar tashlab yuborilmaydi. Telegram yetkazmagan yoki muddati o'tgan eski hodisalarni bu usul qaytara olmaydi.
- Telegram Bot API bot qo'shilgan barcha tarixiy guruhlar ro'yxatini bermaydi. Bazada izi yo'q guruh botga yangi hodisa yuborganda (masalan `/start`) ko'rinadi. Butunlay noma'lum eski guruhlarni 100% tiklash kafolatlanmaydi.
