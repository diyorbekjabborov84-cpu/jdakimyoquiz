# JDA Kimyo Quiz — Antigravity uchun yo‘l rejasi

## Loyiha maqsadi

Telegram guruhlarida kimyo fanidan ko‘p savolli quiz o‘tkazadigan bot yaratish. Foydalanuvchi savollarga Telegramning **quiz poll** ko‘rinishida javob beradi. Bot to‘g‘ri javoblarni, sarflangan vaqtni va yakuniy reytingni hisoblaydi. Bot Render’da, keyinchalik qo‘shiladigan admin panel Vercel’da ishlaydi.

Bu hujjatni bosqichma-bosqich bajar. Har bosqich oxirida ishlaydigan natijani tekshir, nima bajarilganini va keyingi qadamni qisqa yoz. Hozircha `.txt` fayldan savol o‘qish yoki import qilishni amalga oshirma.

## Asosiy talablar

- Quizlar dastlab **kod ichida** saqlansin. Birinchi namunada kamida 5 ta kimyo savoli bo‘lsin.
- Har savolda matn, 2–4 javob varianti, bitta to‘g‘ri javob va ixtiyoriy tushuntirish bo‘lsin.
- Savollar oddiy xabar yoki inline tugma emas, Telegramning `quiz` turidagi poll xabari bo‘lsin.
- Bot guruhda ishga tushadigan ko‘p savolli quizni qo‘llasin. Bitta guruhdagi bir nechta ishtirokchi qatnashib, o‘z ballini olishi kerak.
- Har savol uchun vaqt chegarasi bo‘lsin. Vaqt tugagach, keyingi savolga o‘tilsin.
- Yakunda to‘g‘ri javoblar soni bo‘yicha reyting chiqsin; teng ball bo‘lsa, qisqaroq umumiy javob vaqti ustun bo‘lsin.
- **Vaqt qoidasi (foydalanuvchi tasdiqlagan):** ishtirokchi faqat javobni bosgan savollarining javob berish vaqtini yig‘adi; javobsiz savollar vaqtga qo‘shilmaydi. Noto‘g‘ri bosilgan javobning vaqti ham yig‘iladi. Masalan, 20 savoldan 15 tasiga javob berib, 7 tasini to‘g‘ri topgan ishtirokchi uchun natija `7/20`, vaqt esa faqat bosilgan 15 ta javob vaqtining yig‘indisi bo‘ladi. Javoblar soni va jami savollar sonini bir-biriga almashtirma.
- Quizni guruhda boshlash huquqi dastlab guruh adminlariga berilsin. Keyinchalik bu qoida sozlanadigan bo‘lsin.
- Bir guruhda bir paytning o‘zida faqat bitta faol quiz bo‘lsin. Turli guruhlar bir vaqtda alohida quiz ishlata olsin.
- Bot tokeni, webhook siri, baza paroli va boshqa maxfiy ma’lumotlar kodga yoki Git tarixiga yozilmasin.

## Texnik yo‘nalish

- Bot/backend: Node.js + TypeScript; Telegram Bot API bilan ishlaydigan mos kutubxonani tanla va tanlov sababini `README.md` da yoz.
- Hosting: bot uchun Render **web service** va HTTPS webhook. Lokal ishlab chiqishda qulay usuldan foydalanish mumkin, lekin production’da bitta aniq update qabul qilish usuli ishlasin.
- Admin panel: keyingi bosqichda Vercel’da joylashadigan web ilova. U Render backend API bilan ishlaydi.
- Ma’lumotlar bazasi: birinchi prototipda quiz mazmuni kodda bo‘ladi. Natijalar va sessiyalarni doimiy saqlash bosqichida PostgreSQL qo‘shilsin.
- Render’ning bepul web xizmati faolsizlikdan keyin uxlaydi, bepul Render Postgres esa muddatli. Shuning uchun bepul tarifni faqat sinov deb hisobla; doimiy foydalanish uchun barqaror xizmat va baza tanlovini deploy hujjatida qayd et.

## 1-bosqich — loyiha asosi

1. Bot loyihasini yarat: TypeScript sozlamalari, kerakli skriptlar, `.gitignore`, `.env.example`, `README.md`.
2. Konfiguratsiyani muhit o‘zgaruvchilaridan o‘qi; kerakli qiymat bo‘lmasa tushunarli xato ber.
3. `/start` va `/help` buyruqlarini qo‘sh. Guruhda bot nima qila olishini qisqa tushuntir.
4. Bot sog‘lig‘ini tekshirish uchun HTTP endpoint qo‘sh; Render shu serverni ishga tushira olsin.

**Qabul mezoni:** bot lokal ishlaydi, buyruqlarga javob beradi, token kodda yo‘q, ishga tushirish yo‘riqnomasi aniq.

## 2-bosqich — koddagi savollar bilan guruh quizsi

