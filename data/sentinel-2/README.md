# Lady Bird Lake from Sentinel-2

Author: Copernicus / ESA; Element 84 Earth Search mirror

Source: https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2B_14RPU_20190813_0_L2A

Licence: [Copernicus free, full and open use](https://documentation.dataspace.copernicus.eu/FAQ.html)

Retrieved: 2026-10-10T03:26:32.240012+00:00

Period: 2019-08-13. 1 images.

## Cleaning
- Select audited scene S2B_14RPU_20190813_0_L2A.
- Range-read a native 10 m RGB crop covering the lake; save georeferenced TIFF and JPEG.
- Contains modified Copernicus Sentinel data 2019.

## Limitations
- True colour does not identify toxins or hidden bottom mats.
- L2A land surface reflectance is not water-leaving reflectance.
- Cloud/shadow suitability requires visual review; no quantitative cloud mask was applied.

## Refresh
`python3 scripts/freeze-imagery.py sentinel`. See script docstring for dependencies. Exact requests and SHA-256 checksums are in metadata.json. Originals are cached; move this folder aside for a new retrieval.
