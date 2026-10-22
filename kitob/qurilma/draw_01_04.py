#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, csv, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'lewis';OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(F,n)
portrait=Image.open(ROOT.parent/'image-search'/'gilbert-n-lewis-public-domain-commons-po-1.jpg')
w,h=portrait.size
portrait.crop((0,0,w,int(h*.89))).save(OUT/'lewis.jpg',quality=95)

def canvas(height=900):
    im=Image.new('RGB',(640,height),'#F5F8FA');return im,ImageDraw.Draw(im)
def arrow(d,start,end):
    x,y=start;xx,yy=end;d.line((x,y,xx,yy),fill='#A8752E',width=5)
    angle=math.atan2(yy-y,xx-x)
    pts=[(xx,yy)]+[(xx-22*math.cos(angle+a),yy-22*math.sin(angle+a)) for a in [-.4,.4]]
    d.polygon(pts,fill='#A8752E')
im,d=canvas()
d.text((75,40),'DONOR: NH₃',font=font(37),fill='#0B2C4A')
d.text((270,155),'N',font=font(53),fill='#0B2C4A')
for x,y in [(200,115),(405,115),(315,275)]:
    d.text((x-18,y-24),'H',font=font(37),fill='#243746')
d.line((255,155,220,135),fill='#243746',width=3)
d.line((325,155,380,135),fill='#243746',width=3)
d.line((293,215,305,250),fill='#243746',width=3)
# A separate explicitly labelled pair avoids misrepresenting a full geometry.
d.ellipse((345,170,354,179),fill='#A8752E');d.ellipse((345,191,354,200),fill='#A8752E')
d.text((365,265),'erkin juft',font=font(26),fill='#243746')
arrow(d,(450,323),(450,450))
d.text((70,480),'AKSEPTOR: BF₃',font=font(35),fill='#0B2C4A')
d.text((210,590),'F₃B←NH₃',font=font(39),fill='#0B2C4A')
d.text((100,700),'Yangi B–N bog‘i',font=font(31),fill='#243746')
d.text((75,770),'Elektron jufti: N → B',font=font(29),fill='#243746')
im.save(OUT/'donor_akseptor.png')

im,d=canvas(820)
d.text((85,45),'[Ag(NH₃)₂]⁺',font=font(41),fill='#0B2C4A')
d.text((255,180),'NH₃',font=font(39),fill='#243746')
arrow(d,(300,255),(300,345))
d.text((255,375),'Ag⁺',font=font(43),fill='#0B2C4A')
arrow(d,(300,580),(300,485))
d.text((255,615),'NH₃',font=font(39),fill='#243746')
d.text((65,735),'Juftlar metallga beriladi',font=font(28),fill='#243746')
im.save(OUT/'kumush.png')

def graph(name,xmin,xmax,ymin,ymax,xticks,yticks,func,xlabel,ylabel):
    im,d=canvas(720);l,r,t,b=110,590,110,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-(y-ymin)/(ymax-ymin)*(b-t)
    d.text((28,24),ylabel,font=font(30),fill='#0B2C4A')
    for y in yticks:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((15,yy-18),str(y).replace('-','−'),font=font(26),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        d.text((xx-17,b+17),str(x).replace('-','−'),font=font(26),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((140,650),xlabel,font=font(28),fill='#0B2C4A')
    rows=[]
    for i in range(201):
        x=xmin+(xmax-xmin)*i/200;rows.append((x,func(x)))
    d.line([(X(x),Y(y)) for x,y in rows],fill='#A8752E',width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        w=csv.writer(f);w.writerow(['x','y']);w.writerows(rows)

graph('energiya.png',-3,3,-20,20,[-3,0,3],[-20,-10,0,10,20],lambda x:-8.314462618*298.15*math.log(10)*x/1000,'lg K','ΔG°, kJ/mol')
graph('kompleks.png',-6,-1,0,100,[-6,-4,-2,-1],[0,25,50,75,100],lambda x:100*1e3*10**x/(1+1e3*10**x),'lg([L]/(1 mol/L))','θ, %')
assert abs(1e3*1e-3/(1+1e3*1e-3)-.5)<1e-12
print(OUT)
