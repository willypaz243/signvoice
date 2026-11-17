# Story 02 — Datos Espejel: spike, extracción y splits

**Estado:** completa (17/11) · **Entrega 2** (hackathon 16/11) · **T2**

## Story

Como evaluador, quiero ver de dónde salen los datos (dataset, licencia, las glosas piloto con
sus clips y señantes), para creerme que el experimento es reproducible.

## Fuente (verificada 16/11)

- Paper: Espejel et al. 2024, *Data in Brief* 55:110566 — doi 10.1016/j.dib.2024.110566.
- Repo: Mendeley Data doi **10.17632/6rj76z6y3n.1**, **CC BY 4.0** (datos; el paper es
  CC BY-NC). 249 clases × 7–11 señantes, 31 417 archivos (2 GB): 31 415 JPG + 1 `.xlsx`
  (clases) + 1 `.mov`. Estructura: `MSLwords1/<clase 001-249>/<señante NN+clase>/<NNNNNN.jpg>`
  (frames por clip: 1–33, promedio 12.8). Caras **anonimizadas** (bloque borroso).
- Descarga **100 % automática**: `scripts/download_dataset.py` (API pública, sin token,
  sha256 por archivo). Se registró en AGENTS.md (Commands).

## Spike (16/11, `scripts/spike_mediapipe.py`, 20 imágenes, 7 clases × señantes)

| Preprocesamiento | Pose | Manos |
|---|---|---|
| as-is | 10/20 (50 %) | 13/20 (65 %) |
| CLAHE | 12/20 | 15/20 |
| **gamma 0.5** | 10/20 | **18/20 (90 %)** |
| CLAHE+up2x | 11/20 | 16/20 |

- La imagen publicada es oscura (brillo medio 16–38/255) y con **cara borrosa**:
  el pose landmarker (que depende de la cara/torso) no supera ~55 % con ningún
  preprocesamiento probado. **Las manos con gamma llegan a 90 %.**
- El fallo es por señante (iluminación), no por clase: el 01 detecta siempre,
  el 02 nunca (sin preprocesar).

## Acceptance criteria

- [x] Descarga Espejel (CC BY 4.0, Mendeley) **100 % automatizada**: `dataset/` con las
      31 417 imágenes (no subset: 2 GB caben y el script reanuda); `.xlsx` de clases verificado.
- [x] **Spike**: registrado arriba → la evidencia apunta a **Plan B: solo manos** (pendiente
      de aprobación del grupo: contrato F 75→42).
- [x] `dataset/landmarks/clip_<sesion>.npz` con `(32, 42, 3)` por clip (Plan B: solo manos,
      2×21): **53 clips, 643 frames fuente** (good morning 137, goodbye 132, man 137,
      please 124, thank you 113), `meta.json` por clip (`senante`/`glosa`/`sesion`/`frames`)
      y `splits.json` LOSO por señante: **48 train / 5 test** (señante 11 held out).
      Gotcha: los señantes 10-11 crean carpetas `10CCC`/`11CCC` — el glob era `0*` y los
      perdía. Calidad honesta: 1 clip (07055) sale sin manos detectadas en ninguna frame.
- [x] Tabla de conteos para el informe: glosa × imágenes × señantes × frames
      (Tabla 6 del borrador, `docs/informe/entrega2_borrador.md`).
- [x] `ruff check` + `ty check` + `pytest` en verde (lógica pura con test).

## Plan

1. ~~Descarga + conteo por glosa~~ (hecho: `dataset/manifest.json` con DOI + licencia +
   las 249 palabras; 31 415 jpg, 0 fallos).
2. ~~Spike sobre 20 imágenes~~ (hecho: 90 % manos con gamma, ~55 % pose).
3. ~~Splits LOSO + extracción~~ (hecho: `Catalog.splits` testeado + 53 clips `.npz`).
4. Tabla de conteos para T4 (informe).

## Glosas piloto (pendiente de decisión del grupo)

El xlsx etiqueta en inglés; de nuestras 10 glosas solo existen: **adios→7 (goodbye),
gracias→4 (Thank you), hombre→55 (Man), casa→71 (Home)**. `hola, si, no, agua, mujer, amigo`
no están en las 249. Candidatas de saludo/cortesía con 11 señantes: Good morning (1),
Please (5), See you (6), Sign language (39, 165 frames).

## Plan B (si el spike falla)

- Fondo/ropa negras → no detecta cuerpo: pasar a **solo Hand Landmarker** y normalizar por la
  muñeca (el `normalize` de la story 01 cambia de referencia, el resto del pipeline no).
- Si también falla: registrar el resultado del spike (número honesto) y avisar a T3 para que
  el informe lleve el plan MSLR en lugar de métricas de Espejel.

## Out of scope

Las 10 glosas completas (story 05, stretch → entrega 3) · video (Espejel son imágenes) ·
etiquetado propio.
