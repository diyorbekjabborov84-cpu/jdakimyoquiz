# Everest Mafia — Instagram reklama videosi

**Guruh:** [t.me/everest_mafia_uzbekiston](https://t.me/everest_mafia_uzbekiston)
**Format:** 9:16 (Reels/Stories) va 4:5 (Feed) · **Uzunlik:** 22.4 s · **Ovoz:** oʻzbekcha matn, 1.12x tezlashtirilgan

---

## 1. Tayyor fayllar

| Fayl | Vazifasi |
|---|---|
| `output/everest_mafia_9x16.mp4` | **Asosiy reklama** — Reels, Stories, bio'dagi havola. Ovozli. |
| `output/everest_mafia_9x16_muted.mp4` | Ovozsiz variant — Instagram'ning trend musiqasi bilan qoʻshish uchun. |
| `output/everest_mafia_4x5.mp4` | Feed (lenta) uchun 4:5 formatli reklama. |
| `output/everest_mafia_4x5_muted.mp4` | 4:5 ovozsiz variant. |
| `output/cover_9x16.jpg`, `output/cover_4x5.jpg` | Post uchun cover (CTA kadr). |
| `audio/vo_01..07.mp3` | Sahna matnlari (har biri alohida). |
| `frames/*.jpg` | AI bilan generatsiya qilingan 5 ta asosiy kadr. |
| `render_video.py` | Matnni kadrlar ustiga joylashtiradi (Pillow). |
| `build.sh` | Butun videoni ffmpeg bilan yigʻadi. |

---

## 2. Video ssenariy (kadrlar boʻyicha)

| # | Vaqt | Kadrlar | Ekran matni | Ovoz (sahna matni) |
|---|---|---|---|---|
| 1 | 0.0–2.7 | Telefon ekranida yuz, qorongʻi xona | **TELEGRAMʼDA MAFA OʻYINI** → *OʻYINCHI BOʻL!* → Oʻzbek tilidagi haqiqiy mafiya oʻyini | «Telegram'da Everest Mafia o'yini!» |
| 2 | 2.7–6.1 | Doʻstlar stol atrofida kartalar bilan | **SIZ SHAHARDASIZ** → *DOʻSTLARINGIZ YONDAKI XONADA* → Ulardan biri — mafiya. Siz esa shahof. | «Do'stlaringiz yondaki xonada, siz esa shaharda.» |
| 3 | 6.1–8.1 | Ochilgan kartalar, lupa | **ROLLAR** → *KIM MAFIYA, KIM SHAHOF?* → Mafiya · Shahof · Tibbiyotchi | «Kim mafiya, kim shahof?» |
| 4 | 8.1–11.0 | Telefonda chat (bokeh) | **FEIL** → *FAQAT FEILIN SOʻZLARI SIZNI OGOHLANTIRADI* → Har bir soʻz — dalil. Har bir dalil — gʻalaba. | «Faqat feilin so'zlari sizni ogohlantiradi.» |
| 5 | 11.0–15.4 | Qizil kart, shashka karta | **DALIL TOʻPLA** → *MAFIYANI USHLA* → Shahof boʻlsangiz — shaharda yutasaniz | «Shahof bo'lsangiz, dalil to'plang va mafiyani ushlang.» |
| 6 | 15.4–18.6 | Doʻstlar telefon atrofida xursand | **TUNDA YOKI KUNDA** → *GʻALABA SENING QOʻLINGDA* → Everest Mafia — har kuni yangi oʻyin | «Tunda yoki kunda yutish sizning qo'lingizda.» |
| 7 | 18.6–22.4 | Yuz + CTA | **EVEREST MAFIA** → tugma **HOZIR OʻYNASH** → `t.me/everest_mafia_uzbekiston` → Telegramʼda — bepul va oʻzbek tilida | «Hozir o'ynash uchun havola bio'da — Everest Mafia.» |

**Montaj qoidalari:** har sahna oʻz ovozi bilan boshlanadi; kadrlar orasida 0.3 s qora «cut»; har bir kadra yengilkin (Ken Burns) zoom qilinadi — push-in / pull-out navbatma; matnlar pastdan yuqoriga «safe zone» ichida (Reels UI tegilmaydi).

---

## 3. Instagram caption (3 ta variant)

**A variant (savol bilan — izohlarni kuchaytiradi)**
```
Siz shaharda. Doʻstlaringiz esa yondaki xonada. 🃏

Kim mafiya, kim shahof? Qaysi biri xiyonat qiladi?

Telegramʼdagi Everest Mafia — oʻzbek tilidagi mafiya oʻyini.
🔗 Bioʼdagi havolaga oʻting

#mafia #mafiaoyini #mafiauzbekiston #everestmafia
```

**B variant (qisqa va shiddiy)**
```
Tunda yoki kunda — yutish sizning qoʻlingizda. 🔦

Everest Mafia: faqat feilin soʻzlari sizni ogohlantiradi.
→ Bioʼdagi havolaga oʻting

#mafia #tgoyin #mafiauzbekistan #uzbekcha
```

**C variant (bonus/CTA)**
```
🎭 Yangi oʻyinchilar uchun: birinchi oʻyinda 3 ta sovgʻa!

Everest Mafia — t.me/everest_mafia_uzbekiston
```

> Eslatma: faqat haqiqatga toʻgʻri keladigan va'dalarni yozing (masalan «bepul», «oʻzbek tilida»). Reyting yoki oʻyinchi sonini tasdiqlanmagan holda yozmang.

**Tavsiya etilgan hashtaglar:**
`#mafia #mafiaoyini #mafiauzbekiston #everestmafia #tgoyin #uzbekcha #telefonoyin #mafiao` (8–12 ta, katta yoki nisbiy yiriklar bilan aralashtiring: `#mafia` + `#uzbekistan` + `#telegram`).

---

## 4. Joylashuv (post qilishdan oldin)

1. **Bio havolasi:** Instagram → Profil → tahrirlash → havolalar → `https://t.me/everest_mafia_uzbekiston`.
2. **Yashirilgan izoh** (birinchi 60 soniya ichida yozish eng samarali):
   `Havoqa oʻtish uchun bioʼdagi havolani bosing 👆`
3. **Cover:** `output/cover_9x16.jpg` — postga cover tanlashda yuklang.
4. **Story qayta tarqatish:** reklama yigʻilgan zahoti Stories'ga ham joylang (badge «Reel» bilan), bio havolasi ochiq boʻlsin.

---

## 5. 7 kunlik post rejasi

| Kun | Kontent | Maqsad |
|---|---|---|
| 1 | Asosiy reklama (9:16, ovozli) | Birinchi auditoriya, asosiy trafik |
| 2 | Caption B + 4x5 formatli reklama | Feed'dan qayta ta'sir |
| 3 | Savol: «Siz shahof boʻlardim yoki mafiya?» (Story + rasm) | Izohlar va DM'lar |
| 4 | Ovozsiz video (trend musiqasi bilan) | Yangi auditoriya |
| 5 | «Mafiya oʻyini qanday oʻyniladi?» — 3 kadrlik qisqa video | Savol-javob, obyektiv |
| 6 | Guruhdan ichki boʻlak (skrin/video) + «hamkorlarimiz» | Ishonch (social proof) |
| 7 | CTA takror: «Bugungi kechqurun oʻyinni boshlaymiz» | Konvertatsiya |

Har bir postga **bir xil bio havolasi** va bir xil brend (yuqorida `EVEREST MAFIA`) — bu CTA ni kuchaytiradi.

---

## 6. Video qayta yigʻish (build)

```bash
cd reklama/everest-mafia
bash build.sh 9x16     # Reels/Stories versiyasi
bash build.sh 4x5      # Feed versiyasi
```

Talablar: `ffmpeg` (imageio-ffmpeg orqali), Python 3 + `Pillow`.

- Matnni oʻzgartirmoq uchun: `render_video.py` ichidagi `SCENES` roʻyxatini tahrirlang, keyin `build.sh` ni qayta ishga tushiring.
- Ovozni oʻzgartirmoq uchun: `audio/vo_01..07.mp3` fayllarini yangilang (har biri — bitta sahna matni).
- Ovoz tezligi: `build.sh` ichidagi `atempo=1.12`; `1.0` — tabiiy, `1.2` — ancha tez.

---

## 7. A/B test va optimizatsiya maslahatlari

| Element | A variant | B variant | Nimani tekshirish |
|---|---|---|---|
| Birinchi kadrdagi matn | «OʻYINCHI BOʻL!» | «Telegram'da MAFA oʻyini» | 3 soniyada toʻxtash (hold rate) |
| CTA | «HOZIR OʻYNASH» | «GURUHGA KIR» | Tugma bosilishi |
| Uzumlik | 22 s | 12 s (faqat 1, 2, 7-kadrlar) | Toʻliq koʻrish % |
| Musiqa | trend audio | trend suspense audio | Reach |

Koʻrsatkichlar: **Reach → 3-sekundagi qolish → profilga oʻtish → bio havolasi bosilishi → Telegram'da a'zolik.** Aynan shu zanjir boʻyicha A/B test qiling, har safar faqat bitta elementni oʻzgartiring.
