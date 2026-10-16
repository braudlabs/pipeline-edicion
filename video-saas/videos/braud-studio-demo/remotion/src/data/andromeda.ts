import {ClipCrop} from '../Clip';

// Planos del anuncio de la maquinita (Ecommerce Andrómeda) y su encuadre: zoom z anclado en (fx, fy).
// Criterio (veto de Ale, 15/10): la sudadera morada no aparece; manda la máquina y su pantalla.
// `offset`: segundo del clip desde el que se usa (en algunos, la cámara acaba descubriendo la sudadera).
export const SHOTS: Record<string, {id: string; crop: ClipCrop; what: string; offset?: number}> = {
  aprobados: {id: 'V07b-hq', crop: {z: 1.5, fx: 0.3, fy: 0.9}, what: 'tres zapatillas con check verde en la pantalla', offset: 1.0}, // limpio solo entre 1,0 y 3,3 s,
  campanas: {id: 'V07a-hq', crop: {z: 1.25, fx: 0.3, fy: 0.6}, what: 'pantalla «Campañas» con barras verdes'},
  perchero: {id: 'V12a-hq', crop: {z: 2.0, fx: 0.0, fy: 0.4}, what: 'perchero de creativos impresos'},
  maquina: {id: 'V05-hq', crop: {z: 1.8, fx: 0.1, fy: 0.95}, what: 'la maquinita'},
  pantalla: {id: 'V08a-hq', crop: {z: 1.6, fx: 0.35, fy: 0.8}, what: 'pantalla con dos versiones'},
  lavadora: {id: 'V09a-hq', crop: {z: 1.8, fx: 0.0, fy: 0.9}, what: 'ojo de pez desde dentro de la lavadora'},
  estanteria: {id: 'V12b-hq', crop: {z: 2.2, fx: 0.6, fy: 0.2}, what: 'zapatillas en la estantería'},
  maquinaLado: {id: 'V15b-hq', crop: {z: 1.7, fx: 0.9, fy: 1.0}, what: 'la máquina con la zapatilla en pantalla'},
  sesion: {id: 'V06c-hq', crop: {z: 1.75, fx: 0.25, fy: 0.9}, what: 'sesión de producto en la pantalla'},
  anuncio: {id: 'V13-hq', crop: {z: 1.7, fx: 0.75, fy: 0.55}, what: 'el anuncio en la pantalla y el azul', offset: 3.0},
  impresos: {id: 'V11-hq', crop: {z: 2.2, fx: 0.5, fy: 1.0}, what: 'anuncios impresos sobre la mesa'},
  suela: {id: 'V08b-hq', crop: {z: 1.8, fx: 0.0, fy: 0.85}, what: 'la suela en la pantalla'},
  textura: {id: 'V06d-hq', crop: {z: 1.8, fx: 0.3, fy: 0.95}, what: 'textura de la suela en pantalla'},
  detalle: {id: 'V07c-hq', crop: {z: 2.0, fx: 0.3, fy: 1.0}, what: 'detalle de la zapatilla en pantalla'},
};
/**
 * «Listo para publicar»: los anuncios aprobados en la pantalla de la máquina (V07b, 1,0–3,1 s a 0,7×).
 * El montaje final (C05) lleva la sudadera detrás de la máquina en todo el tramo y, recortado, pierde los subtítulos.
 */
export const FINAL_AD = {id: 'V07b-hq', offset: 1.0, rate: 0.7, crop: {z: 1.5, fx: 0.3, fy: 0.9}};
