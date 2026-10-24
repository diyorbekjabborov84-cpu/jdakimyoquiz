#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'bufer_gidroliz';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 variables={'K_w,c':('K','w,c'),'K_c':('K','c'),'K₂,c':('K','2,c'),'C_s':('C','s'),'C_T':('C','T'),'C_a':('C','a'),'C_b':('C','b'),'V_a':('V','a'),'V_b':('V','b'),'V_e':('V','e'),'V_oxir':('V','oxir'),'V_yakun':('V','yakun'),'pK_In':('pK','In'),'β_juft':('β','juft'),'C_T':('C','T')}
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
from buffer_03_05 import buffer,beta,solve,PHOS,K_HF,K_NH4
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
 text(d,(38,595),'Idealizatsiyalangan o‘quv tasviri',24,G);save(im,name)
im,d=canvas('Bufer tarkibi o‘zgarib javob beradi',1000)
for i,(a,b) in enumerate([('Kislota qo‘shildi','A⁻ + H₃O⁺ → HA + H₂O'),('Asos qo‘shildi','HA + OH⁻ → A⁻ + H₂O'),('Nisbat o‘zgardi','pH ham cheklangan darajada siljidi'),('Zaxira cheklangan','Bir shakl kamaygach ta’sir ortadi')]):box(d,150+i*180,a,b)
save(im,'mexanizm')
im,d=canvas('Analitik nisbat va to‘liq balans',1100)
p=axes(d,-2,2,2.5,7.5,'lg[n(NaA)/n(HA)]','Ideal hisobiy pH',[(-2,'−2'),(-1,'−1'),(0,'0'),(1,'1'),(2,'2')],[(3,'3'),(5,'5'),(7,'7')])
rows=[]
for i in range(321):
 lr=-2+i/80;ratio=10**lr;rows.append((lr,ratio,buffer(ratio=ratio),5+lr))
