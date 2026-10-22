#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'ka_pka_alfa';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 for part in re.split(r'(K_c|C_T)',s):
  if part in ('K_c','C_T'):
   main,sub=part.split('_');d.text((x,y),main,font=f(n),fill=c);x+=d.textlength(main,font=f(n))
   d.text((x,y+n*.30),sub,font=f(round(n*.72)),fill=c);x+=d.textlength(sub,font=f(round(n*.72)))
  else:d.text((x,y),part,font=f(n),fill=c);x+=d.textlength(part,font=f(n))
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
from equilibria_03_01 import quadratic,with_water,diprotic,KC,KWC
im,d=canvas('Uchta mustaqil tushuncha')
for i,(a,b) in enumerate([('Kₐ','Muvozanat konstantasi'),('pKₐ','−lg Kₐ; logarifmik miqyos'),('α','Aniq ta’riflangan shakl ulushi'),('C','Analitik konsentratsiya')]):box(d,150+i*180,a,b)
save(im,'uch_belgi')
im,d=canvas('Faollik va konsentratsiya')
for i,(a,b) in enumerate([('Termodinamik Kₐ','Faolliklar; o‘lchamsiz'),('a(i) = γᵢ[i]/c°','Standart holat ko‘rsatiladi'),('K_c: konsentratsion nisbat','Birligi mol L⁻¹'),('γ = 1 bo‘lsa','K_c = Kₐc°')]):box(d,150+i*180,a,b)
save(im,'faollik')
im,d=canvas('Logarifmik miqyos')
for i,(a,b) in enumerate([('Kₐ = 10⁻³','pKₐ = 3'),('Kₐ = 10⁻⁶','pKₐ = 6'),('Farq: 3 birlik','Konstantalar nisbati 1000'),('Kichik pKₐ','Shu muhitda kuchliroq donor')]):box(d,150+i*180,a,b)
save(im,'pka')
def axes(d,xmin,xmax,ymin,ymax,xlabel,ylabel,xticks,yticks):
 x0,x1,y0,y1=120,680,170,695
 def pos(x,y):return (x0+(x-xmin)/(xmax-xmin)*(x1-x0),y1-(y-ymin)/(ymax-ymin)*(y1-y0))
 line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
 for x,s in xticks:text(d,(pos(x,ymin)[0]-15,710),s,25)
 for y,s in yticks:text(d,(35,pos(xmin,y)[1]-16),s,25)
 text(d,(55,110),ylabel,28);text(d,(200,770),xlabel,29)
 return pos
def csvout(name,headers,rows):
 with (OUT/(name+'.csv')).open('w') as ff:w=csv.writer(ff);w.writerow(headers);w.writerows(rows)
im,d=canvas('Moddiy balansdan α ga')
p=axes(d,-5,3,0,1,'lg(K_c / C)','α',[(-5,'−5'),(-3,'−3'),(-1,'−1'),(1,'1'),(3,'3')],[(0,'0'),(.5,'0,5'),(1,'1')])
rows=[]
for i in range(321):
 x=-5+.025*i;q=10**x;a=2/(1+math.sqrt(1+4/q));rows.append((x,q,a))
d.line([p(x,a) for x,q,a in rows],fill=N,width=6)
text(d,(40,850),'K_c/C = α²/(1−α)',29,B);text(d,(40,910),'Suv va boshqa ionlar tashlangan',25,G);save(im,'alfa_model');csvout('alfa_model',['log10_Kc_over_C','Kc_over_C','alpha'],rows)
im,d=canvas('Taqribning nisbiy xatosi')
p=axes(d,0,5,0,65,'lg(C / K_c)','x xatosi, %',[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],[(0,'0'),(20,'20'),(40,'40'),(60,'60')])
rows=[]
for i in range(251):
 x=i*.02;r=10**x;a=2/(1+math.sqrt(1+4*r));ap=1/math.sqrt(r);err=100*(ap/a-1);rows.append((x,r,a,err))
