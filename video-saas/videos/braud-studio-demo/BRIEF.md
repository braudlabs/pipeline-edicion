# Encargo · demo SaaS de BRAUD Studio (vertical e-commerce)

**Pedido de Ale (15/10/2026):** estudiar las funcionalidades del dashboard, escribir la voz en off y producir un vídeo estilo demo de software, con la interfaz real (mismo diseño, mismo dashboard), para enseñarlo en llamadas de venta a e-commerce.

**Para qué sirve:** la Biblia de closers lo da como pendiente, como respuesta a la objeción «¿Sabré manejarlo?» (7 de 39 llamadas). Debe dejar claro que se maneja hablando, que el cliente dirige y aprueba, y que dentro hay un proceso de producción completo.

## Estado

| Paso | Estado |
| --- | --- |
| Inventario de funcionalidades | Hecho. Ver `FUNCIONALIDADES.md` |
| Guion de locución | G03 entregado, sin aprobar. G01 y G02 en `archive/`. Ver `GUION-LOCUCION.md` |
| Afirmaciones sobre Meta, subida y montaje final | Ale las pidió el 15/10. Falta confirmar que funcionan en producción; el frontal las marca como pendientes |
| Locución | Recibida (ElevenLabs, Guillermo). Acelerada a 1,08× y con «pumicar» corregido: `assets/locucion.wav`, 2:02,8 |
| Caso que se ve dentro del dashboard | Ecommerce Andrómeda, con datos reales. Ver `DATOS-DEMO.md` |
| Dirección visual | D: fondo negro con brillo cobalto e interfaz clara. Ver `styleframes/contacto-v2.jpg` |
| Montaje | En Remotion (`remotion/`). Avance 01 (bloques 1–5, 31 s) enviado y sin veredicto. Faltan los bloques 6–21 |

## Formato

- 16:9, 1920×1080, unos 2:30 (versión corta de unos 2:00).
- Se ve en pantalla compartida durante una llamada, así que el texto de la interfaz tiene que leerse a tamaño de Meet: hay que acercar la cámara a cada zona y no enseñar la pantalla entera mucho rato.

## Interfaz: cómo traerla al vídeo

El frontal es DOM puro, sin canvas: unos 200 elementos y unos 10 KB de HTML en el inicio. Usa `-apple-system` (SF Pro) y tokens en `tokens.css` y `theme.css`:
- acento `#367dff`;
- papel `#f2f5f8`;
- tinta `#243448`;
- radio 22 px;
- vidrio con `backdrop-filter`.

Tiene tema claro y oscuro, y tres inicios (Actual, Líquido y Mosaico). El de referencia es el Actual.

**Propuesta:** levantar el frontal real con un `demo/state.json` propio, con el caso e-commerce cargado, sin tocar la copia de `~/Downloads`.
- De cada estado se captura el DOM del `#app`.
- Esos DOM se montan en Remotion con el CSS original. Así la interfaz es idéntica, vectorial y nítida en cualquier zoom.
- Las animaciones salen deterministas: cursor, tecleo en el chat, clic en «Usar apertura», cotización, aprobado…

**Probado el 15/10** con Chrome headless y CDP, sin dependencias nuevas:
- **Inicio:** 0 píxeles distintos entre el frontal vivo y su DOM congelado (3024×1800, DPR 2).
- **Guion:** solo cambia el 0,9 % de los píxeles, en el chat lateral, porque no se conserva su `scrollTop`. Hay que guardarlo al capturar.

El script de prueba está en `tools/cdp-capture.mjs`.

La alternativa es grabar pantalla del frontal. Es más rápida, pero los zooms quedan blandos y las transiciones dependen del tiempo real.

## Decisión pendiente: qué pieza se construye dentro del dashboard

Los datos de muestra traen un anuncio de BRAUD para **agencias** (el tío Jerry), con Founders Picks vacío y ceros en Taller y Actividad. Para vender a e-commerce, el caso tiene que ser e-commerce. Opciones:

1. **El anuncio «Ecommerce Andrómeda»**, el de la lavandería que se está editando ahora:
   - tiene clips reales en disco y no cuesta generar nada;
   - encaja con el reencuadre de los closers: «los mismos creativos que produce el sistema te han traído hasta aquí».
2. **Una marca de producto ficticia** (la propia app usa de ejemplo una botella reutilizable):
   - se parece más a lo que pide el cliente con «quiero verlo con mi marca»;
   - pero hay que generar producto y clips, con coste.

En los dos casos hay que llenar Founders Picks, Taller y Actividad, siempre **sin cifras inventadas** (regla del pipeline, ver abajo):
- en el Taller, resultados reales de BRAUD (`resultados.html` de la landing) o el formulario de registro sin números;
- en Founders Picks, referencias reales con su motivo.

## Herramienta

**Remotion.** Es la base de producto fijada el 14/10 en `MOTION-GRAPHICS-AE-REMOTION.md`, y además es la única de las dos que puede pintar el HTML real del dashboard.

El vídeo SaaS anterior, «El Sistema», se hizo en After Effects porque Ale lo pidió para esa pieza. Allí la interfaz era una recreación simplificada, no la real. Si Ale quiere AE también aquí, habría que recrear el dashboard a mano y se perdería la fidelidad que pide.

Para render, copiar el patrón de `ecommerce-andromeda-claude/c03/render.mjs`:
- obturador de `c03/src/lib/Shutter.tsx`;
- fuentes SF Pro de `c03/src/lib/Fonts.tsx`;
- iterar con `REMOTION_SAMPLES=1`.

## Reglas de Ale que aplican

Salen del feedback de «El Sistema» (V1 y V2 rechazadas, V3 sin veredicto), de `estilo-editor/FEEDBACK-ALE.md` y de la skill `motion-art-direction`.

**Ritmo**
- La queja número uno fue «lento».
- Ale autorizó recortar pausas de la voz.
- Cambios frecuentes, «dopamínico».
- Nada de objetos parados.

**Cámara**
- Un solo viaje continuo, con acercamientos y alejamientos fluidos.
- Motion blur de obturador, no gaussiano.
- Planos oblicuos de interfaz.
- El campo del agente que se acerca y da el relevo a la respuesta (fue una de sus referencias).

**Cursor**
- Entra desde fuera de cuadro.
- El clic deja un pulso y dispara el siguiente beat.
- El teclado suena sincronizado con lo que se escribe.

**Tipografía y texto**
- SF Pro Display.
- Nada de texto que duplique la voz ni de rótulos explicativos.
- Entradas por un solo eje.
- Anclas estables.
- No abusar de ningún recurso.

**Fondo**
- Con textura y producido, no plano.
- **Ojo:** para «El Sistema» Ale rechazó un styleframe blanco y azul («asqueroso»), y la interfaz de Studio es blanca y azul. Aquí la interfaz real es obligatoria, pero el marco no tiene por qué serlo. Hay que explorarlo en los styleframes, con el tema oscuro de Studio como alternativa.

**Proceso**
- Tres direcciones con fotogramas antes de animar; se elige una de forma autónoma.
- Previews breves mientras se trabaja.
- Aprobar un fragmento no aprueba el vídeo entero.

**Audio**
- Música con ducking bajo la voz.
- Efectos con causa: clic, teclado, whoosh.
- −15 LUFS y −1,5 dBTP.

**Entrega**
- Subtítulos en SRT aparte.
- `CURRENT-VERSION.json` y `Revisar-VN.html`.
- Comprobaciones: hoja de contactos, tiras de transiciones, detección de negros, sonoridad, fuentes y medios.
