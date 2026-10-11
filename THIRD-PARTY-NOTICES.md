# Credits, licences and scope

Original application code © 2026 Chintan B. Maniyar, MIT. Original educational copy, icon line drawings and mat illustration: Chintan B. Maniyar / Lake Lab, CC BY 4.0. Diagram source is in `app.js` and `shared/ui.js`. The home map uses real USGS geometry and City monitoring locations, with custom display styling.

## Frozen datasets

| Collection | Author / owner | Terms | Source |
|---|---|---|---|
| Water quality | City of Austin Watershed Protection | Public Domain, as declared by source metadata | https://data.austintexas.gov/d/5tye-7ray |
| Discharge | U.S. Geological Survey | Public Domain | https://waterdata.usgs.gov/monitoring-location/USGS-08158000/ |
| Weather | NOAA NCEI, GHCN-Daily (Austin Camp Mabry) | Public Domain US observations; retain dataset citation | https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861 |
| Shoreline | USGS National Hydrography Dataset | Public Domain | https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12 |
| Local micrographs | Katherine Perri, Schonna Manning, Matt Ashworth, Brent Bellinger | CC BY 4.0 | https://data.mendeley.com/datasets/f94329byhk/2 |
| Sentinel-2 crop | Copernicus / ESA; Element 84 Earth Search / AWS mirror | Copernicus free, full and open use, attribution retained | https://documentation.dataspace.copernicus.eu/FAQ.html |

Sentinel credit: **Contains modified Copernicus Sentinel data 2019.** Scene S2B_14RPU_20190813_0_L2A. Native 10 m crop of the supplied true-colour asset, with a JPEG display copy; no extra contrast stretch. Source/processing details, geometry transform and checksums are in `data/sentinel-2`.

GHCN-Daily citation: Menne, M. J., et al. (2012), Global Historical Climatology Network – Daily (GHCN-Daily), Version 3. NOAA National Climatic Data Center. https://doi.org/10.7289/V5D21VHZ. Cite the specific station/window and retrieval date in `data/noaa-weather/metadata.json`.

Perri data citation: Perri, K.; Manning, S.; Ashworth, M.; Bellinger, B. (2024), dataset version 2, https://doi.org/10.17632/f94329byhk.2. Original microscope plates are unchanged and publisher checksums verified. OTU-to-genus mapping remains under review.

## Comparison photographs

All four originals are unchanged. Sources, licences, capture dates, alt text and individual retrieval timestamps are in `data/open-images/images.json` and request sidecars. These do not depict Lady Bird Lake.

- **Microcystis live.jpg** — Panek, [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/), [source](https://commons.wikimedia.org/wiki/File:Microcystis_live.jpg).
- **Dolichospermum sp..jpg** — Masa Zupancic, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), [source](https://commons.wikimedia.org/wiki/File:Dolichospermum_sp..jpg). Adapted images must retain applicable share-alike terms; the original is not relicensed as CC BY.
- **Microscopic image of spirogyra.jpg** — SPJ777, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [source](https://commons.wikimedia.org/wiki/File:Microscopic_image_of_spirogyra.jpg).
- **20230604Lemna minor1.jpg** — AnRo0002, [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), [source](https://commons.wikimedia.org/wiki/File:20230604Lemna_minor1.jpg).

The pollen photo was not downloaded due to host rate limits. It is a candidate, not a bundled asset.

## Not distributed as app data

No LCRA, NASA POWER or non-USGS WQP observations are included. Forward optical equations are adapted from Water Optics Lab (MIT), revision cf17a481bea2cbbcb98142274bfa6fede9df6529. Numerical reference tables are original analytic teaching shapes (CC BY 4.0), not copied research tables. See docs/optical-methods.md. The Phase 0 folder contains audit evidence, not an approved training dataset. LCRA inventory metadata were moved outside the repository while redistribution terms remain unresolved.

No third-party runtime libraries are used in Phase 1. Rasterio and Pillow are optional maintainer tools for the Sentinel crop and do not ship to the browser. Chart.js can be vendored with its MIT notice when the chart stations are implemented.

Field photos: Perri, Bellinger, Ashworth and Manning, Toxins 16 (2024), 91, Figure 2, CC BY 4.0, https://doi.org/10.3390/toxins16020091 . Both panels retained without visual changes.
