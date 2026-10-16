# landing-A

Revisión de Codex, 10/10/2026. Índices desde 0, extremos incluidos, 60 fps. Todas las hojas densas abiertas; cobertura nativa parcial, límites explícitos. Audio: espectrogramas del mix, sin identificación auditiva de SFX.

## 1. Planos

f0–214 sujeto camiseta negra, ayudante coloca micrófono, fondo negro/halo. Corte215 a escala mayor; corte308 perfil,508 frontal,570 perfil. Todos los bordes comprobados con selección de índice nativo. Primera voz transcrita f408; el arranque contiene sonido y acciones aunque Whisper no dé palabras.

## 2. Cortes y transiciones

215,308,508,570 son cambios secos. Intro y bienvenida sostienen continuidad por encima de cambios; placas de fundador mantienen posición a través570. El texto inicia/transiciona independientemente de metraje.

## 3. Subtítulos base

Intro lateral blanca fina: Gracias primera tinta9, acumulación por/reservar hasta línea completa. Te ya aparece86 mientras sale Gracias (última línea89, fuera90), continúa movimiento ascendente; dejamos96 y resto forma Te dejamos un mensaje de los fundadores. Ponte209 y resto de auriculares/experiencia acumula otra frase. La salida409–426 no borra todo a la vez: letras desaparecen alrededor421/422, auriculares aún423 y teléfono tenue426. Buenas416 ya íntegra a tamaño/posición final (x≈50%,y≈77%); Soy451/Alejandro470 usan rail inferior. No trasladar entrada fina a rail.

## 4. Énfasis

*inaudible* lima desde inicio, y≈76%. Bienvenida no es rail hablado. Gracias se desplaza arriba al entrar: cy585.6f9,580.5f10,575.5f11,569f13,561.5f16,555f20,548f26,544f32,542f35,540f40; estabiliza≈537.5 hacia55. Ancho127/128px y alto38/39px permanecen casi constantes. Contrast metric aumenta; no equivale a alpha ni demuestra easing original.

## 5. Escenas gráficas

Tarjetas de prueba social integradas a la izquierda mientras persona ocupa derecha. Primera tarjeta: avatar632, cabecera635, estadísticas641–647,bio649–655,botones655–666. Segunda:681–683 aún vacía; avatar684,cabecera686,estadísticas692–698,bio700–710,botones711–723; estable hacia725. Hay revelado por partes, no demostración de zoom uniforme de captura entera.

## 6. Superposiciones

Iconos son auriculares y teléfono vibrando. Placa fundador entra517–536:517/518 streak horizontal, cargo519,nombre520 inicialmente solapados; cargo se despliega/reposiciona debajo hasta534, línea extiende hacia derecha523–536. No basta etiquetar entrada por izquierda. Placa y rail cumplen funciones diferentes, permanecen a través corte570.

## 7. Sonido

Espectros0–8 y8–16 abiertos. Banda ancha fuerte inicio≈5s, región más armónica≈5.1–6.9, voz desde≈6.9. Picos3.48/3.64 próximos al corte215 no permiten identificar whoosh/impacto. No hubo escucha validada ni separación de pistas.

## 8. Ritmo

6.8s prepara el rodaje y la experiencia antes de voz. Frases intro acumulan mientras planos cambian. Fundador se identifica después del saludo; prueba social sigue mención contextual, con secuencia de elementos en vez de efecto aislado.

## 9. Reglas respaldadas

Modelar overlay con ciclo independiente de plano; permitir solapamiento de salidas/entradas de frases. Entrada protagonista/lateral y sustitución ordinaria usan comportamientos distintos. Prueba social requiere elementos/mascaras de revelado por etapas. Landings no heredan ritmo de gancho vertical automáticamente.

## 10. Dudas y alcance

21/21densas y4/4suplementarias abiertas;11 rangos nativos abiertos. Curva Gracias: ROI completa evita clipping que contaminaba medición anterior. Distancia RGB/255 puede superar1 (máximo√3): métricas de contraste no son alpha. Nameplate no tiene aún curva de cada componente ni cada palabra del rail comprobada nativa. No certificar estudio forense exhaustivo. Final exacto del pictograma tras426 pendiente.

## 11. Láminas

Evidencia persistente laminas/landing-A: intro-gracias, intro-handoff, intro-exit, buenas-entry, name-entry, proof-entry, proof2-entry y cortes215/308/508/570. Tabla medidas/landing-A/gracias-ink-all.tsv de selección por índice exacto. Los crops completos llevan índices visibles.

## Sucesos estructurados

```json
[
  {
    "f0": 9,
    "f1": 89,
    "tipo": "texto",
    "nombre": "Gracias",
    "nota": "Movimiento ascendente casi48px; contrasta con rail directo",
    "evidence_level": "native_verified"
  },
  {
    "f0": 86,
    "f1": 96,
    "tipo": "texto",
    "nombre": "solapamiento_Gracias_Te",
    "nota": "Te visible antes de desaparecer frase previa",
    "evidence_level": "native_verified"
  },
  {
    "f0": 215,
    "f1": 215,
    "tipo": "corte",
    "nombre": "escala_mayor",
    "nota": "Intro persiste",
    "evidence_level": "native_verified"
  },
  {
    "f0": 308,
    "f1": 308,
    "tipo": "corte",
    "nombre": "perfil",
    "nota": "Intro persiste",
    "evidence_level": "native_verified"
  },
  {
    "f0": 409,
    "f1": 426,
    "tipo": "salida",
    "nombre": "letras_iconos",
    "nota": "Desaparición escalonada",
    "evidence_level": "native_verified"
  },
  {
    "f0": 416,
    "f1": 419,
    "tipo": "texto",
    "nombre": "Buenas",
    "nota": "Entrada íntegra a escala final",
    "evidence_level": "native_verified"
  },
  {
    "f0": 508,
    "f1": 508,
    "tipo": "corte",
    "nombre": "frontal",
    "nota": "Saludo",
    "evidence_level": "native_verified"
  },
  {
    "f0": 517,
    "f1": 536,
    "tipo": "overlay",
    "nombre": "placa_fundador",
    "nota": "Streak/cargo/nombre/línea con trayectorias distintas",
    "evidence_level": "native_verified"
  },
  {
    "f0": 570,
    "f1": 570,
    "tipo": "corte",
    "nombre": "perfil",
    "nota": "Placa persiste",
    "evidence_level": "native_verified"
  },
  {
    "f0": 632,
    "f1": 666,
    "tipo": "prueba",
    "nombre": "perfil1",
    "nota": "Avatar/cabecera/estadísticas/bio/botones secuenciales",
    "evidence_level": "native_verified"
  },
  {
    "f0": 684,
    "f1": 725,
    "tipo": "prueba",
    "nombre": "perfil2",
    "nota": "Revelado por partes",
    "evidence_level": "native_verified"
  }
]
```
