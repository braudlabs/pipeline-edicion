const positive=value=>Math.max(0,Number(value)||0);

// Calculate both resting states from content geometry, never from an animated footer.
export function threadListLayout({rowBottoms=[],contentHeight=0,chrome=0,toggleHeight=0,gap=0,collapsedLimit=0,expandedLimit=0,expanded=false}){
 const rows=rowBottoms.map(positive).filter(Boolean),content=Math.max(positive(contentHeight),rows.at(-1)||0);
 const base=positive(chrome),footer=positive(toggleHeight)+positive(gap);
 const collapsed=Math.max(0,positive(collapsedLimit)-base-footer);
 const expandedRoom=Math.max(collapsed,positive(expandedLimit)-base-footer);
 const fitsWithoutToggle=content<=Math.max(0,positive(collapsedLimit)-base)+1;
 const snap=available=>Math.min(content,rows.filter(bottom=>bottom<=available+1).at(-1)??available);
 const canExpand=!fitsWithoutToggle&&snap(expandedRoom)>snap(collapsed)+1;
 const available=canExpand?(expanded?expandedRoom:collapsed):Math.max(0,positive(collapsedLimit)-base);
 // Finish on a full conversation row; the user can still scroll to every remaining row.
 const linksHeight=snap(available);
 return {linksHeight,listHeight:base+linksHeight+(canExpand?footer:0),canExpand};
}

const topOf=node=>{let top=0;for(let el=node;el;el=el.offsetParent)top+=el.offsetTop;return top;};
const px=(style,key)=>parseFloat(style[key])||0;

export function fitConversationList({list,composer,links,expanded=false}){
 if(!list||!composer||!links||!list.getClientRects().length)return null;
 const toggle=list.querySelector('.thread-expand'),heading=list.querySelector('.thread-list-heading'),order=list.querySelector('.thread-order');
 if(!toggle||!heading||!order)return null;
 const win=list.ownerDocument.defaultView,style=win.getComputedStyle(list),gap=px(style,'rowGap');
 const listTop=topOf(list),linksTop=topOf(links),composerTop=topOf(composer);
 const rows=[...links.querySelectorAll('.thread-row')];
 const rowBottoms=rows.map(row=>topOf(row)-linksTop+row.offsetHeight);
 const children=[...links.children];
 const contentHeight=Math.max(0,...children.map(child=>topOf(child)-linksTop+child.offsetHeight));
 const chrome=px(style,'paddingTop')+px(style,'paddingBottom')+px(style,'borderTopWidth')+px(style,'borderBottomWidth')+heading.offsetHeight+order.offsetHeight+gap*2;
 // Hidden controls have no offsetHeight; their measured size is retained for later growth.
 const toggleHeight=toggle.offsetHeight||Number(list.dataset.threadToggleHeight)||30;
 if(toggle.offsetHeight)list.dataset.threadToggleHeight=String(toggle.offsetHeight);
 const viewport=win.visualViewport,viewportBottom=win.scrollY+(viewport?.offsetTop||0)+(viewport?.height||win.innerHeight)-20;
 const collapsedLimit=Math.max(chrome+38,composerTop-listTop-12);
 const expandedLimit=Math.max(collapsedLimit,Math.min(viewportBottom,composerTop+composer.offsetHeight)-listTop);
 const layout=threadListLayout({rowBottoms,contentHeight,chrome,toggleHeight,gap,collapsedLimit,expandedLimit,expanded});
 toggle.hidden=!layout.canExpand;
 list.style.setProperty('--thread-list-height',layout.listHeight+'px');
 list.style.setProperty('--thread-links-height',layout.linksHeight+'px');
 list.dataset.threadExpanded=String(expanded&&layout.canExpand);
 links.classList.remove('fade-top','fade-bottom');links.onscroll=null;
 if(!list.dataset.threadMeasured){
  list.dataset.threadMeasured='true';
  // A new route takes its size directly. Only user changes interpolate afterwards.
  win.requestAnimationFrame(()=>{if(list.isConnected)list.dataset.threadMotion='ready';});
 }
 return layout;
}
