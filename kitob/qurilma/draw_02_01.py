#!/usr/bin/env python3
"""Original conceptual diagrams and illustrative model graphs, not measured data."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'boglanish';OUT.mkdir(parents=True,exist_ok=True)
NAVY='#0B2C4A';BRONZE='#B37C2D';GRAY='#657583'
def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def canvas(title):
 im=Image.new('RGB',(760,900),'#F5F8FA');d=ImageDraw.Draw(im);d.text((38,30),title,font=font(32),fill=NAVY);return im,d
def text(d,xy,s,n=29,c=NAVY):d.text(xy,s,font=font(n),fill=c)
def line(d,a,b,c=NAVY,w=5):d.line((a,b),fill=c,width=w)
def save(im,name):im.save(OUT/(name+'.png'))
def arrow(d,x,y):
 line(d,(x,y),(x,y+48),BRONZE);d.polygon([(x,y+60),(x-12,y+40),(x+12,y+40)],fill=BRONZE)
def formula(d,cy,lower,title):
 text(d,(225,cy-145),title,38)
 text(d,(350,cy),'P',42);text(d,(350,cy-95),'O',38)
 line(d,(360,cy-10),(360,cy-45));line(d,(374,cy-10),(374,cy-45))
 text(d,(140,cy),'HO',38);text(d,(555,cy),'OH',38)
 line(d,(225,cy+25),(325,cy+25));line(d,(400,cy+25),(540,cy+25))
 line(d,(368,cy+65),(368,cy+120));text(d,(345,cy+132),lower,38)
im,d=canvas('Ulanish — asosiy farq');formula(d,240,'H','H₃PO₃');formula(d,640,'OH','H₃PO₄');text(d,(58,460),'2 ta O–H; 1 ta P–H',28,BRONZE);text(d,(58,850),'3 ta O–H',28,BRONZE);save(im,'ulanish')
# Graph axes are common: plot in 125..670, 165..700.
def axes(d,xlabel,ylabel,lo,hi,ylo,yhi):
 x0,x1,y0,y1=130,675,175,700
 def pos(x,y):return (x0+(x-lo)/(hi-lo)*(x1-x0),y1-(y-ylo)/(yhi-ylo)*(y1-y0))
 line(d,(x0,y0),(x0,y1),GRAY,3);line(d,(x0,y1),(x1,y1),GRAY,3)
 text(d,(80,110),ylabel,27);text(d,(170,770),xlabel,27)
 return pos
im,d=canvas('Bog‘ energiyasi modeli');pos=axes(d,'r / rₑ','V / Dₑ',.6,3,-1.2,2.2)
rows=[]
for i in range(241):
 r=.6+i*.01;v=(1-math.exp(-2*(r-1)))**2-1;rows.append((r,v))
d.line([pos(r,v) for r,v in rows],fill=NAVY,width=6)
line(d,pos(.6,0),pos(3,0),GRAY,2)
for x in [1,2,3]:text(d,(pos(x,0)[0]-10,715),str(x),26)
for y in [-1,0,1,2]:text(d,(55,pos(1,y)[1]-15),str(y),26)
x,y=pos(1,-1);d.ellipse((x-7,y-7,x+7,y+7),fill=BRONZE);text(d,(x+23,y-30),'minimum',25,BRONZE)
text(d,(65,840),'Faraziy Morse potensiali',25,GRAY);save(im,'morse')
with (OUT/'morse.csv').open('w') as f:w=csv.writer(f);w.writerow(['r_over_re','V_over_De']);w.writerows(rows)
im,d=canvas('NO₃⁻: bitta Lewis yozuvi')
text(d,(350,400),'N⁺',48);text(d,(350,210),'O',45);text(d,(95,590),'O⁻',45);text(d,(575,590),'O⁻',45)
line(d,(365,380),(365,285));line(d,(380,380),(380,285));line(d,(335,460),(185,570));line(d,(425,460),(560,570))
for xy in [(295,228),(418,228),(90,560),(90,653),(55,605),(578,560),(578,653),(663,605)]:text(d,xy,'••',23,BRONZE)
text(d,(75,735),'FZ yig‘indisi: −1',33);text(d,(75,790),'Valent elektronlar: 24',30);text(d,(75,845),'Teng yozuvlardan bittasi',25,GRAY);save(im,'lewis')
im,d=canvas('Geometriya va yakka juft')
for cy,title,kind in [(200,'AX₂ — chiziqli',0),(450,'AX₃ — tekis',1),(720,'AX₂E₂ — egik',2)]:
 text(d,(65,cy-95),title,30);cx=380
 if kind==0:pts=[(170,cy),(590,cy)]
 elif kind==1:pts=[(380,cy-45),(210,cy+55),(550,cy+55)]
 else:pts=[(240,cy+75),(520,cy+75)]
 for p in pts:line(d,(cx,cy),p);d.ellipse((p[0]-21,p[1]-21,p[0]+21,p[1]+21),fill=BRONZE)
 d.ellipse((cx-25,cy-25,cx+25,cy+25),fill=NAVY)
 if kind==2:text(d,(305,cy-57),'••    ••',29,BRONZE)
text(d,(58,850),'Sxemalar masshtabsiz',25,GRAY);save(im,'geometriya')
im,d=canvas('Ikki dipolning yig‘indisi');pos=axes(d,'θ, gradus','μ / μᵦ',0,180,0,2.2)
rows=[(i,2*math.cos(math.radians(i/2))) for i in range(181)];d.line([pos(x,y) for x,y in rows],fill=BRONZE,width=6)
for x in [0,60,120,180]:text(d,(pos(x,0)[0]-18,715),str(x),26)
for y in [0,1,2]:text(d,(70,pos(0,y)[1]-15),str(y),26)
text(d,(65,835),'Teng bog‘ dipollari modeli',26,GRAY);save(im,'dipol')
with (OUT/'dipol.csv').open('w') as f:w=csv.writer(f);w.writerow(['theta_degrees','mu_over_mu_b']);w.writerows(rows)
im,d=canvas('Kislotalik — umumiy natija')
for y,title,body in [(160,'1. Reagent','HA va erituvchi'),(365,'2. Elektronlar','Bog‘ va zaryad taqsimoti'),(570,'3. Mahsulotlar','A⁻ va protonlangan suv')]:
 d.rounded_rectangle((45,y,715,y+125),radius=14,outline=NAVY,width=3);text(d,(72,y+16),title,33);text(d,(72,y+70),body,29,GRAY)
 if y<570:arrow(d,380,y+135)
text(d,(70,775),'Solvatlanish + entropiya',30,BRONZE);text(d,(70,830),'Faqat bog‘ energiyasi emas',27);save(im,'energiya')
im,d=canvas('Tuzilishni o‘qish tartibi')
for i,label in enumerate(['Ulanish','Elektronlar va zaryad','Elektron sohalar','Geometriya va dipol','Muhit va muvozanat']):
 y=125+i*148;d.rounded_rectangle((40,y,720,y+85),radius=12,fill='#E8EFF4');text(d,(65,y+22),f'{i+1}. {label}',30)
 if i<4:arrow(d,380,y+89)
text(d,(65,865),'Har bosqich — alohida tekshiruv',25,GRAY);save(im,'algoritm')
print('7 visuals and 2 graph CSV files written:',OUT)
