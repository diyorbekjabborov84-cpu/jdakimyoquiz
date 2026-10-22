from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('families','Noorganik bufer juftliklari',['Juftlik','Proton donor / akseptor','Muhim cheklov'],[
['H₂PO₄⁻/HPO₄²⁻','H₂PO₄⁻ donor; HPO₄²⁻ akseptor','Metall ionlari va boshqa fosfat shakllari'],['NH₄⁺/NH₃','NH₄⁺ donor; NH₃ akseptor','NH₃ uchuvchanligi va T'],['Karbonat oilasi','Tanlangan tutash bosqich','CO₂ bilan ochiq/yopiq tizim farqi'],['Shartli HA/A⁻','Bu mavzuda K_c=10⁻⁵','Aniq HF deb qabul qilinmaydi']]),
('ratio','Nisbatning ma’nosi; ideal miqdorlar taqribi',['n(A⁻)/n(HA)','pH−pKₐ, taxminan','Amaliy ma’no'],[
['0,01','−2','Asosli shakl zaxirasi kichik'],['0,1','−1','Ko‘pincha ishchi oraliq chekkasi'],['1','0','Juftlik hissasining maksimal β sohasi'],['10','+1','Kislotali shakl kamaygan'],['100','+2','Asos qo‘shishga qarshilik cheklangan']]),
('addition','100,0 mL buferga 10,00 mL 0,1000 M reagent',['Holat','HA / A⁻ miqdorlari','Ideal pH'],[
['Dastlab','5,000 / 5,000 mmol','5,00017'],['NaOH qo‘shilgach','4,000 / 6,000 mmol; stexiometrik','5,17622; to‘liq balans'],['HCl qo‘shilgach','6,000 / 4,000 mmol; stexiometrik','4,82421; to‘liq balans'],['Yakuniy hajm','110,0 mL; qo‘shiluvchan','C_T=0,090909 mol L⁻¹'],['Formula chegarasi','Bir shakl tugasa','Ortiqcha reagentni hisoblang']]),
('capacity','Sig‘im va nisbatni farqlash',['Kattalik / holat','Natija','Ma’no'],[
['C_T=0,1000; pH=5','β_juft≈0,0575646','mol L⁻¹ pH⁻¹'],['Suv hissasi; pH=5','β_suv≈0,0000230','Juftlikdan alohida had'],['Jami; shu nuqtada','β≈0,0575877','Doimiy hajm va C_T'],['C_T o‘n marta kam','Juftlik hissasi o‘n marta kam','Bir xil pH teng sig‘im emas'],['Katta Δb qo‘shilsa','β yo‘l bo‘ylab o‘zgaradi','Boshlang‘ich β yetarli emas']]),
('dilution','Teng analitik HA/NaA; K_c=10⁻⁵ mol L⁻¹',['C_T, mol L⁻¹','To‘liq ideal pH','Miqdorlar taqribi'],[
['0,1000','5,00017','5'],['10⁻³','5,01672','5'],['10⁻⁵','5,55130','5 — farq katta'],['10⁻⁷','6,89518','5 — yaroqsiz'],['10⁻⁹','6,99894','Suv chegarasiga yaqin']]),
('anion','Anion gidrolizi va tekshiruv',['Tizim / bosqich','Yozuv','Shart'],[
['NaA ning erishi','NaA → Na⁺+A⁻','Ionlarga ajralish'],['Anionning proton olishi','A⁻+H₂O ⇌ HA+OH⁻','Gidroliz muvozanati'],['Konstanta','K_b,c=K_w,c/K_c','Bir xil T va ideal shkala'],['Kichik gidroliz','[OH⁻]≈√(K_b,cC)','Suv va sarflangan ulush kichik'],['Shartli NaA; C=0,0100','Ideal pH≈8,50015','K_c(HA)=10⁻⁵ mol L⁻¹']]),
('cation','Kation kislotaligi',['Tizim','Proton donor','Chegara / natija'],[
['NH₄Cl','NH₄⁺','Cl⁻ balansda saqlanadi'],['0,0100 M NH₄Cl','K_c≈5,6×10⁻¹⁰ mol L⁻¹','Ideal pH≈5,62557'],['[Al(H₂O)₆]³⁺','Koordinatsiyalangan H₂O','Ligand proton beradi'],['Metall gidrolizi','Ketma-ket gidrokso shakllar','Cho‘kma, komplekslar, polimerlar'],['Na⁺ modeli','Sezilarli proton almashinuvi yo‘q','Barcha metallarga umumlashtirmang']]),
('both','Ikki faol ion va amfiprot shakllar',['Tizim; C=0,0100 M','To‘liq ideal pH','Hisobning xususiyati'],[
['NH₄F','6,23592','NH₄⁺ va F⁻ birga; suv saqlangan'],['NH₄F, suvni tashlagan','6,22282','Cheklangan yarim yig‘indi taqribi'],['NaH₂PO₄','4,78834','Barcha fosfat bosqichlari'],['Na₂HPO₄','9,52671','Barcha fosfat bosqichlari'],['H₂PO₄⁻ / HPO₄²⁻','Amfiprot ionlar','Proton ham beradi, ham oladi']]),
('checks','Formula o‘rniga modelni tanlash',['Savol','Tayanch','Xato belgisi'],[
['Qaysi oilalar bor?','HA/A⁻; BH⁺/B; poliprotik','Kerakli shakl tashlab ketilgan'],['Qaysi ionlar kuzatuvchi?','Na⁺, Cl⁻ va boshqalar','Zaryad balansidan o‘chirilgan'],['Nisbat nima?','Muvozanatmi yoki analitikmi?','Juda suyultirilganda ham aynan pKₐ'],['Sig‘im qanday?','C_T, V, qo‘shimcha miqdori','Faqat boshlang‘ich pH ga qaralgan'],['Model yopiqmi?','CO₂, NH₃, cho‘kma, kompleks','Bir fazali model shartsiz ishlatilgan'],['Yechim to‘g‘rimi?','Modda + zaryad + K','Manfiy konsentratsiya yoki balans yo‘q']])]
out={}
for i,(key,title,headers,rows) in enumerate(data,1):out[key]={'caption':f'3.5.{i}-jadval. {title}','headers':headers,'widths':[3.0,4.9,4.9],'rows':rows}
(R/'03_05_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
[['Tutashlik sharti','Juftlik bir proton bilan farqlanadi. Istalgan ikkita kislota yoki tuz aralashmasi bufer bo‘lavermaydi.'],['pH qotib qolmaydi','Bufer tarkibini o‘zgartirib javob beradi. Zaxira kamaygach o‘zgarishga qarshilik ham pasayadi.']],
[['Nisbatning yo‘nalishi','Asosli shakl suratda, kislotali shakl maxrajda. NH₃/NH₄⁺ va HPO₄²⁻/H₂PO₄⁻ misollarida ham shu tartib.'],['Analitik ≠ muvozanat','Tayyorlashdagi miqdorlar nisbatini [A⁻]/[HA] ga tenglashtirish alohida taqribdir.']],
[['Avval stexiometriya','Kuchli reagent qaysi shaklni qancha sarflashini hisoblang; manfiy miqdorni logarifmga kiritmang.'],['Grafik sharti','q yakuniy konsentratsiya bo‘yicha taqqoslash parametri. Bir idishga o‘zgarmas hajmda quyish tajribasi emas.']],
[['β ning birligi','Bu yerda mol L⁻¹ pH⁻¹. Butun idishning mol zaxirasi va birlik hajmdagi sig‘imni adashtirmang.'],['Maksimum nimaniki?','pH≈pKₐ da juftlik hissasi maksimum. Suv hadlari bor umumiy β ga global hukm chiqarilmaydi.']],
[['Nisbat saqlansa ham','Suyultirishdan keyin analitik nisbat saqlanadi; shakllar qayta muvozanatlangani uchun haqiqiy nisbat o‘zgarishi mumkin.'],['Haqiqiy eritma','T, ion kuchi, CO₂, uchuvchan NH₃ va cho‘kma — faqat kalkulyator bilan yo‘qolmaydigan cheklovlar.']],
[['Ikki xil γ','γ_h — shu matnda gidroliz ulushi; faollik koeffitsiyenti γ bilan bir kattalik emas.'],['Ulush va miqdor','Suyultirishda gidroliz ulushi ortib, mutlaq OH⁻ konsentratsiyasi kamayishi mumkin.']],
[['Proton qayerdan?','NH₄⁺ da ionning o‘zi proton donor; Al akvakompleksida esa suv ligandining O–H guruhi donor.'],['Kuzatuvchi zaryad','Cl⁻ reaksiyada sezilarli qatnashmasa ham, elektr neytrallik tenglamasidan olib tashlanmaydi.']],
[['HF qiymati alohida','NH₄F hisobida HF uchun K_c≈6,4×10⁻⁴ mol L⁻¹. Boshqa grafiklarning shartli HA konstantasi emas.'],['Amfiprot tushunchasi','Bitta ionning ikki yo‘nalishdagi proton almashinuvi. Bu ikkita turli ion gidrolizi bilan aynan bir emas.']],
[['Qayta qo‘yish','Topilgan konsentratsiyalarni moddiy balans, zaryad va K ifodalariga qayta joylashtiring.'],['Keyingi savol','3.6 da jarayon tezligi va kataliz ko‘riladi. Muvozanatdagi tarkib bilan unga yetishish tezligi boshqa xossalardir.']]]
(R/'03_05_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
