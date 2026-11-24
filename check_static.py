#!/usr/bin/env python3
"""SZB salary pack offline integrity checks. Stdlib only."""
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
import re, subprocess, sys, tempfile, argparse
ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.scripts=[];self.script=False;self.parts=[];self.classes=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and (a.get('href') or '').startswith('#'):self.links.append(a['href'][1:])
        if tag=='script' and 'src' not in a:self.script=True;self.parts=[]
        if 'class' in a:self.classes.extend(a['class'].split())
    def handle_endtag(self,tag):
        if tag=='script' and self.script:self.scripts.append(''.join(self.parts));self.script=False
    def handle_data(self,data):
        if self.script:self.parts.append(data)

def errors(html):
    p=Parser();p.feed(html);bad=[]
    dup=[id for id,n in Counter(p.ids).items() if n>1]
    if dup:bad.append('Дубликаты ID: '+', '.join(dup[:15]))
    broken=[href for href in p.links if href and href not in p.ids]
    if broken:bad.append('Несуществующие якоря: '+', '.join(sorted(set(broken))[:15]))
    if len(re.findall(r'<section\b[^>]*class="[^"]*\bview\b',html))!=26:bad.append('Изменилось число маршрутизируемых разделов')
    if html.count('class="sp-micro ')!=25:bad.append('Изменилось число мини-баннеров')
    if 'id="emp-mobile"' not in html or 'class="sm-offer' not in html:bad.append('Нет большого баннера СберМобайл')
    if re.search(r'location\.search\.match\(/\[\?&\]today',html):bad.append('Возвращён URL override ?today=')
    if 'paket-prodavca-zp.pdf' not in html:bad.append('Утеряна ссылка на PDF')
    pdf=ROOT/'paket-prodavca-zp.pdf'
    if pdf.exists() and not pdf.read_bytes().startswith(b'%PDF-'):bad.append('PDF повреждён: отсутствует сигнатура')
    if '<meta name="robots" content="noindex' not in html:bad.append('Не найден существующий noindex')
    for i,src in enumerate(p.scripts):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.js',encoding='utf-8',delete=False) as f:f.write(src);name=f.name
        r=subprocess.run(['node','--check',name],capture_output=True,text=True)
        Path(name).unlink(missing_ok=True)
        if r.returncode:bad.append('JS #'+str(i)+': '+r.stderr[:250])
    return bad,len(p.links),len(p.scripts)

def main():
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');args=p.parse_args()
    src=(ROOT/'index.html').read_text(encoding='utf-8');bad,nlinks,njs=errors(src)
    if args.self_test:
        x=src.replace('href="#biz-money"','href="#missing-szb-test"',1)
        assert any('якоря' in e for e in errors(x)[0]), 'broken-link injection not detected'
        x=src.replace('window.ASK_EP=\'\';',"window.ASK_EP='';function(",1)
        assert any('JS' in e for e in errors(x)[0]),'invalid-JS injection not detected'
        print('Проверка негативных тестов: оба дефекта обнаружены')
    print(f'Статическая проверка: {nlinks} внутренних ссылок, {njs} JS-блоков; дефектов: {len(bad)}')
    for e in bad:print('FAIL:',e,file=sys.stderr)
    return 1 if bad else 0
if __name__=='__main__':raise SystemExit(main())
