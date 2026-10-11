# Lady Bird Lake shoreline

Source: https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12

Author: U.S. Geological Survey, National Hydrography Dataset

Licence: [Public Domain](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer)

Retrieved: 2026-10-09T22:29:47.669449+00:00

Period: Feature timestamp: 2013-03-19. Count: 1 records.

## Processing
- Select GNIS 01376484 and verified Lady Bird Lake feature.
- Preserve geometry, holes and attributes; WGS84 coordinates. No simplification.

## Known gaps
- Historical mapped shoreline, not today’s measured water edge.
- Display map is for learning, not navigation.

## Refresh
Run `python3 scripts/freeze.py outline` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.
