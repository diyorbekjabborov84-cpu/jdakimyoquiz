#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'kinetika_kataliz';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 variables={'K_w,c':('K','w,c'),'K_c':('K','c'),'K₂,c':('K','2,c'),'C_s':('C','s'),'C_T':('C','T'),'C_a':('C','a'),'C_b':('C','b'),'V_a':('V','a'),'V_b':('V','b'),'V_e':('V','e'),'V_oxir':('V','oxir'),'V_yakun':('V','yakun'),'pK_In':('pK','In'),'β_juft':('β','juft'),'k_obs':('k','obs'),'k_HA':('k','HA'),'k_ref':('k','ref'),'E_a':('E','a'),'k_f':('k','f'),'k_r':('k','r'),'k_A':('k','A'),'C_T':('C','T')}
 for part in re.split('('+'|'.join(re.escape(v) for v in variables)+')',s):
  if part in variables:
   main,sub=variables[part];d.text((x,y),main,font=f(n),fill=c);x+=d.textlength(main,font=f(n))
   d.text((x,y+n*.30),sub,font=f(round(n*.72)),fill=c);x+=d.textlength(sub,font=f(round(n*.72)))
  else:d.text((x,y),part,font=f(n),fill=c);x+=d.textlength(part,font=f(n))

def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,min(32,int(32*700/max(700,d.textlength(title,font=f(32))))));return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
from kinetics_03_06 import reversible,profile,arrhenius,ph_channels,buffer_rate,T0
def axes(d,xmin,xmax,ymin,ymax,xlabel,ylabel,xticks,yticks):
 x0,x1,y0,y1=120,680,175,700
 def pos(x,y):return (x0+(x-xmin)/(xmax-xmin)*(x1-x0),y1-(y-ymin)/(ymax-ymin)*(y1-y0))
 line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
 for x,s in xticks:text(d,(pos(x,ymin)[0]-20,717),s,24)
 for y,s in yticks:text(d,(25,pos(xmin,y)[1]-16),s,24)
 text(d,(45,110),ylabel,28);text(d,(200,780),xlabel,29)
 return pos
def csvout(name,headers,rows):
 with (OUT/(name+'.csv')).open('w') as ff:w=csv.writer(ff);w.writerow(headers);w.writerows(rows)
def sphere(d,x,y,r,color,label):
 for rr in range(r,0,-1):
  t=1-rr/r;cx=x-r*.22*t;cy=y-r*.28*t;col=tuple(min(255,int(c*(.55+.45*t)+255*.18*t)) for c in color)
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=col)
 bb=d.textbbox((0,0),label,font=f(29));text(d,(x-(bb[2]-bb[0])/2,y-21),label,29,N if label=='H' else '#FFFFFF')
def render(name,title,atoms,bonds):
 im,d=canvas(title,650)
 for i,j in bonds:
  a,b=atoms[i],atoms[j];line(d,(a[1],a[2]),(b[1],b[2]),'#8F9DA6',17);line(d,(a[1]-3,a[2]-3),(b[1]-3,b[2]-3),'#CAD5DD',5)
 colors={'Cl':(65,170,115),'S':(205,170,45),'Si':(150,140,170),'N':(70,125,205),'O':(225,80,75),'P':(215,145,55),'B':(180,115,160),'F':(65,170,115),'H':(245,246,249)}
 for label,x,y in atoms:sphere(d,x,y,44 if label!='H' else 27,colors[label],label)
 text(d,(38,595),'Idealizatsiyalangan o‘quv modeli',24,G);save(im,name)
# All graphics below are original illustrative models, never experimental observations.
im,d=canvas('Muvozanat bir xil, vaqt boshqa',1100)
p=axes(d,0,240,0,.85,'Vaqt, s','Mahsulot ulushi',[(0,'0'),(60,'60'),(120,'120'),(180,'180'),(240,'240')],[(0,'0'),(.4,'0,4'),(.8,'0,8')])
rows=[]
for i in range(481):
 t=i*.5;s1,p1=reversible(t);s2,p2=reversible(t,factor=10);rows.append((t,s1,p1,s2,p2))
