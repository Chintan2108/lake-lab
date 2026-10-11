#!/usr/bin/env python3
"""Offline validation of snapshot provenance, temporal scope, source keys and links."""
import json,csv,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for p in R.rglob('*.json'):json.loads(p.read_text())
config=json.loads((R/'config/lady-bird-lake.json').read_text())
manifest=json.loads((R/config['datasets']).read_text())
assert manifest['window']==['2016-01-01','2025-12-31']
for d in manifest['datasets']:
 assert all(d.get(x) for x in ['agency','license','licenseUrl','sourceUrl','retrievedAt','limitations','cleaning'])
 assert (R/'data'/d['id']/'README.md').exists()
 for f in d['files']:
  p=R/f['path'];assert p.is_file(),p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],p
for path in [config['outline']['file'],*config['content'].values()]:assert (R/path.split("?")[0]).exists(),path
for s in config['stations'].values():
 assert isinstance(s['enabled'],bool)
 assert (R/s['module']).exists() and (R/s['content']).exists()
def rows(path):return list(csv.DictReader((R/path).open()))
city=rows('data/austin-water-quality/observations.csv')
assert len({x['ref_no'] for x in city})==len(city)
assert all('2016-01-01'<=x['sample_date'][:10]<='2025-12-31' for x in city)
for x in city:assert x['watershed']=='Lady Bird Lake'
hab=rows('data/austin-water-quality/hab.csv');other=rows('data/austin-water-quality/other-projects.csv')
assert len(hab)+len(other)==len(city)
assert not ({r['ref_no'] for r in hab}&{r['ref_no'] for r in other})
toxins=rows('data/austin-water-quality/toxins.csv')
assert any(r['qualifier']=='<' for r in toxins)
assert all(r['sample_date'].startswith('2019') for r in toxins),'Toxin scope changed; review before continuing'
for p,datefield in [('data/usgs-flow/daily.csv','date'),('data/noaa-weather/daily.csv','DATE')]:
 r=rows(p);assert len({x[datefield] for x in r})==len(r)
 assert all('2016-01-01'<=x[datefield]<='2025-12-31' for x in r)
assert not any(x['date']=='2017-01-26' for x in rows('data/usgs-flow/daily.csv')),'Source gap changed; review documentation'
geo=json.loads((R/config['outline']['file']).read_text());assert len(geo['features'])==1
assert geo['features'][0]['properties']['GNIS_ID']=='01376484'
# Local assets in the entry page must exist; no remote scripts/styles/fonts.
html=(R/'index.html').read_text()
for tag,attribute in [('script','src'),('link','href')]:
 for path in re.findall(fr'<{tag}[^>]*\b{attribute}="([^"]+)"',html):
  assert not path.startswith(('https:','http:','//')),path
  assert (R/path.split("?")[0]).exists(),path
assert 'connect-src \'self\'' in html
print(f'PASS: {len(manifest["datasets"])} datasets, all output checksums, approved dates, distinct source keys, preserved toxin qualifiers, config/module paths and local entry assets.')
