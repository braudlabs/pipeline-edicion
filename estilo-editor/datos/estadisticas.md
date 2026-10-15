# Estadísticas automáticas y sus límites

Generado por `scripts/stats.py` a partir de `datos/<slug>/`. No editar a mano: volver a ejecutar el script.
`v6-ads90` se excluye para no ponderar dos veces el montaje compartido: 2424/2650 fotogramas decodificados coinciden por hash con rev; 226 difieren. V7 reutiliza visualmente gran parte de la cola con desplazamiento de 5f en anclas verificadas, sin identidad general por hash.

Estas cifras describen candidatos OCR/detector; no son reglas creativas ni verificación visual. La fracción localizada no permite distinguir omisión editorial, oclusión y fallo OCR. El resumen de desfase base condiciona a |lag| ≤0,25 s; ver todos los desfases y n excluidos en JSON. La cadencia es una estimación de cambios en la imagen final, no los fps originales del rodaje. Los énfasis se detectan por altura relativa y pueden mezclar textos de interfaz, grafismos y OCR parcial.

## Material

| vídeo | px | fps | s | metraje fps | LUFS | LRA | pico dBTP | palabras/s |
|---|---|---|---|---|---|---|---|---|
| landing | 1920×1080 | 60.0 | 94.667 | 26.07 | -11.0 | 9.8 | 1.2 | 2.891 |
| v1-pagado | 1080×1920 | 24.0 | 79.083 | 22.81 | -11.5 | 1.9 | 0.4 | 3.229 |
| v2-churros | 1080×1920 | 24.0 | 70.792 | 21.87 | -11.9 | 1.5 | 0.2 | 3.272 |
| v3-ia-cara | 1080×1920 | 24.0 | 64.25 | 22.02 | -12.0 | 2.2 | 0.9 | 3.287 |
| v5-maquina | 1080×1920 | 29.97 | 76.443 | 23.47 | -11.4 | 2.6 | 0.1 | 2.586 |
| v6-ads90-rev | 1080×1920 | 60.0 | 44.167 | 28.77 | -11.8 | 2.5 | 0.7 | 2.834 |
| v7-ads90-rev | 1080×1920 | 60.0 | 44.683 | 28.71 | -11.6 | 2.8 | 0.4 | 2.965 |
| lafabrica-v1 | 1080×1920 | 24.0 | 45.667 | 19.95 | -14.1 | 2.4 | 0.4 | 2.972 |
| lafabrica-v2p1 | 1080×1920 | 24.0 | 79.458 | 22.2 | -12.7 | 1.2 | 0.6 | 3.891 |

## Subtítulo base

| vídeo | localizadas % | desfase f (p10–p50–p90) | cuerpo px | % del ancho | en pantalla s (p10–p50–p90) | centro y % (p10–p50–p90) | respecto a la cara (p10–p50–p90) |
|---|---|---|---|---|---|---|---|
| landing | 89.2 | -4–0–6 | 62 | 3.24 | 0.117–0.283–0.62 | 50.1–50.8–77 | 0.038–0.36–1.33 |
| v1-pagado | 89.9 | -2–0–2 | 105 | 9.7 | 0.125–0.292–0.758 | 49.8–60–65.8 | 0.456–0.65–0.87 |
| v2-churros | 92.4 | -2–-1–1 | 124 | 11.47 | 0.083–0.333–0.55 | 33.58–49.4–55.58 | -2.904–1.25–2.084 |
| v3-ia-cara | 90.3 | -2–0–2 | 99 | 9.12 | 0.125–0.292–0.75 | 30.4–56.5–73 | -1.184–0.74–1.004 |
| v5-maquina | 79.8 | -2–0–3 | 106 | 9.84 | 0.133–0.334–0.667 | 24.6–50.2–50.8 | -1.763–1.03–2.588 |
| v6-ads90-rev | 83.8 | -4.2–0–8 | 96 | 8.86 | 0.117–0.358–0.708 | 41.2–50.3–54.55 | -0.015–1.1–1.874 |
| v7-ads90-rev | 85.8 | -5–0–6 | 98 | 9.03 | 0.117–0.383–0.742 | 47.85–50.4–51.35 | -0.006–1.11–1.978 |
| lafabrica-v1 | 89.3 | -3–0–3 | 179 | 16.58 | 0.125–0.312–0.792 | 23.05–29.65–51.55 | -1.796–-0.15–1.394 |
| lafabrica-v2p1 | 87.1 | -2–0–2 | 177 | 16.35 | 0.083–0.292–0.583 | 16.75–25.8–50.1 | -2.514–-1.4–0.848 |

