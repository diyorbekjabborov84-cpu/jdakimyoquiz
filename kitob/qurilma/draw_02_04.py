#!/usr/bin/env python3
"""Original nomenclature figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'nomenklatura';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):d.text(p,s,font=f(n),fill=c)
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
im,d=canvas('Nomlashning axborot darajasi')
for i,(a,b) in enumerate([('Saqlangan nom','sulfuric acid'),('Tarkibiy nom','Atomlar va nisbatlar'),('Additiv nom','Markaz + guruhlar'),('Zarur aniqlik','Formula + zaryad + holat')]):box(d,150+i*180,a,b)
save(im,'darajalar')
im,d=canvas('HCl: holatni ko‘rsating')
box(d,170,'HCl(g)','hydrogen chloride');box(d,410,'HCl(aq)','hydrochloric acid')
text(d,(48,690),'Gazsimon modda va',32);text(d,(48,750),'suvli eritma farqlanadi.',32)
text(d,(48,860),'(aq) — suvli eritma',29,B);save(im,'holat')
im,d=canvas('Fosfat qatori')
for i,(a,b) in enumerate([('H₃PO₄','phosphoric acid'),('H₂PO₄⁻','dihydrogenphosphate'),('HPO₄²⁻','hydrogenphosphate'),('PO₄³⁻','phosphate')]):
 y=120+i*200;box(d,y,a,b)
 if i<3:text(d,(346,y+125),'−H⁺ ↓',28,B)
save(im,'fosfat_qatori')
im,d=canvas('H₂SO₄: nomni ajrating')
for i,(a,b) in enumerate([('2 × OH','dihydroxido'),('2 × O','dioxido'),('Markaziy S','sulfur')]):box(d,150+i*195,a,b)
text(d,(40,810),'dihydroxidodioxidosulfur',29,B);text(d,(40,880),'Guruhlar hisobi — ionlar rasmi emas',24,G);save(im,'additiv')
im,d=canvas('Per- va perokso- farqi')
box(d,160,'HClO₄: perxlorat kislota','O–O fragmenti talab qilinmaydi')
box(d,420,'H₂SO₅: perokso hosila','O–O fragmenti mavjud')
text(d,(50,700),'Tio-: oltingugurtli',31);text(d,(50,755),'funksional almashtirish',31)
text(d,(50,860),'Prefiksni strukturaga bog‘lang',27,G);save(im,'prefikslar')
im,d=canvas('Kompleks va uning zaryadi')
text(d,(180,180),'[SiF₆]²⁻',70)
for i,(a,b) in enumerate([('6 ta F','hexa + fluorido'),('Butun ion zaryadi','(2−) — arab raqami va ishora'),('Si oksidlanish darajasi','+4; nomda tegishli bo‘lsa (IV)')]):box(d,365+i*175,a,b)
save(im,'kompleks')
im,d=canvas('Nomni tekshirish yo‘li')
for i,(a,b) in enumerate([('1. Obyekt','Molekula / ion / eritma'),('2. Nomlash usuli','Saqlangan / tarkibiy / additiv'),('3. Formula','Guruh va atomlar soni'),('4. Nazorat','Zaryad va fizik holat')]):box(d,150+i*185,a,b)
save(im,'tekshirish')
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
 text(d,(38,595),'Idealizatsiyalangan o‘quv tasviri',24,G);save(im,name)
render('hcl_model','HCl: molekulyar tasvir',[('H',265,325),('Cl',460,325)],[(0,1)])
render('sulfat_model','SO₄²⁻: ideal proyeksiya',[('S',380,295),('O',380,130),('O',200,345),('O',560,345),('O',380,475)],[(0,1),(0,2),(0,3),(0,4)])
render('sulfat_kislota_model','H₂SO₄: ikki OH guruhi',[('S',380,295),('O',380,130),('O',200,315),('O',560,315),('O',380,475),('H',140,405),('H',625,250)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)])
render('sif6_model','[SiF₆]²⁻: oktaedrik tasvir',[('Si',380,310),('F',380,130),('F',380,490),('F',180,310),('F',580,310),('F',270,210),('F',490,410)],[(0,j) for j in range(1,7)])
print('7 nomenclature schemes and 4 molecular models:',OUT)
