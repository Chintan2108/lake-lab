# Austin daily weather

Source: https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00013958/detail

Author: NOAA NCEI / GHCN-Daily, Austin Camp Mabry

Licence: [Public Domain](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861)

Retrieved: 2026-10-09T22:29:46.896242+00:00

Period: 2016-01-01 to 2025-12-31. Count: 3,653 records.

## Processing
- Request metric daily minimum/maximum air temperature (°C) and precipitation (mm).
- Retain source attribute flags and missing fields; no interpolation.

## Known gaps
- Air temperature is not water temperature; rain is measured at Camp Mabry, not at the lake.
- Attribute strings preserve measurement, quality and source flags; trace rain must not be treated as exact zero.
- No solar radiation or hourly observations included.

## Refresh
Run `python3 scripts/freeze.py noaa` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.
