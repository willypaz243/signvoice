# Story 06 — Frase en español: glosario + plantillas

**Estado:** pendiente · **Entrega 2** (hackathon 16/11) · **T2** (B; F o D la toman si programan)

## Story

Como oyente, quiero **escuchar una frase de 2‑3 palabras en español** construida con
diccionario y plantillas, para que el mensaje se entienda.

## Acceptance criteria

- [ ] `glossary/LSM.yaml` con las glosas del piloto: cada glosa → palabra en español
      (validada en GDLSM/FENAMAS/SIGNA por C; **nadie inventa glosas**).
- [ ] Plantillas deterministas en `postprocess.py`: afirmativa ("…"), pregunta ("…?") y
      cortesía; glosa de pregunta como marcador.
- [ ] `pytest`: 3 frases (afirmativa, pregunta, cortesía) con datos sintéticos, sin cámara.
- [ ] La demo (story 01) muestra la frase en el panel y la lee con `pyttsx3`.
- [ ] El español vive **solo en el YAML** (dato); el código está en inglés.

## Plan

1. C: validación de las palabras en los glosarios de referencia.
2. B: `glossary/LSM.yaml` + plantillas + tests.
3. B: conectar a `app.py` (ya está cableado por la story 01).

## Out of scope

Sintaxis LSM real (no la inventamos) · BLEU/chrF · i18n de la interfaz (story 10).
