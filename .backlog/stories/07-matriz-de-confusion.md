# Story 07 — Matriz de confusión y análisis de error

**Estado:** pendiente (va con la 04) · **Entrega 2** (hackathon 16/11) · **T3** (A)

## Story

Como evaluador, quiero ver la **matriz de confusión** y los pares de glosas más confundidos,
para explicar el error con evidencia.

## Acceptance criteria

- [ ] Matriz de confusión en PNG (modo claro, texto legible en PDF) sobre el test ciego
      del piloto (story 04).
- [ ] Top 3 pares de glosas más confundidos, con el % de cada par, en `data/results/`.
- [ ] Un párrafo‑semilla para T4: qué se confunde y por qué (semejanzas visuales).
- [ ] `pytest` para la función que arma la matriz (función pura, sin GPU).

## Plan

1. A: función pura de matriz de confusión + test (reusa `train.py`).
2. A: PNG + top 3 pares → `data/results/`.
3. A: nota de 3‑4 líneas para la sección de métricas del informe.

## Out of scope

Métricas de secuencia (BLEU) · comparación con otros modelos.
