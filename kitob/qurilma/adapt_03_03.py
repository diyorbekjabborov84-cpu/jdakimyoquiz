from pathlib import Path
p=Path(__file__).with_name('build_03_02_sidebar.py').read_text()
p=p.replace('3.2','3.3').replace('03_02','03_03').replace('Kuchga-tasir-etuvchi-omillar','Dissotsiatsiya-va-pH').replace('Kuchga ta’sir etuvchi omillar','Dissotsiatsiya va pH').replace('KUCHGA TA’SIR ETUVCHI OMILLAR','DISSOTSIATSIYA VA pH').replace('kuch_omillari','dissotsiatsiya_ph')
a=p.index('    special=');b=p.index('    if index in special:',a)
p=p[:a]+"    special={1:'shkala.png',2:'balans.png',3:'kuchli.png',4:'kuchsiz.png',5:'miqdor.png',6:'umumiy_ion.png',7:'sulfat.png',8:'faollik.png',9:'nazorat.png'}\n"+p[b:]
a=p.index('panels=[');b=p.index('\n\ndoc=Document()',a)
p=p[:a]+'''panels=[
('Logarifm va faollik',[],'3.3.1-sxema. Faolliklar nisbati: bir pH birligi — o‘n karra farq.'),
('Balanslar bir tizim',[],'3.3.2-sxema. Faqat HA va suv uchun konsentratsion ideal tenglamalar.'),
('Suv chegarasiga yaqin',[],'3.3.1-grafik. Kuchli bir asosli kislota: suvli yechim va suvni tashlagan ifoda; 25 °C.'),
('Bir xil C, turli ajralish',[],'3.3.2-grafik. Shartli HA va to‘liq ajralgan HX; ikkala ideal model suvni saqlaydi.'),
('Miqdor va yakuniy hajm',[],'3.3.3-sxema. Ikki kuchli bir asosli kislota aralashmasining hisob yo‘li.'),
('Umumiy H⁺ ta’siri',[],'3.3.3-grafik. Kuchli kislota C_s ortganda shartli HA ning deprotonlangan ulushi.'),
('Ikkinchi proton',[],'3.3.4-grafik. H₂SO₄ ning birinchi bosqichi to‘liq deb olingan ideal model. K₂,c≈0,012 mol L⁻¹; 25 °C.'),
('Faollikni ajrating',[],'3.3.4-sxema. Shartli molal misol: γ koeffitsiyentining pH ga hissasi.'),
('Yechimning nazorati',[],'3.3.5-sxema. Tarkibdan fizik ildiz va balanslarni qayta tekshirishga o‘tish.')
]'''+p[b:]
a=p.index('sub=dict(');b=p.index('\ndef shade(',a)
p=p[:a]+'''sub=dict(zip('₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ','0123456789abmj'));sup=dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻','0123456789+−'))
variables={'K_w,c':('K','w,c'),'K_w':('K','w'),'K_c':('K','c'),'K₂,c':('K','2,c'),'C_s':('C','s'),'V_yakun':('V','yakun'),'pH_neytral':('pH','neytral')}
def runs(p,text,size=11,bold=False,color=INK):
    pattern='('+'|'.join(re.escape(v) for v in variables)+r'|[₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ]+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)'
    def put(t,lower=False,upper=False):
        r=p.add_run(t);r.font.name='Times New Roman';r.font.size=Pt(size);r.bold=bold;r.font.color.rgb=RGBColor.from_string(color)
        if lower:r.font.subscript=True
        if upper:r.font.superscript=True
    for token in re.split(pattern,text):
        if not token:continue
        if token in variables:
            main,low=variables[token];put(main);put(low,lower=True)
        elif all(c in sub for c in token):put(''.join(sub[c] for c in token),lower=True)
        elif all(c in sup for c in token):put(''.join(sup[c] for c in token),upper=True)
        else:put(token)
'''+p[b:]
p=p.replace('idx in [5,7]','idx in [2,3,5,6]')
a=p.index('    extra_models=');b=p.index('\n    if idx in extra_models:',a)
p=p[:a]+'''    extra_models={1:('gidroksoniy_model.png','3.3.1-rasm. H₃O⁺ ionining shar–tayoqcha tasviri.'),2:('hcl_model.png','3.3.2-rasm. Neytral HCl; suvdagi asosiy zarracha deb talqin qilinmaydi.'),3:('hf_model.png','3.3.3-rasm. HF tuzilishi; grafikdagi shartli HA bilan aynanlashtirilmaydi.'),6:('sulfat_model.png','3.3.4-rasm. H₂SO₄ molekulasidagi ikki O–H ulanishi.')}'''+p[b:]
a=p.index('        refs=[');b=p.index('\n        for ref in refs:',a)
p=p[:a]+'''        refs=[
        '[1] IUPAC Gold Book. pH. DOI: 10.1351/goldbook.P04524. https://goldbook.iupac.org/terms/view/P04524 . Molal faollik ta’rifi va yakka ion konvensiyasi; mazmun mustaqil o‘zbekcha bayon qilindi.',
        '[2] Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11-nashr. Oxford University Press, 2018. Kimyoviy muvozanat, faollik va elektrokimyo asoslari.',
        '[3] OpenStax. Chemistry 2e. Appendix H: Ionization Constants of Weak Acids. https://openstax.org/books/chemistry-2e/pages/h-ionization-constants-of-weak-acids . HSO₄⁻ uchun 25 °C dagi Kₐ₂=1,2×10⁻² qiymati.',
        'Barcha grafiklar ideal konsentratsion modellar; tajriba natijalari emas. Tuzilish tasvirlari original sxematik o‘quv modellari, optimallashtirilgan koordinatalar emas. K_c=10⁻⁵ shartli HA uchun, HF uchun emas.'
        ]'''+p[b:]
p=p.replace('assert counter==8','assert counter==9').replace('7 schemes; 2 illustrative graphs; 4 molecular renders; 8 equations','5 schemes; 4 calculated graphs; 4 molecular renders; 9 equations')
Path(__file__).with_name('build_03_03_sidebar.py').write_text(p)
