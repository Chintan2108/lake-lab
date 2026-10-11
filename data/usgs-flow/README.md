# Daily river flow below the lake

Source: https://waterdata.usgs.gov/monitoring-location/USGS-08158000/

Author: U.S. Geological Survey

Licence: [Public Domain](https://www.usgs.gov/faqs/are-usgs-reportspublications-copyrighted)

Retrieved: 2026-10-09T22:29:45.704026+00:00

Period: 2016-01-01 to 2025-12-31. Count: 3,652 records.

## Processing
- Extract daily mean discharge (00060, statistic 00003).
- Preserve source units and qualifiers. Do not fill missing dates or convert flow to lake speed.

## Known gaps
- Gauge is downstream of Longhorn Dam, not a measurement of lake currents or Tom Miller releases.
- Daily means hide changes within a day. Preserve approval/estimate qualifiers and no-data sentinel.

## Refresh
Run `python3 scripts/freeze.py usgs` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.

Observed gap: 2017-01-26 is absent from this snapshot. It remains absent; no value was filled in.
