import data from '../data/words.json';
import hook from '../data/hook-native-words.json';
import {FPS} from './anim';

export type Word = {i: number; text: string; start: number; end: number};
export const WORDS: Word[] = data.words;
export const HOOK_WORDS = hook.words as {text: string; start: number; end: number}[];

/** Fotograma que contiene el inicio de la palabra (la palabra aparece con su sonido). */
export const wf = (i: number) => Math.floor(WORDS[i].start * FPS + 1e-6);
/** Fotograma en que termina de pronunciarse. */
export const we = (i: number) => Math.ceil(WORDS[i].end * FPS - 1e-6);
/** Texto mostrado: corrección del ASR (ecommerce, IA…) ya aplicada en el guion alineado. */
export const wt = (i: number) => WORDS[i].text;
export const strip = (s: string) => s.replace(/[.,;:«»"]/g, '');
