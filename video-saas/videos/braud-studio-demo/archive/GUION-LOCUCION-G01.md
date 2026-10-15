# Guion de locución · G01 (sustituido por G02 el 15/10/2026, no aprobado)

Vídeo de demo estilo SaaS para enseñar en llamadas de venta. Responde a la objeción «¿Sabré manejarlo?»: la Biblia de closers lo da como pendiente («vídeo de cómo funciona el producto, corto y al estilo de una demo de software»).

- **Idea central:** tú das la dirección y apruebas; el sistema produce.
- **Extensión:** 377 palabras, unos 2:20 de voz. Con el aire entre bloques, el vídeo queda en unos **2:30**, en 16:9.
- **Narrador:** BRAUD le habla al cliente de tú.
- **Lo que no se promete:** solo se dice lo que el dashboard hace hoy. Meta Ads, la voz con ElevenLabs y el render final siguen pendientes; ver `FUNCIONALIDADES.md`.

## Texto para pegar en ElevenLabs

```
Desde Andrómeda, Meta pide creatividad nueva cada semana. Y tu producción sigue yendo a ritmo de mes.

Esto es BRAUD Studio. Tu sistema de producción creativa, instalado en tu tienda.

Y se maneja como le hablas a ChatGPT. Le escribes, o se lo dices, con tus palabras.

Antes de producir, conoce tu marca. Tu web, tus productos, tu oferta y a quién le vendes. Todo queda en Mi marca, y cada anuncio parte de ahí.

Cada pieza empieza con una conversación. Le cuentas la idea, y el agente la aterriza contigo: el objetivo, el público, qué le frena y qué lo demuestra. Te propone varios ángulos, y tú eliges desde dónde contarla.

Después escribe el guion, frase a frase, con lo que se verá en cada una. Y como el hook lo decide casi todo, te prepara tres maneras de empezar. Aplicas una, y el resto se queda igual.

Luego, el reparto. Primero el papel, después el personaje. Eliges entre candidatos, y su identidad se mantiene en todas las escenas. Tu producto, igual: parte de tus fotos reales.

Decides quién dice cada frase, importas la locución, y la escuchas aquí mismo.

Y llegamos a las escenas. Una frase, una escena. El agente escribe el prompt con tu dirección y tus referencias, y antes de generar, ves lo que cuesta. Sin tu visto bueno, no se genera nada. Cada escena guarda sus versiones: comentas, apruebas, y te quedas con la buena.

En Montaje ves el ritmo del conjunto y lo que falta. Cuando está todo, preparas la entrega con lo aprobado, lista para edición.

¿Otro hook? ¿Otro personaje? Guardas la versión, y sacas la siguiente sin empezar de cero.

Y en el Taller decides qué probar después. Comparas anuncios con una variable y una hipótesis, registras los resultados, y el agente te propone la lectura y el siguiente test. Datos. Hipótesis. Siguiente versión.

En la Biblioteca conservas personajes, materiales y clips aprobados. En Founders Picks, las referencias que seleccionamos en BRAUD, cada una con su porqué. Y en Actividad, todo lo que espera tu criterio.

Tú das la dirección y apruebas. El sistema produce.

No es una agencia. Lo instalamos con tu marca, formamos a quien lo va a pilotar, y se queda en tu tienda.

BRAUD Studio.
```

## Qué se ve con cada bloque

| # | Voz (inicio) | Pantalla | ≈ seg. |
| --- | --- | --- | --- |
| 1 | «Desde Andrómeda…» | Tipografía sobre fondo de la marca, sin interfaz. Calendario de Meta frente a ritmo de producción. | 0–7 |
| 2 | «Esto es BRAUD Studio…» | Entra el inicio: «Una idea. Todo lo que puede ser.» | 7–13 |
| 3 | «Y se maneja como…» | Cursor en la caja del agente; se escribe una idea; botón Dictar. | 13–20 |
| 4 | «Antes de producir…» | Mi marca: tarjetas de negocio, productos y oferta, públicos, identidad. | 20–32 |
| 5 | «Cada pieza empieza…» | Chat del agente → paso 01 Idea: intención y ángulos. | 32–47 |
| 6 | «Después escribe el guion…» | Paso 02 Guion: las tres aperturas; clic en «Usar apertura». | 47–62 |
| 7 | «Luego, el reparto…» | Paso 03 Casting: papel, candidatos, identidad incorporada; referencia de producto. | 62–74 |
| 8 | «Decides quién dice…» | Paso 04 Voces: frase a frase, importar locución, forma de onda. | 74–80 |
| 9 | «Y llegamos a las escenas…» | Paso 05 Escenas: dirección, «Preparar una generación» (Seedance 2.5 · 1080p), «Consultar coste», versiones, Aprobado. | 80–100 |
| 10 | «En Montaje…» | Paso 06 Montaje: pista de voz y visuales, lista de pendientes, «Preparar entrega». | 100–109 |
| 11 | «¿Otro hook?…» | Versiones de la pieza. | 109–116 |
| 12 | «Y en el Taller…» | Taller: proyecto, comparación, tabla de resultados con CTR y CPA, lectura del agente. | 116–130 |
| 13 | «En la Biblioteca…» | Biblioteca → Founders Picks → Actividad («Necesita tu criterio»). | 130–143 |
| 14 | «Tú das la dirección…» | Vuelta al inicio con zoom de salida: todas las vistas a la vez. | 143–147 |
| 15 | «No es una agencia…» | Cierre tipográfico y logo. | 147–157 |

## Si la quieres más corta (≈ 2:00)

Quita el bloque 1 (si el closer ya ha hablado del dolor), el 11 (Versiones) y el 13 (Biblioteca, Founders Picks, Actividad). El resto se sostiene sin ellos.

## Al generarla

- **Una sola generación** con el texto entero, para que el tono sea continuo. Las líneas en blanco son las pausas. El vídeo se sincroniza con la grabación, así que no hace falta cuadrar tiempos.
- **Voz:** castellano de España, cercana y segura, un punto más rápida que una conversación. Ni locutor de anuncio ni voz fría de tutorial.
- **Pronunciación, por si falla:**
  - «BRAUD»: si no la dice como queréis, escríbela tal como suena (por ejemplo «Brod»).
  - «hook»: si suena raro, cámbialo por «gancho» en los dos sitios.
  - «Founders Picks»: igual, escríbelo como suena.
  - «ChatGPT»: déjalo; si falla, pon «chat ge pe te».
- **Guárdala como** `video-saas/videos/braud-studio-demo/assets/locucion.wav` (o `.mp3`).
- **Si cambias una frase, no pasa nada:** el montaje sigue a la grabación. Si quitas un bloque entero, se cae su escena.
