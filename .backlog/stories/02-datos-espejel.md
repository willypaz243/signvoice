# Story 02 — Datos Espejel: spike, extracción y splits

**Estado:** pendiente (arranca D1) · **Entrega 2** (hackathon 16/11) · **T2** (B + C)

## Story

Como evaluador, quiero ver de dónde salen los datos (dataset, licencia, las glosas piloto con
sus clips y señantes), para creerme que el experimento es reproducible.

## Acceptance criteria

- [ ] Subconjunto Espejel descargado hoy (CC BY 4.0, Mendeley): las **3‑5 glosas piloto**
      con más frames, ≈ 500‑1 000 imágenes, **no** las 31 442.
- [ ] **Spike primero** (~30 min): MediaPipe Pose + Hands sobre 20 imágenes; queda registrado
      el % de detección (cuántas de 20 encuentran cuerpo y manos).
- [ ] `data/landmarks/clip_XXXX.npz` con `(32, 75, 3)` por clip (33 pose + 2×21 manos),
      `data/meta.json` por clip con `senante`/`glosa`/`sesion`, y `data/splits.json`
      **por señante** (LOSO).
- [ ] Tabla de conteos para el informe: glosa × imágenes × señantes × frames.
- [ ] `ruff check` + `pytest` en verde (el script de extracción reusa `g11.landmarks`
      de la story 01; la parte pura —splits, metadatos— tiene test).

## Plan

1. C: descarga en Mendeley + conteo de imágenes por glosa → lista de las 3‑5 glosas piloto.
2. B: spike sobre 20 imágenes (mismo código que usará la extracción completa).
3. B: extracción completa → `.npz` + `meta.json` + `splits.json`.
4. C: tabla de conteos para T4 (informe).

## Plan B (si el spike falla)

- Fondo/ropa negras → no detecta cuerpo: pasar a **solo Hand Landmarker** y normalizar por la
  muñeca (el `normalize` de la story 01 cambia de referencia, el resto del pipeline no).
- Si también falla: registrar el resultado del spike (número honesto) y avisar a T3 para que
  el informe lleve el plan MSLR en lugar de métricas de Espejel.

## Out of scope

Las 10 glosas completas (story 05, stretch → entrega 3) · video (Espejel son imágenes) ·
etiquetado propio.
