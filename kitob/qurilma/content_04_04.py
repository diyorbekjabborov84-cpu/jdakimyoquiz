from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'matn'
data=[
('roles','Eritilgan metallning turlari va ularning vazifasi',[
 ['Erkin metall ioni','Koordinatsion holda, lekin ligand bog‘lanmagan','K_sp va β hisoblarida ishlatiladi'],
 ['Bir ligandli kompleks','[ML] kabi oddiy turlar','Bosqichli konstantalarda'],
 ['Ko‘p ligandli kompleks','[ML₂], [ML₃] va boshqalar','β_2, β₃ umumiy konstantalar'],
 ['Gidroksokompleks','pH ga bog‘liq paydo bo‘ladi','Amfoterlik bilan bog‘liq'],
 ['Qattiq fazadagi metall','Eritilmagan, cho‘kma tarkibida','Modda balansining alohida qismi'],
 ['Ligandning o‘zi','Metallga bog‘langan yoki erkin','Balansga alohida kiritiladi']]),
('saturation','Q_sp va K_sp taqqoslashining natijalari',[
 ['Q_sp < K_sp','Erish termodinamik jihatdan qulay','Qattiq faza barqaror qoladi'],
 ['Q_sp = K_sp','Tanlangan faza bilan muvozanat','To‘yingan eritma'],
 ['Q_sp > K_sp','Cho‘kishga moyil holat','Zarracha tez paydo bo‘lishi shart emas'],
 ['Qattiq faza yo‘q','Sodda tenglik qo‘shimcha shart','Sig‘im chegarasi bilan to‘qnashuv mumkin'],
 ['Nukleatsiya to‘sig‘i','Kinetik, termodinamikdan alohida','Kolloid barqarorlikni belgilaydi'],
 ['Tovush o‘zgarishi','Chiqish natijasi, konstanta emas','Faza tarkibi alohida aniqlanadi']]),
('constants','Kompleks barqarorligi konstantalari va ularning bog‘lanishi',[
 ['K_1','Birinchi ligand qo‘shilishi','[ML]/([M][L])'],
 ['K_2','Ikkinchi ligand qo‘shilishi','[ML₂]/([ML][L])'],
 ['β_2','Umumiy hosil bo‘lish konstantasi','K_1·K_2; K_2 bilan chalkashtirilmaydi'],
 ['K_d','Dissotsiatsiya konstantasi','Faqat teskari reaksiyaning konstantasi'],
 ['β′_2,c','Shartli hosil bo‘lish konstantasi','Faqat ligandning erkin shakliga nisbatan'],
 ['β_2,c (kumush–ammiak)','1,7×10⁷ L² mol⁻²','25 °C; taxminiy hisoblarda ishlatiladigan qiymat']]),
('protonation','Protonlanish va shartli konstantaning pH ga bog‘liqligi',[
 ['pH = 7,25','α_L ≈ 0,00990','Erkin NH₃ ulushi juda kichik'],
 ['pH = 9,25','α_L ≈ 0,500','Teng ikki shakl'],
 ['pH = 11,25','α_L ≈ 0,990','Erkin ligand deyarli to‘liq'],
 ['β′_2,c = β_2,c·α_L²','Ikki ligandli holat','pH ta’siri kvadrat bilan kuchayadi'],
 ['B_u = [NH₃]+[NH₄⁺]','Ligand balansi','Metallga bog‘langan qism alohida'],
 ['C_B,0 ni tenglashtirish','Faqat bog‘lanmagan ligand oz bo‘lsa','Aks holda yechim noto‘g‘ri bo‘ladi']]),
('anions','Kislota anionlarining roli va ularning o‘zgarishi',[
 ['F⁻','Al³⁺, Fe³⁺ bilan kuchli kompleks','[AlF₆]³⁻; β_6 ≈ 7×10¹⁹'],
 ['Cl⁻','Ba’zi metallarda kuchli ligand','[AgCl₂]⁻; [HgCl₄]²⁻ shakllari'],
 ['SO₄²⁻','Kation bilan bog‘lanish va cho‘kish','Protonlanish erkin ulushni kamaytiradi'],
 ['PO₄³⁻','Kuchli cho‘ktiruvchi anion','Protonlanish uch bosqichli'],
 ['S²⁻','Ko‘p og‘ir metall sulfidlarini cho‘qtiradi','Kislotali muhitda faolligi pasayadi'],
 ['NO₃⁻','Ko‘p tizimda nisbatan sust ligand','“Har doim inert” degani emas'],
 ['CN⁻','Juda kuchli ligand','Metallni eritilgan holda ushlab turadi']]),
('dissolve','Komplekslanish eruvchanlikka ta’sir qilishi',[
 ['Ligand yo‘q','Faqat erkin ion hisobga olinadi','s ≈ 1,26×10⁻⁵ mol L⁻¹ (AgCl)'],
 ['Erkin NH₃ = 0,0100','To‘yinganlik sig‘imi kattalashadi','s ≈ 5,22×10⁻⁴ mol L⁻¹'],
 ['Erkin ion kamayadi','Q_sp < K_sp bo‘lib qoladi','Yangi cho‘kma erishi mumkin'],
 ['Jami metall ortadi','Analitik miqdor erkin iondan katta','O‘lchash usuli farq qilishi mumkin'],
 ['Ligand sarflanadi','C_B,0 balansi kerak','Yaxlitlash 8,84% ga chiqadi'],
 ['Modda yetarli emas','Qattiq faza tugaydi','To‘yinganlik sig‘imi chegarasi bor']]),
('separation','Tanlab cho‘ktirish taxminiy hisobining natijalari',[
 ['A²⁺: K_sp,c = 10⁻¹⁸','Cho‘kish boshlanishi pH = 6,00','F_M = 1'],
 ['B²⁺: K_sp,c = 10⁻¹²','Cho‘kish boshlanishi pH = 9,00','F_M = 1'],
 ['A: 99,9% ajralishi','pH = 7,50','B hali to‘yinmagan'],
 ['A uchun F_A = 10⁴','Boshlanishi pH = 8,00 ga suriladi','Selektivlik pasayadi'],
 ['A: 99,9% (F_A = 10⁴)','pH = 9,50','B oldin cho‘ka boshlaydi'],
 ['Xulosa','Faqat K_sp taqqoslash yetarli emas','Protonlanish va komplekslanish hisobga olinadi']]),
('amphoteric','Amfoterlik taxminiy hisobining sonli natijalari',[
 ['K_sp,c = 10⁻³⁰','Shartli hisob uchun tanlangan qiymat','Tajriba konstantasi emas'],
 ['β_4,c = 10³⁴','Shartli hisob uchun tanlangan qiymat','Xayoliy M(OH)₄⁻ tizimi'],
 ['C_sat = K_sp,c(x⁻³+β_4,c·x)','Ikkala tur hisobga olinadi','x = [OH⁻]'],
 ['β_4,c·x⁴ = 3','Minimum sharti','pH ≈ 5,619'],
 ['C_sat(min) ≈ 5,55×10⁻⁵','Yechimning eng kam eruvchanligi','mol L⁻¹'],
 ['C_M,0 = 10⁻³','Jami metall zaxirasi','Real eritilgan miqdor chegaralanadi']]),
('acidph','Kislota ta’siri: stoxiometriya va protonlanish',[
 ['CaSO₄ (1:1)','K_sp,c = [Ca²⁺][SO₄²⁻] = s²','s = √K_sp,c = 7,81×10⁻³ mol L⁻¹'],
 ['CaF₂ (1:2)','K_sp,c = [Ca²⁺][F⁻]² = 4s³','s = (K_sp,c/4)^(1/3)'],
 ['Ag₂SO₄ (2:1)','K_sp,c = [Ag⁺]²[SO₄²⁻] = 4s³','Stox. 1:1 emas'],
 ['HSO₄⁻','K_a,c = 1,2×10⁻²','Erkin SO₄²⁻ ulushi kislotada kamayadi'],
 ['HS⁻','K_a,c = 1,0×10⁻¹⁹','Sulfid faqat kichik pH da faol'],
 ['H₃PO₄','7,5×10⁻³; 6,2×10⁻⁸; 4,2×10⁻¹³','PO₄³⁻ uch bosqichli hosil bo‘ladi']]),
('workflow','Qo‘shma muvozanatni yechish tartibi',[
 ['1. Turlar ro‘yxati','Eritilgan va qattiq fazalar','Nima mavjudligi aniqlanadi'],
 ['2. Modda balansi','Metall, ligand, proton','Qoldiqlar nol bo‘lishi kerak'],
 ['3. Zaryad balansi','Kation va anionlar','Elektroneytrallik'],
 ['4. Tashqi shartlar','pH, harorat, faollik','Noma’lum bo‘lsa noma’lum qoladi'],
 ['5. Faza tekshiruvi','n_s ≥ 0','Manfiy natija — qayta yechish'],
 ['6. Natijani baholash','Taxminiy hisob va tajriba farqi','Muhit effekti ham bo‘lishi mumkin']]),
('worked','Ishlangan hisob: AgCl + ammiak tizimi',[
 ['pH = 10,00','α_L = 0,8490204','pK_a,c = 9,25'],
 ['Erkin NH₃ (l)','0,00779980 mol L⁻¹','Balansli yechim'],
 ['C_Ag,diss (s)','0,000406984 mol L⁻¹','To‘yinganlik sig‘imi'],
 ['[Ag⁺]','3,93136×10⁻⁷ mol L⁻¹','Erkin qism nol emas'],
 ['[Ag(NH₃)₂]⁺','0,000406591 mol L⁻¹','Jami metallning 99,903% i'],
 ['Ligand balansi','0,00918682 + 0,000813182','Yig‘indi aynan 0,0100']])]
