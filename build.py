import os, json, pathlib, subprocess, concurrent.futures, zipfile, io
from PIL import Image
P=pathlib.Path(__file__).parent
S=pathlib.Path('/root/.hermes/cache/scratch')
SRC=S/'xaero-root/client-overrides/xaero/world-map/Multiplayer_mc.zixing.fun/null/mw$-1024774095'
BIN=S/'xaerotools-src/target/release/xaerotools'
NATIVE=7
T=P/'tiles/overworld'
def path(z,x,y):
 p=T/str(z)/str(x)/f'{y}.webp';p.parent.mkdir(parents=True,exist_ok=True);return p
def render(f):
 x,y=map(int,f.stem.split('_')); tmp=P/'raw'/f.name.replace('.zip','.png');tmp.parent.mkdir(exist_ok=True)
 subprocess.run([str(BIN),'render-region',str(f),'-o',str(tmp)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 with Image.open(tmp) as im:
  assert im.size==(512,512)
  im.convert('RGBA').save(path(NATIVE,x,y),'WEBP',lossless=True,method=4)
 tmp.unlink();return x,y
files=sorted(SRC.glob('*.zip'))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: cells=set(pool.map(render,files))
counts={str(NATIVE):len(cells)}
for z in range(NATIVE-1,-1,-1):
 parents={(x//2,y//2) for x,y in cells}
 for x,y in parents:
  im=Image.new('RGBA',(1024,1024))
  for dx in range(2):
   for dy in range(2):
    c=(2*x+dx,2*y+dy)
    if c in cells:
     with Image.open(path(z+1,*c)) as child: im.paste(child,(dx*512,dy*512))
  im.resize((512,512),Image.Resampling.LANCZOS).save(path(z,x,y),'WEBP',lossless=True,method=4)
 cells=parents;counts[str(z)]=len(cells)
wp=[]
with zipfile.ZipFile(S/'zixing.mrpack') as a:
 names=[n for n in a.namelist() if '/minimap/Multiplayer_mc.zixing.fun/dim%0/' in n and n.endswith('.txt')]
 for n in names:
  for line in a.read(n).decode('utf-8-sig').splitlines():
   if line.startswith('waypoint:'):
    v=line.split(':');wp.append(dict(name=v[1],initials=v[2],x=int(v[3]),y=v[4],z=int(v[5]),color=int(v[6]),disabled=v[7]=='true'))
(P/'waypoints.json').write_text(json.dumps(wp,ensure_ascii=False,indent=2))
allcells=[tuple(map(int,f.stem.split('_'))) for f in files]
core=[(x,y) for x,y in allcells if abs(x)<=100 and abs(y)<=100]
manifest=dict(regions=len(files),counts=counts,totalTiles=sum(counts.values()),bytes=sum(f.stat().st_size for f in T.rglob('*.webp')),nativeZoom=NATIVE,tileSize=512,transform='Leaflet coords [-MC_Z, MC_X], CRS.Simple scale=2^(zoom-7); tile x=floor(X/(512*2^(7-zoom))), y=floor(Z/(512*2^(7-zoom)))',coreBounds=[min(x for x,y in core)*512,min(y for x,y in core)*512,(max(x for x,y in core)+1)*512,(max(y for x,y in core)+1)*512],source='26.3生电(based on xplus).mrpack',waypoints=len(wp))
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest,ensure_ascii=False))
