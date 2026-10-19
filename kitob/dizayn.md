# NOORGANIK KISLOTALAR — Kitob dizayni konsepsiyasi (taklif)

> Tasdiqlangandan keyin `qurilma/build_docx.py` ga kod sifatida o'tkaziladi.

## 1. Umumiy g'oya
**Ilmiy, toza, ishonchli.** Oq fonda chuqur ko'k + bronza aksentlari. Har bir sahifa — darslik emas, laboratoriya jurnali va ilmiy atlas aralashmasi.

### Rang palitrasi
| Rol | Rang | Kod | Qaerda ishlatiladi |
|---|---|---|---|
| Asosiy ko'k | Chuqur dengiz ko'ki | `#0B2C4A` | Muqova, bob sarlavhalari, jadvallar sarlavhasi |
| Aksent | Bronza / oltin | `#C28E3B` | Raqamlar, chiziqlar, muhim bloklar |
| Yordamchi | Och ko'k-kulrang | `#E8F0F6` | Jadval fonlari, eslatma bloklari |
| Ogohlantirish | To'q qizil | `#8B1A1A` | Diqqat, xavfsizlik bloklari |
| Matn | Grafit | `#1A1A1A` | Asosiy matn |
| Izoh | Kulrang | `#5A5A5A` | Rasm osti, manba izohlari |

### Shriftlar (Word da mavjud, o'rnatish shart emas)
- **Sarlavhalar:** Cambria / Times New Roman, qalin (Bold), ko'k rang
- **Asosiy matn:** Times New Roman 11 pt, qator oralig'i 1.15
- **Formulalar:** Cambria Math, markazda, raqami o'ngda `(1.3)`
- **Jadvallar:** Calibri 9.5 pt, ixcham
- **Kod / misol:** Consolas 9 pt

