from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
root=Path(__file__).resolve().parents[1]
im=Image.new('RGB',(1800,1120),'white'); d=ImageDraw.Draw(im)
f='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
font=lambda n:ImageFont.truetype(f,n)
d.text((90,40),'Kislota tushunchasining rivojlanishi',font=font(48),fill='#0B2C4A')
items=[('XVII asr','Boyl: kuzatiladigan xossalar va indikatorlar'),('XVIII asr oxiri','Lavuazye: kislorodga asoslangan talqin'),('XIX asr boshi','Devi: kislorodsiz kislotalar mavjudligi'),('1884','Arrhenius: suvdagi ionlar'),('1923','Brønsted–Lowry: proton almashinuvi'),('1923','Lewis: elektron jufti almashinuvi')]
d.line((140,165,140,975),fill='#C28E3B',width=8)
for i,(a,b) in enumerate(items):
 y=160+i*154
 d.ellipse((123,y,157,y+34),fill='#0B2C4A')
 d.text((200,y-8),a,font=font(33),fill='#0B2C4A')
 d.text((200,y+42),b,font=font(34),fill='#222222')
d.text((90,1050),'Sxematik ketma-ketlik; vaqt oraliqlari masshtabda berilmagan.',font=font(25),fill='#555555')
im.save(root/'rasmlar'/'01_timeline_uz.png')
