# Kitob loyihasi — ish hujjati

Bu papka **kitob yozish** uchun mo'ljallangan. U JDA Kimyo Quiz botidan mustaqil
ishlaydi: bot kodi bilan hech qanday bog'liqlik yo'q, faqat bitta jamiyat — Word formatidagi
kitobni yig'ish.

---

## 1. Nima qurildi

| Narsa | Joyi | Vazifasi |
|---|---|---|
| DOCX qurilchi | `qurilma/build_docx.py` | Markdown manbalarni chiroyli Word kitobiga aylantiradi |
| Metadata | `kitob.json` | Sarlavha, muallif, nashr, muqova matni |
| Boblar | `boblar/*.md` | Kitobning barcha matni shu yerda (Markdown) |
| Tayyor kitob | `chiqish/*.docx` | Qurilgan Word fayli (avtomatik yaratiladi) |

Tizim: **Markdown (manba) → DOCX (tayyor kitob)**. Matn Markdown'da yoziladi, format esa
bir xil qoidalar bo'yicha avtomatik qo'yiladi — shuning uchun butun kitob bo'ylab
bir xil ko'rinish saqlanadi.

---

## 2. Qurish buyruqlari

```bash
# 1) Bir marta: kutubxona o'rnatish
python3 -m venv .venv-book
.venv-book/bin/pip install python-docx

# 2) So'zlar hisoboti (tez, fayl yaratmaydi)
.venv-book/bin/python kitab/qurilma/build_docx.py --check

# 3) To'liq kitobni qurish
.venv-book/bin/python kitab/qurilma/build_docx.py

# 4) Faqat bitta bobni qurish
.venv-book/bin/python kitab/qurilma/build_docx.py --bob 03
```

Natija: `kitob/chiqish/<Sarlavha>.docx`

---

## 3. Markdown dialekti

### Sarlavhalar
```markdown
## 2.1. Kimyoviy bog'lanish      ->  2.1. Kimyoviy bog'lanish (avtomatik raqamlanadi)
### Molekulyar geometriya         ->  2.1.1. Molekulyar geometriya
```
`#` sarlavha bob sarlavhasi bo'lib, har bir yangi bob avtomatik ravishda yangi sahifadan
boshlanadi. Bo'limlar avtomatik raqamlanadi: **1.1, 1.1.1, 1.2 ...**

### Formulalar
Blokli formula (markazga joylashadi, o'ng tomonda avtomatik raqam):
```markdown
$$ \Delta E = E_{\text{reaktsiya}} - \sum E_{\text{reaktant}} $$
```
Natija: *ΔE = E*<sub>reaktsiya</sub> − ∑*E*<sub>reaktant</sub>  **(1.2)**

Inline formula: `molekula massasi $M = 12 \cdot n$ g`a teng.

Qo'llab-quvvatlanadigan yozuvlar: `\frac{a}{b}`, `\sqrt{x}`, `\text{...}`, `\mathrm{...}`,
grek harflari (`\alpha … \omega`, `\Delta`, `\Sigma`), `\times`, `\cdot`, `\pm`, `\to`,
`\approx`, `\neq`, `\le`, `\ge`, `\infty`, `\sum`, `\prod`, `\int`, `\sqrt`.

### Rasmlar
```markdown
![Alt matn](../../assets/alkenlar/q49.png "Rasm sarlavhasi")
```
Rasm markazga joylashadi, ostida avtomatik **1.1-rasm.** sarlavhasi chiqadi.

### Jadvallar
```markdown
| Turi | Belgisi | Uzunligi, pm |
|---|---|---|
| Oqilona (bir) | – | 74 |
```
Jadval ustidda avtomatik **1.1-jadval.** yozuvi chiqadi.

### Eslatma / muhim bloklari
```markdown
> [!NOTE]
> Matn

> [!IMPORTANT]
> Matn
```
Variantlar: `NOTE` (Eslatma), `IMPORTANT` (Muhim), `TIP` (Maslahat), `WARNING` (Diqqat),
`EXAMPLE` (Misol).

### Ro'yxatlar
```markdown
- oddiq element
- [ ] bajarilmagan vazifa
- [x] bajarilgan vazifa

1. birinchi
2. ikkinchi
```

### Test variantlari
```markdown
A) birinchi variant
B) ikkinchi variant
```
Har bir variant "chiziqli" uslubda, osilgan indent bilan chiqadi.

### Boshqa
- `<!-- pagebreak -->` — yangi sahifa
- `---` — ajratuvchi chiziq
- `**qalin**`, `*kursiv*`, `` `kod` ``, `[havola](https://...)`

---

## 4. Boblar strukturasi (yagona shakl)

Har bir bob shu tuzilma bilan yoziladi:

```markdown
---
number: 3
title: "Bob sarlavhasi"
subtitle: "Qo'shimcha sarlavha"
---

## Mavzu haqida            (2-3 paragraf)
## Asosiy tushunchalar      (nazariy material + formulalar + jadvallar)
### Tarmoqlar / Misollar
## Rasmlar va sxemalar
## Mustaqil mashqlar        (masalalar + test savollari)
### Test savollari
## Yakuniy xulosalar
## Adabiyotlar
```

---

## 5. Ish tartibi

1. **Reja** — boblar ro'yxati va qisqa mazmuni tasdiqlanadi.
2. **Yozish** — har bir bob alohida yoziladi (`boblar/NN_nomi.md`).
3. **Tekshiruv** — muallif o'qib chiqadi, izoh beradi.
4. **Tuzatish** — izohlarga ko'ra bob yangilanadi.
5. **Yig'ish** — `build_docx.py` barcha boblardan bitta DOCX yig'adi.
6. **Chop etish** — Word/PDF eksport (Google Docs orqali ham bo'ladi).

---

## 6. Sizdan kutilayotgan qarorlar

- [ ] Kitobning **mavzusi** (mavzu bo'yicha boblar ro'yxati)
- [ ] **Hajmi** (taxminan necha bob / necha sahifa)
- [ ] **Tuzilma turi**: nazariy darslik / masalalar to'plami / o'quv qo'llanma / aralash
- [ ] Har bir bobda **javoblar** bo'ladimi (yechimlar alohida bo'limda)
- [ ] **Rasmlar**: mavjudmi (sxemalar, tuzilmalar) yoki chizilishi kerakmi
- [ ] Kitob **kim uchun**: 1-kurs, 2-kurs, magistrantura, o'quv qo'llanma
