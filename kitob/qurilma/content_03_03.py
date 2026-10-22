from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
specs=[
('definition','pH va konsentratsiya',['Kattalik','To‘g‘ri ma’no','Ishlatish sharti'],[
['pH','−lg a(H⁺)','Faollik o‘lchamsiz'],['m(H⁺)','mol kg⁻¹; molallik','IUPAC ifodasidagi shkala'],['h=[H⁺]','mol L⁻¹; molyar konsentratsiya','Ideal masalalardagi o‘zgaruvchi'],['−lg(h/c°)','Konsentratsion yaqinlashuv','γ≈1 va mos suyultirish'],['pKₐ','−lg Kₐ','pH bilan aynan bir son emas']]),
('balances','Modelni yopadigan tenglamalar',['Tayanch','HA uchun yozuv','Tekshiruv'],[
['Moddiy balans','C=[HA]+[A⁻]','Kislota oilasi saqlanadi'],['Zaryad balansi','h=[A⁻]+[OH⁻]','Faqat HA va suv uchun'],['Kislota muvozanati','K_c=h[A⁻]/[HA]','Ideal konsentratsion model'],['Suv muvozanati','K_w,c=h[OH⁻]','25 °C da 10⁻¹⁴ (mol L⁻¹)²'],['Kuchli HX qo‘shilsa','h=C_s+[A⁻]+[OH⁻]','[X⁻]=C_s; boshqa ionlar yo‘q']]),
('strong','Kuchli bir asosli kislota; 25 °C ideal model',['C, mol L⁻¹','Suv bilan pH','Suvsiz −lg(C/c°)'],[
['10⁻³','3,00000','3'],['10⁻⁶','5,99572','6'],['10⁻⁷','6,79101','7'],['10⁻⁸','6,97829','8 — yaroqsiz'],['C → 0','7 ga pastdan intiladi','Cheksiz ortish fizik emas']]),
('weak','HA uchun hisob bosqichlari',['Model','Tenglama / natija','Qachon yaroqli?'],[
['Suv saqlanadi','h=CK_c/(K_c+h)+K_w,c/h','Ushbu ideal tizimning to‘liq hisobi'],['Suv kichik','x²+K_cx−K_cC=0','h≈[A⁻] tekshirilgan'],['Kichik x ham olinadi','h≈√(K_cC)','x/C kichik va suv kichik'],['C=0,01; K_c=10⁻⁵','Ideal pH≈3,50687','α≈3,1127%; kichik x nisbati'],['C=10⁻⁴; K_c=10⁻⁵','Ideal pH≈4,56838','α≈27,02%; kvadrat model kerak'],['C=10⁻⁸; K_c=10⁻⁵','Ideal pH≈6,97852','Suvni tashlab bo‘lmaydi']]),
('mixstrong','Kuchli kislotalar aralashmasini hisoblash',['Bosqich','Hisob','Natija'],[
['Birinchi miqdor','0,0100×0,0100','1,00×10⁻⁴ mol'],['Ikkinchi miqdor','0,00100×0,0300','3,00×10⁻⁵ mol'],['Jami miqdor','n₁+n₂','1,30×10⁻⁴ mol'],['Yakuniy hajm','0,0100+0,0300','0,0400 L; qo‘shiluvchan deb olingan'],['C_s va ideal pH','0,000130/0,0400','0,003250 mol L⁻¹; pH≈2,48812']]),
('mixweak','Umumiy H⁺ ta’siri: shartli HA, K_c=10⁻⁵',['Holat / kattalik','Faqat HA','HA + kuchli HX'],[
['C(HA), mol L⁻¹','0,0100','0,0100'],['C_s, mol L⁻¹','0','0,00100'],['[A⁻], mol L⁻¹','0,0003112673','0,0000908397'],['α, %','3,1127','0,9084'],['Ideal pH','3,50687','2,96224'],['O‘zgarmagan kattalik','Berilgan K_c','Berilgan K_c']]),
('diprotic','H₂SO₄; birinchi bosqich to‘liq, ikkinchisi muvozanatli',['Kattalik','Ideal natija','Nazorat'],[
['C, mol L⁻¹','0,0100','S oilasining analitik jami'],['K₂,c, mol L⁻¹','0,012','25 °C; γ≈1 deb olingan'],['[HSO₄⁻], mol L⁻¹','0,00547583','C−x'],['[SO₄²⁻], mol L⁻¹','0,00452417','x'],['h, mol L⁻¹','0,01452417','Bir va ikki zaryadni farqlang'],['Ideal pH','1,83791','O‘lchangan pH emas']]),
('quality','Aniqlik chegaralari',['Omil','Nima o‘zgaradi?','Nimani tekshirish kerak?'],[
['Faollik koeffitsiyenti','a bilan konsentratsiya farqi','Shkala, konvensiya, ion kuchi'],['Harorat','Kₐ va K_w','Konstantalarning T si'],['Yakuniy hajm','Barcha analitik C lar','Qo‘shiluvchanlik farazi'],['Juda kichik C','Suv va tashqi aralashmalar hissasi','CO₂, iz ionlar, o‘lchash chegarasi'],['Ko‘p hisobiy raqam','Model ildizining yozilishi','Tajriba aniqligi bilan teng emas']]),
('checks','Yechimni tanlash va rad etish mezonlari',['Vaziyat','Boshlang‘ich yo‘l','Xato belgisi'],[
['Kuchli kislota','h=strong(C, K_w,c)','Suyultirilgan kislota uchun pH=8'],['HA','Balanslar va K_c','α>1 yoki manfiy konsentratsiya'],['Kuchli + kuchli','Miqdor → hajm → C_s','pH larni o‘rtachalashtirish'],['Kuchli + HA','Kuchli anionni balansga kiriting','[A⁻]=h deb qo‘yish'],['Ko‘p bosqichli','Har bir bosqich va zaryad','Har doim h=nC'],['Har qanday model','Qayta qo‘yish va birlik nazorati','Balans yoki K tiklanmaydi']])]
out={}
for i,(key,title,headers,rows) in enumerate(specs,1):out[key]={'caption':f'3.3.{i}-jadval. {title}','headers':headers,'widths':[3.0,4.9,4.9],'rows':rows}
(R/'03_03_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['Logarifmning argumenti','a o‘lchamsiz. Konsentratsiya ifodasida c° standart konsentratsiya yashirib yuborilmasin.'],['Suvdagi H⁺ yozuvi','H⁺ proton faolligi uchun odatiy qisqa yozuv. Suvda u solvatlangan shakllar bilan bog‘liq.']],
[['Birliklar izchil bo‘lsin','Bu mavzuda K_c mol L⁻¹, K_w,c esa (mol L⁻¹)². Termodinamik konstantalar o‘lchamsiz.'],['Zaryad koeffitsiyenti','Bir mol SO₄²⁻ ikki mol manfiy zaryad ekvivalentini beradi, lekin bir mol S markazi saqlaydi.']],
[['HCl rasmi haqida','Neytral H–Cl tasviri boshlang‘ich molekula ulanishini ko‘rsatadi. Suyultirilgan suvli modelda asosiy shakllar H₃O⁺ va Cl⁻.'],['Suv qayta muvozanatlanadi','Kislota qo‘shilgach suvning H⁺ va OH⁻ hissalari dastlabki 10⁻⁷ qiymatda qotib qolmaydi.']],
[['HF: faqat tuzilish tasviri','Grafikdagi K_c=10⁻⁵ shartli HA uchun. Bu qiymat HF konstantasi sifatida berilmagan.'],['Ikki soddalashtirish','Suvni tashlash va x≪C deb olish — alohida taxminlar; biri ikkinchisini kafolatlamaydi.']],
[['Asosiy tartib','Avval mol, keyin yakuniy litr, oxirida logarifm. pH ni moddalar miqdoridek qo‘shib bo‘lmaydi.'],['Hajm farazi','V₁+V₂ ishlatilsa, hajmlar qo‘shiluvchan deb olinganini ayting. Bu barcha eritmalarda aniq tenglik emas.']],
[['Umumiy proton','HX borligida HA uchun α=K_c/(K_c+h) saqlanadi; α=h/C esa yaramaydi.'],['O‘zgarmas narsa nima?','Berilgan ideal K_c saqlanadi, lekin h va tarkib o‘zgaradi. α ning kamayishi kislotaning tabiatan kuchsizlashishi emas.']],
[['Molekula va eritma','H₂SO₄ tasviri ulanishni ko‘rsatadi. Yonidagi grafik eritmadagi ion muvozanati modeli, molekula rasmi emas.'],['Ikkinchi bosqich','HSO₄⁻ ham proton donor. Uning qolgan ulushi nol deb olinmasa h=2C avtomatik chiqmaydi.']],
[['γ=0,75 misoli','Shartli, molal shkala va konvensiyaga tegishli. Bu koeffitsiyentni boshqa ionlarga yoki barcha eritmalarga ko‘chirmang.'],['Kalibrlash zarur','pH-metr faqat son ko‘rsatadigan elektrod emas; standartlar, harorat va o‘lchash tizimi natijaga kiradi.']],
[['Muvozanatni qayta tiklang','Topilgan konsentratsiyalarni K ifodasiga qayta qo‘ying; faqat kalkulyatorning ildiziga ishonmang.'],['Mavzular chegarasi','Titrlash egri chiziqlari va indikatorlar — 3.4; buferlar va gidrolizning tizimli tahlili — 3.5.']]]
(R/'03_03_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
