from __future__ import annotations
import contextlib
import http.server
import socketserver
import subprocess
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
PORT = 8891

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args): pass

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address=True

@contextlib.contextmanager
def server():
    handler=lambda *args, **kwargs: Quiet(*args, directory=str(ROOT), **kwargs)
    with ReusableTCPServer(("127.0.0.1", PORT), handler) as httpd:
        thread=threading.Thread(target=httpd.serve_forever, daemon=True); thread.start()
        try: yield
        finally: httpd.shutdown(); thread.join()

with server(), sync_playwright() as p:
    url=f"http://127.0.0.1:{PORT}/projects/laifen-wave-case/preview/p2-r10-parameter-sensitivity-recovery/"
    for engine in (p.chromium, p.firefox, p.webkit):
        for viewport in ({"width":1280,"height":900},{"width":390,"height":844}):
            browser=engine.launch()
            page=browser.new_page(viewport=viewport)
            errors=[]; page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(url, wait_until="networkidle")
            assert page.locator('[data-core-piece="upper-piece"]').count()==1
            assert page.locator('[data-core-piece="lower-piece"]').count()==1
            assert page.locator('[data-target]').count()>0
            assert "dimensionally proportional visual" in page.locator("body").inner_text().lower()
            assert "true scale" not in page.locator("body").inner_text().lower()
            page.locator("#tier").click()
            field=page.locator('[data-path="container.outerDiameter"]'); field.fill("3"); field.dispatch_event("input")
            assert page.locator("#viewer").inner_text()==""
            assert page.locator("#detail").inner_text()==""
            assert page.locator("#comparison").inner_text()==""
            assert "Invalid active state" in page.locator("#alert").inner_text()
            assert not errors, errors
            browser.close()
print("R10 browser passed: Chromium/Firefox/WebKit desktop/mobile targets and invalid clearing")
