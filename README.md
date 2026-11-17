# RadarAlertas - Red Automatizada de Canales de Alertas

Plataforma modular para la extracción de alertas públicas (Subastas BOE, Subvenciones, Licitaciones, Empleo Público), generación automática de contenido vertical en vídeo para TikTok/Reels y monetización recurrente mediante canales de Telegram por suscripción.

## 🎯 Arquitectura de Alto Nivel

```
[ Fuente Pública ] ──► [ Extractor ] ──► [ Generador de Guión ]
                                                 │
                                                 ▼
[ Canal Telegram ] ◄── [ Bot Cobro ] ◄── [ Generador de Vídeo (Edge-TTS + FFmpeg) ]
(Suscripción €)                                  │
                                                 ▼
                                        [ Publicador TikTok ]
```

## 📁 Estructura del Proyecto

* `docs/`: Documentación del producto (PRD, Arquitectura, Roadmap).
* `src/extractores/`: Scrapers y conectores de fuentes públicas oficiales (BOE, BDNS, PLACSP).
* `src/video_generator/`: Motor de generación de voz neuronal (Edge-TTS), montaje audiovisual (FFmpeg) y subtitulado dinámico.
* `src/publishers/`: Automatización de subida a TikTok y redes sociales.
* `src/telegram_bot/`: Bot de gestión de usuarios, pasarela de pago (Stripe/Telegram Stars) y control de accesos/expulsiones.
* `assets/`: Plantillas gráficas (1080x1920) y pistas de audio de fondo sin copyright.

## 🚀 Requisitos y Setup

Python 3.12+ y FFmpeg. Ver `docs/02_ARQUITECTURA_MOTOR.md` para más detalles.
