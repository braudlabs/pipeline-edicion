import type {Cue} from './motion';
export const cream='#fffdf1',accent='#dcf395',ink='#18382b';
// A block owns its resting layout. Shot changes never recompute these anchors.
const make=(block:string,defaults:Partial<Cue>,list:Partial<Cue>[])=>list.map(c=>({block,x:540,y:1390,size:126,motion:'direct',out:'cut',...defaults,...c}) as Cue);
export const cues:Cue[]=[
 ...make('hook',{out:'lift',outDuration:.07},[
  {id:'cansado',text:'¿Cansado',start:1.22,end:1.66,y:1110,size:138,motion:'soft',out:'cut'},
  {id:'dejarte',text:'de dejarte un',start:1.66,end:3.06,y:1110,size:96},
  {id:'rinon',text:'riñón',start:2.26,end:3.06,y:1415,size:350,color:accent,motion:'hero',tracking:-.06},
  {id:'bolas-hook',text:'en bolas',start:2.68,end:3.06,x:215,y:1500,size:91,anchor:'start',motion:'cascade',travel:34,duration:.20},
 ]),
 ...make('question',{y:1360},[
  {id:'cada',text:'cada vez que sales',start:3.06,end:3.76,size:122,motion:'soft',travel:20},
  {id:'jugar',text:'a jugar?',start:3.76,end:4.24,size:166,motion:'snap',out:'fade',outDuration:.09},
 ]),
 ...make('gag',{x:748,y:1140},[
  {id:'venga1',text:'venga…',start:4.44,end:4.84,size:86,motion:'soft',axis:'x',direction:1,travel:24},
  {id:'venga2',text:'venga…',start:4.84,end:5.00,size:99},
  {id:'venga3',text:'¡VENGA!',start:5,end:5.34,size:116,color:accent,motion:'snap',out:'fade'},
  {id:'no',text:'¡NO!',start:6.22,end:6.63,x:540,size:335,condensed:true,color:ink,motion:'snap',out:'fade',outDuration:.09},
 ]),
 ...make('reassurance',{},[
  {id:'tranquilo',text:'Tranquilo,',start:7.62,end:8.06,motion:'soft'},
  {id:'mindunguis',text:'mindunguis.',start:8.06,end:8.59,size:136,out:'fade'},
 ]),
 ...make('solution',{end:9.97,out:'lift',outDuration:.085},[
  {id:'traigo',text:'que te traigo la',start:8.62,x:540,y:355,size:79,motion:'cascade',travel:35,duration:.22},
  {id:'solucion',text:'SOLUCIÓN',start:9.34,y:570,size:201,weight:700,color:accent,motion:'hero',strength:.62,masked:true},
  {id:'solucion-outline',text:'SOLUCIÓN',start:9.34,y:570,size:201,weight:700,color:accent,motion:'hero',strength:.62,outline:true},
 ]),
 ...make('literal-brand',{},[
  {id:'literal',text:'Literalmente.',start:10.74,end:11.31,size:126,out:'fade'},
  {id:'en',text:'En',start:11.48,end:11.76,size:108,motion:'soft'},
  {id:'brand',text:'Birdieballs.',start:11.76,end:12.30,size:138,out:'fade',outDuration:.045},
 ]),
 ...make('product',{y:900,contrast:true},[
  {id:'recuperamos',text:'recuperamos',start:12.30,end:12.86,size:136,motion:'soft',travel:24},
  {id:'bolas-product',text:'bolas',start:12.86,end:13.70,x:150,size:108,anchor:'start',motion:'soft',out:'lift',outDuration:.06},
  {id:'originales',text:'originales',start:13.16,end:13.70,x:418,size:144,weight:700,color:accent,anchor:'start',motion:'reveal',duration:.21,revealWidth:610,out:'lift',outDuration:.06},
  {id:'marcas',text:'de tus marcas',start:13.70,end:14.30,size:132,motion:'soft',travel:18},
  {id:'favoritas',text:'favoritas.',start:14.30,end:14.95,size:170,motion:'hero',strength:.5,color:accent,out:'fade'},
  {id:'lagos',block:'origins',y:1390,text:'De lagos,',start:15.08,end:15.90,size:146,motion:'soft',travel:22},
  {id:'campos',block:'origins',y:1390,text:'de campos…',start:15.90,end:16.76,size:146,out:'fade',outDuration:.05},
 ]),
 ...make('reaction',{},[
  {id:'mecago',text:'me cago en…',start:16.79,end:17.44,size:108,motion:'soft',out:'fade'},
  {id:'justo',text:'Justo',start:18.72,end:19.16,size:126,motion:'soft'},
  {id:'ahi',text:'Justo ahí.',start:19.16,end:19.47,size:140,out:'fade'},
 ]),
 ...make('cleaning',{y:560,out:'cut'},[
  {id:'las-limpieza',text:'Las',start:19.62,end:20,size:122,motion:'soft'},
  {id:'limpiamos',text:'Las limpiamos',start:20,end:20.54,size:134},
  {id:'y-las',text:'y las',start:20.54,end:20.82,size:122},
  {id:'revisamos',text:'y las revisamos',start:20.82,end:21.40,size:134},
  {id:'una1',text:'una',start:21.40,end:22.34,x:340,size:156,color:accent,motion:'cascade',travel:40,out:'lift',outDuration:.07},
  {id:'a-una',text:'a',start:21.86,end:22.34,size:98,motion:'soft',travel:20,out:'lift',outDuration:.07},
  {id:'una2',text:'una.',start:22.06,end:22.34,x:747,size:156,color:accent,motion:'cascade',travel:40,out:'lift',outDuration:.07},
 ]),
 ...make('inspection-dialogue',{},[
  {id:'al-punto',text:'Al punto de que',start:22.42,end:23.12,size:117,motion:'soft'},
  {id:'ni-el',text:'ni el',start:23.12,end:23.36,size:117},
  {id:'mindunguis2',text:'ni el mindunguis este',start:23.36,end:24.10,size:112},
  {id:'se-da-cuenta',text:'se da cuenta',start:24.10,end:24.62,size:127},
  {id:'no-son',text:'de que no son',start:24.62,end:25.58,y:1270,size:95,motion:'soft',travel:18,out:'lift',outDuration:.075},
  {id:'nuevas',text:'nuevas.',start:25.16,end:25.58,y:1460,size:230,color:accent,motion:'hero',strength:.65,out:'lift',outDuration:.075},
  {id:'pues-si',text:'Pues sí que están',start:25.68,end:26.16,size:112,motion:'soft',travel:18},
  {id:'como-nuevas-dialogo',text:'como nuevas,',start:26.16,end:26.88,size:146},
  {id:'si-remate',text:'sí.',start:26.88,end:27.04,size:112,out:'fade',outDuration:.04},
 ]),
 ...make('offer',{y:330,contrast:true,strokeWidth:2.6},[
  {id:'tu-lo-has-dicho',text:'Tú lo has dicho.',start:27.34,end:28.06,size:110,motion:'soft',out:'fade'},
  {id:'como-nuevas-oferta',text:'Como nuevas',start:28.20,end:28.80,size:117,motion:'soft'},
  {id:'hasta-un',text:'y hasta un',start:28.80,end:30.16,size:114},
  {id:'mas-baratas',text:'más baratas.',start:30.16,end:30.99,size:124,weight:700,motion:'snap',out:'fade'},
 ]),
 ...make('cta',{},[
  {id:'no-esperes',text:'No esperes más',start:31.16,end:31.86,size:122,motion:'soft'},
  {id:'pide',text:'y pide las tuyas.',start:31.86,end:32.72,size:126,highlight:'tuyas',motion:'soft',travel:18,out:'fade'},
  {id:'que-el-golf',text:'Que el golf',start:32.92,end:33.44,size:123,motion:'soft'},
  {id:'esta-para',text:'está para',start:33.44,end:33.90,size:123},
  {id:'disfrutarlo',text:'disfrutarlo,',start:33.90,end:34.53,size:165,color:accent,motion:'hero',strength:.45,out:'fade'},
  {id:'chaval',text:'chaval.',start:34.62,end:35.08,size:126,out:'fade'},
 ]),
 ...make('brand-close',{y:900},[
  {id:'birdie-end',text:'Birdieballs.',start:35.52,end:36.06,size:140,motion:'soft',out:'fade'},
  {id:'juega-mas',text:'Juega más,',start:36.12,end:37.95,size:145,motion:'cascade',travel:34,out:'fade',outDuration:.12},
  {id:'por-menos',text:'por menos.',start:36.88,end:37.95,y:1070,size:173,color:accent,motion:'cascade',duration:.28,travel:42,out:'fade',outDuration:.12},
 ]),
];
