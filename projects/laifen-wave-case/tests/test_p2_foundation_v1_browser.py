from __future__ import annotations
import contextlib, http.server, socketserver, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"projects/laifen-wave-case/scratch/p2-foundation-v1-implementation/screenshots"
PORT=8897
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args): pass
class Server(socketserver.TCPServer): allow_reuse_address=True
@contextlib.contextmanager
def server():
    handler=lambda *args, **kwargs: Quiet(*args,directory=str(ROOT),**kwargs)
    with Server(("127.0.0.1",PORT),handler) as httpd:
        thread=threading.Thread(target=httpd.serve_forever,daemon=True);thread.start()
        try: yield
        finally: httpd.shutdown();thread.join()

def exercise(page):
    page.goto(f"http://127.0.0.1:{PORT}/projects/laifen-wave-case/preview/p2-foundation-v1/",wait_until="networkidle")
    assert page.locator("#v1-viewport canvas").count()==1
    assert page.locator("#v1-derived").inner_text().find("Clear ID")>=0
    page.locator("#v1-OD").fill("3");page.locator("#v1-OD").dispatch_event("input")
    assert "Invalid active state" in page.locator("#v1-errors").inner_text()
    assert page.evaluate("window.__v1.descriptor === null"),"invalid input must clear the scene descriptor"
    page.locator("#v1-OD").fill("60");page.locator("#v1-OD").dispatch_event("input")
    assert page.evaluate("window.__v1.descriptor !== null")
    page.locator("#v1-view-exploded").click(); assert page.evaluate("window.__v1.descriptor.presentation === 'exploded'")
    page.locator("#v1-view-open").click();page.locator("#v1-view-cutaway").click()
    assert page.evaluate("window.__v1.scene.getObjectByName('v1.lower.shell').material.clippingPlanes.length === 1")
    page.locator("#v1-view-reset").focus();page.keyboard.press("Enter")
    page.locator("#v1-viewport").hover();page.mouse.wheel(0,180);page.mouse.move(450,350);page.mouse.down();page.mouse.move(490,370);page.mouse.up()
    assert page.locator("#v1-disclosure").inner_text()=="Conceptual, dimensionally proportional preview. Not CAD; no printability, fit, strength, drainage, export, or physical validation."

OUT.mkdir(parents=True,exist_ok=True)
with server(),sync_playwright() as p:
    for engine in (p.chromium,p.firefox,p.webkit):
        for viewport in ({"width":1280,"height":900},{"width":390,"height":844}):
            browser=engine.launch();page=browser.new_page(viewport=viewport);errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
            exercise(page);assert not errors,errors
            if engine==p.chromium:
                tag="desktop" if viewport["width"]>700 else "mobile"
                for view in ("assembled","open","exploded","cutaway"):
                    page.locator(f"#v1-view-{view}").click();page.screenshot(path=str(OUT/f"{tag}-{view}.png"),full_page=True)
            browser.close()
print("Foundation V1 browser gates passed: Chromium/Firefox/WebKit desktop/mobile, interaction, invalid recovery, view controls, screenshots")
