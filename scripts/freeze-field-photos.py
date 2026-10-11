#!/usr/bin/env python3
"""Freeze the openly licensed, original embedded Figure 2 from Perri et al. (2024).
Requires pypdf. Supply --pdf for an already retrieved publisher PDF; otherwise download.
No crop, recolour, upscaling, image synthesis, or classifier augmentation is performed.
"""
import argparse, hashlib, io, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from pypdf import PdfReader
ROOT = Path(__file__).resolve().parents[1]
URL = 'https://mdpi-res.com/d_attachment/toxins/toxins-16-00091/article_deploy/toxins-16-00091-v2.pdf'
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--pdf', type=Path)
a = p.parse_args()
raw = a.pdf.read_bytes() if a.pdf else urllib.request.urlopen(URL, timeout=60).read()
reader = PdfReader(io.BytesIO(raw))
assert len(reader.pages) == 15, 'Publisher file changed: review before extracting.'
images = [im for im in reader.pages[2].images if im.image.size == (451, 302)]
assert images and len({hashlib.sha256(i.data).hexdigest() for i in images}) == 1
image = images[0].data
out = ROOT / 'data/field-photos'
out.mkdir(parents=True, exist_ok=True)
(out / 'red-bud-mats-2019.jpg').write_bytes(image)
stamp = datetime.now(timezone.utc).isoformat()
item = dict(id='red-bud-mats-2019', file='data/field-photos/red-bud-mats-2019.jpg',
 title='Red Bud Isle mat photographs, August 2019',
 author='Katherine A. Perri, Brent J. Bellinger, Matt P. Ashworth and Schonna R. Manning',
 license='CC BY 4.0', licenseUrl='https://creativecommons.org/licenses/by/4.0/',
 sourceUrl='https://doi.org/10.3390/toxins16020091', downloadUrl=URL,
 retrievedAt=stamp, dates=['2019-08-08','2019-08-12'],
 alt='Two field photographs of thick olive-brown and green mats in shallow water near Red Bud Isle. These are real mat photographs; appearance does not show toxin levels.',
 changes='Original embedded JPEG extracted from page 3, Figure 2, without visual changes; both panels preserved.',
 specimenGroup='Perri2024-Figure2-RedBud2019',
 evidence='Figure 2 caption identifies metaphyton mats around Red Bud Isle in Lady Bird Lake, photographed August 8 (A) and August 12 (B), 2019.',
 quizLabel='mat', explanation='The researchers identified these as mats at Red Bud Isle. The clumps look different from a smooth green surface bloom. A photo cannot tell us whether toxins are present.',
 uncertainty='A source-identified example, not a rule for identifying every photo. Mat presence does not establish toxicity. No individual photographer is credited separately in the article.',
 sha256=hashlib.sha256(image).hexdigest(), bytes=len(image))
(out / 'images.json').write_text(json.dumps([item], indent=2)+'\n')
meta=dict(id='field-photos',title='Lady Bird Lake mat field photographs',agency=item['author'],kind='Real image',
 license=item['license'],licenseUrl=item['licenseUrl'],sourceUrl=item['sourceUrl'],retrievedAt=stamp,
 period='2019-08-08 and 2019-08-12',recordCount=2,countUnit='photographs in one published figure',
 files=[dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size) for f in [out/'red-bud-mats-2019.jpg',out/'images.json']],
 requests=[dict(url=URL,sha256=hashlib.sha256(raw).hexdigest(),retrievedAt=stamp,access='Previously retrieved publisher PDF supplied locally' if a.pdf else 'Downloaded publisher PDF')],
 cleaning=[item['changes']],limitations=[item['uncertainty'],'The two panels are not independent training or validation sets.'],
 script='scripts/freeze-field-photos.py',scriptVersion='1.0.0')
(out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Extracted verified Figure 2:',len(image),'bytes')
