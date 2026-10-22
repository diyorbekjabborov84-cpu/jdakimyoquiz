from pathlib import Path
s=Path(__file__).with_name('build_03_05_sidebar.py').read_text().replace('03_05','03_06').replace('3.5','3.6').replace('Buferlar-va-gidroliz','Kinetika-va-kataliz').replace('Buferlar va gidroliz','Kinetika va kataliz').replace('BUFERLAR VA GIDROLIZ','KINETIKA VA KATALIZ').replace('bufer_gidroliz','kinetika_kataliz')
a=s.index('    special=');b=s.index('\npanels=[',a)
s=s[:a]+'''    special={1:'muvozanat.png',2:'tezlik.png',3:'energiya.png',4:'harorat.png',5:'ph_tezlik.png',6:'bufer.png',7:'sikl.png',8:'noorganik.png',9:'nazorat.png'}
    return ROOT/'rasmlar'/'kinetika_kataliz'/special[index]
'''+s[b:]
a=s.index('panels=[');b=s.index('\n\ndoc=Document()',a)
s=s[:a]+'''panels=[
('Bir xil oxirgi holat',[],'3.6.1-grafik. Qaytar S⇌P modelida ikkala tezlik konstantasini 10 marta oshirish. K=4 saqlanadi.'),
('Tenglama va kuzatuv',[],'3.6.1-sxema. Signal, tezlik qonuni, tajribaviy tartiblar va psevdotartib shartlari.'),
('To‘siq va ΔG°',[],'3.6.2-grafik. Mustaqil shartli erkin energiya profillari. Boshlanish va oxir bir xil; 1-bo‘lim K=4 modeli emas.'),
('Haroratning hissasi',[],'3.6.3-grafik. E_a=50,0 kJ mol⁻¹ uchun shartli Arrhenius modeli; o‘lchangan qiymatlar emas.'),
('Maxsus kanallar',[],'3.6.4-grafik. Shartli H⁺/OH⁻ va fon yo‘llarining jami. Ideal konsentratsion pH; 25 °C.'),
('Buferning kinetik roli',[],'3.6.5-grafik. Bir xil pH=5 da oldindan berilgan umumiy HA kanali. k_A=0 — model farazi.'),
('Protonning aylanishi',[],'3.6.2-sxema. Formal qaytar protonlanish–qayta tuzilish–deprotonlanish sikli.'),
('Redoks vositachilik',[],'3.6.3-sxema. NO/NO₂ ning muvozanatlangan formal sikli; elementar yoki to‘liq sanoat mexanizmi emas.'),
('Dalillarni birlashtiring',[],'3.6.4-sxema. Kinetik modelni dalil, nazorat va muqobil yo‘llar bilan tekshirish.')
]'''+s[b:]
s=s.replace("sup=dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻','0123456789+−'))","sup=dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡','0123456789+−mn‡'))")
s=s.replace("r'|[₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ]+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)'","r'|[₀₁₂₃₄₅₆₇₈₉ₐᵦₘⱼ]+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡]+)'")
a=s.index('variables={');b=s.index('\ndef runs(',a)
s=s[:a]+'''variables={
'k_maxsus':('k','maxsus'),'k_obs':('k','obs'),'k_HA':('k','HA'),'k_OH':('k','OH'),
'k_H':('k','H'),'k_A':('k','A'),'k_f':('k','f'),'k_r':('k','r'),'k_B':('k','B'),'k_ref':('k','ref'),
'h_P':('h','P'),'K_p':('K','p'),'E_a':('E','a'),'C_T':('C','T'),'α_Br':('α','Br'),
'[S]_t':('[S]','t'),'[S]_0':('[S]','0'),'t_1/2':('t','1/2'),
'K_w,c':('K','w,c'),'K_c':('K','c'),'K_w':('K','w')}
'''+s[b:]
s=s.replace('idx in [1,2,3,4,7]','idx in [0,2,3,4,5]')
a=s.index('    extra_models=');b=s.index('\n    if idx in extra_models:',a)
s=s[:a]+'''    extra_models={4:('gidroksoniy_model.png','3.6.1-rasm. H₃O⁺ — suvli proton tashuvchisi.'),5:('fosfat_model.png','3.6.2-rasm. H₂PO₄⁻ — proton donorining ulanish misoli. Grafikdagi pKₐ=5 shu ionniki emas.'),6:('ammiak_model.png','3.6.3-rasm. NH₃ — proton akseptorining ulanish misoli.'),7:('no2_model.png','3.6.4-rasm. Neytral NO₂ radikalining ulanish tasviri; to‘liq Lewis modeli emas.')}'''+s[b:]
a=s.index('        refs=[');b=s.index('\n        for ref in refs:',a)
s=s[:a]+'''        refs=[
        '[1] IUPAC Gold Book. Catalyst. DOI: 10.1351/goldbook.C00876. https://goldbook.iupac.org/terms/view/C00876 . Katalizator, umumiy ΔG° va qayta hosil bo‘lish tushunchalari.',
        '[2] IUPAC Gold Book. Specific acid–base catalysis. DOI: 10.1351/goldbook.S05789. https://goldbook.iupac.org/terms/view/S05789 . Erituvchi ionlariga tegishli kuzatiladigan kataliz.',
        '[3] IUPAC Gold Book. General acid catalysis. DOI: 10.1351/goldbook.G02609. https://goldbook.iupac.org/terms/view/G02609 . Katalitik koeffitsiyentlar va bufer konsentratsiyasini o‘zgartirish mezoni.',
        '[4] IUPAC Gold Book. Gibbs energy of activation. DOI: 10.1351/goldbook.G02631. https://goldbook.iupac.org/terms/view/G02631 . To‘siq, tezlik konstantasi birliklari va standart holat.',
        '[5] Atkins, P.; de Paula, J.; Keeler, J. Atkins’ Physical Chemistry. 11-nashr. Oxford University Press, 2018. Kimyoviy kinetika va o‘tish holati nazariyasi.',
        '[6] Housecroft, C. E.; Sharpe, A. G. Inorganic Chemistry. 5-nashr. Pearson, 2018. Noorganik kataliz, koordinatsiya va sanoat kimyosiga umumiy bibliografik tayanch.',
        'IUPAC atamalari mazmuni mustaqil o‘zbekcha bayon qilindi. Barcha grafiklar original shartli modellar; real kislota/katalizator uchun tajribaviy ma’lumotlar emas. Molekulalar sxematik ulanish tasvirlari; optimallashtirilgan koordinatalar yoki elektron zichlik emas.'
        ]'''+s[b:]
s=s.replace('assert counter==9','assert counter==8').replace('4 structural images; 9 equations','4 molecular images; 8 equations')
Path(__file__).with_name('build_03_06_sidebar.py').write_text(s)
