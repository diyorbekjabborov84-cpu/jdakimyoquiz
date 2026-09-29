# Antigravityga topshiriq — admin panel qidiruvi va sahifalashni yakunlash

Codex qayta topshiriqni tekshirdi. Auth va Firestore bo'yicha asosiy tuzatishlar qabul qilindi. **Hali deploy qilma.** Quyidagi qolgan xatolarni shu 1-bosqichda tuzat, keyin hisobot ber.

Codex kichik xatolarni allaqachon tuzatdi: `admin/app/api/groups/route.ts` va `admin/app/api/users/route.ts` endi `cursor`ni Render API'ga uzatadi; `admin/lib/csrf.ts` Origin ham, Referer ham yo'q POST so'rovini rad etadi. Ularni saqla.

## Qolgan xatolar

1. `src/tracking/tracker.ts` ning guruh nomi va foydalanuvchi ism/username prefix qidiruvi `limit(50)` bilan tugaydi va har doim `nextCursor: null` qaytaradi. 51- va undan keyingi mos yozuvlar ko'rinmaydi. Qidiruv natijasida ham cursorli sahifalashni ishlat. Foydalanuvchilarning ikki maydonli qidiruvida takroriy hujjatlarni olib tashlash, sahifalar orasida takror va o'tkazib yuborishni oldini olish zarur. Qidiruv uchun `total` butun kolleksiya soni emas, mos keladigan yozuvlar soni bo'lsin; agar buni samarali hisoblab bo'lmasa, API/UI uni `total` deb ko'rsatmasin va `hasMore` bilan ishlasin.
2. Oddiy ro'yxat cursori faqat `lastActivity` qiymatidir. Bir nechta hujjatning vaqti bir xil bo'lsa, `startAfter(cursor)` ayrimlarini tashlab ketishi yoki takrorlashi mumkin. `lastActivity` + document ID (yoki Firestore `DocumentSnapshot`) bilan barqaror tartib va cursor yarating. Cursorni xavfsiz parse/validate qiling; noto'g'ri cursor uchun 400 javob qaytaring. Sahifa mavjudligini `limit + 1` yozuv bilan aniqlang, aynan 50 ta qolganida keraksiz "Keyingi sahifa" tugmasi chiqmasin.
3. `admin/app/groups/page.tsx` va `admin/app/users/page.tsx` har bir harf kiritilganda alohida so'rov yuboradi. Eski so'rov keyinroq tugasa, yangi qidiruv natijasini ustidan yozadi. Debounce (masalan 250–350 ms) va `AbortController` yoki request sequence bilan eskirgan javoblarni e'tiborsiz qoldiring. Qidiruv o'zgarganda eski satrlar va cursorni tozalang. Sahifa yuklashda takror bosishni cheklang.
4. Testda mock Firestore haqiqiy query/cursor semantikasiga yaqin bo'lsin. Kamida 60 ta bir xil prefixga mos guruh, 60 ta username/ismga mos foydalanuvchi, bir xil `lastActivity`li yozuvlar, 50 tadan aynan teng sahifa va noto'g'ri cursor holatini tekshir. Next BFF route'lari `cursor`ni Renderga yuborishini ham maqsadli test bilan tekshir. Testlar production Firestore'ga yozmasin.

Bot va `admin/` buildlari, tegishli testlar o'tsin. `ANTIGRAVITY_HISOBOT.md` oxiriga o'zgarishlar va test dalillarini qo'sh. Git commit/push va Render/Vercel deploy qilma. Tugagach Codex tekshirsin.
