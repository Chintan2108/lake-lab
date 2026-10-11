# Teaching models and limits

All coefficients below are author-chosen teaching assumptions, not fitted Lady Bird Lake parameters. No output establishes toxin presence or safety. Version 1, October 2026. Original content CC BY 4.0; code MIT. Frozen source provenance is in each data directory.

## Understand

Temperature support is exp(-((T−28)/12)²). Nutrient support is min(P/(P+0.03), N/(N+0.5)), with P and N in mg/L. Light is surface percent/100, multiplied by exp(-0.7×0.5) for the mat example. Retention is 1−0.8×flushing/100. Score is round(100×sqrt(temperature×nutrients×light×retention)). The 28°C optimum, 12°C width, half-saturation values, 0.7 attenuation, 0.5 m depth and 0.8 flushing coefficient are illustrative choices. The form teaches limiting factors; it is not a mechanistic biomass model. No species competition, nutrient cycling, attachment, resuspension, toxin genes, grazing, depth variability or elapsed growth time is represented.

Temperature presets use screened City shallow-water visit medians. These uneven visits are not seasonal climatology. All other preset controls are simulated. See data/derived/README.md for flags, exclusions and source row references. Ecological context: Perri et al. (2024), https://doi.org/10.3390/toxins16020091; these authors did not supply or validate the score coefficients.

## Predict

scripts/make-simulations.py is the exact reproducible generator (seed 6202019). All 240 rows are invented. Its seasonal temperature, nutrient, rain and flow relationships and Bernoulli outcome are pedagogical choices. The nutrient relationship weakens after row 160 to demonstrate a changing system. The last 80 rows are always held out; training uses only the first selected 40, 80, 120 or 160 rows. Training normalization uses training rows only. Logistic regression uses 700 full-batch gradient steps, learning rate 0.12 and L2 penalty 0.02 on non-intercept weights. Probability threshold is 0.5. The comparison model always predicts the training majority class. Neither model is calibrated to real toxins. Repeated experiments on a fixed test set can overfit model choices to that test set.

The real-data view is for exploring weather, downstream flow and toxin sample groups. Missing results and less-than values are never converted into safe/unsafe labels. Samples differ in medium, analyte and units. No real toxin classifier is trained.

## Identify

A 1-nearest-neighbour teaching classifier compares average R, G, B and mean horizontal red-channel contrast in 32×32 versions of frozen images, using Euclidean distance. It learns student labels, not toxin biology. Original specimens stay in one partition. The tiny training collection contains only cyanobacteria examples; green-alga and Microcystis originals are held out. This deliberate limitation is disclosed before training: performance on two images is not general accuracy. Changing a correct label can accidentally improve this tiny score. No neural-network library, photo upload or disease/safety detection is used. Source-identified local OTU plates remain unnamed pending expert taxonomic review.

## Decide

Six invented rounds use asymmetric teaching costs: warning costs 2, with 3 additional points for a false alarm; waiting during an event costs 12; sampling costs 3 before a second choice. Lower total cost is better under this game's chosen values. Sampling is instant and perfect in the game; real sampling is neither. Costs do not represent dollars or official policy. Forecast values and reports are invented. Teams should debate whose interests these chosen costs represent.

## Detect

The daily sensor sequence is invented and reproducible in scripts/make-simulations.py; its timing is not a universal early-warning rule. Real visit curves retain gaps, units, quality flags and source identifiers. The nominal satellite grid is drawn in UTM metres over a real historical outline; its alignment is arbitrary, not an actual orbital footprint. A true-colour image cannot locate toxins. See optical-methods.md for the spectrum.
