// Original teaching model v1. All coefficients are author-chosen, not fitted to lake data.
export const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
export function growth(s){
 const temperature=Math.exp(-(((s.temperature-28)/12)**2));
 const nutrients=Math.min(s.phosphorus/(s.phosphorus+0.03),s.nitrogen/(s.nitrogen+0.5));
 const bottomLight=s.light/100*Math.exp(-0.7*0.5);
 const light=s.mode==='mat'?bottomLight:s.light/100;
 const retention=1-0.8*s.flow/100;
 const score=Math.round(100*Math.sqrt(Math.max(0,temperature*nutrients*light*retention)));
 return {score,temperatureSupport:temperature,nutrientSupport:nutrients,lightSupport:light,bottomLight,retention};
}
