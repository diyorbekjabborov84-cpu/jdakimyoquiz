#!/usr/bin/env python3
"""Seven teaching figures and four shaded molecular models, all original."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'rezonans';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):d.text(p,s,font=f(n),fill=c)
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def dashed(d,a,b,c=B):
 dx=b[0]-a[0];dy=b[1]-a[1];l=math.hypot(dx,dy)
 for j in range(0,int(l),25):
  t=j/l;u=min((j+13)/l,1);line(d,(a[0]+dx*t,a[1]+dy*t),(a[0]+dx*u,a[1]+dy*u),c,5)
def nitrate(d,cy,k):
 cx=380;ps=[(380,cy-78),(215,cy+70),(545,cy+70)]
 text(d,(cx-20,cy-20),'N⁺',34)
 for j,(x,y) in enumerate(ps):
  dx=x-cx;dy=y-cy;l=math.hypot(dx,dy);a=(cx+dx*.23,cy+dy*.23);b=(cx+dx*.73,cy+dy*.73)
  if k==j:
   px=-dy/l*6;py=dx/l*6;line(d,(a[0]+px,a[1]+py),(b[0]+px,b[1]+py));line(d,(a[0]-px,a[1]-py),(b[0]-px,b[1]-py))
  else:line(d,a,b)
  text(d,(x-17,y-18),'O' if k==j else 'O⁻',33)
im,d=canvas('NO₃⁻: uchta hissa',1080)
for i in range(3):
 cy=220+i*300;nitrate(d,cy,i)
 if i<2:text(d,(359,cy+135),'↕',46,B)
text(d,(35,1015),'Bitta ion; yadrolar ko‘chmaydi',28,G);save(im,'hissalar')
im,d=canvas('Rezonans tekshiruvi')
labels=[('1. Bir xil yadrolar','Ulanish o‘zgarmaydi'),('2. Bir xil elektronlar','Hisob saqlanadi'),('3. Bir xil zaryad','Yig‘indi o‘zgarmaydi'),('4. Oktet tekshiruvi','N uchun sakkiz elektron')]
for i,(a,b) in enumerate(labels):
 y=125+i*180;d.rounded_rectangle((30,y,730,y+135),radius=16,outline=N,width=3);text(d,(55,y+18),a,31);text(d,(55,y+75),b,29,G)
text(d,(40,875),'↔ rezonans     ⇌ muvozanat',31,B);save(im,'tekshiruv')
im,d=canvas('Delokallashgan tasvir')
# Equal bonds with dashed additional formal bond contribution; not density calculation.
center=(380,420);ps=[(380,180),(170,550),(590,550)]
for x,y in ps:
 line(d,center,(x,y));dx=x-380;dy=y-420;l=math.hypot(dx,dy);px=-dy/l*15;py=dx/l*15
 dashed(d,(380+dx*.2+px,420+dy*.2+py),(380+dx*.8+px,420+dy*.8+py))
 d.ellipse((x-43,y-43,x+43,y+43),fill='#BD5050');text(d,(x-18,y-24),'O',38,'#FFFFFF')
d.ellipse((345,385,415,455),fill='#4777B6');text(d,(363,397),'N',34,'#FFFFFF')
text(d,(60,700),'Uchta teng yo‘nalish',32);text(d,(60,765),'Formal o‘rtacha: 4/3',31,B);text(d,(60,835),'Elektron zichlik xaritasi emas',27,G);save(im,'delokal')
im,d=canvas('Vodorod bog‘i geometriyasi')
for y,label,bent in [(250,'To‘g‘ri yo‘nalishga yaqin',False),(580,'Egilgan kontakt',True)]:
 text(d,(55,y-100),label,30)
 text(d,(65,y),'X',44);text(d,(285,y),'H',44);text(d,(600,y+(100 if bent else 0)),'Y',44)
 line(d,(115,y+30),(270,y+30));dashed(d,(340,y+30),(580,y+(130 if bent else 30)))
text(d,(55,800),'X–H: kovalent bog‘',31);text(d,(55,858),'H···Y: vodorod bog‘i',31,B);save(im,'geometriya')
im,d=canvas('IR: faraziy tasmalar')
x0,x1,y0,y1=115,680,180,690
line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
def pos(x,y):return (x0+(4000-x)/1200*(x1-x0),y1-y*430)
rows=[]
for x in range(2800,4001,3):
 a=.85*math.exp(-.5*((x-3700)/35)**2);b=math.exp(-.5*((x-3300)/145)**2);rows.append((x,a,b))
for idx,col in [(1,N),(2,B)]:d.line([pos(r[0],r[idx]) for r in rows],fill=col,width=5)
for x in [4000,3600,3200,2800]:text(d,(pos(x,0)[0]-30,710),str(x),25)
text(d,(45,115),'Shartli absorbans',28);text(d,(150,770),'To‘lqin soni, cm⁻¹',29)
text(d,(45,835),'Ko‘k: erkin X–H hisobi',27,N);text(d,(45,883),'Bronza: bog‘langan hisob',27,B);save(im,'ir_model')
with (OUT/'ir_model.csv').open('w') as ff:w=csv.writer(ff);w.writerow(['wavenumber_cm-1','free_model','bonded_model']);w.writerows(rows)
im,d=canvas('Proton almashinuvi')
for y,after in [(270,False),(625,True)]:
 text(d,(50,y-105),'Keyin' if after else 'Oldin',32)
 for x in [130,375,620]:text(d,(x-24,y),'O',44)
 for i,x in enumerate([130,375]):
  hx=x+(160 if after else 85);text(d,(hx-13,y+8),'H',32)
  if after:dashed(d,(x+32,y+28),(hx-20,y+28));line(d,(hx+25,y+28),(x+215,y+28))
  else:line(d,(x+32,y+28),(hx-20,y+28));dashed(d,(hx+25,y+28),(x+215,y+28))
text(d,(45,795),'O skeleti shartli o‘zgarmas',27,G);text(d,(45,850),'Boshqa H atomlar chizilmagan',27,G);save(im,'proton')
im,d=canvas('Ikki darajadagi tushuntirish')
for y,title,lines in [(160,'REZONANS',['Bitta zarracha','Elektronlar delokallashuvi','Muqobil Lewis yozuvlari']),(530,'VODOROD BOG‘I',['Donor va akseptor','Yo‘nalgan o‘zaro ta’sir','Geometriya + boshqa dalillar'])]:
 d.rounded_rectangle((30,y,730,y+300),radius=16,outline=N,width=3);text(d,(55,y+25),title,30,B)
 for i,s in enumerate(lines):text(d,(55,y+100+i*59),s,28)
save(im,'qiyos')
# Shaded ball-and-stick teaching renders, manually chosen ideal geometry, not experimental coordinates.
def sphere(d,x,y,r,color,label):
 for rr in range(r,0,-1):
  t=1-rr/r;cx=x-r*.22*t;cy=y-r*.28*t
  col=tuple(int(c*(.55+.45*t)+255*.18*t) for c in color);col=tuple(min(255,v) for v in col)
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=col)
 box=d.textbbox((0,0),label,font=f(31));text(d,(x-(box[2]-box[0])/2,y-22),label,31,'#FFFFFF' if label!='H' else N)
def render(name,title,atoms,bonds,contacts=()):
 im,d=canvas(title,650)
 for i,j in bonds:
  a,b=atoms[i],atoms[j];line(d,(a[1],a[2]),(b[1],b[2]),'#8F9DA6',18);line(d,(a[1]-3,a[2]-3),(b[1]-3,b[2]-3),'#CAD5DD',6)
 for i,j in contacts:dashed(d,(atoms[i][1],atoms[i][2]),(atoms[j][1],atoms[j][2]))
 colors={'O':(225,80,75),'N':(70,125,205),'C':(100,110,123),'H':(245,246,249)}
 for label,x,y in atoms:sphere(d,x,y,48 if label!='H' else 30,colors[label],label)
 text(d,(38,595),'O‘quv tasviri; masshtabsiz',26,G);save(im,name)
for name,title,center in [('nitrat_model','Nitrat: tekis tasvir','N'),('karbonat_model','Karbonat: tekis tasvir','C')]:
 render(name,title,[(center,380,340),('O',380,155),('O',220,432),('O',540,432)],[(0,1),(0,2),(0,3)])
render('dimer_model','Suv dimeri: O–H···O',[('O',185,350),('H',290,350),('H',159,249),('O',510,350),('H',592,286),('H',552,445)],[(0,1),(0,2),(3,4),(3,5)],[(1,3)])
render('gidroksoniy_model','H₃O⁺: piramidal tasvir',[('O',380,290),('H',220,365),('H',540,365),('H',380,470)],[(0,1),(0,2),(0,3)])
print('11 original visuals; 1 illustrative spectrum CSV:',OUT)