for k,col in [(3,B),(2,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: to‘liq suvli balans',27,N);text(d,(45,915),'Bronza: miqdorlar taqribi',27,B)
text(d,(45,975),'C_T=0,1000 M; K_c=10⁻⁵ M',26,G)
text(d,(45,1040),'Shartli HA; γ≈1; 25 °C',27,G);save(im,'nisbat');csvout('nisbat',['log_ratio','ratio','pH_full','pH_HH'],rows)
im,d=canvas('Kuchli reagent: zaxiraning tugashi',1120)
p=axes(d,-.06,.06,0,14,'q, mol L⁻¹','Ideal hisobiy pH',[(-.06,'−0,06'),(-.03,'−0,03'),(0,'0'),(.03,'0,03'),(.06,'0,06')],[(0,'0'),(4,'4'),(7,'7'),(10,'10'),(14,'14')])
rows=[];hh=[]
for i in range(481):
 q=-.06+i*.00025;pf=buffer(added=q);pa=5+math.log10((.05+q)/(.05-q)) if abs(q)<.0499999 else None
 rows.append((q,pf,pa))
 if pa is not None:hh.append(p(q,pa))
d.line(hh,fill=B,width=5);d.line([p(r[0],r[1]) for r in rows],fill=N,width=5)
text(d,(45,855),'Ko‘k: to‘liq balans; C_T=0,1000 M',24,N)
text(d,(45,915),'Bronza: ikki miqdor musbat taqrib',24,B)
text(d,(45,975),'q<0: kislota; q>0: asos',27,G)
text(d,(45,1040),'Yakuniy C lar bo‘yicha ideal qator',24,G);save(im,'qoshish');csvout('qoshish',['q_M','pH_full','pH_HH_or_empty'],rows)
im,d=canvas('Bufer juftligining sig‘im hissasi',1100)
p=axes(d,2,8,0,.06,'Ideal hisobiy pH','β_juft, mol L⁻¹ pH⁻¹',[(2,'2'),(4,'4'),(5,'5'),(6,'6'),(8,'8')],[(0,'0'),(.03,'0,03'),(.06,'0,06')])
rows=[]
for i in range(361):
 pH=2+i/60;b1,w,t1=beta(pH,.1);b2,w,t2=beta(pH,.01);rows.append((pH,b1,b2,w,t1,t2))
for k,col in [(1,N),(2,B)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: C_T=0,1000 mol/L',27,N);text(d,(45,915),'Bronza: C_T=0,0100 mol/L',26,B)
text(d,(45,975),'Faqat juftlik hissasi; K_c=10⁻⁵ M',24,G)
text(d,(45,1040),'Suv hadlari jami β da alohida',26,G);save(im,'sigim');csvout('sigim',['pH','beta_pair_C_01','beta_pair_C_001','beta_water','beta_total_C_01','beta_total_C_001'],rows)
im,d=canvas('Suyultirish: nisbat saqlansa ham',1100)
p=axes(d,-10,-1,4.5,7.1,'lg(C_T/c°)','Ideal hisobiy pH',[(-10,'−10'),(-8,'−8'),(-6,'−6'),(-4,'−4'),(-2,'−2')],[(5,'5'),(6,'6'),(7,'7')])
rows=[]
for i in range(361):
 lc=-10+i/40;c=10**lc;rows.append((lc,c,buffer(c=c),5))
for k,col in [(3,B),(2,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: suvli muvozanat balansi',26,N);text(d,(45,915),'Bronza: nisbatdan pH=5 taqribi',25,B)
text(d,(45,975),'Teng analitik HA/NaA; 25 °C',26,G)
text(d,(45,1040),'K_c=10⁻⁵ M; shartli HA',27,G);save(im,'suyultirish');csvout('suyultirish',['log_CT','CT_M','pH_full','pH_HH'],rows)
im,d=canvas('Tuz erishi ≠ gidroliz',1000)
for i,(a,b) in enumerate([('Elektrolitning erishi','NaA → Na⁺ + A⁻'),('Proton almashinuvi','A⁻ + H₂O ⇌ HA + OH⁻'),('Moddiy balans','C = [A⁻] + [HA]'),('Zaryad balansi','h + C = [A⁻] + [OH⁻]')]):box(d,150+i*180,a,b)
save(im,'anion')
im,d=canvas('Kation: proton donor qayerda?',1000)
for i,(a,b) in enumerate([('NH₄⁺','Ionning o‘zi proton beradi'),('Akvakompleks','Suv ligandidagi O–H donor'),('Gidroksokompleks','Ligand H₂O dan OH⁻ ga o‘tdi'),('Keyingi jarayonlar','Bosqichlar, kompleks, cho‘kma')]):box(d,150+i*180,a,b)
save(im,'kation')
im,d=canvas('NH₄F: ikkala ion va suv',1100)
p=axes(d,-9,-1,6.1,7.05,'lg(C/c°)','Ideal hisobiy pH',[(-9,'−9'),(-7,'−7'),(-5,'−5'),(-3,'−3'),(-1,'−1')],[(6.25,'6,25'),(6.5,'6,50'),(6.75,'6,75'),(7,'7,00')])
rows=[]
for i in range(321):
 lc=-9+i/40;c=10**lc;pf=solve([(c,(K_HF,))],[(c,K_NH4)]);pa=-math.log10(math.sqrt(K_HF*K_NH4));rows.append((lc,c,pf,pa))
for k,col in [(3,B),(2,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: ikki oila + suv balansi',26,N);text(d,(45,915),'Bronza: suvni tashlagan taqrib',25,B)
text(d,(45,975),'HF: K_c=6,4×10⁻⁴ M',26,G)
text(d,(45,1040),'NH₄⁺: K_c=5,6×10⁻¹⁰ M',25,G);save(im,'ikkala');csvout('ikkala',['log_C','C_M','pH_full','pH_approx'],rows)
im,d=canvas('Birlashtiruvchi muvozanat taxminiy hisobi',1100)
for i,(a,b) in enumerate([('1. Tarkib','HA, tuz, BH⁺ yoki poliprotik'),('2. Oilalar','Har biri uchun moddiy balans'),('3. Elektr neytrallik','Kuzatuvchi ionlar ham qatnashadi'),('4. Konstantalar','Bir xil T, birlik va taxminiy hisob'),('5. Nazorat','Suv, ulush, cho‘kma va gaz')]):box(d,130+i*185,a,b)
save(im,'nazorat')
# Structural illustrations. Sticks show connectivity, not a complete bond-order taxminiy hisob.
render('h2po4_model','H₂PO₄⁻: ikki O–H ulanishi',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)])
render('hpo4_model','HPO₄²⁻: bitta O–H ulanishi',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410)],[(0,1),(0,2),(0,3),(0,4),(2,5)])
render('nh4_model','NH₄⁺: ammoniy ioni',[('N',370,315),('H',370,135),('H',200,350),('H',540,350),('H',370,480)],[(0,1),(0,2),(0,3),(0,4)])
im,d=canvas('[Al(H₂O)₆]³⁺: suv ligandlari',850)
cx,cy=370,400
for j in range(6):
 ang=-math.pi/2+j*math.pi/3;x=cx+190*math.cos(ang);y=cy+190*math.sin(ang)
 line(d,(cx,cy),(x,y),'#91A9B9',8);sphere(d,x,y,36,(225,80,75),'O')
 # Two schematic H positions outside each O, no experimental angles implied.
 for delta in [-.45,.45]:
  xx=x+78*math.cos(ang+delta);yy=y+78*math.sin(ang+delta);line(d,(x,y),(xx,yy),'#A9B6C0',5);sphere(d,xx,yy,22,(245,246,249),'H')
sphere(d,cx,cy,48,(135,150,175),'Al')
text(d,(35,745),'Olti Al–O ulanishi; sxematik proyeksiya',24,G)
text(d,(35,795),'Optimallashtirilgan geometriya emas',25,G);save(im,'akva_model')
print('4 schemes, 5 calculated graphs, 4 structural images, 5 CSV:',OUT)
