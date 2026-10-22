"""Native editable Word equations (OMML), not flattened slash notation or images.
Explicit formula trees keep numerator/denominator and scripts semantically grouped.
"""
from copy import deepcopy
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
import re

def el(tag,*children):
    x=OxmlElement('m:'+tag)
    for c in children:
        for item in (c if isinstance(c,list) else [c]):x.append(deepcopy(item))
    return x

EQ_SIZE = 22
EQ_GAP = 7
EQ_LEAD = 1.15

def text(s):
    r=el('r');pr=el('rPr');sty=el('sty');sty.set(qn('m:val'),'p');pr.append(sty);r.append(pr)
    wp=OxmlElement('w:rPr');fo=OxmlElement('w:rFonts')
    for a in ['ascii','hAnsi']:fo.set(qn('w:'+a),'Cambria Math')
    wp.append(fo);size=OxmlElement('w:sz');size.set(qn('w:val'),str(EQ_SIZE));wp.append(size);r.append(wp)
    t=el('t');t.set(qn('xml:space'),'preserve');t.text=s;r.append(t);return r

def seq(*xs):
    out=[]
    for x in xs:out.extend(x if isinstance(x,list) else [text(x) if isinstance(x,str) else x])
    return out

def sub(base,script):return el('sSub',el('e',seq(base)),el('sub',seq(script)))
def sup(base,script):return el('sSup',el('e',seq(base)),el('sup',seq(script)))
def frac(a,b):return el('f',el('num',seq(a)),el('den',seq(b)))
def par(a):return seq('(',a,')')
def var(a,b):return sub(a,b)
SUB=str.maketrans('₀₁₂₃₄₅₆₇₈₉ₐ','0123456789a')
SUP=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡','0123456789+−mn‡')
def chem(s):
    result=[]
    for t in re.findall(r'[₀₁₂₃₄₅₆₇₈₉ₐ]+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡]+|[^₀₁₂₃₄₅₆₇₈₉ₐ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡]+',s):
        if t[0] in '₀₁₂₃₄₅₆₇₈₉ₐ':result.append(sub(result.pop(),t.translate(SUB)))
        elif t[0] in '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵐⁿ‡':result.append(sup(result.pop(),t.translate(SUP)))
        else:result.append(text(t))
    return result

def equations(topic):
    if topic=='5.2':
        from equations_05_02 import purification_equations
        return purification_equations()
    if topic=='5.1':
        from equations_05_01 import preparation_equations
        return preparation_equations()
    if topic=='4.5':
        from equations_04_05 import decomposition_equations
        return decomposition_equations()
    if topic=='4.4':
        from equations_04_04 import complex_equations
        return complex_equations()
    if topic=='4.3':
        from equations_04_03 import passive_equations
        return passive_equations()
    if topic=='4.2':
        from equations_04_02 import redox_equations
        return redox_equations()
    ko=var('k','obs');kw=var('K','w,c');cp=var('C','P');dh=var('ΔH','neut')
    if topic=='3.6':return [
      [seq(sup('ΔG','°'),' = −RT ln K')],
      [seq('v = k',sup('[S]','m'),sup(chem('[H⁺]'),'n'))],
      [seq('ln',par(frac(var('[S]','t'),var('[S]','0'))),' = −',ko,' t'),seq(var('t','1/2'),' = ',frac('ln 2',ko))],
      [seq('k = κ',frac(seq(var('k','B'),' T'),var('h','P')),' exp',par(frac(seq('−',sup('ΔG','‡')),'RT')))],
      [seq(frac('k(T)',seq('k(',var('T','0'),')')),' = exp',par(seq('−',frac(var('E','a'),'R'),par(seq(frac('1','T'),' − ',frac('1',var('T','0')))))))],
      [seq(ko,' = ',var('k','0'),' + ',var('k','H'),' h + ',var('k','OH'),' ',frac(kw,'h'))],
      [seq(ko,' = ',var('k','maxsus'),' + ',var('k','HA'),'[HA] + ',var('k','A'),chem('[A⁻]'))],
      [chem('S + H⁺ ⇌ SH⁺;   SH⁺ ⇌ PH⁺'),chem('PH⁺ ⇌ P + H⁺')]
    ]
    assert topic=='4.1'
    ka=lambda s:seq(var('K','a'),par(chem(s)))
    return [
      [chem('H₃O⁺(aq) + OH⁻(aq) → 2H₂O(l)')],
      [seq('lg K = p',ka('BH⁺'),' − p',ka('HA')),seq('K = ',frac(ka('HA'),ka('BH⁺')))],
      [seq(var('ξ','max'),' = min{',frac(var('n','i,0'),var('ν','i')),'}')],
      [seq(cp,' = ',chem('[H₃PO₄] + [H₂PO₄⁻]')),chem('       + [HPO₄²⁻] + [PO₄³⁻]')],
      [chem('A⁻ + H₂O ⇌ HA + OH⁻'),chem('BH⁺ + H₂O ⇌ B + H₃O⁺')],
      [seq('ΔH',par(chem('HA + OH⁻ → A⁻ + H₂O'))),seq('= ',var('ΔH','diss'),'(HA) + ΔH',par(chem('H⁺ + OH⁻ → H₂O')))],
      [seq('ΔT = ',frac(seq('−ξ',dh),seq('m',var('c','p'),' + ',var('C','cal'))))],
      [seq('D = ',frac(seq(var('n','kislota'),' − ',var('n','asos')),var('V','yakun'))),seq('h − ',frac(kw,'h'),' = D')]
    ]

def add_equation(p,cell,topic,number,runs):
    lines=equations(topic)[number-1]
    for i,line in enumerate(lines):
        if i:
            p=cell.add_paragraph();p.paragraph_format.space_before=Pt(1)
        p.paragraph_format.line_spacing=EQ_LEAD
        p.paragraph_format.space_after=Pt(EQ_GAP)
        p.paragraph_format.keep_together=True
        p.paragraph_format.keep_with_next=i<len(lines)-1
        om=el('oMath',line);p._p.append(om)
        if i==len(lines)-1:runs(p,f'   ({topic}.{number})',10)
    return p
