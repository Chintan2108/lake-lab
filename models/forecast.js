// Browser logistic regression: original implementation; no ML dependency.
export const sigmoid=x=>1/(1+Math.exp(-Math.max(-30,Math.min(30,x))));
export function train(rows,features,iterations=700){
 if(!rows.length)throw Error('Training rows required');
 const mean=features.map(f=>rows.reduce((s,r)=>s+r[f],0)/rows.length);
 const scale=features.map((f,j)=>Math.sqrt(rows.reduce((s,r)=>s+(r[f]-mean[j])**2,0)/rows.length)||1);
 const weights=Array(features.length+1).fill(0);
 for(let k=0;k<iterations;k++){
  const gradients=weights.map(()=>0);
  rows.forEach(r=>{const x=[1,...features.map((f,j)=>(r[f]-mean[j])/scale[j])];const p=sigmoid(x.reduce((s,v,j)=>s+v*weights[j],0));x.forEach((v,j)=>gradients[j]+=(p-r.outcome)*v/rows.length);});
  weights.forEach((w,j)=>weights[j]-=.12*(gradients[j]+(j?.02*w:0)));
 }
 return {features,mean,scale,weights,predict(r){return sigmoid(weights[0]+features.reduce((s,f,j)=>s+weights[j+1]*(r[f]-mean[j])/scale[j],0));}};
}
export function evaluate(model,rows,threshold=.5){const c={hits:0,misses:0,falseAlarms:0,correctQuiet:0};rows.forEach(r=>{const yes=model.predict(r)>=threshold;c[yes?(r.outcome?'hits':'falseAlarms'):(r.outcome?'misses':'correctQuiet')]++;});return {...c,total:rows.length,accuracy:(c.hits+c.correctQuiet)/rows.length};}
export function baseline(trainRows,testRows){const majority=trainRows.reduce((s,r)=>s+r.outcome,0)>=trainRows.length/2?1:0;return {prediction:majority,correct:testRows.filter(r=>r.outcome===majority).length,total:testRows.length};}
