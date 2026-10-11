import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const load=async path=>import('data:text/javascript;base64,'+Buffer.from(await readFile(new URL(path,import.meta.url),'utf8')).toString('base64'));
const {simulate}=await load('../models/optical.js');
const {train,evaluate}=await load('../models/forecast.js');
test('PC changes absorption at 620 nm without double-counting scattering',()=>{const a=simulate({pc:0}),b=simulate({pc:50});assert.equal(b.length,81);for(let i=0;i<a.length;i++){assert.equal(a[i].bb,b[i].bb);assert.ok(Number.isFinite(b[i].Rrs));assert.ok(b[i].Rrs<=a[i].Rrs);}assert.equal(b.reduce((a,b)=>a.apc>b.apc?a:b).wavelength,620);assert.ok(Math.abs(b.find(x=>x.wavelength===620).apc-.35)<1e-12);});
test('normalization uses only provided training rows and confusion counts conserve test size',()=>{const rows=[{x:0,outcome:0},{x:1,outcome:0},{x:2,outcome:1},{x:3,outcome:1}];const m=train(rows,['x']);assert.equal(m.mean[0],1.5);assert.ok(m.predict({x:0})<m.predict({x:3}));const c=evaluate(m,[...rows,{x:1000,outcome:1}]);assert.equal(c.hits+c.misses+c.falseAlarms+c.correctQuiet,5);assert.equal(m.mean[0],1.5);});
test('optical invalid parameters fail explicitly',()=>assert.throws(()=>simulate({pc:NaN}),RangeError));

const {growth}=await load('../models/growth.js');
test('growth exports retain control units and distinguish support factors',()=>{const controls={temperature:28,phosphorus:.15,nitrogen:2,light:90,flow:5,mode:'mat'};const record={...controls,...growth(controls)};assert.equal(record.temperature,28);assert.equal(record.light,90);assert.equal(record.temperatureSupport,1);assert.ok(record.score>=55);assert.ok(growth({...controls,flow:100}).score<=record.score-20);});
