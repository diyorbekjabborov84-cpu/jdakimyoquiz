from pathlib import Path
import re
s=Path(__file__).with_name('build_03_06_sidebar.py').read_text().replace('03_06','04_01')
s=re.sub(r'(?<!\d)3\.6', '4.1',s)
s=s.replace('Kinetika-va-kataliz','Neytrallanish-va-tuz-hosil-bolishi').replace('Kinetika va kataliz','Neytrallanish va tuz hosil bo‘lishi').replace('KINETIKA VA KATALIZ','NEYTRALLANISH VA TUZ HOSIL BO‘LISHI').replace('kinetika_kataliz','neytrallanish')
s=s.replace('3-BOB','4-BOB').replace('KISLOTALILIK KUCHI VA MUVOZANATLAR','UMUMIY KIMYOVIY XOSSALAR').replace('13.6','13.5')
a=s.index('    special=');b=s.index('\npanels=[',a)
s=s[:a]+'''    special={1:'ionli.png',2:'yonalish.png',3:'ekvivalent.png',4:'fosfat.png',5:'tuz_ph.png',6:'issiqlik.png',7:'yollar.png',8:'faza.png',9:'nazorat.png'}
    return ROOT/'rasmlar'/'neytrallanish'/special[index]
'''+s[b:]
a=s.index('panels=[');b=s.index('\n\ndoc=Document()',a)
s=s[:a]+'''panels=[
('Ion jarayonining markazi',[],'4.1.1-sxema. Molekulyar, ionli va qisqartirilgan yozuvlarning turli vazifalari.'),
('Yo‘nalish va to‘liqlik',[],'4.1.1-grafik. Teng boshlang‘ich HA va B uchun ideal o‘zgarish ulushi; suv va yon muvozanatlar tashlangan.'),
('Nishon proton bosqichi',[],'4.1.2-sxema. Bir mol kislota uchun OH⁻ ekvivalentlari tanlangan nishonga bog‘liq.'),
('Formal formula va turlar',[],'4.1.2-grafik. Yakuniy C_P=0,0100 M saqlangan fosfat eritmalari qatori; suv va barcha shakllar hisoblangan.'),
('Mahsulotning pH i',[],'4.1.3-grafik. Tuzlarning 25 °C dagi ideal pH qiyosi. NaA va BH⁺A⁻ shartli hisoblar.'),
('Entalpiya va issiqlik',[],'4.1.4-grafik. Shartli −57 va −42 kJ mol⁻¹ uchun ajralgan issiqlik. Real kislota o‘lchovi yoki universal konstanta emas.'),
('Turli tuz hosil bo‘lishlar',[],'4.1.3-sxema. Gidroksid, ammiak, qattiq oksid va gidrokarbonat ishtirokidagi yo‘llar.'),
('Qaysi faza tasvirlangan?',[],'4.1.4-sxema. Tuz formulasi, kristall va suvli eritmadagi ionlarni ajratish.'),
('Hisobni qayta tekshiring',[],'4.1.5-sxema. Stexiometriyadan muvozanat tarkibi va nazariy hosilga o‘tish.')
]'''+s[b:]
a=s.index('variables={');b=s.index('\ndef runs(',a)
s=s[:a]+'''variables={
'ξ_max':('ξ','max'),'n_i,0':('n','i,0'),'n_i':('n','i'),'ν_i':('ν','i'),
'n_kislota':('n','kislota'),'n_asos':('n','asos'),'V_yakun':('V','yakun'),
'ΔH_neut':('ΔH','neut'),'ΔH_diss':('ΔH','diss'),'q_rxn':('q','rxn'),'q_abs':('q','abs'),
'C_cal':('C','cal'),'c_p':('c','p'),'C_P':('C','P'),
'K₁,c':('K','1,c'),'K₂,c':('K','2,c'),'K₃,c':('K','3,c'),
'K_w,c':('K','w,c'),'K_c':('K','c'),'K_w':('K','w')}
'''+s[b:]
s=s.replace('idx in [0,2,3,4,5]','idx in [1,3,4,5]')
a=s.index('    extra_models=');b=s.index('\n    if idx in extra_models:',a)
s=s[:a]+'''    extra_models={0:('gidroksoniy_model.png','4.1.1-rasm. H₃O⁺ — suvdagi proton tashuvchisi.'),3:('fosfat_model.png','4.1.2-rasm. HPO₄²⁻: ikkinchi formal bosqichdagi ionning ulanish tasviri.'),6:('ammoniy_model.png','4.1.3-rasm. NH₄⁺: NH₃ ning proton olgan tutash shakli.'),7:('panjara_model.png','4.1.4-rasm. NaCl panjarasining cheklangan bo‘lagi; ranglar shartli, chiziqlar qo‘shnichilikni ko‘rsatadi.')}'''+s[b:]
a=s.index('        refs=[');b=s.index('\n        for ref in refs:',a)
s=s[:a]+'''        refs=[
        '[1] OpenStax. Chemistry 2e. 4.2: Classifying Chemical Reactions. https://openstax.org/books/chemistry-2e/pages/4-2-classifying-chemical-reactions . Kislota–asos jarayoni va ionli tenglamalar; matn mustaqil bayon qilindi.',
        '[2] OpenStax. Chemistry 2e. 14.4: Hydrolysis of Salts. https://openstax.org/books/chemistry-2e/pages/14-4-hydrolysis-of-salts . Tuz ionlarining kislota–asos xossalari va NH₄⁺ konstantasi.',
        '[3] Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11-nashr. Oxford University Press, 2018. Proton almashinuvi termodinamikasi, Hess qonuni va kalorimetriyaga umumiy bibliografik tayanch.',
        '[4] OpenStax. Chemistry 2e. Appendix H: Ionization Constants of Weak Acids. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . Fosfat konstantalari; 25 °C.',
        '[5] IUPAC Gold Book. Salt. DOI: 10.1351/goldbook.S05447. https://goldbook.iupac.org/terms/view/S05447 . Kation va anionlardan tuzilgan birikma tushunchasi.',
        'Barcha tasvirlar original o‘quv ishlanmalari; grafiklar tajriba emas. Tuzilishlar sxematik, optimallashtirilgan koordinatalar emas. −57/−42 kJ mol⁻¹ qiymatlari shartli issiqlik taxminiy hisoblari; HF yoki universal neytrallanish entalpiyasiga biriktirilmagan.'
        ]'''+s[b:]
s=s.replace('4 schemes; 5 calculated graphs','5 schemes; 4 calculated graphs')
Path(__file__).with_name('build_04_01_sidebar.py').write_text(s)
