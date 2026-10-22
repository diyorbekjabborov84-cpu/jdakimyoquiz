from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('roles','Proton ko‘chishi va elektron ko‘chishini farqlash',[
['HCl+NH₃','Hamma darajalar saqlanadi','Kislota–asos, redoks emas'],['Zn+2H⁺→Zn²⁺+H₂','Zn: 0→+2; H: +1→0','Zn qaytaruvchi; H⁺ oksidlovchi'],['Cu va HNO₃','Cu: 0→+2; N: +5→+4/+2','Nitrat elektron qabul qiladi'],['H₃PO₃→H₃PO₄','P: +3→+5','Fosforli kislota qaytaruvchi'],['Cl⁻ ning roli','Ba’zan kuzatuvchi, ba’zan qaytaruvchi','Reagent juftligi tekshiriladi']],['Tizim','Daraja / markaz','Mazmun']),
('potentials','25 °C, SHE ga nisbatan qaytarilish potensiallari [2,4]',[
['Zn²⁺+2e⁻→Zn','−0,7618 V','H⁺ bilan taqqoslanadi'],['2H⁺+2e⁻→H₂','0,0000 V','Etalon; gazning standart holati'],['Cu²⁺+2e⁻→Cu','+0,337 V','Erkin Cu²⁺ jufti'],['Fe³⁺+e⁻→Fe²⁺','+0,771 V','n=1; komplekslar tashlangan'],['NO₃⁻+4H⁺+3e⁻→NO+2H₂O','+0,957 V','NO nishoni; kislotali standart'],['MnO₄⁻+8H⁺+5e⁻→Mn²⁺+4H₂O','+1,507 V','Mn²⁺ nishoni; n=5']],['Qaytarilish yarimreaksiyasi','E°','Qo‘llanish sharti']),
('ph','pH qiyaligi: boshqa faolliklar birga teng bo‘lgan model',[
['H⁺/H₂','−0,05915935 V/pH','E(pH=2)=−0,11832 V'],['MnO₄⁻/Mn²⁺','−0,09465496 V/pH','E(pH=2)=1,31769 V'],['NO₃⁻/NO','−0,07887913 V/pH','E(pH=2)=0,79924 V'],['pH ortishi','Proton sarflanadigan juft E si pasayadi','Yarimreaksiya o‘zgarmaganida'],['Chiziqlar chegarasi','Turlar, faza va boshqa faolliklar saqlangan','To‘liq Pourbaix xaritasi emas']],['Juft / holat','Qiyalik yoki shart','Natija / cheklov']),
('medium','Permanganatning turli nishonlari va elektron talabi',[
['MnO₄⁻→Mn²⁺','Mn: +7→+2; 5e⁻','Kislotali nishon; 8H⁺ sarfi'],['MnO₄⁻→MnO₂(s)','Mn: +7→+4; 3e⁻','Suv/OH⁻ bilan balanslanadi'],['MnO₄⁻→MnO₄²⁻','Mn: +7→+6; 1e⁻','Manganat nishoni; ishqoriy sharoit'],['H⁺ ning vazifasi','H darajasi +1 da qolishi mumkin','Proton manbai ≠ redoks markazi'],['Elektron tekshiruvi','Fe²⁺ dan har biriga 1e⁻','Mn²⁺ uchun Fe:Mn=5:1']],['Nishon','Elektron balansi','Muhit / talqin']),
('nitrogen','Nitratdan turli azot mahsulotlariga formal elektron hisobi',[
['NO₂','N(+4); 1e⁻/N','Cu misolida 2NO₂ / 1Cu'],['NO','N(+2); 3e⁻/N','Cu misolida 2NO / 3Cu'],['N₂O','O‘rtacha N(+1); 4e⁻/N','8e⁻ / 1N₂O; atomlar ekvivalent emas'],['N₂','N(0); 5e⁻/N','10e⁻ / 1N₂'],['NH₄⁺','N(−3); 8e⁻/N','Mahsulot bo‘lsa; universal bashorat emas'],['Kuzatuvchi NO₃⁻','N(+5) saqlanadi','Tuzdagi nitratni qaytarilgan deb sanamang']],['Nishon mahsulot','Bir N uchun elektron','Muhim izoh']),
('sulfur','Oltingugurtning elektron sig‘imi nishonga bog‘liq',[
['S(+6)→SO₂; S(+4)','2e⁻ qabul','Oksidlovchi markaz qaytariladi'],['S(+6)→S(0)','6e⁻ qabul','Mahsulot tanlovi sharoitga bog‘liq'],['S(+6)→H₂S; S(−2)','8e⁻ qabul','Grafik mahsulotni bashorat qilmaydi'],['SO₂→SO₄²⁻','2e⁻ beradi','S(+4) qaytaruvchi'],['H₂S→S(0)','2e⁻ beradi','Bir nishon'],['H₂S→SO₄²⁻','8e⁻ beradi','Boshqa nishon; sarf 4 marta katta']],['O‘tish','1 mol S uchun','Talqin']),
('phosphorus','H soni, kislotalilik va elektron ekvivalenti boshqa kattaliklar',[
['H₃PO₄; OP(OH)₃','3 O–H; 0 P–H; P(+5)','Odatiy qaytaruvchi emas'],['H₃PO₃; HP(O)(OH)₂','2 O–H; 1 P–H; P(+3)','H₃PO₄ nishoniga 2e⁻ beradi'],['H₃PO₂; H₂P(O)(OH)','1 O–H; 2 P–H; P(+1)','H₃PO₄ nishoniga 4e⁻ beradi'],['Proton ekvivalenti','Tanlangan neytrallanish bosqichi','O–H sarfi bilan bog‘liq'],['Elektron ekvivalenti','Tanlangan oksidlanish mahsuloti','Proton ekvivalentiga teng emas']],['Kislota / ulanish','Tuzilish va daraja','Redoks talqini']),
('dual','Disproportsiyalanish va H₂O₂ ning ikki roli',[
['HNO₂→HNO₃','N: +3→+5; 2e⁻ beradi','Bir N oksidlanadi'],['2HNO₂→2NO','Har N: +3→+2; 1e⁻ qabul','Ikki N qaytariladi'],['H₂O₂→H₂O','O: −1→−2; 2e⁻/H₂O₂ qabul','E°(qaytarilish)=1,776 V'],['H₂O₂→O₂','O: −1→0; 2e⁻/H₂O₂ beradi','Teskari juft E°=0,695 V'],['2H₂O₂→2H₂O+O₂','E°_cell=1,081 V; n=2','ΔG°≈−208,60 kJ mol⁻¹'],['Termodinamika va tezlik','Katta K tez reaksiya degani emas','Kataliz/sirtlar alohida tekshiriladi']],['Jarayon','Elektron / potensial','Ma’no']),
('worked','Ideal kislotali MnO₄⁻–Fe²⁺ hisobining nazorati',[
['MnO₄⁻ boshlang‘ich','0,02000×0,02000','0,4000 mmol'],['Fe²⁺ boshlang‘ich','0,05000×0,05000','2,500 mmol'],['Elektron sig‘imi','0,4000×5','2,000 mmol e⁻'],['Fe³⁺ hosil / Fe²⁺ qoldiq','2,000 / 0,5000 mmol','Nisbat 4'],['Mn²⁺ hosil / H⁺ sarfi','0,4000 / 3,200 mmol','a(H⁺) yakunda ham berilgan'],['Fe juftining E si','0,771+0,05915935·lg4','0,80662 V (SHE)'],['Muvozanat MnO₄⁻ izi','a(H⁺)=0,100; γ≈1','≈3,65×10⁻⁵⁴ mol L⁻¹, model']],['Bosqich','Hisob / shart','Natija'])]
out={}
for i,(key,title,rows,headers) in enumerate(data,1):
 out[key]={'caption':f'4.2.{i}-jadval. {title}','headers':headers,'widths':[4.1,4.2,4.5],'rows':rows}
