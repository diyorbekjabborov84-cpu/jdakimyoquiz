# JDA Kimyo Quiz — Firebase tayyorgarligi

2026-09-26 holati. Ushbu faylda maxfiy kalit yo'q.

## Tayyorlangan xizmat

- Google akkaunt: `diyorbekjabborov84@gmail.com`.
- Firebase loyiha ID: `jda-kimyo-quiz`.
- Reja: Spark (bepul).
- Cloud Firestore: `(default)` bazasi, Standard edition, Native mode, `europe-west3` (Frankfurt).
- Firestore mijoz qoidalari: `allow read, write: if false;`. Server Admin SDK xizmat akkaunti orqali ulanadi.
- Xizmat akkaunti: `firebase-adminsdk-fbsvc@jda-kimyo-quiz.iam.gserviceaccount.com`.
- Lokal, Git tomonidan e'tiborsiz qoldiriladigan `.env` faylida `FIREBASE_SERVICE_ACCOUNT_JSON` bor.
- Render `jda-kimyo-quiz` xizmatining Secret Files bo'limida `firebase-service-account.json` bor. Runtime yo'li: `/etc/secrets/firebase-service-account.json`.

## Tekshiruv

Bir martalik lokal sinovda xizmat akkaunti bilan OAuth token olindi va Firestore REST API `(default)` bazasini o'qidi: loyiha `jda-kimyo-quiz`, joylashuv `europe-west3`. Maxfiy kalit yoki token chiqishga yozilmadi. Vaqtinchalik sinov kodi o'chirildi. Yuklab olingan ortiqcha JSON nusxasi Downloads ichidan o'chirildi.

Render Secret File saqlanganda panel kutilmaganda eski `00a9161` commitini qayta deploy qildi; deploy muvaffaqiyatli tugadi va `/health` HTTP 200 qaytardi. Yangi lokal kod push yoki deploy qilinmadi. Hozirgi ishlab turgan bot hali Firestore'dan foydalanmaydi.

## Antigravity uchun keyingi integratsiya

1. PostgreSQL o'rniga Firestore Admin SDK ishlating. `firebase-admin` uchun Node.js 22+ talabini Render va `package.json` da aniq belgilang. Lokal `.env` dagi `FIREBASE_SERVICE_ACCOUNT_JSON` ni, Render'da esa `/etc/secrets/firebase-service-account.json` ni o'qing. Kalitni kodga, logga, hisobotga yoki Gitga yozmang.
2. Productionda Firestore ulanishi va sessiyalarni restore qilish muvaffaqiyatsiz bo'lsa, webhook ishga tushmasin; `/health` ham nosog'lom javob qaytarsin. `DATABASE_URL` ni majburiy konfiguratsiyadan olib tashlang. Lokal JSONga yashirin fallback bo'lmasin.
3. Sessiya va natija ma'lumotlarini Firestore'da saqlang. Bir chat uchun yozuvlar tartibi, qayta kelgan `poll_answer` dedup, bot restartidan keyingi tiklash, yakuniy natija yozilmaguncha yangi quizni bloklash va Telegram poll yuborilib DB yozuvi xato bergan holatni xavfsiz boshqarish shart. `ANTIGRAVITY_QAYTA_TOPSHIRIQ.md` ning 2026-09-26 bo'limidagi 3 ta xato Firestore'ga o'tishda ham tuzatilsin.
4. Sekin va xato beradigan saqlovchi bilan regression testlar hamda kamida bitta haqiqiy Firestore integratsiya testi o'tsin. Test hujjatlari aniq alohida test kolleksiyasida bo'lsin; haqiqiy guruh natijalariga aralashtirilmasin.
5. Kodni push/deploy qilmang. Yakuniy hisobotdan keyin Codex qayta ko'radi.
