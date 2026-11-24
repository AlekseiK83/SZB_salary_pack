#!/usr/bin/env python3
"""Weekly non-blocking external link health report. 403/429 never means dead."""
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from pathlib import Path
import json,datetime,sys
class P(HTMLParser):
 def __init__(self):super().__init__();self.urls=set()
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key in ('href','src') and value and value.startswith(('https://','http://')):self.urls.add(value)

def probe(url):
 try:
  req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; SZB-link-audit/1.0)'},method='HEAD')
  with urlopen(req,timeout=10) as r:status=r.status;dest=r.url
 except HTTPError as e:
  if e.code in (403,405,429):return {'url':url,'status':'manual_review','http_code':e.code,'note':'bot/rate limit or HEAD unsupported'}
  return {'url':url,'status':'broken' if e.code in (404,410) else 'manual_review','http_code':e.code}
 except (URLError,TimeoutError,ValueError) as e:return {'url':url,'status':'manual_review','note':str(e)[:130]}
 return {'url':url,'status':'redirect' if dest!=url else 'ok','http_code':status,'target':dest if dest!=url else None}

p=P();p.feed((Path(__file__).resolve().parents[1]/'index.html').read_text('utf-8'))
results=[]
with ThreadPoolExecutor(max_workers=6) as ex:
 for f in as_completed({ex.submit(probe,u):u for u in sorted(p.urls)}):results.append(f.result())
results.sort(key=lambda x:x['url'])
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(results),'results':results}
out=Path('reports/link_status.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
print('Проверено',len(results),'ссылок; статусы', {x:sum(r['status']==x for r in results) for x in set(r['status'] for r in results)})
