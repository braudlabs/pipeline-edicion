# Ecommerce Andrómeda: versiones de Claude y Codex en paralelo

> Anuncio ecommerce/Andrómeda se edita en paralelo — Codex en ecommerce-andromeda/ (V01–V05), Claude en ecommerce-andromeda-claude/ (C01–C06, la vigente en CURRENT-VERSION.json); no tocar la carpeta del otro.

El 2026-10-14 Ale encargó a Claude el mismo anuncio (azul calvo + bigote daliniano, lavandería) que Codex ya editaba en `ecommerce-andromeda/` (V01→V05 ese mismo día). La pieza de Claude vive en `ecommerce-andromeda-claude/c01/` con su propio `CURRENT-VERSION.json`; la de Codex no se modifica. Ale da feedback en ambos hilos y `estilo-editor/FEEDBACK-ALE.md` es compartido (releerlo justo antes de editarlo: Codex lo cambia a menudo).

Feedback de Ale aplicable a este anuncio: subtítulos centrados para Meta; audio nativo de todos los clips, también el hook (voz generada sincronizada); relleno detrás + contorno delante sí pero sin abusar; gag de la sudadera en blanco y negro sin subtítulos; nada de motion en la pantalla de la maquinita. Sobre C01: «el hook es la polla», también el cartel impreso en la persiana y «OTRA PUTA VEZ»; el resto «fuente muy pequeña, demasiado a los lados (se cortará en meta) y no es estética». Desde C02 los subtítulos de lectura son frases cortas grandes en una línea, centradas, tinta dentro de x≈100–980, con el lenguaje del hook.

2026-10-15: con la entrega completa (17 unidades, 85,417 s) Ale pidió «terminar el vídeo» → C04 en `ecommerce-andromeda-claude/c04/` (C03 intacta). La música es la toma 2 de ElevenLabs de `ecommerce-andromeda-claude/music/` (spec funk 122 BPM que Ale pegó en el chat y cuyas dos tomas aprobó); el brief del director (`08_MUSICA`) describe otra pieza (118 BPM pizzicato/fagot/piano). Discrepancia señalada a Ale, sin resolver: no tratar ninguna de las dos como aprobada.

Sobre C04 Ale dijo «overall no está mal» pero rechazó la tinta marino/azul BRAUD (solo blanco + azul claro), los rótulos pegados al lateral (Meta recorta bordes: x 100–980 obligatorio, también en lo ya aprobado), el eco «mierda mierda», la tarjeta «nuevo ángulo» poco integrada y la música (la toma 2 «frena mucho a la mitad»). Aprobó una toma 3 continua y pidió «más salsa» (luces, objeto que refleja). C05 aplica todo; detalle en `estilo-editor/FEEDBACK-ALE.md`. C05 se entregó a 24 fps y a 144 fps el 15/10 (verify TOTAL OK). Ale no corrigió nada de C05 y pidió «otra versión con más efectos aún, un upgrade infernal».

C06 (`ecommerce-andromeda-claude/c06/`) añade a C05:
- una cámara digital: golpes, escalones, empujes, caída, temblor y barrido;
- unos 30 efectos, cada uno atado a una palabra o acción.

Montaje, audio y rótulos no cambian. Se entregó a 24 fps el 15/10 (verify TOTAL OK, 0 fotogramas fuera del margen) y está pendiente de veredicto. La cámara y los efectos están en `src/fx/`, y el registro en `c06/CAMBIOS.md`. Ale vuelve a pedir más densidad de efectos («más salsa» en C04, «upgrade infernal» tras C05): no quedarse corto, pero sin tocar lo aprobado ni la pantalla de la maquinita.

**Why:** dos agentes escriben a la vez en el mismo repo y Ale compara resultados.
**How to apply:** al retomar, leer ambos CURRENT-VERSION.json y el feedback más reciente; trabajar solo en la carpeta propia. Ver [Estudio del estilo del editor](estudio-estilo-editor.md) y [Render y herramientas locales (Remotion, iCloud, mattes)](remotion-render-local.md).
