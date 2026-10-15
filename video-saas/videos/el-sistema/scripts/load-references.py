from pathlib import Path
import json,subprocess,urllib.parse,re,concurrent.futures
R=Path(__file__).resolve().parents[1];refs=json.loads((R/'references/sources.json').read_text())
def fetch(url):return subprocess.check_output(['curl','-L','--fail','-s',url])
def one(r):
 stem=Path(r['url']).stem;base=r['url'].rsplit('/',1)[0]+'/'
 for label,playlist in [('v',stem+'_720w.m3u8'),('a',stem+'_audio.m3u8')]:
  txt=fetch(base+playlist).decode();(R/'references'/f'ref-{r["id"]}-{label}.m3u8').write_text(txt)
  uri=re.search(r'URI="([^"]+)"',txt).group(1);url=urllib.parse.urljoin(base,uri)
  data=fetch(url+'?full=1');p=R/'references'/f'ref-{r["id"]}-{label}.mp4';p.write_bytes(data)
  print(r['id'],label,len(data),flush=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'references'/f'ref-{r["id"]}-v.mp4'),'-i',str(R/'references'/f'ref-{r["id"]}-a.mp4'),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(R/'references'/f'ref-{r["id"]}.mp4')],check=True)
with concurrent.futures.ThreadPoolExecutor(3) as ex:list(ex.map(one,refs))
