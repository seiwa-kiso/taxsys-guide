#!/usr/bin/env python3
"""Update official TaxSys release index; only official-version metadata, no invented steps."""
import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'releases.json'
URL = 'https://docs.taxsys.so-labo.co.jp/releases'
# Official announced dates: 2026-11-12, 11-26, 12-10, 12-24, 2027-01-07, 01-21, ...
ANCHOR = dt.date(2026, 11, 12)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.href=dict(attrs).get('href', ''); self.parts=[]
    def handle_data(self, data):
        if self.href is not None: self.parts.append(data)
    def handle_endtag(self, tag):
        if tag=='a' and self.href is not None:
            self.links.append((''.join(self.parts).strip(), self.href))
            self.href=None; self.parts=[]

def fetch():
    req=Request(URL, headers={'User-Agent':'TaxSys-Guide-Release-Checker/1.0 (public guide)', 'Accept':'text/html'})
    with urlopen(req, timeout=25) as response:
        return response.read().decode('utf-8')

def extract(doc):
    parser=LinkParser(); parser.feed(doc)
    versions=[]; seen=set()
    for title,href in parser.links:
        title=title.strip()
        if not re.fullmatch(r'v\d+\.\d+\.\d+',title, re.I): continue
        full=urljoin(URL,html.unescape(href))
        if urlparse(full).netloc!='docs.taxsys.so-labo.co.jp' or full in seen: continue
        seen.add(full); versions.append({'version':title,'url':full})
    # Source index table is plain rendered text; only capture date and concise official row summary.
    raw=re.sub(r'<[^>]+>',' ',doc)
    raw=html.unescape(re.sub(r'\s+',' ',raw))
    for item in versions:
        v=item['version']
        # dates belong in table immediately after the linked version
        match=re.search(r'\b'+re.escape(v)+r'\s+(20\d{2}-\d{2}-\d{2})\s+(.{0,600}?)(?=\s+v\d+\.\d+\.\d+\s+20\d{2}-\d{2}-\d{2}|$)',raw)
        if match:
            item['date']=match.group(1)
            summary=match.group(2).strip()
            item['summary']=summary[:350]
    return versions

def should_run(today):
    return today >= ANCHOR and (today-ANCHOR).days % 14 in (0,1)

def main():
    now=dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    today=now.date()
    if '--force' not in sys.argv and not should_run(today):
        print('Outside announced biweekly Thu/Fri release window; skip')
        return
    doc=fetch(); records=extract(doc)
    if not records or 'date' not in records[0] or len(records)<5:
        raise RuntimeError('Cannot reliably parse official version/date index. Refuse to overwrite.')
    old=json.loads(OUTPUT.read_text('utf-8')) if OUTPUT.exists() else {}
    payload={'source': URL,'releases':records[:30]}
    # No commit if same releases; avoids updating timestamp every run.
    if old.get('releases')==payload['releases']:
        print('No release updates'); return
    OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Updated release index: '+records[0]['version'])

if __name__=='__main__': main()
