# Microscope images from the local study

Source: https://data.mendeley.com/datasets/f94329byhk/2

Author: Katherine Perri, Schonna Manning, Matt Ashworth and Brent Bellinger

Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

Retrieved: 2026-10-09T22:31:57.368917+00:00

Period: 2019 study; dataset version 2 published 2024-02-07. Count: 3 records.

## Processing
- Download original microscopy files from version 2.
- Verify each file against the publisher SHA-256; no crop or alteration.

## Known gaps
- OTU names retained until species mapping is reviewed.
- Three microscope plates are not three verified toxin outcomes or enough independent examples for a robust classifier.

## Refresh
Run `python3 scripts/freeze.py perri` from the repository root. Existing source files are cached; move this folder aside before a deliberate refresh. Exact requests, checksums and output counts are in metadata.json. Source responses retain their own retrieval dates.
