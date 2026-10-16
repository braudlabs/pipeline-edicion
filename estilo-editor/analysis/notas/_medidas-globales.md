# Medidas globales (cuaderno de trabajo; se vuelca en ALGORITMO.md)

Todo lo de aquí sale de código que recorre los 24.094 fotogramas, no de muestreo. Scripts en `scripts/`.

## Material

| slug | original | px | fps | f | s | LUFS | pico dBTP | cola negra |
|---|---|---|---|---|---|---|---|---|
| landing | BRAUDLABS - LANDING | 1920×1080 | 60 | 5680 | 94,67 | −11,0 (LRA 9,8) | +1,2 | 85 f |
| v1-pagado | V1 - NI ME HAN PAGADO | 1080×1920 | 24 | 1898 | 79,08 | −11,5 (1,9) | +0,4 | 38 f |
| v2-churros | V2 - CHURROS COCINA | 1080×1920 | 24 | 1699 | 70,79 | −11,9 (1,5) | +0,2 | 43 f |
| v3-ia-cara | V3 - LA IA TE SALE CARA | 1080×1920 | 24 | 1542 | 64,25 | −12,0 (2,2) | +0,9 | 29 f |
| v5-maquina | V5 - LA MAQUINA - REV | 1080×1920 | 29,97 | 2291 | 76,44 | −11,4 (2,6) | +0,1 | 29 f |
| v6-ads90 | V6 - ADS 90S | 1080×1920 | 60 | 2650 | 44,17 | −11,8 (2,5) | +0,7 | 65 f |
| v6-ads90-rev | V6 - ADS 90s - REV | 1080×1920 | 60 | 2650 | 44,17 | −11,8 (2,5) | +0,7 | 65 f |
| v7-ads90-rev | V7 - ADS 90s - REV | 1080×1920 | 60 | 2681 | 44,68 | −11,6 (2,8) | +0,4 | 101 f |
| lafabrica-v1 | LaFabrica-V1 | 1080×1920 | 24 | 1096 | 45,67 | −14,1 (2,4) | +0,4 | 33 f |
| lafabrica-v2p1 | LaFabrica_V2_P1 | 1080×1920 | 24 | 1907 | 79,46 | −12,7 (1,2) | +0,6 | 34 f |

H.264 Main, 9–10 Mb/s a 24 fps, ~20 Mb/s a 60 fps; AAC 125–190 kb/s.

- Cadencia: líneas de tiempo a 24 / 29,97 / 60 fps con metraje a ~24–25 fps repetido (2-3-2-3 en 60; 1 de cada 5 en 29,97).
  Los rótulos se animan a la cadencia completa de la línea. En 60 fps solo un tercio de los fotogramas es repetición exacta.
- v6-ads90 y v6-ads90-rev: audio idéntico bit a bit; imagen idéntica salvo f960–f1082 (16,0–18,0 s), donde la revisión
  añade subtítulos a una frase que no los tenía.
- v7 = v6 con otro gancho: desde ≈f420 es el mismo montaje desplazado 5 fotogramas (v7[i] ≈ v6[i+5]); cambian f0–f520.

## Tipografía (ajuste contra la tinta real, `fontfit.py`)

- **SF Pro Display Bold, interletrado ≈ −60 milésimas.** Solape 0,958 («hooks», landing f4990, cuerpo 166 px);
  0,933 («también», v1 f1255, 99 px); 0,920 («generando», v1 f1790, 98 px). Helvetica Neue Bold queda en 0,81–0,89.
  Rasgos que lo confirman a ojo: «a» sin rabo, «t» de corte recto, punto de la «i» redondo.
- Línea secundaria de la landing («a la respuesta del mercado»): **SF Pro Thin**, cuerpo ≈ 93 px, interletrado ≈ −110,
  asta de 4 px (Ultralight daría 2, Light 6).
- Interlineado de los bloques de palabras grandes: muy cerrado (≈ 0,85 del cuerpo en «planos / escenas / hooks / visuales»).
- **Licencia**: SF Pro solo está licenciada para maquetas de interfaces de plataformas Apple; no para anuncios. Para vender:
  Inter (OFL) u otra grotesca con licencia. Fuente: developer.apple.com/fonts y foros de Apple.
- En los gráficos a pantalla completa de V1 el texto va en un plano con perspectiva: los glifos crecen hacia la derecha
  (anchura candidata/real 1,01 → 0,84 a lo largo de «300€»), y deriva lentamente de escala (ancho 849 → 790 px en 13 f).

## Subtítulo base

- Una palabra por unidad; aparece en el fotograma en que empieza a sonar: desfase mediano 0 f en los 9 vídeos
  (p10 −2, p90 +2 a 24 fps; el margen es el de la transcripción). 84–92 % de las palabras dichas localizadas en pantalla;
  lo no localizado es sobre todo «y», artículos y cifras tapadas por el sujeto.
