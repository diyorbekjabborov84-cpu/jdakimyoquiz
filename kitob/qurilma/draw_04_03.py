"""Original passivation teaching figures. Numerical curves are illustrative, not data."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv
from passive_04_03 import save_data,log_anodic,log_cathodic
A=Path(__file__).resolve().parents[1]/'rasmlar/passivlanish';A.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';TEAL='#318E95';BG='#F5F8FA'
def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def txt(d,x,y,s,n=28,c=N):d.text((x,y),s,font=font(n),fill=c)
def canvas(s,h=1120):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);n=32
 while d.textlength(s,font=font(n))>700:n-=1
 txt(d,30,22,s,n);return im,d

def save(im,n):im.save(A/(n+'.png'))
def rows(n):return [{k:float(v) for k,v in r.items()} for r in csv.DictReader((A/(n+'.csv')).open())]
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
im,d=canvas('Faol → passiv → yuqori anod tok')
p=axes(d,0,1,-7,-2,'E nisbiy, V','lg(i / i°)',[(0,'0'),(.3,'0,3'),(.6,'0,6'),(1,'1')],[(-7,'−7'),(-6,'−6'),(-3,'−3'),(-2,'−2')])
curve(d,p,rows('qutblanish'),'E_relative_V','log_i_anodic',N)
x,y=p(.3,-3);d.ellipse((x-7,y-7,x+7,y+7),fill=B);txt(d,x-75,y-58,'kritik',28,B)
txt(d,45,865,'i°=1 A cm⁻²; logarifmik o‘q',27,G)
txt(d,45,930,'i kritik = 10⁻³; i passiv = 10⁻⁶',27,N)
txt(d,45,995,'Sun’iy anod model; real qotishma emas',25,G);save(im,'qutblanish')
im,d=canvas('Katod yo‘li o‘zgarsa sirt holati o‘zgaradi',1180)
p=axes(d,0,1,-7,1,'E nisbiy, V','lg(|i| / i°)',[(0,'0'),(.3,'0,3'),(.7,'0,7'),(1,'1')],[(-7,'−7'),(-6,'−6'),(-3,'−3'),(1,'1')])
rr=rows('aralash')
for col,c in [('log_i_anodic',N),('log_abs_i_weak',B),('log_abs_i_strong',TEAL)]:curve(d,p,rr,'E_relative_V',col,c,-7,1)
for e,s,c in [(.15,'faol',B),(.7,'passiv',TEAL)]:
 x,y=p(e,log_anodic(e));d.ellipse((x-7,y-7,x+7,y+7),fill=c);txt(d,x+8,y-43,s,26,c)
for y,s,c in [(865,'Anod yo‘li — ko‘k',N),(925,'Kuchsiz katod yo‘li — bronza',B),(985,'Kuchli katod yo‘li — ko‘kimtir',TEAL)]:txt(d,45,y,s,27,c)
txt(d,45,1060,'i°=1 A cm⁻²; bir xil shartli anod egri',25,G)
txt(d,45,1115,'Kesishishlar modelga tegishli',25,G);save(im,'aralash')
im,d=canvas('Parda o‘sishi va erishining shartli balansi',1190)
p=axes(d,0,300,0,3.5,'Vaqt, s','Qalinlik L, nm',[(0,'0'),(100,'100'),(200,'200'),(300,'300')],[(0,'0'),(1,'1'),(2,'2'),(3.5,'3,5')])
for col,c in [('L_v002_nm',N),('L_v006_nm',B),('L_v008_nm',TEAL)]:curve(d,p,rows('qalinlik'),'time_s',col,c)
for y,s,c in [(865,'Erish 0,0200 nm/s → 3,00 nm',N),(925,'Erish 0,0600 nm/s → 1,00 nm',B),(985,'Erish 0,0800 nm/s → 0 nm',TEAL)]:txt(d,45,y,s,27,c)
txt(d,45,1060,'L₀=0,500 nm; vaqt ko‘lami 50,0 s',26,G)
txt(d,45,1120,'Ideal model; o‘lchangan parda emas',26,G);save(im,'qalinlik')
im,d=canvas('Xlorid faolligi: ikki shartli chegara',1140)
p=axes(d,-3,0,0,.85,'lg a(Cl⁻)','E, V (shartli etalon)',[(-3,'−3'),(-2,'−2'),(-1,'−1'),(0,'0')],[(0,'0'),(.35,'0,35'),(.65,'0,65'),(.85,'0,85')])
for col,c in [('E_pit_model_V',N),('E_rp_model_V',B)]:curve(d,p,rows('xlorid'),'log_a_Cl',col,c)
txt(d,45,865,'Boshlanish chegarasi — ko‘k',28,N)
txt(d,45,925,'Qayta passivlanish — bronza',28,B)
txt(d,45,995,'b=0,0800 V / dekada; shartli model',25,G)
txt(d,45,1060,'Real materialning xavfsiz chegarasi emas',24,G);save(im,'xlorid')

def scheme(name,title,boxes):
 im,d=canvas(title,1050)
 for i,(s,a,b) in enumerate(boxes):
  y=125+210*i;d.rounded_rectangle((32,y,728,y+160),radius=14,outline=N,width=3)
  txt(d,52,y+14,s,30,B);txt(d,52,y+65,a,27);txt(d,52,y+109,b,26,G)
  if i<len(boxes)-1:txt(d,360,y+165,'↓',33,B)
 save(im,name)
scheme('holatlar','Termodinamik imkoniyat va amaldagi tezlik',[
 ('Immun holat','Metallning o‘zi barqaror','Tanlangan E, pH va turlar uchun'),
 ('Faol holat','Erish uchun ochiq sirt','Anod va katod yo‘llari ishlaydi'),
 ('Passiv holat','Sirt to‘sig‘i erishni sekinlatadi','Ichki qisman toklar nol bo‘lishi shart emas'),
 ('Ochiq zanjir','i anod = |i katod|','Tashqi nol tok ≠ nol korroziya')])
scheme('parda','Nega ayrim qatlam himoya qiladi?',[
 ('Tarkib','Oksid / gidroksid / oksigidroksid','Real parda gidratlangan va nuqsonli'),
 ('Uzluksizlik','Yalang‘och yo‘llar kam bo‘lishi kerak','G‘ovak cho‘kma ayni narsa emas'),
 ('Transport','Ion va elektron oqimi cheklangan','Mutlaq ideal izolyator bo‘lishi shart emas'),
 ('Dinamik saqlanish','Hosil bo‘lish va erish raqobati','Faqat qalinlik yetarli mezon emas')])
scheme('yuqori','Katta anod tok: bir nechta sabab bor',[
 ('Transpassiv erish','Cr(III) → Cr(VI) misoli','Qatlam kimyosi o‘zgaradi'),
 ('Kislorod ajralishi','2H₂O → O₂ + 4H⁺ + 4e⁻','Bu tok metall erishi bilan ayni emas'),
 ('Mahalliy buzilish','Agressiv ion va nuqsonlar','Pitting boshqa yo‘l bilan boshlanishi mumkin'),
 ('Mexanik shikast','Sirt to‘sig‘ining ochilishi','Qayta tiklanish muhitga bog‘liq')])
scheme('dalil','Passivlikni bir nechta dalil bilan tekshiring',[
 ('Elektrokimyo','E, i, vaqt va qutblanish','Etalon, skan tezligi, iR nazorati'),
 ('Sirt tarkibi','XPS va mos kimyoviy usullar','Qatlamning oksidlanish holatlari'),
 ('Morfologiya','Pitting va nuqsonlar','Faqat yaltiroq ko‘rinish yetarli emas'),
 ('Metall yo‘qotilishi','Massa / eritmadagi metall','Kichik o‘rtacha son pitni yashirishi mumkin')])
scheme('hisob','Bir xil massa, boshqa mahalliy xavf',[
 ('Metallga tegishli tok','10,00 μA; 24,00 soat','Al³⁺ nishoni; Q=0,8640 C'),
 ('Massa ekvivalenti','0,08054 mg','Faraday qonuni; berilgan model'),
 ('Bir tekis erish','10,00 cm² da 0,02983 μm','Butun yuzaga keltirilgan qalinlik'),
 ('f=0,001000','0,01000 cm² da 29,83 μm','Mahalliy o‘rtacha; maksimal pit emas')])
# Original explanatory cross-sections, not micrographs or atomic structures.
def base(title):return canvas(title,590)
def metal(d):d.rectangle((70,295,690,490),fill=N)
im,d=base('Sirt kesimi: to‘siq qatlam va eritma');metal(d)
d.rectangle((70,125,690,265),fill='#DCEBF4');d.rectangle((70,265,690,295),fill=B)
txt(d,110,175,'Eritma',38);txt(d,110,365,'Metall',38,'white')
d.line((480,235,560,278),fill=G,width=4);txt(d,405,185,'Parda',32,B)
txt(d,35,525,'Qalinlik va ranglar shartli; mikrofoto emas',25,G);save(im,'kesim')
im,d=base('Shikastlangan joyning qayta qoplanishi');metal(d)
d.rectangle((70,270,690,295),fill=B);d.polygon([(325,270),(385,270),(415,340),(300,340)],fill='#DCEBF4')
d.line((260,230,340,310),fill=TEAL,width=6);d.line((450,230,370,310),fill=TEAL,width=6)
txt(d,150,125,'Qayta hosil bo‘lish mumkin',31,TEAL);txt(d,120,390,'Metall',36,'white')
txt(d,35,525,'Faqat mos muhitda; darhol tiklanish kafolat emas',23,G);save(im,'tiklanish')
im,d=base('Pitting: kichik og‘iz, mahalliy kimyo');metal(d)
d.rectangle((70,270,690,295),fill=B)
d.polygon([(350,270),(390,270),(415,340),(465,450),(285,450),(325,340)],fill='#DCEBF4')
txt(d,125,130,'Gidroliz, H⁺ va Cl⁻',36);d.line((365,195,365,370),fill=G,width=4)
txt(d,35,525,'Geometriya shartli; haqiqiy chuqurlik xaritasi emas',23,G);save(im,'pit_kesim')
im,d=base('Qatlamdan erigan yuqori valentli turga');metal(d)
d.rectangle((70,265,690,295),fill=B);txt(d,135,365,'Metall / qotishma',35,'white')
txt(d,85,110,'Cr(VI) erigan turlar',35);txt(d,95,220,'Cr(III) qatlam',30,B)
for x in [390,490,590]:
 d.line((x,265,x,175),fill=TEAL,width=5);d.polygon([(x,165),(x-9,181),(x+9,181)],fill=TEAL)
txt(d,35,525,'Formal jarayon tasviri; tajriba retsepti emas',25,G);save(im,'trans_kesim')
print('4 graphs + CSV; 5 schemes; 4 original process illustrations.')
