from pathlib import Path
import json
R = Path(__file__).resolve().parents[1] / 'matn'

data = [
('types', 'Parchalanish va uning qarindoshlari: farqlar', [
 ['Dissotsiatsiya', 'HA ⇌ H⁺ + A⁻', 'Ionlar paydo bo‘ladi'],
 ['Gidroliz', 'XO⁻ + H₂O ⇌ XOH + OH⁻', 'Suv bilan o‘zaro ta’sir'],
 ['Redoks', 'Elektron almashinuvi', 'Daraja o‘zgaradi'],
 ['Kondensatsiya', '2H₃PO₄ → H₄P₂O₇ + H₂O', 'Suv ajratib oligomer'],
 ['Polimerlash', 'Zanjirga ulanadi', 'Kovalent bog‘lar hosil bo‘ladi'],
 ['Termik parchalanish', 'H₂SO₄ → SO₃ + H₂O', 'Energiya haroratdan olinadi'],
 ['Fotoliz', 'HNO₃ → NO₂ + H₂O + ½O₂', 'Energiya yorug‘likdan olinadi'],
 ['Dismutatsiya', '3HNO₂ → HNO₃ + 2NO + H₂O', 'Bitta element ikki yo‘naladi'],
 ['Avtokataliz', 'Mahsulot katalizator', 'Jarayon tezlashadi']]),
('thermo', 'Uchta parchalanish reaksiyasining termodinamik ko‘rsatkichlari', [
 ['HNO₃ → NO₂ + H₂O + ½O₂', 'ΔH°=−78,53; ΔS°=257,10', 'ΔG°(298,15)=−155,18 kJ/mol'],
 ['H₂SO₄ → SO₃ + H₂O', 'ΔH°=+132,44; ΔS°=169,86', 'ΔG°(298,15)=+81,80 kJ/mol'],
 ['H₂O₂ → H₂O + ½O₂', 'ΔH°=−98,05; ΔS°=63,00', 'ΔG°(298,15)=−116,83 kJ/mol'],
 ['T* = ΔH°/ΔS°', 'ΔG(T)=0 bo‘lgan harorat', 'Ishoralar bir xil bo‘lishi kerak'],
 ['H₂SO₄ uchun T*', '779,7 K ≈ 507 °C', 'Standart holat modeli'],
 ['HNO₃ uchun T*', '−305 K', 'Barcha T da qulay'],
 ['Manba', 'OpenStax Chemistry 2e, Appendix G', '25 °C uchun standart qiymatlar'],
 ['Chegara', 'ΔH° va ΔS° doimiy deb olindi', 'ΔC_p hisobga olinmagan']]),
('keq', 'Sulfur kislota parchalanishining muvozanat konstantasi', [
 ['K(600 K)', '2,2×10⁻³', 'Reagentlar tomoni ustun'],
 ['K(700 K)', '9,8×10⁻²', 'Hali reagentlar tomoni'],
 ['K(780 K)', '1,0', 'T* nuqtasi: K=1'],
 ['K(900 K)', '15', 'Mahsulotlar tomoni'],
 ['K(1000 K)', '90', 'SO₃ va suv ustun'],
 ['K(1200 K)', '1,3×10³', 'Amaliyotda ancha parchalanadi'],
 ['Amaliy kuzatuv', '610 K da qaynab chiqadi', '573 K dan yuqorida sekin parchalanadi'],
 ['Chegara', 'K_p va K_c farqi hisoblanmagan', 'Faollik tuzatmalari kiritilmagan']]),
('kinetics', 'Kinetik model: haroratga bog‘liq tezlik va yarim vaqt', [
 ['Model prefaktori A', '1,0×10¹³ s⁻¹', 'Aniq kislotga tegishli emas'],
 ['Model aktivatsiya energiyasi E_a', '100 kJ/mol', 'O‘quv modeli'],
 ['298,15 K', 'k=3,02×10⁻⁵ s⁻¹', 't½=2,30×10⁴ s ≈ 6,4 soat'],
 ['320 K', 'k=4,74×10⁻⁴ s⁻¹', 't½=1,46×10³ s ≈ 24 daqiqa'],
 ['350 K', 'k=1,19×10⁻² s⁻¹', 't½=58,3 s'],
 ['400 K', 'k=0,873 s⁻¹', 't½=0,79 s'],
 ['Tezlashtiruvchilar', 'Metall iflosligi, chang', 'Sirt katalizi va avtokataliz'],
 ['Chegara', 'Model emas, o‘quv taxmini', 'Saqlash muddatini aniqlab bermaydi']]),
('photo', 'Fotokimyoviy parchalanishning mexanizm qismlari', [
 ['Yutilish sharti', 'Foton faqat yutilganda ta’sir qiladi', 'Spektrlar kesishgan qism'],
 ['Kvant unumi Φ', 'Mol mahsulot / mol yutilgan foton', 'Zanjirda birdan dan katta bo‘lishi mumkin'],
 ['Boshlanish', 'Radikal yoki qo‘shimcha tuzilma hosil bo‘ladi', 'Energiya ta’mini bo‘lishi kerak'],
 ['Davomi', 'Radikal yangi radikal hosil qiladi', 'Zanjir uzluksiz davom etadi'],
 ['Tarmoqlanish', 'Bitta o‘lchovdan ko‘p zanjir', 'Tezlashuv'],
 ['Tugatish', 'Radikallar bir-birini yo‘q qiladi', 'Zanjir uziladi'],
 ['Nitrik kislota misoli', 'NO₂ hosil bo‘ladi, kislota sargayadi', 'Rang — miqdor emas, belgi']]),
('dismutation', 'Dismutatsiya misollari va ularning o‘lchov oqibatlari', [
 ['3HNO₂ → HNO₃ + 2NO + H₂O', 'N: +3 → +5 va +2', 'Nitrit kislota tez buziladi'],
 ['3HClO₃ → HClO₄ + 2ClO₂ + H₂O', 'Cl: +5 → +7 va +4', 'Tarkib tez o‘zgaradi'],
 ['4HClO₃ → 3HClO₄ + HCl', 'Oddiy dismutatsiya', 'Perxlorat barqarorroq'],
 ['2H₂O₂ → 2H₂O + O₂', 'Ishqoriy muhitda tezlashadi', 'Stabilizatorlar qo‘shiladi'],
 ['2H₂S + H₂SO₃ → 3S + 3H₂O', 'S: −2 va +4 → 0', 'Kolloid oltingugurt hosil bo‘ladi'],
 ['Tahlil oqibati', 'Titrlash jami kislotalikni o‘lchaydi', 'Mahsulot protonlari ham hisobga olinadi'],
 ['Saqlash', 'Nitrit kislota yangi tayyorlanadi', 'Yorug‘lik va haroratdan himoya']]),
('condensation', 'Kondensatsiya reaksiyalari va ularning entalpiyasi', [
 ['2H₃PO₄ → H₄P₂O₇ + H₂O', 'ΔH°=+31,2 kJ/mol', 'Pirofosfat; pastroq harorat'],
 ['H₄P₂O₇ → 2HPO₃ + H₂O', 'ΔH°=+58,2 kJ/mol', 'Metafosfat; yuqoriroq harorat'],
 ['H₂SO₄ + SO₃ → H₂S₂O₇', 'ΔH°=−63,9 kJ/mol', 'Oleum hosil bo‘ladi'],
 ['H₂S₂O₇ + H₂O → 2H₂SO₄', 'Ekzotermik gidroliz', 'Suv qo‘shilishi xavfli'],
 ['H₂SiO₃ → SiO₂ + H₂O', 'ΔH°=−7,9 kJ/mol', 'Gel hosil bo‘ladi'],
 ['H₃BO₃ → HBO₂ + H₂O', 'ΔH°=+14,3 kJ/mol', 'Issiqda metabor kislota'],
 ['2H₃BO₃ → B₂O₃ + 3H₂O', 'ΔH°=+57,7 kJ/mol', 'Yuqori harorat kerak'],
 ['(HF)ₙ assotsiatsiya', 'Vodorod bog‘i', 'Molekula o‘zgarmaydi']]),
('medium', 'S(IV) tizimining pH ga bog‘liq ulushlari', [
 ['K_a1 (H₂SO₃)', '1,6×10⁻²', '25 °C; OpenStax Appendix H'],
 ['K_a2 (HSO₃⁻)', '6,4×10⁻⁸', 'Ikkinchi bosqich'],
 ['pH = 1,00', 'α(SO₂·H₂O)=0,862', 'α(HSO₃⁻)=0,138'],
 ['pH = 7,00', 'α(SO₂·H₂O)=3,8×10⁻⁶', 'α(HSO₃⁻)=0,610; α(SO₃²⁻)=0,390'],
 ['pH = 12,00', 'α(SO₃²⁻)=0,999984', 'Gaz holatiga chiqish to‘siqlanadi'],
 ['Muqobilat qoidasi', 'H⁺ iste’moli yoki ajralishi', 'pH muvozanatni siljitadi'],
 ['Konsentratsiya', 'Birinchi tartibli model', 'Ion kuchi buzadi']]),
('storage', 'Barqarorlik guruhlari va saqlash tamoyillari', [
 ['Nitrik kislota', 'Termodinamik beqaror, kinetik barqaror', 'Sovuq, qorong‘i sharoit'],
 ['Sulfur kislota', 'Gigroskopik; 573 K dan yuqorida parchalanadi', 'Suv bilan aralashganda qizishadi'],
 ['Vodorod peroksid', 'Tez gaz ajratadi', 'Qorong‘i, sovuq, stabilizator bilan'],
 ['Perxlor kislota', 'Sof holda barqaror', 'Organik aralashuv bilan xavfli'],
 ['HCN va H₂S', 'Uchuvchan va zaharli', 'Faqat xavfsizlik nuqtai nazaridan'],
 ['Umumiy tamoyillar', 'Qorong‘i, sovuq, toza idish', 'Yozib borish, belgilash, ikkilamqi himoya'],
 ['Chegara', 'Usullar 5-bob va 12-bobda', 'Bu bob amaliyot tavsiyasi bermaydi']]),
('analysis', 'Parchalanish mahsulotlarini aniqlash usullari', [
 ['Titratsiya', 'Jami titratsion kislotalik', 'Protonlarni, kislotani emas o‘lchaydi'],
 ['pH o‘lchash', 'Erkin faol proton', 'Kislota kuchini ko‘rsatadi'],
 ['UV–Vis spektroskopiyasi', 'NO₂, ClO₂ kabi rangli turlar', 'Konsentratsiya chegarasi bor'],
 ['IR va Raman', 'Molekulyar turlar', 'Gidrat va oligomer farqi'],
 ['Boshlash gazi xromatografiyasi', 'Uchuvchi mahsulotlar', 'Sarf bo‘lishini aniqlaydi'],
 ['Ion xromatografiyasi', 'Anionlar', 'Nitrat va sulfat kabi'],
 ['ICP spektrometriyasi', 'Metallar', 'Katalizator qoldig‘ini ko‘rsatadi'],
 ['Karl Fischer', 'Suv miqdori', 'Kondensatsiya darajasi'],
 ['Tavsiya etilmaydi', 'Hid orqali aniqlash', 'Zaharli gazlarni hid bilish xavfli']]),
('worked', 'Ishlangan hisob: H₂SO₄ parchalanishining natijalari', [
 ['ΔH°', '+132,44 kJ/mol', '−395,72 − 285,83 + 813,99'],
 ['ΔS°', '169,86 J/(mol·K)', '256,76 + 70,00 − 156,90'],
 ['ΔG°(298,15)', '+81,80 kJ/mol', '132,44 − 298,15·0,16986'],
 ['lg K(298,15)', '−14,33', 'K ≈ 4,8×10⁻¹⁵'],
 ['T*', '779,7 K ≈ 507 °C', 'ΔH°/ΔS°'],
 ['K(700 K) va K(900 K)', '9,8×10⁻² va 15', 'van ’t Hoff qoidasi'],
 ['Nitrik kislota solishtiruvi', 'ΔG°=−155,18 kJ/mol', 'lg K ≈ 27,2; T* = −305 K'],
 ['Kinetik model', '298 K → 6,4 soat; 320 K → 24 daqiqa', 'A=1,0×10¹³ s⁻¹; E_a=100 kJ/mol']])]

