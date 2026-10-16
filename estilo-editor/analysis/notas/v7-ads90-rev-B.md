# v7-ads90-rev-B

Revisión de Codex, 10/10/2026. Índices desde 0, extremos incluidos, 60 fps. Todas las hojas densas abiertas; cobertura nativa parcial, límites explícitos. Audio: espectrogramas del mix, sin identificación auditiva de SFX.

## 1. Planos

f598–637 máquina marca (continuación hook revisadoA);638 mano/perfume;813 encuadre cerrado;830 selector;943 inserto frontal borroso1f;944 joven oblicuo;1069 teclado;1098 interior;1146 pantalla;1192 selfie;1302 presentador;1402 dos hombres;1506 oficina;1683 tecla;1744 reacción;1794 hombre máquina;1862 hombre selfie;1905 mujer;1955 coche;2015 mujer;2070 oficina;2216 CTA;2580–2680 negro. La cola reutiliza material de V6, pero no asumir igualdad de todos los fotogramas ni de overlays.

## 2. Cortes y transiciones

Nativa940–946 verifica943 frontal entre942pantalla/944oblicuo. Produce blanco atraviesa. Destellos interior1111/1138 no cortan. Reencuadre1335+ acompaña ¡Y atención!, con blur hasta≈1343.1462 oscurece dos hombres sin congelación. Frasco se acerca a lente desde2040, se desenfoca; no necesariamente filtro. Negro termina101f,100 idénticos consecutivos según hash.

## 3. Subtítulos base

Pones743/tu754/producto764, luego elige813 y estilo842; selector hasta942. Produce924,y952,edita960,el978,anuncio984,completo1004. Segunda pista amarilla inferior: quiero949/un967/UGC978/de1029/este≈1046/avatar≈1051; de1029 confirmado por nativa1026–1033, UGC sigue hasta1028. La versiónV6rev no pasa a de hasta1040: no trasladar toda cola por−5. Completo blanco sigue1083 con amarillo ya ausente. Le1086 cruza interior1098; das se suma. Oficina1506 coloca rail alto: Lo,instalamos,el,tu,negocio,y,lo,usas,cuando,quieras. CTA2216+ rail pecho: Pincha/abajo/y/agenda/una/llamada/Analizaremos/tu/caso/y/veremos/si/el/sistema/sirve/para/tu/ecommerce/Nos/vemos/dentro. No todos inicios tienen primer pixel nativo.

## 4. Énfasis

Así672,de695,fácil701. Generar1122 bajo Le das, cruza pantalla1146 hasta≈1159. Voilà1187 antes del corte selfie1192, permanece hasta1258. ¡Y atención!1305+; no1367/no es1380/no es un1387/servicio1393 (atraviesa1402hasta1441),Es1442/tuyo1468 sobre dim. Las y veces1689,que1699,quieras1709; acumulación hasta1743. ¿1 ya tenue1744,anuncio1754, cruza1794 y termina1800;No1801.10 empieza1859 antes del selfie1862,versiones1870;para1899 y regreso al rail. Tu2111,Q4 empieza2121, luegoen2167/tus2181/manos2193; Q4hasta2215. Tiempos visuales de hoja salvo donde figura nativa.

## 5. Escenas gráficas

Marca en pantalla sigue perspectiva. Selector gira/desplaza tarjetas y expande retrato central. Loading y resultado tienen preparación compartida. Expresión selfie1259–1301 continúa sin rail; respetar gesto/reacción. Material generado o recreado no revela por sí mismo herramienta original.

## 6. Superposiciones

Blanco y amarillo pertenecen a funciones simultáneas diferentes; conservar speakerId/railId y rangos independientes. Amarillo vive alrededor70% mientras blanco≈50%. Héroe Q4 alto convive con rail subordinado. Oclusión exacta de Q4 pendiente nativa, no copiar máscara del héroe de otro vídeo.

## 7. Sonido

Seis espectrogramas vistos por revisorB y lista transferida con procedencia. Mantiene fondo grave/tonal en pausas≈10–11.2 y20.2–21.3. Negro43s aún tiene cola hasta≈44s, no silencio instantáneo. No se identificaron SFX por escucha.

## 8. Ritmo