### Sahifa
- O'lcham: A4, hoshiyalar 2 sm (ichki 2.5 sm tikish uchun)
- Kolontitul: yuqorida — bob nomi (kulrang, 8 pt), pastda — sahifa raqami (o'rtada, bronza chiziq ustida)
- Har bob yangi sahifadan boshlanadi, bob raqami katta (48 pt, och kulrang watermark uslubida)

## 2. Muqova (3 ta variant — tanlang)

**Variant A — «Laboratoriya» (tavsiya):**
Oq fonda markazda H₂SO₄ tetraedr modeli (3D, yarim shaffof), orqada xira davriy jadval fragmenti. Yuqorida seriya chizig'i (bronza), pastda muallif. Orqa muqovada anotatsiya + 3 ta ikonka (nazariya / tajriba / sanoat).

**Variant B — «Sanoat»:**
To'q ko'k fonda oq chiziqli zavod blok-sxemasi (kontakt apparati kesimi). Sarlavha oq, aksent bronza.

**Variant C — «Minimal ilmiy»:**
Toza oq, faqat tipografika: katta sarlavha, ingichka bronza chiziqlar, kichik molekula piktogrammalari burchaklarda.

> Siz bittasini tanlaysiz, qolganini moslashtiraman. Hozir A ni asos qilib olaman.

## 3. Ichki elementlar dizayni

### Bob kirishi
Har bob boshida:
- Katta bob raqami (masalan `01` — 48 pt, #E8F0F6 rangda)
- Sarlavha (18 pt, #0B2C4A, Bold)
- Taglavha / epigraf (italic, kulrang, chap chiziq bilan)
- «Ushbu bobda o'rganasiz» — 4–6 punktli ko'k ramkali blok (och ko'k fon #E8F0F6, chapda qalin ko'k chiziq)

### Formulalar
- Blokli: markazda, raqami o'ngda `(bob.formula)` — masalan `(4.2)`
- Inline: matn ichida, subscript/superscript Word formatida (H₂SO₄, SO₄²⁻, Eₐ)

### Jadvallar
- Sarlavha yuqorida: **1.2-jadval. Nomi** (10 pt, Bold, ko'k, markazda)
- Bosh qator: to'q ko'k fon (#0B2C4A), oq matn, Bold
- Qolgan qatorlar: juft qatorlar och ko'k fon (#E8F0F6) — zebra
- Chegaralar: faqat gorizontal, ingichka (0.5 pt, #0B2C4A)

### Rasmlar / chizmalar / grafiklar
- Markazda, 85% eni
- Ostida: **1.3-rasm. Nomi** (10 pt, kulrang, markazda, italic)
- Har rasmda manba izohi (agar kerak bo'lsa): 7 pt kulrang
- Turlari:
  - **Tuzilish sxemalari:** oq fonda, ko'k bog'lar, qizil kislorod, sariq oltingugurt
  - **Grafiklar:** toza chiziqli, ko'k/bронза ranglarda, panjara och kulrang
  - **Blok-sxemalar:** yumaloq burchakli to'rtburchaklar, strelkalar bronza
  - **3D modellar:** oq fon, yumshoq soya

### Maxsus bloklar
```
> [!NOTE]      → Eslatma (ko'k, ℹ️, och ko'k fon)
> [!IMPORTANT] → Muhim (bronza, ⭐, och sariq fon)
> [!TIP]       → Maslahat (yashil, 💡)
> [!WARNING]  → Diqqat (qizil, ⚠️, och qizil fon)
> [!EXAMPLE]  → Misol (kulrang, och kulrang fon, chap chiziq)
```

### Mashqlar
- Har bir topshiriq: **1.1-masala.** qalin, keyin matn
- Test variantlari: A) B) C) D) — osilgan indent, Variant uslubida
- Javoblar ilovada — bobda faqat savol

### Xulosa
- Ko'k ramkali blok, ichida 6–8 punkt (har punkt boshida bronza nuqta •)
- Pastda ingichka bronza chiziq

## 4. Chizma uslubi (barcha rasmlar uchun yagona)

- **Chiziq qalinligi:** 1.5 pt (asosiy), 1 pt (yordamchi)
- **Strelkalar:** uchburchak, 8 pt
- **Ranglar:** ko'k (#0B2C4A) — bog'lar/ramkalar, bronza (#C28E3B) — aksent, qizil (#D32F2F) — O atomi, sariq (#FBC02D) — S atomi, yashil (#388E3C) — N, h.k.
- **Fon:** har doim oq, soyasiz (chop etishga qulay)
- **Izohlar:** rasm ichida o'zbekcha, 8 pt Calibri, qisqa

## 5. Mundarija (TOC) dizayni
- Qism nomi: 14 pt, ko'k, Bold, ustidan bronza chiziq
- Bob qatori: 11 pt, chapda bob raqami (bronza), o'ngda sahifa raqami (nuqtalar bilan)
- Ilovalar: italic, kulrang

## 6. Texnik amalga oshirish
`build_docx.py` da quyidagilar sozlanadi:
- Sahifa o'lchami va hoshiyalar (A4)
- Barcha uslublar (Heading 1/2/3, Normal, Caption, Variant, Admonition)
- Ranglar RGBColor orqali
- Kolontitul va sahifa raqami (footer, bronza chiziq)
- Jadval uslubi (zebra, ko'k sarlavha)
- Muqova sahifasi (jadval yoki rasm bilan)

> Tasdiqlasangiz, 1-bob yozilishi bilan birga dizayn ham kodga o'tadi — birinchi namuna DOCX da jonli ko'rasiz.

## 7. Sizdan kerak
1. Muqova varianti: **A / B / C** (yoki aralash)
2. Rang bo'yicha izoh: shu palitra ma'qulmi yoki boshqa rang xohlaysizmi (masalan, yashil kimyo, qora-oltin premium)
3. Mundarijada bob qo'shish/olib tashlash istagi bormi

Keyin darhol 1-bobga o'tamiz.
