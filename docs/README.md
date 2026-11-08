# Documentación — Traductor de Lengua de Señas Mexicana (LSM) a voz

**Práctica de Inteligencia Artificial — Grupo 11**
Área: Aprendizaje supervisado · Subárea: Visión por computadora
Problema: *Reconocimiento de señas y conversión a voz*

---

## Cómo está organizada esta carpeta

```
docs/
├── README.md                          ← este archivo (índice)
├── informe/
│   └── entrega1_informe.md            ← BORRADOR DEL INFORME DE LA 1.ª ENTREGA (I-IV)
└── investigacion/
    ├── 01_estado_del_arte.md          ← qué se ha hecho, taxonomía, modelos, SOTA, retos
    ├── 02_datasets.md                 ← datasets de LSM y de referencia + protocolo de captura
    ├── 03_proyectos_y_herramientas.md ← proyectos reales, repos, stack técnico, TTS
    ├── 04_arquitectura_propuesta.md   ← pipeline, decisiones de diseño, plan de experimentos
    ├── 05_lsm_y_marco_legal.md        ← lingüística de la LSM, marco legal, ético y social
    ├── 06_glosario.md                 ← términos clave para estudiar
    ├── referencias.md                 ← bibliografía verificada (APA 7 + enlaces)
    └── referencias.bib                ← la misma bibliografía en BibTeX
```

## Orden de estudio recomendado

| # | Documento | Para qué sirve |
|---|-----------|----------------|
| 1 | `01_estado_del_arte.md` | Entender el problema: qué es SLR, tipos, modelos que funcionan, por qué es difícil. |
| 2 | `05_lsm_y_marco_legal.md` | Entender la LSM como lengua (parámetros, dactilología vs. ideologías) y el marco legal/ético. |
| 3 | `02_datasets.md` | Conocer los datos disponibles y cómo vamos a grabar los nuestros. |
| 4 | `03_proyectos_y_herramientas.md` | Qué existe implementado (código abierto y comercial) y con qué herramientas se hace. |
| 5 | `04_arquitectura_propuesta.md` | Nuestro diseño concreto: diagramas, modelos a comparar, métricas, riesgos. |
| 6 | `06_glosario.md` | Definiciones rápidas para defender el informe en clase. |
| 7 | `informe/entrega1_informe.md` | El documento que se imprime. |

## Datos duros que conviene memorizar para la defensa

- **70 millones** de personas sordas en el mundo; **>80 %** en países de ingreso bajo y medio; existen **más de 300 lenguas de señas** y **no existe una lengua de señas universal** (ONU, 2021).
- **430 millones** de personas requieren rehabilitación auditiva; se proyectan **>700 millones en 2050** (OMS).
- México, Censo 2020: **6 179 890 personas con discapacidad (4,9 %)** de la población (INEGI).
- La LSM fue reconocida oficialmente como **lengua nacional** el **10 de junio de 2005**, y la Ley General para la Inclusión de las Personas con Discapacidad la reconoce como patrimonio lingüístico de los sordos de México.
- El dataset público de ASL más grande (**WLASL**, 2 000 palabras, +100 señantes) deja a los mejores modelos base en **62,63 % top-10** → el problema **no está resuelto**.
- En LSM, los mejores reportes en vocabularios pequeños (30 signos) llegan a **97 %**, pero caen a **63–65 % top-1** cuando el vocabulario crece a 62 clases → **la escala es el reto real**.

## Generar el PDF del informe

```bash
cd docs/informe
pandoc entrega1_informe.md -o entrega1.pdf --pdf-engine=xelatex -V geometry:margin=2.5cm \
  -V mainfont="Liberation Serif" -V fontsize=12pt --toc
# Alternativa: abrir el .md en Typora / VS Code + "Markdown PDF" y exportar.
```

> Los diagramas están en **Mermaid**. Para que salgan en el PDF impreso, exportarlos como imagen
> (`npx @mermaid-js/mermaid-cli -i entrega1_informe.md -o figs/`) o pegar las capturas desde
> <https://mermaid.live>. En la sección `04_arquitectura_propuesta.md` están las versiones editables.

## Fuentes

Toda cifra y toda referencia citada provienen de artículos indexados, páginas oficiales (OMS, ONU,
INEGI, Cámara de Diputados de México) o repositorios públicos, con fecha de verificación
**5 de noviembre de 2026**. Detalle en `investigacion/referencias.md`.

## Checklist antes de imprimir la 1.ª entrega

- [ ] Portada con universidad, asignatura, profesor(a), los integrantes reales con matrícula y fecha.
- [ ] Índice con números de página; cuerpo en Times New Roman 12, interlineado 1.5, márgenes 2.5 cm.
- [ ] Borrar del informe las notas marcadas **"antes de imprimir"** y la sección **"Notas de edición"**.
- [ ] Diagramas exportados a imagen y numerados (Figura 1, 2, …) con su título en el texto.
- [ ] Completar los autores de `Rodriguez et al. (2025)` y `Becerril-Carrillo et al. (2025)` en
      `referencias.md` / `referencias.bib` desde la página oficial del artículo.
- [ ] Verificar que cada cifra del informe esté respaldada en `referencias.md` (≈ 30 fuentes,
      18 con doi); borrar lo que no se pueda respaldar.
- [ ] Los 5 integrantes que defienden responden en voz alta cualquier fila de `06_glosario.md`.
- [ ] Toda meta de desempeño aparece como **objetivo**, nunca como resultado.

> Estado de los diagramas: los **20 bloques Mermaid** de `docs/` fueron validados con el validador
> de sintaxis Mermaid (todos válidos al 5-nov-2026). Si alguien edita un diagrama, hay que
> revalidarlo en <https://mermaid.live> antes de exportarlo.

### Convención de color en los diagramas