«Cuerpo px» sale de la anchura medida dividida por la anchura de la palabra en SF Pro Display Bold a −60; el ajuste directo contra la tinta (`fontfit.py`) da en torno a un 7 % menos (98 px en v1).
«Respecto a la cara»: centro del subtítulo medido en alturas de cara desde el centro de la cara (+0,5 = barbilla; negativo = por encima).

## Palabras de énfasis

| vídeo | n | 1 cada s | gigantes | ancho % (p25–p50–p75) | en pantalla s (p10–p50–p90) | con línea pequeña | línea encima | salen a la vez | separación centros px | línea entra antes s |
|---|---|---|---|---|---|---|---|---|---|---|
| landing | 22 | 3.77 | 18 | 51.2–52.2–61.2 | 0.313–0.65–4.598 | 10 | 7 | 8 | 116.0 | 0.25 |
| v1-pagado | 15 | 5.12 | 8 | 70.5–73.3–74.9 | 0.542–0.75–1.508 | 12 | 10 | 10 | 155.5 | 0.25 |
| v2-churros | 11 | 6.25 | 1 | 71.925–73.8–78.4 | 0.5–0.708–1.25 | 2 | 0 | 2 | 157.5 | -0.125 |
| v3-ia-cara | 13 | 4.82 | 5 | 69.9–73.6–80.7 | 0.325–0.583–1 | 9 | 5 | 8 | 175.0 | 0.0 |
| v5-maquina | 21 | 3.55 | 3 | 69.2–70.5–73.1 | 0.1–0.4–1.802 | 0 | 0 | 0 | None | None |
| v6-ads90-rev | 20 | 2.06 | 10 | 66.9–71.1–74.9 | 0.08–0.533–0.95 | 3 | 3 | 2 | 149.0 | 0.433 |
| v7-ads90-rev | 33 | 1.3 | 10 | 53.725–65.55–72.6 | 0.103–0.333–0.903 | 3 | 2 | 1 | 148.0 | 0.417 |
| lafabrica-v1 | 10 | 4.41 | 0 | 68.725–74.3–76.225 | 0.079–0.333–0.629 | 1 | 0 | 1 | 630.0 | 0.25 |
| lafabrica-v2p1 | 5 | 15.58 | 1 | 62.85–63.7–72.95 | 0.142–0.417–0.925 | 3 | 3 | 3 | 178.0 | 0.333 |

## Cortes

| vídeo | fuente | n | plano medio s | plano s (p10–p50–p90–máx) | primer corte s | corte − inicio de palabra, f (p10–p50–p90) | tolerancia f | % dentro de tolerancia | % tras puntuación |
|---|---|---|---|---|---|---|---|---|---|
| landing | detector | 46 | 1.932 | 0.507–1.517–4.373–6.6 | 3.583 | -11.5–-2.5–13.5 | 2 | 19.6 | 43.5 |
| v1-pagado | detector | 25 | 2.992 | 0.938–2.396–5.938–11.583 | 6.292 | -5–0–4.6 | 1 | 40.0 | 64.0 |
| v2-churros | detector | 29 | 2.325 | 0.496–2.312–4.721–5.333 | 3.042 | -2.4–0–2.2 | 1 | 55.2 | 41.4 |
| v3-ia-cara | detector | 19 | 3.183 | 0.887–2.979–5.825–8.375 | 4.458 | -1.2–0–3 | 1 | 52.6 | 73.7 |
| v5-maquina | detector | 17 | 4.199 | 0.801–3.987–7.247–15.549 | 4.671 | -5.6–1–25.4 | 1 | 29.4 | 58.8 |
| v6-ads90-rev | detector | 31 | 1.372 | 0.29–1.008–2.947–4.167 | 1.067 | -10–-1–6 | 2 | 29.0 | 54.8 |
| v7-ads90-rev | detector | 30 | 1.414 | 0.283–0.917–2.95–6.233 | 6.233 | -10–-2–5.6 | 2 | 30.0 | 56.7 |
| lafabrica-v1 | detector | 19 | 2.252 | 0.696–1.979–4.188–5.708 | 5.708 | -2–0–6.2 | 1 | 57.9 | 68.4 |
| lafabrica-v2p1 | detector | 43 | 1.793 | 0.537–1.292–3.683–5.125 | 1.042 | -1–0–2.8 | 1 | 69.8 | 69.8 |

