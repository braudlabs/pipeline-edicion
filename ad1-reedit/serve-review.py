from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import re,os
ROOT=Path(__file__).resolve().parent/'output'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def send_head(self):
  self.remaining=None;p=self.translate_path(self.path)
  if not os.path.isfile(p):return super().send_head()
  f=open(p,'rb');size=os.fstat(f.fileno()).st_size;r=self.headers.get('Range');start=0;end=size-1
  if r:
   m=re.fullmatch(r'bytes=(\d*)-(\d*)',r.strip())
   if not m:f.close();self.send_error(416);return None
   if m[1]:start=int(m[1]);end=min(end,int(m[2]) if m[2] else end)
   elif m[2]:start=max(0,size-int(m[2]))
   if start>end or start>=size:f.close();self.send_error(416);return None
  self.send_response(206 if r else 200);self.send_header('Content-Type',self.guess_type(p));self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-cache');self.send_header('Content-Length',str(end-start+1))
  if r:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  self.end_headers();f.seek(start);self.remaining=end-start+1;return f
 def copyfile(self,source,out):
  if self.remaining is None:return super().copyfile(source,out)
  try:
   while self.remaining:
    b=source.read(min(65536,self.remaining))
    if not b:break
    out.write(b);self.remaining-=len(b)
  except (BrokenPipeError,ConnectionResetError):pass
ThreadingHTTPServer(('127.0.0.1',8778),Handler).serve_forever()
