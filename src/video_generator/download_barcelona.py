import json
import urllib.request
from pathlib import Path

DEST = Path("C:/Ideas/radar-alertas/assets/templates/barcelona_aerea.jpg")
DEST.parent.mkdir(parents=True, exist_ok=True)

# Query Wikimedia API for direct URL
api_url = "https://commons.wikimedia.org/w/api.php?action=query&titles=File:Eixample_aire.jpg&prop=imageinfo&iiprop=url&format=json"
headers = {"User-Agent": "RadarAlertasApp/1.0 (info@radar-alertas.es)"}

req = urllib.request.Request(api_url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))

pages = data.get("query", {}).get("pages", {})
img_url = None
for page_id, page_val in pages.items():
    if "imageinfo" in page_val and len(page_val["imageinfo"]) > 0:
        img_url = page_val["imageinfo"][0]["url"]
        break

if img_url:
    print(f"Found URL: {img_url}")
    req_img = urllib.request.Request(img_url, headers=headers)
    with urllib.request.urlopen(req_img, timeout=20) as resp_img:
        content = resp_img.read()
        DEST.write_bytes(content)
    print(f"SUCCESS: Saved {len(content)} bytes to {DEST}")
else:
    print("Could not find image URL in API response")