## Arranque y final

| vídeo | 1.ª palabra s | 1.er rótulo (f / s) | 1.er énfasis | última palabra s | cola tras la voz s | negro final (f / s) |
|---|---|---|---|---|---|---|
| landing | 6.8 | 0 / 0.0 | funcionan @ 15.16 | 89.82 | 4.847 | 85 / 1.417 |
| v1-pagado | 0.0 | 0 / 0.0 | pagado @ 5.16 | 76.8 | 2.283 | 38 / 1.583 |
| v2-churros | 0.0 | 0 / 0.0 | crear @ 0.66 | 68.76 | 2.032 | 43 / 1.792 |
| v3-ia-cara | 0.0 | 1 / 0.0417 | producir @ 1.52 | 62.68 | 1.57 | 29 / 1.208 |
| v5-maquina | 0.0 | 13 / 0.4338 | produce @ 37.76 | 74.64 | 1.803 | 29 / 0.968 |
| v6-ads90-rev | 1.64 | 117 / 1.95 | e @ 2.64 | 42.92 | 1.247 | 65 / 1.083 |
| v7-ads90-rev | 0.0 | 0 / 0.0 | creador @ 0.68 | 42.84 | 1.843 | 101 / 1.683 |
| lafabrica-v1 | 0.0 | 0 / 0.0 | exige @ 1.04 | 44.08 | 1.587 | 33 / 1.375 |
| lafabrica-v2p1 | 0.0 | 2 / 0.0833 | creativa @ 0.46 | 77.88 | 1.578 | 34 / 1.417 |

## Palabras de énfasis, una a una

### landing

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 15.16 | funcionan | 4.55 | 330 | 70.2 | 29.5 | 1.9 | «probablemente producir anundios que» encima, a 177 px, entra +1.333 s antes |
| 17.48 | negocio | 1.58 | 101 | 17.4 | 51.3 | 0.45 | — |
| 20.14 | inteligencia | 3.15 | 166 | 39.7 | 45.9 | 0.883 | «conlallegada de la» encima, a 119 px, entra +0.017 s antes |
| 20.5 | artificial | 2.65 | 174 | 28.5 | 59.8 | 0.617 | «conlallegada de la» encima, a 270 px, entra +0.283 s antes |
| 21.4 | media | 3.06 | — | 46.1 | 34.4 | 1.433 | — |
| 27.88 | costes | 3.15 | 260 | 37.2 | 52.9 | 0.683 | «reducir» encima, a 100 px, entra +0.25 s antes |
| 29.2 | volumen | 3.35 | 272 | 50.2 | 53.0 | 0.433 | «multiplicar el» encima, a 82 px, entra +0.467 s antes |
| 29.78 | velocidad | 2.95 | 217 | 44.5 | 49.5 | 1.3 | «de producción» debajo, a 120 px, entra -0.35 s antes |
| 32.72 | adaptarse | 2.85 | 174 | 37.5 | 44.6 | 2.983 | «alarespuesta del mercado» debajo, a 113 px, entra -0.8 s antes |
| 46.54 | creador | 2.4 | 186 | 30.7 | 45.2 | 0.95 | — |
| 46.82 | UGC | 2.5 | 165 | 17.4 | 57.8 | 0.55 | — |
| 47.66 | editor | 2.3 | 172 | 21.2 | 52.5 | 0.45 | «Al» encima, a 107 px, entra +0.25 s antes |
| 49.1 | rodaje | 2.85 | 187 | 24.9 | 52.5 | 0.583 | «al equipo de» encima, a 110 px, entra +0.433 s antes |
| 52.72 | produce | 4.05 | 222 | 39.7 | 54.4 | 0.55 | — |
| 53.5 | edita | 3.6 | 271 | 28.9 | 52.2 | 0.3 | — |
| 53.8 | el | 3.35 | — | 11.6 | 54.4 | 0.033 | — |
| 54.04 | anuncio | 3.1 | 243 | 41.4 | 55.4 | 0.283 | «5220005» debajo, a 121 px, entra +0.0 s antes |
| 54.32 | completo | 4.1 | 259 | 52.2 | 53.8 | 0.467 | — |
| 78.88 | planos | 2.8 | 169 | 24.1 | 31.8 | 5.65 | — |
| 79.44 | escenas | 1.9 | 170 | 30.5 | 44.3 | 5.25 | — |
| 80.0 | hooks | 2.45 | 171 | 22.5 | 57.8 | 4.65 | — |
| 80.48 | visuales | 2.35 | 174 | 29.9 | 70.4 | 4.133 | — |

