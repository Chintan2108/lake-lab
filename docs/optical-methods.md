# Optical model and numerical-reference distinction

Forward equations are reused from Water Optics Lab, revision cf17a481bea2cbbcb98142274bfa6fede9df6529, app.js: https://github.com/Chintan2108/Water_Optics_Rrs_Simulator/blob/cf17a481bea2cbbcb98142274bfa6fede9df6529/app.js . Consult the sibling SOURCES.md for its literature provenance. Lake Lab retains the sibling's empirical coefficient choices; these are not Lady Bird Lake calibrations.

At wavelength λ (nm), aph=0.04×chl×shape(λ); apc=0.007×pc×exp(-0.5((λ−620)/18)²); ag=CDOM440×exp(-0.018(λ−440)); ased=0.041×TSS×exp(-0.0123(λ−443)). Absorptions are m⁻¹; chl and pc are µg/L, TSS g/m³. Total absorption adds water and these four terms.

Backscatter: bbw=0.00111×(λ/500)^−4.32 for fresh water (marine alternative 0.00144); bbph=0.0006×chl^0.8×550/λ; bbsed=0.01×TSS×(550/λ)^0.5. PC does not add scattering biomass. u=bb/(a+bb); rrs=0.089u+0.1245u²; Rrs=0.52rrs/(1−1.7rrs). The app fixes CDOM440=0.3 m⁻¹ and TSS=2 g/m³, with fresh water.

**Numerical spectra differ from the sibling.** Redistribution permission for the sibling's third-party numerical water/phytoplankton reference tables was not verified. Lake Lab instead uses original, explicitly illustrative analytic inputs: aw=0.005+0.03×exp((λ−500)/70); shape is [exp(-0.5((λ−440)/45)²)+0.5exp(-0.5((λ−675)/18)²)] normalized to 1 at 440 nm. These are not Pope/Fry or Bricaud measurements, fits, or claimed replacements for research. Output is sampled every 5 nm from 400–800 nm. The 620 nm phycocyanin absorption term is retained exactly.

Omitted: bottom reflectance and mat optics, depth, atmosphere, adjacency, sensor band integration, fluorescence, viewing geometry, pigment packaging, species-specific spectra and toxins. The spectral panel explains general pigment optics, not satellite detection of local benthic mats. Original analytic reference data are CC BY 4.0; original model implementation is MIT. The drawer and exported CSV identify the analytic model version.
