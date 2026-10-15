import {createContext, useContext} from 'react';
import {useT} from '../lib/time';
import {Cam, camAt, CamEvent} from './camera';

// ───────── Plan de cámara de C06 («upgrade infernal», Ale tras C05) ─────────
// Cada movimiento está atado a una palabra o a una acción del plano (fotogramas de 24 fps del
// máster); ninguno se repite como receta por corte. Familias del estudio del editor: golpe de
// zoom en la palabra que pesa, zoom por escalones cuando la voz repite («días y días», «meses y
// meses»), empuje lento mientras se explica, caída cuando algo «se cae» y temblor en el impacto.

// Bloque protagonista (presentación de la máquina, f740–840): dos alternativas para el estudio
// de fotogramas. A = barrido + flash + onda + chispas. B = apagón y haz cenital.
export type VariantId = 'A' | 'B';
export const Variant = createContext<VariantId>('A');
export const useVariant = () => useContext(Variant);

const FACE_03B: [number, number] = [600, 660];

const COMMON: CamEvent[] = [
  // 00 · hook (aprobado): solo un empuje muy suave y un golpe corto en «Andrómeda».
  {k: 'push', from: 0, to: 128, amt: 0.03, x: 520, y: 760, until: 130},
  {k: 'punch', at: 56, amt: 0.025, x: 520, y: 700, release: 9},
  // 01 · «es la misma MIERDA de siempre»: golpe y temblor sobre el cartel de la persiana.
  {k: 'punch', at: 210, amt: 0.045, x: 520, y: 640},
  {k: 'shake', at: 211, frames: 6, amp: 10, seed: 3},
  // 01 · «días y días»: dos escalones de zoom (el tiempo se acumula) hasta el corte.
  {k: 'steps', ats: [246, 263], amt: 0.025, x: 540, y: 900, until: 350},
  // 02 · «semanas»: empuje hacia la ranura mientras sale el ticket.
  {k: 'push', from: 396, to: 422, amt: 0.07, x: 700, y: 860, until: 450},
  // 03 · «se te han caído los ads»: la imagen cae.
  {k: 'drop', at: 519, amt: 0.05, frames: 14},
  // 03b · «OTRA PUTA VEZ»: tres golpes que crecen y temblor en «vez».
  {k: 'punch', at: 579, amt: 0.02, x: FACE_03B[0], y: FACE_03B[1]},
  {k: 'punch', at: 585, amt: 0.035, x: FACE_03B[0], y: FACE_03B[1]},
  {k: 'punch', at: 593, amt: 0.055, x: FACE_03B[0], y: FACE_03B[1], release: 12},
  {k: 'shake', at: 594, frames: 7, amp: 12, seed: 5},
  // 04 · «Vengo a hablarte de la solución»: empuje hacia el prota antes del corte.
  {k: 'push', from: 740, to: 781, amt: 0.06, x: 430, y: 520, until: 782},
  // 05 · «esta maquinita» / 06 · «5 ads».
  {k: 'punch', at: 823, amt: 0.025, x: 500, y: 1000},
  {k: 'punch', at: 856, amt: 0.03, x: 450, y: 1100},
  // 08 · «Sí» y «escalarás» (empuje en el primer plano, hasta su corte en 1229).
  {k: 'punch', at: 1199, amt: 0.035, x: 540, y: 820},
  {k: 'push', from: 1211, to: 1229, amt: 0.07, x: 640, y: 640, until: 1229},
  // 09 · «Pero eh,» y la bola de papel que cae en la cesta (impacto ≈ f1268).
  {k: 'punch', at: 1250, amt: 0.02, x: 300, y: 650},
  {k: 'punch', at: 1268, amt: 0.03, x: 600, y: 1330},
  {k: 'shake', at: 1268, frames: 8, amp: 10, seed: 9},
  {k: 'punch', at: 1328, amt: 0.03, x: 520, y: 1640},
  // 10 · los fundadores: golpe en cada nombre y escalones en «meses y meses».
  {k: 'punch', at: 1367, amt: 0.03, x: 575, y: 820},
  {k: 'punch', at: 1405, amt: 0.03, x: 420, y: 713},
  {k: 'steps', ats: [1461, 1473], amt: 0.025, x: 420, y: 713, until: 1478},
  // 11 · «criterio»: empuje lento hacia el prota durante todo el plano.
  {k: 'push', from: 1478, to: 1584, amt: 0.05, x: 821, y: 500, until: 1585},
  // 12 · «una máquina» (los proyectores se encienden en 1621).
  {k: 'punch', at: 1619, amt: 0.03, x: 820, y: 820},
  // 13 · «la maquinita».
  {k: 'punch', at: 1747, amt: 0.03, x: 740, y: 1150},
  // 15 · remate en «ads.».
  {k: 'punch', at: 2038, amt: 0.05, x: 700, y: 1100, release: 12},
  {k: 'shake', at: 2039, frames: 6, amp: 8, seed: 11},
];

const BLOCK: Record<VariantId, CamEvent[]> = {
  // A: la máquina «aterriza» con un golpe al salir del barrido.
  A: [{k: 'punch', at: 784, amt: 0.04, x: 560, y: 1050, release: 12}],
  // B: sin golpe; la luz hace el trabajo.
  B: [{k: 'push', from: 782, to: 840, amt: 0.03, x: 560, y: 1050, until: 840}],
};

export const camEvents = (v: VariantId): CamEvent[] => [...COMMON, ...BLOCK[v]];

/** Barrido (whip) en el corte: desenfoque horizontal que crece hasta el corte y se disipa. */
export type Whip = {at: number; pre: number; post: number; px: number};
const WHIPS: Record<VariantId, Whip[]> = {A: [{at: 782, pre: 4, post: 4, px: 48}], B: []};
export function whipAt(v: VariantId, t: number): number {
  for (const w of WHIPS[v]) {
    if (t >= w.at - w.pre && t < w.at) return w.px * ((t - (w.at - w.pre)) / w.pre) ** 2;
    if (t >= w.at && t < w.at + w.post) return w.px * (1 - (t - w.at) / w.post) ** 1.6;
  }
  return 0;
}

/** Fallo de imagen «meta» en «este mismo ad» (13): franjas desplazadas 3 fotogramas. */
export const GLITCHES = [{at: 1729, frames: 3}];

export const useCamAt = () => {
  const v = useVariant();
  const ev = camEvents(v);
  return (t: number): Cam => camAt(ev, t);
};
export const useCam = (): Cam => useCamAt()(useT());
