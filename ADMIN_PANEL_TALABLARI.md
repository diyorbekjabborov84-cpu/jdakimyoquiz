# JDA Kimyo admin paneli — kelishilgan talablar

Holat: mahsulot talablari. Ushbu hujjat kod yozish va deploydan oldin Antigravity uchun topshiriq hamda Codex uchun qabul mezoni sifatida ishlatiladi.

## Asosiy qoida

- Admin panel Vercel'da, bot va xavfsiz API Render'da ishlaydi; ma'lumotlar doimiy bazada saqlanadi. Render qayta ishga tushganda testlar, guruhlar, foydalanuvchilar, bloklar va yuborish tarixi yo'qolmasin.
- Hozircha faqat loyiha egasi kira oladi. Ochiq ro'yxatdan o'tish bo'lmasin. Telegram orqali kirishda tasdiqlangan raqamli Telegram ID serverda ruxsat etilgan ID bilan solishtirilsin; username ruxsat mezoni bo'lmasin. Bot tokeni va boshqa sirlar brauzer kodiga chiqmasin.
- Panel telefon va kompyuterda qulay ishlasin. Xavfli amallar (umumiy xabar yuborish, nashr qilingan testni arxivlash) oldidan aniq tasdiq ko'rsatsin.

## 1. Bosh sahifa

- Bot mavjud guruhlar, shaxsiy botni ishga tushirgan foydalanuvchilar, nashr qilingan testlar va o'tkazilgan quizlar soni ko'rinsin.
- Oxirgi quizlar, muvaffaqiyatsiz xabarlar va xizmat holatiga tez o'tish bo'lsin.

## 2. Guruhlar

- Bot aniqlagan guruhlar ro'yxati: nom, Telegram chat ID, botning faol/chiqqan holati, oxirgi faollik, o'tkazilgan quizlar soni.
- Qidirish, saralash va guruh tafsilotida quizlar hamda natijalar bo'lsin.
- A'zolar soni Telegram API orqali mavjud bo'lsa ko'rsatilsin. Panel Telegram API bermaydigan to'liq a'zolar ro'yxatini va'da qilmasin.
- Umumiy xabar uchun guruhlarni alohida yoki filtr orqali tanlash mumkin bo'lsin.

## 3. Foydalanuvchilar va blok

- Bot bilan shaxsiy chat boshlagan yoki quizda qatnashgan foydalanuvchilar ro'yxati: Telegram ID, ko'rinadigan ism/username, oxirgi faollik, shaxsiy bot holati va natijalari. Ma'lum bo'lmagan barcha guruh a'zolarini ro'yxatga qo'shilgandek ko'rsatmasin.
- Qidirish va foydalanuvchi tafsilotlarini ko'rish bo'lsin.
- Blok **faqat botning shaxsiy chatdagi funksiyalariga** ta'sir qilsin: shaxsiy testni buyruq yoki havola orqali boshlash to'xtasin; foydalanuvchiga qisqa tushunarli javob qaytsin. Guruh quizidagi ishtiroki va natijasi saqlansin.
- Blokni ochish, bloklangan vaqt va sababni ko'rish bo'lsin. Bloklangan foydalanuvchi shaxsiy umumiy xabar oluvchilarga kiritilmasin.

## 4. Testlar

- Testlar ro'yxati: nom, o'zgarmas ID, savollar soni, holat (qoralama/nashr etilgan/arxiv), oxirgi tahrir. Qidirish, nusxalash va arxivlash bo'lsin.
- Muharrir: savol, 2–4 variant, bitta to'g'ri javob, vaqt va ixtiyoriy izoh. Savollar tartibini o'zgartirish, Telegram Quiz Poll ko'rinishini oldindan ko'rish va xatolarni nashrdan oldin ko'rsatish bo'lsin.
- Nashr qilingan test uchun `/quiz_<ID>` kodi va `https://t.me/<bot_username>?start=quiz_<ID>` havolasini bir bosishda nusxalash bo'lsin. ID tahrir/deploydan keyin ham o'zgarmasin.
- Bot panelda nashr qilingan testni yangi deploysiz o'qisin. Avvaldan kodda bor testlarning IDsi va havolalari migratsiyadan keyin ham ishlasin. Davom etayotgan sessiya tahrir sabab o'rtada o'zgarmasin.
- `.txt` importi alohida keyingi bosqich: haqiqiy namuna fayli berilgach qo'shiladi.

