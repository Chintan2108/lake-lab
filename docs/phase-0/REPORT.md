# Lake Lab — Phase 0

Checked **9 October 2026**. This is a proposal for science review, not an implemented app. The new `lake-lab` folder is ready to become the repository root. No GitHub repository or deployment was created.

## Recommendation

Build Lake Lab as a small, static sibling of Water Optics Lab. Use real local records for exploring evidence and seasonal context, a clearly labelled teaching model for growth, and a separate simulated training mode for forecasting. Make bottom-growing mats the default Lady Bird Lake story.

The source audit found more local environmental data than expected, but much less verified toxin-training data. Austin's HAB project has 12,099 measurement rows across several watersheds. Filtering to Lady Bird Lake leaves **8,212 rows across 23 site IDs and 481 site/calendar-day combinations**, from August 2019 to October 2026. These are not 8,212 independent bloom outcomes. In that subset, the toxin rows identified in the parameter inventory all fall in **August–November 2019**. The complete findings, query scope and limitations are in [Data availability](DATA-AVAILABILITY.md).

## 1. What the sibling repository actually uses

I inspected the public repository tree at commit `cf17a481bea2cbbcb98142274bfa6fede9df6529`, its application/model source, HTML, CSS, data-source notes and deployment README. I also opened the live app and inspected its rendered design.

**The current repository is not JSX.** It uses plain JavaScript, HTML and CSS, plus Chart.js 4.4.8. There is no React dependency, package manifest, JSX compiler, Vite configuration or application build pipeline in the inspected tree. GitHub Pages serves the repository root or `docs/` directly from a branch, with `.nojekyll` and relative asset paths. Optional maintenance uses Python to embed reference tables; model regression checks use Node's built-in test runner. [Repository](https://github.com/Chintan2108/Water_Optics_Rrs_Simulator), [deployment and model README](https://github.com/Chintan2108/Water_Optics_Rrs_Simulator/blob/main/README.md).

I recommend the **same buildless stack and branch-based Pages deployment**. Split JavaScript into station and shared modules, use locally bundled Chart.js, and draw maps/illustrations with SVG or canvas. Use hash navigation so deep links work on GitHub Pages without server routing. Serve locally over HTTP for config/content loading. This changes the sibling's CDN-first Chart.js loading to local-only loading, satisfying Lake Lab's privacy and static-snapshot requirements. No runtime external fonts, map tiles, API requests, embedded videos, analytics or image hosts.

If JSX is an intentional requirement, React plus Vite would be a different stack, rather than a faithful copy of this repository. Please choose explicitly before Phase 1.

### Optical model to carry over

Preserve the numerical forward model as a separate, tested module, pinned to the inspected reference commit:

```text
a = aw + aph + apc + acdom + ased
bb = bbw + bbph + bbsed
u = bb / (a + bb)
rrs = 0.089u + 0.1245u²
Rrs = 0.52rrs / (1 − 1.7rrs)
apc(λ) = 0.007 PC exp[−0.5((λ − 620) / 18)²]
```

