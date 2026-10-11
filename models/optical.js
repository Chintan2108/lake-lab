/* Lake Lab — MIT. Forward equations adapted from Chintan B. Maniyar's
 * Water Optics Lab cf17a481bea2cbbcb98142274bfa6fede9df6529.
 * Default reference shapes are ORIGINAL ANALYTIC TEACHING APPROXIMATIONS,
 * not the sibling's Pope/Fry–Smith/Baker–Bricaud numerical reference tables.
 * See docs/optical-methods.md. No colour-matching data are included. */
const gaussian = (nm, center, width) => Math.exp(-0.5 * ((nm - center) / width) ** 2);
const shape = nm => gaussian(nm, 440, 45) + 0.5 * gaussian(nm, 675, 18);
export const opticalTable = Object.freeze(Array.from({ length: 81 }, (_, i) => {
  const nm = 400 + i * 5;
  return Object.freeze([nm, 0.005 + 0.03 * Math.exp((nm - 500) / 70), shape(nm) / shape(440)]);
}));
export const OPTICAL_TABLE = opticalTable;
export const opticalReference = Object.freeze({
  kind: 'simulated',
  label: 'Illustrative spectrum — analytic teaching shapes, not field measurements',
  exactSiblingReferenceTables: false,
  version: 'lake-lab-analytic-v1',
  omitted: ['bottom mats', 'depth and bottom reflectance', 'atmosphere', 'surface glint', 'fluorescence', 'toxins', 'sensor band responses']
});
/** Outputs absorption/backscatter in m^-1, Rrs in sr^-1, wavelength in nm.
 * Pigments: micrograms/litre; cdom: m^-1 at 440 nm; tss: g/m^3.
 * Optional suppliedTable must contain [wavelength, waterAbsorption, phyShape].
 * A caller supplying a table is responsible for its source and licence. */
export function simulate(input, suppliedTable = opticalTable) {
  const s = { chl: 5, pc: 0, cdom: 0.3, tss: 2, water: 'fresh', ...input };
  for (const [key, max] of Object.entries({ chl: 100, pc: 100, cdom: 5, tss: 100 })) {
    if (!Number.isFinite(s[key]) || s[key] < 0 || s[key] > max) throw new RangeError(`Invalid ${key}`);
  }
  if (!['fresh', 'marine'].includes(s.water)) throw new RangeError('Choose fresh or marine water');
  if (!Array.isArray(suppliedTable) || !suppliedTable.length) throw new RangeError('Reference table is empty');
  return suppliedTable.map(([wavelength, aw, phyShape]) => {
    if (![wavelength, aw, phyShape].every(Number.isFinite) || wavelength <= 0 || aw < 0 || phyShape < 0) throw new RangeError('Invalid optical reference row');
    const aph = s.chl * 0.04 * phyShape;
    const apc = s.pc * 0.007 * gaussian(wavelength, 620, 18);
    const ag = s.cdom * Math.exp(-0.018 * (wavelength - 440));
    const ased = 0.041 * s.tss * Math.exp(-0.0123 * (wavelength - 443));
    const bbw = (s.water === 'fresh' ? 0.00111 : 0.00144) * (wavelength / 500) ** -4.32;
    const bbph = 0.0006 * s.chl ** 0.8 * (550 / wavelength);
    const bbsed = 0.01 * s.tss * (550 / wavelength) ** 0.5;
    const a = aw + aph + apc + ag + ased;
    const bb = bbw + bbph + bbsed;
    const u = bb / (a + bb);
    const rrs = 0.089 * u + 0.1245 * u * u;
    const Rrs = 0.52 * rrs / (1 - 1.7 * rrs);
    return { wavelength, aw, phyShape, aph, apc, ag, ased, bbw, bbph, bbsed, a, bb, u, rrs, Rrs };
  });
}
