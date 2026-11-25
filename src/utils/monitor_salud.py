"""
Monitor Automático de Salud Integral de RadarAlertas (Coste 0,00 €).
Verifica en vivo: Web Vercel, Vercel Analytics, Catálogo JSON, Bot Render y Contador de Visitas.
Si falla algo y TELEGRAM_BOT_TOKEN + TELEGRAM_ADMIN_USER_ID están disponibles, alerta al admin.
"""
import os
import sys
import json
import urllib.request
import urllib.error


def check_url(url: str, timeout: int = 15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RadarAlertas-HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="ignore")
            return True, r.status, body
    except urllib.error.HTTPError as e:
        return False, e.code, str(e)
    except Exception as e:
        return False, 0, str(e)


def ejecutar_chequeo():
    resultados = []

    # 1. Web principal
    ok, st, body = check_url("https://radaralertas.com")
    resultados.append(("Web radaralertas.com", ok and len(body) > 10000, f"HTTP {st}"))

    # 2. Vercel Analytics
    ok, st, _ = check_url("https://radaralertas.com/_vercel/insights/script.js")
    resultados.append(("Vercel Web Analytics", ok, f"HTTP {st}"))

    # 3. Catálogo JSON
    ok, st, body = check_url("https://radaralertas.com/data/oportunidades.json")
    n_items = 0
    if ok:
        try:
            n_items = len(json.loads(body))
        except Exception:
            ok = False
    resultados.append(("Catálogo oportunidades.json", ok and n_items > 0, f"HTTP {st} ({n_items} items)"))

    # 4. Bot Render /ping
    ok, st, body = check_url("https://radar-alertas-bot-du2p.onrender.com/ping", timeout=25)
    ver = ""
    if ok:
        try:
            ver = json.loads(body).get("version", "")
        except Exception:
            pass
    resultados.append(("Bot Render 24/7", ok, f"HTTP {st} {ver}".strip()))

    # 5. Contador /api/stats
    ok, st, body = check_url("https://radar-alertas-bot-du2p.onrender.com/api/stats", timeout=20)
    vis = ""
    if ok:
        try:
            v = json.loads(body).get("visitas", {})
            vis = f"hoy={v.get('visitas_hoy', 0)}, total={v.get('visitas_total', 0)}"
        except Exception:
            ok = False
    resultados.append(("Contador visitas API", ok, f"HTTP {st} ({vis})" if vis else f"HTTP {st}"))

    return resultados


def main():
    resultados = ejecutar_chequeo()
    fallos = []
    lineas = []
    for nombre, ok, detalle in resultados:
        icono = "🟢" if ok else "🔴"
        linea = f"{icono} {nombre}: {detalle}"
        lineas.append(linea)
        print(linea)
        if not ok:
            fallos.append(linea)

    if fallos:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        admin_id = os.getenv("TELEGRAM_ADMIN_USER_ID")
        if token and admin_id:
            msg = "🚨 <b>ALERTA DE MONITOREO RADARALERTAS</b>\n\n" + "\n".join(lineas)
            data = json.dumps({"chat_id": admin_id, "text": msg, "parse_mode": "HTML"}).encode("utf-8")
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            try:
                urllib.request.urlopen(req, timeout=10)
            except Exception as e:
                print(f"No se pudo enviar alerta Telegram: {e}")
        sys.exit(1)
    print("\n✅ TODOS LOS SISTEMAS OPERATIVOS AL 100%")


if __name__ == "__main__":
    main()
