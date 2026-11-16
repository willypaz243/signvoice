# Plan hackathon — entrega 2 (16/11 → 17/11 12:45)

> La entrega 2 es **mañana** a las 12:45. Un solo ciclo de trabajo: el objetivo no es el
> sistema completo, sino un informe de V. Ingeniería con **números reales y honestos** y un
> esqueleto que corre. Regla de oro: **lo que no se entrena hoy no se inventa en el informe**;
> se etiqueta como "piloto" o "en curso" y se deja la planilla para la siguiente entrega.

## Qué tiene que salir impreso

1. **Arquitectura**: la figura 1 (ya existe en PNG modo claro) + el esqueleto `src/g11`
   corriendo con predicción simulada (`python -m g11 demo`).
2. **Datos**: conteo **real** del subconjunto Espejel descargado hoy (glosas, imágenes,
   señantes) + descripción del dataset y su licencia.
3. **Método**: GRU 2 capas + atención, input `(B,32,F,3)`, AdamW, splits LOSO por señante,
   semillas fijadas.
4. **Métricas piloto**: si la extracción de landmarks funciona, entrenar con **3‑5 glosas y
   2‑3 señantes** → top‑1, F1 macro y **matriz de confusión** (aunque salga bajo). Si no
   funciona: resultado del spike (detección sobre N imágenes) + plan B, sin números falsos.
5. **Plan de continuidad**: qué queda para la entrega 3 (10 glosas completas, stories 3‑11).

## Equipos (6 personas)

| Equipo | Quién | Qué hace hoy |
|---|---|---|
| **T1 · Esqueleto** | A + F (con el asistente de IA) | Entorno conda `signvoice` (py 3.11), `pyproject.toml`, `src/g11` (6 módulos ≤100 líneas), `.task` locales, tests, `demo` con simulación |
| **T2 · Datos** | B + C | Descarga Espejel (hoy), **spike MediaPipe sobre 20 imágenes primero**, extracción de landmarks → `.npz` + `meta.json` + `splits.json` por señante |
| **T3 · Modelo** | A (o B, cuando haya datos) | `model.py` + `train.py`, entrenamiento CPU con LOSO, top‑1, F1 macro, matriz de confusión (PNG) |
| **T4 · Informe** | D + E | Redacción V. Ingeniería (2 000‑2 500 palabras), tablas con los conteos reales, figuras, capturas, `.docx` con genoffice, **impresión** |

Contrato entre T1 y T2 (fijo desde ya, para no reescribir): `landmarks/clip_XXXX.npz` con
`(T=32, F, 3)` + `meta.json` (`senante`, `glosa`, `sesion`) + `splits.json` por señante.

## Cronograma

| Bloque | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| 16/11 tarde | Esqueleto completo + `demo` simulada corriendo | Spike 20 imágenes + conteo de glosas → lista de las 3‑5 glosas piloto | — | Esqueleto del informe I‑V + tabla de datos |
| 16/11 noche | Soporte a T3 (módulos `model`/`train`) | Extracción de landmarks del subconjunto piloto | Entrenamiento piloto + métricas + matriz | Secciones de método y datos con números reales |
| 17/11 mañana | Integración final, capturas | Splits y verificación | Métricas finales y figura | Maquetación, revisión en equipo, **imprimir y entregar 12:45** |

## Línea mínima de salvación (si todo se rompe)

Informe con: arquitectura + esqueleto corriendo (simulado) + **conteos reales** del dataset +
método + **resultado del spike** (detección sobre N imágenes, honesto) + plan de continuidad.
Aun así es una entrega visible y creíble: no hay un solo número inventado.

## Riesgos de hoy (y su plan B)

| Riesgo | Plan B |
|---|---|
| MediaPipe no detecta cuerpo (fondo/ropa negras) | Solo Hand Landmarker, normalizando por la muñeca; si también falla → MSLR o reportar solo el spike |
| Poca extracción útil (imágenes estáticas, ≈15 frames) | Pilotear con las glosas de más frames y menos señantes; reportar la limitación |
| Entrenamiento no termina a tiempo | 1 sola configuración (sin retunes), 3‑5 glosas, batch 32, semilla 1234 |
| `.task` de MediaPipe no se consiguen sin red | Se descargan hoy con internet (la demo final sí es offline) |

## Después de la entrega 2 (recuperación, 10 días)

El plan anterior de `plan.md` (fases 1‑3) sigue vigente: 10 glosas completas, stories 3‑7,
umbral de confianza, máquina limpia, informe final. Lo que se construya hoy **no se
descarta**: el esqueleto, la extracción y el entrenamiento piloto son la base de ese plan.
