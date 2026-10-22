from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('terms','Asosiy tushunchalar',['Tushuncha','Mazmun','Chalkashtirmang'],[
['Titrant','Konsentratsiyasi aniqlangan reagent','Faqat taxminiy yorliq yetmaydi'],['Ekvivalentlik','Tanlangan reaksiya stexiometriyasi','Har doim pH=7 emas'],['Oxirgi nuqta','Qabul qilingan kuzatuv signali','Nazariy nuqta bilan aynan bir emas'],['Titrlanadigan kislotalik','Berilgan oxirgacha sarflangan asos','Boshlang‘ich pH ning o‘zi emas']]),
('strong','Kuchli kislota–NaOH; ideal 25 °C',['V_b, mL','Hisobiy pH','Ustun holat'],[
['0','1,00000','Boshlang‘ich kuchli kislota'],['12,50','1,47712','Kislota ortiqcha'],['24,90','3,69810','Ekvivalentlikka yaqin, kislota'],['25,00','7,00000','Suvli neytral ideal nuqta'],['25,10','10,30016','Asos oz ortiqcha'],['50,00','12,52288','Asos ortiqcha']]),
('weak','Shartli HA, K_c=10⁻⁵ mol L⁻¹',['V_b, mL','Hisobiy pH','Yaroqli yo‘l'],[
['0','3,00217','HA va suv balansi'],['12,50','5,00026','Yarim ekvivalentlik; pH≈pKₐ'],['24,90','7,39575','To‘liq balans afzal'],['25,00','8,84950','A⁻ gidrolizi va suv'],['25,10','10,30071','Asos ortig‘i + muvozanat'],['50,00','12,52288','Ortiqcha asos ustun']]),
('poly','H₃PO₄–NaOH; ideal bosqichlar',['Nishon hajm','Ustun oraliq shakl','Hisobiy pH'],[
['25,00 mL; 1 ekv.','H₂PO₄⁻','4,69678'],['50,00 mL; 2 ekv.','HPO₄²⁻','9,67465'],['75,00 mL; 3 ekv.','PO₄³⁻/HPO₄²⁻ va suv','12,18305'],['3 bosqichli formula','Uchta ravshan sakrash shart emas','Taqsimot va zaryadni saqlang']]),
('indicator','Ikki shaklli indikatorning shartli modeli',['pH−pK_In','[In⁻]/[HIn]','In⁻ ulushi'],[
['−2','0,01','0,9901%'],['−1','0,1','9,0909%'],['0','1','50%'],['+1','10','90,9091%'],['+2','100','99,0099%']]),
('ranges','Ma’lumotnoma rang o‘tish intervallari [2]',['Indikator','Odatiy pH intervali','Kislotali → asosli rang'],[
['Metiloranj','3,1–4,4','Qizil → sariq'],['Bromtimol ko‘ki','6,0–7,6','Sariq → ko‘k'],['Fenolftalein','8,3–10,0','Rangsiz → pushti/qizil'],['Tanlash mezoni','Egri chiziqdagi hajm oralig‘i','Faqat bitta pH soni emas']]),
('error','Tanlangan pH mezoni; shartli HA misoli',['pH mezoni','V_oxir, mL','ε_V, %'],[
['4,0','2,24548','−91,0181'],['7,0','24,75248','−0,9901'],['8,3','24,98847','−0,0461'],['10,0','25,04980','+0,1992'],['Haqiqiy V_e','25,00000','0; stexiometrik nishon']]),
('instrument','Instrumental kuzatuv va cheklovlar',['Signal / ishlov','Foydasi','Xavf / shart'],[
['pH(V)','To‘liq egri chiziqni kuzatish','Kalibrlash, T va vaqt'],['ΔpH/ΔV','Tik sohani ajratish','Shovqin kuchayadi'],['Ikkinchi hosila','Infleksiya atrofini baholash','Qadam va silliqlashga sezgir'],['Takroriy o‘lchash','Tarqalishni baholash','Sistematik xatoni yo‘qotmaydi']]),
('quality','Analitik hisob va sifat nazorati',['Bosqich','Namuna / shart','Nazorat'],[
['Alikvota','25,00 mL','Kalibrlangan hajm'],['Titrant','0,1000 mol L⁻¹ NaOH','Standartlangan konsentratsiya'],['Tuzatilgan sarf','24,98 mL','Blank va oxirgi nuqta'],['C_a','0,09992 mol L⁻¹','Bir protonli reaksiya'],['u_r(C_a)','≈0,1756%','Mustaqil standart noaniqliklar'],['Asosiy shart','Yon reaksiya yo‘q','Nishon komponent aniq']])]
out={}
for i,(key,title,headers,rows) in enumerate(data,1):out[key]={'caption':f'3.4.{i}-jadval. {title}','headers':headers,'widths':[3.0,4.9,4.9],'rows':rows}
(R/'03_04_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['Miqdor va kuch','Boshlang‘ich pH teng bo‘lgan ikki eritmaning titrlanadigan kislota miqdori teng bo‘lishi shart emas.'],['Qurilma rasmi','Byuretka va kolba tasviri tushuntiruvchi sxema; muayyan laboratoriyaning fotosurati emas.']],
[['Hajm ortadi','Qolgan proton yoki ortiqcha asos konsentratsiyasi V_a+V_b ga bo‘linadi.'],['7 ning sharti','pH=7 — ayni kuchli juftlikning 25 °C ideal modeli. Ekvivalentlikning universal ta’rifi emas.']],
[['Bu grafik HF emas','K_c=10⁻⁵ mol L⁻¹ berilgan shartli HA ishlatilgan. Aniq kislota tajribasi deb talqin qilinmaydi.'],['Yarim ekvivalentlik','pH≈pKₐ — foydali yaqinlashuv. Suv va haqiqiy muvozanat ulushlari uning aniqligini cheklaydi.']],
[['Har bir ion zaryadi','H₂PO₄⁻, HPO₄²⁻ va PO₄³⁻ balansda 1, 2 va 3 koeffitsiyent bilan qatnashadi.'],['Uchinchi bosqich','Kₐ₃ kichik; suv muvozanati oxirgi hududni kuchli o‘zgartiradi. Uchta teng keskin sakrash kutilmaydi.']],
[['Umumiy HIn modeli','pK_In=7 grafik uchun shartli tanlov. U yon tasvirdagi nitrofenolning o‘lchangan konstantasi emas.'],['Rang va ulush','Bir xil 50:50 ulush barcha indikatorlarda aynan bir ko‘zga ko‘rinadigan rang intensivligini bermaydi.']],
[['Interval universal emas','Ma’lumotnoma qiymatlari erituvchi, harorat va kuzatuv mezoniga bog‘liq. Fenolftalein chegaralari manbalarda farqlanadi.'],['Sakramaga moslang','Indikator intervalini pH o‘qidan V o‘qiga ko‘chiring; analitik sarf qanchaga siljishini baholang.']],
[['Og‘ishning ishorasi','Kislota miqdori titrant sarfidan topilsa, erta signal kamaytiradi, kech signal oshiradi.'],['Bir tomchi doim bir xil emas','Tomchi hajmi qurilma va eritmaga bog‘liq. Uni barcha tajribalarda o‘zgarmas son deb olmang.']],
[['Hosila asbob yozuvi emas','Yon grafik ideal modeldan sonli differensiallash bilan hosil qilingan; haqiqiy tajriba shovqini qo‘shilmagan.'],['Barqarorlashishni kutish','Elektrod javob vaqti va aralashtirish muhim. Bir lahzalik raqam muvozanat qiymati bo‘lmasligi mumkin.']],
[['Mustaqillik farazi','Noaniqliklarni kvadratik qo‘shish misolida korrelatsiyalar nol deb olingan. Real baholashda bu tekshiriladi.'],['Keyingi mavzu','Buferlar va gidrolizning tizimli nazariyasi 3.5 da; bu yerda ular titrlash hududlarini tushuntirish uchun ishlatildi.']]]
(R/'03_04_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
