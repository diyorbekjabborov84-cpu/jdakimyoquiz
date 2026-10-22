from pathlib import Path
s=Path(__file__).with_name('build_03_03_sidebar.py').read_text().replace('03_03','03_04').replace('3.3','3.4').replace('Dissotsiatsiya-va-pH','Titrlash-va-indikatorlar').replace('Dissotsiatsiya va pH','Titrlash va indikatorlar').replace('DISSOTSIATSIYA VA pH','TITRLASH VA INDIKATORLAR').replace('dissotsiatsiya_ph','titrlash')
a=s.index('def scheme(');b=s.index('\npanels=[',a)
s=s[:a]+'''def scheme(index,nodes):
    special={1:'nuqtalar.png',2:'kuchli.png',3:'kuchsiz.png',4:'fosfat.png',5:'indikator.png',6:'intervallar.png',7:'xato.png',8:'hosila.png',9:'nazorat.png'}
    return ROOT/'rasmlar'/'titrlash'/special[index]
'''+s[b:]
a=s.index('panels=[');b=s.index('\n\ndoc=Document()',a)
s=s[:a]+'''panels=[
('Ikki xil nuqta',[],'3.4.1-sxema. Nazariy stexiometriya va kuzatilgan oxirgi nuqtani ajratish.'),
('Kuchli juftlik',[],'3.4.1-grafik. Kuchli bir asosli kislota–NaOH. Bronza chiziq: 25,00 mL ekvivalent hajm.'),
('Kuchsiz kislota',[],'3.4.2-grafik. Shartli HA–NaOH. K_c=10⁻⁵ mol L⁻¹; suv va barcha muvozanat hissalari saqlangan.'),
('Ko‘p bosqichli egri chiziq',[],'3.4.3-grafik. Ideal H₃PO₄–NaOH. Bronza chiziqlar uchta stexiometrik hajm, uchta teng keskin sakrash emas.'),
('Indikator ulushlari',[],'3.4.4-grafik. pK_In=7 bo‘lgan shartli ikki shaklli model; real spektr yoki nitrofenol o‘lchovi emas.'),
('Rang o‘tish intervali',[],'3.4.2-sxema. Uch indikatorning odatiy intervallari [2]. Chiziqlar rang intensivligi o‘lchovi emas.'),
('Hajmdagi og‘ish',[],'3.4.3-sxema. Oxirgi nuqta siljishi va hisoblangan kislota miqdorining ishorali og‘ishi.'),
('Sonli hosila',[],'3.4.5-grafik. Kuchli juftlikning ideal modelidan hisoblangan hosila; haqiqiy asbob signali emas.'),
('Natijaning zanjiri',[],'3.4.4-sxema. Reaksiya, standartlash, signal, tuzatish va noaniqlikni birga nazorat qilish.')
]'''+s[b:]
a=s.index('variables={');b=s.index('\ndef runs(',a)
s=s[:a]+'''variables={
'K_w,c':('K','w,c'),'K_b,c':('K','b,c'),'K_w':('K','w'),'K_c':('K','c'),'K₂,c':('K','2,c'),
'C_s':('C','s'),'C_a':('C','a'),'C_b':('C','b'),'C_T':('C','T'),
'V_yakun':('V','yakun'),'V_oxir':('V','oxir'),'V_e':('V','e'),'V_a':('V','a'),'V_b':('V','b'),
'pH_neytral':('pH','neytral'),'pK_In':('pK','In'),'ε_V':('ε','V'),
'pH_(i+1)':('pH','i+1'),'pH_(i−1)':('pH','i−1'),'V_(i+1)':('V','i+1'),'V_(i−1)':('V','i−1'),
'(dpH/dV)_i':('(dpH/dV)','i')}
'''+s[b:]
s=s.replace('idx in [2,3,5,6]','idx in [1,2,3,4,7]')
a=s.index('    extra_models=');b=s.index('\n    if idx in extra_models:',a)
s=s[:a]+'''    extra_models={0:('qurilma.png','3.4.1-rasm. Byuretka–kolba qurilmasining original sxematik tasviri.'),3:('fosfat_model.png','3.4.2-rasm. H₃PO₄ da uch O–H ulanishi.'),4:('hin_tuzilish.png','3.4.3-rasm. para-Nitrofenol ulanish modeli.'),5:('in_tuzilish.png','3.4.4-rasm. para-Nitrofenolyat ulanish modeli. Nitro guruhining bitta rezonans yozuvi.')}'''+s[b:]
a=s.index('        refs=[');b=s.index('\n        for ref in refs:',a)
s=s[:a]+'''        refs=[
        '[1] OpenStax. Chemistry 2e. 14.7: Acid-Base Titrations. https://openstax.org/books/chemistry-2e/pages/14-7-acid-base-titrations . Egri chiziqlar, indikatorning ikki shaklli modeli va o‘tish intervali nazariyasi.',
        '[2] Harvey, D. Analytical Chemistry 2.1. Chapter 9: Titrimetric Methods. https://www.asdlib.org/onlineArticles/ecourseware/Text_Files_files/Chapter9.pdf . Indikator tanlash, hajm og‘ishi, instrumental aniqlash; jadvaldagi odatiy indikator intervallari.',
        '[3] OpenStax. Chemistry 2e. Appendix H: Ionization Constants of Weak Acids. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . H₃PO₄ uchun 25 °C dagi konstantalar.',
        'Barcha tasvirlar original o‘quv ishlanmalari. Grafiklar ideal konsentratsion muvozanat hisoblari; tajriba emas. Strukturaviy tasvirlar optimallashtirilgan koordinatalar emas. NitrofenoI tasvirlari shartli indikator grafigining moddasini belgilamaydi.'
        ]'''+s[b:]
s=s.replace('assert counter==9','assert counter==8').replace('5 schemes; 4 calculated graphs; 4 molecular renders; 9 equations','4 schemes; 5 calculated graphs; 4 apparatus/structural images; 8 equations')
Path(__file__).with_name('build_03_04_sidebar.py').write_text(s)
