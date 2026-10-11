# Data availability audit

Checked **2026-10-09**. Counts below are audit results, not cleaned datasets. “Unknown” means not verified, not zero. Raw values were sampled temporarily to test access; production downloads and cleaning are Phase 1. All app data will be frozen locally, with no runtime service calls.

## Availability at a glance

| Candidate | Reached / access | Verified span and count | Licence finding | Stations / decision |
|---|---|---|---|---|
| Austin harmful algae monitoring | City page reached; numerical records found in City dataset `5tye-7ray` | Project: 12,099 result rows, 2019-08-05–2026-10-02. Lady Bird Lake watershed subset: 8,212 rows, 23 site IDs, 481 site-days. Identified toxin rows in that subset: 2019 only. | Dataset metadata explicitly `PUBLIC_DOMAIN`; City webpage photographs have no verified open licence. | Understand, Predict, Decide. Use data; do not copy unlicensed City images. |
| Austin water quality | Socrata metadata and JSON queries succeeded; CSV route available | Whole portal dataset: 1,519,778 rows, 1947-12-07–2026-10-07. Lady Bird Lake watershed: 141,015 rows, 1982-05-01–2026-10-02. | Public domain in source API metadata. | Understand, Detect, Predict. Primary local source. |
| USGS 08158000 | Site catalogue and daily-values service succeeded | Mean discharge catalogue: 46,972 daily entries, 1898-03-01–2026-10-08. 2019 probe: 365 discharge and 365 current-location mean-height values; zero temperature values. | USGS-produced data: public domain. | Understand, Detect, Predict. Downstream context only. |
| Nearby USGS sites | Multi-site catalogue succeeded | Site AC: 413 discrete activities, 1975–2018. 08157900: 10 activities, 1975–1977. MoPac: 4, 1991–1994. | Public domain for USGS-produced records; distinguish partner-origin data. | Historical Detect context; not a recent continuous dock. |
| LCRA Hydromet | UI, site list and historical API reached | 18 lake-level sites listed. Longhorn-area probe: 193 hourly records, 2026-10-01 05:00Z–2026-10-09 05:00Z. Full archival span/count unknown. | No explicit open-data redistribution licence verified; site footer reserves rights. | Flow/level context conditional on reuse terms. |
| Water Quality Portal | Station search and period-of-record summary succeeded | Bounding box: 204 stations; 58 name matches for Lady Bird/Town Lake, including tributaries and duplicate agency locations. Site AC summary: 12,729 results, 1975–2018. | USGS subset public domain; do not assume one licence for all contributors. | Optional historical Detect/Understand records after deduplication. |
| NOAA/NCEI weather | Camp Mabry station page and access API reached, no key needed | Station page: 1938-06-01–2026-09-06 as indexed. Verified 2019 query: 365 days, each with TMAX, TMIN and PRCP. | NOAA-produced US data public domain; retain GHCN citation and source flags. | Understand, Predict. Prefer this for observed air temperature/rainfall. |
| NASA POWER | Daily API reached, no key needed | Documented daily availability from 1981 to near-present; 2019 probe: 365 entries each for solar, air temperature and corrected rainfall. | Public NASA access verified; a precise dataset-specific redistribution licence was not established in the reviewed pages. | Optional sunlight context pending policy documentation; derived estimates. |
| Perri et al. dataset v2 | Landing page and file/folder APIs succeeded | 2019 event, contextual 2016–2018 comparison, some 2021 isolate analyses. 15 folders; Micrographs folder: 3 JPGs; Statistics folder: 1 DOCX. Total files/observations in other folders not counted. | CC BY 4.0 explicitly stated. | Identify; Understand/Predict historical case study. |
| Open micrographs/look-alikes | Individual Commons file pages reached | Five core candidate files verified below, plus Perri's 3 micrograph files. This is not a sufficient independent training set by itself. | Asset-specific CC BY, CC BY-SA or CC0. | Identify and simulated Decide rounds. |
| Lake outline | USGS NHD REST query returned GeoJSON; OSM licence page also reached | One Lady Bird Lake polygon; feature date 2013-03-19, service refreshed October 2026. Geometry is a snapshot, not a series. | NHD public domain; OSM alternative ODbL. | Detect and navigation. Prefer NHD. |
| Sentinel-2 | Copernicus catalogue and anonymous Earth Search mirror reached | August 2019 bbox: 12 Copernicus items; Earth Search: 24 items (processing alternatives, not 24 independent days). Candidate true-colour COG returned HTTP 200. | Copernicus Sentinel open-data terms; retain modified-data attribution. | Detect. Crop/cloud QA still needed. |
| EPA/NASA CyAN Sentinel-3 | EPA page, guide and published lake list reached | 2,370 waterbodies in published 2018 list. Lady Bird/Texas Town Lake absent; Lake Austin present. No local CyAN measurement count verified. | Government guidance; underlying imagery retains applicable source terms. | Teach resolution limits. Do not promise a usable local CyAN trend. |

