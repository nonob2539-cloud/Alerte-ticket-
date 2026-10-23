import os, re, sys, requests
from playwright.sync_api import sync_playwright

URL = "https://fr.ra.co/events/2392797"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
SOLD_OUT = re.compile(r"épuisé|sold out|complet|indisponible", re.I)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(locale="fr-FR")
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    title = page.title()
    text = page.inner_text("body")
    b.close()
    
print("TITRE:", title)
print("DEBUT:", text[:300])
if "Spectrum Waves" not in title:
    print("Page mal chargée, on ignore")
    sys.exit(0)

if SOLD_OUT.search(text):
    print("Toujours épuisé")
else:
    print("ALERTE : plus de mention d'épuisement")
    requests.post(WEBHOOK, json={"content": f"🎟️ Des billets sont peut-être dispos ! {URL}"})
