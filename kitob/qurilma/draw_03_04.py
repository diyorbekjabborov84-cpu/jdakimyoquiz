#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'titrlash';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 variables={'K_w,c':('K','w,c'),'K_c':('K','c'),'K₂,c':('K','2,c'),'C_s':('C','s'),'C_T':('C','T'),'C_a':('C','a'),'C_b':('C','b'),'V_a':('V','a'),'V_b':('V','b'),'V_e':('V','e'),'V_oxir':('V','oxir'),'V_yakun':('V','yakun'),'pK_In':('pK','In')}
 for part in re.split('('+'|'.join(re.escape(v) for v in variables)+')',s):
  if part in variables:
   main,sub=variables[part];d.text((x,y),main,font=f(n),fill=c);x+=d.textlength(main,font=f(n))
   d.text((x,y+n*.30),sub,font=f(round(n*.72)),fill=c);x+=d.textlength(sub,font=f(round(n*.72)))
  else:d.text((x,y),part,font=f(n),fill=c);x+=d.textlength(part,font=f(n))

def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,min(32,int(32*700/max(700,d.textlength(title,font=f(32))))));return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
from titration_03_04 import ph,indicator_fraction,PHOS
def axes(d,xmin,xmax,ymin,ymax,xlabel,ylabel,xticks,yticks):
 x0,x1,y0,y1=120,680,175,700
 def pos(x,y):return (x0+(x-xmin)/(xmax-xmin)*(x1-x0),y1-(y-ymin)/(ymax-ymin)*(y1-y0))
 line(d,(x0,y0),(x0,y1),G,3);line(d,(x0,y1),(x1,y1),G,3)
 for x,s in xticks:text(d,(pos(x,ymin)[0]-20,717),s,24)
 for y,s in yticks:text(d,(25,pos(xmin,y)[1]-16),s,24)
 text(d,(45,110),ylabel,28);text(d,(200,780),xlabel,29)
 return pos
def csvout(name,headers,rows):
 with (OUT/(name+'.csv')).open('w') as ff:w=csv.writer(ff);w.writerow(headers);w.writerows(rows)
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
 text(d,(38,595),'Idealizatsiyalangan o‘quv modeli',24,G);save(im,name)
im,d=canvas('Ekvivalentlik ≠ kuzatilgan oxir',1000)
for i,(a,b) in enumerate([('Stexiometriya','n(OH⁻) = n(HA)'),('Nazariy nishon','V_e = C_aV_a/C_b'),('Kuzatuv mezoni','Rang yoki elektrod signali'),('Analitik nazorat','V_oxir va V_e farqini baholang')]):box(d,150+i*180,a,b)
save(im,'nuqtalar')
def curve(name,title,ks,xmax,step):
 im,d=canvas(title,1100)
 p=axes(d,0,xmax,0,14,'V(NaOH), mL','Ideal hisobiy pH',[(i,str(i).replace('.',',')) for i in ([0,12.5,25,37.5,50] if xmax==50 else [0,25,50,75])],[(0,'0'),(4,'4'),(7,'7'),(10,'10'),(14,'14')])
 rows=[]
 for i in range(round(xmax/step)+1):
  ml=i*step;rows.append((ml,ph(ml/1000,ks)))
 d.line([p(r[0],r[1]) for r in rows],fill=N,width=5)
 for ml in ([25] if xmax==50 else [25,50,75]):line(d,p(ml,0),p(ml,14),B,2)
 text(d,(45,850),'V_a = 25,00 mL; C_a = 0,1000 M',24,N)
 text(d,(45,910),'NaOH: 0,1000 M; 25 °C; γ≈1',25,B)
 if ks==PHOS:text(d,(45,975),'H₃PO₄: barcha bosqichlar + suv',24,G)
 elif ks:text(d,(45,975),'Shartli HA: K_c = 10⁻⁵ mol/L',25,G)
 else:text(d,(45,975),'Kuchli bir asosli kislota + suv',25,G)
 text(d,(45,1040),'Hisobiy model, tajriba emas',25,G);save(im,name);csvout(name,['Vb_mL','pH'],rows)
curve('kuchli','Kuchli kislota–kuchli asos',None,50,.05)
curve('kuchsiz','Kuchsiz HA–kuchli asos',(1e-5,),50,.05)
curve('fosfat','H₃PO₄: stexiometrik bosqichlar',PHOS,87.5,.125)
im,d=canvas('Indikatorning ikki shakli',1080)
p=axes(d,3,11,0,1,'Hisobiy pH','Shaklning ulushi',[(3,'3'),(5,'5'),(7,'7'),(9,'9'),(11,'11')],[(0,'0'),(.5,'0,5'),(1,'1')])
rows=[]
for i in range(321):
 pH=3+i/40;a=indicator_fraction(pH);rows.append((pH,a,1-a))
for k,col in [(1,N),(2,B)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,860),'Ko‘k: In⁻; bronza: HIn',28,N);text(d,(45,920),'Shartli pK_In = 7',28,B)
text(d,(40,1000),'Ulush grafigi; spektr yoki rang emas',24,G);save(im,'indikator');csvout('indikator',['pH','fraction_In','fraction_HIn'],rows)
im,d=canvas('Indikatorlar: odatiy intervallar',1000)
for i,(label,lo,hi,col) in enumerate([('Metiloranj',3.1,4.4,'#D57E3E'),('Bromtimol ko‘ki',6,7.6,'#458D9B'),('Fenolftalein',8.3,10,'#C86B97')]):
 y=180+i*235;text(d,(45,y),label,31);text(d,(45,y+55),f'{lo:g}–{hi:g} pH',29,B)
 line(d,(100,y+135),(660,y+135),G,3);x0=100+lo/14*560;x1=100+hi/14*560
 d.rounded_rectangle((x0,y+115,x1,y+155),radius=6,fill=col)
