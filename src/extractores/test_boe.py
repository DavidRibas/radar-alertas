import requests
from bs4 import BeautifulSoup

url = "https://subastas.boe.es/subastas_ava.php"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

form = soup.find("form", id="formulario") or soup.find("form")
if form:
    print("Action:", form.get("action"))
    for sel in form.find_all("select"):
        name = sel.get("name")
        opts = [(o.get("value"), o.text.strip()) for o in sel.find_all("option")[:6]]
        print(f"Select: {name} -> {opts}")
    for inp in form.find_all("input")[:15]:
        print(f"Input: {inp.get('name')} ({inp.get('type')}) = {inp.get('value')}")
