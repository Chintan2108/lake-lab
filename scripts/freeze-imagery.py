#!/usr/bin/env python3
"""Optional imagery snapshot. Requires rasterio and Pillow ONLY to refresh satellite crop.
Run: python3 scripts/freeze-imagery.py [commons|sentinel|all]
Never used by the website. Existing downloaded files are cached.
"""
import sys,json,math,urllib.parse
from pathlib import Path
from freeze import ROOT,DATA,get,save,sha,manifest
from datetime import datetime,timezone

def finish(id,title,agency,lic,licurl,source,kind,files,rows,period,cleaning,limits):
 folder=DATA/id
 requests=[json.loads(p.read_text()) for p in folder.glob('*.request.json')]
 meta={'id':id,'title':title,'agency':agency,'license':lic,'licenseUrl':licurl,'sourceUrl':source,'kind':kind,'recordCount':rows,'countUnit':'images','period':period,'retrievedAt':max([r['retrievedAt'] for r in requests] or [datetime.now(timezone.utc).isoformat()]),'files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in files],'requests':requests,'cleaning':cleaning,'limitations':limits,'script':'scripts/freeze-imagery.py','scriptVersion':'1.0.0'}
 save(folder/'metadata.json',meta)
 (folder/'README.md').write_text(f'# {title}\n\nAuthor: {agency}\n\nSource: {source}\n\nLicence: [{lic}]({licurl})\n\nRetrieved: {meta["retrievedAt"]}\n\nPeriod: {period}. {rows} images.\n\n## Cleaning\n'+''.join('- '+s+'\n' for s in cleaning)+'\n## Limitations\n'+''.join('- '+s+'\n' for s in limits)+f'\n## Refresh\n`python3 scripts/freeze-imagery.py {"sentinel" if id=="sentinel-2" else "commons"}`. See script docstring for dependencies. Exact requests and SHA-256 checksums are in metadata.json. Originals are cached; move this folder aside for a new retrieval.\n')
 manifest();print(id,rows,flush=True)
def commons():
 folder=DATA/'open-images';folder.mkdir(exist_ok=True)
 items=[('Microcystis_live.jpg','Panek','CC BY 2.5','https://creativecommons.org/licenses/by/2.5/','2007-02-11','Microcystis cells seen through a microscope.'),('Dolichospermum_sp..jpg','Masa Zupancic','CC BY-SA 4.0','https://creativecommons.org/licenses/by-sa/4.0/','2019-05-13','Microscope image of Dolichospermum.'),('Microscopic_image_of_spirogyra.jpg','SPJ777','CC BY 4.0','https://creativecommons.org/licenses/by/4.0/','2023-03-15','Microscope image of the green alga Spirogyra.'),('20230604Lemna_minor1.jpg','AnRo0002','CC0 1.0','https://creativecommons.org/publicdomain/zero/1.0/','2023-06-04','Duckweed plants on water, photographed from above.'),('Pollen_on_the_water.jpg','T.Smirnova','CC BY 4.0','https://creativecommons.org/licenses/by/4.0/','2020-05-31','Pollen floating on the surface of water.')]
 items=items[:4]  # Pollen original was rate-limited; explicitly deferred, not substituted.
 images=[];files=[]
 for name,author,lic,licurl,date,alt in items:
  url='https://commons.wikimedia.org/wiki/Special:FilePath/'+urllib.parse.quote(name)
  p=folder/name;get(url,p,True)
  assert p.read_bytes()[:2]==b'\xff\xd8','Not a JPEG response'
  files.append(p);images.append({'file':str(p.relative_to(ROOT)),'author':author,'license':lic,'licenseUrl':licurl,'sourceUrl':'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(name),'imageDate':date,'alt':alt,'changes':'None; original file.','specimenGroup':name,'kind':'Real image','local':False})
 save(folder/'images.json',images);files.append(folder/'images.json')
 finish('open-images','Organisms and look-alikes','Individual photographers; see images.json','Mixed open licences; see each image','https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia','https://commons.wikimedia.org/','Real image',files,len(items),'2007–2023 images; not Lady Bird Lake',['Download original JPEGs without alteration.','Retain per-image author, licence, date, source and specimen-group ID.'],['These images are not local lake measurements or toxin evidence.','CC BY-SA applies to adaptations of the Dolichospermum image.','A small curated gallery is not a validated identification system.'])
def sentinel():
 import rasterio
 from rasterio.warp import transform_bounds
 from rasterio.windows import from_bounds,Window
 from PIL import Image
 folder=DATA/'sentinel-2';folder.mkdir(exist_ok=True)
 source='https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2B_14RPU_20190813_0_L2A'
 item=get(source,folder/'scene.json');href=item['assets']['visual']['href']
 bounds=[-97.800,30.235,-97.690,30.303]
 with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif',GDAL_HTTP_TIMEOUT='120'):
  with rasterio.open(href) as src:
   b=transform_bounds('EPSG:4326',src.crs,*bounds)
   w=from_bounds(*b,transform=src.transform).round_offsets().round_lengths()
   array=src.read([1,2,3],window=w)
   transform=src.window_transform(w)
   profile=src.profile.copy();profile.update(width=array.shape[2],height=array.shape[1],transform=transform,compress='deflate',tiled=True)
   with rasterio.open(folder/'lake-true-colour.tif','w',**profile) as dst:dst.write(array)
   Image.fromarray(array.transpose(1,2,0)).save(folder/'lake-true-colour.jpg',quality=90)
   save(folder/'crop.json',{'scene':item['id'],'date':item['properties']['datetime'],'requestedBoundsWGS84':bounds,'crs':str(src.crs),'transform':list(transform),'width':array.shape[2],'height':array.shape[1],'pixelSizeMetres':10,'sourceAsset':href,'processing':'Crop existing 8-bit TCI RGB at native 10 m; JPEG quality 90; no additional contrast stretch.','attribution':'Contains modified Copernicus Sentinel data 2019, processed by ESA; hosted by Element 84 / AWS.','alt':'True-colour Sentinel-2 view of Lady Bird Lake and surrounding Austin on 13 August 2019.','cloudReview':'Visual screening required; tile cloud percentage is not local cloud fraction.'})
   save(folder/'asset.request.json',{'url':href,'retrievedAt':datetime.now(timezone.utc).isoformat(),'method':'HTTP byte-range crop via rasterio; full original not downloaded','cropSha256':sha(folder/'lake-true-colour.tif')})
 finish('sentinel-2','Lady Bird Lake from Sentinel-2','Copernicus / ESA; Element 84 Earth Search mirror','Copernicus free, full and open use','https://documentation.dataspace.copernicus.eu/FAQ.html',source,'Real image',[folder/'lake-true-colour.jpg',folder/'lake-true-colour.tif',folder/'crop.json',folder/'scene.json'],1,'2019-08-13',['Select audited scene S2B_14RPU_20190813_0_L2A.','Range-read a native 10 m RGB crop covering the lake; save georeferenced TIFF and JPEG.','Contains modified Copernicus Sentinel data 2019.'],['True colour does not identify toxins or hidden bottom mats.','L2A land surface reflectance is not water-leaving reflectance.','Cloud/shadow suitability requires visual review; no quantitative cloud mask was applied.'])
if __name__=='__main__':
 choice=sys.argv[1] if len(sys.argv)>1 else 'all'
 if choice in ['all','commons']:commons()
 if choice in ['all','sentinel']:sentinel()
