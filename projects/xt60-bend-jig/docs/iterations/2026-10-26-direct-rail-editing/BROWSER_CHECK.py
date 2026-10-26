import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse
PROJECT=Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser()
parser.add_argument('--url',default=(PROJECT/'preview/xt60-rail-customizer.html').as_uri())
args=parser.parse_args()
OUT=PROJECT.parents[1]/'scratch/rail-customizer-browser'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1100},accept_downloads=True)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(args.url)
 assert page.locator('[data-edit]').count()==0
 assert page.locator('[data-handle]').count()==9
 def coords(name,end):
  return [float(page.get_by_label(f'{name} {end} {axis}',exact=True).input_value()) for axis in ['Y','Z']]
 def drag(selector,dx,dy):
  box=page.locator(selector).bounding_box()
  x,y=box['x']+box['width']/2,box['y']+box['height']/2
  page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+dx,y+dy,steps=8);page.mouse.up()
 before=coords('Blue','OPEN');end=coords('Blue','END')
 drag('[data-handle="0"][data-kind="open"] .handle-target',25,0)
 assert coords('Blue','OPEN')[0]>before[0]+1
 assert coords('Blue','END')==end
 before=coords('Orange','END');start=coords('Orange','OPEN')
 drag('[data-handle="1"][data-kind="end"] .handle-target',0,-20)
 assert coords('Orange','END')[1]>before[1]+1
 assert coords('Orange','OPEN')==start
 page.locator('#reset').click()
 before=coords('Blue','OPEN');end=coords('Blue','END')
 point=page.evaluate('''()=>{const p=RailGeometry.world(RailGeometry.defaults().rods[0],.25);const v=new DOMPoint(p[0],-p[1]).matrixTransform(document.querySelector('#editor').getScreenCTM());return [v.x,v.y]}''')
 page.mouse.move(*point);page.mouse.down();page.mouse.move(point[0]+22,point[1]-12,steps=8);page.mouse.up()
 after=coords('Blue','OPEN');afterend=coords('Blue','END')
 assert after[0]>before[0]+1
 assert abs((after[0]-before[0])-(afterend[0]-end[0]))<.02
 assert abs((after[1]-before[1])-(afterend[1]-end[1]))<.02
 assert coords('Blue','curve offset')==[0,0]
 paths=page.locator('#left-view [data-rail="0"]').get_attribute('d')
 before=coords('Blue','OPEN');end=coords('Blue','END')
 drag('[data-handle="0"][data-kind="curve"] .handle-target',10,-30)
 bend=coords('Blue','curve offset')
 assert bend[1]>1
 assert coords('Blue','OPEN')==before and coords('Blue','END')==end
 assert paths!=page.locator('#left-view [data-rail="0"]').get_attribute('d')
 curvepath=page.locator('#left-view [data-rail="0"]').get_attribute('d')
 page.locator('[data-state="1"]').click()
 assert curvepath==page.locator('#left-view [data-rail="0"]').get_attribute('d')
 page.reload();assert coords('Blue','curve offset')==bend
 with page.expect_download() as d: page.locator('#save').click()
 d.value.save_as(OUT/'profile.json')
 saved=json.loads((OUT/'profile.json').read_text());assert saved['rods'][0]['bendMm'][1]>1
 page.locator('#reset').click();page.locator('#file').set_input_files(OUT/'profile.json')
 page.wait_for_function('document.querySelector("#status").textContent==="Profile loaded."')
 assert coords('Blue','curve offset')==bend
 page.locator('#editor [data-line="0"]').focus();before=coords('Blue','OPEN');end=coords('Blue','END');page.keyboard.press('ArrowRight')
 assert abs(coords('Blue','OPEN')[0]-before[0]-.1)<.02
 assert abs(coords('Blue','END')[0]-end[0]-.1)<.02
 page.locator('#editor [data-handle="0"][data-kind="curve"]').focus();beforebend=coords('Blue','curve offset');page.keyboard.press('ArrowUp')
 assert abs(coords('Blue','curve offset')[1]-beforebend[1]-.1)<.02
 page.locator('#reset').click()
 drag('[data-handle="2"][data-kind="open"] .handle-target',-20,0)
 assert coords('Green','OPEN')[0]<14
 assert coords('Green','END')==[14.73,-6.25]
 page.locator('#reset').click()
 before=coords('Green','OPEN');end=coords('Green','END')
 point=page.evaluate('''()=>{const p=RailGeometry.defaults().rods[2].open;const v=new DOMPoint(p[0],-p[1]).matrixTransform(document.querySelector('#editor').getScreenCTM());return [v.x,v.y]}''')
 assert page.evaluate('''([x,y])=>document.elementFromPoint(x,y).getAttribute('data-line')''',point)=='2'
 page.mouse.move(*point);page.mouse.down();page.mouse.move(point[0]+18,point[1]-10,steps=8);page.mouse.up()
 assert coords('Green','OPEN')[0]>before[0]+1
 assert abs((coords('Green','OPEN')[0]-before[0])-(coords('Green','END')[0]-end[0]))<.02
 assert abs(coords('Green','OPEN')[0]-coords('Green','END')[0])<.01
 page.locator('#reset').click()
 for endpoint in ['OPEN','END']:
  for axis in ['Y','Z']:
   field=page.get_by_label(f'Green {endpoint} {axis}',exact=True);field.fill('-10');field.press('Tab')
 point=page.evaluate('''()=>{const v=new DOMPoint(-10,10).matrixTransform(document.querySelector('#editor').getScreenCTM());return [v.x,v.y]}''')
 assert page.evaluate('''([x,y])=>document.elementFromPoint(x,y).getAttribute('data-line')''',point)=='2'
 page.mouse.move(*point);page.mouse.down();page.mouse.move(point[0]+18,point[1]-10,steps=8);page.mouse.up()
 assert coords('Green','OPEN')[0]>-9 and coords('Green','OPEN')==coords('Green','END')
 page.locator('#reset').click()
 page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
 assert not errors,errors
 print(json.dumps({'url':args.url,'endpoint_drag':'PASS','whole_line_drag':'PASS','curve_drag':'PASS','legacy_save_reload_keyboard':'PASS','coincident_handles':'PASS','errors':errors}))
 browser.close()