for k,col in [(4,N),(2,B)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: ikkala k 10× oshirilgan',25,N)
text(d,(45,915),'Bronza: k_f=0,020; k_r=0,005 s⁻¹',23,B)
text(d,(45,975),'K=4; oxirgi ulush=0,8; yopiq tizim',24,G)
text(d,(45,1040),'Shartli qaytar birinchi tartibli model',23,G);save(im,'muvozanat');csvout('muvozanat',['t_s','S_base_fraction','P_base_fraction','S_fast_fraction','P_fast_fraction'],rows)
im,d=canvas('Tezlik tenglamasini tekshiring',1000)
for i,(a,b) in enumerate([('Kuzatilgan signal','Qaysi tur konsentratsiyasiga bog‘liq?'),('Vaqt qonuni','Qaytar yoki qaytmas modelmi?'),('Tartiblar','Tajribaviy m, n va k birliklari'),('Psevdotartib','pH va boshqa komponentlar doimiymi?')]):box(d,150+i*180,a,b)
save(im,'tezlik')
im,d=canvas('Bir xil oxirlar, boshqa yo‘l',1120)
p=axes(d,0,1,-25,90,'Shartli reaksiya koordinatasi','Nisbiy G, kJ mol⁻¹',[(0,'S'),(.5,'0,5'),(1,'P')],[(-20,'−20'),(0,'0'),(40,'40'),(80,'80')])
rows=[]
for i in range(1001):
 x=i/1000;rows.append((x,profile(x),profile(x,True)))
for k,col in [(1,B),(2,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Bronza: katalizsiz o‘quv yo‘li',26,B)
text(d,(45,915),'Ko‘k: ikki bosqichli katalitik yo‘l',24,N)
text(d,(45,975),'ΔG° bir xil; cho‘qqilar shartli',26,G)
text(d,(45,1040),'1-bo‘limdagi K=4 ga mos model emas',23,G);save(im,'energiya');csvout('energiya',['coordinate','G_uncatalyzed_kJmol','G_catalyzed_kJmol'],rows)
im,d=canvas('Arrhenius: harorat qiyaligi',1100)
p=axes(d,2.95,3.60,-2,3,'1000 K/T','ln[k(T)/k_ref]',[(3,'3,0'),(3.2,'3,2'),(3.4,'3,4'),(3.6,'3,6')],[(-2,'−2'),(0,'0'),(2,'2')])
rows=[]
for i in range(241):
 t=278.15+i*.25;k=arrhenius(t);rows.append((t,1000/t,k,math.log(k/.001)))
d.line([p(r[1],r[3]) for r in rows],fill=N,width=5)
text(d,(45,855),'E_a=50,0 kJ mol⁻¹; doimiy model',24,N)
text(d,(45,915),'k_ref=0,001000 s⁻¹; T₀=298,15 K',24,B)
text(d,(45,975),'Logarifmning argumenti o‘lchamsiz',24,G)
text(d,(45,1040),'To‘g‘ri chiziq — model; tajriba emas',23,G);save(im,'harorat');csvout('harorat',['T_K','1000K_over_T','k_per_s','ln_k_over_kref'],rows)
im,d=canvas('pH–tezlik: parallel kanallar',1120)
p=axes(d,2,12,-5.2,.2,'Ideal hisobiy pH','lg(k_obs/k°)',[(2,'2'),(4,'4'),(6,'6'),(8,'8'),(10,'10'),(12,'12')],[(-5,'−5'),(-3,'−3'),(-1,'−1'),(0,'0')])
rows=[]
for i in range(401):
 pH=2+i/40;k0,kh,koh,total=ph_channels(pH);rows.append((pH,k0,kh,koh,total,math.log10(total)))
line(d,p(2,-5),p(12,-5),G,2);d.line([p(r[0],r[5]) for r in rows],fill=N,width=5)
cx,cy=p(6.5,math.log10(ph_channels(6.5)[3]));d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=B)
text(d,(45,855),'Ko‘k: jami; kulrang: faqat k₀',26,N)
text(d,(45,915),'Bronza nuqta: minimum, pH=6,5',25,B)
text(d,(45,975),'k°=1 s⁻¹; γ≈1; 25 °C',27,G)
text(d,(45,1040),'U shakl mexanizmning yagona isboti emas',22,G);save(im,'ph_tezlik');csvout('ph_tezlik',['pH','k0_per_s','kH_h_per_s','kOH_OH_per_s','kobs_per_s','log_kobs_over_1s'],rows)
im,d=canvas('Bir xil pH da buferning ta’siri',1120)
p=axes(d,0,.1,0,1.2,'C_T, mol L⁻¹','k_obs, 10⁻³ s⁻¹',[(0,'0'),(.025,'0,025'),(.05,'0,05'),(.075,'0,075'),(.1,'0,10')],[(0,'0'),(.4,'0,4'),(.8,'0,8'),(1.2,'1,2')])
rows=[]
for i in range(301):
 c=i/3000;ha,a,spec,total=buffer_rate(c);rows.append((c,ha,a,spec,total))
for k,col in [(4,N),(3,B)]:d.line([p(r[0],1000*r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: HA umumiy katalizi bor',26,N)
text(d,(45,915),'Bronza: faqat maxsus kanallar',26,B)
text(d,(45,975),'pH=pKₐ=5; [HA]=[A⁻]=C_T/2',25,G)
text(d,(45,1040),'k_HA=0,0200 L mol⁻¹ s⁻¹; k_A=0',24,G);save(im,'bufer');csvout('bufer',['CT_M','HA_M','A_M','k_specific_per_s','k_with_general_per_s'],rows)
im,d=canvas('Formal proton tashish sikli',1050)
for i,(a,b) in enumerate([('1. Protonlanish','S + H⁺ ⇌ SH⁺'),('2. Qayta tuzilish','SH⁺ ⇌ PH⁺'),('3. Deprotonlanish','PH⁺ ⇌ P + H⁺'),('Yig‘indi','S ⇌ P; H⁺ qayta tiklandi')]):box(d,150+i*180,a,b)
text(d,(45,980),'S va P teng atom tarkibli shartli belgilar',22,G);save(im,'sikl')
im,d=canvas('NO/NO₂: formal redoks sikli',1050)
for i,(a,b) in enumerate([('Oksidlanish bosqichi','2NO + O₂ → 2NO₂'),('SO₂ bilan almashinuv','2NO₂ + 2SO₂ → 2NO + 2SO₃'),('Umumiy balans','2SO₂ + O₂ → 2SO₃'),('Siklning ma’nosi','NO qayta hosil bo‘ladi')]):box(d,150+i*180,a,b)
text(d,(45,980),'To‘liq sanoat mexanizmi yoki yo‘riqnoma emas',21,G);save(im,'noorganik')
im,d=canvas('Tezlikdan mexanistik xulosaga',1100)
for i,(a,b) in enumerate([('1. Faol shakllar','Tarkib va muvozanatni tekshiring'),('2. Signal va vaqt','Boshlang‘ich tezlik / to‘liq egri'),('3. Tashqi omillar','pH, bufer, T, ion kuchi'),('4. Muqobil modellar','Bir xil qonunni berishi mumkin'),('5. Nazorat','Balans, birlik, qaytar yo‘l, sirt')]):box(d,130+i*185,a,b)
save(im,'nazorat')
# Molecular illustrations: schematic connectivity, not optimized coordinates or electron density.
render('gidroksoniy_model','H₃O⁺: suvli proton tashuvchisi',[('O',370,290),('H',230,350),('H',510,350),('H',370,455)],[(0,1),(0,2),(0,3)])
render('fosfat_model','H₂PO₄⁻: proton donor misoli',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)])
render('ammiak_model','NH₃: proton akseptor misoli',[('N',370,290),('H',230,350),('H',510,350),('H',370,455)],[(0,1),(0,2),(0,3)])
render('no2_model','NO₂: neytral radikalning ulanishi',[('N',370,270),('O',220,405),('O',520,405)],[(0,1),(0,2)])
print('4 schemes, 5 original model graphs, 4 molecular images, 5 CSV:',OUT)