- Sin animación de entrada en geometría: tamaño y posición finales desde el primer fotograma legible, sin deriva.
- Dura hasta que entra la siguiente: en pantalla p50 0,29–0,36 s (palabra dicha p50 0,24–0,26 s).
- Cuerpo estimado (anchura medida / anchura unitaria en SF Pro Display Bold −60; el ajuste directo da ~7 % menos):

| vídeo | cuerpo base | % ancho | centro y (p10–p50–p90) | respecto a la cara (alturas de cara desde su centro) |
|---|---|---|---|---|
| v1-pagado | 106 (98 ajustado) | 9,8 | 50–60–66 % | +0,65 (bajo la barbilla) |
| v2-churros | 125 | 11,6 | 34–49–56 % | +1,25 |
| v3-ia-cara | 101 | 9,3 | 30–56–73 % | +0,74 |
| v5-maquina | 111 | 10,3 | 25–50–51 % | +1,03 |
| v6-ads90-rev | 101 | 9,3 | 41–50–55 % | +1,10 |
| lafabrica-v1 | 182 | 16,8 | 23–30–52 % | (pocas caras) |
| lafabrica-v2p1 | 177 | 16,4 | 17–26–50 % | −1,40 (por encima de la cabeza) |
| landing | 64 | 3,3 | 50–51–77 % | +0,36; x entre 22 % y 61 % (a un lado) |

## Palabras de énfasis

- Anchura de la palabra gigante en los verticales: p25–p50–p75 = 70–73–75 % del ancho, sea cual sea su longitud
  («300» 432 px de cuerpo, «cara» 405, «mejor» 350, «pagado» 264, «mínimo» 249, «funcionan» 199, «consistente» 170: todas ≈ 72–77 %).
  Es un ajuste a anchura, no un cuerpo fijo.
- Frecuencia (≥ 1,55× el base): v1 1 cada 3,8 s · v2 5,7 · v3 4,5 · v5 3,4 · v6 2,0 · lafabrica-v1 4,4 · lafabrica-v2p1 15,6 · landing 3,8.
- Qué palabras: el foco de la frase —cifra, verbo de acción, beneficio o dolor, negación—, casi siempre la última de la cláusula.
  Listas por vídeo en `datos/<slug>/guion-anotado.md`.
- Landing: las grandes son de cuerpo fijo ≈ 165–175 px (15–16 % de la altura), con algunas a 220–330.
- Entrada (v6, 60 fps, geometría OCR): tamaño estable desde que es legible; deslizamiento lateral que frena durante
  ≈ 20–25 f (−33 → 0 px) en «voilà», «servicio», «veces»; «Braud» deriva en vertical de forma continua.

## Cortes (detector, pendiente de la verificación visual)

| vídeo | cortes | plano medio | p10 | p50 | p90 | % a ≤1 f de un inicio de palabra | % tras puntuación |
|---|---|---|---|---|---|---|---|
| v1-pagado | 25 | 2,99 s | 0,94 | 2,40 | 5,94 | 40 | 64 |
| v2-churros | 29 | 2,33 | 0,50 | 2,31 | 4,72 | 55 | 41 |
| v3-ia-cara | 19 | 3,18 | 0,89 | 2,98 | 5,83 | 53 | 74 |
| v5-maquina | 17 | 4,20 | 0,80 | 3,99 | 7,25 | 29 | 59 |
| v6-ads90-rev | 31 | 1,37 | 0,29 | 1,01 | 2,95 | 29 | 55 |
| v7-ads90-rev | 30 | 1,41 | 0,28 | 0,92 | 2,95 | 30 | 57 |
| lafabrica-v1 | 19 | 2,25 | 0,70 | 1,98 | 4,19 | 58 | 68 |
| lafabrica-v2p1 | 43 | 1,79 | 0,54 | 1,29 | 3,68 | 70 | 70 |
| landing | 46 | 1,93 | 0,51 | 1,52 | 4,37 | 20 | 43 |

Separación corte–inicio de palabra más cercano: mediana 0 f en los verticales a 24 fps.

## Arranques y finales

- Voz y primer subtítulo en el fotograma 0 en v1, v2, v3, v7, lafabrica-v1, lafabrica-v2p1. Excepciones: v6 (1,6 s de
  gag visual antes de la primera palabra), v5 (primer rótulo a 0,43 s), landing (6,8 s sin voz).
- Primer énfasis: 0,46–1,5 s en v2, v3, v7, lafabrica; 5,2 s en v1; 2,6 s en v6.
- Cola tras la última palabra: 1,25–2,3 s (landing 4,85 s); los últimos 29–101 fotogramas son negro fijo.
- Ritmo de voz: 2,6–3,3 palabras/s (lafabrica-v2p1 3,9). Pausas ≥ 0,3 s: muy pocas, y casi siempre antes de un remate.
