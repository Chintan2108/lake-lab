#!/usr/bin/env python3
"""Check local content links and JavaScript syntax without network access."""
import json,subprocess,sys,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
node=sys.argv[1] if len(sys.argv)>1 else 'node'
for p in R.rglob('*.js'):
 if '.git' not in p.parts:subprocess.run([node,'--check',str(p)],check=True,capture_output=True)
for p in (R/'content').rglob('*.json'):
 d=json.loads(p.read_text())
 if isinstance(d,dict):
  for source in d.get('sources',[]):
   url=source['url']
   if not url.startswith(('http:','https:')):assert (R/url).is_file(),url
print('PASS: JavaScript syntax and local educational source links')