HookA distinto; esta cola conserva cadencia semántica de demo/resultado/propiedad/cantidad/CTA. Reacción tiene pausa sin rail; muestras rápidas encadenan texto; cierre directo estabiliza. Negro final más largo queV6 no cambia duración deargumento previo.

## 9. Reglas respaldadas

Comparar variantes por anclas y luego por eventos individuales. Retiming local del diálogo rompe la equivalencia−5f aun cuando cortes y blanco comparten ese desplazamiento. Rótulos atraviesan planos y no necesitan reinicio al corte. Distinguir negro editorial de fin de audio.

## 10. Dudas y alcance

35/35densas y17/17suplementarias abiertas paraB. Suplementaria s006 compartida cruzaA/B, leída por root;16 restantes por revisorB. Dos rangos nativos abiertos. Detalles nativos de curvas/asentamiento de cada palabra aún pendientes; no certificar exhaustividad por hojas completas.

## 11. Láminas

laminas/v7-ads90-rev/inserto-f940-946.jpg y dialogo-f1026-1033.jpg (crop y.65–.77). Cobertura adicional y sus hallazgos en notas/v7-tail-extra.coverage.json, consolidada en coberturaB.

## Sucesos estructurados

```json
[
  {
    "f0": 638,
    "f1": 812,
    "tipo": "demostración",
    "nombre": "caída_producto",
    "nota": "Material compartido, no hash identidad total",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 830,
    "f1": 942,
    "tipo": "escena",
    "nombre": "selector",
    "nota": "Carrusel/retrato",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 943,
    "f1": 943,
    "tipo": "inserto",
    "nombre": "frontal_borroso",
    "nota": "Un frame confirmado",
    "evidence_level": "native_verified"
  },
  {
    "f0": 949,
    "f1": 1083,
    "tipo": "texto",
    "nombre": "dos_rails",
    "nota": "Narración blanca/diálogo amarillo extremos independientes",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1029,
    "f1": 1033,
    "tipo": "diálogo",
    "nombre": "de_amarillo",
    "nota": "UGC1028→de1029, retiming local frente rev1040",
    "evidence_level": "native_verified"
  },
  {
    "f0": 1122,
    "f1": 1159,
    "tipo": "énfasis",
    "nombre": "generar",
    "nota": "Cruza pantalla1146",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1187,
    "f1": 1258,
    "tipo": "énfasis",
    "nombre": "voilà",
    "nota": "Anticipa resultado1192",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1259,
    "f1": 1301,
    "tipo": "reacción",
    "nombre": "selfie_sin_rail",
    "nota": "Expresión con movimiento",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1367,
    "f1": 1441,
    "tipo": "énfasis",
    "nombre": "no_es_un_servicio",
    "nota": "Acumulación cruza1402",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1462,
    "f1": 1505,
    "tipo": "color",
    "nombre": "dim_tuyo",
    "nota": "Metraje sigue vivo",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1506,
    "f1": 1682,
    "tipo": "layout",
    "nombre": "rail_alto",
    "nota": "Oficina",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1689,
    "f1": 1743,
    "tipo": "énfasis",
    "nombre": "veces_que_quieras",
    "nota": "Jerarquía acumulativa",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1744,
    "f1": 1800,
    "tipo": "énfasis",
    "nombre": "pregunta_1",
    "nota": "Cruza1794",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1859,
    "f1": 1898,
    "tipo": "énfasis",
    "nombre": "10_versiones",
    "nota": "Cantidad antes de ejemplo",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 1905,
    "f1": 2069,
    "tipo": "montaje",
    "nombre": "muestras",
    "nota": "Rail cruza productos",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 2111,
    "f1": 2215,
    "tipo": "énfasis",
    "nombre": "Tu_Q4",
    "nota": "Héroe y frase subordinada",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 2216,
    "f1": 2579,
    "tipo": "cta",
    "nombre": "presentador",
    "nota": "Rail estable",
    "evidence_level": "dense_observed"
  },
  {
    "f0": 2580,
    "f1": 2680,
    "tipo": "cierre",
    "nombre": "negro",
    "nota": "101f/100duplicados;mixdecay aftercut",
    "evidence_level": "dense_observed"
  }
]
```
