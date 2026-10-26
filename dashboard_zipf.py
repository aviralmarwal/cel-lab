# District urban-hierarchy explorer (Zipf exponent b by district). Data: docs/assets/data/district-zipf.json

CSS = r"""
/* district explorer */
.zx-top{display:grid;grid-template-columns:minmax(0,11fr) minmax(0,9fr);gap:22px;align-items:start}
#zxMap svg{width:100%;height:auto;display:block}
#zxMap path{stroke:#fff;stroke-width:.45;cursor:pointer;transition:opacity .15s}
#zxMap path.nd{fill:#e9e4da;cursor:default}
#zxMap path:hover{stroke:#16222e;stroke-width:1.2}
#zxMap path.sel{stroke:#16222e;stroke-width:1.6}
#zxMap path.stl{fill:none;stroke:#16222e;stroke-width:.7;pointer-events:none;opacity:.55}
.zx-legend{display:flex;align-items:center;gap:10px;margin-top:10px;font-size:12px;color:var(--muted);flex-wrap:wrap}
.zx-legend .ramp{display:flex}
.zx-legend .ramp i{width:26px;height:12px;display:inline-block}
@media(max-width:900px){.zx-top{grid-template-columns:1fr}}
.zx-search{position:relative}
.zx-search input{width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:2px;background:var(--cream);font-family:var(--sans);font-size:15px;color:var(--ink)}
.zx-search input:focus{border-color:var(--teal);outline:none}
.zx-sugg{position:absolute;left:0;right:0;top:100%;background:var(--paper);border:1px solid var(--line);border-top:none;z-index:20;max-height:260px;overflow:auto;display:none}
.zx-sugg div{padding:9px 14px;font-size:14px;cursor:pointer}
.zx-sugg div:hover,.zx-sugg div.on{background:var(--cream)}
.zx-sugg span{color:var(--muted);font-size:12.5px;margin-left:6px}
.zx-detail .big{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.zx-detail .big b{font-family:var(--serif);font-size:56px;color:var(--navy);line-height:1;font-variant-numeric:tabular-nums}
.zx-detail .verdict{font-size:15px;color:var(--ink);max-width:48ch}
.zx-gauge{margin:14px 0 6px}
.zx-gauge svg{width:100%;height:auto;display:block}
.zx-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-top:14px}
.zx-facts div{background:var(--cream);border:1px solid var(--line);border-radius:2px;padding:10px 12px}
.zx-facts b{display:block;font-family:var(--serif);font-size:22px;color:var(--navy);font-variant-numeric:tabular-nums}
.zx-facts span{font-size:11.5px;color:var(--muted)}
#zxFinger svg{width:100%;height:auto;display:block}
.zx-table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
.zx-table th,.zx-table td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
.zx-table th:first-child,.zx-table td:first-child,.zx-table th:nth-child(2),.zx-table td:nth-child(2){text-align:left;white-space:normal}
.zx-table th{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:400;cursor:pointer;user-select:none}
.zx-table th.on{color:var(--navy)}
.zx-table tr{cursor:pointer}
.zx-table tr:hover td{background:var(--cream)}
.zx-table tr.sel td{background:#e6f1f1}
.zx-bar{display:inline-block;height:8px;background:var(--teal);border-radius:1px;vertical-align:middle;margin-right:6px}
.zx-wrap{overflow-x:auto}
.zx-more{text-align:center;margin-top:12px}
"""

BODY = r"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow"><a href="../data.html">Data &amp; visuals</a> / Explorer</div>
  <h1>District urban hierarchy explorer</h1>
  <p>For 415 Indian districts, how top-heavy is the system of towns? The Zipf exponent <em>b</em> is 1 when town sizes follow Zipf's law, higher when one town dominates, lower when towns are of similar size. Search a district, or browse by state.</p>
