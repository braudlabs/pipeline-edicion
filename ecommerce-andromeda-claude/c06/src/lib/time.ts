import {createContext, useContext} from 'react';
import {useCurrentFrame} from 'remotion';

// Reloj de diseño: todo el montaje y la coreografía se definen en fotogramas de 24 fps
// (los del CSV y de la alineación). Una composición a 144 fps usa escala 6: el metraje
// repite cada fotograma fuente ×6 y los rótulos se evalúan en tiempo fraccionario.
export const TimeScale = createContext(1);
export const useScale = () => useContext(TimeScale);
/** Tiempo actual en fotogramas de 24 fps (fraccionario si la salida tiene más fps). */
export const useT = () => useCurrentFrame() / useContext(TimeScale);
