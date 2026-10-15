from pathlib import Path
import shutil,json
V=Path(__file__).resolve().parents[1];P=V/'Entrega';D=Path((V.parent/'source-path.txt').read_text().strip())/'edicion-final/V2'
shutil.copytree(P,D,dirs_exist_ok=True)
ids=json.load(open(V/'ae/ids.json'));req=[]
for p in (V/'assets').iterdir():
 if p.name in ids:req.append({'name':'ae_do','arguments':{'operation':'footage.replace','args':{'item':ids[p.name],'path':str(D/'After-Effects/assets'/p.name)}}})
req += [{'name':'ae_do','arguments':{'operation':'render.clear_queue','args':{}}},{'name':'ae_do','arguments':{'operation':'project.reduce','args':{'comps':['AD3 - FINAL V2']}}},{'name':'ae_save_project','arguments':{'path':str(D/'After-Effects/AD3-Pipeline-V2.aep')}},{'name':'ae_do','arguments':{'operation':'font.list_missing','args':{}}},{'name':'ae_do','arguments':{'operation':'footage.list_missing','args':{}}},{'name':'ae_project_info','arguments':{}}]
(V/'ae/collect.json').write_text(json.dumps(req));(V/'destination.txt').write_text(str(D));print(D)
