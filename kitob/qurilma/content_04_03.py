from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('distinction','Immun holat, passiv holat va oddiy cho‘kma',[
 ['Immun holat','Metall termodinamik barqaror','Berilgan potensial/pH va turlar uchun'],
 ['Faol korroziya','Anod erish tezligi katta','Mahsulotlar chetlanadi; parda yetarli emas'],
 ['Passiv holat','Sirt to‘sig‘i erishni sekinlatadi','Kichik, ammo noldan farqli tezlik mumkin'],
 ['G‘ovak cho‘kma','Yomon qoplash yoki yopishish','Oksid borligi himoya isboti emas'],
 ['Tashqi tok nol','i_a+i_c=0','Ichki qisman toklar nol bo‘lishi shart emas']]),
('films','Parda tarkibi va uning shartli tasviri',[
 ['Fe','Fe(II)/Fe(III), oksid/oksigidroksid','Yagona sof kristall formula emas'],
 ['Cr / zanglamas po‘lat','Cr(III) ga boy to‘siq qatlam','Tashqi gidratlangan qism va qotishma ta’siri'],
 ['Al','Oksid/gidroksidli sirt','Kislota va ishqorda erishi mumkin'],
 ['Ti','Oksidli himoya','Barcha muhitlarga mutlaq inert emas'],
 ['Samarali to‘siq','Uzluksizlik, yopishish, transport','Faqat qalinlikning o‘zi yetmaydi']]),
('polarization','Sun’iy anod taxminiy hisobining to‘rt hududi',[
 ['Faol','E_rel=0…0,300 V','i 10⁻⁶ dan 10⁻³ A cm⁻² gacha'],
 ['Faol–passiv o‘tish','E_rel=0,300…0,450 V','Tok 3 tartibga pasayadi'],
 ['Passiv','E_rel=0,450…0,800 V','i_pass=10⁻⁶ A cm⁻²'],
 ['Yuqori potensial','E_rel>0,800 V','Qo‘shimcha anod tok ortishi taxminiy hisobi'],
 ['Muhim cheklov','Ixtiyoriy o‘quv etaloni','Real metallning xavfsiz ish oynasi emas']]),
('acids','Kislota nomi va sirt holatini birga talqin qilish',[
 ['Sovuq konsentrlangan HNO₃','Fe, Cr, Al passivlanishi mumkin','Metall navi, sirt va harorat muhim'],
 ['Oksidlovchi katod yo‘li','Potensialni passiv sohaga olib kelishi mumkin','E° ning o‘zi yetarli emas'],
 ['Sovuq konsentrlangan H₂SO₄','Ayrim temirli materiallar sekin yemiriladi','Parda, suv faolligi va transportni ajrating'],
 ['Harorat / suyultirish','Erish va parda saqlanishi o‘zgaradi','Idish materiali nazariy qoidadan tanlanmaydi'],
 ['Sun’iy ikki katod shartli hisobi','Faol: E_rel=0,150 V; passiv: 0,700 V','i mos ravishda 3,162×10⁻⁵ va 10⁻⁶ A cm⁻²']]),
('kinetics','L₀=0,500 nm; L_lim=4,00 nm; k_g=0,0200 s⁻¹',[
 ['v_diss=0,0200 nm s⁻¹','L_inf=3,00 nm','O‘sish–erish balansi'],
 ['v_diss=0,0600 nm s⁻¹','L_inf=1,00 nm','Boshqa musbat limit'],
 ['v_diss=0,0800 nm s⁻¹','L_inf=0','Parda kamayadigan chegaraviy taxminiy hisob'],
 ['1/k_g','50,0 s','Yechimning relaksatsiya vaqt ko‘lami'],
 ['L_inf>0','Musbat qalinlik sharti','Himoya va uzluksizlik alohida tekshiriladi']]),
('pitting','Mahalliy korroziyada o‘zaro kuchayuvchi omillar',[
 ['Metall ionlari chiqishi','Al → Al³⁺+3e⁻ misoli','Mahalliy anod joyi'],
 ['Gidroliz','Mahalliy H⁺ ortishi mumkin','Tashqi pH bilan teng bo‘lishi shart emas'],
 ['Ionlar ko‘chishi','Cl⁻ va boshqa ionlar muvozanati','Xloridning oksidlanishi shart emas'],
 ['Cheklangan transport','Chuquroqda boshqa kimyo','Tirqish geometriyasi ham muhim'],
 ['E_rp<E_pit bo‘lishi mumkin','Boshlanish va davom etish chegarasi boshqa','Etalon, vaqt va sirt tarixini yozing']]),
('highpotential','Katta anod tokini bitta sababga bog‘lamang',[
 ['Transpassiv erish','Parda markazi yuqori darajaga o‘tadi','Cr(III)→Cr(VI) misoli'],
 ['Kislorod ajralishi','Suv anodda oksidlanadi','Tok ortishi metall erishining o‘zi emas'],
 ['Mahalliy buzilish','Cl⁻ li tizimda oldinroq bo‘lishi mumkin','Pitting bilan transpassivlik boshqa'],
 ['Mexanik shikast','Yalang‘och joy ochiladi','Elektrokimyoviy yuqori valentli erish emas'],
 ['Material farqi','Elektron/ion transporti boshqacha','Barcha oksidlar bir xil tutmaydi']]),
