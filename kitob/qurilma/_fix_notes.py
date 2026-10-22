from pathlib import Path
p=Path(__file__).resolve().parent/'content_04_04.py'
lines=p.read_text().split('\n')
start=next(i for i,l in enumerate(lines) if l.startswith('notes=['))
end=next(i for i,l in enumerate(lines[start:],start) if l.startswith("(R/'04_04_yonlavhalar.json')"))
notes=[
 ('Analitik miqdor','Eritilgan metallning umumiy miqdori erkin ion miqdoriga teng emas.'),
 ('Suvli qobiq','“Erkin ion” suvli koordinatsion qobiq bilan ham bog‘liq.'),
 ('Faollik bilan ishlash','a_i=γ_i c_i/c°; γ_i≈1 faqat ideal yaqinlashuvda.'),
 ('Sig‘im chegarasi','Hisoblangan to‘yinganlik sig‘imi mavjud moddadan katta bo‘lishi mumkin.'),
 ('β_2 ≠ K_2','Umumiy konstanta K_1·K_2 ko‘paytmasidir; bosqichli konstanta bilan chalkashtirilmaydi.'),
 ('K_d faqat teskari yo‘nalish','Konstanta teskari reaksiyaga tegishli bo‘lsa qo‘llanadi.'),
 ('α_L²','Ikki ligandli kompleksda pH ta’siri kvadrat bilan kuchayadi.'),
 ('Proton rezervuari','pH berilgan bo‘lsa, yetarli proton manbai yoki bufer nazarda tutiladi.'),
 ('Anion — kuzatuvchi emas','Perklorat va nitrat ko‘p tizimda faol emas, lekin har doim ham emas.'),
 ('Kislota bilan kuchayish','Ba’zi anionlar kislotada protonlanib kuchsizlashadi, ba’zilari kuchaydi.'),
 ('Erish — natija emas','Komplekslanish erkin ionni kamaytiradi, umumiy eruvchanlikni oshiradi.'),
 ('Miqdoriy chegara','Katta β ham barcha cho‘kmani eritishga yetarli emas.'),
 ('Selektivlik masalasi','Ikkita K_sp ni solishtirish selektiv ajratishni hal qilmaydi.'),
 ('Maskalash','Kerakli metallni vaqtincha kompleksga bog‘lash usuli.'),
 ('Amfoterlik redoks emas','Markaziy metallning oksidlanish darajasi o‘zgarmaydi.'),
 ('Model chegarasi','Xayoliy M(OH)₃/[M(OH)₄]⁻ tizimi haqiqiy Al uchun universal diagramma emas.'),
 ('Ikkita qarama-qarshi ta’sir','Protonlanish eruvchanlikni oshiradi, cho‘ktiruvchi anion kuchaytiradi.'),
 ('Stokhiometriya','1:1 va 2:2 tuzlar uchun eruvchanlik formulasi turlicha.'),
 ('Yaxlitlash xatosi','Ligand sarflanishini e’tiborsiz qoldirish 8,84% ga chiqdi.'),
 ('Balans birga','Protonlanish, ligand sarfi va faza miqdori birga tekshiriladi.'),
 ('Model chegarasi','Erish modeli faqat Ag(NH₃)₂⁺ turini hisobga oladi; boshqa turlar chetga chiqariladi.'),
 ('Xulosa','Komplekslanish erkin ionni kamaytiradi, umumiy eruvchanlikni oshiradi.')]
assert len(notes)==22
block=['notes=[']
for i in range(0,22,2):
    block.append(' ['+repr(list(notes[i]))+',')
    block.append('  '+repr(list(notes[i+1]))+'],')
block[-1]=block[-1][:-1]+']'
lines=lines[:start]+block+lines[end:]
p.write_text('\n'.join(lines))
print('notes block rewritten')
