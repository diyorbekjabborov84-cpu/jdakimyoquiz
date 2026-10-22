from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('equilibrium','Bir xil muvozanat, turli vaqt o‘lchovi',['Kattalik','Dastlabki model','Ikkala k ni 10× oshirish'],[
['k_f, s⁻¹','0,0200','0,2000'],['k_r, s⁻¹','0,00500','0,05000'],['K=k_f/k_r','4','4'],['P ning muvozanat ulushi','0,8000','0,8000'],['Og‘ishning yarim vaqti, s','27,7259','2,77259'],['ΔG°; 298,15 K','−3,43656 kJ mol⁻¹','O‘zgarmaydi']]),
('orders','Tezlik qonuni va birliklar',['Model','k ning birligi','Muhim shart'],[
['v=k','mol L⁻¹ s⁻¹','Nolinchi tartib'],['v=k[S]','s⁻¹','Birinchi tartib'],['v=k[S][H⁺]','L mol⁻¹ s⁻¹','Umumiy ikkinchi tartib'],['v=k_obs[S]','k_obs: s⁻¹','Boshqa ta’sirlar kuzatilgan k da'],['ln([S]_t/[S]_0)','−k_obs t','Qaytmas / mos psevdobirinchi model'],['Umumiy tenglama','Darajalarni o‘zi bermaydi','Elementar bosqich bilan adashtirmang']]),
('barrier','Yon energiya profilining shartli qiymatlari',['Nuqta / tushuncha','G, kJ mol⁻¹','Izoh'],[
['Reagent','0','Ikkala yo‘l uchun bir xil'],['Katalizsiz maksimum','80','Bitta o‘quv cho‘qqisi'],['Katalitik maksimumlar','55; 45','Oraliq minimum bilan ajralgan'],['Katalitik oraliq','10','O‘tish holati emas'],['Mahsulot','−20','Ikkala yo‘l uchun bir xil'],['1-bo‘limdagi model','Boshqa sonli parametrlar','Bu profil K=4 ga moslashtirilmagan']]),
('temperature','E_a=50,0 kJ mol⁻¹ shartli Arrhenius modeli',['T, K','k, s⁻¹','k/k(298,15)'],[
['288,15','0,000496598','0,496598'],['298,15','0,00100000','1'],['308,15','0,00192426','1,92426'],['10 K qo‘shimcha','Doimiy ko‘paytirgich emas','T va E_a ga bog‘liq'],['Harorat nazorati','Kₐ va K_w ham o‘zgarishi mumkin','Bir xil retsept bir xil pH emas']]),
('ph','Parallel maxsus kanallar; ideal 25 °C',['pH','k_obs, s⁻¹','Ustunlik / qiyos'],[
['3,0','0,010010001','H⁺ kanali ustun'],['5,0','0,0001101','H⁺ va fon hissasi'],['6,5','0,0000163246','Ayni model minimumi'],['9,0','0,00101001','OH⁻ kanali ustun'],['11,0','0,1000100001','OH⁻ kanali ustun'],['Parametrlar','k₀=10⁻⁵ s⁻¹','k_H=10; k_OH=100 L mol⁻¹ s⁻¹']]),
('buffer','Bir xil pH=5 da shartli bufer katalizi',['C_T, mol L⁻¹','k_maxsus, s⁻¹','Jami k_obs, s⁻¹'],[
['0','0,0001101','0,0001101'],['0,0100','0,0001101','0,0002101'],['0,1000','0,0001101','0,0011101'],['HA/A⁻ ulushlari','Haqiqiy muvozanatda 1:1','Har biri C_T/2'],['Berilgan koeffitsiyentlar','k_HA=0,0200 L mol⁻¹ s⁻¹','k_A=0; oldindan berilgan faraz'],['Bitta chiziq','k_HA va k_A ni ajratmaydi','Og‘irlashtirilgan yig‘indi o‘lchanadi']]),
('cycle','Formal proton tashish sikli',['Bosqich','Yozuv','Mazmun'],[
['Protonlanish','S+H⁺ ⇌ SH⁺','Faolroq holat hosil bo‘lishi mumkin'],['Qayta tuzilish','SH⁺ ⇌ PH⁺','S va P — teng atom tarkibli belgilar'],['Deprotonlanish','PH⁺ ⇌ P+H⁺','Proton qayta tiklanadi'],['Yig‘indi','S ⇌ P','H⁺ umumiy sarfda yo‘q'],['Neytrallanish','H⁺+OH⁻ → H₂O','Stexiometrik sarf; o‘zi katalitik sikl emas']]),
('inorganic','Noorganik katalitik ta’sirlarning farqi',['Tizim turi','Asosiy rol','Talqin chegarasi'],[
['H₃O⁺ / OH⁻','Erituvchi ionlarining katalitik hissasi','Maxsus kislota–asos katalizi'],['Bufer HA / A⁻','Boshqa donor/akseptor hissasi','Umumiy kataliz; muhit nazorati'],['NO/NO₂ formal sikli','Redoks vositachilik','To‘liq sanoat mexanizmi emas'],['V oksidli kontakt tizimi','SO₂ oksidlanishidagi kataliz','Faol faza oddiy bitta formula emas'],['Metall koordinatsiyasi','Ligand faolligi va proton tashish','Faqat pH bilan izohlab bo‘lmaydi']]),
('checks','Dalil va xulosaning chegaralari',['Kuzatuv','Nimani ko‘rsatishi mumkin?','Nimani o‘zi isbotlamaydi?'],[
['Eksponenta','Mos k_obs bilan ishchi model','Barcha bosqichlar birinchi tartibli'],['pH profili','Faol shakllar yoki H⁺/OH⁻ ta’siri','Yagona aniq mexanizm'],['Buferga bog‘liqlik','Umumiy katalitik/muhit hissasi','k_HA va k_A ning alohida qiymati'],['Arrhenius qiyaligi','Ishchi E_a','Bitta bog‘ uzilish energiyasi'],['Izotop effekti','Proton dinamikasi haqida dalil','Yagona o‘tish holati'],['Katalizator bilan tezlashish','Boshqa kinetik yo‘l','Bir xil umumiy reaksiya K si oshishi']])]
out={}
for i,(key,title,headers,rows) in enumerate(data,1):out[key]={'caption':f'3.6.{i}-jadval. {title}','headers':headers,'widths':[3.0,4.9,4.9],'rows':rows}
(R/'03_06_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['Oxirgi ulush saqlanadi','Yopiq ideal bir xil reaksiya uchun katalizator vaqt o‘lchovini o‘zgartiradi, termodinamik K ni emas.'],['Ikki xil yarim vaqt','Bu grafikda muvozanatdan og‘ish yarimlanadi. Qaytmas S ning yarmi sarflanishi bilan aynan bir emas.']],
[['Daraja va koeffitsiyent','Umumiy stexiometrik koeffitsiyentlarni ko‘r-ko‘rona tezlik darajalari deb ko‘chirmang.'],['k_obs shartli','pH yoki katalizatorning aktiv shakli vaqt davomida o‘zgarsa, doimiy k_obs modeli buzilishi mumkin.']],
[['Profil mustaqil model','80/55/45/−20 qiymatlari o‘quv sonlari. Ular 1-bo‘limdagi K=4 ga yoki real kislota tajribasiga tegishli emas.'],['Ikki xil ΔG','ΔG° — umumiy termodinamika; ΔG‡ — tanlangan kinetik yo‘l to‘sig‘i. Bir xil birlik bir xil ma’no degani emas.']],
[['Kelvin zarur','1/T yozuviga °C emas, K qo‘yiladi. ln(k/k_ref) argumenti o‘lchamsiz.'],['E_a bog‘ energiyasi emas','Murakkab tizimdagi ko‘rinma E_a bir nechta muvozanat va bosqichlarning ta’sirini birlashtirishi mumkin.']],
[['Maxsus nimani bildiradi?','Suvda kuzatilgan kataliz erituvchining H⁺/OH⁻ ionlariga tegishli. Bu kuchli kislota nomining sinonimi emas.'],['To‘yinish ham mumkin','Tez protonlanish muvozanati to‘yinganda H⁺ bo‘yicha tartib noldan farqli boshqa hududlarga o‘tadi.']],
[['Bufer faol bo‘lishi mumkin','Bir xil pH da ham HA yoki A⁻ bevosita kinetik hissa berishi mumkin. Ion kuchi va muhit nazorat qilinadi.'],['α_Br ≠ α','Brønsted kinetik qiyaligi dissotsiatsiya ulushi emas. Bitta oiladagi korrelyatsiyani boshqasiga shartsiz o‘tkazmang.']],
[['Qayta hosil bo‘lish','Katalizator har bir bosqichda o‘zgarmas emas; umumiy siklda tiklanadi.'],['NH₃ rasmi','NH₃ proton akseptorining tuzilish misoli. Formal sikldagi barcha S yoki P aynan shu modda degani emas.']],
[['NO₂ radikal','Neytral NO₂ toq elektronli zarracha. Yon shar–tayoqcha tasviri to‘liq Lewis yoki elektron zichlik modeli emas.'],['NOₓ xavfi','Zaharli gazlar haqida konseptual sikl berilgan, laboratoriya bajarish yo‘riqnomasi emas.']],
[['Bir dalil yetmaydi','Tezlik tartibi, pH, bufer, T va izotop kuzatuvlari birgalikda tekshiriladi.'],['3-bob yakuni','Muvozanat tarkibni, kinetika vaqtni yoritadi. Keyingi mavzu: 4.1 — neytrallanish va tuz hosil bo‘lishi.']]]
(R/'03_06_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