### v1-pagado

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 5.16 | pagado | 3.35 | 264 | 77.0 | 68.9 | 0.542 | «nimehan» encima, a 171 px, entra +0.25 s antes |
| 6.08 | Porque | 1.97 | — | 68.1 | 34.4 | 0.833 | — |
| 7.92 | 300 | 2.87 | 432 | 72.4 | 50.1 | 1.625 | «no necesito» encima, a 161 px, entra +0.208 s antes |
| 11.68 | semanas | 3.97 | 215 | 74.9 | 67.1 | 0.542 | — |
| 13.9 | funcionan | 1.9 | 199 | 75.2 | 68.8 | 0.708 | «que luegoni» encima, a 160 px, entra +0.417 s antes |
| 17.5 | mínimo | 2.39 | 249 | 70.5 | 51.3 | 1.333 | «de producción» debajo, a 87 px, entra -0.417 s antes |
| 19.78 | mejor | 3.3 | 350 | 76.2 | 64.2 | 0.208 | «conelque» encima, a 191 px, entra +0.333 s antes |
| 24.4 | con | 2.54 | — | 64.1 | 67.4 | 0.542 | «hechos» encima, a 142 px, entra +0.208 s antes |
| 27.02 | cara | 3.0 | 405 | 68.0 | 69.6 | 0.75 | «porla» encima, a 176 px, entra +0.208 s antes |
| 28.02 | mensaje | 2.47 | 231 | 74.7 | 68.8 | 0.75 | «porel» encima, a 164 px, entra +0.25 s antes |
| 30.68 | conecta | 1.93 | 238 | 73.4 | 68.2 | 0.667 | «conelque» encima, a 151 px, entra +0.375 s antes |
| 52.98 | curso | 2.63 | 340 | 73.3 | 19.0 | 1.75 | — |
| 53.78 | aprendas | 2.17 | 203 | 72.4 | 70.9 | 1.0 | «a hacerlo» debajo, a 70 px, entra -0.5 s antes |
| 58.28 | consistente | 1.7 | 170 | 74.9 | 66.8 | 0.833 | «mantenerme» encima, a 127 px, entra +0.708 s antes |
| 70.24 | vendan | 2.2 | 249 | 70.5 | 61.2 | 0.75 | «deverdad» encima, a 149 px, entra +0.333 s antes |

### v2-churros

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 0.66 | crear | 2.19 | 405 | 79.3 | 50.9 | 1.042 | «contenido con IA» debajo, a 175 px, entra -0.167 s antes |
| 3.18 | alguno | 1.84 | 207 | 53.8 | 40.3 | 1.417 | — |
| 3.78 | problemas | 1.76 | 201 | 81.1 | 67.1 | 0.875 | — |
| 7.84 | la | 1.78 | — | 75.7 | 47.7 | 1.0 | «persona» debajo, a 140 px, entra -0.083 s antes |
| 20.84 | usable | 2.3 | 283 | 71.6 | 53.4 | 0.083 | — |
| 22.46 | absurda | 1.67 | 234 | 72.9 | 40.2 | 1.25 | — |
| 23.14 | de | 1.76 | — | 25.3 | 49.8 | 0.625 | — |
| 23.26 | créditos | 1.81 | 234 | 71.6 | 58.5 | 0.542 | — |
| 32.3 | dinero | 2.43 | — | 93.8 | 50.4 | 0.5 | — |
| 47.36 | profesional | 1.65 | 176 | 73.4 | 52.3 | 0.583 | — |
| 56.58 | realistas | 1.65 | 237 | 74.2 | 49.6 | 0.708 | — |