('evidence','Usul qaysi savolga javob beradi?',[
 ['Potensial–tok / vaqt','Faol–passiv o‘tish va relaksatsiya','Skan tezligi va iR xatosi tekshiriladi'],
 ['R_p / kichik-signal','Mos shartli hisobda i_corr bahosi','Tafel qiyaligi yoki B kerak'],
 ['XPS','Sirt kimyoviy holati','Yakka o‘zi chuqurcha tezligini bermaydi'],
 ['Mikroskopiya','Pitting, darz va morfologiya','Kimyoviy tarkib uchun qo‘shimcha usul'],
 ['Eritmadagi metall / massa','Jami yo‘qotish yoki erish','Kichik o‘rtacha son mahalliy xavfni yashiradi']]),
('worked','Al→Al³⁺; i_M=1,000 μA cm⁻²; A=10,00 cm²; 24 soat',[
 ['Metall erish toki','i_M A','10,00 μA'],
 ['Elektr miqdori','It','0,8640 C'],
 ['Massa ekvivalenti','QM/(3F)','0,08054 mg'],
 ['Bir tekis qalinlik','m/(ρA)','0,02983 μm'],
 ['Faol maydon ulushi','f=0,001000','fA=0,01000 cm²'],
 ['Mahalliy tok zichligi','i_M/f','1,000 mA cm⁻²'],
 ['Mahalliy o‘rtacha ekvivalent','h_uniform/f','29,83 μm; maksimal pit chuqurligi emas']])]
out={}
for i,(key,title,rows) in enumerate(data,1):out[key]={'caption':f'4.3.{i}-jadval. {title}','headers':['Obyekt / bosqich','Mazmun / hisob','Chegara / natija'],'widths':[3.8,4.4,4.6],'rows':rows}
(R/'04_03_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
 [['Nol tashqi tok','Ochiq zanjirda anod va katod qisman toklari o‘zaro qoplanishi mumkin. Metall baribir eriydi.'],['Immun ≠ passiv','Immun holat termodinamik; passiv holat sirt to‘sig‘i va kichik erish tezligi bilan bog‘liq.']],
 [['Formula — soddalashtirish','Cr₂O₃ qisqa yozuvi real pardani butunlay sof stexiometrik kristall deb tasdiqlamaydi.'],['Qalinlik yetmaydi','Uzluksizlik, yopishish va transport xossalarisiz qalin cho‘kma yaxshi himoya emas.']],
 [['Uch tartibli pasayish','Grafikdagi 10⁻³→10⁻⁶ A cm⁻² — 1000 marta pasayish, lekin tok nol emas.'],['Etalonni ayting','E_rel o‘quv siljish potensiali. Uni SHE yoki SCE qiymati deb qabul qilmang.']],
 [['E° va tezlik','Katta E° passivlanishni yolg‘iz kafolatlamaydi: katod reaksiyasi kinetikasi ham kerak.'],['Har doim «ko‘proq» emas','Kuchliroq oksidlovchi passiv hududdan tashqariga ham olib chiqishi mumkin.']],
 [['Bir taxminiy hisoblar, uch limit','Vaqt ko‘lami 50 s, ammo v_diss o‘zgarsa qalinlik limiti boshqa bo‘ladi.'],['Tiklanish shartli','Tirnalgan joy mos muhit bo‘lsa qayta qoplanadi; darhol tiklanishga mutlaq kafolat yo‘q.']],
 [['Mahalliy pH','Chuquroqda gidroliz va transport cheklanishi tashqi eritmadan boshqa tarkib yaratadi.'],['Tarix ahamiyatli','Pitting boshlanishi va mavjud chuqurchaning so‘nishi bir xil chegara bilan ifodalanmaydi.']],
 [['Tokning manbasini ajrating','Metall erishi, parda o‘sishi va O₂ ajralishi bir xil tok samaradorligi emas.'],['Cr(VI) xavfi','Formal tenglama texnologik retsept emas. Cr(VI) turlari jiddiy xavfli.']],
 [['R_p birliklari','Bu matnda Ω cm²: maydonga normallangan qarshilik. Oddiy Ω bilan almashtirmang.'],['Bitta dalil yetmaydi','Kichik massa yo‘qotilishi, yaltiroq sirt yoki gaz chiqmasligi pitting yo‘qligini isbotlamaydi.']],
 [['Maydon ulushi muhim','f=0,001 bo‘lsa bir xil hajm yo‘qotilishi mahalliy o‘rtacha chuqurlikni 1000 marta oshiradi.'],['Keyingi mavzu','4.4 — kompleks va cho‘kma hosil qilish. Komplekslanish sirt hamda eruvchanlikka ta’sir qiladi.']]]
(R/'04_03_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
