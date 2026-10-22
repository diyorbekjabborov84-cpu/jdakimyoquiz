"""Original vector-like Pillow figures: formal redox models, never measured curves."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,math
from redox_04_02 import save as save_data
A=Path(__file__).resolve().parents[1]/'rasmlar/redoks';A.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';TEAL='#318E95';BG='#F5F8FA'
def font(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def txt(d,x,y,s,n=28,c=N):d.text((x,y),s,font=font(n),fill=c)
def title(d,s):
 n=32
 while d.textlength(s,font=font(n))>700:n-=1
 txt(d,30,22,s,n)
def canvas(s,h=1120):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);title(d,s);return im,d
def save(im,n):im.save(A/(n+'.png'))
def axes(d,xlo,xhi,ylo,yhi,xlabel,ylabel,xt,yt):
 def p(x,y):return (120+(x-xlo)/(xhi-xlo)*560,700-(y-ylo)/(yhi-ylo)*525)
 d.line((120,175,120,700,680,700),fill=G,width=3)
 for x,s in xt:txt(d,p(x,ylo)[0]-15,718,s,24)
 for y,s in yt:txt(d,14,p(xlo,y)[1]-16,s,24)
 txt(d,45,108,ylabel,28);txt(d,165,780,xlabel,27)
 return p
def rows(n):return [{k:float(v) for k,v in r.items()} for r in csv.DictReader((A/(n+'.csv')).open())]
def curve(d,p,rr,x,y,color):d.line([p(r[x],r[y]) for r in rr],fill=color,width=5)
save_data()
im,d=canvas('E ko‘paymaydi, ΔG reaksiya ko‘lamiga bog‘liq')
p=axes(d,-.2,1.2,-600,120,'E(element), V','ΔG, kJ / mol reaksiya',[(-.2,'−0,2'),(0,'0'),(.6,'0,6'),(1.2,'1,2')],[(-600,'−600'),(-300,'−300'),(0,'0'),(120,'120')])
for n,c in [(1,N),(2,B),(5,TEAL)]:curve(d,p,rows('energiya'),'E_cell_V',f'dG_n{n}_kJ',c)
for y,s,c in [(870,'n=1 — ko‘k',N),(925,'n=2 — bronza',B),(980,'n=5 — ko‘kimtir',TEAL)]:txt(d,45,y,s,28,c)
txt(d,45,1050,'ΔG=−nFE; nazariy bog‘lanish',26,G);save(im,'energiya')
im,d=canvas('Proton faolligi redoks potensialini o‘zgartiradi',1200)
p=axes(d,0,4,-.3,1.6,'pH = −lg a(H⁺)','E, V (SHE)',[(0,'0'),(2,'2'),(4,'4')],[(-.3,'−0,3'),(0,'0'),(.8,'0,8'),(1.6,'1,6')])
for k,c in [('H_V',G),('Mn_V',N),('NO_V',B)]:curve(d,p,rows('ph'),'pH',k,c)
for y,s,c in [(860,'H⁺/H₂ — kulrang',G),(920,'MnO₄⁻/Mn²⁺ — ko‘k',N),(980,'NO₃⁻/NO — bronza',B)]:txt(d,45,y,s,28,c)
txt(d,45,1060,'Boshqa nisbiy faolliklar = 1; 25 °C',25,G)
txt(d,45,1120,'Shartli chiziqlar; faza xaritasi emas',25,G);save(im,'ph')
im,d=canvas('Elektron sig‘imi: mahsulotni oldindan ayting',1140)
rr=list(csv.DictReader((A/'sigim.csv').open()))
labels=['N(+5) → NO₂','N(+5) → NO','N(+5) → NH₄⁺','S(+6) → SO₂','S(+6) → S','S(+6) → H₂S']
for i,(r,label) in enumerate(zip(rr,labels)):
 y=150+i*125;n=int(r['electrons_per_center']);txt(d,40,y,label,27)
 d.rounded_rectangle((50,y+44,50+n*70,y+82),radius=5,fill=N if i<3 else B)
 txt(d,70+n*70,y+40,str(n)+' e⁻',25)
txt(d,40,955,'Bir N yoki S markaziga to‘g‘ri keladi',26,G)
txt(d,40,1020,'Bu mahsulotlar aralashmasi bashorati emas',25,G);save(im,'sigim')
im,d=canvas('H₂O₂: ikki qaytarilish jufti, ikki xil rol',1150)
p=axes(d,0,4,0,2,'pH = −lg a(H⁺)','E, V (SHE)',[(0,'0'),(2,'2'),(4,'4')],[(0,'0'),(1,'1'),(2,'2')])
for k,c in [('water_V',N),('oxygen_V',B)]:curve(d,p,rows('peroksid'),'pH',k,c)
txt(d,45,860,'H₂O₂/H₂O — ko‘k; E°=1,776 V',27,N)
txt(d,45,925,'O₂/H₂O₂ — bronza; E°=0,695 V',27,B)
txt(d,45,995,'Farq 1,081 V; boshqa faolliklar = 1',25,G)
txt(d,45,1060,'25 °C; ideal qiyos, tajriba emas',26,G);save(im,'peroksid')

def scheme(n,title_,boxes):
 im,d=canvas(title_,1080)
 for i,(label,a,b) in enumerate(boxes):
  y=135+i*215;d.rounded_rectangle((32,y,728,y+165),radius=15,outline=N,width=3)
  txt(d,52,y+16,label,30,B);txt(d,52,y+68,a,27);txt(d,52,y+113,b,26,G)
  if i<len(boxes)-1:txt(d,360,y+173,'↓',33,B)
 save(im,n)
scheme('elektron','Kislota qatnashsa ham jarayonlar har xil',[
 ('Proton ko‘chishi','HCl + NH₃ → NH₄Cl','Oksidlanish darajalari o‘zgarmaydi'),
 ('Elektron almashinuvi','Zn → Zn²⁺ + 2e⁻','Qaytaruvchi o‘zi oksidlanadi'),
 ('Qabul qiluvchi proton','2H⁺ + 2e⁻ → H₂','H⁺ oksidlovchi; H(+1) → H(0)'),
 ('Alohida oksidlovchi anion','NO₃⁻ → NO; N(+5) → N(+2)','Bu yo‘l proton ajralishidan boshqa')])
scheme('balans','Ion–elektron usuli: nishon va muhit',[
 ('1. Mahsulot nishoni','MnO₄⁻ → Mn²⁺','Mn(+7) → Mn(+2): 5e⁻'),
 ('2. O va H balansi','MnO₄⁻ + 8H⁺ + 5e⁻','→ Mn²⁺ + 4H₂O'),
 ('3. Ikkinchi yarimreaksiya','5Fe²⁺ → 5Fe³⁺ + 5e⁻','Elektronlar teng miqdorda yo‘qoladi'),
 ('4. Umumiy nazorat','Chap va o‘ng zaryad: +17','Mn, Fe, O va H ham teng')])
scheme('nitrat','Nitrat: bir nom, turli azot nishonlari',[
 ('N(+5) → N(+4)','NO₂: har N uchun 1e⁻','Cu 2e⁻ beradi: 2NO₂ / Cu'),
 ('N(+5) → N(+2)','NO: har N uchun 3e⁻','3Cu 6e⁻ beradi: 2NO / 3Cu'),
 ('Tuzda qolgan nitrat','Cu(NO₃)₂ dagi N(+5)','Bu nitrat elektron qabul qilmagan'),
 ('Kuzatuvni ehtiyot talqin qiling','2NO + O₂ → 2NO₂','Havodagi rang birlamchi mahsulot emas')])
scheme('fosfor','P–H va O–H: ikki xil kimyoviy vazifa',[
 ('H₃PO₄','3 O–H; 0 P–H; P(+5)','Neytrallanishdagi to‘liq nishon: 3H⁺'),
 ('H₃PO₃','2 O–H; 1 P–H; P(+3)','Fosfat nishoniga oksidlansa 2e⁻'),
 ('H₃PO₂','1 O–H; 2 P–H; P(+1)','Fosfat nishoniga oksidlansa 4e⁻'),
 ('H sonining o‘zi yetmaydi','Proton va elektron ekvivalenti boshqa','An’anaviy ulanish yozuvlari')])
scheme('hisob','Ideal hisob: qoldiq juft potensialni belgilaydi',[
 ('1. Qabul qiluvchi','0,4000 mmol MnO₄⁻','Mn²⁺ nishoni: 2,000 mmol e⁻'),
 ('2. Beruvchi','2,500 mmol Fe²⁺','0,5000 mmol Fe²⁺ qoladi'),
 ('3. Yakuniy nisbat','Fe³⁺ / Fe²⁺ = 2,000 / 0,5000 = 4','70,00 mL; ideal ionlar'),
 ('4. Qoldiq juft E si','E=0,771+0,05915935·lg4','E≈0,80662 V (SHE); n=1')])
COL={'H':(220,225,230),'O':(205,75,70),'N':(60,120,190),'P':(190,125,40)}
def sphere(d,x,y,label,r=40):
 col=COL[label]
 for k in range(r,0,-1):
  t=1-k/r;c=tuple(min(255,round(v*(.6+.4*t)+255*.12*t)) for v in col)
  d.ellipse((x-k-5*t,y-k-5*t,x+k-5*t,y+k-5*t),fill=c)
 box=d.textbbox((0,0),label,font=font(28));txt(d,x-(box[2]-box[0])/2,y-19,label,28,N if label=='H' else 'white')
def molecule(name,title_,atoms,bonds,lines):
 im,d=canvas(title_,800)
 for i,j in bonds:
  a,b=atoms[i],atoms[j];c=B if 'P' in [a[0],b[0]] and 'H' in [a[0],b[0]] else '#8799A6'
  d.line((a[1],a[2],b[1],b[2]),width=15,fill=c)
 for label,x,y in atoms:sphere(d,x,y,label,26 if label=='H' else 43)
 for i,line in enumerate(lines):txt(d,35,605+i*58,line,25,G)
 save(im,name)
molecule('nitrat_model','NO₃⁻: tekis ulanish va delokalizatsiya',[
 ('N',380,310),('O',380,115),('O',211,408),('O',549,408)],[(0,1),(0,2),(0,3)],['N(+5), O(−2); ionning jami zaryadi −1','Uch N–O ulanish; rezonansli anion','Chiziqlar lokal bog‘ tartibi tasviri emas'])
molecule('fosfit_model','H₃PO₃: bitta P–H, ikkita O–H',[
 ('P',380,310),('O',380,120),('O',210,300),('O',550,300),('H',100,260),('H',660,260),('H',380,500)],[(0,1),(0,2),(0,3),(2,4),(3,5),(0,6)],['HP(O)(OH)₂; P ning darajasi +3','Bronza — P–H ulanish','P darajasi: an’anaviy H(+1) konvensiyasi'])
molecule('gipofosfit_model','H₃PO₂: ikkita P–H, bitta O–H',[
 ('P',380,310),('O',380,120),('O',210,300),('H',100,260),('H',550,300),('H',380,500)],[(0,1),(0,2),(2,3),(0,4),(0,5)],['H₂P(O)(OH); P ning darajasi +1','Bronza — ikki P–H ulanish','P darajasi: an’anaviy H(+1) konvensiyasi'])
molecule('peroksid_model','H₂O₂: O–O bog‘i va O(−1)',[
 ('H',140,200),('O',280,320),('O',470,320),('H',610,440)],[(0,1),(1,2),(2,3)],['O–O ulanish peroksid guruhini belgilaydi','Suvga qaytarilish: O(−1) → O(−2)','Sxema; haqiqiy molekula tekis emas'])
print('4 graphs + CSV, 5 schemes, 4 original connectivity models.')

# Sidebar crops keep the complete P/O/H connectivity while removing repeated raster captions.
for stem in ['fosfit','gipofosfit']:
 Image.open(A/(stem+'_model.png')).crop((50,60,710,555)).save(A/(stem+'_yon.png'))