out = {}
for i, (key, title, rows) in enumerate(data, 1):
    out[key] = {'caption': f'4.5.{i}-jadval. {title}',
                'headers': ['Obyekt / parametr', 'Mazmun / qiymat', 'Chegara / izoh'],
                'widths': [3.8, 4.4, 4.6],
                'rows': rows}
(R / '04_05_jadvallar.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))

notes = [
 [['Parchalanish — keng ma’noda', 'Molekula bir necha mahsulotga bo‘linishi; kislota turi butunlay yo‘qoladi.'],
  ['Tor ma’noda', 'Faqat kislota turining yo‘qolishi; proton yo‘qotish emas.']],
 [['Amaliy savollar', 'Qancha saqlanadi, nima hosil bo‘ladi, muhitga ta’siri qanday?'],
  ['Barqarorlik xarakteri', 'Ba’zi kislotalar termodinamik beqaror, lekin saqlanadigan.']],
 [['Standart sharoit', 'Standart holat — birlik faollik, 1 bar bosim, 298,15 K.'],
  ['K ≠ tezlik', 'K katta bo‘lishi tez borishni bildirmaydi.']],
 [['Model chegarasi', 'A va E_a — o‘quv uchun tanlangan qiymatlar.'],
  ['Real tizim', 'Aniq kislot uchun E_a tajribada aniqlanadi.']],
 [['Radikal zanjiri', 'Boshlanish — davom — tarmoqlanish — tugatish.'],
  ['Faqat yutilgan foton', 'Yutilmagan nur spektri o‘zgarishni kuchaytirmaydi.']],
 [['Dismutatsiya belgisi', 'Bitta elementning oksidlanish darajasi ikki yo‘naladi.'],
  ['Perxlor kislota', 'Kontakt va aralashuv bilan xavfli; usul berilmaydi.']],
 [['Entalpiya belgisi', 'Pozitiv ΔH° — kondensatsiya uchun energiya kerak.'],
  ['Oleum', 'SO₃ ning H₂SO₄ ga yutilishi; teskari yo‘nalish ekzotermik.']],
 [['pH — kuchli vosita', 'Protonlanish gaz holatiga chiqishni to‘siqlaydi.'],
  ['Ko‘p tizim', 'Bitta pH barcha kislotalar uchun bir xil ta’sir qilmaydi.']],
 [['Saqlash — kinetik qaror', 'Harorat, yorug‘lik va ifloslik nazorati.'],
  ['Mas’uliyat chegarasi', 'Ishlab chiqarish va xavfsizlik 5- va 12-boblarda.']],
 [['O‘lchash obyekti', 'Qolgan kislota, mahsulot yoki ajralgan gaz — aniq tanlanadi.'],
  ['Ekstrapolatsiya', 'Tezlashtirilgan saqlash sinovi model doirasida qoladi.']],
 [['Natija faqat model ichida', 'Termodinamik chegara va kinetik blok birga baholanadi.'],
  ['Yakuniy xulosa', 'O‘lchash usuli noma’lum bo‘lsa, xulosa ham noma’lum.']]]
(R / '04_05_yonlavhalar.json').write_text(json.dumps(notes, ensure_ascii=False, indent=2))
print(f'11 jadval, {sum(len(n) for n in notes)} yon lavha.')