Los nodos **no llevan relleno**: el color va **solo en el borde**, y el resto lo pone el tema oscuro
de Mermaid. Al editar o crear diagramas, mantener esta forma:

```
style Nodo fill:none,stroke:#e8b339,stroke-width:2.5px
```

| Color del borde | Código | Significado en los diagramas |
|---|---|---|
| Amarillo | `#e8b339` | Modelos / núcleos de la IA (el bloque que se compara o se estudia) |
| Verde | `#8bc34a` | Post-proceso lingüístico, cuerpo (AM) y salida en español |
| Naranja | `#f0863c` | Etapa de entrada/salida (cámara, TTS), opciones recomendadas y advertencias |
| Azul | `#4dabf5` | Contexto social / marco teórico |
| Rosa | `#e0559c` | Conjunto de **prueba ciego** (no se toca) |
| Rojo | `#ef5350` | Riesgo de alta severidad |

**Base de texto claro (en los 20 diagramas del repo).** Cada bloque `mermaid` empieza con esta línea:

```
%%{init: {'theme':'dark','themeVariables':{'darkMode':true,'primaryTextColor':'#e6e6e6','nodeTextColor':'#e6e6e6','edgeLabelColor':'#e6e6e6','lineColor':'#9a9a9a'},'themeCSS':'.nodeLabel,.nodeText,.edgeLabel,.label{color:#e6e6e6!important}'}}%%
```

Por qué hace falta: en Mermaid 11 las etiquetas de `flowchart`, `graph` y `classDiagram` **no son SVG**:
son HTML (`div.nodeLabel`) dentro de un `foreignObject`, y se colorean con la propiedad CSS `color`; las
de `gantt` sí son `text` SVG con `fill`. Con el tema claro salen en `#333` → **negro sobre fondo negro**.
`primaryTextColor`/`nodeTextColor`/`edgeLabelColor` y la regla `.nodeLabel{color:… !important}` cubren
los dos casos, y `lineColor` aclara fechas, rejillas y puntas de flecha.

Comprobado: se renderizaron los **20 bloques** del repo con Mermaid 11, `securityLevel: 'strict'`, fondo
`#1e1e24` y una hoja de estilos que fuerza `#333` en `text` y `.nodeLabel`: **20/20 renderizan y 0 de
1035 textos quedan oscuros**. Sin esa línea, un bloque de flujo típico dejaba **18 de 22** etiquetas en `#333`.

**Excepción:** `timeline`, `mindmap` y `gantt` **no admiten** `style` ni `classDef`; los colores los pone
el tema: los recuadros con la escala `cScale0…cScale11` (**relleno**) y el texto con `cScaleLabelN`
(**negro** en el tema claro, ilegible sobre fondo oscuro). Ahí se controla con la directiva
`%%{init: … }%%` de la primera línea. Ejemplo recortado (la versión completa está en
`investigacion/01_estado_del_arte.md`, línea de tiempo):

```
%%{init: {'theme':'dark','themeVariables':{'darkMode':true,'primaryTextColor':'#e6e6e6','titleColor':'#f2f2f2','cScaleLabel0':'#e8b339','cScaleLabel1':'#f0863c'},'themeCSS':'.timeline-node .node-bkg{fill:none!important;stroke-width:2.5px!important}.timeline-node.section--1 .node-bkg{stroke:#e8b339!important}.timeline-node.section--1 [dy]{fill:#e8b339!important}[font-weight]{fill:#f2f2f2!important}.lineWrapper [stroke]{stroke:#9a9a9a!important}'}}%%
```

Reglas útiles (verificadas renderizando con Mermaid 11, `securityLevel: 'strict'`, fondo `#1e1e24`):
- el recuadro es un `path.node-bkg` **sin borde**: se quita el relleno con `fill:none!important` y el
  color se pone en el **borde** con `stroke` (2.5 px);
- cada franja trae la clase `.section--1` (1.ª), `.section-0`, `.section-1`, … **en orden de aparición**,
  así que se le asigna un color distinto a cada periodo;
- el texto se controla con `cScaleLabelN` en `themeVariables` (N = orden de aparición) **y**, si el visor
  impone su propio `fill`, con `.timeline-node.section-N [dy]{fill:… !important}`: todos los textos del
  `timeline` llevan atributo `dy`, y ese selector gana a la hoja de estilos del visor;
- **dentro de `themeCSS` solo sobreviven selectores de clase y de atributo**: los de etiqueta (`text`,
  `tspan`, `path`) o que lleven `>` hacen que el saneador de Mermaid (DOMPurify) **descarte todo el
  `themeCSS`** del bloque (el diagrama vuelve a salir con relleno y texto negro);
- `themeCSS` se aplica a **todos** los diagramas de la página → **escopar** los selectores
  (`.timeline-node …`); `[font-weight]` (título) y `.lineWrapper [stroke]` (eje, que viene con
  `stroke="black"`) van sin escopar: en un visor oscuro dejan ese texto casi blanco, que es lo que toca;
- para imprimir en papel blanco: `'theme':'default'`, sin `darkMode:true`, y texto oscuro
  (`cScaleLabelN:'#333333'`, `[dy]{fill:#333333 !important}`, `[font-weight]{fill:#111111 !important}`),
  manteniendo los bordes de color;
- **exportar para el PDF impreso:** quita la línea de base oscura del bloque que exportes (o cámbiala a
  `'theme':'neutral'` con texto `#333333`) y usa `-b white`. Con `-t dark -b transparent` el texto casi
  blanco **desaparece sobre el papel**: la línea `style … fill:none` sí se imprime (el borde), el texto no.
- al exportar para pantalla/visor oscuro: `mmdc -i fig.mmd -o fig.svg -t dark -b transparent --cssFile borde.css`.
