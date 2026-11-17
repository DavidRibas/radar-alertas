# Manual de Operación y Negocio - RadarAlertas 🚀

Este documento resume la operativa diaria del negocio automatizado **RadarAlertas**, cómo funciona el sistema, cómo escalar los ingresos y la operativa técnica.

---

## 1. El Circuito del Negocio (100% Autónomo)

```
[ BOE Oficial cada mañana ]
            │
            ▼ (Extractor Python)
[ Detección de Inmuebles con >50% descuento ]
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
[ Generador de Vídeo TikTok/Reels/Shorts ]    [ Canal Privado VIP Telegram ]
   - Zoom 3D satelital (Google Earth)             - Ficha técnica completa
   - Vistas de dron y fotos de fachada/interior   - Enlace oficial al BOE
   - Subtítulos dinámicos y voz IA                - Datos catastrales y cargas
            │
            ▼
[ Publicación en Redes Sociales (Orgánico) ]
            │
            ▼
[ Tráfico hacia @RadarAletasSubastas_bot ]
            │
            ▼
[ Cobro Mensual Stripe (2,99 €/mes recurrentes) ]
            │
            ▼
[ Ingreso directo en tu Cuenta Bancaria (IBAN) ]
```

---

## 2. Configuración Oficial en Producción

* **Bot Oficial de Telegram:** [@RadarAletasSubastas_bot](https://t.me/RadarAletasSubastas_bot)
* **Canal Privado VIP:** [RadarAlertas VIP](https://t.me/+H9DxrDvgJLQ0YWY8) (ID: `-1004355179430`)
* **Pasarela de Pago Stripe (Modo Real):** [https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00](https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00)
* **Precio Promoción de Lanzamiento:** 2,99 € / mes recurrente.

---

## 3. Operativa Diaria

### A. Ejecución Automática (Sin que tengas que hacer nada)
* Está registrada la tarea programada en Windows **`RadarAlertasDiario`**.
* Se ejecuta automáticamente **3 veces al día**:
  - **09:00 AM** (Apertura matinal de expedientes)
  - **14:00 PM** (Actualización de mediodía)
  - **18:30 PM** (Cierre de jornada)
* Extrae las subastas del día, genera el vídeo en formato vertical en la carpeta `output/` y publica la alerta técnica en el canal VIP. Si no hay novedades, termina en 2 segundos sin duplicar.

### B. Ejecución Manual bajo demanda
* Si un día quieres forzar la búsqueda o generar un nuevo vídeo al instante:
  - Doble clic en `c:\Ideas\radar-alertas\run_diario.bat`
* Si quieres mantener el bot interactivo atendiendo altas en Telegram:
  - Doble clic en `c:\Ideas\radar-alertas\run_bot.bat`

---

## 4. Estrategia de Publicación en Redes (Para captar clientes)

Cada día que se genere un vídeo en `output/`:

1. **Dónde subirlo:**
   - TikTok (canal principal de mayor alcance orgánico sin seguidores).
   - Instagram Reels.
   - YouTube Shorts.
2. **Biografía del perfil:**
   > *"Alertas de chollos judiciales del BOE en tiempo real 🏠⚖️ Accede al radar oficial gratis:* 👉 `t.me/RadarAletasSubastas_bot`*"*
3. **Texto del vídeo (Copy):**
   > *"🚨 Piso en subasta en Madrid con un 60% de descuento sobre el precio de mercado.*
   > *Ficha técnica, cargas y enlace oficial en el link de la bio 👆.*
   > *#subastas #inversion #inmobiliaria #boe #oportunidades #madrid"*

---

## 5. Proyección de Ingresos (Modelo Recurrente)

| Suscriptores VIP | Ingreso Mensual Bruto (2,99 €/mes) | Anualizado (MRR x 12) |
| :---: | :---: | :---: |
| **50** | 149,50 € / mes | 1.794 € / año |
| **150** | 448,50 € / mes | 5.382 € / año |
| **350** | 1.046,50 € / mes | 12.558 € / año |
| **1.000** | 2.990,00 € / mes | 35.880 € / año |

*Nota: Una vez validado este canal con los primeros 100 miembros, el precio estándar subirá a 9,99 €/mes o 14,99 €/mes, multiplicando por 3 o 5 los ingresos con la misma base de usuarios.*
