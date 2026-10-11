import {esc} from './ui.js';
export function lakeMap(geo,sites,copy,name){
 const rings=geo.features.flatMap(f=>f.geometry.type==='Polygon'?f.geometry.coordinates:f.geometry.coordinates.flat());
 const points=rings.flat();const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
 const scale=Math.min(560/((maxX-minX)*Math.cos(30.26*Math.PI/180)),225/(maxY-minY));
 const width=(maxX-minX)*Math.cos(30.26*Math.PI/180)*scale;
 const xy=([x,y])=>[45+(560-width)/2+(x-minX)*Math.cos(30.26*Math.PI/180)*scale,42+(maxY-y)*scale];
 const d=rings.map(r=>r.map((p,i)=>`${i?'L':'M'}${xy(p).map(n=>n.toFixed(2)).join(',')}`).join(' ')+'Z').join(' ');
 return `<svg class="lake-map" viewBox="0 0 650 335" role="img" aria-labelledby="map-title map-desc"><title id="map-title">${esc(copy.title.replace('{lake}',name))}</title><desc id="map-desc">${esc(copy.description)}</desc><defs><pattern id="mapdots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#c9d9cc"/></pattern></defs><rect width="650" height="335" fill="url(#mapdots)"/><path d="${d}" fill="#74b3aa" stroke="#155d54" stroke-width="1.5" fill-rule="evenodd"/>${sites.map((s,i)=>{const[x,y]=xy(s.coordinates);return `<circle cx="${x}" cy="${y}" r="6" fill="#f7c568" stroke="#173c3a" stroke-width="2"/><path d="M${x} ${y+8}v${i===0?25:30}" stroke="#173c3a"/><text x="${x}" y="${y+(i===0?49:55)}" text-anchor="middle">${esc(s.shortName)}</text>`}).join('')}<path d="M606 63V30l-5 10m5-10 5 10" fill="none" stroke="#173c3a" stroke-width="2"/><text x="606" y="22" text-anchor="middle">N</text><text x="31" y="316" class="map-small">${esc(copy.region)}</text></svg>`;
}
