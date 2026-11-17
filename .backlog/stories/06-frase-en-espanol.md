# Story 06 — Frase en español: glosario + plantillas

**Estado:** en curso (plantillas y tests listos; falta: YAML con las 10 glosas confirmadas + frases de 3 glosas) · **Entrega 2** (hackathon 16/11) · **T2** (B; F o D la toman si programan)

## Story

Como oyente, quiero **escuchar una frase de al menos 3 glosas en español** construida
con diccionario y plantillas, para que el mensaje se entienda.

## Acceptance criteria

- [ ] `glossary/LSM.yaml` con las 10 glosas confirmadas (HOLA, SI, NO, GRACIAS,
      CASA, AMIGO, NOS_VEMOS, POR_FAVOR, DOCTOR, AYUDA): cada glosa → palabra en
      español (validada en GDLSM/FENAMAS/SIGNA por C; **nadie inventa glosas**).
- [ ] Al menos 3 frases de 3 glosas cada una, formables con las 10 (p. ej.
      HOLA‑DOCTOR‑GRACIAS, HOLA‑AMIGO‑NOS_VEMOS, AYUDA‑DOCTOR‑POR_FAVOR),
      cubiertas por `pytest` y audibles en la demo.
- [x] Plantillas deterministas en `postprocess.py`: afirmativa ("…"), pregunta ("…?") y
      cortesía; glosa de pregunta como marcador.
- [x] `pytest`: 3 frases (afirmativa, pregunta, cortesía) con datos sintéticos, sin cámara.
- [x] La demo (story 01) muestra la frase en el panel y la lee con `pyttsx3`.
- [ ] El español vive **solo en el YAML** (dato); el código está en inglés.

## Plan

1. C: validación de las palabras en los glosarios de referencia.
2. B: `glossary/LSM.yaml` + plantillas + tests.
3. B: conectar a `app.py` (ya está cableado por la story 01).

## Out of scope

Sintaxis LSM real (no la inventamos) · BLEU/chrF · i18n de la interfaz (story 10).
