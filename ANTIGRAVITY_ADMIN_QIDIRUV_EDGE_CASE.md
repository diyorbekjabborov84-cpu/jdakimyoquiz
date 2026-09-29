# Antigravityga oxirgi qayta topshiriq — foydalanuvchi qidiruvidagi chegara holatlari

Codex kodni ko'rib chiqdi: mavjud testlar va buildlar o'tgan, ammo `src/tracking/tracker.ts` ning ikki maydonli (`usernameLower` + `nameLower`) qidiruvida hali ma'lumot yo'qotiladigan aniq holatlar bor. **Deploy qilma; faqat shu algoritmni va testlarini tuzat.**

## Tasdiqlangan mantiqiy xatolar

1. `usernameLower` bosqichida aynan `limit` (masalan 50) ta mos hujjat bo'lsa, `uSnap.docs.length > limit` false bo'ladi. Kod `items.length === limit` bilan `name` bosqichini bajarmaydi va `hasMore: false` qaytaradi. Agar ism bo'yicha yana 1 ta mos foydalanuvchi bo'lsa, u **umuman ko'rinmaydi**. Test: 50 ta faqat username mos + 1 ta faqat ism mos; birinchi sahifada 50, `hasMore=true`, keyingisida 1 bo'lishi shart.
2. `name` bosqichida `limit(remainingLimit + 25)` olinadi. Agar shu oynadagi 25+ yozuv username bosqichida allaqachon chiqarilgan bo'lsa, dublikatlar chiqarib tashlangach to'liq sahifa to'lmaydi. `nSnap.docs.length > remainingLimit` noto'g'ri `hasMore=true` deb belgilaydi, hatto qolgan unikal mos foydalanuvchi bo'lmasa ham. Dublikatlar juda ko'p bo'lganda ketma-ket bo'sh sahifalar paydo bo'lishi yoki davom cursorining yurishi qiyinlashadi. Usernamega ham ismga ham mos 100+ hujjat va keyin faqat ismga mos hujjatlar bilan tekshir. Har sahifada unikal yozuvlar bo'lsin, yo'qotish va takror bo'lmasin, oxirgi sahifada `hasMore=false` bo'lsin.
3. Cursor yaratishda `data.userId` va `data.chatId` ishlatilmoqda, ammo `orderBy("__name__")` Firestore **hujjat IDsi** bo'yicha saralaydi. Ma'lumotdagi ID hujjat IDsi bilan farq qilsa cursor noto'g'ri bo'ladi. Cursorni oxirgi haqiqiy `doc.id` dan tuzing; guruh ro'yxati, guruh qidiruvi, foydalanuvchi ro'yxati va qidiruvining barcha yo'llarida.

## UI kichik xato

`admin/app/groups/page.tsx` va `users/page.tsx` da qidiruv matni o'zgargandan keyin eski so'rov faqat 300 ms o'tgach bekor qilinadi. Shu vaqt ichida eski javob yangisini ustidan yozishi mumkin. `handleSearchChange` paytidayoq eski so'rovni abort qiling, `searchSeqRef` ni oshiring, eski satrlar va cursorni tozalang; 300 ms debounce yangi so'rov uchun qolsin.

## Tekshiruv va topshirish

- Yuqoridagi har bir holatga mock Firestore bilan alohida regressiya testi qo'sh; testlar haqiqiy Firestore'ga yozmasin. Mock `__name__` + cursor tartibini real Firestore semantikasiga yaqin tekshirsin.
- `npm test`, root TypeScript build va `admin/` Next.js build o'tsin.
- `ANTIGRAVITY_HISOBOT.md` ga tuzatish va test natijasini yoz. Git push, Render/Vercel deploy qilma. Tugagach Codex tekshirsin.