text(d,(90,910),'0',27);text(d,(645,910),'14',27);text(d,(270,910),'pH shkalasi',27)
save(im,'intervallar')
im,d=canvas('Oxirgi nuqta og‘ishi',1000)
for i,(a,b) in enumerate([('Oldin to‘xtash','V_oxir < V_e → kamaygan natija'),('Keyin to‘xtash','V_oxir > V_e → ortgan natija'),('Hajm og‘ishi','ε = (V_oxir − V_e)/V_e'),('Boshqa xatolar','Blank, standartlash va hajm')]):box(d,150+i*180,a,b)
save(im,'xato')
im,d=canvas('Hosila: juda yaqin soha',1120)
p=axes(d,24.999,25.001,0,4500,'V(NaOH), mL','dpH/dV, pH mL⁻¹',[(24.999,'24,999'),(25,'25,000'),(25.001,'25,001')],[(0,'0'),(2000,'2000'),(4000,'4000')])
# More margin for long derivative tick labels.
rows=[]
for i in range(401):
 ml=24.999+i*.000005;dt=1e-10;v=ml/1000;der=(ph(v+dt)-ph(v-dt))/(2*dt)/1000;rows.append((ml,ph(v),der))
d.line([p(r[0],r[2]) for r in rows],fill=N,width=5)
text(d,(45,860),'Kuchli kislota–NaOH modeli',27,N);text(d,(45,920),'Simmetrik hosila: δV=10⁻⁷ mL',25,B)
text(d,(45,990),'Ideal model; tajriba shovqini yo‘q',24,G)
text(d,(45,1055),'Cho‘qqi ekvivalentlik atrofida',25,G);save(im,'hosila');csvout('hosila',['Vb_mL','pH','dpH_per_mL'],rows)
im,d=canvas('Titrlash natijasini qabul qilish',1100)
for i,(a,b) in enumerate([('1. Nishon reaksiya','Komponent va proton bosqichi'),('2. O‘lchash zanjiri','Alikvota + standart titrant'),('3. Signal mezoni','Indikator yoki elektrod'),('4. Tuzatishlar','Blank, hajm va suyultirish'),('5. Sifat nazorati','Takrorlar va noaniqlik')]):box(d,130+i*185,a,b)
save(im,'nazorat')
# Original glassware illustration, not a photograph or procedural instruction.
im,d=canvas('Byuretka va kolba: qurilma',1000)
d.rounded_rectangle((355,100,420,590),radius=14,outline=N,width=5)
d.rectangle((361,230,414,580),fill='#BDD8E9')
for y in range(135,560,25):line(d,(355,y),(380 if y%50==10 else 392,y),N,3)
line(d,(290,600),(475,600),B,12);line(d,(390,605),(390,680),N,5)
d.ellipse((378,715,400,745),fill='#7BAEC7')
d.polygon([(280,780),(320,780),(320,820),(450,950),(150,950),(280,820)],outline=N,fill='#E0ECF4',width=5)
text(d,(450,300),'Titrant',29);text(d,(450,450),'V_b',29)
text(d,(450,860),'Namuna',29);text(d,(35,960),'Sxematik tasvir; masshtab saqlanmagan',24,G)
save(im,'qurilma')
# Structural motifs: explicit nitro charges; no invented optimized 3D geometry.
def nitrophenol(name,deprotonated):
 im,d=canvas('para-Nitrofenolyat' if deprotonated else 'para-Nitrofenol',820)
 cx,cy,rad=360,395,130;pts=[(cx+rad*math.cos(-math.pi/2+i*math.pi/3),cy+rad*math.sin(-math.pi/2+i*math.pi/3)) for i in range(6)]
 for i in range(6):line(d,pts[i],pts[(i+1)%6],N,5)
 for i in [0,2,4]:
  a,b=pts[i],pts[(i+1)%6];a=(cx+.82*(a[0]-cx),cy+.82*(a[1]-cy));b=(cx+.82*(b[0]-cx),cy+.82*(b[1]-cy));line(d,a,b,N,3)
 line(d,pts[0],(360,200),N,5);text(d,(330,150),'O⁻' if deprotonated else 'OH',38,B)
 line(d,pts[3],(360,590),N,5);text(d,(335,600),'N⁺',34)
 line(d,(346,645),(260,700),N,4);line(d,(355,650),(269,705),N,3);text(d,(212,703),'O',34)
 line(d,(390,645),(465,700),N,4);text(d,(468,703),'O⁻',34)
 text(d,(35,775),'Ulanish modeli; spektr hisoblanmagan',24,G);save(im,name)
nitrophenol('hin_tuzilish',False);nitrophenol('in_tuzilish',True)
render('fosfat_model','H₃PO₄: uch O–H guruhi',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265),('H',450,520)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6),(4,7)])
print('4 schemes; 5 model graphs; apparatus and 3 structural illustrations; 5 CSV datasets:',OUT)
