#!/usr/bin/env python3
"""Generate openly licensed, explicitly simulated teaching examples. No field data input."""
import json,csv,math,random,hashlib
from pathlib import Path
from datetime import date,timedelta
R=Path(__file__).resolve().parents[1];D=R/'data/simulations';D.mkdir(exist_ok=True)
r=random.Random(6202019);rows=[]
for i in range(240):
 day=date(2020,1,1)+timedelta(days=i*5);season=math.sin(2*math.pi*(i%73)/73-1.0)
 temperature=round(23+9*season+r.gauss(0,2),1);nutrients=round(max(0,min(1,r.random()*.7+.2)),2);rain=round(max(0,r.gauss(6,8)),1);flow=round(max(0,min(100,30+rain*1.5+r.gauss(0,13))),1)
 # Later simulated seasons change the nutrient effect: a deliberate distribution shift.
 z=-1.8+.16*(temperature-20)+(2.8 if i<160 else 1.4)*nutrients-.025*flow+.025*rain+r.gauss(0,.65)
 outcome=int(r.random()<1/(1+math.exp(-z)))
 rows.append({'id':i,'date':str(day),'temperature':temperature,'nutrients':nutrients,'rain':rain,'flow':flow,'outcome':outcome,'kind':'Simulated','modelVersion':'forecast-teaching-v1','seed':6202019})
(D/'forecast.json').write_text(json.dumps(rows,indent=2)+'\n')
with (D/'forecast.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
sensors=[]
for h in range(24):
 light=max(0,math.sin((h-6)*math.pi/12));warm=max(0,math.sin((h-9)*math.pi/12));growth=max(0,math.sin((h-10)*math.pi/12))
 sensors.append({'hour':h,'temperature_c':round(24+5*warm,2),'ph':round(7.7+.7*light,2),'oxygen_mg_l':round(6+3*light,2),'turbidity_ntu':round(5+2*growth,2),'phycocyanin_rfu':round(10+8*growth,2),'kind':'Simulated'})
(D/'sensor-day.json').write_text(json.dumps(sensors,indent=2)+'\n')
with (D/'sensor-day.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(sensors[0]));w.writeheader();w.writerows(sensors)
(D/'README.md').write_text('''# Original teaching simulations

Author: Chintan B. Maniyar / Lake Lab. Licence: CC BY 4.0. Code: MIT.
Source: scripts/make-simulations.py, version 1.0. Seed 6202019. These are NOT Lady Bird Lake measurements or validated forecasts.

forecast: 240 invented visits spaced five days apart starting 2020-01-01. Inputs: temperature °C, relative nutrient index 0–1, prior rain mm and relative flow 0–100. Synthetic outcomes use logistic probability with intercept -1.8, temperature coefficient .16, nutrient coefficient 2.8 then 1.4 after visit 159, flow -.025, rain .025, Gaussian latent noise SD .65, plus a Bernoulli draw. All choices are author assumptions for learning. The later change deliberately tests generalization. Browser training uses first N of first160 rows; last80 remain held out. They are generated independently of real lab results. Never merge with measured outcomes.

sensor-day: 24 invented hourly values. Light rises after06:00; delayed warmth after09:00; delayed pigment/particles after10:00. Sine pulses, amplitudes, lags and baseline values are author chosen. pH and DO rise together; a pigment signal lags in this specific scenario, not a general biological rule. RFU is instrument-dependent. No toxin concentration is simulated.

Refresh: python3 scripts/make-simulations.py. Deterministic seed; no network. Outputs stay separate from field data.
''')