### v3-ia-cara

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 1.52 | producir | 3.39 | 263 | 83.0 | 31.7 | 1.0 | «más» debajo, a 171 px, entra -0.333 s antes |
| 8.8 | Abres | 2.81 | 306 | 69.8 | 22.7 | 0.708 | «una app» debajo, a 186 px, entra -0.25 s antes |
| 9.8 | generas | 2.21 | 232 | 71.6 | 27.3 | 0.583 | — |
| 10.4 | no | 2.75 | — | 80.0 | 24.0 | 0.917 | «bien» debajo, a 175 px, entra -0.333 s antes |
| 10.72 | bien | 1.63 | 181 | 30.0 | 33.1 | 0.583 | — |
| 11.68 | generar | 2.27 | 113 | 33.3 | 27.7 | 0.458 | «vuelves a» encima, a 160 px, entra +0.333 s antes |
| 12.76 | prompt | 2.49 | 263 | 73.6 | 26.8 | 0.167 | «cambias el» encima, a 179 px, entra +0.0 s antes |
| 13.6 | otra | 3.68 | 459 | 70.0 | 29.7 | 0.5 | «pruebas» encima, a 180 px, entra +0.25 s antes |
| 16.76 | horas | 2.27 | 377 | 81.4 | 23.5 | 0.583 | «hasgastado» encima, a 212 px, entra +0.625 s antes |
| 17.9 | créditos | 2.01 | 266 | 81.1 | 21.5 | 1.083 | — |
| 32.06 | proceso | 2.4 | 210 | 65.1 | 56.7 | 1.0 | «soguir» debajo, a 156 px, entra -0.083 s antes |
| 49.72 | generaciones | 1.76 | 157 | 80.3 | 68.6 | 0.708 | — |
| 59.04 | clientes | 1.82 | 215 | 62.8 | 36.0 | 0.292 | «ocon» encima, a 119 px, entra +0.292 s antes |

### v5-maquina

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 37.76 | produce | 2.27 | 222 | 70.5 | 30.5 | 2.135 | — |
| 38.12 | creativos | 1.79 | 217 | 74.4 | 66.3 | 1.802 | — |
| 38.7 | a | 2.27 | — | 69.5 | 30.6 | 0.1 | — |
| 40.92 | ya | 2.35 | — | 26.9 | 52.7 | 0.267 | — |
| 41.38 | estás | 2.33 | 269 | 55.8 | 50.4 | 0.234 | — |
| 41.56 | viendo | 2.21 | 273 | 69.9 | 50.3 | 0.567 | — |
| 49.56 | visual | 3.04 | 341 | 74.1 | 50.2 | 0.601 | — |
| 51.2 | cuesta | 1.97 | 262 | 67.7 | 36.3 | 0.1 | — |
| 51.68 | mucho | 2.15 | 259 | 69.5 | 36.0 | 0.267 | — |
| 51.98 | dinero | 2.12 | 270 | 64.6 | 35.9 | 0.367 | — |
| 52.54 | tiempo | 2.58 | 267 | 71.3 | 37.0 | 0.067 | — |
| 52.82 | y | 2.61 | — | 71.4 | 37.1 | 0.3 | — |
| 52.98 | dolores | 2.06 | 260 | 73.1 | 36.2 | 0.4 | — |
| 53.48 | cabeza | 2.0 | 250 | 69.2 | 36.4 | 0.534 | — |
| 53.8 | Cuando | 1.91 | 232 | 70.5 | 36.1 | 0.334 | — |
| 54.4 | intentas | 1.94 | 243 | 73.9 | 36.1 | 0.501 | — |
| 54.96 | escalar | 1.91 | 245 | 67.2 | 36.0 | 0.734 | — |
| 55.76 | apagar | 1.94 | — | 81.9 | 20.4 | 6.84 | — |
| 68.92 | pincha | 1.56 | 161 | 41.5 | 51.2 | 0.4 | — |
| 72.42 | máquina | 1.73 | 130 | 43.1 | 49.6 | 0.367 | — |
| 73.6 | dentro | 1.56 | 136 | 34.1 | 51.2 | 0.467 | — |

