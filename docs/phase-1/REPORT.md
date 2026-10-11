# Phase 1 handoff

Implemented 9–10 October 2026 (retrieval timestamps use UTC). Phase 2 has not started.

## What is ready

- Buildless HTML/CSS/JavaScript app, matching the inspected Water Optics setup. No runtime libraries or external services. Relative paths and hash navigation support GitHub Pages.
- Field-notebook home, actual NHD lake outline and selected verified City locations, local mat-science explanation and five clearly marked station previews.
- Each preview has an open project question, methods drawer, notebook action and persistent “explored” progress. No experiment is presented as finished.
- Searchable 23-term glossary; keyboard/tap definitions in a modal dialog.
- Device-local notebook: create, edit, delete, reset, JSON export, standalone printable HTML export and browser print action. Storage failures fall back to memory with an export warning. No names or uploads requested.
- Seven frozen source collections, downloadable CSV/GeoJSON/images and provenance, plus a source gallery with author/licence/source credits.
- One lake config, JSON educational copy, station module paths and switches, schema, starter adaptation instructions, MIT code and CC BY 4.0 original-content notices.
- Local Git repository. No remote repository, push or deployment performed.

## Frozen evidence

| Collection | Snapshot |
|---|---|
| Austin water quality | 39,001 measurement rows, 2016-02-17–2025-12-16; 57 watershed site IDs. The watershed includes tributaries, different sample media and QC samples, not just lake water. |
| Austin HAB subset | 7,334 rows; 447 site/calendar days. Toxin subset: 545 measurement rows, all in 2019. Subsets preserve source qualifiers and IDs. |
| USGS daily discharge | 3,652 daily means, 2016–2025. Missing 2017-01-26 remains missing. Gauge is downstream of Longhorn Dam. |
| NOAA daily weather | 3,653 dates, 2016–2025. Camp Mabry minimum/maximum air temperature and rain, with source attribute flags. |
| NHD shoreline | One verified historical Lady Bird Lake feature, preserving original geometry and holes. |
| Perri microscopy | Three unchanged local research plates, CC BY 4.0; publisher hashes verified. |
| Comparison images | Four unchanged images: Microcystis, Dolichospermum, Spirogyra and duckweed, with individual licences. |
| Sentinel-2 | 2019-08-13 native 10 m true-colour crop, 1,066 × 765 pixels. GeoTIFF and JPEG; no extra stretch. Visual inspection found no obvious cloud over the lake, but no quantitative cloud/shadow mask was applied. |

Counts are observation/measurement or image counts, not independent toxicity labels. Raw source responses, exact queries, actual retrieval timestamps and SHA-256 checksums are retained. CSV cleaning is deliberately conservative: scope and separate records, preserve flags/units/depth/method/medium, inventory and validate keys. Numerical screening and seasonal derivations await station-specific science review; no local seasonal ranges were invented.

## Verification

- Offline validator passed: seven manifests, all listed output hashes, observation window, unique City source IDs, disjoint HAB/other subsets, preserved `<` toxin qualifiers, daily date uniqueness, known flow gap, correct NHD identity, local entry assets and configuration/module paths.
- Five Node storage tests passed: blocked access, quota failure, corrupted/unsupported saved state, reload/provenance/reset isolation and malformed-entry filtering.
- Served over local HTTP and inspected in the Codex browser at requested desktop, tablet and phone sizes. Effective CSS widths (browser zoom applied) were 1,600, 853, 433 and 355 px. No horizontal overflow in inspected home/source views. Screenshots: [desktop](desktop.jpg), [phone](phone.jpg).
- Browser-tested glossary search (`pixel` → two entries), tap definition, Escape dismissal, keyboard skip link, station navigation, station note creation, notebook edit, reload persistence, JSON download and reset. Disposable test notes were removed.
- Downloaded printable HTML successfully; verified both test notes and source-snapshot context. [Disposable export fixture](qa-notebook.html). The embedded browser print action produced a control timeout, so operating-system print/PDF output is **not verified**. The standalone printable download is the reliable fallback and can be printed in a standard browser.
- Browser console had no errors/warnings in the inspected station/source flow. Runtime connections are restricted to the site origin by Content Security Policy; no external fonts, scripts or data services are referenced at startup.
- Core text/background contrast pairs measured 5.68:1 or higher (body text, muted text, buttons, notices and badges). Full WCAG, assistive-technology and device coverage are reserved for Phase 5, not claimed here.
- Local documentation links checked. No build step exists, so the static-file checks are the build verification.

## What remains uncertain or deferred

- Pollen image download was rate-limited by Wikimedia. It is not bundled; no replacement with unclear rights was used.
- LCRA and NASA POWER reuse terms remain unresolved; non-federal WQP rights/deduplication remain unresolved. They are excluded from app datasets. LCRA audit inventory was moved outside the public repository.
- Local microscope OTU-to-genus assignments need researcher review. The gallery retains source labels. No classifier has been trained.
- A complete public post-2019 toxin outcome table and a local phycocyanin time series have not been verified. Forecast training will be explicitly simulated as approved.
- No growth/optical/forecast/decision simulation is implemented yet. Phase 1 uses real sources plus a labelled original mat illustration and student reflections.
- Footer GitHub source link awaits an actual repository URL; it currently links to the local source/setup README. No repository URL was invented.
- Coach/adaptation pages are short starter notes, not the final Phase 5 guides.

## View and next review

From the `lake-lab` directory, run:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. If the preview server is already running, use that address directly. All progress belongs to this browser origin; another port/device has separate storage.

Please review the visual tone and local-science wording. The next authorized phase can add Understand and Predict, including clearly labelled simulations and documented model assumptions.
