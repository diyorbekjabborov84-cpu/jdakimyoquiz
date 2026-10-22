#!/usr/bin/env python3
"""Original nomenclature figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'oksidlanish';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):d.text(p,s,font=f(n),fill=c)
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
im,d=canvas('Bir atom — uch xil hisob')
for i,(a,b) in enumerate([('Oksidlanish darajasi','Ionli yaqinlashuv'),('Formal zaryad','Bog‘ elektronlari teng bo‘linadi'),('Qisman zaryad','Elektron zichlik tahlili'),('NO₃⁻ dagi N','OD = +5; FZ = +1')]):box(d,150+i*180,a,b)
save(im,'zaryadlar')
im,d=canvas('Hisobning shartlarini ayting')
for i,(a,b) in enumerate([('Neytral zarracha','OD yig‘indisi = 0'),('Ion','OD yig‘indisi = ion zaryadi'),('O ko‘pincha −2','O–O va O–F ni tekshiring'),('H ko‘pincha +1','Gidrid va P–H ga ehtiyot')]):box(d,150+i*185,a,b)
save(im,'balans')
im,d=canvas('Nitrat: ikki hisobni ajrating')
text(d,(70,180),'⁻O–N⁺(=O)–O⁻',45)
for i,(a,b) in enumerate([('N uchun bog‘lar hissasi','+1 + 2 + 1 = +4'),('Formal zaryadni qo‘shing','+4 + (+1) = +5'),('O atomlarini tekshiring','Yakka: −1−1; qo‘sh: −2+0')]):box(d,340+i*180,a,b)
save(im,'nitrat')
im,d=canvas('Xlor qatori: tuzilish birga')
for i,(a,b) in enumerate([('H–O–Cl','Cl: +1'),('H–O–Cl=O','Cl: +3'),('H–O–Cl(=O)₂','Cl: +5'),('H–O–Cl(=O)₃','Cl: +7')]):box(d,130+i*185,a,b)
text(d,(45,905),'Tendensiya — shu oila doirasida',26,G);save(im,'xlor')
# Triprotic acid ideal distribution at prescribed pH, constants from cited teaching table.
im,d=canvas('P(+5): ulushlar o‘zgaradi',1080)
x0,x1,y0,y1=110,685,170,720
line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
def pos(x,y):return x0+x/14*(x1-x0),y1-y*(y1-y0)
K1,K2,K3=7.5e-3,6.2e-8,4.2e-13;rows=[]
for j in range(561):
 ph=j*.025;h=10**(-ph);terms=[h**3,K1*h*h,K1*K2*h,K1*K2*K3];den=sum(terms);rows.append((ph,*[t/den for t in terms]))
colors=[N,B,'#2A8C80','#895AA6']
for k,col in enumerate(colors):d.line([pos(row[0],row[k+1]) for row in rows],fill=col,width=5)
for x in [0,4,8,12,14]:text(d,(pos(x,0)[0]-12,736),str(x),26)
for y,s in [(0,'0'),(.5,'0,5'),(1,'1')]:text(d,(40,pos(0,y)[1]-17),s,26)
text(d,(44,110),'α',32);text(d,(350,790),'pH',31)
for k,label in enumerate(['H₃PO₄','H₂PO₄⁻','HPO₄²⁻','PO₄³⁻']):text(d,(50+(k%2)*345,865+(k//2)*65),label,30,colors[k])
text(d,(40,1015),'Ideal hisob; titrlash egri chizig‘i emas',24,G);save(im,'fosfat_ulush')
with (OUT/'fosfat_ulush.csv').open('w') as ff:w=csv.writer(ff);w.writerow(['pH','alpha_H3PO4','alpha_H2PO4','alpha_HPO4','alpha_PO4']);w.writerows(rows)
im,d=canvas('O–O ni alohida belgilang')
text(d,(45,160),'H₂SO₅',45);text(d,(45,240),'HO–S(=O)₂–O–OH',34)
for i,(a,b) in enumerate([('2 ta perokso O','Har biri −1'),('3 ta boshqa O','Har biri −2'),('Oltingugurt','S = +6; +8 emas')]):box(d,345+i*175,a,b)
save(im,'perokso')
im,d=canvas('P–H: konvensiyani ayting')
for i,(a,b) in enumerate([('An’anaviy hisob','H₃PO₂: +1; H₃PO₃: +3'),('Fosfat kislota','H₃PO₄: P(+5)'),('Chegaraviy P–H','Juftni berish konvensiyasi muhim'),('Asoslilik boshqa mezon','1, 2, 3 — O–H va mexanizm')]):box(d,145+i*185,a,b)
save(im,'fosfor')
im,d=canvas('Tiosulfat: atomlar turlicha')
text(d,(60,150),'⁻O–S(=O)₂–S⁻',42)
for i,(a,b) in enumerate([('Algoritmik ajratish','Markaziy +5; terminal −1'),('O‘rtacha qiymat','(+5 − 1) / 2 = +2'),('Nominal boshqa hisob','+6 / −2 — shu algoritm emas')]):box(d,330+i*185,a,b)
save(im,'tiosulfat')
im,d=canvas('Strukturadan xulosaga',1100)
for i,(a,b) in enumerate([('1. Ulanish','O–H, P–H, O–O, S–S'),('2. Elektron hisobi','Qoida va konvensiya'),('3. Zaryad balansi','Yig‘indi Q ga tengmi?'),('4. Qiyos sharti','Markaz va oila bir xilmi?'),('5. Kislotalik','Asos + muhit + muvozanat')]):box(d,130+i*185,a,b)
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
render('hclo4_model','HClO₄: O–O bog‘i yo‘q',[('Cl',380,295),('O',380,130),('O',200,315),('O',560,315),('O',380,475),('H',135,405)],[(0,1),(0,2),(0,3),(0,4),(2,5)])
render('h2so5_model','H₂SO₅: perokso zanjir',[('S',350,300),('O',350,130),('O',350,470),('O',180,300),('O',490,300),('O',620,300),('H',140,400),('H',670,390)],[(0,1),(0,2),(0,3),(0,4),(4,5),(3,6),(5,7)])
render('ph_model','HP(O)(OH)₂: P–H',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('H',370,440),('H',150,410),('H',620,265)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)])
render('thio_model','S₂O₃²⁻: S–S fragment',[('S',350,300),('O',350,130),('O',350,470),('O',175,300),('S',550,300)],[(0,1),(0,2),(0,3),(0,4)])
print('9 primary visuals + 4 molecular models and 1 CSV:',OUT)
