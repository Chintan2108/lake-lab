#!/usr/bin/env python3
"""Generate the original analytic fallback; never redistribute unlicensed tables.

The historical name reflects the planned extraction, which was not done because
source-table open licences could not be verified. No network required.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
root = Path(__file__).resolve().parents[1]
out = root / 'data' / 'optical-reference'
out.mkdir(parents=True, exist_ok=True)
def gaussian(nm, center, width):
    return math.exp(-0.5 * ((nm - center) / width) ** 2)
def shape(nm):
    return gaussian(nm, 440, 45) + 0.5 * gaussian(nm, 675, 18)
with (out / 'analytic-reference.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['wavelength_nm', 'water_absorption_teaching_m-1', 'phytoplankton_shape_teaching_relative'])
    for nm in range(400, 801, 5):
        writer.writerow([nm, 0.005 + 0.03 * math.exp((nm - 500) / 70), shape(nm) / shape(440)])
meta = {
    'id': 'lake-lab-analytic-v1', 'kind': 'simulated',
    'author': 'Chintan B. Maniyar / Lake Lab', 'license': 'CC BY 4.0',
    'created': '2026-10-09', 'retrieved': None,
    'source': 'Original analytic teaching formulas; see docs/optical-methods.md',
    'rows': 81, 'wavelength_nm': [400, 800], 'step_nm': 5,
    'sha256': hashlib.sha256((out / 'analytic-reference.csv').read_bytes()).hexdigest(),
    'upstream_equations': 'https://github.com/Chintan2108/Water_Optics_Rrs_Simulator/blob/cf17a481bea2cbbcb98142274bfa6fede9df6529/app.js',
    'upstream_numerical_tables_copied': False,
    'transform': 'Evaluate documented analytic functions at 5 nm intervals; no measured data fitted or copied.'
}
(out / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
print('Generated 81 analytic teaching rows; no original measurement tables copied.')
