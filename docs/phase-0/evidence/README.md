# Phase 0 evidence

Checked 2026-10-09. These are small **research-audit metadata/aggregate responses**, not approved, cleaned app datasets. The main report distinguishes tested observations, published metadata and unresolved items. No local data here should be shown as a current lake-safety assessment.

- `request-manifest.json`: source URLs, audit date, transformation notes and SHA-256 checksums for retained responses.
- `audit-summary.json`: computed counts for probes, satellite catalogue items and NHD identifiers. Original sample data used to calculate these summaries remain temporary research material; fetch scripts and a full reproducible production snapshot are Phase 1 work.
- `austin-*.json`: scoped counts and inventories from City dataset 5tye-7ray. Licence metadata is retained separately. Counts precede cleaning and are not independent event counts.
- `usgs-*.txt`: series inventories with parameter, statistic, location, period and source count. These are metadata, not time-series observations.
- `mendeley-*.json`: metadata for the three micrographs and the Statistics folder. Images/documents are not copied here. The v2 dataset is CC BY 4.0; authors are listed in the availability report.
- `lcra-sites.json`: public site-name inventory inspected for feasibility only. LCRA observation redistribution rights are unresolved. This metadata is not an approved app asset and must be reviewed or removed before publication.

The source files reflect the provider's own units, labels, formatting and timestamps. Some APIs return JSON encoded inside a JSON string. Preserve this evidence independently of future cleaning. Current provider counts may change after the audit date.

See [Data availability](../DATA-AVAILABILITY.md) for full source citations and exact probe routes; see [Phase 0 report](../REPORT.md) for implementation decisions.

Phase 1 note: the LCRA site-inventory JSON was moved out of this repository because redistribution terms remain unresolved. Its verified findings remain described in the audit; it is not app data.