d.line([p(x,e) for x,r,a,e in rows],fill=B,width=6)
xx=math.log10(400);line(d,p(xx,0),p(xx,65),G,2)
text(d,(40,845),'Chiziq: C/K_c = 400',28,G);text(d,(40,903),'5% mezoni pH xatosi emas',27,B);save(im,'taqrib_xato');csvout('taqrib_xato',['log10_C_over_Kc','C_over_Kc','alpha_exact','x_relative_error_percent'],rows)
im,d=canvas('Suvni unutish oqibati')
p=axes(d,-10,-2,2,10,'lg(C / c°)','pH',[(-10,'−10'),(-8,'−8'),(-6,'−6'),(-4,'−4'),(-2,'−2')],[(2,'2'),(4,'4'),(6,'6'),(8,'8'),(10,'10')])
rows=[]
for i in range(321):
 x=-10+i*.025;c=10**x;h,a=with_water(c);hq=quadratic(c);rows.append((x,c,-math.log10(h),-math.log10(hq),h,a))
for k,col in [(2,N),(3,B)]:d.line([p(row[0],row[k]) for row in rows],fill=col,width=5)
line(d,p(-10,7),p(-2,7),G,2)
text(d,(40,850),'Ko‘k: suv bilan ideal hisob',27,N);text(d,(40,905),'Bronza: suvsiz kvadrat model',26,B);save(im,'suv_tasiri');csvout('suv_tasiri',['log10_C_over_c0','C_mol_L','pH_with_water','pH_quadratic','h_mol_L','alpha_with_water'],rows)
im,d=canvas('Umumiy ionni unutmang')
for i,(a,b) in enumerate([('HA + NaA','A⁻ ning ikki manbasi bor'),('Zaryad balansi','h + [Na⁺] = [A⁻] + [OH⁻]'),('Moddiy balans','C_T = [HA] + [A⁻]'),('α_A','Shakl ulushi; h/C_T emas')]):box(d,150+i*180,a,b)
save(im,'umumiy_ion')
im,d=canvas('Diprotik: uchta shakl',1080)
p=axes(d,0,12,0,1,'pH','αᵢ',[(0,'0'),(3,'3'),(6,'6'),(9,'9'),(12,'12')],[(0,'0'),(.5,'0,5'),(1,'1')]);rows=[]
for i in range(481):
 ph=i*.025;rows.append((ph,*diprotic(ph)))
for k,col in [(1,N),(2,B),(3,'#2A8C80')]:d.line([p(row[0],row[k]) for row in rows],fill=col,width=5)
for j,(lab,col) in enumerate([('H₂A',N),('HA⁻',B),('A²⁻','#2A8C80')]):text(d,(45+j*235,855),lab,31,col)
text(d,(40,925),'K₁ = 10⁻³; K₂ = 10⁻⁷ mol L⁻¹',26,G);text(d,(40,1000),'Shartli ideal tizim; o‘lchov emas',25,G);save(im,'diprotik');csvout('diprotik',['pH','alpha_H2A','alpha_HA','alpha_A'],rows)
im,d=canvas('Hisobni tekshirish tartibi',1100)
for i,(a,b) in enumerate([('1. Obyekt va tarkib','HA / tuz / ko‘p protonli tizim'),('2. Model','Faollik va suv hissasi'),('3. Tenglamalar','Moddiy + zaryad + muvozanat'),('4. Yechim','Aniq yoki tekshirilgan taqrib'),('5. Qayta tekshirish','Ulushlar, birliklar, balanslar')]):box(d,130+i*185,a,b)
save(im,'algoritm')
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
render('suv_model','H₂O: proton akseptori',[('O',380,290),('H',230,410),('H',530,410)],[(0,1),(0,2)])
render('hf_model','HF: bitta protonli molekula',[('H',265,325),('F',460,325)],[(0,1)])
render('gidroksoniy_model','H₃O⁺: suvdagi qisqartma',[('O',380,290),('H',220,365),('H',540,365),('H',380,470)],[(0,1),(0,2),(0,3)])
render('fosfat_model','H₃PO₄: uch asosli misol',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265),('H',450,520)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6),(4,7)])
print('9 primary visuals, 4 molecular renders and 4 CSV datasets:',OUT)
