# Story 04 — Entrenamiento GRU + atención con métricas LOSO

**Estado:** pendiente (cuando T2 tenga datos) · **Entrega 2** (hackathon 16/11) · **T3** (A)

## Story

Como evaluador, quiero ver top‑1 y F1 macro al dejar fuera a un señante (LOSO) en el
entrenamiento, para que el número del modelo no venga de memorizar a la persona.

## Acceptance criteria

- [ ] `src/g11/model.py` (GRU 2 capas + atención temporal, salida softmax) y
      `src/g11/train.py`, cada uno ≤ 100 líneas.
- [ ] Configuración **única** (sin retunes, es un piloto): AdamW 1e‑3, batch 32, dropout 0.3,
      semilla 1234, input `(B, 32, 75, 3)`.
- [ ] **LOSO** con los señantes disponibles en el subconjunto piloto (2‑3 folds).
- [ ] Salida en `data/results/`: top‑1 por señante excluido, F1 macro, latencia de
      inferencia (CPU), curva de entrenamiento (PNG, modo claro).
- [ ] El test ciego se abre **una sola vez** por configuración.
- [ ] Si el top‑1 sale bajo (60‑75 %), **se reporta igual**: es un resultado, no un fracaso.

## Plan

1. A: `model.py` + `train.py` (contrato: lee `data/landmarks/` + `splits.json`).
2. A: 1 entrenamiento por fold, CPU, sin retunes.
3. A: métricas → `data/results/` + PNGs para T4.

## Out of scope

Comparativa de arquitecturas · GPU (queda para el entrenamiento final) · 10 glosas
(story 05) · retunes de hiperparámetros.
