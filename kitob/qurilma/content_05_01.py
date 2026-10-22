from pathlib import Path
import json
R = Path(__file__).resolve().parents[1] / 'matn'

data = [
('tamoyillar', 'Kislota olishining uch o‘lchagi va mahsulot talablari', [
 ['Termodinamik o‘lchak', 'ΔG° va K', 'Reaksiya o‘z-o‘zidan olish mumkinmi'],
 ['Kinetik o‘lchak', 'Tezlik va to‘siq', 'Realda qanday tez boradi'],
 ['Texnologik o‘lchak', 'Ajratish va konsentratsiya', 'Chiqindi va xavfsizlik'],
 ['Tozalik talabi', 'Ifloslik, rang, metallar', 'Analitik nazorat'],
 ['Konsentratsiya talabi', 'Mass ulushi va zichlik', 'Titrlash va areometr'],
 ['Barqarorlik talabi', 'Parchalanish va saqlash', '4.5-bo‘lim bilan bog‘liq'],
 ['Ziddiyat', 'Konsentratsiya ↔ barqarorlik', 'Har bir kislota uchun alohida'],
 ['Chegara', 'Texnologik parametrlar', 'Bu bobda berilmaydi']]),
('usullar', 'Olish usullarining tasnifi va ularning chegaralari', [
 ['To‘g‘ridan-to‘g‘ri birikish', 'H₂ + Cl₂ → 2HCl', 'Yon mahsulot yo‘q; boshqarish qiyin'],
 ['Oksidlash zanjiri', 'S → SO₂ → SO₃', 'Ko‘p bosqich; mustaqil moddalar'],
 ['Tuzdan siqish', 'Tuz + kuchliroq kislota', 'Sulfat kislota sarflanadi'],
 ['Gidroliz', 'Galogenid + H₂O', 'Suv bilan birga chiqadi'],
 ['Elektrokimyaviy', 'Tok bilan yuqoriga surish', 'm = MQ/(zF); elektr toki kerak'],
 ['Tabiiy tiklash', 'Chiqindini qayta ishlash', 'Sifat past, arzon'],
 ['Tanlash mezoni', 'ΔG°, K, faza, chiqindi', 'Barchasi birga baholanadi'],
 ['Chegara', 'Amaliyot ko‘rsatmasi', 'Texnologik parametrlar berilmaydi']]),
('termo', 'Termodinamik mezon: to‘rtta tipik reaksiya', [
 ['SO₂ + ½O₂ → SO₃', 'ΔH°=−98,89; ΔS°=−94,04', 'ΔG°=−70,85 kJ/mol; lg K=12,41'],
 ['4NH₃ + 5O₂ → 4NO + 6H₂O', 'ΔH°=−1170,38; ΔS°=−534,00', 'ΔG°=−1011,17; lg K=177,15'],
 ['N₂O₄ ⇌ 2NO₂', 'ΔH°=+55,30; ΔS°=+175,80', 'ΔG°=+2,89 kJ/mol; lg K=−0,506'],
 ['H₂ + Cl₂ → 2HCl', 'ΔH°=−184,61; ΔS°=+20,00', 'ΔG°=−190,58 kJ/mol; lg K=33,39'],
 ['Manba', 'OpenStax Appendix G', '25 °C standart qiymatlar'],
 ['Model', 'ΔH° va ΔS° doimiy', 'Issiqlik sig‘imi hisobga olinmagan'],
 ['Chegara', 'ΔG° ≠ tezlik', 'K faqat standart holatda'],
 ['Xulosa', 'Termodinamik mezon — birinchi filtr', 'Tezlik va texnologiya alohida']]),
('muvozanat', 'Muvozanatni boshqarishning to‘rt dastagi', [
 ['Harorat', 'Endotermik yo‘nalishda K ortadi', 'N₂O₄: 250 K → 0,033; 400 K → 0,979'],
 ['Bosim', 'Moddalar soni ortsa, K pasayadi', '298,15 K: 1 bar → 0,269; 100 bar → 0,028'],
 ['Konsentratsiya', 'Reagent qo‘shilsa orqaga suriladi', 'Ortiqcha suv sulfatni bo‘shaydi'],
 ['Mahsulotni chiqarish', 'Suv yoki gaz chiqishi suradi', 'SO₃ ning suv bilan birikishi'],
 ['van ’t Hoff', 'ln(K₂/K₁)=−ΔH°/R(1/T₂−1/T₁)', '300 → 400 K: K 255 marta'],
 ['Model', 'N₂O₄ ⇌ 2NO₂; ideal gaz', '1, 10 va 100 bar egri chiziqlari'],
 ['Chegara', 'Faollik va issiqlik sig‘imi', 'Real tizimda natijani siljitadi'],
 ['Amaliy natija', 'Dastakni tanlash', 'Har bir usul uchun alohida hisob']]),
('kinetika', 'Kinetik to‘siqlar va ularning yechimi', [
 ['Aktivatsiya to‘sig‘i', 'Sekin boshlanish', 'Katalizator (3.6 va 4.5)'],
 ['Fazalararo mass transfer', 'Interfeysda reagent tanqisligi', 'Yaxshi aralash, doljinka'],
 ['Reagent donadorligi', 'Faqat yuzada reaksiya', 'Reagent usuli'],
 ['Qalqon usuli', 'Reaksiya qalqon bilan boshqariladi', 'Qalqonning asta ochilishi'],
 ['Harorat profili', 'Issiq nuqta hosil bo‘ladi', 'Profilni boshqarish choralari'],
 ['Diffuziya chegarasi', 'Tezlik mass transfer bilan cheklanadi', 'Yuzani kattalashtirish'],
 ['Chegara', 'Texnologik parametr yo‘q', 'Amaliyot 7, 8 va 12-bo‘limlarda'],
 ['Xulosa', 'To‘siq turlari ajratilgan', 'Har biri o‘z yechimini talab qiladi']]),
('bloklar', 'Umumiy blok-sxema va har bir blokning vazifasi', [
 ['Xom ashyo', 'Kerakli moddani kiritish', 'Tarkib va namdorlik'],
 ['Reagent tayyorlash', 'Eritma yoki gaz tayyorlash', 'Konsentratsiya va tozalik'],
 ['Reaksiya', 'Kimyoviy o‘zgarish', 'Konversiya va selektivlik'],
 ['Fazalarni ajratish', 'Cho‘kma va suyuqni ajratish', 'Qoldiq miqdori'],
 ['Absorbsiya', 'Gazni suyuq fazaga o‘tkazish', 'Yutilish unumi'],
 ['Tozalash va konsentratsiya', 'Ifloslik va suvni olib tashlash', 'Mass ulushi va zichlik'],
 ['Chiqindini tiklash', 'Resursni qaytarish', 'Chiqindi omili'],
 ['Chegara', 'Parametrlar berilmaydi', 'Faqat tamoyil va o‘lchov ko‘rsatiladi']]),
('unum', 'Unum, konversiya, selektivlik va chiqindi omili', [
 ['Konversiya X', 'Reagentning mahsulotga ulushi', 'Model: SO₂ → SO₃: 0,96'],
 ['Selektivlik S', 'Kerakli mahsulotning ulushi', 'Yon mahsulot kam bo‘lishi kerak'],
 ['Unum η', 'Haqiqiy va nazariy miqdor nisbati', 'Modelda η = 0,9408 (94,08 %)'],
 ['Nazariy miqdor', 'FeS₂ dan H₂SO₄', '1000 t pyrit → 1634,94 t'],
 ['Chiqindi omili', '1 kg mahsulotga chiqindi massasi', '0,46 kg/kg (X = 0,96)'],
 ['Cho‘kma qoldig‘i', 'Fe₂O₃ ulushi', '665,49 t'],
 ['Reagent qaytarish', 'Siklga qaytarish', 'Begona modda chegarasi'],
 ['Chegara', 'Model sodda', 'Issiqlik sig‘imi va faza o‘zgarishi yo‘q']]),
('ajratish', 'Ajratish usullari va ularning imkoniyatlari', [
 ['Bug‘lash (rektifikatsiya)', 'Uchuvchanlik farqi', 'Nisbiy uchuvchanlik α'],
 ['Ekstraksiya', 'Erituvchi tanlanish', 'Kam uchuvchi moddalar uchun'],
 ['Cho‘ktirish', 'Eriuvchanlik farqi', 'Kuchli elektrolitlar'],
 ['Adsorbsiya', 'Sirt bilan tutish', 'Yuqori tozalik talab qilinadi'],
 ['Membrana', 'Selektiv o‘tkazish', 'Suyuq–suyuq ajratish'],
 ['Kimyoviy yutish', 'Reaktsiya bilan ushlamoq', 'SO₃ → H₂SO₄'],
 ['Minimal pog‘onalar', 'Fenske formulasi', 'α = 1,1 → 61,8; α = 2,0 → 8,5'],
 ['Chegara', 'Azeotrop nuqta', 'HNO₃ uchun 8-bo‘limga']]),
('ekologiya', 'Chiqariladigan moddalar va ularni ushlash tamoyillari', [
 ['SO₂', 'Kislota gazi', 'Yutish va reagentga qaytarish'],
 ['NO₂', 'Nitrik kislota gazi', 'Yutish va tiklash'],
 ['HCl', 'Xlorid kislota gazi', 'Yutish; suv bilan yiqilish'],
 ['H₂S', 'Sulfid kislota', 'Yutish; zaxira usuli bilan'],
 ['Manba', 'Xom ashyo va reaksiya', 'Ajratishdan oldin ushlash'],
 ['Usul', 'Yutish va tiklash', 'Resurs qaytadi'],
 ['Xavfsizlik', 'Yopiq tizim, ikki himoya', 'Kislota suvga quyiladi'],
 ['Chegara', 'Texnologiya va retsept', 'Berilmaydi; 7, 8 va 12-bo‘limlar']]),
('sifat', 'Tayyor kislota sifati: ko‘rsatkich va hujjat', [
 ['Kislota miqdori', 'Titrlash (3.4-bo‘lim)', 'c = n(titrant)/V; mass ulushi'],
 ['Zichlik', 'Areometr', 'Solishtirish uchun qiymat'],
 ['HCl (savdo)', '36 %; 1,18 g/mL; 11,6 M', 'OpenStax Appendix F'],
 ['HNO₃ (savdo)', '71 %; 1,42 g/mL; 16,0 M', 'OpenStax Appendix F'],
 ['HClO₄ (savdo)', '70 %; 1,67 g/mL; 11,65 M', 'OpenStax Appendix F'],
 ['H₂SO₄ (savdo)', '96 %; 1,84 g/mL; 18,0 M', 'OpenStax Appendix F'],
 ['H₃PO₄ (savdo)', '85 %; 1,70 g/mL; 14,7 M', 'OpenStax Appendix F'],
 ['Ifloslik', 'Metallar, rang, qoldiq', 'ICP va spektroskopiya'],
 ['Hujjat', 'Partiya, metod, natija, sana', 'Mas’ul shaxs; barqarorlik 4.5']]),
('hisob', 'Ishlangan hisob: pyritdan sulfat kislotagacha material balansi', [
 ['n(FeS₂)', '8334,72 kmol', '1000 t / 119,98 kg/kmol'],
 ['n(SO₂)', '16 669,44 kmol', '1 mol FeS₂ → 2 mol SO₂'],
 ['n(SO₃)', '16 002,67 kmol', 'Konversiya 0,96'],
 ['n(H₂SO₄)', '15 682,61 kmol', 'Yutilish unumi 0,98'],
 ['m(H₂SO₄)', '1538,15 t', 'Nazariy 1634,94 t'],
 ['Fe₂O₃ qoldig‘i', '665,49 t', '4167,36 kmol'],
 ['Unum va chiqindi', '94,08 %; 0,4604 kg/kg', 'Chiqindi omili model bo‘yicha'],
 ['Suv balansi', '346,61 t', '282,52 + 64,09 t (96 % kislota)']])]

