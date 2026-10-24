#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'dissotsiatsiya_ph';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 for part in re.split(r'(K_w,c|K_c|K₂,c|C_s|C_T|V_yakun)',s):
  if part in ('K_w,c','K_c','K₂,c','C_s','C_T','V_yakun'):
   main,sub=('K','2,c') if part=='K₂,c' else part.split('_');d.text((x,y),main,font=f(n),fill=c);x+=d.textlength(main,font=f(n))
   d.text((x,y+n*.30),sub,font=f(round(n*.72)),fill=c);x+=d.textlength(sub,font=f(round(n*.72)))
  else:d.text((x,y),part,font=f(n),fill=c);x+=d.textlength(part,font=f(n))
def line(d,a,b,c=N,w=5):d.line((a,b),fill=c,width=w)
def canvas(title,h=960):
 im=Image.new('RGB',(760,h),BG);d=ImageDraw.Draw(im);text(d,(30,24),title,min(32,int(32*700/max(700,d.textlength(title,font=f(32))))));return im,d
def save(im,name):im.save(OUT/(name+'.png'))
def box(d,y,a,b):
 d.rounded_rectangle((32,y,728,y+120),radius=14,outline=N,width=3);text(d,(55,y+14),a,31,B);text(d,(55,y+68),b,28)
from ph_03_03 import strong_h,mono_mix,first_complete_diprotic
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
 text(d,(38,595),'Idealizatsiyalangan o‘quv tasviri',24,G);save(im,name)
# All images are original explanatory drawings, never experimental data.
im,d=canvas('pH: logarifmik shkala',1000)
text(d,(45,115),'Faolliklar nisbatini ko‘ring',29,G)
for i,(ph,a,count) in enumerate([(2,'10⁻²',100),(3,'10⁻³',10),(4,'10⁻⁴',1)]):
 y=230+i*225;text(d,(45,y),f'pH = {ph}',34);text(d,(45,y+62),'a(H⁺) = '+a,30,B)
 d.rounded_rectangle((340,y+5,340+count*3,y+75),radius=3,fill=N)
 text(d,(340,y+105),f'{count} nisbiy birlik',27,G)
text(d,(45,925),'a(H⁺) — o‘lchamsiz faollik',28,G);save(im,'shkala')
im,d=canvas('Muvozanatni uch tayanch yopadi')
for i,(a,b) in enumerate([('Moddiy balans','C = [HA] + [A⁻]'),('Zaryad balansi','h = [A⁻] + [OH⁻]'),('Kislota muvozanati','K_c = h[A⁻]/[HA]'),('Suv muvozanati','K_w,c = h[OH⁻]')]):box(d,150+i*180,a,b)
save(im,'balans')
im,d=canvas('Kuchli kislota: suvni unutmang',1080)
p=axes(d,-10,-2,2,10,'lg(C/c°)','Ideal hisobiy pH',[(-10,'−10'),(-8,'−8'),(-6,'−6'),(-4,'−4'),(-2,'−2')],[(2,'2'),(4,'4'),(6,'6'),(8,'8'),(10,'10')])
rows=[]
for i in range(321):
 lc=-10+i/40;c=10**lc;h=strong_h(c);rows.append((lc,c,h,-math.log10(h),-lc))
for k,col in [(4,B),(3,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,860),'Ko‘k: suv bilan muvozanat',27,N);text(d,(45,920),'Bronza: −lg(C/c°)',28,B)
text(d,(40,1000),'25 °C; γ≈1; o‘lchov emas',26,G);save(im,'kuchli');csvout('kuchli',['log_C_over_c0','C_M','h_M','pH_water','pH_naive'],rows)
im,d=canvas('Kuchsiz HA va kuchli HX qiyosi',1080)
p=axes(d,-10,-2,2,8,'lg(C/c°)','Ideal hisobiy pH',[(-10,'−10'),(-8,'−8'),(-6,'−6'),(-4,'−4'),(-2,'−2')],[(2,'2'),(4,'4'),(6,'6'),(8,'8')])
rows=[]
for i in range(321):
 lc=-10+i/40;c=10**lc;h,a=mono_mix([(c,1e-5)]);hs=strong_h(c);rows.append((lc,c,h,a[0],-math.log10(h),-math.log10(hs)))
