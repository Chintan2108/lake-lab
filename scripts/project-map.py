#!/usr/bin/env python3
"""Local-only NHD geometry reprojection for metre-sized teaching grids; requires rasterio."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
from rasterio.warp import transform_geom
R=Path(__file__).resolve().parents[1];D=R/'data/map-grid';D.mkdir(exist_ok=True)
x=json.loads((R/'data/lake-outline/lake.geojson').read_text())
for f in x['features']:f['geometry']=transform_geom('EPSG:4326','EPSG:32614',f['geometry'])
x['crs']={'type':'name','properties':{'name':'EPSG:32614'}}
p=D/'lake-utm.geojson';p.write_text(json.dumps(x,separators=(',',':'))+'\n')
m={'id':'map-grid','title':'Lake geometry in metres','agency':'USGS NHD; projection by Lake Lab','kind':'Derived from public data','license':'Public Domain','licenseUrl':'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer','sourceUrl':'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12','retrievedAt':json.loads((R/'data/lake-outline/metadata.json').read_text())['retrievedAt'],'derivedAt':datetime.now(timezone.utc).isoformat(),'period':'Historical NHD outline','recordCount':1,'countUnit':'projected polygon','files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}],'cleaning':['Reproject frozen WGS84 polygon to UTM zone14N (EPSG:32614), preserving holes; no simplification.'],'limitations':['Grid alignment in the browser is author-chosen, not an actual sensor footprint.','Outline is historical; mixed-pixel effects vary by real orbit, geolocation and shoreline.'],'requests':[],'script':'scripts/project-map.py'}
(D/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
(D/'README.md').write_text('# Metre-based lake outline\n\nUSGS NHD, Public Domain. Reprojected from the frozen lake outline to EPSG:32614 using rasterio. Original source and retrieval date are in metadata.json; coordinates are metres. No simplification.\n\nRun `python3 scripts/project-map.py` with rasterio installed. No network. Grid alignment is a demonstration, not a satellite product.\n')
