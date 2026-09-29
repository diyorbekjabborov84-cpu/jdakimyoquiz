# Antigravityga qayta topshiriq — admin panel 1-bosqich qabulidan oldingi tuzatishlar

Codex 1-bosqich kodini ko'rib chiqdi. Bot va Next.js buildlari o'tdi, admin/auth va regressiya testlari ham o'tdi. Lekin hozirgi testlar quyidagi haqiqiy xavf va funksional kamchiliklarni qamramagan. **Render/Vercel deploy qilma.** Tuzatishlarni shu bosqich ichida yakunla; keyingi bosqichlarga o'tma. `KK3` quizlari va mavjud bot oqimini buzma.

Codex kichik uchta tuzatishni allaqachon kiritdi: ildiz `.gitignore` ga `.next/` va `*.tsbuildinfo` qo'shildi; Telegram Login vidjetidan so'ralmagan `data-request-access="write"` olib tashlandi; noto'g'ri 64 belgili hex bo'lmagan hash `RangeError` bermasdan rad etiladi va regression testi qo'shildi. Bu o'zgarishlarni saqla.

## 1. Autentifikatsiya va sessiya xavfsizligi

- `src/server/adminRoutes.ts` production CORS hozir `origin.includes("localhost")` va `origin.includes("vercel.app")` bo'lsa har qanday manbaga ruxsat beradi, hatto `ADMIN_CORS_ORIGIN` boshqa qiymat bo'lsa ham. Brauzer to'g'ridan-to'g'ri Render API'ga murojaat qilmaydi (BFF), shuning uchun CORS kerak bo'lmasa umuman ochma; kerak bo'lsa faqat **aniq** konfiguratsiyalangan originni qabul qil. `*`, suffix/substring yoki istalgan `vercel.app` domeni productionda o'tmasin. CORS sharti haqiqiy avtorizatsiya o'rniga o'tmasin.
- `admin/app/api/auth/login/route.ts` va `logout/route.ts` POST so'rovlari uchun Origin/CSRF tekshiruvi yo'q. Topshiriqda mutatsiyalarda himoya so'ralgan. Same-origin, konfiguratsiyalangan production domeni va xavfsiz sessiya bilan tekshir; begona Origin bilan yuborilgan login/logout rad etilsin. Kelajakdagi blok, test tahriri, broadcast route'lari ham shu himoya yordamchisidan foydalansin.
- `src/server/adminAuth.ts` dagi `getSessionSecret` uchun static `fallback_insecure_key_change_in_production` va bot tokenidan avtomatik hosil qilinadigan fallbackni olib tashla. Production admin endpointlari `ADMIN_SESSION_SECRET` kuchli va alohida bo'lmasa fail-closed bo'lsin. Sessiya payloadida `iat`/`exp` raqamli va mantiqan yaroqli bo'lishi, maksimal umr 7 kundan oshmasligi tekshirilsin. Telegram `auth_date` qayta ishlatish oynasini 24 soatdan qisqartirib, yangi login uchun oqilona qisqa muddatga (masalan 5 daqiqa) tushir.
- `admin/lib/auth.ts` productionda `RENDER_API_URL` bo'lmasa jim `http://localhost:3000` ga o'tmasin; aniq konfiguratsiya xatosi ko'rsatsin.
- Telegram auth HMAC tekshiruviga faqat tanlab olingan maydonlar emas, Telegram yuborgan barcha ruxsat etilgan primitive maydonlar qatnashishi yoki kutilmagan maydonlar rad etilishi kerak. `hash` va maxfiy bo'lmagan metama'lumotlarni noto'g'ri almashtirish o'tmasin. Testlarga malformed payload va qo'shimcha maydon holatlarini qo'sh.

## 2. Firestore ma'lumotlarining to'g'riligi

- `src/tracking/tracker.ts` da `getOverviewStats` baza xatosini ushlab `0` qaytaradi va shu noto'g'ri ma'lumotni 30 soniya keshga qo'yadi. `getGroupsList/getUsersList` ham xatoda bo'sh ro'yxat qaytaradi. Bunday holatda API `503` yoki aniq xato holatini qaytarsin, panel `0 ta` yoki `hech kim yo'q` deb yanglish ko'rsatmasin. Birorta muvaffaqiyatsiz hisoblash keshga yozilmasin. Faol guruhlar soni bilan hamma tarixiy guruhlar sonini farqlang.
- Qidiruv hozir `orderBy(lastActivity).limit(50)` **keyin** brauzer yoki serverda filtr qiladi. 51- va undan eski yozuvlarni ism/ID bo'yicha topib bo'lmaydi. Firestore'ga mos server qidiruvi va sahifalash (cursor) yarating. Kamida exact chat/user ID hamda normalizatsiyalangan ism/title prefix qidiruvi barcha yozuvlar bo'ylab ishlasin. Agar substring qidiruv qilinmasa, UI placeholder shu chegarani to'g'ri tushuntirsin. `total: groups.length` ni umumiy baza soni sifatida ko'rsatma.
- Guruhning `left/kicked` hodisasi oldin boshlangan, lekin kech tugagan `active` upsert bilan qayta `active` bo'lib qolmasin. Fire-and-forget yozuvlarning navbati/kronologiyasini per-chat himoyalang yoki Firestore transaction bilan event vaqtini solishtiring. Bot chiqarilgan guruh panelda faol deb turmasin.
- Yangi tracker tarixiy guruhlarni avtomatik bilolmaydi. Panelning bosh sahifa va ro'yxatida `Bot kuzatuvi yoqilgandan keyin qayd etilgan` degan tushunarli yozuv bo'lsin; mavjud Firestore sessiyalaridan ishonchli ma'lumot bilan backfill mumkin bo'lsa, alohida, idempotent va xavfsiz migratsiya rejasini hisobotda yozing. Telegram API bermaydigan to'liq a'zolar ro'yxatini taxmin qilmang.

## 3. Test va topshirish

- Hozirgi `test/admin-auth-tracking.test.ts` tracker testida DB yo'q; `trackGroupEvent/trackUserEvent` no-op bo'lib o'tmoqda. Mock Firestore bilan haqiqiy upsert, guruh status tartibi, xato propagatsiyasi, 50 tadan ko'p yozuvli qidiruv va cursorni tekshir.
- `Origin` rad javobi, CORS qat'iyligi, session secret yo'qligi, malformed session payload, `RENDER_API_URL` yo'qligi uchun maqsadli testlar qo'sh.
- Botning va `admin/` ning buildlari va tegishli regressiya testlari o'tsin. Haqiqiy production Firestore ma'lumotlariga test yozma.
- `ANTIGRAVITY_HISOBOT.md` oxiriga nimalar tuzatilgani, fayllar, testlar va **deploy qilinmagan** holatni yoz. Tugagach `qayta topshiriq tugadi, Codex tekshirsin` deb xabar ber.
