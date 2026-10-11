export const KEY='lake-lab:lady-bird-lake:v1';
export const fresh=()=>({version:1,notes:[],visited:[],activities:{},completed:{}});
export function validate(value){
 if(!value||value.version!==1||!Array.isArray(value.notes)||!Array.isArray(value.visited))throw Error('Unsupported notebook');
 return {version:1,activities:value.activities&&typeof value.activities==='object'?value.activities:{},completed:value.completed&&typeof value.completed==='object'?value.completed:{},notes:value.notes.filter(n=>n&&typeof n.id==='string'&&typeof n.text==='string').map(n=>({id:n.id,text:n.text.slice(0,10000),station:typeof n.station==='string'?n.station:'home',created:typeof n.created==='string'?n.created:'',kind:typeof n.kind==='string'?n.kind:'Student reflection',sources:Array.isArray(n.sources)?n.sources.filter(x=>typeof x==='string'):[],settings:n.settings&&typeof n.settings==='object'?n.settings:{},modelVersion:typeof n.modelVersion==='string'?n.modelVersion:'',snapshot:typeof n.snapshot==='string'?n.snapshot:''})),visited:value.visited.filter(x=>typeof x==='string')};
}
export function createStore(getStorage=()=>globalThis.localStorage,onFailure=()=>{},key=KEY){
 let state=fresh();let available=true;
 try{const raw=getStorage().getItem(key);if(raw)state=validate(JSON.parse(raw));}catch{available=false;onFailure();}
 const persist=()=>{try{getStorage().setItem(key,JSON.stringify(state));available=true;}catch{available=false;onFailure();}};
 return {get:()=>state,available:()=>available,save(next){state=validate(next);persist();return state;},reset(){state=fresh();try{getStorage().removeItem(key);}catch{available=false;onFailure();}return state;}};
}