out = {}
for i, (key, title, rows) in enumerate(data, 1):
    out[key] = {'caption': f'5.1.{i}-jadval. {title}',
                'headers': ['Obyekt / parametr', 'Mazmun / qiymat', 'Chegara / izoh'],
                'widths': [3.8, 4.4, 4.6],
                'rows': rows}
(R / '05_01_jadvallar.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))

notes = [
 [['Uch o‘lchak', 'Termodinamik, kinetik va texnologik mezon birga baholanadi.'],
  ['Ziddiyat', 'Konsentratsiya oshsa, barqarorlik pasayadi.']],
 [['Reagent — chiqindi', 'Har bir usul o‘z chiqindisini yaratadi.'],
  ['Tanlash', 'ΔG°, K, faza va chiqindi birga solishtiriladi.']],
 [['Standart holat', '1 bar, 298,15 K, birlik faollik.'],
  ['K ≠ tezlik', 'K katta bo‘lishi tez borishni bildirmaydi.']],
 [['To‘rt dastak', 'Harorat, bosim, konsentratsiya, mahsulot chiqarish.'],
  ['Model', 'N₂O₄ ⇌ 2NO₂; ideal gaz, doimiy ΔH° va ΔS°.']],
 [['Reagent usuli', 'Donador reagent yuzasi asta-sekin mayinadi.'],
  ['Qalqon usuli', 'Reaksiya qalqonning ochilishi bilan boshqariladi.']],
 [['Absorbsiya', 'Gazni suyuq fazaga o‘tkazish — muvozanatni surish vositasi.'],
  ['Kaskad', 'N o‘sishi unumni oshiradi, marginal samarasi kamayadi.']],
 [['Unum', 'Konversiya va selektivlikning mahsuloti.'],
  ['Chiqindi omili', '1 kg mahsulotga to‘g‘ri keladigan chiqindi massasi.']],
 [['Nisbiy uchuvchanlik', 'α — bug‘lash qiyinligining o‘lchovi.'],
  ['Azeotrop', 'Oddiy bug‘lash yetarli bo‘lmasligi mumkin.']],
 [['Manbadan ushlash', 'Gaz yig‘ilib, yutilib, tiklanadi.'],
  ['Chegara', 'Texnologik parametrlar va retseptlar berilmaydi.']],
 [['Titrlash', 'Kislota miqdorining universal usuli.'],
  ['Sifat hujjati', 'Partiya, metod, natija, sana va mas’ul shaxs.']],
 [['Model', 'Barcha natijalar ochiq shartli modeldan olingan.'],
  ['Chegara', 'Issiqlik sig‘imi va faza o‘zgarishi hisobga olinmagan.']]]
(R / '05_01_yonlavhalar.json').write_text(json.dumps(notes, ensure_ascii=False, indent=2))
print(f'11 jadval, {sum(len(n) for n in notes)} yon lavha.')
