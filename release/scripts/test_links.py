from unittest.mock import patch
from urllib.error import HTTPError
import importlib.util
from pathlib import Path
p=Path(__file__).with_name('check_links.py')
# Script checks live links when imported; instead test core classifications with extracted probe code.
src=p.read_text()
start=src.index('def probe(url):')
end=src.index('\np=P()',start)
namespace={'Request':lambda *a,**k:'req','HTTPError':HTTPError,'URLError':__import__('urllib.error',fromlist=['URLError']).URLError,'TimeoutError':TimeoutError,'ValueError':ValueError}
exec(src[start:end],namespace)
with patch.dict(namespace,{'urlopen':lambda *a,**kw: (_ for _ in ()).throw(HTTPError('https://example.invalid/test',404,'Not found',{},None))}):
 assert namespace['probe']('https://example.invalid/test')['status']=='broken'
with patch.dict(namespace,{'urlopen':lambda *a,**kw: (_ for _ in ()).throw(HTTPError('https://example.invalid/test',403,'Forbidden',{},None))}):
 assert namespace['probe']('https://example.invalid/test')['status']=='manual_review'
print('Link-check: 404=broken; 403=manual_review; негативные тесты пройдены')
