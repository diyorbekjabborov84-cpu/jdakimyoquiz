#!/usr/bin/env python3
"""HSAB rasmlari: sifat eskizi va aniq farazli ikki hisobiy grafik."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,shutil,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'hsab';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(FONT,n)
shutil.copyfile(ROOT.parent/'image-search'/'ralph-g-pearson-chemist-portrait-hsab-1.jpg',OUT/'pearson.jpg')

def canvas(h=900):
    im=Image.new('RGB',(640,h),'#F5F8FA');return im,ImageDraw.Draw(im)
im,d=canvas(1000)
for cy,label,bbox,color in [(240,'QATTIQ',(-100,-90,100,90),'#0B2C4A'),(680,'YUMSHOQ',(-160,-70,160,70),'#A8752E')]:
    d.text((180,cy-170),label,font=font(37),fill=color)
    d.ellipse((215,cy-105,425,cy+105),outline='#AABBC7',width=3)
    x1,y1,x2,y2=bbox
    d.ellipse((320+x1,cy+y1,320+x2,cy+y2),outline=color,width=6)
    d.ellipse((310,cy-10,330,cy+10),fill=color)
    d.text((80,cy+145),'Kamroq deformatsiya' if label=='QATTIQ' else 'Ko‘proq deformatsiya',font=font(31),fill='#243746')
d.text((90,950),'Sifat eskizi; masshtabsiz',font=font(27),fill='#243746')
im.save(OUT/'qutblanish.png')

im,d=canvas(1020)
for y,head,one,two in [(60,'QATTIQ JUFT','A₁ — B₁','moslik moyilligi'),(420,'YUMSHOQ JUFT','A₂ — B₂','moslik moyilligi')]:
    d.text((100,y),head,font=font(35),fill='#0B2C4A')
    d.text((165,y+100),one,font=font(52),fill='#A8752E')
    d.text((110,y+195),two,font=font(30),fill='#243746')
d.text((65,810),'Sifat mezoni, konstanta emas',font=font(28),fill='#243746')
d.text((80,880),'Erituvchi va faza muhim',font=font(30),fill='#243746')
im.save(OUT/'moslik.png')

def graph(name,xmin,xmax,ymin,ymax,xticks,yticks,curves,xlabel,ylabel):
    im,d=canvas(730);l,r,t,b=105,595,110,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-(y-ymin)/(ymax-ymin)*(b-t)
    d.text((22,22),ylabel,font=font(29),fill='#0B2C4A')
    for y in yticks:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((12,yy-18),f'{y:g}'.replace('-','−'),font=font(26),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        d.text((xx-20,b+16),f'{x:g}'.replace('-','−'),font=font(25),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((135,655),xlabel,font=font(28),fill='#0B2C4A')
    rows=[]
    for i in range(201):
        x=xmin+(xmax-xmin)*i/200;rows.append([x]+[func(x) for color,func in curves])
    for j,(color,func) in enumerate(curves):
        d.line([(X(row[0]),Y(row[j+1])) for row in rows],fill=color,width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        out=csv.writer(f);out.writerow(['x']+[f'curve{j+1}' for j in range(len(curves))]);out.writerows(rows)

graph('qattiqlik.png',-.5,.5,0,1.1,[-.5,0,.5],[0,.25,.5,.75,1],[('#0B2C4A',lambda x:4*x*x),('#A8752E',lambda x:x*x)],'ΔN','η(ΔN)², eV')
graph('raqobat.png',-2,3,0,100,[-2,-1,0,1,2,3],[0,25,50,75,100],[('#0B2C4A',lambda x:100*10/(11+.1*10**x)),('#A8752E',lambda x:100*.1*10**x/(11+.1*10**x))],'lg([L₂]/[L₁])','Ulush, %')
assert abs(10/(11+.1*100)-10/21)<1e-12
assert abs(100*10/(11+.1)-90.09009009009)<1e-9
print(OUT)
