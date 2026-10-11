#!/usr/bin/env python3
"""Derive small teaching assets from frozen sources. No network or invented labels."""
import csv, json, hashlib, calendar, statistics
from pathlib import Path
from datetime import date, timedelta, datetime, timezone
from collections import defaultdict, Counter
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=DATA/'derived'
SITES={'1996','1252','1997'}
PARAMS={'WATER TEMPERATURE':'Deg. Celsius','PH':'Standard units','DISSOLVED OXYGEN':'MG/L','PHOSPHORUS AS P':'MG/L','ORTHOPHOSPHORUS AS P':'MG/L','TOTAL KJELDAHL NITROGEN AS N':'MG/L','NITRATE/NITRITE AS N':'MG/L'}
def read(p):
 with (DATA/p).open(newline='') as h:return list(csv.DictReader(h))
def number(v):
 try:return float(v)
 except (ValueError,TypeError):return None
def save(name,rows):
 (OUT/(name+'.json')).write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/(name+'.csv')).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=keys);w.writeheader();w.writerows(rows)
OUT.mkdir(exist_ok=True)
observations=read('austin-water-quality/observations.csv')
selected=[r for r in observations if r['sample_site_no'] in SITES and r['medium']=='Surface Water' and PARAMS.get(r['parameter'])==r['unit']]
# Export every selected candidate with original fields, including excluded rows.
save('water-evidence',selected)
accepted=[];exclusions=Counter()
for r in selected:
 reason=None; depth=number(r['depth_in_meters']);value=number(r['result'])
 if r['qc_type']:reason='nonempty qc_type (replicate/QC sample)'
 elif r['qualifier']:reason='qualified or censored result'
 elif depth is None or not 0<=depth<=0.5:reason='missing or deeper than 0.5 m'
 elif value is None:reason='nonnumeric result'
 if reason:exclusions[reason]+=1
 else:accepted.append(r)
# No interpretation of undocumented QC flags: retain counts alongside estimates.
groups=defaultdict(list)
for r in accepted:groups[(r['sample_site_no'],r['sample_date'][:10],r['parameter'],r['unit'])].append(r)
visits=[]
for (site,day,param,unit),rows in sorted(groups.items()):
 visits.append(dict(date=day,site_id=site,site_name=rows[0]['site_name'],parameter=param,unit=unit,value=statistics.median(float(r['result']) for r in rows),measurement_count=len(rows),depth_min_m=min(float(r['depth_in_meters']) for r in rows),depth_max_m=max(float(r['depth_in_meters']) for r in rows),qc_flags='|'.join(sorted(set(r['qc_flag'] or '(blank)' for r in rows))),source_refs='|'.join(r['ref_no'] for r in rows)))
save('water-visits',visits)
monthly=defaultdict(list)
for r in visits:monthly[(int(r['date'][5:7]),r['parameter'],r['unit'])].append(r)
seasons=[]
for (month,param,unit),rows in sorted(monthly.items()):
 values=[r['value'] for r in rows]
 seasons.append(dict(month=month,month_name=calendar.month_name[month],parameter=param,unit=unit,median=statistics.median(values),minimum=min(values),maximum=max(values),site_day_count=len(rows),measurement_count=sum(r['measurement_count'] for r in rows),site_count=len(set(r['site_id'] for r in rows)),year_count=len(set(r['date'][:4] for r in rows)),first_date=min(r['date'] for r in rows),last_date=max(r['date'] for r in rows),qc_flags='|'.join(sorted(set(r['qc_flags'] for r in rows)))))
save('water-monthly',seasons)
weather={r['DATE']:r for r in read('noaa-weather/daily.csv')}
flowrows=read('usgs-flow/daily.csv');flow={r['date']:r for r in flowrows if r['parameter']=='00060' and r['statistic']=='00003'}
assert len(flow)==len(flowrows),'Duplicate daily flow rows require review'
daily=[];day=date(2016,1,1)
while day<=date(2025,12,31):
 d=day.isoformat();w=weather.get(d,{});f=flow.get(d,{})
 v=number(f.get('value'));v=None if v==number(f.get('noDataValue')) else v
 daily.append(dict(date=d,air_max_c=number(w.get('TMAX')),air_min_c=number(w.get('TMIN')),rain_mm=number(w.get('PRCP')),flow_ft3_s=v,weather_station=w.get('STATION','USW00013958'),flow_site='08158000',tmax_attributes=w.get('TMAX_ATTRIBUTES',''),tmin_attributes=w.get('TMIN_ATTRIBUTES',''),rain_attributes=w.get('PRCP_ATTRIBUTES',''),flow_qualifiers=f.get('qualifiers',''),weather_row_present=bool(w),flow_row_present=bool(f)))
 day+=timedelta(days=1)
save('environment-daily',daily)
toxins=[r for r in read('austin-water-quality/toxins.csv') if r['sample_site_no'] in SITES]
save('toxin-evidence',toxins)
groups=defaultdict(list)
for r in toxins:groups[(r['sample_site_no'],r['sample_date'],r['sample_ref_no'],r['medium'],r['unit'])].append(r)
samples=[]
for (site,timestamp,ref,medium,unit),rows in sorted(groups.items()):
 samples.append(dict(site_id=site,site_name=rows[0]['site_name'],sample_date=timestamp,sample_ref_no=ref,medium=medium,unit=unit,time_null=rows[0]['time_null'],measurement_count=len(rows),below_limit_count=sum(r['qualifier']=='<' for r in rows),unqualified_count=sum(not r['qualifier'] for r in rows),analytes='|'.join(sorted(set(r['parameter'] for r in rows))),source_refs='|'.join(r['ref_no'] for r in rows)))
save('toxin-samples',samples)
inputs=['austin-water-quality/observations.csv','austin-water-quality/toxins.csv','noaa-weather/daily.csv','usgs-flow/daily.csv']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
metadata=dict(generated_at=datetime.now(timezone.utc).isoformat(),script='scripts/derive-station-data.py',license='Public-domain source data; transformation script MIT',period=['2016-01-01','2025-12-31'],sites=sorted(SITES),inputs=[dict(path='data/'+p,sha256=digest(DATA/p),metadata='data/'+p.split('/')[0]+'/metadata.json') for p in inputs],source_ids=['Austin Socrata 5tye-7ray','NOAA GHCND USW00013958','USGS 08158000 parameter 00060 daily mean 00003'],counts=dict(water_candidates=len(selected),water_accepted_measurements=len(accepted),water_visits=len(visits),monthly_rows=len(seasons),daily_rows=len(daily),toxin_measurements=len(toxins),toxin_sample_groups=len(samples)),water_exclusions=dict(exclusions),water_qc_flags=dict(Counter(r['qc_flag'] or '(blank)' for r in accepted)),missing_flow_dates=[r['date'] for r in daily if r['flow_ft3_s'] is None],outputs=[dict(path='data/derived/'+p.name,sha256=digest(p)) for p in sorted(OUT.glob('*')) if p.suffix in ('.csv','.json') and p.name!='metadata.json'])
(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
assert len(daily)==3653
assert all(r['medium']=='Surface Water' for r in selected)
assert all(r['unit']==PARAMS[r['parameter']] for r in visits)
assert sum(r['measurement_count'] for r in samples)==len(toxins)
print(json.dumps(metadata['counts'],indent=2));print('Missing flow:',metadata['missing_flow_dates']);print('Exclusions:',dict(exclusions))