for k,col in [(4,N),(5,B)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: HA, K_c = 10⁻⁵ mol/L',25,N);text(d,(45,920),'Bronza: to‘liq ajralgan HX',26,B)
text(d,(40,1000),'Shartli HA; ikkala hisobda suv bor',23,G);save(im,'kuchsiz');csvout('kuchsiz',['log_C_over_c0','C_M','h_M','A_M','pH_HA','pH_strong'],rows)
im,d=canvas('pH lar emas, miqdorlar qo‘shiladi',1100)
for x,title,sub in [(80,'C₁, V₁','n₁ = C₁V₁'),(420,'C₂, V₂','n₂ = C₂V₂')]:
 line(d,(x,200),(x,400),N,6);line(d,(x,400),(x+240,400),N,6);line(d,(x+240,400),(x+240,200),N,6)
 d.rectangle((x+6,270,x+234,393),fill='#CDDFEC');text(d,(x+25,285),title,30);text(d,(x+25,445),sub,29,B)
for x in [200,540]:line(d,(x,520),(380,620),B,5)
box(d,650,'C_s = (n₁ + n₂)/V_yakun','Hajm birligini izchil saqlang')
box(d,835,'Avval h ni hisoblang','So‘ng pH ≈ −lg(h/c°)')
text(d,(45,1030),'Yon reaksiya yo‘q; kuchli bir asosli',25,G);save(im,'miqdor')
im,d=canvas('Umumiy H⁺: HA ajralishi susayadi',1080)
p=axes(d,-8,-1,0,3.5,'lg(C_s/c°)','HA oilasida α, %',[(-8,'−8'),(-6,'−6'),(-4,'−4'),(-2,'−2'),(-1,'−1')],[(0,'0'),(1,'1'),(2,'2'),(3,'3')])
rows=[]
for i in range(281):
 ls=-8+i/40;cs=10**ls;h,a=mono_mix([(.01,1e-5)],cs);rows.append((ls,cs,h,a[0],100*a[0]/.01))
d.line([p(r[0],r[4]) for r in rows],fill=N,width=5)
text(d,(45,860),'C(HA) = 0,0100 mol/L',28,N);text(d,(45,920),'K_c = 10⁻⁵ mol/L; 25 °C',27,B)
text(d,(40,1000),'Yakuniy C lar; ideal shartli hisob',24,G);save(im,'umumiy_ion');csvout('umumiy_ion',['log_Cs_over_c0','Cs_M','h_M','A_M','alpha_percent'],rows)
im,d=canvas('H₂SO₄: ikkinchi bosqich hissasi',1120)
p=axes(d,-5,-1,.5,5.3,'lg(C/c°)','Ideal hisobiy pH',[(-5,'−5'),(-4,'−4'),(-3,'−3'),(-2,'−2'),(-1,'−1')],[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
rows=[]
for i in range(321):
 lc=-5+i/80;c=10**lc;h,ha,a2=first_complete_diprotic(c,.012);rows.append((lc,c,h,ha,a2,-math.log10(h),-lc,-math.log10(2*c)))
for k,col in [(6,G),(7,B),(5,N)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,845),'Ko‘k: ikkinchi bosqich muvozanati',24,N);text(d,(45,900),'Kulrang: h≈C; bronza: h≈2C',25,B)
text(d,(45,960),'K₂,c ≈ 0,012 mol/L; γ≈1',26,G)
text(d,(40,1040),'Birinchi bosqich to‘liq; o‘lchov emas',24,G);save(im,'sulfat');csvout('sulfat',['log_C_over_c0','C_M','h_M','HSO4_M','SO4_M','pH_equilibrium','pH_one','pH_two'],rows)
im,d=canvas('Faollik: shartli molal misol',1050)
for i,(a,b) in enumerate([('m(H⁺)/m° = 0,0100','Molal shkala tanlandi'),('γₘ(H⁺) = 0,75','Shartli, konvensiyaga bog‘liq'),('a(H⁺) = 0,00750','O‘lchamsiz ko‘paytma'),('pH = 2,12494','Ideal γ=1 holatida: 2,00000')]):box(d,150+i*180,a,b)
text(d,(45,980),'γ barcha ionlar uchun bir xil emas',25,G);save(im,'faollik')
im,d=canvas('Hisob → qayta tekshirish',1100)
for i,(a,b) in enumerate([('1. Tarkib va hajm','Yakuniy analitik C lar'),('2. Shartli hisob tanlash','Kuchli / kuchsiz / bosqichli'),('3. Tenglamalar','Modda + zaryad + muvozanat'),('4. Musbat ildiz','Birlik va fizik cheklovlar'),('5. Nazorat','Balanslar, K va taxminlar')]):box(d,130+i*185,a,b)
save(im,'nazorat')
render('hcl_model','HCl: neytral molekula tasviri',[('H',265,325),('Cl',460,325)],[(0,1)])
render('hf_model','HF: H–F ulanishi',[('H',265,325),('F',460,325)],[(0,1)])
render('gidroksoniy_model','H₃O⁺: sxematik ion tasviri',[('O',370,290),('H',230,350),('H',510,350),('H',370,455)],[(0,1),(0,2),(0,3)])
render('sulfat_model','H₂SO₄: ikkita O–H guruhi',[('S',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410),('H',620,265)],[(0,1),(0,2),(0,3),(0,4),(2,5),(3,6)])
print('5 schemes, 4 calculated graphs, 4 original models; 4 CSV datasets',OUT)