### v6-ads90-rev

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 2.64 | e | 1.68 | — | 75.6 | 50.6 | 0.567 | — |
| 4.5 | Black | 2.35 | 318 | 66.9 | 36.4 | 0.75 | — |
| 4.66 | Friday | 2.39 | 310 | 72.9 | 47.1 | 0.5 | — |
| 11.28 | Así | 3.43 | 431 | 52.7 | 35.0 | 1.167 | — |
| 11.66 | de | 2.76 | — | 35.0 | 50.7 | 0.767 | — |
| 11.8 | fácil | 3.62 | 423 | 65.2 | 66.9 | 0.683 | — |
| 18.78 | generar | 2.42 | 252 | 74.2 | 52.6 | 0.35 | «Ledasa» encima, a 140 px, entra +0.433 s antes |
| 19.72 | voilá | 3.19 | 313 | 54.3 | 50.2 | 1.1 | — |
| 21.92 | atención | 1.9 | — | 74.9 | 68.8 | 0.767 | — |
| 23.36 | servicio | 2.65 | 240 | 69.8 | 49.6 | 0.783 | — |
| 24.42 | tuyo | 4.25 | 393 | 67.4 | 53.3 | 0.35 | «Es» encima, a 187 px, entra +0.45 s antes |
| 25.14 | Lo | 2.03 | — | 25.1 | 29.9 | 0.05 | — |
| 25.32 | instalamos | 2.26 | 184 | 75.5 | 30.2 | 0.483 | — |
| 25.76 | en | 1.68 | — | 20.4 | 30.5 | 0.033 | — |
| 25.9 | tu | 1.84 | — | 24.0 | 30.2 | 0.117 | — |
| 26.58 | usas | 1.74 | 168 | 30.8 | 29.9 | 0.317 | — |
| 26.9 | cuando | 2.45 | 164 | 47.3 | 30.3 | 0.333 | — |
| 27.16 | quieras | 2.35 | 164 | 45.7 | 30.7 | 0.933 | — |
| 28.08 | veces | 2.5 | 314 | 71.1 | 52.5 | 0.933 | «las» encima, a 149 px, entra +0.067 s antes |
| 30.9 | 10 | 7.0 | — | 75.2 | 50.0 | 0.083 | — |

