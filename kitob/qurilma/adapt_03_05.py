from pathlib import Path
s=Path(__file__).with_name('build_03_04_sidebar.py').read_text().replace('03_04','03_05').replace('3.4','3.5').replace('Titrlash-va-indikatorlar','Buferlar-va-gidroliz').replace('Titrlash va indikatorlar','Buferlar va gidroliz').replace('TITRLASH VA INDIKATORLAR','BUFERLAR VA GIDROLIZ').replace('titrlash','bufer_gidroliz')
a=s.index('    special=');b=s.index('\npanels=[',a)
s=s[:a]+'''    special={1:'mexanizm.png',2:'nisbat.png',3:'qoshish.png',4:'sigim.png',5:'suyultirish.png',6:'anion.png',7:'kation.png',8:'ikkala.png',9:'nazorat.png'}
    return ROOT/'rasmlar'/'bufer_gidroliz'/special[index]
'''+s[b:]
a=s.index('panels=[');b=s.index('\n\ndoc=Document()',a)
s=s[:a]+'''panels=[
('Juftlikning javobi',[],'3.5.1-sxema. Kuchli kislota/asos qo‘shilganda tutash shakllarning o‘zaro aylanishi.'),
('Qaysi nisbat ishlatildi?',[],'3.5.1-grafik. Shartli HA ning to‘liq balansi va analitik miqdorlar taqribi; C_T=0,1000 mol L⁻¹.'),
('Zaxira cheklangan',[],'3.5.2-grafik. Yakuniy C_T saqlangan ideal eritmalar qatori; q kuchli asos ekvivalentlarining konsentratsiyasi.'),
('Sig‘imning hissalari',[],'3.5.3-grafik. Ikki C_T uchun faqat HA/A⁻ juftligining β hissasi. Suv hadlari grafikda yo‘q.'),
('Suyultirish chegarasi',[],'3.5.4-grafik. Teng analitik HA/NaA: pH o‘zgarmas taqrib va to‘liq suvli muvozanat.'),
('Anionning proton olishi',[],'3.5.2-sxema. Elektrolitik dissotsiatsiya va gidrolizni ajratish; muvozanatni balanslar bilan yopish.'),
('Kation kislotaligi',[],'3.5.3-sxema. Ammoniydagi va metall akvakompleksidagi proton donorni ajratish.'),
('Ikki ion va suv',[],'3.5.5-grafik. NH₄F ning ideal pH i: to‘liq balans va suvni tashlagan taqrib. 25 °C, γ≈1.'),
('Modelni qayta tiklang',[],'3.5.4-sxema. Bufer va gidroliz uchun bir xil oilalar/balanslar usulini qo‘llash.')
]'''+s[b:]
s=s.replace("variables={\n","variables={\n'β_juft,max':('β','juft,max'),'β_juft':('β','juft'),'β_suv':('β','suv'),'γ_h':('γ','h'),'n_tuz':('n','tuz'),'n_kislota':('n','kislota'),'Kₐ,j+1':('K','a,j+1'),'Kₐ,j':('K','a,j'),\n")
a=s.index('    extra_models=');b=s.index('\n    if idx in extra_models:',a)
s=s[:a]+'''    extra_models={0:('h2po4_model.png','3.5.1-rasm. H₂PO₄⁻ dagi ikki O–H ulanishi.'),1:('hpo4_model.png','3.5.2-rasm. HPO₄²⁻ dagi bitta O–H ulanishi.'),6:('akva_model.png','3.5.3-rasm. [Al(H₂O)₆]³⁺: olti suv ligandining sxematik proyeksiyasi.'),7:('nh4_model.png','3.5.4-rasm. NH₄⁺ ionining ulanishga yo‘naltirilgan shar–tayoqcha tasviri.')}'''+s[b:]
a=s.index('        refs=[');b=s.index('\n        for ref in refs:',a)
s=s[:a]+'''        refs=[
        '[1] OpenStax. Chemistry 2e. 14.6: Buffers. https://openstax.org/books/chemistry-2e/pages/14-6-buffers . Buferning ta’siri, tarkib nisbatlari va cheklangan zaxira. Mustaqil o‘zbekcha bayon.',
        '[2] OpenStax. Chemistry 2e. 14.4: Hydrolysis of Salts. https://openstax.org/books/chemistry-2e/pages/14-4-hydrolysis-of-salts . Anion/kation gidrolizi, NH₄⁺, amfiprot ionlar va metall akvakomplekslari.',
        '[3] OpenStax. Chemistry 2e. Appendix H: Ionization Constants of Weak Acids. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . HF va fosfat uchun 25 °C dagi konstantalar.',
        '[4] Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11-nashr. Oxford University Press, 2018. Faollik va kimyoviy muvozanatga bibliografik tayanch.',
        'Barcha grafiklar original ideal konsentratsion hisoblar; tajriba emas. Tuzilishlar sxematik ulanish tasvirlari, optimallashtirilgan koordinatalar yoki elektron zichlik emas. Shartli HA K_c=10⁻⁵ qiymati HF ga tegishli emas.'
        ]'''+s[b:]
s=s.replace('assert counter==8','assert counter==9').replace('4 apparatus/structural images; 8 equations','4 structural images; 9 equations')
Path(__file__).with_name('build_03_05_sidebar.py').write_text(s)
