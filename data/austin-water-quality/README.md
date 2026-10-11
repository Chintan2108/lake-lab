# Lady Bird Lake water-quality records

Source: https://data.austintexas.gov/d/5tye-7ray

Author: City of Austin Watershed Protection

Licence: [Public Domain](https://data.austintexas.gov/api/views/5tye-7ray.json)

Retrieved: 2026-10-09T22:29:38.332246+00:00

Period: 2016-02-17 to 2025-12-16. Count: 39,001 measurement rows.

## Processing
- Filter exact watershed and approved 2016–2025 dates; paginate by unique ref_no.
- Retain all source fields as text in CSV, including qualifier, method, depth and QC. Missing fields become empty cells.
- Separate HAB project, other projects and toxin analytes; preserve all rows.
- List unique site IDs and every returned name/coordinate variant; inventory parameter/unit/medium counts.

## Known gaps
- Source is provisional and may include unreviewed or QC samples.
- Watershed filter includes tributaries and varied media, depths and projects; not all rows are in-lake water.
- No interpolation, unit conversion, outlier removal or safe/unsafe labels. Review parameter, medium, depth, qualifier and QC fields before analysis.
- Toxin coverage is sparse and selectively sampled; below reporting limit is not zero or proof of safety.

## Refresh
Run `python3 scripts/freeze.py austin` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.
