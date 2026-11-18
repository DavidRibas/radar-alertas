import os
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from dotenv import load_dotenv

load_dotenv("c:/Ideas/radar-alertas/.env")
token = os.getenv("TELEGRAM_BOT_TOKEN")

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = ssl.create_default_context()
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        # Allow legacy renegotiation in OpenSSL
        try:
            ctx.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
        except Exception:
            pass
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx
        )

s = requests.Session()
s.mount("https://", TLSAdapter())
try:
    r = s.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    print("SUCCESS with TLSAdapter!")
    print("Bot Name:", r.json().get("result", {}).get("username"))
except Exception as e:
    print("TLSAdapter Error:", e)

# Also test urllib with custom context
try:
    import urllib.request
    ctx = ssl.create_default_context()
    ctx.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getMe")
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print("SUCCESS with urllib + OP_LEGACY_SERVER_CONNECT!")
except Exception as e:
    print("urllib Error:", e)

