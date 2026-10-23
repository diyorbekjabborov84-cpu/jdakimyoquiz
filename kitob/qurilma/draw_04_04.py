"""Original teaching figures for 4.4. Numerical curves are model outputs, not data."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,math
from complex_04_04 import (ASSETS as A,saturation_s,complex_fraction,alpha_nh3,
                           conditional_beta,amph_csat,CM0,save_data)
N='#0B2C4A';B='#B37C2D';G='#657583';TEAL='#318E95';BG='#F5F8FA'
def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def txt(d,x,y,s,n=28,c=N):d.text((x,y),s,font=font(n),fill=c)
def canvas(s,h=1120):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);n=32
 while d.textlength(s,font=font(n))>700:n-=1
 txt(d,30,22,s,n);return im,d
def save(im,n):im.save(A/(n+'.png'))
def rows(n):return [{k:float(v) for k,v in r.items()} for k,v in [(k,v) for k,v in csv.reader([])] ] if False else [{k:float(v) for k,v in r.items()} for r in csv.DictReader((A/(n+'.csv')).open())]
def axes(d,xlo,xhi,ylo,yhi,xlabel,ylabel,xt,yt):
 def p(x,y):return (120+(x-xlo)/(xhi-xlo)*560,700-(y-ylo)/(yhi-ylo)*525)
 d.line((120,175,120,700,680,700),fill=G,width=3)
 for x,s in xt:txt(d,p(x,ylo)[0]-15,718,s,24)
 for y,s in yt:txt(d,20,p(xlo,y)[1]-16,s,24)
 txt(d,45,108,ylabel,28);txt(d,145,780,xlabel,27)
 return p
def curve(d,p,rr,x,y,col,ylo=None,yhi=None):
 line=[]
 for r in rr:
  if (ylo is None or ylo<=r[y]) and (yhi is None or r[y]<=yhi):line.append(p(r[x],r[y]))
  else:
   if len(line)>1:d.line(line,fill=col,width=5)
   line=[]
 if len(line)>1:d.line(line,fill=col,width=5)

save_data()
# Graph 1 — species distribution versus free ligand.
im,d=canvas('Erkin ligand konsentratsiyasi va turlar taqsimoti',1160)
p=axes(d,-7,-2,0,1,'lg[NH₃], mol L⁻¹','Ulush',[(-7,'−7'),(-5,'−5'),(-4,'−4'),(-3,'−3'),(-2,'−2')],[(0,'0'),(.25,'0,25'),(.5,'0,5'),(.75,'0,75'),(1,'1')])
rr=rows('species')
curve(d,p,rr,'log_free_L','fraction_free_Ag',N)
curve(d,p,rr,'log_free_L','fraction_complex',B)
x,y=p(-3.615224460689137,.5);d.ellipse((x-7,y-7,x+7,y+7),fill=TEAL)
txt(d,45,865,'Erkin Ag⁺ ulushi — ko‘k',28,N)
txt(d,45,925,'[Ag(NH₃)₂]⁺ ulushi — bronza',28,B)
txt(d,45,995,'β₂,c = 1,7×10⁷; teng ulush nuqtasi lg[NH₃] ≈ −3,62',25,G)
txt(d,45,1060,'Model egri chizig‘i; tajriba ma’lumoti emas',25,G);save(im,'species')
# Graph 2 — protonation and conditional constant.
im,d=canvas('Protonlanish va shartli hosil bo‘lish konstantasi',1180)
p=axes(d,2,12,0,1,'pH','α_L (chap o‘q) va lg β′₂,c (o‘ng o‘q)',[(2,'2'),(5,'5'),(7.25,'7,25'),(9.25,'9,25'),(11.25,'11,25')],[(0,'0'),(.25,'0,25'),(.5,'0,5'),(.75,'0,75'),(1,'1')])
rr=rows('proton')
curve(d,p,rr,'pH','alpha_NH3',N)
for r in rr:
 v=r['log_beta_conditional'];frac=(v+8.0)/16.0
 if -0.01<=frac<=1.01:
  x,y=p(r['pH'],frac);d.ellipse((x-4,y-4,x+4,y+4),fill=B)
for v,lab in [(8,'8'),(0,'0'),(-8,'−8')]:
 yy=p(2,(v+8.0)/16.0)[1];txt(d,690,yy-14,lab,22,G)
txt(d,45,865,'α_L (erkin NH₃ ulushi) — ko‘k egri chiziq',28,N)
txt(d,45,925,'lg β′₂,c — bronza nuqtalar, o‘ng o‘q −8…8',28,B)
txt(d,45,995,'pK_a,c = 9,25; β′₂,c = β₂,c·α_L²',25,G)
txt(d,45,1060,'Model egri chizig‘i; tajriba ma’lumoti emas',25,G);save(im,'proton')
# Graph 3 — solubility promoted by complexation.
im,d=canvas('Komplekslanish cho‘kmaning eruvchanligini oshiradi',1180)
p=axes(d,-7,-2,-6,-3,'lg[NH₃], mol L⁻¹','lg s, mol L⁻¹',[(-7,'−7'),(-5,'−5'),(-4,'−4'),(-3,'−3'),(-2,'−2')],[(-6,'−6'),(-5,'−5'),(-4,'−4'),(-3,'−3')])
rr=rows('solubility')
curve(d,p,rr,'log_free_L','log_s',N)
x,y=p(-2,math.log10(saturation_s(1e-2)));d.ellipse((x-7,y-7,x+7,y+7),fill=B)
txt(d,45,865,'S ≈ √(K_sp,c(1 + β₂,c[NH₃]²))',28,N)
txt(d,45,925,'K_sp,c = 1,6×10⁻¹⁰; β₂,c = 1,7×10⁷',26,G)
txt(d,45,995,'Erkin ligand, ortiqcha AgCl bilan',26,G)
txt(d,45,1060,'Model egri chizig‘i; tajriba ma’lumoti emas',25,G);save(im,'solubility')
# Graph 4 — amphoteric U-curve.
im,d=canvas('Amfoterlik: to‘yinganlik sig‘imining U shakli',1200)
p=axes(d,4.5,7.5,-5,-1,'pH','lg C_sat, mol L⁻¹',[(4.5,'4,5'),(5.5,'5,5'),(6.5,'6,5'),(7.5,'7,5')],[(-5,'−5'),(-4,'−4'),(-3,'−3'),(-2,'−2'),(-1,'−1')])
rr=rows('amph')
curve(d,p,rr,'pH','log_Csat',N)
x,y=p(5.6193,math.log10(amph_csat(5.6193)));d.ellipse((x-7,y-7,x+7,y+7),fill=B)
d.line((x,700,x,y),fill=TEAL,width=3)
txt(d,x-118,648,'minimum pH ≈ 5,619',25,TEAL)
txt(d,45,865,'C_sat = K_sp,c(x⁻³ + β₄,c·x);  x = [OH⁻]',28,N)
txt(d,45,925,'K_sp,c = 10⁻³⁰; β₄,c = 10³⁴ (xayoliy model)',26,G)
txt(d,45,995,'C_M,0 = 10⁻³ mol L⁻¹;  C_diss = min(C_sat, C_M,0)',25,G)
txt(d,45,1060,'Model egri chizig‘i; real Al uchun emas',25,G);save(im,'amph')

def scheme(name,title,boxes,h=1050):
 im,d=canvas(title,h)
 for i,(s,a,b) in enumerate(boxes):
  y=125+210*i;d.rounded_rectangle((32,y,728,y+160),radius=14,outline=N,width=3)
  txt(d,52,y+14,s,30,B);txt(d,52,y+65,a,26);txt(d,52,y+107,b,25,G)
  if i<len(boxes)-1:txt(d,360,y+165,'↓',33,B)
 save(im,name)
scheme('turlar','Metall eritmada qanday turlarda bo‘ladi',[
 ('Erkin (akva) ion','Suvli qobiq bilan o‘ralgan','Analitik miqdor ≠ erkin ion'),
 ('Kompleks','Ligand elektron jufti beradi','β₂ va β₄ orqali hisoblanadi'),
 ('Gidroksokompleks','pH ga bog‘liq paydo bo‘ladi','Amfoterlik bilan bog‘liq'),
 ('Qattiq faza','Cho‘kma tarkibida metall','Modda balansiga alohida kiritiladi')])
scheme('toyinganlik','Q_sp va K_sp nima uchun farqlanadi',[
 ('Q_sp — holat','Aralashtirilgandan keyingi ion ko‘paytmasi','Hali muvozanat bo‘lmagan'),
 ('K_sp — doimiy','Tanlangan faza bilan muvozanat konstantasi','Faolliklar orqali yoziladi'),
 ('Q_sp < K_sp','Erish qulay','Qattiq faza barqaror'),
 ('Q_sp > K_sp','Cho‘kishga moyil','Nukleatsiya kechishi mumkin')])
scheme('ligand','Ligand qanday yo‘l bilan faollashadi',[
 ('Erkin ligand','Faol shakl','Kompleks hosil qilishga tayyor'),
 ('Protonlanish','NH₃ + H⁺ → NH₄⁺','Faollik pasayadi, β′₂ kichikadi'),
 ('Shartli konstanta','β′₂,c = β₂,c·α_L²','Ammo turgun pH da qo‘llanadi'),
 ('Ligand sarfi','Kompleksga bog‘langan qism','Balansda alohida hisoblanadi')])
scheme('anion','Kislota anioni uchta vazifani bajarishi mumkin',[
 ('Kuzatuvchi ion','Perklorat, nitrat','Nisbatan faol emas'),
 ('Cho‘ktiruvchi ion','Fosfat, sulfat, sulfid','Kam eruvchan tuz hosil qiladi'),
 ('Kuchli ligand','Fluorid, tsianid','Metallni eritilgan holda ushlab turadi'),
 ('Protonlanish bilan o‘zgaruvchi','Bisulfat, fosfat','pH bilan faolligi o‘zgaradi')])
scheme('kislota','Kislota eruvchanlikka qanday ta’sir qiladi',[
 ('Protonlanish','Anionning erkin shakli kamayadi','Eruvchanlik ko‘tariladi'),
 ('Cho‘ktiruvchi anion','Q_sp > K_sp sharti','Yangi cho‘kma hosil bo‘ladi'),
 ('Komplekslanish','Erkin metall ioni kamayadi','To‘yinganlik sig‘imi o‘sadi'),
 ('Natija','Ikkala ta’sir bir-birini bekor qilishi mumkin','Kontekstga qarab baholash kerak')])
scheme('yechim','Muqobilatni yechish tartibi',[
 ('1. Turlar','Eritilgan va qattiq fazalar','Nima mavjudligini aniqlash'),
 ('2. Balanslar','Metall, ligand, zaryad','Qoldiqlar nol bo‘lishi shart'),
 ('3. Yechim','Tenglamalar tizimi','Faqat fizik ildiz qabul qilinadi'),
 ('4. Faza tekshiruvi','n_s ≥ 0 va Q_sp ≤ K_sp','Manfiy bo‘lsa qayta yechish')])
scheme('selektiv','Tanlab cho‘ktirish uchun nimani nazorat qilish kerak',[
 ('K_sp farqi','Kichik K_sp oldin cho‘kadi','Yagona omil emas'),
 ('Protonlanish','Anion faolligini o‘zgartiradi','pH boshqaruvi bilan bog‘liq'),
 ('Komplekslanish','Tanlab cho‘ktirishni buzadi','Maskalash ham shu bilan'),
 ('Ishlab chiqarish','Ajratish, qayta cho‘ktirish','Analitik usul bilan tasdiqlash')])
scheme('hisob','AgCl va ammiak tizimi: balansli yechim',[
 ('Ligand balansi','l/α_L + 2(s − K_sp,c/s) = C_B,0','Bu tengsizlik yechiladi'),
 ('Topilgan ildiz','l ≈ 0,00779980; s ≈ 0,000406984','mol L⁻¹'),
 ('Yaxlitlash xatosi','Ligand sarfi e’tiborsiz qoldirilsa','s ≈ 0,000442976 (+8,84%)'),
 ('Xulosa','Balans har doim qayta tekshiriladi','Natija faqat model ichida')])
# Original schematic illustrations, not micrographs or atomic structures.
def base(t,h=590):return canvas(t,h)
im,d=base('Cho‘kma sirti va eritma: diffuziya qatlami')
d.rectangle((70,300,690,470),fill=N);txt(d,110,360,'Qattiq faza',36,'white')
d.rectangle((70,120,690,290),fill='#DCEBF4')
for x in [160,300,440,580]:
 d.line((x,290,x,190),fill=TEAL,width=6);d.polygon([(x,180),(x-10,200),(x+10,200)],fill=TEAL)
txt(d,110,150,'Eritma — diffuziya qatlami',32)
d.rectangle((70,290,690,300),fill=B);txt(d,430,215,'Cho‘kish yuzasi',27,B)
txt(d,35,505,'Geometriya shartli; mikrofoto yoki atom tuzilmasi emas',23,G);save(im,'kesim')
im,d=base('Kompleks hosil bo‘lishi va erishning ikki yo‘li')
d.rounded_rectangle((60,180,330,400),radius=14,outline=N,width=3)
txt(d,90,215,'Erkin ion',30,B);txt(d,90,265,'[Ag⁺]',30);txt(d,90,320,'Q_sp < K_sp',26,TEAL)
d.line((330,290,440,290),fill=B,width=5);d.polygon([(440,290),(420,275),(420,305)],fill=B)
d.rounded_rectangle((440,180,710,400),radius=14,outline=N,width=3)
txt(d,470,215,'Kompleks',30,B);txt(d,470,265,'[Ag(NH₃)₂]⁺',28);txt(d,470,320,'Erkin ion kamayadi',24,G)
txt(d,35,505,'Termodinamik yo‘nalish; mexanizm chizilmagan',23,G);save(im,'erish')
im,d=base('Ko‘p ligandli va gidroksokompleks turlari')
d.ellipse((300,230,460,390),fill=N);txt(d,340,290,'M',40,'white')
for i,(dx,dy) in enumerate([(-120,-90),(120,-90),(-150,60),(150,60),(0,-130),(0,130)]):
 x,y=380+dx,310+dy
 d.ellipse((x-42,y-42,x+42,y+42),outline=TEAL,width=4)
 txt(d,x-26,y-16,'L',30,TEAL)
 d.line((380,310,x,y),fill=G,width=3)
txt(d,120,455,'Ligandlar soni va turi metallga bog‘liq',27)
txt(d,35,505,'Sxematik; atom masshtabi va orbital model emas',23,G);save(im,'gidroksokompleks')
im,d=base('Protonlanish faollikni o‘zgartiradi')
d.rectangle((60,150,330,400),fill='#DCEBF4');txt(d,95,185,'Kislotali muhit',29,N)
txt(d,120,265,'NH₃',34);txt(d,95,330,'NH₄⁺ — ligand emas',26)
d.rectangle((440,150,710,400),fill='#EAF1E4');txt(d,475,185,'Ishqoriy muhit',29,N)
txt(d,500,265,'NH₃',34);txt(d,455,330,'Erkin ligand faol',26)
d.line((330,275,440,275),fill=B,width=5);d.polygon([(440,275),(418,262),(418,288)],fill=B)
txt(d,35,505,'Chiqish o‘zi emas; muvozanat ta’siri chizilgan',23,G);save(im,'protonatsiya')
print('4 grafik + CSV; 7 sxema; 4 original illustration.')
