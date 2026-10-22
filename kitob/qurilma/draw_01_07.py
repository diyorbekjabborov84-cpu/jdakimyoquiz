#!/usr/bin/env python3
"""Superkislotalar: tushuntiruvchi chizma va hisobiy grafiklar; tajriba ma’lumoti emas."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'superkislotalar';OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(F,n)
def canvas(h=900):
    im=Image.new('RGB',(640,h),'#F5F8FA');return im,ImageDraw.Draw(im)
im,d=canvas(950)
d.text((80,60),'TAQQOSLASH MEZONI',font=font(32),fill='#0B2C4A')
d.rounded_rectangle((95,170,545,360),radius=12,fill='#E2EAF0')
d.text((165,205),'100% H₂SO₄',font=font(37),fill='#0B2C4A')
d.text((175,275),'H₀ ≈ −12',font=font(35),fill='#0B2C4A')
d.line((320,405,320,515),fill='#A8752E',width=5)
d.polygon([(320,535),(307,510),(333,510)],fill='#A8752E')
d.text((80,595),'Kuchliroq protonlash',font=font(33),fill='#243746')
d.text((100,665),'Shu shkalada H₀ ning',font=font(30),fill='#243746')
d.text((115,720),'kamayishi bilan',font=font(32),fill='#243746')
d.text((105,845),'Mezon va muhit zarur',font=font(29),fill='#243746')
im.save(OUT/'taqqoslash.png')

im,d=canvas(890)
d.text((170,35),'[SbF₆]⁻',font=font(46),fill='#0B2C4A')
cx,cy=320,440
for x,y in [(320,190),(320,690),(100,320),(540,320),(100,560),(540,560)]:
    a=math.atan2(y-cy,x-cx)
    d.line((cx+60*math.cos(a),cy+60*math.sin(a),x-35*math.cos(a),y-35*math.sin(a)),fill='#6C8394',width=4)
    d.text((x-18,y-25),'F',font=font(43),fill='#A8752E')
d.text((cx-38,cy-31),'Sb',font=font(45),fill='#0B2C4A')
d.text((85,785),'Olti F: koordinatsiya 6',font=font(30),fill='#243746')
d.text((85,835),'Geometriyaning eskizi',font=font(28),fill='#243746')
im.save(OUT/'sbf6.png')

def graph(name,xmin,xmax,ymax,xticks,yticks,curves,xlabel,ylabel):
    im,d=canvas(740);l,r,t,b=105,595,110,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-y/ymax*(b-t)
    d.text((25,25),ylabel,font=font(29),fill='#0B2C4A')
    for y in yticks:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((10,yy-18),f'{y:g}',font=font(26),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        d.text((xx-24,b+17),str(x).replace('-','−'),font=font(24),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((160,660),xlabel,font=font(30),fill='#0B2C4A')
    rows=[]
    for i in range(241):
        x=xmin+(xmax-xmin)*i/240;rows.append([x]+[func(x) for color,func in curves])
    for j,(color,func) in enumerate(curves):
        d.line([(X(row[0]),Y(row[j+1])) for row in rows],fill=color,width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        w=csv.writer(f);w.writerow(['x']+[f'curve_{i+1}' for i in range(len(curves))]);w.writerows(rows)

graph('protonlanish.png',-12,-4,100,[-12,-10,-8,-6,-4],[0,25,50,75,100],[('#0B2C4A',lambda h:100/(1+10**(h+6))),('#A8752E',lambda h:100/(1+10**(h+9)))],'H₀','BH⁺ ulushi, %')
graph('spektr_eskizi.png',250,500,1.1,[250,350,450,500],[0,.5,1],[('#0B2C4A',lambda w:math.exp(-.5*((w-320)/20)**2)),('#A8752E',lambda w:math.exp(-.5*((w-410)/27)**2))],'λ, nm','Nisbiy yutilish')
assert abs(100/(1+10**(-8+6))-99.00990099009901)<1e-10
assert abs(100/(1+10**(-8+9))-9.09090909090909)<1e-10
print(OUT)
