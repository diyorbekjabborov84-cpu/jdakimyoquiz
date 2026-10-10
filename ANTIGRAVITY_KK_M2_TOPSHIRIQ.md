# Antigravity uchun topshiriq: KK_M2 quizlari

`KK_M2_QUIZ_SAVOLLAR.txt` faylidagi 60 ta savolni mavjud Telegram quiz botiga qo'shing. Kod yozish sizning vazifangiz; Codex tekshiradi va keyin deploy qiladi.

## Talablar

1. `KK2_1`, `KK2_2`, `KK2_3` IDlari bilan 3 ta alohida quiz yarating. Har birida TXT fayldagi tegishli 20 ta savol aynan bir martadan bo'lsin. Savol va variant matnlarini, to'g'ri javoblarni TXT faylga mos ko'chiring. `Slayd` va `Izoh` qatorlarini savol matniga qo'shmang; `Izoh`ni mavjud `explanation` maydoniga o'tkazish mumkin.
2. Mavjud `src/quiz/kk1Questions.ts` uslubiga amal qiling. Har savolda `timeLimitSeconds: 20`, har quizda `groupOnly: true`, `shuffle: true`, `source: "Bahora Nayimova slaydlaridan"` bo'lsin.
3. Yangi quizlarni `src/quiz/questions.ts` dagi `allQuizzes` ro'yxatiga ulang. Guruhda `/quiz_KK2_1`, `/quiz_KK2_2`, `/quiz_KK2_3` (va mavjud `/start_<ID>` shakli) ishlasin. Shaxsiy chatda quiz boshlanmasin; mavjud guruhga o'tish tugmasi ishlasin. Savollar va variantlar har sessiyada mustaqil aralashsin, to'g'ri javob indeksi mos ravishda qayta hisoblansin.
4. Mavjud pauza, davom ettirish, stop, Firestore saqlash, yakuniy reyting va tugmalar ishlashini saqlang. Shu funksiyalarni KK2 uchun alohida nusxalamang.
5. Faqat zarur hujjatlarni yangilang: yangi kodlar va 20 soniyalik vaqtni README'ga kiriting. Maxfiy kalitlar yoki `.env` faylini Git'ga qo'shmang.
6. `npm run build` va tegishli testlarni bajaring. Testlar uch to'plamning har birida 20 tadan savol, jami 60 ta noyob savol, 4 tadan variant, 0–3 oralig'idagi to'g'ri indeks, 20 soniyalik limit va registry orqali ID bilan topilishini tekshirsin.

Ish tugagach, `ANTIGRAVITY_HISOBOT.md` ga o'zgargan fayllar, test natijalari va qolgan muammolarni qisqa yozing. **GitHub'ga push qilmang va Render'ga deploy qilmang** — buni Codex tekshiruvdan keyin bajaradi.
