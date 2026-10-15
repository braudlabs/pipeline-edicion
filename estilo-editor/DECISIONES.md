# Decisiones vigentes

Fuente: mensajes de Ale en la última sesión local de Claude del proyecto, recuperados
el 10/10/2026. Las interpretaciones del agente se indican como tales.

| Decisión | Evidencia y alcance |
|---|---|
| Reproducir estilo profesional con Remotion | Ale pidió estudiar diez vídeos para crear un algoritmo que permita editar de esa forma con Remotion. No convertir el estudio en un nuevo anuncio. |
| Evitar AE como dependencia del producto | Ale explicó que quiere comercializar el pipeline y AE añade coste y complejidad. Esta decisión específica actualiza la elección anterior de herramientas para producir anuncios concretos. |
| No renderizar pruebas durante el estudio | «actualiza remotion, de mientras no hagamos pruebas». La actualización de Remotion fue reportada por Claude; no se repite ni se hacen renders. Las comprobaciones de índices y datos son parte de la medición. |
| Máximo detalle temporal | Ale rechazó mirar segundo a segundo porque se pierden detalles. Se revisan hojas con fotogramas consecutivos y se extraen eventos a resolución nativa. |
| Revisores por tramos | Ale pidió lanzar los ocho tramos pendientes. La continuación conserva esa división con revisores y añade cobertura de variantes que faltaba. |
| SF Pro se conserva | «usaremos SF pro sin problema, no pasa nada». No volver a proponer cambio de fuente. Bold/Thin y otros estilos concretos se confirman por evidencia. |
| Documentación independiente de la sesión | «todo este estudio ... se debe dejar redactado y actualizado ... sin tener que depender de esta sesión». Estado, cobertura, notas, evidencias y reglas viven en este proyecto. |
| Pasar del documento a un motor ejecutable | Ale: «necesito un motor que sea capaz de aplicar el mismo estilo de edición que el de las refs». Se crea `motor-editor/` en Remotion, aislado de los anuncios anteriores. Implementación y pruebas funcionales autorizadas por el encargo; no se interpreta como aprobación estética ni como reanudación de renders. |
| Incluir motion graphics y reconocer lo incompleto | Ale pregunta explícitamente si se estudió su estilo. `MOTION-GRAPHICS.md` enlaza estudio, mediciones, recetas y límites. Una adaptación funcional no se presenta como réplica verificada. |

Las preferencias anteriores de Ale siguen siendo contexto para diseñar una pieza
nueva, pero no reescriben lo observado en las referencias. Por ejemplo, observar un
subtítulo sobre una cabeza en LaFabrica no convierte esa posición en preferencia de
Ale; tampoco la preferencia por entradas en un eje permite afirmar que todas las
palabras de las referencias entran animadas.

No hay aprobación del algoritmo completo, de un render nuevo ni de cualquier
reconstrucción aún no realizada. Los ejemplos aprobados de Cocina son locales a
aquellos fragmentos. Este estudio no modifica esos proyectos.

## Actualización: pruebas cortas y revisión visual

Ale autoriza comenzar pruebas de edición con un clip de unos 20 segundos para acortar las iteraciones. Queda levantada la pausa anterior de renders para estas pruebas. Solicita una interfaz de versiones, comentarios por frame/intervalo y marcas espaciales. Se implementa localmente en `motor-editor/review/`, con persistencia de notas y evidencias por versión. El clip del usuario aún no se ha recibido al preparar la interfaz; las verificaciones de interfaz usan un vídeo sintético aparte.
