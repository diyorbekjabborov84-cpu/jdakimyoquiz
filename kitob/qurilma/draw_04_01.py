#!/usr/bin/env python3
"""Original acid equilibrium figures and idealized molecular illustrations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rasmlar'/'neytrallanish';OUT.mkdir(parents=True,exist_ok=True)
N='#0B2C4A';B='#B37C2D';G='#657583';BG='#F5F8FA'
def f(n):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',n)
def text(d,p,s,n=30,c=N):
 x,y=p
 variables={'K_w,c':('K','w,c'),'K_c':('K','c'),'K₂,c':('K','2,c'),'C_s':('C','s'),'C_T':('C','T'),'C_a':('C','a'),'C_b':('C','b'),'V_a':('V','a'),'V_b':('V','b'),'V_e':('V','e'),'V_oxir':('V','oxir'),'V_yakun':('V','yakun'),'pK_In':('pK','In'),'β_juft':('β','juft'),'k_obs':('k','obs'),'k_HA':('k','HA'),'k_ref':('k','ref'),'E_a':('E','a'),'k_f':('k','f'),'k_r':('k','r'),'k_A':('k','A'),'C_T':('C','T'),'C_P':('C','P'),'ΔH_neut':('ΔH','neut')}
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
from neutral_04_01 import proton_transfer,phosphate,calorimetry,salt_ph
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
im,d=canvas('Yozuvdan ion jarayoniga',1050)
for i,(a,b) in enumerate([('Molekulyar balans','HCl + NaOH → NaCl + H₂O'),('Eritmadagi ionlar','H₃O⁺, Na⁺, Cl⁻, OH⁻'),('Qisqartirilgan jarayon','H₃O⁺ + OH⁻ → 2H₂O'),('Kuzatuvchi zaryadlar','Na⁺ va Cl⁻ eritmada qoladi')]):box(d,150+i*180,a,b)
text(d,(45,980),'Kuchsiz va qattiq turlarni asossiz ajratmang',22,G);save(im,'ionli')
im,d=canvas('Proton ko‘chishi: K va ulush',1120)
p=axes(d,-6,6,0,1,'ΔpKₐ = lg K','O‘zgargan ulush, x/C',[(-6,'−6'),(-3,'−3'),(0,'0'),(3,'3'),(6,'6')],[(0,'0'),(.5,'0,5'),(1,'1')])
rows=[]
for i in range(481):
 dp=-6+i/40;k,frac,dg=proton_transfer(dp);rows.append((dp,k,frac,dg))
d.line([p(r[0],r[2]) for r in rows],fill=N,width=5)
text(d,(45,855),'Boshlang‘ich HA va B miqdori teng',24,N)
text(d,(45,915),'Mahsulotlar dastlab yo‘q; ideal model',23,B)
text(d,(45,975),'x/C = √K/(1+√K)',30,G)
text(d,(45,1040),'Suv/yon muvozanatlar tashlangan',25,G);save(im,'yonalish');csvout('yonalish',['delta_pKa','K','fraction','dG_standard_Jmol'],rows)
im,d=canvas('Ekvivalent — tanlangan bosqich',1050)
for i,(a,b) in enumerate([('HCl → xlorid','1 mol uchun 1 mol OH⁻'),('H₂SO₄ → sulfat','1 mol uchun 2 mol OH⁻'),('H₃PO₄ → formal fosfat','Nishonga qarab 1 / 2 / 3 mol'),('Chegaralovchi reagent','n / ν eng kichik bo‘lgan reagent')]):box(d,150+i*180,a,b)
text(d,(45,980),'Formal talab ≠ boshlang‘ich dissotsiatsiya',23,G);save(im,'ekvivalent')
im,d=canvas('Formal tuz va haqiqiy fosfat turlari',1200)
p=axes(d,0,3,0,1,'r = n(NaOH)/n(P)','Fosfat oilasidagi ulush',[(0,'0'),(1,'1'),(2,'2'),(3,'3')],[(0,'0'),(.5,'0,5'),(1,'1')])
rows=[]
for i in range(301):
 r=i/100;ph,al=phosphate(r);rows.append((r,ph,*al))
for k,col in [(2,G),(3,N),(4,B),(5,'#398E94')]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
for y,label,col in [(850,'H₃PO₄ — kulrang',G),(910,'H₂PO₄⁻ — ko‘k',N),(970,'HPO₄²⁻ — bronza',B),(1030,'PO₄³⁻ — ko‘kimtir', '#398E94')]:text(d,(45,y),label,28,col)
text(d,(45,1120),'Yakuniy C_P=0,0100 M; 25 °C; γ≈1',24,G);save(im,'fosfat');csvout('fosfat',['OH_equivalents_per_P','pH','alpha_H3PO4','alpha_H2PO4','alpha_HPO4','alpha_PO4'],rows)
im,d=canvas('Ekvivalentlik har doim pH=7 emas',1120)
p=axes(d,0,4,0,10,'Tuz modeli','Ideal hisobiy pH',[],[(0,'0'),(5,'5'),(7,'7'),(10,'10')])
rows=[]
for j,(name,value) in enumerate(salt_ph().items()):
 x=j+.5;xa,ya=p(x-.27,value);xb,yb=p(x+.27,0);d.rounded_rectangle((xa,ya,xb,yb),radius=4,fill=N if j%2==0 else B)
 text(d,(xa-5,ya-42),f'{value:.2f}'.replace('.',','),25,N);text(d,(xa-3,725),['NaCl','NaA','NH₄Cl','BH⁺A⁻'][j],22)
 rows.append((name,.01,value))
text(d,(45,855),'Barcha tuz oilalari: C=0,0100 M',25,N)
text(d,(45,915),'NaA va BH⁺A⁻ — shartli modellar',24,B)
text(d,(45,975),'Formal sarf va proton muvozanati boshqa',22,G)
text(d,(45,1040),'25 °C; suvli ideal hisob; tajriba emas',23,G);save(im,'tuz_ph');csvout('tuz_ph',['salt_model','C_M','pH'],rows)
im,d=canvas('Issiqlik: shartli Hess qiyosi',1120)
p=axes(d,0,10,0,600,'Reaksiya miqdori ξ, mmol','Ajralgan issiqlik, J',[(0,'0'),(5,'5'),(10,'10')],[(0,'0'),(300,'300'),(600,'600')])
rows=[]
for i in range(201):
 mmol=i/20;q1=calorimetry(mmol/1000)[1];q2=calorimetry(mmol/1000,dh=-42000)[1];rows.append((mmol,q1,q2))
for k,col in [(1,N),(2,B)]:d.line([p(r[0],r[k]) for r in rows],fill=col,width=5)
text(d,(45,855),'Ko‘k: ΔH_neut=−57,0 kJ/mol',25,N)
text(d,(45,915),'Bronza: −57,0+15,0=−42,0',25,B)
text(d,(45,975),'Shartli doimiy entalpiyalar; tajriba emas',22,G)
text(d,(45,1040),'Bu qiymatlar HF ga biriktirilmagan',24,G);save(im,'issiqlik');csvout('issiqlik',['extent_mmol','q_abs_model57_J','q_abs_model42_J'],rows)
im,d=canvas('Tuz hosil qilish yo‘llari',1050)
for i,(a,b) in enumerate([('Gidroksid bilan','Kislota + OH⁻ → suv + tuz ionlari'),('Ammiak bilan','NH₃ + H₃O⁺ → NH₄⁺ + H₂O'),('Asosli oksid bilan','CuO + 2H₃O⁺ → Cu²⁺ + 3H₂O'),('Gidrokarbonat bilan','HCO₃⁻ + H₃O⁺ → CO₂ + 2H₂O')]):box(d,150+i*180,a,b)
text(d,(45,980),'Gaz va qattiq fazalar alohida hisoblanadi',23,G);save(im,'yollar')
im,d=canvas('Formula — panjara — eritma',1050)
for i,(a,b) in enumerate([('NaCl formulasi','Na : Cl analitik nisbati 1 : 1'),('Kristall','Ionlarning fazoviy panjarasi'),('Eritma','Solvatlangan Na⁺ va Cl⁻'),('Tasnif va pH','Kislotali tuz ≠ albatta pH<7')]):box(d,150+i*180,a,b)
text(d,(45,980),'Quruq kristall hosili eritmadagi mol emas',23,G);save(im,'faza')
im,d=canvas('Neytrallanish hisobining nazorati',1100)
for i,(a,b) in enumerate([('1. Nishon reaksiya','Qaysi proton, qaysi faza?'),('2. Stexiometriya','n/ν va qolgan reagent'),('3. Muvozanat','Suv, kuchsiz ionlar, yon jarayonlar'),('4. Yakuniy tarkib','Hajm, pH, tuzning formal miqdori'),('5. Tekshiruv','Atom, zaryad, massa, nazariy hosil')]):box(d,130+i*185,a,b)
save(im,'nazorat')
render('gidroksoniy_model','H₃O⁺: suvli proton belgisi',[('O',370,290),('H',230,350),('H',510,350),('H',370,455)],[(0,1),(0,2),(0,3)])
render('fosfat_model','HPO₄²⁻: formal ikkinchi bosqich',[('P',370,285),('O',370,130),('O',195,315),('O',545,315),('O',370,440),('H',150,410)],[(0,1),(0,2),(0,3),(0,4),(2,5)])
render('ammoniy_model','NH₄⁺: proton qabul qilgan NH₃',[('N',370,315),('H',370,135),('H',200,350),('H',540,350),('H',370,480)],[(0,1),(0,2),(0,3),(0,4)])
im,d=canvas('NaCl: panjaraning cheklangan bo‘lagi',850)
positions={}
for k in range(2):
 for j in range(3):
  for i in range(3):positions[i,j,k]=(170+150*i+55*k,240+135*j-45*k)
for (i,j,k),pos in positions.items():
 for v in [(i+1,j,k),(i,j+1,k),(i,j,k+1)]:
  if v in positions:line(d,pos,positions[v],'#A6B2BF',5)
for (i,j,k),(x,y) in sorted(positions.items(),key=lambda pair:pair[1][1]):
 is_na=(i+j+k)%2==0;sphere(d,x,y,30 if is_na else 37,(80,125,195) if is_na else (65,165,115),'Na' if is_na else 'Cl')
text(d,(35,680),'Ranglar shartli; ionlar 1:1 nisbatda',25,G)
text(d,(35,745),'Chiziqlar — yaqin qo‘shnichilik aloqasi',24,G)
text(d,(35,795),'Alohida NaCl molekulalari emas',25,G);save(im,'panjara_model')
print('5 schemes, 4 model graphs, 4 structural images and 4 CSV:',OUT)
