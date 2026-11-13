from pathlib import Path
import shutil,json,hashlib
P=Path(__file__).resolve().parent;F=Path('/Users/USER/.codex/skill-repos/FredTalk');R=P/'skills/FredTalk';A=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/解包只读副本');W=A/'fred-wave3-40-20261012';R.mkdir(parents=True,exist_ok=True)
for name in ['catalog.json','routes.json','media-manifest.json','member-packages.json','history.json']:
 src=F/'library'/name
 if src.exists():(R/'library').mkdir(exist_ok=True);shutil.copy2(src,R/'library'/name)
shutil.copytree(F/'skills/fred-remotion-output/scripts',R/'skills/fred-remotion-output/scripts',dirs_exist_ok=True)
shutil.copytree(F/'skills/fred-remotion-output/references',R/'skills/fred-remotion-output/references',dirs_exist_ok=True)
(R/'scripts').mkdir(exist_ok=True)
shutil.copy2(F/'scripts/member_access.py',R/'scripts/member_access.py')
# All source package files copied and checked against author's manifest. No login, token or remote download.
pkg=next(x for x in json.loads((R/'library/member-packages.json').read_text())['collections'] if x['collectionId']=='fred-wave3-40-20261012')
for name,rec in pkg['files'].items():
 src=A/name;dest=R/pkg['installRoot']/name
 assert hashlib.sha256(src.read_bytes()).hexdigest()==rec['sha256'],name
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
cat=json.loads((R/'library/catalog.json').read_text());routes=json.loads((R/'library/routes.json').read_text())
for label in ['L81-R001','L81-R006']:
 row=next(r for r in cat['items'] if r['label']==label)
 for s in row['sources']:
  rel=s.get('installPath') or routes.get(s['url']);src=F/rel;dest=R/rel
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
# parser dependency uses existing verified runtime and is local-only; npm never executed.
node=R/'apps/library/node_modules';node.mkdir(parents=True,exist_ok=True)
lib=P/'node_modules/typescript'
if not (node/'typescript').exists():(node/'typescript').symlink_to(lib.resolve(),target_is_directory=True)
(R/'skills/fred-remotion-output/assets').mkdir(exist_ok=True)
shutil.copy2(F/'skills/fred-remotion-output/assets/dependency-registry.json',R/'skills/fred-remotion-output/assets/dependency-registry.json')
print('copied source package',len(pkg['files']),sum(r['size'] for r in pkg['files'].values()),'bytes; local gate root',R)