## 1. City of Austin: monitoring visits and toxin outcomes

[Official algae page](https://www.austintexas.gov/watershed-protection/algae-austins-waterways) explains the monitoring programme and local mat problem. It is not a complete downloadable visit ledger. The useful numerical route is the City's [Water Quality Sampling Data](https://data.austintexas.gov/d/5tye-7ray).

Verified routes:

```text
Metadata: https://data.austintexas.gov/api/views/5tye-7ray.json
Query:    https://data.austintexas.gov/resource/5tye-7ray.json
CSV:      https://data.austintexas.gov/api/v3/views/5tye-7ray/export.csv?accessType=DOWNLOAD
```

The JSON query endpoint was actually called using `$select`, `$where`, `$group` and `$limit`. The CSV export route is published by the [official catalogue record](https://catalog.data.gov/dataset/water-quality-sampling-data); the entire citywide CSV was not downloaded. The source API licence says Public Domain, even though an older aggregator entry said no licence supplied. Source metadata takes precedence for this audit.

Filtering `project = 'Lady Bird Lake Harmful Algal Bloom Monitoring'` alone includes Lake Austin, Barton Creek and downstream Colorado River sites. Also filter the reviewed site IDs and their spatial roles. The `watershed = 'Lady Bird Lake'` audit subset still includes the Barton Creek mouth/bridge and specialist sediment sites; it is broader than three routine shoreline stations.

For that subset:

- 8,212 measurements, 23 site IDs, 708 distinct site/timestamp combinations, **481 site/calendar-day combinations**. These are useful counts, not a validated visit register.
- Dihydroanatoxin-a: **54 mat rows** and **55 surface-water rows**, 2019-08-05 through 2019-11-21. Each medium has 27 distinct timestamp values across sites; timestamps without clock times are not unique visits.
- Mat rows: 41 have a `<` qualifier; 13 do not. Water rows: 51 have `<`; 4 do not. **Absence of a qualifier is not proof of a positive toxin result.** Numeric values, reporting limits, blanks and replicates must be inspected during cleaning.
- MC-LR, MC-LW, MC-RR and MC-YR likewise have 54 mat and 55 water rows apiece in this subset. The verified toxin inventory is therefore **545 measurement rows across five analytes**, not 545 independent outcomes.
- Post-2019 environmental, nutrient and mat-element measurements exist; this inventory did not establish a comparable post-2019 toxin-label series. Such results may exist in a separate publication, lab report or dataset. Their absence here does not imply the City stopped testing.

Three verified source IDs and coordinates:

| ID | Exact source name | Latitude | Longitude |
|---|---|---:|---:|
| 1996 | Redbud West of Parking Lot | 30.2903930913 | -97.7875256538 |
| 1252 | Lady Bird Lake @ Powerline | 30.264224 | -97.753719 |
| 1997 | Lagoon at Festival Beach | 30.2479417164 | -97.7245460451 |

Do not silently rename Powerline to Vic Mathias/Auditorium Shores, or Lagoon at Festival Beach to the boat ramp. The requested public-friendly aliases need a spatial/source crosswalk.

**Proposed cleaning:** preserve source IDs and names; separate mats, surface water and sediment; retain units, method, QC and censoring; group replicates without treating them as new visits; retain missing collection-time flags; distinguish detections from reporting-limit values; document any deduplication. Never convert `ng/g` mat results into `µg/L` water results. Do not impute toxin status between visits.

**Predict implication:** real-data evidence exploration is feasible. Multi-season supervised toxin forecasting is not justified by the verified label coverage alone.

## 2. City of Austin: general water-quality measurements

The same dataset supports real seasonal observations. These counts use **all records whose watershed equals Lady Bird Lake**, before medium/depth/QC screening:

| Parameter / reported unit | Rows | Earliest–latest |
|---|---:|---|
| Water temperature / °C | 9,555 | 1989-11-07–2026-10-02 |
| pH / standard units | 9,448 | 1989-11-07–2026-10-02 |
| Dissolved oxygen / mg/L | 9,429 | 1989-11-07–2026-10-02 |
| Turbidity / NTU | 1,037 | 1990-06-01–2025-11-05 |
| Turbidity / FTU | 798 | 1993-12-03–2009-09-24 |
| Chlorophyll-a / µg/L | 770 | 2001-07-18–2022-10-05 |
| Chlorophyll-a / mg/m³ | 889 | 1991-07-15–2001-06-06 |
| Chlorophyll-a / mg/L | 168 | 1999-08-17–2026-07-30 |
| Chlorophyll-a / RFU | 32 | 2009-09-16–2011-04-19 |
| Orthophosphorus as P / mg/L | 4,272 | 1990-11-02–2026-09-11 |
| Phosphorus as P / mg/L | 4,012 | 1991-09-25–2026-09-11 |
| Total Kjeldahl nitrogen as N / mg/L | 3,708 | 1991-07-15–2026-09-11 |

The inventory contains 1,641 parameter/unit combinations, many irrelevant to the app. No phycocyanin-named parameter appeared in this audit. This is a scoped search, not proof that no local PC measurements exist anywhere.

Important data-quality findings: one water-temperature row is labelled mg/L; some turbidity rows use length units; there are different chlorophyll units and fluorescence units. Do not normalize by label alone. Review method, medium, filter, depth and QC before conversion. Sample-time sequences may be depth profiles or multi-site surveys rather than continuous time series. A day of pH, oxygen, temperature and turbidity at a fixed location/depth remains unverified.

**Use:** empirical ranges and seasonal distributions after screening; real scatterplots and visit sequences in Detect. No interpolation through large sampling gaps. Derive seasonal presets as summaries, with sample counts, rather than presenting a synthetic combination of medians as an actual measured visit.

## 3. USGS 08158000 and nearby sites

[Station page](https://waterdata.usgs.gov/monitoring-location/USGS-08158000/) gives current coordinates **30.24613889, -97.68005556**. It is downstream of Longhorn Dam, outside Lady Bird Lake. Older station reports refer to previous positions, so their quoted dam distance must not be copied as the current distance.

Verified catalogue request:

```text
https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=08158000&seriesCatalogOutput=true
```

Verified daily-values probe:

```text
https://waterservices.usgs.gov/nwis/dv/?format=json&sites=08158000&startDT=2019-01-01&endDT=2019-12-31&parameterCd=00060,00065,00010&statCd=00003
```

It returned 365 discharge values and 365 gage-height values in the current-location series. It also included empty series; count across the response's location series rather than assuming the first one is populated. Temperature returned zero values.

Catalogue findings: mean discharge `00060/00003` spans 1898-03-01–2026-10-08, 46,972 entries. Mean gage height at the current location spans 2011-12-29–2026-10-08, 5,396 entries; a historical upstream-location series overlaps and must stay distinct. Daily mean temperature `00010/00003` has 354 entries, 1990-10-01–1991-09-29; another daily statistic has 1,682 entries, 1986-09-30–1991-09-29. These are not modern thermal records.

The site page lists continuous data beginning in 1991, but an intraday extraction was not counted in Phase 0. Verify the relevant instantaneous-data service and dates before promising a particular teaching day. The legacy services worked during this audit; refresh scripts should fail explicitly if services migrate, rather than replacing missing observations silently.

Nearby catalogue checks:

| Site | What was actually found |
|---|---|
| 08157900 — Town (Lady Bird) Lake | Catalogue: 10 discrete activities, 1975-02-03–1977-08-23. Not a verified contemporary continuous lake gauge. |
| 301500097424801 — Lake Site AC | 413 discrete sampling activities, 1975-02-03–2018-05-05. Historical in-lake chemistry. |
| 301650097453501 — MoPac Bridge | 4 discrete activities, 1991-02-28–1994-08-11. |
| 08154900 — Lake Austin | LCRA-origin lake-elevation unit-value records listed for a recent 120-day window. Preserve agency origin; do not automatically apply USGS rights to partner data. |

USGS data rights: [USGS copyright guidance](https://www.usgs.gov/faqs/are-usgs-reportspublications-copyrighted). Alternative for recent lake temperature: City observations. Downstream discharge is context, not a calibrated residence time or upstream release proxy.

## 4. LCRA Hydromet and dam/lake context

[Hydromet](https://hydromet.lcra.org/) and [Historical Data](https://hydromet.lcra.org/HistoricalData) were reached. The interface provides an Excel-labelled control whose code exports CSV. It limits date windows to less than 180 days. Its published JavaScript exposes the routes below; these are verified application routes, not a guaranteed stable public API contract.

```text
https://hydromet.lcra.org/api/GetSitesBySensorType/lakelevel
https://hydromet.lcra.org/api/HistoricData/GetDataBySite/4543/lakelevel/10-1-2026/10-8-2026/hourly
```

The site list contains 18 entries, including **3999 Tom Miller Dam**, **3963 Mansfield Dam**, and **4543 Lady Bird Lake near Longhorn Dam**. The tested query yielded 193 hourly stage records, UTC 2026-10-01 05:00 through 2026-10-09 05:00. That inclusive boundary is a reason to preserve time zones rather than assuming a simple midnight-to-midnight UTC window. Elevation datum/units must be checked before use.

The [historical lake-level PDF](https://www.lcra.org/download/Historical_Lake_levels.pdf/?wpdmdl=21289) charts Buchanan/Travis storage and elevations from 1940-09-30 to 2026-09-01. It is not a downloadable numeric Lady Bird Lake series. River-operations pages are linked by Hydromet, but a historical Tom Miller release table and its row count were not verified.

**Licence unresolved:** public viewing/downloading is established; open redistribution rights were not. Hold LCRA data out of the committed core until terms are documented. Use USGS discharge and City measurements as openly reusable alternatives, while linking to LCRA for context. No contact message or permission request has been sent to LCRA.

## 5. Water Quality Portal

[Portal](https://www.waterqualitydata.us/), [web-services documentation](https://www.waterqualitydata.us/webservices_documentation/).

Verified requests:

```text
https://www.waterqualitydata.us/data/Station/search?bBox=-97.80,30.23,-97.70,30.30&mimeType=csv
https://www.waterqualitydata.us/data/summary/monitoringLocation/search?siteid=USGS-301500097424801&mimeType=csv&dataProfile=periodOfRecord&summaryYears=all
```

The bbox returned **204 station records**, of which **58** matched Lady Bird/Town Lake in their names. They are not 58 independent in-lake sites: agency duplicates, tributary mouths and adjacent locations occur. Contributors include USGS, TCEQ, Texas Stream Team and NALMS.

For USGS Site AC, 2,223 annual characteristic-summary rows sum to **12,729 results spanning 1975–2018**. Do not sum activity counts across characteristics to claim unique visits. The documented result-download base is `https://waterqualitydata.us/data/Result/search`; a complete result-table extraction was deferred.

The portal warns that its legacy WQX 2.2 interface does not include USGS additions after March 11, 2024; the beta WQX 3.0 route addresses that limitation. Keep the service/profile version in provenance. For the historical Site AC probe, this does not create a new recent record.

Licence: use the confirmed public-domain USGS subset first. Non-federal contributors need their own rights metadata. Deduplicate against City records by agency, source sample ID, location, date, analyte and method before combining. No additional modern PC or toxin series was verified through this probe.

## 6. Weather: NOAA/NCEI and NASA POWER

### NOAA observations — recommended

[Austin Camp Mabry station](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00013958/detail), station `USW00013958`, 30.3208, -97.7604. The station page reports 1938-06-01–2026-09-06 in the version reached; exact current end date for each variable was not exhaustively queried.

The keyless access route was tested:

```text
https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00013958&startDate=2019-01-01&endDate=2019-12-31&dataTypes=TMAX,TMIN,PRCP&units=metric&format=json&includeAttributes=true
```

Result: 365 dates with all three parameters present. They still require quality/trace-precipitation flag handling. Air temperature is not lake-water temperature; the station is not a rain gauge on the lake. No local solar-radiation record was verified in this GHCN selection. Use measured daily maximum/minimum rather than inventing hourly weather.

Retain the [GHCN-Daily dataset citation and constraints](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861); NOAA's [data-management handbook](https://www.ncei.noaa.gov/sites/default/files/2025-04/NAO_212-15B-Data_Mgt_Handbook-2024-Oct-1_destinations_2025.pdf%23.pdf) describes public-domain/CC0 treatment of NOAA-produced data. Do not extend this to every image or external dataset hosted by NOAA.

### NASA POWER — optional derived sunlight

[Daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/), [source explanation](https://power.larc.nasa.gov/docs/faqs/data/).

```text
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,T2M,PRECTOTCORR&community=RE&longitude=-97.74&latitude=30.25&start=20190101&end=20191231&format=JSON&time-standard=UTC
```

The probe returned 365 daily values per parameter, sourced from SYN1DEG and MERRA2. Daily API documentation states availability from 1981 to near-real time; parameter-specific coverage must still be checked for a chosen window. Solar radiation is inferred from satellite observations through radiative-transfer modelling; meteorology is assimilated/model-derived. These are coarse-grid estimates, not measurements at the requested point.

Preserve API units, `-999` missing values, source versions and UTC/local-solar-time setting. Public API access is verified, but the reviewed documentation did not establish an explicit dataset-level redistribution licence. Record that status honestly and resolve the applicable NASA/source policy before committing POWER data. If unresolved, keep sunlight as an illustrative control and use NOAA for measured weather.

## 7. Perri et al. 2024

[Version 2 landing page](https://data.mendeley.com/datasets/f94329byhk/2), DOI **10.17632/f94329byhk.2**, published February 7, 2024. Contributors: Katherine Perri, Schonna Manning, Matt Ashworth and Brent Bellinger. **CC BY 4.0 verified.**

The initial unversioned web fetch failed, but versioned HTML and public APIs worked. Folder inventory:

```text
https://data.mendeley.com/public-api/datasets/f94329byhk/folders/2
https://data.mendeley.com/public-api/datasets/f94329byhk/files?folder_id=a5437c92-e780-46c5-9e68-88d90277ee25&version=2&%24start=0&%24limit=1000
```

The second route lists the **three actual micrograph files**:

| Filename | File ID | Bytes |
|---|---|---:|
| Morphology of OTU 10.JPG | `ba3c5f14-10c4-4df8-9c98-fcf7a94864c8` | 980,113 |
| Morphology of OTUs 7 & 11.JPG | `e1b31e1e-b190-4b04-bcde-9247d02a5e12` | 933,898 |
| Morphology of OTUs 8 & 9.JPG | `a8d7b006-6332-40ed-b715-6dd17e139e00` | 1,097,688 |

Each metadata item supplies a download URL of the form `https://data.mendeley.com/public-files/datasets/f94329byhk/files/FILE_ID/file_downloaded` and a SHA-256 checksum. The Statistics folder (`08b149bb-01d3-4ea4-acc0-bcaf0a8a1555`) contains **Pearson correlation coefficients.docx**, 13,759 bytes. That file is not assumed to be the raw environmental table. Fifteen folders include HPLC and DNA raw/processed data, with 2019/2021 labels. All file and biological observation counts remain unverified outside the two inspected folders.

The [paper](https://doi.org/10.3390/toxins16020091) was downloaded and read. Its sampling description lists four sites and six dates from August–October 2019; the dataset narrative describes collections continuing into November, and the City export includes additional dates. Keep these scopes separate. Do not force the publication's analysis subset and the portal's broader record to have identical counts. Useful content includes mixed mat communities, local micrographs and the distinction between mat and water toxin testing. Review OTU assignments and figure credits before extracting teaching images.

## 8. Individually checked image candidates

These file-description pages were opened; “Original file” provides the download route. Capture dates below are author-supplied metadata. None is claimed to depict Lady Bird Lake unless it comes from the reviewed local study. No images have yet been committed as app assets.

| Subject / file page | Author | Licence | Image date | Intended use |
|---|---|---|---|---|
| [Microcystis live.jpg](https://commons.wikimedia.org/wiki/File:Microcystis_live.jpg) | Panek | CC BY 2.5 | 2007-02-11 | Real microscope example; modest 569×502 size. |
| [Dolichospermum sp..jpg](https://commons.wikimedia.org/wiki/File:Dolichospermum_sp..jpg) | Masa Zupancic | CC BY-SA 4.0 | 2019-05-13 | Real microscope example; preserve share-alike on adaptations. |
| [Microscopic image of spirogyra.jpg](https://commons.wikimedia.org/wiki/File:Microscopic_image_of_spirogyra.jpg) | SPJ777 | CC BY 4.0 | 2023-03-15 | Green-alga look-alike. |
| [20230604Lemna minor1.jpg](https://commons.wikimedia.org/wiki/File:20230604Lemna_minor1.jpg) | AnRo0002 | CC0 1.0 | 2023-06-04 | Duckweed field comparison. |
| [Pollen on the water.jpg](https://commons.wikimedia.org/wiki/File:Pollen_on_the_water.jpg) | T.Smirnova | CC BY 4.0 | 2020-05-31 | Pollen field comparison. |

Also checked [Microcystis 1.jpg](https://commons.wikimedia.org/wiki/File:Microcystis_1.jpg), Michal Maňas, CC BY 4.0: **it is a culture flask photograph, not a micrograph**, so it is excluded from the microscopy shortlist. Do not rely on filenames alone.

The gallery can begin with these examples and Perri's local images. A classifier needs more independent, verified specimens per class. Use multiple crops for display only, not to inflate training/test sample counts. Record both parent-image and specimen/source grouping. Generic agency hosting is not sufficient proof of public-domain image rights; no unverified EPA/USGS/NOAA photographs are approved by this audit.

## 9. Lake outline

The [USGS NHD service](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer) identifies layer 12 as Waterbody — Large Scale and explicitly states open, non-proprietary data. A name query returned GeoJSON, including one Lady Bird Lake polygon:

```text
Base: https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query
Parameters: where=gnis_name like '%Lady Bird%' OR gnis_name = 'Town Lake'
            outFields=*; returnGeometry=true; outSR=4326; f=geojson
```

Verified identifiers: permanent ID **92669797**, GNIS **01376484**, reach **12090205006698**, object ID **1712904** in this service version. Attribute area: **1.962 km²**. Feature timestamp corresponds to March 19, 2013; service copyright text says refreshed October 2026. A service refresh is not proof the shoreline was resurveyed then. The name query returned 11 polygons nationally; geographic/ID filtering is essential.

Phase 1: retain only the verified lake, preserve original geometry and metadata, validate it, optionally simplify a display copy, and document tolerance. Draw metre-sized grids in a suitable projected CRS (UTM 14N), not by treating degrees as metres. Preserve islands/holes.

[OSM's copyright page](https://www.openstreetmap.org/copyright) confirms ODbL and attribution/share-alike requirements. No OSM lake geometry was fetched because the public-domain NHD route succeeded. OSM is a fallback, not an implicitly CC BY dataset; no live basemap tiles are proposed.

## 10. Sentinel-2, CyAN and PACE

### Sentinel-2 imagery

[Copernicus mission page](https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-2), [STAC documentation](https://documentation.dataspace.copernicus.eu/APIs/STAC.html), [attribution guidance](https://documentation.dataspace.copernicus.eu/FAQ.html).

The query below returned **12 catalogue items**, August 2019, tile 14RPU; the response had no next-page link:

```text
https://stac.dataspace.copernicus.eu/v1/search?collections=sentinel-2-l2a&bbox=-97.8,30.23,-97.7,30.30&datetime=2019-08-01T00:00:00Z/2019-08-31T23:59:59Z&limit=100
```

Catalogue access is anonymous; its full-product assets describe authentication. To avoid account dependence, I tested the [Earth Search public STAC mirror](https://earth-search.aws.element84.com/v1) using the same filter. It returned **24 items**, including processing alternatives. A concrete candidate is:

- Item: [`S2B_14RPU_20190813_0_L2A`](https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2B_14RPU_20190813_0_L2A).
- Date: 2019-08-13; catalogue tile-cloud cover 2.537677%. This is **not** the cloud percentage over Lady Bird Lake.
- Asset: [true-colour COG](https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/14/R/PU/2019/8/S2B_14RPU_20190813_0_L2A/TCI.tif), 10 m, 10,980×10,980 pixels. HTTP HEAD returned 200, byte-range support and 211,666,896 bytes; full image was not downloaded.

Use range-based reads to make a small local crop in Phase 1. Check cloud/shadow/nodata over the lake, retain processing baseline and scene ID, and document RGB stretch. L2A land surface reflectance is not automatically water-leaving Rrs. Attribution for a modified crop: “Contains modified Copernicus Sentinel data 2019”, with source/processor credits. Global historical coverage and all usable local scenes were not counted; only the stated one-month window was audited.

### CyAN Sentinel-3 suitability

The [EPA resource page](https://www.epa.gov/water-research/cyanobacteria-assessment-network-application-cyan-app) links a [published resolvable-lake list](https://ars.els-cdn.com/content/image/1-s2.0-S1364815218302482-mmc1.docx). I downloaded and inspected its table: **2,370 waterbody rows**. Lady Bird Lake and Texas Town Lake are absent; Lake Austin is present. This is the published 2018 list, not a claim to have audited every pixel of the current CyAN service.

The [CyAN guide](https://qed.epa.gov/cyanweb/assets/CYANWEB-USERS-GUIDE_09314022-Final.pdf) explains 300 m pixels and a 3×3-water-pixel context for a valid centre pixel. The lake's narrow geometry makes a local CyAN time series unsuitable as a promised feature. Exact mixed-pixel fractions should be computed from the frozen outline, with grid alignment disclosed. Current scene-mask testing was not performed; absence from this list is evidence of the resolution limitation, not proof that no 300 m pixel ever intersects water.

Recommendation: use the real outline to show mixed pixels and explain why a coloured large-lake satellite map cannot certify a nearshore mat hazard. No local CyAN observations will be fabricated.

### PACE

[OCI system paper](https://pace.oceansciences.org/docs/MeisterIEEE2024AsPublished.pdf) verifies approximately 1 km science sampling at nadir. [NASA's FAQ](https://pace.oceansciences.org/faqs.cgi) explicitly discusses inland-water pixels needing enough water area to avoid land mixtures. Use a nominal 1 km grid as an educational comparison; footprint size/shape varies with viewing geometry. No PACE lake dataset was downloaded or counted in this audit.

## What Phase 1 must record for every approved snapshot

Source and exact query; source author/agency; licence evidence; retrieval timestamp; observation span; source and cleaned counts; source-record IDs; checksums; units; spatial and temporal support; qualifiers; transforms; exclusions; gaps; refresh command; and review status. Each dataset gets its own README. Keep author-chosen simulations and coefficients in a separate manifest. Sources requiring unresolved permissions remain excluded, rather than acquiring an invented licence.
