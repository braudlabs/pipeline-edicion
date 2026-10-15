export function selectedBrand(){const explicit=new URLSearchParams(location.search).get('brand');let saved;try{saved=localStorage.getItem('studio-active-brand');}catch{}return explicit||saved||'ecommerce';}
export function selectBrand(id){try{localStorage.setItem('studio-active-brand',id);}catch{}const url=new URL(location.href);url.searchParams.set('brand',id);location.assign(url);}
