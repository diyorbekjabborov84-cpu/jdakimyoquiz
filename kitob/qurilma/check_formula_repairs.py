"""Regression for 3.6/4.1 mathematical typography and optional Google roundtrip."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
NS={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
files={'3.6':'Noorganik-kislotalar-3.6-Kinetika-va-kataliz.docx','4.1':'Noorganik-kislotalar-4.1-Neytrallanish-va-tuz-hosil-bolishi.docx'}
for topic,name in files.items():
 path=ROOT/'chiqish'/name
 with ZipFile(path) as z:tree=etree.fromstring(z.read('word/document.xml'))
 maths=tree.xpath('//m:oMath',namespaces=NS);expected=10 if topic=='3.6' else 13
 assert len(maths)==expected
 assert len(tree.xpath('//m:f',namespaces=NS))==(9 if topic=='3.6' else 5)
 assert len(tree.xpath('//m:sSub',namespaces=NS))>10
 assert len(tree.xpath('//m:sSup',namespaces=NS))>=5
 for node in tree.xpath('//m:f',namespaces=NS):
  assert node.find('m:num',NS) is not None and node.find('m:den',NS) is not None
 for m in maths:
  txt=''.join(m.xpath('.//m:t/text()',namespaces=NS))
  assert '_' not in txt and '\\frac' not in txt and '\\(' not in txt
 plain=''.join(tree.xpath('//w:t/text()',namespaces=NS))
 assert '_' not in plain, 'Unconverted underscore in narrative/table/sidebar'
 assert all(plain.count(f'({topic}.{i})')==1 for i in range(1,9))
 assert not tree.xpath('//w:spacing[@w:lineRule="exact"]/ancestor::w:p[m:oMath]',namespaces=NS)
 # Input tags/fraction operands are retained after native Google Docs import/export.
 candidates=list((ROOT.parent/'google_drive').glob(topic+'*roundtrip.docx'))
 if candidates:
  with ZipFile(candidates[0]) as z:rt=etree.fromstring(z.read('word/document.xml'))
  assert len(rt.xpath('//m:oMath',namespaces=NS))==expected
  for tag in ['f','sSub','sSup']:
   assert len(rt.xpath('//m:'+tag,namespaces=NS))==len(tree.xpath('//m:'+tag,namespaces=NS)),tag
 # Narrative chemical digits and charges are real Word script properties.
 assert tree.xpath('//w:vertAlign[@w:val="subscript"]',namespaces=NS)
 assert tree.xpath('//w:vertAlign[@w:val="superscript"]',namespaces=NS)
 print(topic, 'PASS:',expected,'native Equation lines; fractions, scripts, 8 numbers, no raw markup; Google roundtrip tested' if candidates else 'local checks')
