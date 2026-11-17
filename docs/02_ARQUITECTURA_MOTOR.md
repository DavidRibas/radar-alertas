# 02 - Arquitectura Técnica del Motor

## 1. Diagrama de Flujo Modular

```
┌────────────────────────────────────────────────────────┐
│                   CAPA DE EXTRACCIÓN                   │
│   [BOE Scraper]    [BDNS Scraper]    [PLACSP Scraper]  │
└───────────────────────────┬────────────────────────────┘
                            │ Payload Normalizado (JSON)
                            ▼
┌────────────────────────────────────────────────────────┐
│              CAPA DE TRANSFORMACIÓN & GUION            │
│   - Filtrado de oportunidades reales (score de calidad)│
│   - Generación de guion corto (<35 seg) con gancho     │
│   - Generación de ficha técnica para Telegram          │
└───────────────────────────┬────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│     GENERADOR DE VÍDEO    │ │      TELEGRAM ENGINE      │
│ - Edge-TTS (Audio voz IA) │ │ - Publica en canal VIP    │
│ - Pillow (Composición)    │ │ - Publica en canal Free   │
│ - FFmpeg (Render vertical)│ │ - Gestiona pagos & bajas  │
└─────────────┬─────────────┘ └───────────────────────────┘
              ▼
┌───────────────────────────┐
│     PUBLICADOR SOCIAL     │
│ - TikTok API / Scheduler  │
│ - Instagram Reels         │
└───────────────────────────┘
```

---

## 2. Pila Tecnológica (Stack a Coste Cero)

| Componente | Tecnología Seleccionada | Justificación / Coste |
| :--- | :--- | :--- |
| **Lenguaje Core** | Python 3.12 | Rápido, multiplataforma, rico en librerías de scraping y multimedia. |
| **Voz Neuronal (TTS)** | `edge-tts` (Microsoft) | Voces neuronales en español (ej. `es-ES-AlvaroNeural`, `es-ES-ElviraNeural`). **0 € y sin API key.** |
| **Composición de Vídeo** | `moviepy` + `FFmpeg` | Renderizado por línea de comandos, plantillas 1080x1920 a 30fps. **0 €.** |
| **Extracción Web** | `requests` + `beautifulsoup4` / `playwright` | Capacidad de navegar portales estáticos y JS del gobierno. **0 €.** |
| **Bot de Telegram** | `python-telegram-bot` | Framework robusto para manejar pagos integrados (Telegram Stars / Stripe). **0 €.** |
| **Base de Datos** | SQLite local (o Supabase / Turso en capa gratis) | Almacenamiento de usuarios, subastas procesadas y estado de suscripciones. **0 €.** |

---

## 3. Modelo de Datos Unificado (Payload Normalizado)

Todos los extractores deben emitir un objeto estándar:

```json
{
  "id": "SUB-2026-MAD-001",
  "categoria": "subasta",
  "titulo": "Piso 85m² en Madrid (Barrio del Pilar)",
  "ubicacion": "Madrid, Madrid",
  "valor_tasacion": 210000.00,
  "precio_salida": 48000.00,
  "ahorro_porcentaje": 77,
  "fecha_limite": "2026-12-05T18:00:00",
  "url_oficial": "https://subastas.boe.es/...",
  "detalles_clave": [
    "Sin cargas hipotecarias previas",
    "Depósito requerido: 2.400 €",
    "Inmueble desocupado según expediente"
  ],
  "imagenes": ["https://.../foto1.jpg"]
}
```
