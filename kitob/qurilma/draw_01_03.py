#!/usr/bin/env python3
"""Muvozanat modellari: barcha farazlar grafik izohlarida beriladi."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'bronsted_lowry';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(FONT,n)
for src,dst in [('johannes-br-nsted-portrait-public-domain-1.jpg','bronsted.jpg'),('thomas-martin-lowry-portrait-wikimedia-c-1.jpg','lowry.jpg')]:
    shutil.copyfile(ROOT.parent/'image-search'/src,OUT/dst)

def graph(name,xmin,xmax,xticks,curves,xlabel):
    im=Image.new('RGB',(660,720),'#F5F8FA');d=ImageDraw.Draw(im)
    l,r,t,b=105,605,100,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-y/100*(b-t)
    d.text((40,28),'Ulush, %',font=font(32),fill='#0B2C4A')
    for y in [0,25,50,75,100]:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((12,yy-19),str(y),font=font(28),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        d.text((xx-17,b+17),str(x).replace('-','−'),font=font(27),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((150,650),xlabel,font=font(31),fill='#0B2C4A')
    rows=[]
    for i in range(181):
        x=xmin+(xmax-xmin)*i/180
        rows.append([x]+[func(x) for color,func in curves])
    for j,(color,func) in enumerate(curves):
        d.line([(X(row[0]),Y(row[j+1])) for row in rows],fill=color,width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        out=csv.writer(f);out.writerow(['x']+[f'curve_{j+1}_percent' for j in range(len(curves))]);out.writerows(rows)

graph('yonalish.png',-6,6,[-6,-3,0,3,6],[('#A8752E',lambda x:100*10**(x/2)/(1+10**(x/2)))],'ΔpKₐ')
graph('shakllar.png',-3,3,[-3,-1,0,1,3],[('#0B2C4A',lambda x:100/(1+10**x)),('#A8752E',lambda x:100*10**x/(1+10**x))],'pH − pKₐ')
assert abs(100*10/(1+10)-90.9090909090909)<1e-10
print(OUT)
