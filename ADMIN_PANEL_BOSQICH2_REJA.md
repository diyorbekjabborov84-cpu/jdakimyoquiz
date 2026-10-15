# Admin Panel Rivojlantirish Rejasi (3, 4, 5-Modullar va Google Direct Auth)

## Maqsad
Foydalanuvchi ko'rsatmasiga binoan quyidagi imkoniyatlarni kodga qo'shish (lekin deploy qilmaslik):
1. **Google orqali to'g'ridan-to'g'ri kirish**: `diyorbekjabborov84@gmail.com` uchun silliq, bir bosishda to'g'ridan-to'g'ri kirish.
2. **4-Modul: Umumiy xabarlar (Broadcast)**: Guruhlar yoki shaxsiy chatlarga matn, rasm va inline tugmali xabarlarni rate-limit bilan yuborish, yuborish tarixi.
3. **3-Modul: Natijalar va reyting (Results & Analytics)**: Guruhlar kesimida o'tkazilgan quizlar ro'yxati, filtrlash, sessiya bo'yicha to'liq ishtirokchilar reytingi.
4. **5-Modul: Sozlamalar va Audit tarixi (Settings & Audit Logs)**: Bot kanallari va parametrlarini ko'rish, admin harakatlari jurnali.

---

## 1. Google Direct Login
- `src/server/adminRoutes.ts` va `src/server/googleAuth.ts`:
  - `diyorbekjabborov84@gmail.com` tasdiqlanganda, agar `ADMIN_TELEGRAM_ID` bo'lmasa ham fail-closed bo'lmasdan, email orqali admin sessiyasi beriladi.
- `admin/lib/google-login.ts` va `admin/app/login/page.tsx`:
  - `prompt: "select_account"` olib tashlanadi (agar brauzerda akkaunt ochiq bo'lsa, avtomatik kiradi).
  - Google tugmasi birlamchi yirik dizaynda bo'ladi.

## 2. 4-Modul: Broadcast (Umumiy Xabarnoma)
- **Backend**:
  - `src/server/broadcastService.ts` yoki `src/server/adminRoutes.ts`:
    - `POST /admin/broadcast`:
      - Payload: `{ target: "all_groups" | "private_users" | "selected_groups", selectedChatIds?: number[], message: string, imageUrl?: string, buttons?: Array<{ text: string, url: string }> }`
      - Rate limiting: 50ms kechikish har bir yuborish orasida.
      - Error handling: Agar chat topilmasa yoki bot chiqarilgan bo'lsa (`kicked`), guruh statusini yangilash, navbatni to'xtatmaslik.
      - Audit logga va `broadcast_history` kolleksiyasiga yozish.
    - `GET /admin/broadcast/history`:
      - Yuborilgan xabarlar tarixi (sana, matn, target, muvaffaqiyatli/xato soni).
- **Frontend**:
  - `admin/app/broadcast/page.tsx`:
    - Auditoriya tanlash (Faol guruhlar, Shaxsiy foydalanuvchilar, Tanlangan guruhlar).
    - Jonli Telegram preview.
    - Tasdiqlash modali.
    - Yuborish progress holati.
    - O'tgan xabarlar tarixi jadvali.
  - BFF: `admin/app/api/broadcast/route.ts`, `admin/app/api/broadcast/history/route.ts`.

## 3. 3-Modul: Natijalar va Reyting (Results & Analytics)
- **Backend**:
  - `GET /admin/results`:
    - O'tkazilgan quizlar ro'yxati (`quiz_results` yoki `quiz_sessions` asosida), guruh nomi, test ID, qatnashuvchilar soni, 1-o'rin sohibi, sana.
    - Filtrlash: `quizId`, `chatId`, `days` (1, 7, 30).
  - `GET /admin/results/:sessionId`:
    - Muayyan sessiyaning barcha ishtirokchilari: o'rin, ism, `@username`, ball, to'liq savollar soni, sof vaqt (sekund), aniqlik foizi.
- **Frontend**:
  - `admin/app/results/page.tsx`:
    - Filtr paneli (Test tanlash, sana oralig'i, guruh qidirish).
    - O'tkazilgan quizlar jadvali.
    - Tafsilot modali (Leaderboard / Reyting jadvali).
  - BFF: `admin/app/api/results/route.ts`, `admin/app/api/results/[sessionId]/route.ts`.

## 4. 5-Modul: Sozlamalar va Audit (Settings & Audit Logs)
- **Backend**:
  - `GET /admin/settings`: Majburiy obuna kanallari, standart savol taymerlari, bot holati.
  - `GET /admin/audit-logs`: Admin harakatlari jurnali (`admin_audit_logs`).
  - `src/server/auditService.ts`: Admin amallarini (`recordAuditLog`) yozib borish.
- **Frontend**:
  - `admin/app/settings/page.tsx`:
    - Bot kanallari va sozlamalar kartochkasi.
    - Audit tarixi jadvali (Sana, Admin, Amal, Tafsilotlar).
  - BFF: `admin/app/api/settings/route.ts`, `admin/app/api/audit-logs/route.ts`.

## 5. Sinovlar va Tekshiruv
- Backend unit va integratsion testlari (`test/admin-modules.test.ts`).
- `npm test` va `npm run build`.
- `cd admin && npm run build`.
- Hech qanday git push yoki deploy qilinmaydi.
