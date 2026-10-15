# Ampliación V2 ·10-10-2026

Estado vigente:11referencias,28.384frames con OCR,3.110pistas OCR no certificadas y506observaciones. [Interfaz de estudio](http://127.0.0.1:4317/study). [EspecificaciónV2](ALGORITMO-V2.md). Revisión nativa y sonido **incompletos**; el contador automático no acredita exhaustividad. Ver `CURRENT-STUDY.json.revision_v2`. La tabla siguiente conserva la cobertura anterior de10vídeos; no incluye V8.

# Estado del estudio

Actualizado: 2026-10-10T15:55:29.307412+00:00 (UTC).

Fuente regenerable: `python3 scripts/estado.py`. Copia las notas en curso a `notas/`, fuera del directorio ignorado `analysis/`.

El estudio solo se cierra cuando cada tramo declara revisión forense completa y tiene cobertura de todas sus hojas densas y suplementarias. Una revisión de hojas reducidas no certifica todos los detalles nativos.

| Tramo | Densas abiertas / total | Suplementarias abiertas / total | Estado declarado | Forense completa |
|---|---:|---:|---|---|
| [v1-pagado-A](notas/v1-pagado-A.md) | 16/16 | 1/1 | partial | no |
| [v1-pagado-B](notas/v1-pagado-B.md) | 16/16 | 0/0 | partial | no |
| [v1-pagado-C](notas/v1-pagado-C.md) | 15/15 | 0/0 | partial | no |
| [v2-churros-A](notas/v2-churros-A.md) | 20/20 | 1/1 | partial | no |
| [v2-churros-B](notas/v2-churros-B.md) | 20/20 | 2/2 | partial | no |
| [v3-ia-cara-A](notas/v3-ia-cara-A.md) | 19/19 | 0/0 | partial | no |
| [v3-ia-cara-B](notas/v3-ia-cara-B.md) | 19/19 | 0/0 | partial | no |
| [v5-maquina-A](notas/v5-maquina-A.md) | 17/17 | 3/3 | partial | no |
| [v5-maquina-B](notas/v5-maquina-B.md) | 17/17 | 3/3 | partial | no |
| [v5-maquina-C](notas/v5-maquina-C.md) | 15/15 | 4/4 | partial | no |
| [v6-ads90-rev-A](notas/v6-ads90-rev-A.md) | 15/15 | 8/8 | partial | no |
| [v6-ads90-rev-B](notas/v6-ads90-rev-B.md) | 15/15 | 8/8 | partial | no |
| [v6-ads90-rev-C](notas/v6-ads90-rev-C.md) | 15/15 | 7/7 | partial | no |
| [lafabrica-v1-A](notas/lafabrica-v1-A.md) | 14/14 | 1/1 | partial | no |
| [lafabrica-v1-B](notas/lafabrica-v1-B.md) | 13/13 | 1/1 | partial | no |
| [lafabrica-v2p1-A](notas/lafabrica-v2p1-A.md) | 16/16 | 1/1 | partial | no |
| [lafabrica-v2p1-B](notas/lafabrica-v2p1-B.md) | 16/16 | 1/1 | partial | no |
| [lafabrica-v2p1-C](notas/lafabrica-v2p1-C.md) | 15/15 | 1/1 | partial | no |
| [landing-A](notas/landing-A.md) | 21/21 | 4/4 | dense_complete_native_partial | no |
| [landing-B](notas/landing-B.md) | 21/21 | 9/9 | partial | no |
| [landing-C](notas/landing-C.md) | 21/21 | 2/2 | partial | no |
| [landing-D](notas/landing-D.md) | 21/21 | 13/13 | partial | no |
| [landing-E](notas/landing-E.md) | 21/21 | 28/28 | partial | no |
| [landing-F](notas/landing-F.md) | 18/18 | 13/13 | partial | no |
| [v7-ads90-rev-A](notas/v7-ads90-rev-A.md) | 8/8 | 7/7 | partial | no |
| [v6-ads90-A](notas/v6-ads90-A.md) | 15/15 | 8/8 | dense_complete_native_partial | no |
| [v6-ads90-B](notas/v6-ads90-B.md) | 15/15 | 8/8 | dense_complete_native_partial | no |
| [v6-ads90-C](notas/v6-ads90-C.md) | 15/15 | 7/7 | dense_complete_native_partial | no |
| [v7-ads90-rev-B](notas/v7-ads90-rev-B.md) | 35/35 | 17/17 | dense_complete_native_partial | no |

## Auditoría de omisiones

`repeat_frames` heredado usa diferencia por bloques en JPG reducidos, umbral 3/255; no son duplicados exactos. La auditoría nueva compara hashes de todos los fotogramas decodificados a resolución nativa.

| Vídeo | Fotogramas | Idénticos al anterior | Omitidos legacy no idénticos |
|---|---:|---:|---:|
| landing | 5680 | 83 | 1907 |
| v1-pagado | 1898 | 37 | 3 |
| v2-churros | 1699 | 42 | 72 |
| v3-ia-cara | 1542 | 28 | 0 |
| v5-maquina | 2291 | 35 | 335 |
| v6-ads90 | 2650 | 64 | 817 |
| v6-ads90-rev | 2650 | 64 | 812 |
| v7-ads90-rev | 2681 | 100 | 897 |
| lafabrica-v1 | 1096 | 32 | 15 |
| lafabrica-v2p1 | 1907 | 31 | 18 |

## Continuación independiente

1. Leer `README.md`, `DECISIONES.md`, `METODO.md`, `ALGORITMO.md` y este estado.
2. Retomar las hojas `dense_missing` / `supplemental_missing` de `CURRENT-STUDY.json` y los detalles pendientes de cada nota; escribir cobertura al terminar cada lote.
3. Guardar evidencia nativa por índice explícito con `sheet.py`; no usar tiempo de seek para asignar fotogramas.
4. Ejecutar `estado.py`, `consolidate.py`, `stats.py` y `estado.py` al terminar. Mantener distinción entre detector, observación y propuesta.
