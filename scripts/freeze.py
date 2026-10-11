#!/usr/bin/env python3
"""Manual, keyless snapshot refresh. Standard library only; never run by the website.
Usage: python3 scripts/freeze.py [all|austin|usgs|noaa|outline|perri]
Existing raw responses are reused. Move a dataset folder aside for a deliberate refresh.
"""
import csv, gzip, hashlib, io, json, sys, time, urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timezone, date, timedelta
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
START='2016-01-01'; END='2025-12-31'
def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def get(url,path,binary=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        for attempt in range(4):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'LakeLab educational snapshot (github.com/Chintan2108)'})
                with urllib.request.urlopen(req,timeout=150) as r: data=r.read()
                if not binary:json.loads(data)
                path.write_bytes(data)
                save(path.with_suffix(path.suffix+'.request.json'),{'url':url,'retrievedAt':datetime.now(timezone.utc).isoformat(),'sha256':sha(path)})
                break
            except Exception as error:
                if getattr(error, "code", None) in (403, 429) or attempt==3:raise
                time.sleep(2+attempt*2)
    return path.read_bytes() if binary else json.loads(path.read_text())
def url(base,**kw):return base+'?'+urllib.parse.urlencode(kw)
def csvwrite(path,rows,fields=None):
    fields=fields or sorted({k for r in rows for k in r})
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def finish(id,title,agency,license,licenseUrl,source,rows,files,span,gaps,steps,kind='Measured'):
    folder=DATA/id
    requests=[json.loads(p.read_text()) for p in folder.glob('*.request.json')]
    meta={'id':id,'title':title,'agency':agency,'kind':kind,'license':license,'licenseUrl':licenseUrl,'sourceUrl':source,'retrievedAt':max(r['retrievedAt'] for r in requests),'period':span,'recordCount':rows,'countUnit':'measurement rows' if id=='austin-water-quality' else 'records','files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in files],'requests':requests,'cleaning':steps,'limitations':gaps,'script':'scripts/freeze.py','scriptVersion':'1.0.0'}
    save(folder/'metadata.json',meta)
    (folder/'README.md').write_text(f'# {title}\n\nSource: {source}\n\nAuthor: {agency}\n\nLicence: [{license}]({licenseUrl})\n\nRetrieved: {meta["retrievedAt"]}\n\nPeriod: {span}. Count: {rows:,} {meta["countUnit"]}.\n\n## Processing\n'+''.join('- '+s+'\n' for s in steps)+'\n## Known gaps\n'+''.join('- '+s+'\n' for s in gaps)+f'\n## Refresh\nRun `python3 scripts/freeze.py {dict(zip(["austin-water-quality","usgs-flow","noaa-weather","lake-outline","perri-2019"],["austin","usgs","noaa","outline","perri"]))[id]}` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.\n')
    print(id,rows,flush=True)
def austin():
    folder=DATA/'austin-water-quality';folder.mkdir(exist_ok=True)
    where=f"watershed='Lady Bird Lake' AND sample_date between '{START}T00:00:00' and '{END}T23:59:59'"
    rows=[];offset=0
    while True:
        batch=get(url('https://data.austintexas.gov/resource/5tye-7ray.json',**{'$where':where,'$order':'ref_no','$limit':10000,'$offset':offset}),folder/f'source-{offset}.json')
        rows+=batch
        if len(batch)<10000:break
        offset+=10000
    assert len({r['ref_no'] for r in rows})==len(rows),'Duplicate source IDs; retry a consistent snapshot'
    hab=[r for r in rows if r.get('project')=='Lady Bird Lake Harmful Algal Bloom Monitoring']
    hab_ids={r['ref_no'] for r in hab}
    routine=[r for r in rows if r['ref_no'] not in hab_ids]
    toxins=[r for r in hab if any(x in r.get('parameter','').upper() for x in ['TOXIN','MICROCYSTIN'])]
    files=[]
    for name,subset in [('observations',rows),('hab',hab),('other-projects',routine),('toxins',toxins)]:
        p=folder/(name+'.csv');csvwrite(p,subset);files.append(p)
    # Preserve exact units and flags; no fabricated binary toxicity labels.
    sites={}
    for r in rows:
        sid=r['sample_site_no'];site=sites.setdefault(sid,{'id':sid,'names':[], 'coordinates':[]})
        if r.get('site_name') not in site['names']:site['names'].append(r.get('site_name'))
        if r.get('lon_dd_wgs84') and r.get('lat_dd_wgs84'):
            coord=[float(r['lon_dd_wgs84']),float(r['lat_dd_wgs84'])]
            if coord not in site['coordinates']:site['coordinates'].append(coord)
    save(folder/'sites.json',list(sites.values()));files.append(folder/'sites.json')
    inventory={}
    for r in rows:
        key=(r.get('parameter',''),r.get('unit',''),r.get('medium',''))
        item=inventory.setdefault(key,{'parameter':key[0],'unit':key[1],'medium':key[2],'count':0,'first':r['sample_date'],'last':r['sample_date']})
        item['count']+=1;item['first']=min(item['first'],r['sample_date']);item['last']=max(item['last'],r['sample_date'])
    save(folder/'inventory.json',list(inventory.values()));files.append(folder/'inventory.json')
    dates=sorted(r['sample_date'] for r in rows)
    save(folder/'summary.json',{'rows':len(rows),'habRows':len(hab),'toxinRows':len(toxins),'sites':len(sites),'habSiteDays':len({(r['sample_site_no'],r['sample_date'][:10]) for r in hab}),'first':dates[0],'last':dates[-1]})
    files.append(folder/'summary.json')
    finish('austin-water-quality','Lady Bird Lake water-quality records','City of Austin Watershed Protection','Public Domain','https://data.austintexas.gov/api/views/5tye-7ray.json','https://data.austintexas.gov/d/5tye-7ray',len(rows),files,dates[0][:10]+' to '+dates[-1][:10],['Source is provisional and may include unreviewed or QC samples.','Watershed filter includes tributaries and varied media, depths and projects; not all rows are in-lake water.','No interpolation, unit conversion, outlier removal or safe/unsafe labels. Review parameter, medium, depth, qualifier and QC fields before analysis.','Toxin coverage is sparse and selectively sampled; below reporting limit is not zero or proof of safety.'],['Filter exact watershed and approved 2016–2025 dates; paginate by unique ref_no.','Retain all source fields as text in CSV, including qualifier, method, depth and QC. Missing fields become empty cells.','Separate HAB project, other projects and toxin analytes; preserve all rows.','List unique site IDs and every returned name/coordinate variant; inventory parameter/unit/medium counts.'])
def usgs():
    folder=DATA/'usgs-flow';raw=get(url('https://waterservices.usgs.gov/nwis/dv/',format='json',sites='08158000',startDT=START,endDT=END,parameterCd='00060',statCd='00003'),folder/'source.json')
    rows=[]
    for s in raw['value']['timeSeries']:
        for block in s['values']:
            for v in block['value']:rows.append({'date':v['dateTime'][:10],'value':v['value'],'unit':s['variable']['unit']['unitCode'],'qualifiers':'|'.join(v['qualifiers']),'site':'08158000','parameter':'00060','statistic':'00003','noDataValue':s['variable']['noDataValue']})
    assert len({r['date'] for r in rows})==len(rows)
    p=folder/'daily.csv';csvwrite(p,rows)
    observed={r['date'] for r in rows};day=date.fromisoformat(START);missing=[]
    while day<=date.fromisoformat(END):
        if day.isoformat() not in observed:missing.append(day.isoformat())
        day+=timedelta(days=1)
    finish('usgs-flow','Daily river flow below the lake','U.S. Geological Survey','Public Domain','https://www.usgs.gov/faqs/are-usgs-reportspublications-copyrighted','https://waterdata.usgs.gov/monitoring-location/USGS-08158000/',len(rows),[p],min(r['date'] for r in rows)+' to '+max(r['date'] for r in rows),['Gauge is downstream of Longhorn Dam, not a measurement of lake currents or Tom Miller releases.','Daily means hide changes within a day. Preserve approval/estimate qualifiers and no-data sentinel.','Missing dates: '+(', '.join(missing) if missing else 'none')+'. No values were filled in.'],['Extract daily mean discharge (00060, statistic 00003).','Preserve source units and qualifiers. Do not fill missing dates or convert flow to lake speed.'])
def noaa():
    folder=DATA/'noaa-weather';raw=get(url('https://www.ncei.noaa.gov/access/services/data/v1',dataset='daily-summaries',stations='USW00013958',startDate=START,endDate=END,dataTypes='TMAX,TMIN,PRCP',units='metric',format='json',includeAttributes='true'),folder/'source.json')
    assert len({r['DATE'] for r in raw})==len(raw)
    p=folder/'daily.csv';csvwrite(p,raw)
    finish('noaa-weather','Austin daily weather','NOAA NCEI / GHCN-Daily, Austin Camp Mabry','Public Domain','https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861','https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00013958/detail',len(raw),[p],min(r['DATE'] for r in raw)+' to '+max(r['DATE'] for r in raw),['Air temperature is not water temperature; rain is measured at Camp Mabry, not at the lake.','Attribute strings preserve measurement, quality and source flags; trace rain must not be treated as exact zero.','No solar radiation or hourly observations included.'],['Request metric daily minimum/maximum air temperature (°C) and precipitation (mm).','Retain source attribute flags and missing fields; no interpolation.'])
def outline():
    folder=DATA/'lake-outline';raw=get(url('https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query',where="gnis_id='01376484'",outFields='*',returnGeometry='true',outSR='4326',f='geojson'),folder/'source.json')
    assert 'features' in raw,raw
    features=[f for f in raw['features'] if str(f['properties'].get('PERMANENT_IDENTIFIER'))=='92669797']
    if not features:features=[f for f in raw['features'] if f['properties'].get('GNIS_NAME')=='Lady Bird Lake']
    assert len(features)==1,[(f['properties']) for f in raw['features']]
    p=folder/'lake.geojson';save(p,{'type':'FeatureCollection','features':features})
    finish('lake-outline','Lady Bird Lake shoreline','U.S. Geological Survey, National Hydrography Dataset','Public Domain','https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer','https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12',1,[p],'Feature timestamp: 2013-03-19',['Historical mapped shoreline, not today’s measured water edge.','Display map is for learning, not navigation.'],['Select GNIS 01376484 and verified Lady Bird Lake feature.','Preserve geometry, holes and attributes; WGS84 coordinates. No simplification.'],'Derived from public data')
def perri():
    folder=DATA/'perri-2019';source='https://data.mendeley.com/datasets/f94329byhk/2'
    raw=get('https://data.mendeley.com/public-api/datasets/f94329byhk/files?folder_id=a5437c92-e780-46c5-9e68-88d90277ee25&version=2&%24start=0&%24limit=1000',folder/'source.json')
    files=[];images=[]
    for i,r in enumerate(raw):
        p=folder/f'micrograph-{i+1}.jpg';get(r['content_details']['download_url'],p,True)
        assert sha(p)==r['content_details']['sha256_hash']
        files.append(p);images.append({'id':r['id'],'file':str(p.relative_to(ROOT)),'title':r['filename'],'author':'Katherine Perri, Schonna Manning, Matt Ashworth and Brent Bellinger','license':'CC BY 4.0','sourceUrl':source,'alt':'Research microscope plate: '+r['filename'].removesuffix('.JPG')+'. Species labels await science review.','changes':'None; original file.','specimenGroup':r['filename'],'reviewStatus':'OTU-to-genus mapping pending researcher review'})
    save(folder/'images.json',images);files.append(folder/'images.json')
    finish('perri-2019','Microscope images from the local study','Katherine Perri, Schonna Manning, Matt Ashworth and Brent Bellinger','CC BY 4.0','https://creativecommons.org/licenses/by/4.0/',source,len(raw),files,'2019 study; dataset version 2 published 2024-02-07',['OTU names retained until species mapping is reviewed.','Three microscope plates are not three verified toxin outcomes or enough independent examples for a robust classifier.'],['Download original microscopy files from version 2.','Verify each file against the publisher SHA-256; no crop or alteration.'],'Real image')
def manifest():
    save(DATA/'manifest.json',{'schemaVersion':1,'window':[START,END],'datasets':[json.loads(p.read_text()) for p in sorted(DATA.glob('*/metadata.json'))]})
if __name__=='__main__':
    jobs={'austin':austin,'usgs':usgs,'noaa':noaa,'outline':outline,'perri':perri}
    chosen=sys.argv[1] if len(sys.argv)>1 else 'all'
    for name,job in jobs.items():
        if chosen in ('all',name):job();manifest()
