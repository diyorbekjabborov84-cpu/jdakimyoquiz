# Everest Mafia — Instagram reklama videosi

**Guruh:** [t.me/everest_mafia_uzbekiston](https://t.me/everest_mafia_uzbekiston)
**Format:** 9:16 (Reels/Stories) va 4:5 (Feed) · **Uzunlik:** 26.1 s · **Shrift:** Times New Roman (Tinos) · **Ovoz:** bitta erkak diktor (turkcha ohangli, oʻzbekcha matn) — 7 ta sahnaning hammasi shu ovozda

---

## 1. Tayyor fayllar

| Fayl | Vazifasi |
|---|---|
| `output/everest_mafia_9x16.mp4` | **Asosiy reklama** — Reels, Stories, bio havolasi. Ovozli. |
| `output/everest_mafia_9x16_muted.mp4` | Ovozsiz — Instagram'ning trend musiqasi bilan qoʻshish uchun. |
| `output/everest_mafia_4x5.mp4` | Feed (lenta) uchun 4:5 formatli reklama. |
| `output/everest_mafia_4x5_muted.mp4` | 4:5 ovozsiz variant. |
| `output/cover_9x16.jpg`, `output/cover_4x5.jpg` | Post uchun cover (CTA kadr). |
| `audio/vo_01..07.mp3` | Har bir sahnaning ovozi (alohida fayl). |
| `frames/*.jpg` | AI bilan generatsiya qilingan 5 ta asosiy kadr. |
| `fonts/Tinos-*.ttf` | Times New Roman metrikidagi shrift (OFL). |
| `render_video.py` | Fon kadrlarini + matn qatlamlarini (RGBA PNG) tayyorlaydi, `manifest.json` yozadi. |
| `build_video.py` | ffmpeg orqali videoni yigʻadi: kadr kesilishlari, matn animatsiyalari, effektlar, ovoz. |
| `build.sh` | Qisqa kirish nuqtasi (`bash build.sh 9x16`). |

---

## 2. Video ssenariy (kadrlar boʻyicha)

| # | Vaqt | Kadrlar | Ekran matni | Ovoz |
|---|---|---|---|---|
| 1 | 0.0–2.8 | Telefon ekranida yuz, qorongʻi xona | **TELEGRAMʼDA MAFA OʻYINI** → *OʻYINCHI BOʻL!* → Telegram guruhida, bot orqali oʻynang | «Telegram'da Everest Mafia o'yini!» |
| 2 | 2.8–6.3 | Doʻstlar stol atrofida → **kesilish** → telefon ekrani | **SIZ SHAHARDASIZ** → *DOʻSTLARINGIZ YONDAKI XONADA* → Ulardan biri — mafiya. Siz esa komissar. | «Do'stlarningiz yondaki xonada, siz esa shaharda.» |
| 3 | 6.3–12.0 | Ochilgan kartalar, lupa | **OʻYIN ROLLARI** → *ASOSIY ROLLAR — KIM SIZ?* → **Mafiya · Komissar · Tinch aholi · Doktor** (har biri alohida ochiladi) | «Asosiy rollar: mafiya, komissar, tinch aholi va doktor. Sizniki qaysi?» |
| 4 | 12.0–14.8 | Telefonda chat → **kesilish** → yuz | **FEIL** → *FAQAT FEILIN SOʻZLARI SIZNI OGOHLANTIRADI* → Har bir soʻz — dalil. Har bir dalil — gʻalaba. | «Faqat feilin so'zlari sizni ogohlantiradi.» |
| 5 | 14.8–18.7 | Qizil kart, shashka karta | **DALIL TOʻPLA** → *MAFIYANI USHLA* → Dalil toʻplab, mafiyani ushlang. | «Komissar bo'lsangiz, dalil to'plang va mafiyani ushlang.» |
| 6 | 18.7–22.1 | Doʻstlar xursand → **kesilish** → stol | **TUNDA YOKI KUNDA** → *GʻALABA SENING QOʻLINGDA* → Everest Mafia — har kuni yangi oʻyin | «Tunda yoki kunda yutish sizning qo'lingizda.» |
| 7 | 22.1–26.1 | Yuz + CTA | **EVEREST MAFIA** → tugma **HOZIR OʻYNASH** → `t.me/everest_mafia_uzbekiston` → Bot orqali oʻynang — bepul, oʻzbek tilida | «Hozir o'ynash uchun havola bio'da - Everest Mafia.» |

### Oʻyin qanday ishlaydi

Oʻyin **Telegram guruhida, bot orqali** oʻynaladi: guruhga kirasiz, bot ishlaydi, rollar va oʻyin bosqichlari bot orqali yuritiladi.

**Asosiy rollar** (video shu toʻrtta nomni koʻrsatadi): **Mafiya** (qatlom qiluvchi), **Komissar** (dalil toʻplaydigan), **Tinch aholi** (oddiy oʻyinchi) va **Doktor** (bir hayot saqlaydigan). Oʻyinda boshqa rollar ham bor — shuning uchun matnda «asosiy rollar» deyiladi, «faqat shu toʻrtta» emas. 3-sahnada rol nomlari ketma-ket ochiladi.

### Animatsiya tizimi

Har bir kadra va matn qatlami alohida animatsiyalanadi — montaj sekin emas, jonli:

- **Kadr harakati (Ken Burns):** har kadr yengilkin oldinga yoki orqaga zoʻmlanadi, qoʻshimcha yon siljish (sin/cos drift) bilan — surat «nafas oladi».
- **Kadr kesilishlari:** 2-sahna, 4-sahna va 6-sahnada bitta qism boshqa kadra bilan almashadi (oq chaqnash bilan) — montaj ritmi tezlashadi.
- **Matn ochilishi:** har bir qatlam (kicker → sarlavha → izoh) 0.45 s da ochiladi va 38 px yuqoriga suriladi; qatlamlar bosqichma-bosqich (kaskad) ochiladi.
- **Rolalar roʻyxati:** «Mafiya · Shahof · Tibbiyotchi» — har bir soʻz alohida ochiladi.
- **Qizil chiziq:** kicker ostidagi qizil lenta chapdan oʻnga «yopiladi» (wipe).
- **CTA nuri:** sarlavha ortasidagi qizil halqa sekin pulsatsiya qiladi.
- **Yorqinlik yugurishi:** kadr boʻylab yumshoq yorqinlik chizigʻi oʻtadi.
- **Oq chaqnash:** har bir kesilishda qisqa oq chaqnash (0.08 s).
- **Film doni (grain):** butun video boʻylab yumshoq pleyo grain — kinematik koʻrinish.
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

**C variant (bonus/CTA)**
```
🎭 Yangi oʻyinchilar uchun: birinchi oʻyinda 3 ta sovgʻa!

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
| 2 | Caption B + 4:5 formatli reklama | Feed'dan qayta ta'sir |
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

**Nimani oʻzgartirmoq mumkin:**

| Nima | Qayerda |
|---|---|
| Matn, kadrlar, sahnalar tuzilmasi | `render_video.py` → `SCENES` roʻyxati |
| Ovoz matnlari | `audio/vo_01..07.mp3` (har biri — bitta sahna) |
| Ovoz tezligi | `build_video.py` → `SPEED = "1.12"` (`1.0` tabiiy, `1.2` juda tez) |
| Sahnalar orasidagi jimlik | `build_video.py` → `GAP = 0.14` |
| Shrift | `render_video.py` → `SERIF*` (hozir Tinos = Times New Roman metrikidagi) |
| Film doni kuchi | `build_video.py` → `noise=alls=5` (0 = don yoʻq) |

**Ish tartibi:** `build_video.py` avval ovoz kliplarini tozalaydi va sahna davomiyliklarini oʻlchaydi, keyin `render_video.py` orqali matn qatlamlarini shu davomiyliklarga moslab joylashtiradi, soʻng ffmpeg bilan yigʻadi. Matn qatlamlarining ochilish vaqti shu sababdan ovoz bilan **avtomatik** mos keladi.

---

## 7. A/B test va optimizatsiya maslahatlari

| Element | A variant | B variant | Nimani tekshirish |
|---|---|---|---|
| Birinchi kadrdagi matn | «OʻYINCHI BOʻL!» | «Telegram'da MAFA oʻyini» | 3 soniyada toʻxtash (hold rate) |
| CTA | «HOZIR OʻYNASH» | «GURUHGA KIR» | Tugma bosilishi |
| Uzumlik | 22 s | 12 s (faqat 1, 2, 7-kadrlar) | Toʻliq koʻrish % |
| Musiqa | trend audio | trend suspense audio | Reach |
| Ovoz | ovozli variant | muted + trend audio | Konvertatsiya |

Koʻrsatkichlar: **Reach → 3-sekundagi qolish → profilga oʻtish → bio havolasi bosilishi → Telegram'da a'zolik.** Aynan shu zanjir boʻyicha A/B test qiling, har safar faqat bitta elementni oʻzgartiring.
