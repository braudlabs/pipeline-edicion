# Remotion frente a After Effects

> Rendimiento medido de AE frente a Remotion y con cuál abordar cada pieza

Medido en septiembre de 2026 al recrear los gráficos de AD3 V8 en Remotion:

- **AE**: ~17 fps con desenfoque de movimiento y cámara 3D (piloto BRAUDLABS, 67
  fotogramas en 4 s).
- **Remotion**: 6,83 fps sin desenfoque y 0,86 fps con 8 muestras de obturador, sobre la
  comp más pesada (294 fotogramas, 90 capas). El obturador cuesta exactamente ×8.

**Cómo aplicarlo:** AE para producir, porque es más rápido y el 3D y el desenfoque salen
de fábrica. Remotion cuando haga falta reproducibilidad, verificación automática o
volumen — variantes del mismo anuncio, piezas parametrizadas, render en servidor sin
licencia ni GUI. Portar de AE a Remotion solo con una razón concreta: el último 5 % de
fidelidad es el caro, y el trazado espacial de AE no se ha conseguido igualar del todo.

**Actualización 10/10/2026, sin probar aquí:** Remotion trae desde la 4.0.529
`<HtmlInCanvasMotionBlur>`, obturador real por muestreo y promedio (180° y 8 muestras por
defecto), y su documentación lo recomienda sobre `<CameraMotionBlur>`, que altera color y
opacidad al apilar capas. El repo estaba en 4.0.525, por eso el obturador se construyó a
mano. El 10/10/2026 actualicé a 4.0.534 la raíz, `ad3-pipeline/remotion-mg` y el pin de
`ad4-creatina/remotion`; el resto sigue en 4.0.525. Queda pendiente medir el obturador
oficial contra el propio (comp 05 de AD3); detalle en el §11 de
`MOTION-GRAPHICS-AE-REMOTION.md`. Si el criterio es
calidad máxima sin AE, ver «objetivo-comercializar-sin-ae» (nota interna, no publicada).

Todas las equivalencias (interpolación por influencia y velocidad, 3D, efectos, texto) y
los tropiezos están en `MOTION-GRAPHICS-AE-REMOTION.md`, en la raíz del repo. Ver también
[La spec de diseño de AE se desincroniza del .aep](ae-spec-desincronizada.md).