</div></div></section>
<section class="block"><div class="wrap">
  <div class="kpis" id="zxKpis"></div>
  <div class="ctrls">
    <div class="ctrl" style="flex:1;min-width:240px"><label for="zxQ">Find a district</label><div class="zx-search"><input id="zxQ" type="search" placeholder="Type a district name, e.g. Malappuram" autocomplete="off"><div class="zx-sugg" id="zxSugg"></div></div></div>
    <div class="ctrl"><label for="zxState">State</label><select id="zxState"><option value="">All states</option></select></div>
    <div class="ctrl"><label for="zxMinN">Minimum towns</label><select id="zxMinN"><option value="6">6 or more</option><option value="10">10 or more</option><option value="20">20 or more</option></select></div>
  </div>
  <div class="zx-top">
    <div class="panel"><h3>Map of b by district</h3><div class="sub">Teal: towns of similar size (b below 1). Orange to brown: one dominant town (b above 1). Grey: fewer than six towns in 2011, or no estimate. Click a district.</div><div id="zxMap"></div>
      <div class="zx-legend" id="zxLegend"></div></div>
    <div>
      <div class="panel zx-detail" id="zxDetail"><p class="muted">Pick a district to see its hierarchy, how it compares, and its fitted rank–size line.</p></div>
      <div class="panel" style="margin-top:22px"><h3 id="zxFTitle">Rank–size fingerprint</h3><div class="sub" id="zxFSub">Fitted line; largest town = 100; log scales</div><div id="zxFinger"></div></div>
    </div>
  </div>
  <div class="panel" style="margin-top:22px"><h3 id="zxTTitle">All districts</h3><div class="sub">Click a column to sort; click a row to select.</div>
    <div class="zx-wrap"><table class="zx-table"><thead><tr><th data-k="d">District</th><th data-k="s">State</th><th data-k="b" class="on">b</th><th data-k="n">Towns</th><th data-k="pop">Urban pop. 2011</th><th data-k="r2">R²</th></tr></thead><tbody id="zxBody"></tbody></table></div>
    <div class="zx-more"><button type="button" class="btn" id="zxMore">Show more</button></div>
  </div>
  <p class="dnote">Map boundaries are Census-2011-based district boundaries with later changes; a district created after 2011 is coloured by the 2011 district it was carved from. Towns and populations from the SHRUG database (Development Data Lab), harmonised to Census 2011. <em>b</em> is estimated by least squares on log population against log rank for districts with at least six towns; districts with fewer towns, including most single-city districts, are not included. Estimates with R² below 0.8 should be read with care. Analysis by Ankita Dey and Nikhil Mishra, CEL Lab. See the post <a href="../blog/one-big-town-or-many-small-ones.html">One big town, or many small ones?</a></p>
