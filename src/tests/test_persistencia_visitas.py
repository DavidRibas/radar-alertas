import sys
import os
sys.path.insert(0, os.path.abspath("."))

from src.telegram_bot.database import obtener_metricas_visitas

metrics = obtener_metricas_visitas()
print("Métricas obtenidas:")
for k, v in metrics.items():
    print(f"  {k}: {v}")

assert metrics["visitas_total"] >= 2480, f"Error: visitas_total es {metrics['visitas_total']}"
print("TEST SUCCESS: Visitas persistentes garantizadas!")
