import zipfile, xml.etree.ElementTree as ET, re

z = zipfile.ZipFile('Report/MedRadar_Phase_1_Project_Report_Final_Fixed.docx')
doc_xml = z.read('word/document.xml').decode('utf-8')
rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')

rels_tree = ET.fromstring(rels_xml)
rel_map = {r.attrib['Id']: r.attrib['Target'] for r in rels_tree}

media_files = [f for f in z.namelist() if f.startswith('word/media/')]
print(f'Total media files in zip: {len(media_files)}')
for m in sorted(media_files):
    print(f'  {m} ({z.getinfo(m).file_size:,} bytes)')

# Check all blip embeds in doc
blips = re.findall(r'r:embed="([^"]+)"', doc_xml)
print(f'\nTotal blip embeddings in doc: {len(blips)}')
for b in blips:
    target = rel_map.get(b, 'MISSING!')
    zip_target = 'word/' + target
    in_zip = zip_target in z.namelist()
    print(f'  embed={b} -> target={target} (in zip: {in_zip})')

# Check sequential order of headings, figures, tables
tree = ET.fromstring(doc_xml)
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
print('\n=== Structure and Sequence ===')
for p in tree.findall('.//{' + W_NS + '}p'):
    t = ''.join(x.text for x in p.findall('.//{' + W_NS + '}t') if x.text).strip()
    if any(t.startswith(k) for k in ['CHAPTER', '1.', '2.', '3.', '4.', '5.', 'Figure', 'Table', 'BONAFIDE', 'DECLARATION', 'ABSTRACT', 'TABLE OF CONTENTS', 'LIST OF', 'PROJECT TIMELINES', 'PUBLICATION', 'REFERENCES']):
        if len(t) < 90:
            print(' ', t)
