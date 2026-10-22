#!/usr/bin/env python3
"""Lyuks–Flud: local silicate sketch and two explicitly hypothetical graphs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'usanovich_lux';OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(F,n)

def graph(name,xmin,xmax,ymin,ymax,xticks,yticks,func,xlabel,ylabel):
    im=Image.new('RGB',(660,720),'#F5F8FA');d=ImageDraw.Draw(im)
    l,r,t,b=110,605,110,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-(y-ymin)/(ymax-ymin)*(b-t)
    d.text((30,24),ylabel,font=font(31),fill='#0B2C4A')
    for y in yticks:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((15,yy-18),str(y),font=font(26),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        label=str(x).replace('-','−')
        box=d.textbbox((0,0),label,font=font(25));width=box[2]-box[0]
        d.text((xx-width/2,b+17),label,font=font(25),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((145,650),xlabel,font=font(30),fill='#0B2C4A')
    rows=[]
    for i in range(201):
        x=xmin+(xmax-xmin)*i/200;rows.append((x,func(x)))
    d.line([(X(x),Y(y)) for x,y in rows],fill='#A8752E',width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        w=csv.writer(f);w.writerow(['x','y']);w.writerows(rows)

graph('oksid_faolligi.png',-6,0,0,100,[-6,-4,-2,0],[0,25,50,75,100],lambda x:100*100*10**x/(1+100*10**x),'lg a(O²⁻)','B ulushi, %')
graph('harorat.png',800,1600,0,3,[800,1200,1600],[0,1,2,3],lambda t:(50000-20*t)/(8.314462618*t*math.log(10)),'T, K','lg K')
im=Image.new('RGB',(660,950),'#F5F8FA');d=ImageDraw.Draw(im)
for y,title,formula in [(50,'KO‘PRIK KISLOROD','…Si–O–Si…'),(335,'OKSID QO‘SHILISHI','+ O²⁻'),(630,'KO‘PRIKSIZ UCHLAR','…Si–O⁻')]:
    d.text((45,y),title,font=font(28),fill='#0B2C4A')
    d.text((70,y+85),formula,font=font(42),fill='#243746')
d.line((330,240,330,300),fill='#A8752E',width=5)
d.polygon([(330,313),(318,290),(342,290)],fill='#A8752E')
d.line((330,525,330,590),fill='#A8752E',width=5)
d.polygon([(330,603),(318,580),(342,580)],fill='#A8752E')
d.text((70,790),'+ ⁻O–Si…',font=font(42),fill='#243746')
im.save(OUT/'silikat.png')
assert abs(100*.01/(1+100*.01)-.5)<1e-12
assert 1.56<(50000-20*1000)/(8.314462618*1000*math.log(10))<1.58
print(OUT)
