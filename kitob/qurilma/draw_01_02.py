#!/usr/bin/env python3
"""Hisobiy grafiklar: bir asosli HA, Ka=1e-5; ideal suyultirilgan eritma.
Suv avtoionlanishi tashlab ketilgan. c=1e-2..1e-5 mol/L.
Manba rasm: matn/01_02_rasm_manbasi.md.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'arrhenius'; OUT.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(F,n)
portrait=Image.open(ROOT.parent/'image-search'/'svante-arrhenius-portrait-wikimedia-comm-1.jpg')
# Only the scan margin is cropped; the historical photograph is not regenerated.
w,h=portrait.size
portrait.crop((int(w*.245),int(h*.205),int(w*.745),int(h*.71))).save(OUT/'arrhenius_portret.jpg',quality=95)
rows=[]
for i in range(151):
    pc=2+3*i/150;c=10**(-pc);ka=1e-5
    # Algebraically stable positive root of x^2 + Ka*x - Ka*c = 0.
    x=2*ka*c/(math.sqrt(ka*ka+4*ka*c)+ka)
    rows.append((pc,c,x,x/c*100,-math.log10(x),pc))
with (OUT/'model_hisob.csv').open('w') as f:
    out=csv.writer(f);out.writerow(['pC','c_mol_L','H3O_mol_L','alpha_percent','pH_weak','pH_complete']);out.writerows(rows)

def graph(name,kind):
    im=Image.new('RGB',(660,700),'#F5F8FA');d=ImageDraw.Draw(im)
    left,right,top,bottom=100,605,115,580
    ymax=70 if kind=='alpha' else 5.5;ymin=0 if kind=='alpha' else 1.5
    X=lambda x:left+(x-2)/3*(right-left)
    Y=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
    d.text((50,25),'α, %' if kind=='alpha' else 'pH',font=font(34),fill='#0B2C4A')
    ticks=[0,20,40,60] if kind=='alpha' else [2,3,4,5]
    for y in ticks:
        yy=Y(y);d.line((left,yy,right,yy),fill='#D4DFE6',width=2)
        d.text((25,yy-20),str(y),font=font(30),fill='#243746')
    for x in [2,3,4,5]:
        xx=X(x);d.line((xx,top,xx,bottom),fill='#D4DFE6',width=2)
        d.text((xx-12,bottom+17),str(x),font=font(30),fill='#243746')
    d.line((left,top,left,bottom,right,bottom),fill='#0B2C4A',width=3)
    d.text((510,640),'pC',font=font(32),fill='#0B2C4A')
    d.line([(X(r[0]),Y(r[3] if kind=='alpha' else r[4])) for r in rows],fill='#A8752E',width=6)
    if kind=='ph':
        d.line([(X(r[0]),Y(r[5])) for r in rows],fill='#0B2C4A',width=5)
    im.save(OUT/name)
graph('alpha_grafik.png','alpha');graph('ph_grafik.png','ph')
assert abs(rows[0][3]-3.112672920173694)<1e-7
print(OUT)
