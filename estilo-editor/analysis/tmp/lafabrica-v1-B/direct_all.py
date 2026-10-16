import sys, json, math
sys.path.insert(0,'analysis/tmp/lafabrica-v1-B')
from track import sim, scaled_gray
import numpy as np
cum=json.load(open('analysis/tmp/lafabrica-v1-B/cumscale.json'))
def direct(first,last,name,excl):
    L=np.array(cum[name]); S=np.exp(L)
    out=[]
    for k in range(0,last-first):
        n=first+k
        r=S[-1]/S[k]
        A,box,(rx,ry)=scaled_gray(n,r)
        cx,cy=540,960
        ex=[(cx+(x0-cx)*r,cy+(y0-cy)*r,cx+(x1-cx)*r,cy+(y1-cy)*r) for x0,y0,x1,y1 in excl]
        rr=sim(A,last,excl=ex,roi=(box[0]+8,box[1]+8,box[2]-8,box[3]-8),sr=32,step=70)
        if rr is None: out.append((k,None)); continue
        out.append((k,float(1/(rx*rr['s'])),float(rr['tx']),float(rr['ty']),rr['n'],rr['ntot']))
    out.append((last-first,1.0,0,0,0,0))
    return out
R={}
R['lupa']=direct(836,911,'lupa',[(0,400,1080,760)])
R['final']=direct(1007,1062,'final',[(0,330,1080,640)])
R['cinta']=direct(782,835,'cinta',[(0,280,1080,620)])
R['hornoA']=direct(614,650,'hornoA',[(0,960,1080,1400)])
json.dump(R,open('analysis/tmp/lafabrica-v1-B/direct_all.json','w'))
print('ok')
