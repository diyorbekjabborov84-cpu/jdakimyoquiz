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

---

## 5. Shaxsiy Chatda Majburiy Kanal Obunasi va Yangi /quiz Xulqi

- **Majburiy kanallar**:
  - [@jdaquizkod](https://t.me/jdaquizkod) — Quiz kodlari kanali;
  - [@jdakimyouz](https://t.me/jdakimyouz) — JDA Kimyo rasmiy kanali.
- **Shaxsiy chatda obunani tekshirish**:
  - `/quiz_<ID>` yoki `?start=quiz_<ID>` orqali shaxsiy test boshlashdan oldin `getChatMember` orqali ikkala kanal a'zoligi tekshiriladi;
  - A'zo bo'lmagan foydalanuvchiga ikkala kanal tugmasi va `callback_data: check_sub_<quizId>` bilan «✅ A’zo bo‘ldim — tekshirish» tugmasi ko'rsatiladi;
  - Foydalanuvchi tanlagan quiz ID si yo'qolmaydi va obuna tasdiqlangach o'sha quiz darhol boshlanadi.
- **Xatolik xavfsizligi (API Error handling)**:
  - `getChatMember` chaqiruvi Telegram API xatoligi yoki tarmoq uzilishiga uchrasa, foydalanuvchini asossiz "a'zo emas" deb noto'g'ri ko'rsatmaydi;
  - Tushunarli vaqtinchalik xato xabari beriladi (`⚠️ Kanal a'zoligini tekshirishda vaqtinchalik xatolik yuz berdi...`).
- **Guruhlarda obuna umuman talab qilinmaydi**:
  - Guruh admini kanalga a'zo bo'lmasa ham quizni boshlay oladi;
  - Guruh a'zolari kanalga a'zo bo'lmasa ham savollarga javob bera oladi va ball oladi;
  - Guruhdagi `/stop` qoidasi o'zgarmasdan saqlanadi.
- **/quiz buyrug'i yangilandi**:
  - Quiz kodlarini ro'yxatlash o'rniga «Asosiy quiz kodlarini @jdaquizkod kanalidan olasiz» xabari va kanal tugmasi ko'rsatiladi;
  - Bu xabar guruhda ham, shaxsiy chatda ham birdek chiqadi va hech kimdan obuna talab qilmaydi.
- **O'zgargan va qo'shilgan fayllar**:
  - `src/bot/guards/subscriptionGuard.ts`: Kanal parametrlari, `checkChannelSubscriptions` va tugmalar generatori;
  - `src/bot/handlers/quiz.ts`: Majburiy obuna tekshiruvi, `handleCheckSubscriptionCallback` va yangi `/quiz` xabari;
  - `src/bot/bot.ts`: `check_sub_` callbackQuery tinglovchisi ulandi;
  - `src/quiz/quizManager.ts`: `TelegramApiSender` interfeysiga ixtiyoriy `getChatMember` qo'shildi;
  - `test/subscription.test.ts`: Barcha holatlar uchun 7 ta qat'iy test;
  - `test/multi-quiz.test.ts`: Yangi `/quiz` formatiga moslandi;
  - `package.json`: `npm test` buyrug'iga `test/subscription.test.ts` ulandi;
  - `README.md`: Majburiy kanal obunasi va yangi buyruqlar yo'riqnomasi qo'shildi.
- **Avtomatlashtirilgan testlar natijasi**:
  - `test/subscription.test.ts`: 7/7 test 100% muvaffaqiyatli o'tdi:
    - ✅ Test 1: Obunasiz foydalanuvchiga kanal tugmalari va tekshirish tugmasi ko'rsatilishi;
    - ✅ Test 2: Obuna bo'lmasdan tekshirish tugmasi bosilganda rad etish;
    - ✅ Test 3: Obunadan keyingi qayta tekshiruvda tanlangan quiz (ID saqlangan holda) boshlanishi;
    - ✅ Test 4: Deep link (`?start=quiz_<ID>`) orqali kirganda obuna tekshiruvi;
    - ✅ Test 5: Guruhda hech kimdan obuna talab qilinmasligi (admin boshlaydi, qatnashchilar javob beradi);
    - ✅ Test 6: `getChatMember` xatolik berganda tushunarli vaqtinchalik xato qaytarish;
    - ✅ Test 7: `/quiz` buyrug'i guruhda ham, shaxsiyda ham kanal xabarini ko'rsatishi va obuna talab qilmasligi.
- **Xavfsizlik**: Barcha maxfiy kalitlar va tokenlar himoyalangan, fayl va loglarga yozilmadi.

## 6. Codex qabul tekshiruvi: shaxsiy /start obunasi

- Foydalanuvchi shaxsiy chatda oddiy `/start` bosganda obuna so'ralmayotganini ko'rsatdi. Sabab: avvalgi tekshiruv faqat test boshlashga ulangan edi.
- Oddiy shaxsiy `/start` endi ikkala kanal a'zoligini tekshiradi. A'zo bo'lmaganlarga kanal tugmalari va `check_sub_start` qayta tekshirish tugmasi chiqadi; tekshiruvdan o'tganlarga botdan foydalanish xabari chiqadi.
- Guruhdagi `/start` obuna talab qilmaydi. Test deep linklari tanlangan test ID sini saqlashda davom etadi.
- TypeScript tekshiruvi va `test/subscription.test.ts` dagi 11/11 holat o'tdi. Render deploy va haqiqiy Telegram sinovi alohida tekshiriladi.

---

## 7. Kolloid Kimyo (KK_M1) — 60 ta Savol, 3 ta Yangi Quiz va Dinamik Aralashtirish

- **Manba fayl**: `KK_M1_QUIZ_SAVOLLAR.txt` (KK_M1 taqdimotining 60 ta savoli).
- **3 ta mustaqil Telegram quiz shakllantirildi**:
  1. `KK1_1`: 01–20-savollar — *Kolloid kimyo — 1-qism (KK1_1)* (Kolloid kimyo asoslari, dispers sistemalar va sirt hodisalari).
  2. `KK1_2`: 21–40-savollar — *Kolloid kimyo — 2-qism (KK1_2)* (Sirt energiyasi, adsorbsiya va dispers sistemalar xossalari).
  3. `KK1_3`: 41–60-savollar — *Kolloid kimyo — 3-qism (KK1_3)* (Zol va gellar, optik va kinetik xossalar, koagulyatsiya).
  - Har bir to'plamda roppa-rosa 20 tadan savol, jami 60 ta unikal savol.
  - Har bir savolda aynan 4 ta turli javob varianti va 20 soniyalik Telegram rasmiy taymeri (`timeLimitSeconds: 20`).
- **Dinamik Aralashtirish (Dynamic Shuffling & Recalculation)**:
  - Har safar quiz boshlanganda savollar tartibi tasodifiy aralashtiriladi (`shuffleArray`);
  - Har bir savolning 4 ta javob varianti alohida mustaqil aralashtiriladi;
  - Variantlar aralashgach, to‘g‘ri javob indeksi (`correctOptionId`) yangi variant tartibiga mos ravishda 100% aniq qayta hisoblanadi (`shuffledOptions.indexOf(correctOptionText)`);
  - Asl `Quiz` obyekti va savollar master-to'plami o'zgarmas (`immutable`) qoladi;
  - Bitta quiz ichida hech bir savol takrorlanmaydi.
- **Guruhlar Mustaqilligi va Konkurrentlik**:
  - Har bir chat va guruh o'z alohida `QuizSession` nusxasiga ega;
  - Turli guruhlarda bir vaqtda boshlangan quizlar bir-biriga, ularning savollar tartibiga, ballariga yoki taymerlariga umuman ta'sir qilmaydi.
- **Guruh Buyruqlari va Guruh Havolalari**:
  - Guruhda ishlash buyruqlari: `/quiz_KK1_1`, `/quiz_KK1_2`, `/quiz_KK1_3`;
  - Guruhga qo'shish va boshlash uchun to'g'ridan-to'g'ri havolalar:
    - **KK1_1**: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK1_1` (yoki `https://t.me/jdakimyoquizbot?startgroup=KK1_1`)
    - **KK1_2**: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK1_2` (yoki `https://t.me/jdakimyoquizbot?startgroup=KK1_2`)
    - **KK1_3**: `https://t.me/jdakimyoquizbot?startgroup=quiz_KK1_3` (yoki `https://t.me/jdakimyoquizbot?startgroup=KK1_3`)
- **Shaxsiy Chat Cheklovi (`groupOnly: true`)**:
  - KK1 quizlari jamoaviy musobaqa bo'lgani sababli, shaxsiy chatda boshlanmaydi;
  - Agar foydalanuvchi shaxsiy chatda `/quiz_KK1_1`, `/quiz_KK1_2`, `/quiz_KK1_3` yoki ularning havolasini ochsa, bot tushunarli xabar beradi: *«Ushbu quiz faqat Telegram guruhlarida o'tkaziladi»* va guruhga qo'shish uchun tugma (`➕ Guruhga qo'shish va boshlash`) chiqaradi.
- **Mavjud Quizlar va /stop**:
  - Mavjud `amino_acids` (21 savol) va `kimyo_asoslari` (5 savol) quizlari to'liq o'z kuchida saqlandi;
  - `/stop` va `/stopquiz` buyruqlari guruhda admin tomonidan faol KK1 quizini ham to'xtata oladi.
- **Yaratilgan va o'zgartirilgan fayllar**:
  - `src/quiz/types.ts`: `Quiz` interfeysiga `groupOnly?: boolean` va `shuffle?: boolean` qo'shildi;
  - `src/quiz/kk1Questions.ts`: 60 ta savol 3 ta to'plamga (`kk1Quiz1`, `kk1Quiz2`, `kk1Quiz3`) ajratilgan holda yaratildi;
  - `src/quiz/questions.ts`: KK1 quizlari ro'yxatga olindi va `getQuizById` da `KK1_1`, `KK1_2`, `KK1_3` hamda mos sinonimlar qo'llab-quvvatlandi;
  - `src/quiz/quizManager.ts`: `shuffleArray` va `prepareSessionQuiz` funksiyalari yaratilib, `startQuiz` da dinamik aralashtirish va `correctOptionId` qayta hisoblash integratsiya qilindi;
  - `src/bot/handlers/quiz.ts`: `startQuizById` va obuna callbacklarida `groupOnly` guruh tekshiruvi qo'shildi;
  - `src/bot/handlers/start.ts`: Deep link parametrlarini (`?startgroup=KK1_1` va `?startgroup=quiz_KK1_1`) tanib olish kengaytirildi;
  - `test/kk1-quiz.test.ts`: Barcha talablar (aralashtirish, to'g'ri baholash, 20/20 ball aniqligi, groupOnly, parallel guruhlar, deep linking, stop) bo'yicha 9 ta to'liq test yozildi;
  - `package.json`: `npm test` ga `test/kk1-quiz.test.ts` ulandi.
- **Tekshiruv natijalari**:
  - `npm.cmd run build`: **Exit code 0** (Xatoliksiz kompilyatsiya bo'ldi);
  - `npm.cmd test`: **Exit code 0** (Barcha 6 ta test to'plami va 46 ta avtomatlashtirilgan test 100% muvaffaqiyatli o'tdi):
    - `test/index.test.ts`: 4/4 ✅
    - `test/quiz.test.ts`: 11/11 ✅
    - `test/e2e-simulation.test.ts`: 1/1 ✅
    - `test/multi-quiz.test.ts`: 10/10 ✅
    - `test/subscription.test.ts`: 11/11 ✅
    - `test/kk1-quiz.test.ts`: 9/9 ✅
- **Deploy cheklovi**: Foydalanuvchi talabi bo'yicha **deploy qilinmadi**. Barcha o'zgarishlar lokal tekshiruv uchun saqlandi. Maxfiy tokenlar yozilmadi.

---

## 8. Yakuniy Natija Xabariga Muallif, Manba va «Qayta yechish» Tugmalarining Qo‘shilishi

- **Test yaratuvchisi ko‘rsatilishi**:
  - Barcha quizlarning (`amino_acids`, `kimyo_asoslari`, `KK1_1`, `KK1_2`, `KK1_3`) yakuniy natija xabari tagiga doimiy bir xil shaklda qo‘shildi:
    `Test yaratuvchisi: <a href="https://t.me/diyorbek_jabborov">@diyorbek_jabborov</a>`
  - Foydalanuvchi profiliga bevosita bosib o‘tish imkoniyati ta'minlandi.
- **Savollar manbasi (`source`) va uning saqlanishi**:
  - `Quiz` interfeysiga `source?: string;` maydoni kiritildi (kelajakdagi testlar uchun mustaqil konfiguratsiya);
  - Faqat `KK1_1`, `KK1_2` va `KK1_3` uchun `source: "Bahora Nayimova slaydlaridan"` belgilandi va xabarda `Savollar manbasi: Bahora Nayimova slaydlaridan` ko'rinishida chiqadi;
  - **Manbasi noma'lum/yetishmaydigan eski quizlar (qayd)**:
    1. `amino_acids`: Faqat 17-jadval (329–330-betlar) ma'lumoti kiritilgan, kitob nomi va darslik muallifi dastlabki manbada keltirilmagan;
    2. `kimyo_asoslari`: Namunaviy savollar to‘plami bo‘lib, rasmiy manba ko‘rsatilmagan;
    - Shuning uchun bu ikkita eski quizda **Bahora Nayimova nomi aslo ko‘rsatilmaydi** (faqat test yaratuvchisi ko‘rsatiladi).
- **Ishtirokchi bo‘lmagan holat**:
  - Hech kim javob bermagan holatda ham (`leaderboard.length === 0`) yakuniy xabarda yaratuvchi, manba va ikkala harakat tugmasi to‘liq chiqishi ta'minlandi.
- **Natija xabari ostidagi ikkita tugma**:
  1. `📢 Quiz kodlari` → `https://t.me/jdaquizkod` (Kanalga o'tish URL tugmasi);
  2. `🔄 Qayta yechish` → `callback_data: restart_quiz_<quizId>` (Aynan shu quizni shu chatda qayta boshlash).
- **«🔄 Qayta yechish» tugmasi xavfsizligi va qoidalari**:
  - **Faqat guruh admini**: Guruhda oddiy foydalanuvchi tugmani bossa, xabar alert bilan rad etiladi: *«⚠️ Quizni faqat guruh adminlari qayta boshlashi mumkin»*;
  - **Boshqa faol quiz davom etayotganda bloklash**: Agar chatda allaqachon boshqa quiz davom etayotgan bo'lsa, ikkinchisi boshlanmaydi va alert beriladi: *«⚠️ Bu chatda allaqachon faol quiz davom etmoqda»*;
  - **Qayta aralashtirish**: Qayta boshlangan har safar `prepareSessionQuiz` ishga tushib, 20 ta savol va har bir savolning 4 ta varianti mustaqil yangidan aralashtiriladi va to‘g‘ri javob indeksi qayta hisoblanadi;
  - **Obuna talabi yo'qligi**: Guruhdagi admin va ishtirokchilar uchun kanal obunasi umuman talab qilinmaydi.
- **Yaratilgan va o'zgartirilgan fayllar**:
  - `src/quiz/types.ts`: `Quiz` ga `source?: string` qo'shildi;
  - `src/quiz/kk1Questions.ts`: `KK1_1`, `KK1_2`, `KK1_3` ga `source: "Bahora Nayimova slaydlaridan"` kiritildi;
  - `src/quiz/quizManager.ts`: `finishQuiz` ga profil havolasi, manba va ikkita tugma (`reply_markup`) qo'shildi (ishtirokchi bor va yo'q holatlar uchun);
  - `src/bot/handlers/quiz.ts`: `handleRestartQuizCallback` qo'shildi (admin tekshiruvi, faol quiz tekshiruvi, xavfsiz qayta boshlash);
  - `src/bot/bot.ts`: `restart_quiz_` callback hodisasi ulandi;
  - `test/kk1-quiz.test.ts`: Test 6 kengaytirildi, Test 10 (ishtirokchisiz holat), Test 11 (eski quizlarda Bahora Nayimova chiqmasligi), Test 12 (qayta yechish ruxsatlari, rad etish va aralashtirish) qo'shildi.
- **Kompilyatsiya va Test natijalari**:
  - `npm.cmd run build`: **Exit code 0** (Xatoliksiz kompilyatsiya bo'ldi);
  - `npm.cmd test`: **Exit code 0** (Barcha 6 ta to'plam va 49 ta avtomatlashtirilgan test 100% muvaffaqiyatli o'tdi):
    - `test/index.test.ts`: 4/4 ✅
    - `test/quiz.test.ts`: 11/11 ✅
    - `test/e2e-simulation.test.ts`: 1/1 ✅
    - `test/multi-quiz.test.ts`: 10/10 ✅
    - `test/subscription.test.ts`: 11/11 ✅
    - `test/kk1-quiz.test.ts`: 12/12 ✅ (Aralashtirish, baholash, yaratuvchi linki, manba, ishtirokchisiz holat, eski quizlar xavfsizligi, qayta yechish admin tekshiruvi).
- **Deploy cheklovi**: Foydalanuvchi ko'rsatmasiga asosan **deploy qilinmadi**. Barcha o'zgarishlar tekshiruv uchun lokal muhitda tayyor holatda saqlandi. Maxfiy tokenlar yozilmadi.

---

## 9. Barcha Quizlarning Shaxsiy Chatda Bloklanishi va Faqat Guruhlarga Cheklanishi

- **Talab mohiyati**:
  - Dastlab faqat KK1 quizlari (`KK1_1`, `KK1_2`, `KK1_3`) shaxsiy chatda bloklangan edi, biroq `amino_acids` va `kimyo_asoslari` shaxsiy chatda ishlashda davom etayotgan edi;
  - Foydalanuvchi ko'rsatmasiga asosan **botdagi barcha quizlar (hech qanday istisnosiz)** shaxsiy chatda boshlanishi butunlay taqiqlandi va faqat Telegram guruhlari bilan cheklandi;
  - Barcha quiz boshlash usullari:
    1. `/quiz_<ID>` yoki `/quiz <ID>` buyruqlari;
    2. Deep link havolalari (`?start=quiz_<ID>` yoki `?start=<ID>`);
    3. `🔄 Qayta yechish` (`restart_quiz_<quizId>`) tugmasi;
    4. Obunani tekshirish (`check_sub_<quizId>`) tugmasi orqali qayta boshlash;
    to'liq guruh formati bilan cheklandi.
- **Shaxsiy chatdagi harakatlar va xabarlar**:
  - Agar foydalanuvchi shaxsiy chatda biror quizni boshlashga urinsa (buyruq yoki havola orqali), unga guruhga o'tish xabari chiqariladi:
    `ℹ️ «${quiz.title}» faqat Telegram guruhlarida o'tkaziladi.`
    `Ushbu test jamoaviy musobaqa formatida tuzilgan bo'lib, uni faqat guruhlarda o'ynash mumkin.`
    va pastida inline tugma taqdim etiladi:
    `➕ Guruhga qo'shish va boshlash` (`url: https://t.me/<bot_username>?startgroup=quiz_<quizId>`);
  - `🔄 Qayta yechish` tugmasi shaxsiy chatda bosilsa:
    `ℹ️ Quizlar faqat Telegram guruhlarida o'tkaziladi.` alert ko'rsatiladi va hech qanday test boshlanmaydi;
  - `check_sub_<quizId>` tugmasi bosilganda:
    Obuna tasdiqlanadi va bevosita guruhga yo'naltirish xabari chiqariladi, shaxsiy chatda hech qanday poll yuborilmaydi.
- **Kanal obunasi va guruh qoidalari**:
  - Shaxsiy chatda `/start` yuborilganda ikki kanalga (`@jdaquizkod` va `@jdakimyouz`) majburiy a'zolik tekshirilishi saqlandi;
  - Guruhlarda kanal a'zoligi talabi umuman yo'q (admin quizni erkin boshlaydi, qatnashchilar javob beradi);
  - Guruhda quizni faqat guruh admini boshlashi, to'xtatishi va qayta yechishi mumkin.
- **O'zgartirilgan fayllar**:
  - `src/quiz/questions.ts`: `aminoAcidsQuiz` va `chemistryBasicsQuiz` ga `groupOnly: true` kiritildi (barcha 5 ta quiz endi `groupOnly: true`);
  - `src/bot/handlers/quiz.ts`: `startQuizById` da `!isGroup` bo'lsa darhol guruhga yo'naltirish xabari va `startgroup` havolasi berilishi ta'minlandi; keraksiz o'lik kodlar tozalandi;
  - `test/multi-quiz.test.ts`:
    - Test 5: Shaxsiy chatda `amino_acids` va `kimyo_asoslari` bloklanishi va guruhga yo'naltirish xabari tekshiruvi;
    - Test 6: Guruhda faol quiz paytida ikkinchisini boshlashni bloklash;
    - Test 7: Guruhda faqat admin `/stop` qila olishi va yakuniy reyting yuborilmasligi;
    - Test 8: Deep link shaxsiyda guruhga yo'naltirishi, guruhda admin orqali to'g'ri boshlanishi;
    - Test 9: Ikkita mustaqil guruhda parallel quizlar;
    - Test 10: Guruhda `/quiz_<ID>` regex buyrug'i orqali boshlash va shaxsiyda rad etilishi.
  - `test/subscription.test.ts`:
    - Test 1, Test 2, Test 3, Test 4 va Test 6 yangilandi; obuna tasdiqlangach shaxsiy chatda quiz boshlanmasligi, guruhga yo'naltirish xabari chiqishi va guruhda deep link obunasiz to'g'ridan-to'g'ri boshlanishi tasdiqlandi.
- **Kompilyatsiya va Test natijalari**:
  - `npm.cmd run build`: **Exit code 0** (Xatoliksiz kompilyatsiya bo'ldi);
  - `npm.cmd test`: **Exit code 0** (Barcha 6 ta to'plam va 49 ta test 100% muvaffaqiyatli o'tdi):
    - `test/index.test.ts`: 4/4 ✅
    - `test/quiz.test.ts`: 11/11 ✅
    - `test/e2e-simulation.test.ts`: 1/1 ✅
    - `test/multi-quiz.test.ts`: 10/10 ✅
    - `test/subscription.test.ts`: 11/11 ✅
    - `test/kk1-quiz.test.ts`: 12/12 ✅
- **Deploy holati**: Foydalanuvchining qat'iy ko'rsatmasiga binoan **deploy qilinmadi**. Barcha o'zgarishlar lokal muhitda tekshiruv uchun to'liq tayyor holatda turibdi. Maxfiy tokenlar yozilmadi.
