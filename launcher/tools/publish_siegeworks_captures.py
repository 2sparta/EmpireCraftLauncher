"""Publish only synthetic gameplay PNGs on an isolated inspection branch; never changes the pack channel."""
import base64,json,os,urllib.request,urllib.error
from pathlib import Path
REPO='2sparta/EmpireCraftLauncher';BRANCH='codex/siegeworks-captures'
ROOT=Path('launcher/kitchen-captures/screenshots');files=sorted(ROOT.glob('*.png'))
if not files:raise SystemExit(0)
def api(path,method='GET',data=None):
 request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+path,method=method,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'},data=json.dumps(data).encode() if data is not None else None)
 with urllib.request.urlopen(request) as response:return json.load(response)
try:parent=api('git/ref/heads/'+BRANCH)['object']['sha'];exists=True
except urllib.error.HTTPError as error:
 if error.code!=404:raise
 parent=os.environ['GITHUB_SHA'];exists=False
commit=api('git/commits/'+parent);tree=[]
for file in files:
 assert file.name.startswith(('01-','02-','03-')) and file.stat().st_size<4000000
 blob=api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(file.read_bytes()).decode()})
 tree.append({'path':'launcher/audit/siegeworks-test/captures/'+file.name,'mode':'100644','type':'blob','sha':blob['sha']})
record={'source_commit':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'files':[f.name for f in files]}
blob=api('git/blobs','POST',{'encoding':'utf-8','content':json.dumps(record,indent=2)+'\n'});tree.append({'path':'launcher/audit/siegeworks-test/captures/run.json','mode':'100644','type':'blob','sha':blob['sha']})
tree=api('git/trees','POST',{'base_tree':commit['tree']['sha'],'tree':tree})
new=api('git/commits','POST',{'message':'Capture all Siegeworks engines and item models','parents':[parent],'tree':tree['sha']})
if exists:api('git/refs/heads/'+BRANCH,'PATCH',{'sha':new['sha'],'force':False})
else:api('git/refs','POST',{'ref':'refs/heads/'+BRANCH,'sha':new['sha']})
print('SYNTHETIC_CAPTURES_COMMIT',new['sha'])
