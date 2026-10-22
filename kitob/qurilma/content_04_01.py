from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('ionic','Uch xil yozuv va ularning vazifasi',['Daraja','Misol / mazmun','Nima saqlanadi?'],[
['Molekulyar','HCl+NaOH → NaCl+H₂O','Formal miqdorlar nisbati'],['To‘liq ionli','H₃O⁺, Cl⁻, Na⁺, OH⁻','Haqiqiy ionlar va elektr zaryad'],['Qisqartirilgan','H₃O⁺+OH⁻ → 2H₂O','Markaziy proton almashinuvi'],['Kuzatuvchi ion','Na⁺ va Cl⁻','Zaryad balansi va ion kuchi'],['Qattiq yoki kuchsiz tur','CuO(s), HA, NH₃','Asossiz ionlarga ajratilmaydi']]),
('direction','Teng boshlang‘ich HA va B; ideal cheklangan model',['ΔpKₐ','K','O‘zgargan ulush x/C'],[
['−2','0,01','0,090909; taxminan 9,09%'],['0','1','0,5; 50%'],['+2','100','0,909091; taxminan 90,91%'],['+4','10000','0,990099; taxminan 99,01%'],['HA+OH⁻','K≈Kₐ/K_w','Suv faolligi ≈1, mos standartlar'],['H⁺+OH⁻','K≈1/K_w','25 °C ideal soni ≈10¹⁴']]),
('equivalents','Nishon reaksiyaga bog‘liq proton ekvivalentlari',['Kislota / nishon','1 mol uchun OH⁻ talabi','Izoh'],[
['HCl → xlorid','1 mol','Bir protonli nishon'],['H₂SO₄ → sulfat','2 mol','Boshlang‘ich α umumiy talabni kamaytirmaydi'],['H₃PO₄ → H₂PO₄⁻ formal','1 mol','Birinchi stexiometrik bosqich'],['H₃PO₄ → HPO₄²⁻ formal','2 mol','Ikkinchi stexiometrik bosqich'],['H₃PO₄ → PO₄³⁻ formal','3 mol','Yakuniy suvli ion tarkibi boshqa masala'],['n_i/ν_i minimumi','ξ ning stexiometrik chegarasi','Muvozanat miqdoriylikni cheklashi mumkin']]),
('phosphate','C_P=0,0100 mol L⁻¹; ideal suvli fosfat modeli',['r=n(NaOH)/n(P)','Ustun ionlar ulushi','Hisobiy pH'],[
['1; formal NaH₂PO₄','H₂PO₄⁻ ≈99,406%','4,78834'],['2; formal Na₂HPO₄','HPO₄²⁻ ≈99,383%','9,52671'],['3; formal Na₃PO₄','PO₄³⁻ ≈24,158%; HPO₄²⁻ ≈75,840%','11,87992'],['Har bir nuqta','Barcha 4 shakl + suv','Yakuniy C_P bir xil'],['Formal tuz','Analitik Na:P nisbati','Bitta ionning 100% ulushi emas']]),
('saltph','Ekvivalent tarkib va yakuniy pH; C=0,0100 M',['Tuz modeli','Ideal pH; 25 °C','Muvozanat sababi'],[
['NaCl','7,00000','Ionlar sezilarli gidrolizsiz'],['NaA; K_c(HA)=10⁻⁵','8,50015','Anion suvdan proton oladi'],['NH₄Cl; K_c=5,6×10⁻¹⁰','5,62557','Kation proton beradi'],['BH⁺A⁻ shartli juftlik','7,00000','K_c(HA)=10⁻⁵; K_c(BH⁺)=10⁻⁹'],['Oxirgi juftlik tarkibi','HA va B ≈0,9901% dan','Neytral pH to‘liq sarf isboti emas']]),
('heat','Shartli kalorimetr hisobi; tajriba ma’lumoti emas',['Berilgan kattalik','Qiymat','Natijadagi roli'],[
['ΔH_neut','−57,0 kJ mol⁻¹','Model uchun berilgan doimiy'],['ξ','0,0100 mol','q_rxn=−570 J'],['m va c_p','200 g; 4,18 J g⁻¹ K⁻¹','Eritma issiqlik sig‘imi 836 J K⁻¹'],['C_cal','20 J K⁻¹','Idish hissasi'],['q_abs','+570 J','Issiqlik yo‘qotilmagan'],['ΔT','0,66589 K','Standart tajribaviy qiymat emas']]),
('routes','Tuz hosil bo‘lishining turli yo‘llari',['Reagentlar','Formal misol','Talqin'],[
['Kislota + gidroksid','HCl+NaOH → NaCl+H₂O','Suvli H₃O⁺/OH⁻ jarayoni'],['Kislota + NH₃','HCl+NH₃ → NH₄Cl','Molekulyar yozuvda suv shart emas'],['Kislota + oksid','CuO+2HCl → CuCl₂+H₂O','Qattiq faza saqlanadi'],['Kislota + gidrokarbonat','NaHCO₃+HCl → NaCl+CO₂+H₂O','Gaz fazasi va ochiq/yopiq tizim'],['NaCl(aq)+HNO₃(aq)','Formal qayta guruhlash','Suyultirilgan suvda odatda net reaksiya yo‘q']]),
('types','Tuz turi bilan eritma pH ini aralashtirmang',['Tarkib / faza','Tasnif yoki xossa','Muhim farq'],[
['NaHCO₃','Kislotali tuz; amfiprot anion','Eritmasi ishqoriy bo‘lishi mumkin'],['NH₄Cl','O‘rta tuz','Eritmasi kislotali bo‘lishi mumkin'],['Na₃PO₄','O‘rta tuz, H saqlamaydi','Suvda kuchli gidrolizlanadi'],['Cu₂(OH)₃Cl','Asosli tuzning formal tarkibi','Qisman sarf shu fazani isbotlamaydi'],['CuSO₄ / CuSO₄·5H₂O','Suvsiz / kristallogidrat','Molyar massalar farqli'],['NaCl(s) / NaCl(aq)','Panjara / erigan ionlar','Formula bir xil, mikrotasvir boshqa']]),
('worked','HCl–NaOH aralashmasi; ishlangan nazariy misol',['Bosqich','Hisob','Natija'],[
['Kislota','0,1500×0,04000','0,006000 mol'],['Asos','0,2000×0,02500','0,005000 mol'],['Formal NaCl','Chegaralovchi NaOH bo‘yicha','0,005000 mol'],['Kislota ortig‘i','0,006000−0,005000','0,001000 mol ekv.'],['V_yakun va D','0,06500 L; 0,001000/V_yakun','0,0153846 mol L⁻¹'],['Ideal pH','Suvli tenglama ildizi','1,81291'],['Nazariy NaCl massasi','0,005000×58,44','0,2922 g; amaliy kristall emas']])]
out={}
for i,(key,title,headers,rows) in enumerate(data,1):out[key]={'caption':f'4.1.{i}-jadval. {title}','headers':headers,'widths':[3.0,4.9,4.9],'rows':rows}
(R/'04_01_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['Bir suvmi, ikki suvmi?','H⁺ bilan qisqa yozuvda H₂O; H₃O⁺ bilan yozilganda 2H₂O. Atom balanslari boshqa, markaziy ma’no bir.'],['Kuzatuvchi ≠ yo‘q ion','Na⁺ va Cl⁻ qisqartirilgan reaksiyadan chiqadi, lekin elektr neytrallikdan emas.']],
[['ΔpKₐ ning ishorasi','Bu yerda pKₐ(BH⁺)−pKₐ(HA). Katta musbat farq mahsulotlarni afzal qiladi.'],['K va tezlik','Muvozanat mahsulotlarni afzal ko‘rishi qattiq oksidning tez erishini kafolatlamaydi.']],
[['Reaksiya nishoni','Ekvivalentlar soni qaysi proton bosqichi neytrallanishiga bog‘liq. H₃PO₄ uchun 1, 2 yoki 3 bo‘lishi mumkin.'],['Chegara va haqiqiy ξ','n_i/ν_i minimumi stexiometrik chegaradir. Cheklangan K bo‘lsa real o‘zgarish undan kam bo‘lishi mumkin.']],
[['Tarkibning ikki darajasi','Na₃PO₄ formal formula. Eritmadagi PO₄³⁻ ulushi shartsiz 100% emas.'],['Grafikning sharti','Har bir eritmada yakuniy C_P bir xil. Bu 3.4 dagi hajmi o‘zgaruvchi titrlash egri chizig‘i emas.']],
[['Shartli HA','K_c=10⁻⁵ berilgan HA aniq HF deb olinmagan. pH qiyosi ideal modellar uchun.'],['Neytral son yetmaydi','pH=7 qolgan neytral HA va B yo‘qligini isbotlamaydi; tutash oilalar ta’siri tenglashishi mumkin.']],
[['Issiqlik ishoralari','Ekzotermik reaksiyada q_rxn manfiy; eritma va idish olgan q_abs musbat.'],['−57,0 shartli berilgan','Grafik va misoldagi qiymat universal konstanta yoki muayyan tajriba o‘lchovi emas.']],
[['Faza belgisini saqlang','CuO(s) ni eritmada boshidan erkin O²⁻ ionlari sifatida yozmang.'],['Gaz bilan bog‘lanish','CO₂ chiqib ketishi ochiq tizim tarkibini o‘zgartiradi. Yopiq idishda gaz muvozanati ham kerak.']],
[['Kislotali tuz nomi','Atama tarkibdagi kislota qoldig‘ini tavsiflaydi, eritma rangini yoki pH ini emas.'],['Panjara rasmi','NaCl ning ranglari shartli. Yon tasvir cheklangan bo‘lak, real rang yoki alohida molekulalar to‘plami emas.']],
[['Nazariy va amaliy massa','Hisoblangan molni molyar massaga ko‘paytirish ajratilgan toza kristall hosilini o‘lchamaydi.'],['Keyingi mavzu','4.2 da oksidlovchilik va qaytaruvchilik ko‘riladi; neytrallanish tenglamasi redoksni avtomatik qamramaydi.']]]
(R/'04_01_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