out={}
for i,(key,title,rows) in enumerate(data,1):
    out[key]={'caption':f'4.4.{i}-jadval. {title}','headers':['Obyekt / parametr','Mazmun / qiymat','Chegara / izoh'],'widths':[3.8,4.4,4.6],'rows':rows}
(R/'04_04_jadvallar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
notes=[
 [['Analitik miqdor', 'Eritilgan metallning umumiy miqdori erkin ion miqdoriga teng emas.'],
  ['Suvli qobiq', '“Erkin ion” suvli koordinatsion qobiq bilan ham bog‘liq.']],
 [['Faollik bilan ishlash', 'a_i=γ_i c_i/c°; γ_i≈1 faqat ideal yaqinlashuvda.'],
  ['Sig‘im chegarasi', 'Hisoblangan to‘yinganlik sig‘imi mavjud moddadan katta bo‘lishi mumkin.']],
 [['β_2 ≠ K_2', 'Umumiy konstanta K_1·K_2 ko‘paytmasidir; bosqichli konstanta bilan chalkashtirilmaydi.'],
  ['K_d faqat teskari yo‘nalish', 'Konstanta teskari reaksiyaga tegishli bo‘lsa qo‘llanadi.']],
 [['α_L²', 'Ikki ligandli kompleksda pH ta’siri kvadrat bilan kuchayadi.'],
  ['Proton rezervuari', 'pH berilgan bo‘lsa, yetarli proton manbai yoki bufer nazarda tutiladi.']],
 [['Anion — kuzatuvchi emas', 'Perklorat va nitrat ko‘p tizimda faol emas, lekin har doim ham emas.'],
  ['Kislota bilan kuchayish', 'Ba’zi anionlar kislotada protonlanib kuchsizlashadi, ba’zilari kuchaydi.']],
 [['Erish — natija emas', 'Komplekslanish erkin ionni kamaytiradi, umumiy eruvchanlikni oshiradi.'],
  ['Miqdoriy chegara', 'Katta β ham barcha cho‘kmani eritishga yetarli emas.']],
 [['Selektivlik masalasi', 'Ikkita K_sp ni solishtirish selektiv ajratishni hal qilmaydi.'],
  ['Maskalash', 'Kerakli metallni vaqtincha kompleksga bog‘lash usuli.']],
 [['Amfoterlik redoks emas', 'Markaziy metallning oksidlanish darajasi o‘zgarmaydi.'],
  ['Taxminiy hisob chegarasi', 'Xayoliy M(OH)₃/[M(OH)₄]⁻ tizimi haqiqiy Al uchun universal diagramma emas.']],
 [['Ikkita qarama-qarshi ta’sir', 'Protonlanish eruvchanlikni oshiradi, cho‘ktiruvchi anion kuchaytiradi.'],
  ['Stokhiometriya', '1:1 va 2:2 tuzlar uchun eruvchanlik formulasi turlicha.']],
 [['Yaxlitlash xatosi', 'Ligand sarflanishini e’tiborsiz qoldirish 8,84% ga chiqdi.'],
  ['Balans birga', 'Protonlanish, ligand sarfi va faza miqdori birga tekshiriladi.']],
 [['Taxminiy hisob chegarasi', 'Erish taxminiy hisobi faqat Ag(NH₃)₂⁺ turini hisobga oladi; boshqa turlar chetga chiqariladi.'],
  ['Xulosa', 'Komplekslanish erkin ionni kamaytiradi, umumiy eruvchanlikni oshiradi.']]]
(R/'04_04_yonlavhalar.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
print('11 jadval, 22 yon lavha.')
