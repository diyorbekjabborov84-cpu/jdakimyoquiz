# Everest Mafia — Instagram reklama videosi

**Guruh:** [t.me/everest_mafia_uzbekiston](https://t.me/everest_mafia_uzbekiston)
**Format:** 9:16 (Reels/Stories) va 4:5 (Feed) · **Uzunlik:** 34.8 s · **Sahna:** 8 ta, 18 ta kesish
**Shrift:** Times New Roman (Tinos) · **Ovoz:** bitta erkak diktor (turkcha ohang, oʻzbekcha matn)

Uslub: **noir / kinematik** — qorongʻi shahar, tungi sud, mafiya yurishi. Matn umumiy reklamalar emas, balki shaharga oid dramatik gaplar bilan yozilgan.

---

## 1. Tayyor fayllar

| Fayl | Vazifasi |
|---|---|
| `output/everest_mafia_9x16.mp4` | **Asosiy reklama** — Reels, Stories, bio havolasi. Ovozli. |
| `output/everest_mafia_9x16_muted.mp4` | Ovozsiz — Instagram'ning trend musiqasi bilan qoʻshish uchun. |
| `output/everest_mafia_4x5.mp4` | Feed (lenta) uchun 4:5 formatli reklama. |
| `output/everest_mafia_4x5_muted.mp4` | 4:5 ovozsiz variant. |
| `output/cover_9x16.jpg`, `output/cover_4x5.jpg` | Post uchun cover (CTA kadr). |
| `audio/vo_01..08.mp3` | Har bir sahnaning ovozi (8 ta alohida fayl). |
| `frames/*.jpg` | 10 ta kadr: 5 ta eski + 5 ta yangi (shahar tungi, mafiya yurishi, sud spotlighti, doktor, olchoz). |
| `fonts/Tinos-*.ttf` | Times New Roman metrikidagi shrift (OFL). |
| `render_video.py` | Fon kadrlarini + matn qatlamlarini (RGBA PNG) tayyorlaydi, `manifest.json` yozadi. |
| `build_video.py` | ffmpeg orqali videoni yigʻadi: kesishlar, kamera effektlari, matn animatsiyalari, ovoz. |
| `build.sh` | Qisqa kirish nuqtasi (`bash build.sh 9x16`). |

---

## 2. Ssenariy (8 sahna, 18 kesish)

| # | Vaqt | Kadrlar (kesilishlar) | Ekran matni | Ovoz |
|---|---|---|---|---|
| 1 | 0.0–3.2 | Tungi shahar → yuz | **SHAHARDA KECH QORAYDI** → *SHAHAR TINCH EMAS* → Tunda mafialar oʻz yurishiga chiqadi | «Shaharda kech qoraydi. Shahar tinch emas.» |
| 2 | 3.2–6.9 | Mafiyalar yurishi → kartalar (tebranish) → telefon | **MAFIYALAR** → *OʻZ YURISHLARI UCHUN TUNNI KUTMOQDA* → Ular uchun tun — ish vaqti | «Mafialar shaharda o'z yurishlari uchun tunni kutmoqda.» |
| 3 | 6.9–10.7 | Sud spotlighti → kartalar (zoom snap) | **KOMISSAR** → *TUNGI SUDNI ADOLATLI QILISHGA VAʼDA BERDI* → U faqat dalil toʻplaydi | «Komissar tungi sudni adolatli qilishga va'da berdi.» |
| 4 | 10.7–16.9 | Kartalar → doʻstlar → olchoz | **ASOSIY ROLLAR** → *TOʻRT TA ROL — KIM SIZ?* → **Mafiya · Komissar · Tinch aholi · Doktor** (ketma-ket ochiladi) | «To'rt asosiy rol bor: mafiya, komissar, tinch aholi va doktor. Sizniki qaysi?» |
| 5 | 16.9–20.3 | Doktor stoli → telefon (zoom snap) | **DOKTOR** → *BIR HAYOT SAQLAYDI* → Yoki yoʻqotadi | «Doktor bir hayot saqlaydi. Yoki yo'qotadi.» |
| 6 | 20.3–23.8 | Olchoz → doʻstlar | **TINCH AHOLI** → *HECH NARSA BILMAYDI* → Bilmasligi — omil | «Tinch aholi hech narsani bilmaydi. Ehtimol.» |
| 7 | 23.8–27.4 | Telefon (chat) → yuz (tebranish) | **OʻYIN** → *FAQAT FEILIN SOʻZLARI SIZNI OGOHLANTIRADI* → Har bir soʻz — dalil | «Faqat feilin so'zlari sizni ogohlantiradi.» |
| 8 | 27.4–34.8 | Mafiya stol → telefon (yuz) + CTA | **TUN YOKI KUN — GʻALABA SIZNIKI** → *EVEREST MAFIA* → tugma **HOZIR OʻYNASH** → `t.me/everest_mafia_uzbekiston` → Bot orqali oʻynang — bepul, oʻzbek tilida | «Tunda yoki kunda yutish sizning qo'lingizda. Hozir o'ynash uchun havola bio'da - Everest Mafia.» |

### Oʻyin rollari

Oʻyin **Telegram guruhida, bot orqali** oʻynaladi. Asosiy rollar: **Mafiya** (qatlom qiluvchi), **Komissar** (dalil toʻplaydigan), **Tinch aholi** (oddiy oʻyinchi) va **Doktor** (bir hayot saqlaydigan). Oʻyinda boshqa rollar ham bor — shuning uchun matnda «asosiy rollar» deyiladi, «faqat shu toʻrtta» emas.

### Animatsiya tizimi

- **18 ta kesish, oʻrtacha 1.9 s/kadr** — montaj ritmi tez, koʻz bir joyda turmaydi.
- **Kamera harakati 4 xil:** `in` (sekin ichkariga), `out` (sekin tashqariga), `burst` (1.34 → 1.0 tez zoom "snap" + qisqa kontrast/rang "punch"), `shake` (kamera tebranishi).
- **Kesish effekti:** har bir kesishda iliq chaqnash (light-leak) — 0.06 s.
- **Matn ochilishi:** qatlamlar 0.3 s da ochiladi, 30 px yuqoriga suriladi va 0.94 → 1.0 masshtab bilan "pop" qiladi; qatlamlar kaskad holda ochiladi.
- **Rolalar roʻyxati:** «Mafiya · Komissar · Tinch aholi · Doktor» — har bir soʻz alohida ochiladi.
- **Qizil lenta:** kicker ostida chapdan oʻnga wipe.
- **CTA nuri:** sarlavha ortasidagi qizil halqa sekin pulsatsiya qiladi.
- **Yorqinlik yugurishi:** kadr boʻylab yumshoq yorqinlik chizigʻi.
- **Film doni (grain):** butun video boʻylab kinematik pleyo doni.
- **Vinyetka va gradient:** matn oʻqilishi uchun pastga qoraytirilgan gradient.

---

## 3. Instagram caption (3 ta variant)

**A variant (savol bilan — izohlarni kuchaytiradi)**
```
Siz shaharda. Doʻstlaringiz esa yondaki xonada. 🃏

Mafiya, komissar, tinch aholi yoki doktor — sizniki qaysi rol?

Everest Mafia — Telegram guruhida, bot orqali oʻynaladigan mafiya oʻyini.
🔗 Bioʼdagi havolaga oʻting

#mafia #mafiaoyini #mafiauzbekiston #everestmafia
```

**B variant (qisqa va shiddiy)**
```
Tunda yoki kunda — yutish sizning qoʻlingizda. 🔦

Telegram guruhida, bot orqali oʻynang. Faqat feilin soʻzlari sizni ogohlantiradi.
→ Bioʼdagi havolaga oʻting

#mafia #tgoyin #mafiauzbekistan #uzbekcha
```

**C variant (shoʻr replikasi)**
```
«Komissar tungi sudni adolatli qilishga vaʼda berdi.»

Mafialar esa shaharda oʻz yurishlari uchun tunni kutmoqda. 🎭

Everest Mafia — t.me/everest_mafia_uzbekiston
```

> Eslatma: faqat haqiqatga toʻgʻri keladigan vaʼdalarni yozing (masalan «bepul», «oʻzbek tilida»). Reyting yoki oʻyinchi sonini tasdiqlanmagan holda yozmang.

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
| 2 | Caption C (shoʻr replikasi) + 4:5 formatli reklama | Feed'dan qayta ta'sir |
| 3 | Savol: «Siz komissar boʻlardim yoki mafiya?» (Story + rasm) | Izohlar va DM'lar |
| 4 | Ovozsiz video (trend musiqasi bilan) | Yangi auditoriya |
| 5 | «Mafia oʻyini qanday oʻyniladi?» — 3 kadrlik qisqa video | Savol-javob, obyektiv |
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

**Nimani oʻzgartirmoq mumkin:**

| Nima | Qayerda |
|---|---|
| Matn, kadrlar, sahnalar tuzilmasi | `render_video.py` → `SCENES` roʻyxati |
| Ovoz matnlari | `audio/vo_01..08.mp3` (har biri — bitta sahna) |
| Ovoz tezligi | `build_video.py` → `SPEED = "1.12"` (`1.0` tabiiy, `1.2` juda tez) |
| Sahnalar orasidagi jimlik | `build_video.py` → `GAP = 0.14` |
| Shrift | `render_video.py` → `SERIF*` (hozir Tinos = Times New Roman metrikidagi) |
| Film doni kuchi | `build_video.py` → `noise=alls=5` (0 = don yoʻq) |
| Kesish chaqnashi | `build_video.py` → `build_part()` ichidagi `color`/`fade_in` |

**Ish tartibi:** `build_video.py` avval ovoz kliplarini tozalaydi va sahna davomiyliklarini oʻlchaydi, keyin `render_video.py` orqali matn qatlamlarini shu davomiyliklarga moslab joylashtiradi, soʻng ffmpeg bilan yigʻadi. Matn qatlamlarining ochilish vaqti shu sababdan ovoz bilan **avtomatik** mos keladi.

**Sahnaga yangi qism (kesish) qoʻshish:** `SCENES` ichidagi `parts=[(img, ulush, harakat), ...]` — `ulush` kadrga boʻlinadigan vaqt nisbatini, `harakat` esa `in` / `out` / `burst` / `shake` ni belgilaydi. Yangi kadr qo'shish uchun avval `frames/` ga rasm tushiring.

---

## 7. A/B test va optimizatsiya maslahatlari

| Element | A variant | B variant | Nimani tekshirish |
|---|---|---|---|
| Birinchi kadrdagi matn | «SHAHAR TINCH EMAS» | «OʻYINCHI BOʻL!» | 3 soniyada toʻxtash (hold rate) |
| CTA | «HOZIR OʻYNASH» | «GURUHGA KIR» | Tugma bosilishi |
| Uzumlik | 35 s (toʻliq) | 18 s (faqat 1, 3, 8-kadrlar) | Toʻliq koʻrish % |
| Musiqa | trend audio | trend suspense audio | Reach |
| Ovoz | ovozli variant | muted + trend audio | Konvertatsiya |

Koʻrsatkichlar: **Reach → 3-sekundagi qolish → profilga oʻtish → bio havolasi bosilishi → Telegram'da a'zolik.** Aynan shu zanjir boʻyicha A/B test qiling, har safar faqat bitta elementni oʻzgartiring.
