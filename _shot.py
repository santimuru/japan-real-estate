"""Visual QA for the multi-page Japan RE app: screenshot each page, scroll-tiled."""
import time, os
from playwright.sync_api import sync_playwright

OUT = "C:/Users/biconsulting/portfolio/japan-real-estate/_qa"
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

BASE = "http://localhost:8603"
PAGES = [
    ("0_home", BASE + "/"),
    ("1_divergence", BASE + "/Japan_Overview"),
    ("2_tokyo", BASE + "/Tokyo_Deep_Dive"),
    ("3_about", BASE + "/About"),
]
VH = 1000

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1500, "height": VH})
    for name, url in PAGES:
        pg.goto(url, wait_until="networkidle", timeout=70000)
        time.sleep(6)  # charts + maps render
        cont = pg.query_selector('[data-testid="stMainBlockContainer"]') or pg.query_selector('[data-testid="stMain"]')
        total = pg.evaluate("(e)=>e ? e.scrollHeight : 0", cont)
        n = max(1, min(7, (total // VH) + 1))
        for i in range(n):
            pg.evaluate(f"()=>{{const m=document.querySelector('[data-testid=stMain]'); (m||window).scrollTo(0,{i*VH});}}")
            time.sleep(1.1)
            pg.screenshot(path=f"{OUT}/{name}_{i:02d}.png")
        err = pg.evaluate("""()=>[...document.querySelectorAll('[data-testid=stException],.stException')].map(e=>e.innerText).slice(0,2)""")
        print(f"{name}: {n} tiles ({total}px) errors={err}")
    b.close()