1. Kod ichida `JDA Kimyo — namuna` quizini kamida 5 ta haqiqiy kimyo savoli bilan belgilab qo‘y.
2. Quizni boshlash uchun guruh buyrug‘i va kerakli tugmalarni yarat. Guruh admini ekanini tekshir.
3. Har savolni Telegram `quiz` poll sifatida yubor. Ishtirokchilarni aniqlash va ball hisoblash uchun poll anonim bo‘lmasin.
4. Bot yuborgan poll javoblarini qabul qilib, har foydalanuvchi uchun javobni faqat bir marta hisobla. Takroriy Telegram update ballni ikki marta oshirmasin.
5. Vaqt tugaganda savolni yop, keyingisini yubor. Oxirida guruhga reyting va har ishtirokchining to‘g‘ri javoblar sonini chiqar.
   Reytingdagi vaqtni `jami javob vaqti` deb nomla; u quizning devor soati bo‘yicha umumiy davomiyligi emas. Testda 20 savol, 15 ta bosilgan javob, 7 ta to‘g‘ri javob holatini tekshir: `7/20`, vaqt esa faqat 15 ta bosilgan javobdan yig‘ilsin.
6. Ikki guruhda bir vaqtda quiz, bitta guruhda qayta boshlash, javobsiz qolgan savol va bot qayta ishga tushishi holatlarini tekshir.

**Qabul mezoni:** kamida ikki kishi bitta Telegram guruhida quizni oxirigacha ishlaydi; Telegramning haqiqiy quiz poll interfeysi, vaqt chegarasi va yakuniy reyting ko‘rinadi.

## 3-bosqich — Render deploy

1. GitHub reposiga joylash uchun tayyorla; maxfiy ma’lumotlar repoga kirmaganini tekshir.
2. Render web service build/start buyruqlarini va `PORT` bilan ishlashni sozla.
3. Render’da muhit o‘zgaruvchilarini kiriting, production webhook’ni o‘rnating va Telegram update’larini faqat shu endpointda qabul qiling.
4. Test guruhida `/start`, quizni boshlash, barcha savollar va reytingni qayta sinab ko‘r.
5. `README.md` ga deploy, muhit o‘zgaruvchilari, loglarni ko‘rish va botni yangilash qadamlarini yoz.

**Qabul mezoni:** lokal kompyuter o‘chirilganida ham bot Render orqali test guruhida ishlaydi. Bepul tarifdagi uyg‘onish kechikishi alohida qayd etiladi.

## 4-bosqich — doimiy ma’lumotlar bazasi

1. PostgreSQL’da quiz, savol, variant, guruh, o‘yin sessiyasi, ishtirokchi javobi va natija uchun jadvallarni yarat.
2. Koddagi namuna savollarni bazaga ko‘chirish yo‘lini yarat, lekin birinchi ishlaydigan koddagi quizni buzma.
3. Deploy/restart’dan so‘ng natijalar saqlanishini tekshir. Faol sessiyalar qayta tiklanishi yoki xavfsiz yakunlanishi aniq qoida bilan ishlasin.
4. Zaxira nusxa olish va tiklash tartibini hujjatlashtir.

**Qabul mezoni:** bot qayta ishga tushgandan keyin avvalgi quizlar va yakunlangan natijalar yo‘qolmaydi.

## 5-bosqich — Vercel admin panel

1. Admin kirishini xavfsiz qil; oddiy ochiq URL orqali quizlarni o‘zgartirib bo‘lmasin.
2. Quiz va savollarni yaratish, tahrirlash, o‘chirish, tartiblash, vaqtni belgilash hamda nashr qilish sahifalarini qo‘sh.
3. Guruhlar, o‘tkazilgan quizlar va reytinglarni ko‘rish sahifasini qo‘sh.
4. Panelni Vercel’da deploy qil va Render API bilan ulanishini tekshir.

**Qabul mezoni:** admin panelda yangi quiz yaratiladi va u botda guruh uchun tanlanib ishga tushiriladi.

## 6-bosqich — `.txt` fayldan savol importi

Bu bosqichni **keyinroq**, foydalanuvchi haqiqiy `.txt` namunasini bergach bajar. `+` va `-` belgilari bo‘yicha formatni o‘sha namunaga moslab aniqlang. Importdan oldin xatolarni ko‘rsating: noto‘g‘ri belgi, kam variant, to‘g‘ri javob yo‘qligi yoki ortiqcha to‘g‘ri javob. Import qilingan savollar admin panelda ko‘rib chiqilib, keyin nashr etilsin.

## Antigravity uchun ish tartibi

- Ishni **1-bosqichdan** boshla; bosqichlarni tartib bilan bajar. Har bosqichdan so‘ng ishlaydigan holatni tekshir va natijani foydalanuvchiga yoz.
- Noaniq mahsulot qarori chiqsa, amalga oshirishni to‘xtatmasdan hujjatdagi boshlang‘ich qoidaga amal qil; qarorni `README.md` da qayd et. Faqat token, hosting akkaunti yoki boshqa foydalanuvchigagina tegishli ma’lumot kerak bo‘lsa so‘ra.
- `.txt` importni, admin panelni yoki murakkab statistika funksiyalarini 1–3-bosqichga aralashtirma.
- Har bosqichda faqat haqiqiy xatoni tutadigan zarur tekshiruv/testlarni qo‘sh. Ishlaydigan botni test guruhida sinash asosiy qabul mezoni bo‘lsin.
