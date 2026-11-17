# 03 - Plan de Implementación y Fases

## Fase 1: El Motor Audiovisual (Prueba de Concepto en Local)
* **Objetivo:** Conseguir que con un script de Python le pasemos un JSON de prueba (ej. una subasta o ayuda) y nos escupa un archivo `video_tiktok.mp4` vertical con voz en español, música y textos con gancho.
* **Entregables:**
  * Script de síntesis de voz con `edge-tts`.
  * Generador de plantilla gráfica (tarjeta con título, foto, precio tachado y precio ganga).
  * Renderizador con FFmpeg que une voz + imagen + música de fondo.

## Fase 2: El Primer Conector Oficial (Extracción del BOE / Subastas)
* **Objetivo:** Automatizar la búsqueda de las 3 mejores subastas de inmuebles/vehículos del día con filtro anti-cargas.
* **Entregables:**
  * Scraper que consulta el portal del BOE o su RSS/API.
  * Filtro que descarta subastas con cargas complejas o poco atractivas.
  * Formateador que envía la alerta a la Fase 1 (generador de vídeo) y genera el post de Telegram.

## Fase 3: El Bot de Telegram con Pagos y Membresía
* **Objetivo:** Un bot que gestione altas, cobro de tarjeta con Stripe / Telegram Stars y entregue enlace de invitación único e intransferible.
* **Entregables:**
  * Bot en Python con comandos `/start`, `/suscribirme`, `/estado`.
  * Integración de pasarela de pago recurrente.
  * Tarea periódica de expulsión automática para usuarios con pago fallido.

## Fase 4: Publicador Automático y Escalado a más Canales
* **Objetivo:** Subida automática del MP4 a TikTok mediante API o navegador automatizado y clonación del conector para Subvenciones y Licitaciones.