## 5. Natijalar

- Sana, test, guruh/shaxsiy chat bo'yicha filtrlash; ishtirokchi, to'g'ri javob/jami savol va jami javob vaqti ko'rinsin.
- Vaqt faqat bosilgan javoblarning vaqtlaridan, shu jumladan noto'g'ri javoblardan yig'ilsin. Javobsiz savollar vaqtga kirmasin. Masalan: 20 savol, 15 javob, 7 to'g'ri natija `7/20`.

## 6. Umumiy xabarlar

- Auditoriya: bot mavjud guruhlar; botni avval shaxsiyda ishga tushirgan foydalanuvchilar; yoki tanlangan manzillar. Bloklangan shaxsiy foydalanuvchilar chiqarilsin.
- Matn, rasm va havola tugmasini qo'shish; Telegramdagi ko'rinishini oldindan ko'rish, qoralama saqlash va keyinga rejalashtirish bo'lsin.
- Yuborishdan oldin auditoriya turi va manzillar soni ko'rsatilsin. Yuborish holati (navbatda/yuborildi/xato) va xato sabablari ko'rinsin; muvaffaqiyatsizlarini xavfsiz qayta yuborish mumkin bo'lsin.
- Telegram tezlik cheklovlariga mos navbat, `429` uchun kutish va takror yuborishda dublikatdan himoya bo'lsin. Bot chiqarilgan guruh yoki botni bloklagan foydalanuvchiga yuborish xatosi butun navbatni to'xtatmasin.
- Umumiy xabar faqat panel egasining aniq yuborish amali bilan ketadi; qoralama yoki oldindan ko'rish xabar yubormaydi.

## 7. Sozlamalar va xavfsizlik

- Majburiy obuna kanallari va standart savol vaqti ko'rinsin. Sozlama o'zgarishi guruh quizlariga obuna talabini kiritmasin.
- Muhim admin amallari tarixi: kim, qachon, qaysi test/blok/xabarni o'zgartirgan. Hozir bitta egaga mo'ljallangan bo'lsa ham tarix saqlansin.
- Render API endpointlari server tomonda autentifikatsiya va ruxsat tekshiruviga ega bo'lsin; faqat paneldagi tugmalarni yashirish xavfsizlik o'rnini bosmaydi.

## Antigravity ishini qabul qilish tartibi

Ishni tekshiriladigan bo'laklarga ajrat: (1) baza migratsiyasi va faqat egaga kirish; (2) guruh/foydalanuvchi kuzatuvi va shaxsiy blok; (3) test muharriri, nashr va bot bilan bog'lash; (4) natijalar hamda umumiy xabarlar; (5) Vercel/Render deploy va haqiqiy Telegram sinovi. Har bo'lakning natijasini Codex tekshirmaguncha keyingisini tayyor deb hisoblama.

1. Har modul bo'yicha ishlaydigan natija, o'zgargan fayllar, migratsiya va deploy holati hisobotga yozilsin.
2. Codex diff, qurilish, maqsadli testlar va haqiqiy bot/panel oqimini tekshiradi. Kichik xatolarni Codex tuzatadi; arxitektura, ruxsat yoki ma'lumot yo'qolishiga ta'sir qiladigan katta xatolar Antigravityga qayta beriladi.
3. Obuna tugmasi callback'i guruhga ko'chirilsa ham guruh admini huquqini chetlab o'tmasligi kerak. Shaxsiy blok, majburiy obuna va guruh ruxsatlari barcha kirish yo'llarida bir xil ishlashi tekshirilsin.
4. Panelni to'liq tayyor deb hisoblash uchun kamida: egadan boshqa login rad etilishi; panelda test nashr etilib botda deploysiz ochilishi; shaxsiy blok guruhni buzmasligi; rasm/matn/havolali xabar tanlangan test manzillariga yuborilishi va yuborish tarixi saqlanishi kerak.
