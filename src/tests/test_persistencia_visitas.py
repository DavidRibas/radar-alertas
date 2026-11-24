import sys
import os
sys.path.insert(0, os.path.abspath("."))

from src.telegram_bot.database import obtener_metricas_visitas

metrics = obtener_metricas_visitas()
print("Métricas reales:")
for k, v in metrics.items():
    print(f"  {k}: {v}")