### v7-ads90-rev

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 0.68 | creador | 2.09 | 225 | 65.9 | 50.2 | 0.383 | — |
| 1.0 | UGC | 2.19 | 233 | 43.7 | 50.1 | 0.217 | — |
| 1.58 | te | 1.82 | — | 21.2 | 50.6 | 0.1 | — |
| 1.76 | deja | 2.79 | 225 | 36.7 | 50.7 | 0.283 | — |
| 2.0 | tirado | 2.0 | 233 | 50.9 | 50.7 | 0.35 | — |
| 2.36 | a | 2.0 | — | 53.5 | 50.4 | 0.367 | — |
| 2.72 | hora | 2.15 | 289 | 50.1 | 50.7 | 0.5 | — |
| 3.46 | te | 1.97 | — | 32.8 | 50.8 | 0.117 | — |
| 3.68 | entrega | 2.32 | 235 | 69.0 | 52.1 | 0.317 | — |
| 4.0 | algo | 2.57 | 225 | 37.1 | 51.7 | 0.2 | — |
| 4.34 | no | 1.82 | — | 24.8 | 51.5 | 0.167 | — |
| 4.54 | se | 1.7 | — | 20.9 | 51.5 | 0.15 | — |
| 4.72 | parece | 2.03 | 225 | 59.2 | 52.4 | 0.4 | — |
| 5.06 | en | 1.62 | — | 22.5 | 51.5 | 0.083 | — |
| 5.3 | nada | 2.11 | 272 | 52.6 | 50.8 | 0.283 | — |
| 5.64 | que | 2.28 | 269 | 40.0 | 52.7 | 0.1 | — |
| 5.74 | pediste | 2.44 | 263 | 74.2 | 51.5 | 0.483 | — |
| 11.18 | Así | 3.16 | 433 | 53.0 | 34.9 | 1.167 | — |
| 11.58 | de | 2.51 | — | 35.2 | 50.7 | 0.767 | — |
| 11.72 | fácil | 3.23 | 423 | 65.2 | 67.1 | 0.683 | — |
| 18.7 | generar | 2.21 | 248 | 73.1 | 52.6 | 0.35 | «Ledasa» encima, a 140 px, entra +0.417 s antes |
| 19.64 | voilá | 2.92 | — | 54.4 | 50.2 | 1.1 | — |
| 21.84 | atención | 1.73 | — | 74.9 | 68.8 | 0.767 | — |
| 23.28 | servicio | 2.41 | 240 | 69.8 | 49.6 | 0.783 | — |
| 24.34 | tuyo | 3.56 | 369 | 63.3 | 53.2 | 0.25 | «Es» encima, a 185 px, entra +0.45 s antes |
| 25.06 | Lo | 1.85 | — | 25.1 | 29.9 | 0.05 | — |
| 25.24 | instalamos | 2.06 | 185 | 75.9 | 30.4 | 0.483 | — |
| 25.82 | tu | 1.68 | — | 24.0 | 30.2 | 0.233 | — |
| 26.5 | usas | 1.59 | 170 | 31.0 | 30.1 | 0.15 | — |
| 26.82 | cuando | 2.25 | 164 | 47.3 | 30.3 | 0.333 | — |
| 27.08 | quieras | 2.12 | 164 | 45.8 | 30.7 | 0.933 | — |
| 28.0 | veces | 2.28 | 314 | 71.1 | 52.7 | 0.933 | «quequieras» debajo, a 148 px, entra -0.2 s antes |
| 30.82 | 10 | 6.38 | — | 74.9 | 49.9 | 0.133 | — |

### lafabrica-v1

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 1.04 | exige | 1.81 | 259 | 53.3 | 21.0 | 0.333 | — |
| 2.82 | UGC | 2.07 | 407 | 76.3 | 19.6 | 0.5 | — |
| 15.74 | plazos | 1.75 | 305 | 75.2 | 26.7 | 0.458 | — |
| 16.28 | costes | 1.66 | 288 | 73.4 | 27.1 | 0.667 | — |
| 23.12 | IA | 2.07 | — | 48.1 | 25.4 | 0.125 | — |
| 25.56 | Tú | 1.64 | — | 29.2 | 60.7 | 0.083 | — |
| 25.76 | o | 2.34 | — | 71.3 | 35.3 | 0.625 | «a tu producto y turmarca» debajo, a 630 px, entra +0.25 s antes |
| 26.06 | alguien | 1.68 | 285 | 78.3 | 62.0 | 0.292 | — |
| 26.56 | equipo | 1.68 | 291 | 76.2 | 61.8 | 0.042 | — |
| 26.86 | dirige | 1.69 | 288 | 61.0 | 60.8 | 0.333 | — |

### lafabrica-v2p1

| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |
|---|---|---|---|---|---|---|---|
| 0.46 | creativa | 1.6 | 275 | 82.2 | 28.5 | 0.5 | «LaIA» encima, a 178 px, entra +0.458 s antes |
| 4.14 | Abres | 1.56 | 272 | 62.0 | 12.1 | 0.292 | — |
| 27.74 | cámara | 1.6 | 222 | 63.7 | 34.4 | 1.208 | «sin» encima, a 123 px, entra -0.167 s antes |
| 67.64 | 4 | 2.48 | — | 25.9 | 24.0 | 0.042 | — |
| 73.2 | botella | 1.58 | 173 | 43.9 | 28.6 | 0.417 | «cuello» encima, a 186 px, entra +0.333 s antes |
