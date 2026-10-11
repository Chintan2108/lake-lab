# Original teaching simulations

Author: Chintan B. Maniyar / Lake Lab. Licence: CC BY 4.0. Code: MIT.
Source: scripts/make-simulations.py, version 1.0. Seed 6202019. These are NOT Lady Bird Lake measurements or validated forecasts.

forecast: 240 invented visits spaced five days apart starting 2020-01-01. Inputs: temperature °C, relative nutrient index 0–1, prior rain mm and relative flow 0–100. Synthetic outcomes use logistic probability with intercept -1.8, temperature coefficient .16, nutrient coefficient 2.8 then 1.4 after visit 159, flow -.025, rain .025, Gaussian latent noise SD .65, plus a Bernoulli draw. All choices are author assumptions for learning. The later change deliberately tests generalization. Browser training uses first N of first160 rows; last80 remain held out. They are generated independently of real lab results. Never merge with measured outcomes.

sensor-day: 24 invented hourly values. Light rises after06:00; delayed warmth after09:00; delayed pigment/particles after10:00. Sine pulses, amplitudes, lags and baseline values are author chosen. pH and DO rise together; a pigment signal lags in this specific scenario, not a general biological rule. RFU is instrument-dependent. No toxin concentration is simulated.

Refresh: python3 scripts/make-simulations.py. Deterministic seed; no network. Outputs stay separate from field data.