</div></section>
<script>
(function(){
var D=null,M=null,view=[],sortK='b',sortDir=-1,sel=null,shown=40;
var RAMP=[[0.4,'#0e7c7b'],[0.7,'#5fb3b0'],[0.9,'#b9ddd9'],[1.0,'#f1ede4'],[1.1,'#f3d7a6'],[1.4,'#e8a020'],[1.8,'#c4661c'],[2.3,'#8a3f12']];
function hex(c){return [parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)];}
function col(b){if(b==null)return null;if(b<=RAMP[0][0])return RAMP[0][1];for(var i=1;i<RAMP.length;i++){if(b<=RAMP[i][0]){var a=hex(RAMP[i-1][1]),c=hex(RAMP[i][1]),t=(b-RAMP[i-1][0])/(RAMP[i][0]-RAMP[i-1][0]);return 'rgb('+Math.round(a[0]+(c[0]-a[0])*t)+','+Math.round(a[1]+(c[1]-a[1])*t)+','+Math.round(a[2]+(c[2]-a[2])*t)+')';}}return RAMP[RAMP.length-1][1];}
function drawMap(){if(!M)return;var s='<svg viewBox="0 0 '+M.w+' '+M.h+'" role="img" aria-label="Map of India, districts coloured by Zipf exponent">';
  M.districts.forEach(function(dd,i){var c=col(dd.b);var isSel=sel&&dd.z===sel.d&&dd.zs===sel.s;s+='<path data-i="'+i+'" class="'+(c?'':'nd')+(isSel?' sel':'')+'" d="'+dd.d+'"'+(c?' fill="'+c+'"':'')+'><title>'+dd.n+', '+dd.st+(dd.b!=null?' · b = '+dd.b.toFixed(2)+(dd.z!==dd.n?' (2011 district: '+dd.z+')':''):' · no estimate')+'</title></path>';});
  if(M.states)s+='<path class="stl" d="'+M.states+'"/>';
  s+='</svg>';var el=$('zxMap');el.innerHTML=s;
  el.querySelectorAll('path').forEach(function(p){p.addEventListener('click',function(){var dd=M.districts[+p.dataset.i];if(dd.z){var x=D.find(function(y){return y.d===dd.z&&y.s===dd.zs;});if(x)select(x);}});});
  $('zxLegend').innerHTML='<span>b</span><span class="ramp">'+RAMP.map(function(r){return '<i style="background:'+r[1]+'" title="'+r[0]+'"></i>';}).join('')+'</span><span>'+RAMP[0][0]+' → '+RAMP[RAMP.length-1][0]+'+</span><span><i style="display:inline-block;width:12px;height:12px;background:#e9e4da;vertical-align:middle"></i> no estimate</span>';}
var $=function(id){return document.getElementById(id);};
function fmtPop(v){return v.toLocaleString('en-IN');}
function verdict(b){if(b>=1.6)return 'Strongly top-heavy: one town dominates and the rest fall away quickly.';if(b>=1.2)return 'Top-heavy: the largest town is well ahead of the others.';if(b>=0.9)return 'Close to Zipf\'s law: sizes fall roughly in proportion to rank.';if(b>=0.7)return 'Fairly even: towns of broadly similar size, no clear capital.';return 'Very even: many towns of similar size and no dominant centre.';}
function pct(arr,v){var n=arr.filter(function(x){return x<v;}).length;return Math.round(100*n/arr.length);}
function gauge(b,allB,stB){var W=420,H=64,l=10,r=10;var lo=0.3,hi=2.8;function X(v){return l+(Math.min(Math.max(v,lo),hi)-lo)/(hi-lo)*(W-l-r);}
  var s='<svg viewBox="0 0 '+W+' '+H+'">';
  s+='<rect x="'+l+'" y="26" width="'+(W-l-r)+'" height="6" rx="3" fill="#e6e0d6"/>';
  allB.forEach(function(v){s+='<rect x="'+X(v).toFixed(1)+'" y="22" width="1.5" height="14" fill="#1a3a5c" opacity=".12"/>';});
  stB.forEach(function(v){s+='<rect x="'+X(v).toFixed(1)+'" y="20" width="2" height="18" fill="#0e7c7b" opacity=".6"/>';});
  s+='<line x1="'+X(1)+'" y1="14" x2="'+X(1)+'" y2="44" stroke="#d9901a" stroke-width="1.5"/><text x="'+X(1)+'" y="56" font-size="10" fill="#d9901a" text-anchor="middle" font-family="Outfit,sans-serif">Zipf (b = 1)</text>';
  s+='<circle cx="'+X(b).toFixed(1)+'" cy="29" r="8" fill="#1a3a5c" stroke="#fff" stroke-width="2"/>';
  s+='<text x="'+l+'" y="12" font-size="10" fill="#737b84" font-family="Outfit,sans-serif">even</text><text x="'+(W-r)+'" y="12" font-size="10" fill="#737b84" text-anchor="end" font-family="Outfit,sans-serif">top-heavy</text>';
  return s+'</svg>';}
function finger(x){var W=440,H=300,ox=44,oy=16,cw=W-ox-12,ch=H-oy-40;var N=x.n,b=x.b;
  function px(rk){return ox+(Math.log10(rk)/Math.log10(Math.max(N,10)))*(cw-10)+5;}function py(sz){return oy+((2-Math.log10(Math.max(sz,0.1)))/3)*(ch-10)+5;}
  var s='<svg viewBox="0 0 '+W+' '+H+'"><rect x="'+ox+'" y="'+oy+'" width="'+cw+'" height="'+ch+'" fill="#f7f4ee" stroke="#e6e0d6"/>';
  [100,10,1,0.1].forEach(function(v){s+='<line x1="'+ox+'" y1="'+py(v).toFixed(1)+'" x2="'+(ox+cw)+'" y2="'+py(v).toFixed(1)+'" stroke="#e6e0d6" stroke-dasharray="2 3"/><text x="'+(ox-6)+'" y="'+(py(v)+4).toFixed(1)+'" font-size="10" fill="#737b84" text-anchor="end" font-family="Outfit,sans-serif">'+v+'</text>';});
  [1,2,5,10,20,50,100].filter(function(r){return r<=N;}).forEach(function(r){s+='<text x="'+px(r).toFixed(1)+'" y="'+(oy+ch+16)+'" font-size="10" fill="#737b84" text-anchor="middle" font-family="Outfit,sans-serif">'+r+'</text>';});
  // zipf reference (b=1)
  var ref='';for(var r=1;r<=N;r++){ref+=(r===1?'M':' L')+px(r).toFixed(1)+' '+py(100/r).toFixed(1);}
  s+='<path d="'+ref+'" fill="none" stroke="#d9901a" stroke-width="1.5" stroke-dasharray="4 4"/>';
  var d='';for(var r2=1;r2<=N;r2++){d+=(r2===1?'M':' L')+px(r2).toFixed(1)+' '+py(100*Math.pow(r2,-b)).toFixed(1);}
  s+='<path d="'+d+'" fill="none" stroke="#0e7c7b" stroke-width="2.5"/>';
  for(var r3=1;r3<=Math.min(N,40);r3++){s+='<circle cx="'+px(r3).toFixed(1)+'" cy="'+py(100*Math.pow(r3,-b)).toFixed(1)+'" r="2.8" fill="#1a3a5c"/>';}
  s+='<text x="'+(ox+cw/2)+'" y="'+(H-4)+'" font-size="11" fill="#3d4752" text-anchor="middle" font-family="Outfit,sans-serif">rank of town (log)</text>';
  s+='<text x="'+(ox+10)+'" y="'+(oy+ch-24)+'" font-size="10.5" fill="#0e7c7b" font-family="Outfit,sans-serif">— fitted, b = '+b.toFixed(2)+'</text><text x="'+(ox+10)+'" y="'+(oy+ch-10)+'" font-size="10.5" fill="#d9901a" font-family="Outfit,sans-serif">- - Zipf reference, b = 1</text>';
  return s+'</svg>';}
function select(x){sel=x;var allB=D.map(function(y){return y.b;});var st=D.filter(function(y){return y.s===x.s;});var stB=st.map(function(y){return y.b;});
  var rankNat=D.filter(function(y){return y.b>x.b;}).length+1,rankSt=st.filter(function(y){return y.b>x.b;}).length+1;
  var size2=(100*Math.pow(2,-x.b)).toFixed(0);
  $('zxDetail').innerHTML='<div class="eyebrow">'+x.s+'</div><h2 style="font-size:34px;margin:4px 0 10px">'+x.d+'</h2>'+
   '<div class="big"><b>'+x.b.toFixed(2)+'</b><div class="verdict">'+verdict(x.b)+'</div></div>'+
   '<div class="zx-gauge">'+gauge(x.b,allB,stB)+'</div>'+
   '<p class="muted" style="font-size:12.5px">Dot: this district. Teal ticks: other districts in '+x.s+'. Grey: all 415 districts.</p>'+
   '<div class="zx-facts"><div><b>'+x.n+'</b><span>towns in the fit</span></div><div><b>'+fmtPop(x.pop)+'</b><span>urban population, 2011</span></div><div><b>'+rankSt+' of '+st.length+'</b><span>most top-heavy in state</span></div><div><b>'+rankNat+' of '+D.length+'</b><span>most top-heavy in India</span></div><div><b>'+size2+'%</b><span>second town\'s size vs the largest, on the fitted line</span></div><div><b>'+x.r2.toFixed(2)+'</b><span>R² of the fit'+(x.r2<0.8?' (read with care)':'')+'</span></div></div>';
  $('zxFTitle').textContent='Rank–size fingerprint: '+x.d;$('zxFinger').innerHTML=finger(x);
  $('zxQ').value=x.d;renderTable();if(M){document.querySelectorAll('#zxMap path.sel').forEach(function(p){p.classList.remove('sel');});M.districts.forEach(function(dd,i){if(dd.z===x.d&&dd.zs===x.s){var p=document.querySelector('#zxMap path[data-i="'+i+'"]');if(p){p.classList.add('sel');p.parentNode.appendChild(p);}}});}if(window.innerWidth<900)$('zxDetail').scrollIntoView({behavior:'smooth',block:'start'});}
function applyFilter(){var st=$('zxState').value,mn=+$('zxMinN').value;view=D.filter(function(x){return (!st||x.s===st)&&x.n>=mn;});
  view.sort(function(a,b){var va=a[sortK],vb=b[sortK];if(typeof va==='string')return va.localeCompare(vb)*sortDir;return (va-vb)*sortDir;});shown=40;renderTable();
  $('zxTTitle').textContent=(st||'All districts')+' · '+view.length+' districts';}
function renderTable(){var maxB=2.8;var rows=view.slice(0,shown).map(function(x){return '<tr data-d="'+x.d+'|'+x.s+'"'+(sel&&sel.d===x.d&&sel.s===x.s?' class="sel"':'')+'><td>'+x.d+'</td><td>'+x.s+'</td><td><span class="zx-bar" style="width:'+Math.round(Math.min(x.b,maxB)/maxB*90)+'px"></span>'+x.b.toFixed(2)+'</td><td>'+x.n+'</td><td>'+fmtPop(x.pop)+'</td><td>'+x.r2.toFixed(2)+'</td></tr>';}).join('');
  $('zxBody').innerHTML=rows;$('zxMore').style.display=shown<view.length?'':'none';
  $('zxBody').querySelectorAll('tr').forEach(function(tr){tr.addEventListener('click',function(){var k=tr.dataset.d.split('|');var x=D.find(function(y){return y.d===k[0]&&y.s===k[1];});if(x)select(x);});});}
function kpis(){var bs=D.map(function(x){return x.b;}).sort(function(a,b){return a-b;});var med=bs[Math.floor(bs.length/2)];var near=D.filter(function(x){return x.b>=0.9&&x.b<=1.1;}).length;var states={};D.forEach(function(x){states[x.s]=1;});
  $('zxKpis').innerHTML=[[D.length,'districts'],[Object.keys(states).length,'states & UTs'],[med.toFixed(2),'median b'],[near,'districts within 0.1 of Zipf'],[bs[0].toFixed(2)+' – '+bs[bs.length-1].toFixed(2),'range of b']].map(function(k){return '<div class="kpi"><b>'+k[0]+'</b><span>'+k[1]+'</span></div>';}).join('');}
function init(){kpis();var st={};D.forEach(function(x){st[x.s]=1;});var sel_=$('zxState');Object.keys(st).sort().forEach(function(s){var o=document.createElement('option');o.value=s;o.textContent=s;sel_.appendChild(o);});
  sel_.addEventListener('change',applyFilter);$('zxMinN').addEventListener('change',applyFilter);$('zxMore').addEventListener('click',function(){shown+=40;renderTable();});
  document.querySelectorAll('.zx-table th').forEach(function(th){th.addEventListener('click',function(){var k=th.dataset.k;if(sortK===k)sortDir=-sortDir;else{sortK=k;sortDir=(k==='d'||k==='s')?1:-1;}document.querySelectorAll('.zx-table th').forEach(function(t){t.classList.toggle('on',t===th);});applyFilter();});});
  var q=$('zxQ'),sg=$('zxSugg'),cur=-1;
  q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();cur=-1;if(v.length<2){sg.style.display='none';return;}var m=D.filter(function(x){return x.d.toLowerCase().indexOf(v)===0||x.d.toLowerCase().indexOf(' '+v)>-1||x.s.toLowerCase().indexOf(v)===0;}).slice(0,10);
    sg.innerHTML=m.map(function(x){return '<div data-d="'+x.d+'|'+x.s+'">'+x.d+'<span>'+x.s+' · b '+x.b.toFixed(2)+'</span></div>';}).join('');sg.style.display=m.length?'block':'none';
    sg.querySelectorAll('div').forEach(function(el){el.addEventListener('mousedown',function(ev){ev.preventDefault();var k=el.dataset.d.split('|');var x=D.find(function(y){return y.d===k[0]&&y.s===k[1];});sg.style.display='none';if(x)select(x);});});});
  q.addEventListener('keydown',function(ev){var items=sg.querySelectorAll('div');if(!items.length)return;if(ev.key==='ArrowDown'){cur=Math.min(cur+1,items.length-1);}else if(ev.key==='ArrowUp'){cur=Math.max(cur-1,0);}else if(ev.key==='Enter'){ev.preventDefault();(items[cur>=0?cur:0]).dispatchEvent(new MouseEvent('mousedown'));return;}else if(ev.key==='Escape'){sg.style.display='none';return;}else return;ev.preventDefault();items.forEach(function(it,i){it.classList.toggle('on',i===cur);});});
  q.addEventListener('blur',function(){setTimeout(function(){sg.style.display='none';},150);});
  applyFilter();var h=decodeURIComponent((location.hash||'').slice(1));var start=D.find(function(x){return x.d.toLowerCase()===h.toLowerCase();})||D.find(function(x){return x.d==='Malappuram';});if(start)select(start);}
Promise.all([fetch('../assets/data/district-zipf.json').then(function(r){return r.json();}),fetch('../assets/data/india-districts.json').then(function(r){return r.json();}).catch(function(){return null;})]).then(function(a){D=a[0];M=a[1];drawMap();init();}).catch(function(){$('zxDetail').innerHTML='<p class="muted">The data could not be loaded.</p>';});
})();
</script>
"""