The PC coefficient is literature-used; the Gaussian width of 18 nm is an author-chosen approximation. Keep the original source and assumption distinctions. PC adds absorption at fixed total chlorophyll; it must not add a second population of scattering cells. Use two main sliders, chlorophyll-a and phycocyanin, with fixed, disclosed freshwater/CDOM/sediment settings. An optional third sediment control can come later. [Reference implementation](https://github.com/Chintan2108/Water_Optics_Rrs_Simulator/blob/main/app.js), [coefficient and table provenance](https://github.com/Chintan2108/Water_Optics_Rrs_Simulator/blob/main/data/SOURCES.md).

The model describes homogeneous, optically deep water. It does not simulate a benthic mat, lake-bottom reflectance, a satellite's full spectral response, atmospheric correction, adjacency effects or toxins. The spectrum panel will say **“Illustrative, not field measurements”** and show these omissions. A short prompt will connect that limitation to Lady Bird Lake. CSV export will include every wavelength, model term, setting and model version.

**Licensing finding:** no project-wide licence file was present in the inspected reference tree. Chart.js has its own MIT notice; the CIE colour tables have CC BY-SA 4.0 attribution and adaptation terms. OMLC optical tables have source citations in the sibling but no explicit reuse licence recorded there. Do not relabel third-party data as MIT or CC BY. Confirm the licence for the creator-owned reused code/content; retain asset-specific notices and verify unresolved table provenance before distributing them. CIE colour rendering is optional for Lake Lab's spectrum-only panel.

## 2. Learning and visual direction

Keep the sibling's deep navy, water teal, light backgrounds, rounded panels and inspectable science. Make Lake Lab feel like a field notebook: a winding lake map, five illustrated station signs, large controls, short instruction cards, and a friendly “What did you notice?” prompt. Use locally authored SVG illustrations, not generated images pretending to be micrographs.

Every station follows the same sequence: **Try it → Take a challenge → Explain your evidence → Save a finding.** Let students enter any station immediately. Each offers 3–5 progressively harder challenges and an optional hint. Earn local “Explorer”, “Evidence finder” and “Question builder” stamps through evidence and reflection, not speed. Saved settings and deterministic challenge seeds support repeat visits without accounts or daily streak pressure.

Every station includes the requested free-play sandbox, challenge set, plain-language “How this works” drawer, notebook action and a project question. Examples of project questions, to be reviewed:

| Station | Open question for the team's own solution |
|---|---|
| Understand | Which lake conditions would your idea need to notice, and which could it miss? |
| Identify | How could your team check an identification when a photo is unclear? |
| Detect | What could your sensor or satellite miss near the shore or lake bottom? |
| Predict | What evidence would convince you that your forecast works on a new season? |
| Decide | Who needs a warning, and what extra evidence would change your decision? |

Charts have labels, shapes/dashes, readable data tables and downloads. Glossary terms work by keyboard and tap, not hover alone. Plan for 44-pixel touch targets, visible focus, reduced motion, plain-language validation, and colour-independent feedback. Formal WCAG AA contrast and assistive-technology checks remain implementation work.

## 3. Science decisions and uncertainties for review

- **Local default:** a narrow, dammed river reach between Tom Miller and Longhorn dams, with benthic/mat proliferation as the central hazard. Floating material may have grown on the bottom. General planktonic bloom science remains available through the mode toggle. Austin's current description supports this distinction. [City guidance](https://www.austintexas.gov/watershed-protection/algae-austins-waterways).
- **Growth is not toxicity:** use a “growth conditions” meter, with an explicit note that it cannot tell whether toxins are present. A numeric teaching score must not look like a validated probability of a toxic event.
- **Mat light:** a bottom-mat model needs light at the bottom, not just sunshine above the water. A disclosed fixed shallow depth and water clarity are adequate for the first teaching model; do not silently apply a surface-bloom equation to mats. Temperature, flow and nutrient effects are illustrative, not fitted causal estimates.
- **Nutrients:** preserve distinctions between total phosphorus, orthophosphorus, nitrate/nitrite and total nitrogen. Do not turn laboratory total concentrations directly into “available food” without stating the approximation. Nitrogen fixation is not a universal cyanobacterial ability.
- **2019 evidence:** the Perri study supports dihydroanatoxin-a in mats and identifies mixed communities, including filamentous taxa. Use cautious genus-level labels; a taxon that can produce toxins is not proof that an image or isolate is toxic. Review the OTU-to-genus mapping and the paper's naming/spelling before making student cards. [Perri et al., 2024](https://doi.org/10.3390/toxins16020091), [open dataset](https://data.mendeley.com/datasets/f94329byhk/2).
- **Sampling gaps:** “not sampled”, “sampled but not tested”, “below reporting limit” and “detected” must be different states. Neither a missing visit nor a negative water sample is a safe-lake label. Austin describes sampling conditional on seeing blue-green algae, which creates selection bias. Dates of collection and availability of lab results are different.
- **Flow context:** USGS 08158000 is downstream of the lake. It is not a direct nearshore current measurement or a measurement of Tom Miller Dam releases. Preserve that distinction in charts and model features.
- **Satellite tradeoff:** Sentinel-2 offers small visible pixels but no dedicated narrow 620 nm band. Sentinel-3 OLCI has a 620 nm band but coarse pixels. PACE OCI offers rich spectra with about 1 km sampling at nadir. Thus spatial and spectral resolution must be taught separately. [Sentinel-2 bands](https://sentinels.copernicus.eu/es/web/success-stories/-/a-new-vision-for-earth-the-sentinel-2-mission), [PACE instrument documentation](https://pace.oceansciences.org/docs/MeisterIEEE2024AsPublished.pdf).
- **Look-alikes:** green algae, duckweed and pollen are not cyanobacteria, but their presence does not establish that nearby water is safe. Do not label field photographs “safe”. Field-photo questions need an “uncertain / more evidence needed” option.

Specific unresolved issues: mapping the requested Vic Mathias/Auditorium Shores label to a verified monitoring site; coverage and format of post-2019 toxin results; City sample/replicate conventions; microscopy OTU names; whether any archived local sub-daily multiparameter record is suitable; and licensing for LCRA data and the reused optical reference tables.

## 4. What must be simulated, or separated from measurements

| Feature | Proposed treatment and reason |
|---|---|
| Grow a bloom | Teaching simulation. No locally validated four-slider growth/toxin model was established. Seasonal presets can summarize screened local observations, but the response remains simulated. |
| Sensor changes through a day | Real downstream discharge; real discrete local chemistry where available. Use a separately labelled simulated day for the coordinated pH/oxygen/temperature/PC response unless a suitable continuous record is verified. Never interpolate seasonal visits into a “measured day”. |
| Phycocyanin sensor | No phycocyanin-named parameter was found in the audited Lady Bird Lake parameter inventory. Use a simulation initially; RFU is instrument-dependent and is not interchangeable with µg/L. A public other-lake example is an optional future addition, not yet verified. |
| Spectrum | Reused teaching forward model. Measured reference absorption tables do not make its output a measured lake spectrum. |
| Pixel grid | Computed geometric overlay on a real outline and, if suitable, a real image. Label “resolution demonstration”; arbitrary grid alignment is not an actual overpass footprint or cyanobacteria measurement. |
| Predict: real mode | Explore historical evidence and reveal the next available tested sample result, including unknowns. Do not claim a current operational forecast. |
| Predict: train mode | Seeded simulated visits and outcomes. Teach feature choice, training history, misses and false alarms. The real toxin record verified so far is small, seasonally clustered and selectively sampled. |
| Identify classifier | Real curated images; a real in-browser nearest-neighbour algorithm using disclosed, simple visual features. Its accuracy is on the small teaching collection only. No toxin detection claim. |
| Decide | Invented rounds, hidden outcomes and point costs, all labelled simulated. Calibrate educational tradeoffs through review; scores are not estimates of money, illness or agency policy. |

Use **Measured**, **Derived from public data**, **Simulated**, **Real image**, and **Illustration** badges as applicable. Keep the requested real/simulated distinction prominent, with the finer source type visible nearby. NASA POWER is a public satellite/model-derived estimate, not a thermometer or sunlight sensor in Lady Bird Lake.

### Forecasting and image-learning safeguards

Use a small, explainable logistic regression or shallow decision tree, with no ML library initially. Compare with an “always predict the common class” baseline. Split data chronologically, grouping all samples from a visit and preferably testing on a later season. Fit scaling/imputation only on training data. Features must precede the target visit; do not give the model the target's toxin test or observations recorded after the prediction. Display actual test counts and confusion counts beside percentages. Low data counts, class imbalance and distribution changes are lessons, not obstacles to hide.

For Identify, use simple colour/texture features and nearest neighbours on a curated subset, reveal the neighbour images, and allow deliberate mislabelling. Keep microscope and field-photo tasks separate so the classifier cannot win by learning image type alone. Hold out entire original photographs/specimens; crops and augmented copies stay together. If the verified collection is too small, say so and make labelling/feature comparison the activity rather than inventing impressive accuracy. No heavier library is proposed; any later pretrained image model requires a measured bundle/weights cost before adoption.

## 5. Proposed repository structure

The following tree is a proposal; only the planning documents and audit evidence currently exist.

```text
lake-lab/
  index.html                  # Static entry point
  .nojekyll
  app.js                      # Navigation and station registration
  styles/                     # Shared, station, responsive and print CSS
  stations/
    understand/               # Each module: mount, restore, reset, export, cleanup
    identify/
    detect/
    predict/
    decide/
  shared/                     # Charts/tables, glossary, badges, notebook, storage
  models/                     # Growth, copied optical core, classifier, forecast
  config/
    lake.schema.json
    lady-bird-lake.json
  content/en/
    common.json
    glossary.json
    understand.json           # Copy, challenges, hints, captions, questions
    identify.json
    detect.json
    predict.json
    decide.json
    coach-notes.md
    adapt-your-lake.md
  assets/                     # Local images, original SVGs, image manifest
  vendor/                     # Pinned Chart.js and third-party notices
  data/
    manifest.json
    austin-water-quality/     # CSV/JSON plus README and source metadata
    usgs-flow/
    noaa-weather/
    nasa-power/               # If reuse terms verified
    perri-2019/
    lake-outline/
    sentinel-2/
    simulations/              # Explicitly separate, seeded and versioned
  scripts/                    # One fetch/clean entry per approved dataset
  tests/                      # Models, provenance, storage failure, leakage checks
  docs/                       # Methods, coefficient registry, phase reports
  README.md
  CONTRIBUTING.md
  LICENSE                     # MIT for original code
  LICENSE-CONTENT              # CC BY 4.0 for original content
  THIRD-PARTY-NOTICES.md
```

No build command is needed to publish this proposal. Each later phase will run model/data validation as relevant, serve the static root locally, and receive desktop/phone browser checks. Relative paths and the Pages repository subpath will be tested before deployment.

### Lake configuration schema proposal

| Field | Type and contract |
|---|---|
| `schemaVersion`, `id`, `name` | Version number and stable identifiers. |
| `center`, `bounds`, `timeZone` | WGS84 longitude/latitude centre and bounds; `America/Chicago` for lake observations. This differs from the researcher's device timezone. |
| `outline` | Local GeoJSON path, provenance ID and geometry version. |
| `hydrology` | Inflow/outflow dam names and links; explicit contextual-gauge relationships. |
| `bloom` | Default `benthic-mats`; supported modes; content keys for local caveats. |
| `monitoringSites[]` | Source agency/site ID, exact source name, reviewed display name, coordinates, role, validity dates and provenance ID. Do not silently merge aliases. |
| `stations` | Object with `understand`, `identify`, `detect`, `predict`, `decide`, each containing `enabled` and content/data references. Disabled modules disappear from navigation and progress calculations. |
| `seasonalRanges` | Per parameter: unit, min/max or quantiles, season, source data ID, site/depth filters, valid sample count and derivation. Unverified values remain null, never invented local ranges. |
| `datasets` | IDs resolving to local manifest entries, paths and source-type badges. |
| `models` | Versioned teaching model IDs, assumptions and fixed settings, with review status. |
| `prediction` | Target definition, sample medium, label policy, feature lookback, split policy, minimum-data rule and whether real training is enabled. Initially real training disabled. |
| `satellites[]` | Sensor, nominal pixel size, spectral caveats and overlay type. |
| `agencyLinks` | Official current-guidance and data links, opened only by user choice. |
| `content` | Locale and local content paths. |
| `credits` | Creator, repository URL once established, sibling URL and licence references. |

The source manifest should retain URL, author/agency, licence and licence URL, retrieval timestamp, observation period, units, spatial support, checksum, source row count, cleaned row count, exclusions, script version and known gaps. Images additionally need original file ID, author, capture date if known, crop/resize details, specimen group ID and alt text. A numeric observation retains sample medium, depth, method, qualifier, detection limit, QC flag and source record ID.

### Storage and notebook

Store only device-local progress, settings and notebook entries. Wrap reads, parsing, writes and removal in `try/catch`, validate schema versions, and fall back to in-memory state. Explain when work cannot be saved. Provide export before reset; notebooks must remain useful without storage. A note includes student-edited text, station, settings, source IDs, data/model versions and an explicit simulated/measured label. Printable output and JSON backup remain local downloads. Do not request students' names, locations or uploaded photos.

## 6. Proposed Phase 1 data selection

1. City water-quality observations for **2016–2025**, with separate HAB and routine-monitoring subsets; preserve the 2019 toxin record and its qualifiers. Treat 2026 as an optional, clearly partial extension.
2. USGS 08158000 daily discharge for the same window, with a short real sub-daily flow example only after its availability is checked. Include gauge-height context if useful, not as an in-lake level.
3. NOAA Camp Mabry daily temperature and precipitation for the same window.
4. Perri v2 micrographs and useful processed supporting files, preserving the dataset licence and reviewing specimen labels.
5. USGS NHD Lady Bird Lake polygon and verified monitoring-site coordinates.
6. One cloud-checked Sentinel-2 true-colour crop through anonymous COG access; store a small local crop and metadata, not the full 212 MB candidate image.
7. The individually verified open image candidates listed in the data report, plus more independent specimens if needed for a meaningful classifier.

NASA POWER is an optional derived sunlight source pending final reuse-policy documentation. LCRA and additional non-USGS WQP records remain conditional on clear redistribution terms. Do not block the core app on those extras. Fetch-and-clean scripts and per-dataset READMEs belong to Phase 1 after this selection is reviewed.

## 7. Verification and questions

Verified repository source and live appearance; opened every candidate source family; tested public API/metadata routes; computed scoped record counts; read the study; inspected individual image licences; checked the EPA lake list; verified anonymous access to a Sentinel-2 true-colour asset. Evidence is in the adjacent folder.

**Not yet verified:** cleaned scientific ranges, complete post-2019 toxin outcomes, temporal joins, photo identification quality, lake-specific cloud cover, model validity, final licence clearance for conditional assets, or app accessibility. No app exists yet, so a site build, local run and desktop/phone QA are **not applicable in Phase 0**. They begin in Phase 1, consistent with “no app code” here.

Questions before Phase 1:

1. Shall we match the inspected **plain JavaScript/buildless stack**, or did you intend a different JSX version of Water Optics Lab?
2. Can the creator-owned Water Optics Lab code reused here be released under **MIT**, with original Lake Lab content under **CC BY 4.0** and separately preserved third-party licences? The inspected sibling has no project-wide licence.
3. Do you approve the core data selection above and **real-data exploration plus simulated forecast training** as the initial approach? If you have a public link to a fuller post-2019 toxin-results table, it could change that decision.

Optional science feedback: preferred genus names for local mats; treatment of the paper's OTU taxonomy; terminology for the growth meter; whether 2016–2025 is the right teaching period. Default language will be English at approximately grade 6, with SI units and optional temperature conversion.
