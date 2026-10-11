# Lake Lab

A static field notebook for middle-school lake detectives. First lake: Lady Bird Lake, Austin, Texas. Created by **Chintan B. Maniyar** for independent exploration by Nature Nexus and other teams.

Five interactive stations, 20 challenges, local notebook with settings and exports, frozen evidence, and transparent teaching models. Science content awaits researcher review.

## Run locally

No build step, npm install, account or API key is needed. From this repository folder:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. Serve over HTTP; opening index.html directly as a file will not load JSON/modules reliably. Stop the server with Ctrl+C. All runtime assets and data requests are local to the site. External source links are visited only when selected.

## GitHub Pages

Use this `lake-lab` folder as the repository root. Push the files to your GitHub repository. In Settings → Pages, choose “Deploy from a branch”, select your publishing branch and `/ (root)`. `.nojekyll` is included. No framework build or server routing is required; navigation uses URL hashes and all assets use relative URLs. Test the repository subpath before release.

Target repository: `Chintan2108/lake-lab`. Publish `main` / root. Expected Pages URL after enabling deployment: https://chintan2108.github.io/lake-lab/ . Prepared locally for manual upload; not deployed.

## Layout

- `app.js`, `index.html`, `styles/`: static shell and route rendering.
- `shared/`: guarded browser storage, UI helpers and real-outline SVG map.
- `stations/`: independently loaded station modules. Each station has its own module.
- `config/lady-bird-lake.json`: lake and enabled stations.
- `content/en/`: educational copy, glossary and station questions.
- `data/`: frozen observations, imagery, raw source responses, checksums, licences and per-dataset READMEs. Large CSVs are downloaded on demand, not loaded on startup.
- `scripts/`: manual keyless fetch and clean scripts; not run by the website.
- `tests/`: storage-failure and data-integrity checks.
- `docs/phase-0/`: full audit and initial plan. `docs/phase-1/`: implementation report.

## Refresh snapshots by hand

Core data need Python 3.9+ and the standard library:

```sh
python3 scripts/freeze.py all
```

Choose `austin`, `usgs`, `noaa`, `outline` or `perri` for one source. Existing source responses are reused. Move the dataset folder to a backup outside this repo before a deliberate refresh. Review source changes, licences, flags, output counts, manifest and science before publishing. Never let a failed request overwrite a good snapshot. The scripts record actual retrieval timestamps; old cached responses do not acquire a new date.

Optional imagery uses `python3 scripts/freeze-imagery.py commons`. Sentinel cropping also needs rasterio and Pillow (`python3 -m pip install rasterio Pillow` in your own environment), then `python3 scripts/freeze-imagery.py sentinel`. No image-processing or ML dependency ships to the browser.

## Check a change

```sh
python3 scripts/validate.py
node --test tests/*.test.mjs
python3 scripts/check-local.py
```

Then serve the site and check desktop, tablet and phone widths, keyboard navigation, glossary dialog, note save/edit/delete, reload persistence, JSON download and notebook printing. Do not put student data in a test fixture.

## Use this for another lake

1. Copy the lake config and update its ID, name, coordinates, time zone and agency links.
2. Freeze openly licensed observations and a real outline using a documented script. Add metadata to `data/manifest.json`; do not substitute invented local records.
3. Replace monitoring locations with source IDs, verified names and coordinates. Explain where context gauges sit relative to the lake.
4. Edit `content/en/` for local science, questions and glossary. Keep field evidence separate from teaching simulations.
5. Set any station's `enabled` to false to remove it from navigation and progress. Set its content and module paths when providing a new station.
6. Change the initial config path in `app.js`. Storage is scoped automatically using the lake ID, so use a distinct ID for each lake.
7. Review biology, toxin labels, seasons, measurement units, depth, missingness and model assumptions with a local expert. Leave `seasonalRanges` null until screened values exist.
8. Replace creator/repository credits if appropriate while retaining attribution and licences. Run checks and test your Pages subpath.

## Privacy and scope

No account, analytics, trackers, remote fonts, live map tiles or external runtime API calls. Notes and progress are stored only in localStorage with in-memory fallback if storage fails. Export before clearing browser data. The website host can keep ordinary access logs; Lake Lab adds no tracking. No photo uploads or personal details are requested.

The app is not a safety advisory or a toxin detector. Lady Bird Lake's local mat hazard is different from a broad open-water bloom. Missing results, below-limit tests, clear water and satellite colour do not establish safety. Use current City guidance for current conditions.

## Licence and sibling

Original code: [MIT](LICENSE). Original educational content and SVG illustrations: [CC BY 4.0](LICENSE-CONTENT). Data/images retain their own licences; see [third-party notices](THIRD-PARTY-NOTICES.md).

Related app: [Water Optics Lab](https://chintan2108.github.io/Water_Optics_Rrs_Simulator/) — Detect reuses its forward equations and PC term, with explicitly labelled analytic reference shapes. See [optical methods](docs/optical-methods.md).

## Derived data and review

After a source refresh, run `scripts/derive-station-data.py`, `scripts/project-map.py`, `scripts/make-simulations.py`, then `scripts/register-derived.py`. The optical and field-photo scripts have separate dependency requirements documented in their headers. Review every changed checksum and source licence. See [model methods](docs/methods.md).

[Local review report and scientific limitations](docs/review/PHASES-2-5.md).
