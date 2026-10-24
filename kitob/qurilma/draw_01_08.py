#!/usr/bin/env python3
"""Qiyoslash uchun mualliflik sxemalari va aniq farazli hisobiy grafiklar."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,textwrap
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'rasmlar'/'qiyoslash';OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(n):return ImageFont.truetype(FONT,n)
def canvas(h=1000):
    im=Image.new('RGB',(640,h),'#F5F8FA');return im,ImageDraw.Draw(im)
def stack(name,items):
    im,d=canvas();y=42
    for i,(label,body) in enumerate(items):
        d.line((38,y,602,y),fill='#C28E3B',width=3);y+=23
        d.text((42,y),label,font=font(29),fill='#0B2C4A');y+=52
        for line in textwrap.wrap(body,width=25):
            d.text((42,y),line,font=font(29),fill='#243746');y+=42
        y+=45
    assert y<1000,(name,y)
    im.save(OUT/name)
stack('mezon_xarita.png',[
('IONLAR','Arrhenius: suvli eritma'),
('ALMASHINUV','Brønsted: H⁺; Lewis: elektron jufti'),
('KENG / MAXSUS','Usanovich; Lyuks–Flud: O²⁻'),
('QO‘SHIMCHA SAVOL','HSAB: moslik; H₀: muhit')])
stack('uch_daraja.png',[
('KUZATISH','Suvda OH⁻ miqdori ortadi'),
('PROTON','H₂O → NH₃: proton ko‘chishi'),
('ELEKTRON JUFTI','Azot jufti yangi N–H bog‘ini hosil qiladi')])
stack('protonsiz.png',[
('JUFTNI QABUL QILISH','NH₃ → BF₃: B–N bog‘i'),
('OKSID-ION MEZONI','O²⁻ akseptori: SiO₂'),
('REDOKS ELEKTRONI','Na elektron beradi; Cl₂ qabul qiladi')])
stack('tanlash_yoli.png',[
('01 · HODISA','Qaysi zarracha almashinadi?'),
('02 · SHAROIT','Qaysi erituvchi va faza?'),
('03 · NATIJA','Tasnifmi yoki sonli hisobmi?'),
('04 · TEKSHIRUV','Balans, faollik va yon reaksiyalar')])
stack('boblar_koprik.png',[
('1-BOB','Ta’rif, mezon va yondashuv'),
('2-BOB','Bog‘lanish va tuzilish'),
('3-BOB','Kuch va muvozanat'),
('KEYINGI TAHLIL','Aniq kislotalarning xossalari')])

def graph(name,xmin,xmax,xticks,curves,xlabel):
    im,d=canvas(740);l,r,t,b=105,595,110,580
    X=lambda x:l+(x-xmin)/(xmax-xmin)*(r-l)
    Y=lambda y:b-y/100*(b-t)
    d.text((23,24),'Ulush, %',font=font(31),fill='#0B2C4A')
    for y in [0,25,50,75,100]:
        yy=Y(y);d.line((l,yy,r,yy),fill='#D4DFE6',width=2)
        d.text((10,yy-18),str(y),font=font(26),fill='#243746')
    for x in xticks:
        xx=X(x);d.line((xx,t,xx,b),fill='#D4DFE6',width=2)
        d.text((xx-17,b+17),str(x).replace('-','−'),font=font(26),fill='#243746')
    d.line((l,t,l,b,r,b),fill='#0B2C4A',width=3)
    d.text((135,657),xlabel,font=font(28),fill='#0B2C4A')
    rows=[]
    for i in range(241):
        x=xmin+(xmax-xmin)*i/240;rows.append([x]+[f(x) for color,f in curves])
    for j,(color,f) in enumerate(curves):d.line([(X(row[0]),Y(row[j+1])) for row in rows],fill=color,width=5)
    im.save(OUT/name)
    with (OUT/(Path(name).stem+'.csv')).open('w') as f:
        w=csv.writer(f);w.writerow(['x']+[f'curve_{j+1}_percent' for j in range(len(curves))]);w.writerows(rows)

graph('proton_shakllari.png',-3,3,[-3,-1,0,1,3],[('#0B2C4A',lambda x:100/(1+10**x)),('#A8752E',lambda x:100*10**x/(1+10**x))],'pH − pKₐ')
graph('ikki_model.png',-4,4,[-4,-2,0,2,4],[('#0B2C4A',lambda x:100*10**(x/2)/(1+10**(x/2))),('#A8752E',lambda x:100*10**x/(1+10**x))],'lg q')
assert abs(100*10/11-90.9090909090909)<1e-10
assert abs(100*100/101-99.009900990099)<1e-10
print(OUT)
