# Story 04 — Entrenamiento transformer con métricas LOSO (dataset LSM Glosses)

**Estado:** completa (17/11) · **Entrega 2** · **T3** (A) · Requires: #2

## Story

Como evaluador, quiero ver top‑1 y F1 macro al dejar fuera a un señante (LOSO)
entrenando con los videos de LSM Glosses, para que el número del modelo no
venga de memorizar a la persona.

## Fuente (decisión del grupo, 17/11)

- **Dataset: LSM Glosses** (Zenodo 18330565, doi 10.5281/zenodo.18330565,
  CC BY 4.0; paper: Navarrete‑Lopez et al. 2026, *Front. Artif. Intell.*
  9:1794923). 121 glosas en español (dominio médico), 1 video por señante
  (índices 0‑11), 1 415 videos, 2.5 GB. Videos de 31‑58 frames (25‑30 fps,
  1920×1080), cara visible.
- **Reemplaza a Espejel** como fuente de entrenamiento. Espejel queda como
  evidencia del spike que motivó el pipeline solo‑manos.
- **Las 10 glosas del piloto** (decisión del grupo): HOLA, SI, NO, GRACIAS,
  CASA, AMIGO, NOS_VEMOS, POR_FAVOR, DOCTOR, AYUDA → **120 videos**
  (12 señantes × 10 glosas). Las 121 glosas completas quedan como story 05
  (entrega 3): el paper del dataset ya las cubre como baseline (F1 0.79 con
  GPU + retune), y la pipeline de frases solo valida 10.

## Acceptance criteria

- [x] Given el subconjunto de 10 glosas está extraído de los videos (un clip por
      video, con glosa y señante como metadatos) y el split por señante está
      listo, when entreno una sola vez con la configuración pre‑registrada,
      then veo top‑1 y F1 macro del señante excluido, sin que ningún clip de
      ese señante haya participado en el entrenamiento.
- [x] Given el entrenamiento terminó, when abro los resultados, then veo la
      curva de entrenamiento, la latencia de inferencia en GPU, los pesos
      entrenados y el porcentaje de videos con extracción válida.
- [ ] Given el top‑1 sale bajo, when redacto el informe, then el número se
      reporta igual, como resultado honesto. (Se verifica en la story 12;
      los números ya quedaron fijados en `metrics.json`.)

## Arquitectura (decisión del grupo, 17/11, con evidencia)

- **Transformer encoder chico**: 4 capas, 128 dimensiones, 8 heads, FFN 256,
  codificación posicional sinusoidal, token de clasificación, dropout 0.1,
  sobre la secuencia (32, 42, 3). Reemplaza al GRU + atención de la stack.
- Evidencia: el paper del propio dataset compara 8 arquitecturas con el mismo
  protocolo LOSO sobre las 121 glosas: **transformer F1 0.792 ± 0.074** (la más
  estable), GRU 0.723 ± 0.105, LSTM 0.558; 1D ResNet > 0.8 pero más disperso
  (GPU + 100 trials de retune — fuera de nuestro alcance). Paper KzSL 2026
  (Frontiers): transformer ligero (~3.5 M params, 4 capas, pooling de atención
  temporal) signer‑independent en lengua de señas de baja resource.
- Configuración **única** (sin retunes, es un piloto), GPU (decisión 17/11:
  build CUDA), semilla fija 1234.

## Ingesta de video (diseño)

1. Decodificar cada video y detectar manos en **modo video** (timestamps en ms
   monótonos crecientes) → consistencia temporal entre frames (no frame a frame
   como imagen independiente).
2. Frames sin una o ambas manos: **forward‑fill** con el valor anterior
   (estrategia del paper del dataset); el video queda descartado si las manos
   no aparecen en ningún frame (se reporta el porcentaje).
3. Normalización por la muñeca (L0 existente) → contrato (32, 42, 3).
4. Longitud variable (31‑58 frames) → **re‑muestrear el video completo a 32
   frames** (interpolación de la trayectoria; sin recorte al centro).
5. Cachear un clip por video: extracción offline y reproducible, no se repite
   en cada entrenamiento.
6. Split **LOSO por señante** (índice del video): 11 señantes train, 1 test
   ciego. El test ciego se abre **una sola vez** por configuración.

## Plan

1. Extracción de los 120 videos → clips (32, 42, 3) con metadatos (glosa,
   señante, sesión) + porcentaje de videos válidos.
2. Split LOSO por señante (11 train / 1 test).
3. Red: transformer encoder chico, configuración única pre‑registrada, GPU.
4. Un solo entrenamiento por fold → top‑1, F1 macro, curva de entrenamiento,
   latencia de inferencia y pesos.
5. Resultados listos para el informe (story 12) y, si hay tiempo, para la demo
   en vivo (story 03).

## Out of scope

- Las 121 glosas completas (story 05 → entrega 3).
- Reconocimiento en vivo desde la webcam (story 03) y umbral de confianza (08).
- Matriz de confusión (story 07).
- Comparativa de arquitecturas y retune de hiperparámetros.
- Actualización del informe (story 12) y las frases de 3 glosas (story 06).

## Resultados (17/11, corrida real en GPU, semilla 1234, reproducible)

- Extracción: **120/120 videos válidos (100 %)** → 12 folds LOSO (110 train /
  10 test ciego por fold).
- **Top‑1 LOSO: 0.917 ± 0.140** · **F1 macro: 0.893 ± 0.177**. 9/12 señantes
  con top‑1 = 1.0; peores folds: señante 0 (0.60), 11 (0.70), 6 (0.80).
- Latencia de inferencia: **0.057 ms/clip** en GPU (con `torch.cuda.synchronize`;
  el primer pase cuesta ~0.75 ms por carga de kernels).
- Artefactos en `dataset/lsm_glosses/results/`: `metrics.json` (métricas +
  curva por fold + latencia) y `model_<signer>.pt` × 12.
- Referencia honesta: el paper del dataset reporta F1 0.79 en **121 clases**
  con GPU + 100 trials de Optuna; nuestro 0.89 es sobre 10 clases y no es
  comparable directo (más clases = problema más difícil).
