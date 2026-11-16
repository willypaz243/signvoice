# Story 05 — Las 10 glosas completas (stretch → entrega 3)

**Estado:** pendiente (stretch) · **Entrega 2 solo si sobra tiempo, si no entrega 3** · **T3** (A)

## Story

Como señante, quiero que el sistema reconozca **las 10 glosas**, para poder armar mensajes de
varias palabras.

## Acceptance criteria

- [ ] Subconjunto completo de las 10 glosas (≈ 1 600 imágenes) extraído con el mismo pipeline
      de la story 02.
- [ ] Mismo protocolo de la story 04 (GRU+atención, AdamW 1e‑3, batch 32, semilla 1234, LOSO).
- [ ] top‑1, F1 macro y matriz de confusión actualizados para las 10 glosas.

## Cuándo se hace

Es el primer candidato a aplazar: si el piloto (3‑5 glosas) no está entrenado a media noche
del 16/11, la story 05 entera va a la entrega 3 y el informe se cierra con el piloto
etiquetado como tal.

## Out of scope

Phrases de 2‑3 palabras en vivo (story 06) · umbral de confianza (story 08).