(R/'04_02_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['«Oksidlovchi emas» nisbiy','HCl da H⁺ elektron olishi mumkin. Atama odatda anionning alohida oksidlovchi emasligini anglatadi.'],['Daraja — formal hisob','Oksidlanish darajasi atomning haqiqiy lokal zaryadi yoki mexanizm tasviri emas.']],
[['E° ni ko‘paytirmang','Yarimreaksiya koeffitsiyentlari ortsa n va ΔG° o‘zgaradi; E° saqlanadi.'],['Standart holat','E° muayyan yarimreaksiyaga tegishli. Sof kislota uchun universal «redoks soni» emas.']],
[['lg va ln farqi','25 °C da lg uchun 0,05915935/n V, ln uchun RT/(nF) ishlatiladi.'],['Faollik birinchi o‘rinda','Konsentratsiya faollikning ideal yaqinlashuvi. Konsentrlangan kislotalarda farq muhim.']],
[['Proton ham sarflanadi','MnO₄⁻→Mn²⁺ da 5e⁻ bilan birga 8H⁺ kerak. Faqat elektronlarni sanash yetmaydi.'],['Mn nishonini ayting','Mn²⁺, MnO₂ va MnO₄²⁻ uchun 5, 3 va 1 elektron. Bir xil sarf koeffitsiyenti emas.']],
[['Gaz rangi yetarli emas','NO havoda NO₂ ga oksidlanadi. Kuzatilgan rang birlamchi mahsulotni yolg‘iz aniqlamaydi.'],['Nitratning ikki vazifasi','Cu(NO₃)₂ da qolgan nitrat bilan NOₓ ga qaytarilgan nitrat bir xil hisoblanmaydi.']],
[['Suvni unutmang','Konsentrlangan H₂SO₄ da a(H₂O)≈1 har doim asosli emas.'],['Nishon va sig‘im','Elektron soni mahsulotdan kelib chiqadi; mahsulot esa sharoit bilan aniqlanadi.']],
[['P–H alohida ulanish','H₃PO₃ da bitta, H₃PO₂ da ikkita P–H mavjud. Bular odatiy O–H protonlari emas.'],['1 proton ≠ 1 elektron','Bir asosli H₃PO₂ fosfat nishonigacha 4 elektron ekvivalent bera oladi.']],
[['Bir modda — ikki rol','H₂O₂ suvga qaytarilsa oksidlovchi, O₂ ga oksidlansa qaytaruvchi.'],['Teng qiyalik sharti','Peroksid grafigida boshqa faolliklar birga teng. Real barqarorlik shu chiziqdan topilmaydi.']],
[['E va E_cell farqi','0,80662 V — qolgan Fe³⁺/Fe²⁺ juftining SHE ga nisbatan potensiali; umumiy element E_cell si emas.'],['Keyingi mavzu','4.3 — passivlanish: qulay ΔG bo‘lsa ham sirt qatlami tezlikni cheklashi mumkin.']]]
(R/'04_02_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
