#!/usr/bin/env python3
"""Original classification figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'tasnif';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):d.text(p,s,font=f(n),fill=c)
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
im,d=canvas('Bir modda — ko‘p mezon')
for i,(a,b) in enumerate([('Tarkib','Kislorod bormi?'),('Asoslilik','Nechta proton berish bosqichi?'),('Kuch','Qaysi erituvchi va bosqich?'),('Tuzilish','Qanday atomlar tutashgan?'),('Redoks va fizik xossa','Qaysi reaksiya va sharoit?')]):box(d,120+i*157,a,b)
save(im,'mezonlar')
im,d=canvas('Tarkib ≠ kuch')
box(d,140,'KISLORODSIZ','HCl, HF, H₂S');box(d,340,'KISLORODLI','HNO₃, H₃PO₃, H₃PO₄')
text(d,(50,575),'Har bir guruh ichida:',32)
for i,s in enumerate(['kuch har xil bo‘lishi mumkin;','asoslilik alohida aniqlanadi;','ulanish sxemasi tekshiriladi.']):text(d,(50,650+i*65),s,28)
save(im,'tarkib')
im,d=canvas('3 ta H — turli asoslilik')
for i,(form,stru,n) in enumerate([('H₃PO₂','H₂P(=O)(OH)','1 ta O–H'),('H₃PO₃','HP(=O)(OH)₂','2 ta O–H'),('H₃PO₄','P(=O)(OH)₃','3 ta O–H')]):
 y=130+i*260;text(d,(60,y),form,43);text(d,(60,y+73),stru,35);text(d,(60,y+138),n,33,B)
text(d,(50,915),'P–H bu hisobga qo‘shilmaydi',27,G);save(im,'asoslilik')
im,d=canvas('Dissotsiatsiya ulushi')
x0,x1,y0,y1=120,680,170,705
line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
def pos(x,y):return x0+(x+5)/8*(x1-x0),y1-y*(y1-y0)
rows=[]
for j in range(321):
 x=-5+j*.025;q=10**x;alpha=2/(1+math.sqrt(1+4/q));rows.append((x,q,alpha))
d.line([pos(x,a) for x,q,a in rows],fill=N,width=6)
for x in [-5,-3,-1,1,3]:text(d,(pos(x,0)[0]-13,724),str(x),26)
for y,s in [(0,'0'),(.5,'0,5'),(1,'1')]:text(d,(48,pos(0,y)[1]-18),s,27)
text(d,(55,110),'α',34);text(d,(215,785),'lg(Kₐ / c)',31)
text(d,(45,860),'Ideal bir bosqichli hisob',28,G);text(d,(45,910),'Q = Kₐ / c = α²/(1−α)',27,B);save(im,'ulush')
with (OUT/'ulush.csv').open('w') as ff:w=csv.writer(ff);w.writerow(['log10_Ka_over_c','Ka_over_c','alpha']);w.writerows(rows)
im,d=canvas('Bog‘ turi — alohida mezon')
for y,title,a,b,c in [(200,'Kondensatsiyalangan skelet','P','O','P'),(530,'Perokso fragment','S','O','O')]:
 text(d,(50,y-80),title,29);text(d,(105,y+20),a,48);text(d,(355,y+20),b,48);text(d,(605,y+20),c,48)
 line(d,(170,y+52),(335,y+52));line(d,(420,y+52),(585,y+52))
text(d,(45,790),'Faqat skelet fragmentlari',29,G);text(d,(45,850),'Boshqa atomlar berilmagan',28,G);save(im,'skelet')
im,d=canvas('Kuchsiz ≠ xavfsiz')
text(d,(270,160),'HF',100,B)
for i,(a,b) in enumerate([('Kislotalik','Suvda kuchsiz'),('Xavflilik','Juda xavfli modda'),('Kerakli ma’lumot','Aynan konsentratsiya uchun SDS')]):box(d,355+i*175,a,b)
save(im,'xavf')
im,d=canvas('Kimyoviy pasport')
for i,(a,b) in enumerate([('1. Obyekt va sharoit','Modda / ion / eritma'),('2. Tarkib va ulanish','Atomlar, guruhlar, ko‘priklar'),('3. Asoslilik va kuch','Bosqichlar + muvozanat'),('4. Alohida xossalar','Redoks, uchuvchanlik, xavf')]):box(d,150+i*185,a,b)
save(im,'pasport')
def sphere(d,x,y,r,color,label):
 for rr in range(r,0,-1):
  t=1-rr/r;cx=x-r*.22*t;cy=y-r*.28*t;col=tuple(min(255,int(c*(.55+.45*t)+255*.18*t)) for c in color)
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=col)
 bb=d.textbbox((0,0),label,font=f(29));text(d,(x-(bb[2]-bb[0])/2,y-21),label,29,N if label=='H' else '#FFFFFF')
def render(name,title,atoms,bonds):
 im,d=canvas(title,650)
 for i,j in bonds:
  a,b=atoms[i],atoms[j];line(d,(a[1],a[2]),(b[1],b[2]),'#8F9DA6',17);line(d,(a[1]-3,a[2]-3),(b[1]-3,b[2]-3),'#CAD5DD',5)
 colors={'O':(225,80,75),'P':(215,145,55),'B':(180,115,160),'F':(65,170,115),'H':(245,246,249)}
 for label,x,y in atoms:sphere(d,x,y,44 if label!='H' else 27,colors[label],label)
 text(d,(38,595),'Idealizatsiyalangan o‘quv tasviri',24,G);save(im,name)
render('hf_model','HF: qutbli molekula',[('H',265,325),('F',460,325)],[(0,1)])
for name,title,lower in [('fosfat_model','H₃PO₄: uchta O–H','O'),('fosfit_model','H₃PO₃: bitta P–H','H')]:
 atoms=[('P',370,285),('O',370,130),('O',195,315),('O',545,315),(lower,370,440),('H',150,410),('H',620,265)]
 bonds=[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)]
 if lower=='O':atoms.append(('H',450,500));bonds.append((4,7))
 render(name,title,atoms,bonds)
render('borat_model','B(OH)₃: tekis tasvir',[('B',380,310),('O',380,155),('O',220,402),('O',540,402),('H',465,110),('H',130,355),('H',555,500)],[(0,1),(0,2),(0,3),(1,4),(2,5),(3,6)])
print('11 original images; 1 taxminiy hisob CSV:',OUT)
