# 01 - Documento de Requisitos del Producto (PRD)

## 1. Visión y Propósito
**RadarAlertas** es una red automatizada de canales temáticos de alertas de alto valor económico (Subastas públicas, Subvenciones a fondo perdido, Licitaciones y contratos menores, Bolsas de empleo urgente).

El sistema utiliza un **motor común a coste 0 €** que:
1. Extrae oportunidades reales de fuentes públicas oficiales diariamente.
2. Genera vídeos cortos verticales (1080x1920) con voz neuronal, música y subtítulos para captar tráfico orgánico masivo en **TikTok / Instagram Reels**.
3. Dirige a los usuarios hacia canales privados de **Telegram** donde se cobra una suscripción mensual recurrente por recibir alertas en tiempo real con enlaces directos, análisis y dossiers.

---

## 2. Los 4 Canales Temáticos (Mismo motor, distinto nicho)

| Canal | Audiencia Objetivo | Gancho en TikTok | Rango de Precio Sugerido |
| :--- | :--- | :--- | :--- |
| **1. Subastas & Embargos (BOE / Seg. Social)** | Inversores, cazadores de chollos, personas buscando vivienda/coche | *"Piso en subasta por 35.000 € en Madrid"* | **15 – 25 € / mes** |
| **2. Ayudas & Subvenciones (BDNS / CCAA)** | Autónomos, familias, jóvenes, pymes | *"El Gobierno abre ayuda de hasta 6.000 € sin devolver"* | **12 – 19 € / mes** |
| **3. Licitaciones & Contratos Menores** | Pequeñas empresas de reformas, limpieza, IT, suministros | *"Contrato de 18.000 € del ayuntamiento para pintar colegios"* | **29 – 49 € / mes** |
| **4. Bolsas de Empleo Urgente** | Opositores, interinos, sanitarios, administrativos | *"Bolsa extraordinaria de empleo abierta solo durante 5 días"* | **9 – 15 € / mes** |

**Pack VIP Red Completa:** **39 € / mes** (acceso a los 4 canales con un descuento atractivo).

---

## 3. Modelo de Monetización y Embudo de Conversión

```
   [ Vídeo TikTok / Reel Viral ] (20k - 200k visualizaciones)
                │
                ▼
   [ Enlace en Bio: Bot de Telegram ]
                │
                ├───────► Canal Público Gratuito (Muestra 1 alerta censurada al día)
                │
                ▼
   [ Botón: "Desbloquear alertas completas en tiempo real" ]
                │
                ▼
   [ Pasarela de Pago: Stripe / Telegram Stars ]
                │
                ▼
   [ Acceso instantáneo al Canal VIP ]
   (Cobro recurrente mensual automático; expulsión si no renueva)
```

---

## 4. Requisitos Clave del Sistema (Restricciones del Usuario)
* **Coste mensual de infraestructura:** **0,00 €** fijos (utilizando herramientas open-source, cuotas gratuitas y cobros basados en porcentaje transaccional).
* **Mantenimiento en horas extra:** El sistema debe operar 100% desatendido mediante tareas programadas.
* **Sin atención al cliente presencial ni telefónica:** Altas, cobros, recordatorios y bajas gestionados automáticamente por el bot de Telegram.
