#!/usr/bin/env python3
"""Fit shared trajectory on pagar/Braudd, test shape on sirve (held out)."""
import json
from pathlib import Path
import numpy as np
from common import DATOS
p=DATOS/'revision-v2';curves=json.loads((p/'v8-native-curves.json').read_text());starts={'pagar':550,'Braudd':1653,'sirve':3328}
series={};rejected=[]
for curve in curves:
 interior=[r['threshold30']['pixelCount'] for r in curve['rows'] if r['threshold30'] and 3<=r['frame']-starts[curve['id']]<=20]
 reference=float(np.median(interior));series[curve['id']]={}
 for row in curve['rows']:
  age=row['frame']-starts[curve['id']];v=row['threshold30']
  if not v or not 2<=age<=60:continue
  if v['pixelCount']<.2*reference:
   rejected.append({'label':curve['id'],'frame':row['frame'],'reason':'chroma pixel area <20% of interior median; fragmented low-contrast detection','raw':v});continue
  series[curve['id']][age]=v['y']
rows=[(i,t,y) for i,name in enumerate(['pagar','Braudd']) for t,y in series[name].items()]
g=np.array([r[0] for r in rows]);t=np.array([r[1] for r in rows]);y=np.array([r[2] for r in rows]);bias=np.column_stack([g==0,g==1]).astype(float)
best=None
for decay in np.linspace(.02,.18,161):
 decayv=np.exp(-decay*t)
 for omega in np.linspace(.22,.42,201):
  X=np.column_stack([bias,decayv*np.cos(omega*t),decayv*np.sin(omega*t)])
  coef=np.linalg.lstsq(X,y,rcond=None)[0];error=float(np.mean((X@coef-y)**2))
  if best is None or error<best[0]:best=(error,decay,omega,coef)
err,d,w,c=best
motion=lambda t: np.exp(-d*t)*(c[2]*np.cos(w*t)+c[3]*np.sin(w*t))
test=series['sirve'];base=test[2]-motion(2);residual=[(t,y,base+motion(t),y-base-motion(t)) for t,y in test.items()]
report={'status':'fitted_observed_position_only','source':'v8','sourceFps':{'num':60000,'den':1001},'sourceHeight':1920,'sourceWidth':1080,'coordinate':'top of lime ink box, not center/baseline/fontSize','model':'y(frameAge)=layoutOffset+exp(-decay*frameAge)*(cosCoefficient*cos(omega*frameAge)+sinCoefficient*sin(omega*frameAge))','firstVisibleFrames':starts,'fitDomainSourceFrames':[2,60],'decayPerSourceFrame':float(d),'omegaRadiansPerSourceFrame':float(w),'cosCoefficientPx':float(c[2]),'sinCoefficientPx':float(c[3]),'fitOffsetsPx':{'pagar':float(c[0]),'Braudd':float(c[1])},'trainingRMSEpx':float(np.sqrt(err)),'trainingSamples':len(rows),'rejectedSamples':rejected,'heldOut':{'label':'sirve','range':[min(test),max(test)],'offsetCalibration':'only measured top at age2; no curve parameters refit','rmsePx':float(np.sqrt(np.mean([r[3]**2 for r in residual]))),'maxAbsErrorPx':float(max(abs(r[3]) for r in residual)),'samples':len(residual),'columns':['age','observedY','predictedY','error'],'rows':[[int(t),float(y),float(pred),float(e)] for t,y,pred,e in residual]},'limits':['This is an approximation fitted to a decoded MP4, not recovered source easing/plugin.','Parameters describe translation only. Font, color, opacity, blur, masks and semantics are separate.','Same source piece; NOT cross-video or cross-family validation.','Frame age0/1 is visually present but low contrast makes chroma bounds unreliable. Extrapolation outside measured domain requires review.','Threshold dependence and compression remain; same-word width stable does not identify exact font.']}
early=[r for r in residual if r[0]<=23]
report['heldOut']['entryPhaseReview']={'range':[2,23],'rmsePx':float(np.sqrt(np.mean([r[3]**2 for r in early]))),'maxAbsErrorPx':float(max(abs(r[3]) for r in early)),'note':'Exploratory phase separation after inspecting residuals and native exit frames3349–3364. Not a preregistered independent benchmark. Full-range error is retained above; translation diverges before disappearance/cut during exit.'}
(p/'v8-motion-fit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['heldOut','limits']},indent=2));print('heldout',report['heldOut']['rmsePx'],report['heldOut']['maxAbsErrorPx'])
