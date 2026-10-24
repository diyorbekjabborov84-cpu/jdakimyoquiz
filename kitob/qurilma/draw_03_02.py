#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'kuch_omillari';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 for part in re.split(r'(K_c|C_T)',s):
  if part in ('K_c','C_T'):
   main,sub=part.split('_');d.text((x,y),main,font=f(n),fill=c);x+=d.textlength(main,font=f(n))
   d.text((x,y+n*.30),sub,font=f(round(n*.72)),fill=c);x+=d.textlength(sub,font=f(round(n*.72)))
  else:d.text((x,y),part,font=f(n),fill=c);x+=d.textlength(part,font=f(n))
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,32);return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
from effects_03_02 import born_factor,pka_temperature
im,d=canvas('Kuch: butun jarayon natijasi')
for i,(a,b) in enumerate([('Boshlang‘ich kislota','Bog‘lar va elektron taqsimot'),('Konjugat asos','Zaryad va delokallashuv'),('Erituvchi','Ikkala tomonning solvatlanishi'),('Harorat','Entalpiya va entropiya')]):box(d,150+i*180,a,b)
save(im,'umumiy')
im,d=canvas('Qiyos yo‘nalishini ajrating')
for i,(a,b) in enumerate([('HX oilasi','H–F; H–Cl; H–Br; H–I'),('Bir davr bo‘ylab','Elektron taqsimot muhim'),('Bir guruh bo‘ylab','Bog‘, o‘lcham va solvatlanish'),('Energiya turi','Gomoliz ≠ suvdagi kislotalik')]):box(d,150+i*180,a,b)
save(im,'boglar')
im,d=canvas('Ikki xil oksokislota qiyosi')
for i,(a,b) in enumerate([('Markaz bir xil','HClO → HClO₂ → HClO₃'),('Terminal O soni bir xil','HOCl / HOBr / HOI'),('Qaysi omil almashdi?','Tuzilish / markaziy atom'),('Qoidaning chegarasi','Boshqa oilaga shartsiz o‘tmang')]):box(d,150+i*180,a,b)
save(im,'oksokislota')
im,d=canvas('Faqat asosni emas, HA ni ham')
for i,(a,b) in enumerate([('HA ning elektron holati','Boshlang‘ich barqarorlanish'),('A⁻ ning elektron holati','Mahsulot barqarorlanishi'),('Muhim kattalik','Ularning nisbiy erkin energiyasi'),('Rezonans yozuvlar soni','pKₐ uchun sanash formulasi emas')]):box(d,150+i*180,a,b)
save(im,'delokallashuv')
im,d=canvas('Zaryad ortadi, bosqich boshqa')
for i,(a,b) in enumerate([('H₃PO₄','Birinchi proton donor'),('H₂PO₄⁻','Keyingi donor manfiy zaryadli'),('HPO₄²⁻','Yana boshqa zaryad muhiti'),('P barcha shaklda +5','Kₐ lar teng degani emas')]):box(d,150+i*180,a,b)
save(im,'zaryad')
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
im,d=canvas('Kontinuumdagi bitta hissa',1080)
p=axes(d,.5,3,0,2,'ρ = r/r₀','B, o‘lchamsiz',[(.5,'0,5'),(1,'1'),(2,'2'),(3,'3')],[(0,'0'),(1,'1'),(2,'2')])
rows=[]
for j in range(251):
 rho=.5+.01*j;rows.append((rho,born_factor(rho,2),born_factor(rho,80)))
for k,col in [(1,B),(2,N)]:d.line([p(row[0],row[k]) for row in rows],fill=col,width=5)
text(d,(45,860),'Bronza: εᵣ = 2',29,B);text(d,(45,920),'Ko‘k: εᵣ = 80',29,N)
text(d,(40,1000),'Solishtirma shartli hisob; pKₐ grafigi emas',25,G);save(im,'born');csvout('born',['rho_r_over_r0','B_epsilon_2','B_epsilon_80'],rows)
im,d=canvas('Mahalliy muhitni tekshiring')
for i,(a,b) in enumerate([('Vodorod bog‘i','HA yoki A⁻ ni barqarorlashtiradimi?'),('Assotsiatsiya','HF + F⁻ ⇌ HF₂⁻'),('Ion juftlanishi','Erkin ionlar ulushi o‘zgaradi'),('Sterik va geometriya','Solvatlanish imkoniyati o‘zgaradi')]):box(d,150+i*180,a,b)
save(im,'mahalliy')
im,d=canvas('Harorat yo‘nalishi turlicha',1080)
p=axes(d,273.15,333.15,4.75,5.25,'T, K','pKₐ',[(273.15,'273'),(293.15,'293'),(313.15,'313'),(333.15,'333')],[(4.8,'4,8'),(5,'5,0'),(5.2,'5,2')])
rows=[]
for j in range(241):
 t=273.15+j*.25;rows.append((t,pka_temperature(t,10000),pka_temperature(t,-10000)))
for k,col in [(1,N),(2,B)]:d.line([p(row[0],row[k]) for row in rows],fill=col,width=5)
line(d,p(298.15,4.75),p(298.15,5.25),G,2)
text(d,(45,860),'Ko‘k: ΔH° = +10 kJ mol⁻¹',26,N);text(d,(45,920),'Bronza: ΔH° = −10 kJ mol⁻¹',25,B)
text(d,(40,1000),'Ikkita shartli hisob; o‘lchov emas',25,G);save(im,'harorat');csvout('harorat',['T_K','pKa_dH_plus10kJ','pKa_dH_minus10kJ'],rows)
im,d=canvas('Qoidani sharti bilan tanlang',1100)
for i,(a,b) in enumerate([('1. Muhit va bosqich','Qaysi proton, qaysi erituvchi?'),('2. Ulanish','Proton ketadigan joyni chizing'),('3. O‘xshashlik','Qiyosda nimalar saqlanadi?'),('4. Hissalar','HA + asos + solvatlanish'),('5. Xulosa','Sifat tendensiyasi yoki sonli dalil')]):box(d,130+i*185,a,b)
save(im,'algoritm')
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
render('hf_model','HF: bog‘ va muhit birga',[('H',265,325),('F',460,325)],[(0,1)])
render('hocl_model','HOCl: H kislorodga ulangan',[('O',310,320),('H',285,420),('Cl',480,320)],[(0,1),(0,2)])
render('nitrat_model','NO₃⁻: tekis anion tasviri',[('N',380,340),('O',380,155),('O',220,432),('O',540,432)],[(0,1),(0,2),(0,3)])
render('fosfat_model','H₃PO₄: zaryad qatorining boshi',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265),('H',450,520)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6),(4,7)])
print('7 schemes, 2 illustrative graphs, 4 molecular renders and 2 CSV datasets:',OUT)
