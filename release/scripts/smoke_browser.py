#!/usr/bin/env python3
"""Run basic client scenarios without external network or fonts via set_content."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,sys,shutil
HTML=(Path(__file__).resolve().parents[1]/'index.html').read_text('utf-8')

def run():
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path=shutil.which("chromium") or None,args=["--no-sandbox"])
  passed=0
  for width in (320,390,768,1440):
   page=b.new_page(viewport={'width':width,'height':850});errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.set_content(HTML,wait_until='load')
   for ident in ('biz-money','biz-requisites','emp-mobile','pick','calc','objections'):
    page.evaluate('(h) => {location.hash="#"+h;window.dispatchEvent(new Event("hashchange"))}',ident)
    assert 'on' in (page.locator('#'+ident).get_attribute('class') or '').split(),f'view {ident} not active at {width}'
    passed+=1
   page.evaluate('location.hash="#pick";window.dispatchEvent(new Event("hashchange"))')
   assert page.locator('#onepage .op-top li').count()==7
   assert not any('Sber API' in x for x in page.locator('#onepage .op-top .op-t').all_inner_texts())
   page.locator('#f-api').evaluate('(el)=>{el.checked=true;el.dispatchEvent(new Event("change",{bubbles:true}));}')
   assert page.locator('#onepage .op-top li').count()==7
   page.locator('#f-api').evaluate('(el)=>{el.checked=false;el.dispatchEvent(new Event("change",{bubbles:true}));}')
   passed+=3
   page.evaluate('location.hash="#calc";window.dispatchEvent(new Event("hashchange"))')
   page.locator('#cl-n').fill('0')
   assert 'Проверьте поля' in page.locator('#calc-out').inner_text()
   page.locator('#cl-n').fill('100')
   page.locator('#szb-scenario-mode').select_option('potential')
   assert 'Проверьте поля' in page.locator('#calc-out').inner_text()
   page.locator('#szb-scenario-share').fill('40')
   assert 'бонусов СберСпасибо' in page.locator('#calc-out').inner_text()
   passed+=3
   page.locator('#srch-open').click(force=True)
   assert page.locator('.sr-wrap').is_visible()
   assert page.evaluate('document.activeElement.id')=='sr-q'
   page.keyboard.press('Shift+Tab')
   assert page.evaluate('document.activeElement.id')=='sr-x'
   page.keyboard.press('Tab')
   assert page.evaluate('document.activeElement.id')=='sr-q'
   page.keyboard.press('Escape')
   assert page.evaluate('document.activeElement.id')=='srch-open'
   passed+=5
   assert not errors,errors
   assert not page.evaluate('document.documentElement.scrollWidth>window.innerWidth'),f'overflow at {width}'
   passed+=2
   page.close()
  b.close()
 print('Chromium: '+str(passed)+' проверок, ошибок JS и горизонтального переполнения нет')
if __name__=='__main__':run()
