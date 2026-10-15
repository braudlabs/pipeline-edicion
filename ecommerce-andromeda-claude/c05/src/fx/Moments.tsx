import React from 'react';
import {Flash, Glint, LensGlow, Spotlight, WordGlow} from './Fx';

// ───────── Momentos de luz de C05 (debajo de los subtítulos) ─────────
// Cada efecto está atado a una acción o a una palabra concreta del plano; ninguno se repite
// como receta por corte. Fotogramas en base 24 fps del máster.
export const Moments: React.FC = () => (
  <>
    {/* 02 · «semanas»: el ticket asoma (f406–413) y un reflejo cruza el papel. */}
    <Glint from={404} frames={13} dir="paper-matte" sceneFrom={350} srcIn={12} first={48} count={64} strength={0.8} />
    {/* 05 · corte a la máquina sobre el mostrador («Instalaremos…»): flash cálido del corte. */}
    <Flash at={782} frames={6} peak={0.42} x={540} y={1150} />
    {/* 08 · «Sí»: halo azul claro detrás de la palabra (respuesta satisfecha, sin golpe). */}
    <WordGlow at={1196} to={1207} x={540} y={806} size={250} />
    {/* 11 · «criterio»: foco sobre la propuesta elegida mientras se decide (lenguaje de foco del editor). */}
    <Spotlight from={1536} to={1584} x={568} y={1345} rx={330} ry={240} dim={0.4} />
    {/* 12 · los proyectores se encienden (f1621): destello en cada lente, escalonado. */}
    <LensGlow at={1621} x={670} y={800} size={150} />
    <LensGlow at={1621} x={803} y={818} size={150} delay={1} />
    <LensGlow at={1621} x={970} y={835} size={150} delay={2} />
    {/* 15 · remate final sobre «ads»: flash breve con el golpe grave de la música. */}
    <Flash at={2038} frames={5} peak={0.3} x={540} y={980} />
  </>
);
