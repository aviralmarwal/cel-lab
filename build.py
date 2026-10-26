#!/usr/bin/env python3
"""Builds the CEL Lab static site into ./docs (served by GitHub Pages) from data.py. Run: python3 build.py"""
import os, shutil, html, math, random, re, glob, datetime
import markdown
import dashboard_vlt, dashboard_zipf
from data import LAB, THEMES, PROJECTS, PEOPLE, PUBLICATIONS, ONGOING, EVENTS, OPPORTUNITIES, TALKS, CONFERENCES, NEWS, TEACHING, THESES, BLOG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
THEME_BY_SLUG = {t["slug"]: t for t in THEMES}
e = html.escape

# ───────────────────────── CSS ─────────────────────────
CSS = r"""
/* Layout: quiet academic site. Cream page, navy ink, teal accent, amber used sparingly. */
:root{
  --cream:#f7f4ee; --paper:#ffffff; --mist:#e6e0d6; --line:#d9d2c6;
  --ink:#16222e; --body:#3d4752; --muted:#737b84;
  --navy:#1a3a5c; --teal:#0e7c7b; --teal-dk:#0a6261; --amber:#d9901a;
  --lu-r:#a8c5da; --lu-c:#e8a020; --lu-g:#5a9e6f; --lu-w:#4a90c4; --lu-i:#9b8ea0; --lu-rd:#d4cfc8;
  --serif:'DM Serif Display',Georgia,'Times New Roman',serif;
  --sans:'Outfit',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'Space Mono','SFMono-Regular',Menlo,monospace;
  --wrap:1120px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--cream);color:var(--body);line-height:1.65;font-size:16px;overflow-x:hidden}
a{color:var(--teal);text-decoration:none}
a:hover{color:var(--teal-dk);text-decoration:underline}
a:focus-visible,button:focus-visible{outline:2px solid var(--amber);outline-offset:3px}
img,svg{max-width:100%;display:block}
h1,h2,h3,h4{font-family:var(--serif);font-weight:400;color:var(--ink);line-height:1.15;text-wrap:balance}
.wrap{max-width:var(--wrap);margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--teal)}
.eyebrow.amber{color:var(--amber)}
.lead{font-size:18px;color:var(--body);max-width:62ch}
.muted{color:var(--muted)}
.btn{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:13px 24px;border-radius:2px;border:1.5px solid var(--navy);color:var(--navy);transition:.2s}
.btn:hover{background:var(--navy);color:#fff;text-decoration:none}
.btn.primary{background:var(--teal);border-color:var(--teal);color:#fff}
.btn.primary:hover{background:var(--teal-dk);border-color:var(--teal-dk)}

/* nav */
.nav{position:sticky;top:0;z-index:50;background:rgba(247,244,238,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ink)}
.brand:hover{text-decoration:none}
.mono{font-family:var(--serif);font-size:30px;letter-spacing:-2px;line-height:1}
.mono .c{color:var(--teal)}.mono .e{color:var(--navy)}.mono .l{color:var(--amber)}
.brand-text{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);line-height:1.35}
.brand-text strong{display:block;color:var(--ink);font-size:11px}
.links{display:flex;gap:22px;list-style:none;white-space:nowrap}
.links a{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--body);padding:6px 0;border-bottom:2px solid transparent}
.links a:hover{color:var(--teal);text-decoration:none}
.links a.active{color:var(--navy);border-color:var(--amber)}
.menu-btn{display:none;background:none;border:1px solid var(--line);border-radius:2px;padding:8px 10px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);cursor:pointer}
@media(max-width:1000px){
  .links{display:none;position:absolute;left:0;right:0;top:68px;background:var(--cream);border-bottom:1px solid var(--line);flex-direction:column;gap:0;padding:8px 20px 16px}
  .links.open{display:flex}
  .links a{display:block;padding:12px 0;border-bottom:1px solid var(--line)}
  .links a.active{border-color:var(--amber)}
  .menu-btn{display:block}
}

/* hero */
.hero{padding-block:56px 48px;border-bottom:1px solid var(--line);background:var(--paper)}
.hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;align-items:center}
.hero h1{font-size:clamp(38px,5vw,60px);margin:14px 0 20px}
.hero h1 em{font-style:italic;color:var(--teal)}
.hero p{font-size:18px;max-width:58ch;margin-bottom:32px}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap}
.hero-art{aspect-ratio:1/1;max-width:420px;justify-self:end;width:100%}
@media(max-width:820px){.hero .wrap{grid-template-columns:1fr;gap:32px}.hero-art{max-width:300px;justify-self:start}.hero{padding-block:44px 40px}}

/* home: theme strip + two columns */
.strip{padding-block:28px 32px;border-bottom:1px solid var(--line)}
.strip-head{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:16px}
.strip-head .more{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
.tiles{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}
.tile{display:flex;flex-direction:column;gap:8px;color:var(--ink);font-size:13px;line-height:1.3}
.tile:hover{text-decoration:none;color:var(--teal)}
.tile .tthumb{aspect-ratio:3/2;border:1px solid var(--line);border-radius:3px;overflow:hidden;background:var(--paper)}
.tile .tthumb svg{width:100%;height:100%;display:block}
@media(max-width:1000px){.tiles{grid-template-columns:repeat(4,1fr)}}
@media(max-width:560px){.tiles{grid-template-columns:repeat(2,1fr)}}
.home-cols{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:48px;align-items:start}
@media(max-width:900px){.home-cols{grid-template-columns:1fr;gap:40px}}
.grid.data-cards{grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
.lead-post{display:block;background:var(--paper);border:1px solid var(--line);border-radius:3px;overflow:hidden;color:inherit}
.lead-post:hover{text-decoration:none}
.lead-post img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.lp-body{padding:20px 24px 24px;display:flex;flex-direction:column;gap:8px}
.lp-body h3{font-size:26px}
.lead-post:hover h3{color:var(--teal)}
.lp-body p{font-size:15px}
ul.mini{list-style:none;margin:14px 0 10px;display:grid;gap:0}
ul.mini li{padding:10px 0;border-bottom:1px solid var(--line);font-size:14.5px;line-height:1.45}
ul.mini li a{color:var(--ink);display:block}
ul.mini li a:hover{color:var(--teal);text-decoration:none}
ul.mini li span{display:block;font-size:12.5px;color:var(--muted);margin-top:2px}
.side-block{margin-bottom:34px}
.side-block h3{font-size:19px;padding-bottom:8px;border-bottom:2px solid var(--navy)}
.side-block .more{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}

/* page header (inner pages) */
.page-head{padding-block:56px 40px;border-bottom:1px solid var(--line);background:var(--paper)}
.page-head h1{font-size:clamp(34px,4.2vw,50px);margin:12px 0 16px}
.page-head p{max-width:62ch;font-size:17px}
.page-head .wrap{display:grid;grid-template-columns:1fr auto;gap:40px;align-items:end}
.page-head .thumb{width:260px;aspect-ratio:3/2}
@media(max-width:820px){.page-head .wrap{grid-template-columns:1fr}.page-head .thumb{width:100%;max-width:360px}}

section.block{padding-block:64px}
section.block.alt{background:var(--paper);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:32px;flex-wrap:wrap}
.sec-head h2{font-size:clamp(28px,3.2vw,38px)}
.sec-head a.more{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}

/* theme cards */
.grid{display:grid;gap:24px}
.grid.themes{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.card{background:var(--paper);border:1px solid var(--line);border-radius:3px;overflow:hidden;display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s;color:inherit}
a.card:hover{text-decoration:none;transform:translateY(-3px);box-shadow:0 10px 28px rgba(22,34,46,.09)}
.card .thumb{aspect-ratio:3/2;background:var(--cream);border-bottom:1px solid var(--line)}
.card .thumb svg{width:100%;height:100%}
.card-body{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{font-size:21px}
.card p{font-size:14.5px;color:var(--body)}
.card .cta{margin-top:auto;padding-top:10px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}

/* projects */
.proj-list{display:grid;gap:18px}
.proj{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--navy);border-radius:3px;padding:24px 26px;display:grid;grid-template-columns:1fr;gap:10px}
.proj .meta{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.tag{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding:4px 9px;border-radius:2px;background:var(--cream);border:1px solid var(--line);color:var(--navy)}
.tag.role{background:var(--navy);color:#fff;border-color:var(--navy)}
.proj h3{font-size:22px}
.proj p{font-size:15px;max-width:80ch}
.proj .themes a{font-size:13px}

/* projects: timeline + grouped grid */
.tl-wrap{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:22px 26px 18px;overflow-x:auto;margin-bottom:48px}
.tl-wrap svg{width:100%;min-width:640px;height:auto;display:block}
.tl-legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;font-size:12.5px;color:var(--muted)}
.tl-legend span{display:inline-flex;align-items:center;gap:6px}
.tl-legend i{width:12px;height:12px;border-radius:2px;display:inline-block}
.grid.projects{grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}
.pcard{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:22px 24px 20px;display:flex;flex-direction:column;gap:10px;border-top:4px solid var(--navy)}
.pcard .meta{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.pcard .meta b{color:var(--navy);font-weight:700}
.pcard h3{font-size:20px}
.pcard p{font-size:14.5px}
.pcard .themes{margin-top:auto;padding-top:8px;font-size:13px;border-top:1px solid var(--line)}
.pgroup{margin-bottom:44px}
.pgroup h2{font-size:26px;margin-bottom:6px}
.pgroup .sub{font-size:14px;color:var(--muted);margin-bottom:18px}

/* blog */
.featured{display:grid;grid-template-columns:1.25fr 1fr;gap:0;background:var(--paper);border:1px solid var(--line);border-radius:3px;overflow:hidden;margin-bottom:40px}
.featured .cov{aspect-ratio:16/9;background:var(--ink)}
.featured .cov img{width:100%;height:100%;object-fit:cover;display:block}
.featured .fb{padding:32px 36px;display:flex;flex-direction:column;gap:12px;justify-content:center;min-width:0}
.featured h2{font-size:32px}
.featured h2 a{color:var(--ink)}
.featured h2 a:hover{color:var(--teal);text-decoration:none}
.featured p{font-size:16px}
@media(max-width:820px){.featured{grid-template-columns:1fr}.featured .fb{padding:22px 24px}.featured h2{font-size:26px}}
.pmeta{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.pmeta .tagc{color:var(--amber)}
.grid.posts{grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}
.pcard2{background:var(--paper);border:1px solid var(--line);border-radius:3px;overflow:hidden;display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s}
.pcard2:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(22,34,46,.09)}
.pcard2 .cov{aspect-ratio:16/9;background:var(--ink)}
.pcard2 .cov img{width:100%;height:100%;object-fit:cover;display:block}
.pcard2 .pb{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px}
.pcard2 h3{font-size:21px}
.pcard2 h3 a{color:var(--ink)}
.pcard2 h3 a:hover{color:var(--teal);text-decoration:none}
.pcard2 p{font-size:14.5px}

/* post page */
.post-hero{background:var(--ink);color:#fff}
.post-hero .wrap{padding-block:56px 0;max-width:860px}
.post-hero .pmeta{color:rgba(255,255,255,.6)}
.post-hero h1{color:#fff;font-size:clamp(32px,4.4vw,52px);margin:14px 0 16px}
.post-hero .dek{font-size:19px;color:rgba(255,255,255,.75);max-width:62ch;line-height:1.55;margin-bottom:28px}
.post-hero .byline{display:flex;align-items:center;gap:12px;padding-bottom:36px}
.post-hero .byline img,.post-hero .byline .ini{width:40px;height:40px;border-radius:50%;object-fit:cover;background:var(--teal);display:flex;align-items:center;justify-content:center;font-family:var(--serif);color:#fff;font-size:16px}
.post-hero .byline b{display:block;font-weight:500;color:#fff;font-size:14px}
.post-hero .byline span{font-size:12.5px;color:rgba(255,255,255,.6)}
.post-cover{max-width:860px;margin:-1px auto 0;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.post-cover img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:0 0 3px 3px;box-shadow:0 14px 36px rgba(22,34,46,.18)}
.post-wrap{max-width:860px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.post{max-width:700px;margin:0 auto;padding-block:48px 0}
.post h2{font-size:28px;margin:44px 0 14px}
.post h3{font-size:22px;margin:30px 0 10px}
.post p,.post li{font-size:17.5px;line-height:1.75;margin-bottom:20px;color:var(--ink)}
.post>p:first-of-type::first-letter{font-family:var(--serif);font-size:64px;float:left;line-height:.85;padding:6px 10px 0 0;color:var(--navy)}
.post ul,.post ol{padding-left:22px;margin-bottom:20px}
.post li{margin-bottom:8px}
.post strong{font-weight:600;background:linear-gradient(transparent 62%,rgba(232,160,32,.35) 62%)}
.post blockquote{margin:36px 0;padding:6px 0 6px 26px;border-left:4px solid var(--amber)}
.post blockquote p{font-family:var(--serif);font-size:26px;line-height:1.35;color:var(--navy);margin:0}
.post img{width:100%;border-radius:3px;margin:8px 0 6px;border:1px solid var(--line)}
.post figure{margin:28px 0}
.post figcaption,.post img+em{display:block;font-size:13.5px;color:var(--muted);margin-bottom:22px}
.post code{font-family:var(--mono);font-size:14px;background:var(--mist);padding:1px 5px;border-radius:2px}
.post pre{background:var(--ink);color:#fff;padding:16px 18px;border-radius:3px;overflow-x:auto;margin-bottom:18px}
.post pre code{background:none;color:inherit}
.post hr{border:0;border-top:1px solid var(--line);margin:36px 0}
.post table{width:100%;max-width:480px;border-collapse:collapse;margin:8px 0 26px;font-size:15.5px;font-variant-numeric:tabular-nums}
.post th,.post td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line)}
.post th{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:400;border-bottom:2px solid var(--navy)}
.post td:last-child,.post th:last-child{text-align:right}
.post .verse{margin:22px 0 26px;padding:18px 22px;background:var(--paper);border:1px solid var(--line);border-radius:3px}
.post .verse .dev{font-family:'Noto Serif Devanagari','Noto Sans Devanagari',serif;font-size:19px;line-height:1.9;color:var(--navy)}
.post .verse .ref{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin:8px 0 6px}
.post .verse .tr{font-size:15.5px;line-height:1.6;color:var(--body);font-style:italic}
.post .note{font-size:14.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
.keybox{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--teal);border-radius:3px;padding:20px 24px 8px;margin:8px 0 36px}
.keybox .kh{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:10px}
.keybox ul{list-style:none;padding:0;margin:0}
.keybox li{font-size:15.5px;line-height:1.5;padding-left:18px;position:relative;margin-bottom:10px;color:var(--ink)}
.keybox li::before{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;background:var(--amber);border-radius:1px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin:8px 0 32px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:14px 16px}
.stat b{display:block;font-family:var(--serif);font-size:30px;color:var(--navy);line-height:1.1;font-variant-numeric:tabular-nums}
.stat span{font-size:12.5px;color:var(--muted)}
.author-box{display:grid;grid-template-columns:84px 1fr;gap:20px;align-items:start;background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:24px;margin-top:48px}
.author-box img,.author-box .ini{width:84px;height:84px;border-radius:50%;object-fit:cover;background:var(--navy);display:flex;align-items:center;justify-content:center;font-family:var(--serif);color:#fff;font-size:28px}
.author-box b{font-family:var(--serif);font-weight:400;font-size:20px;color:var(--ink);display:block;margin-bottom:4px}
.author-box p{font-size:14.5px;margin:0}
.share{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px;align-items:center;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.share a,.share button{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--line);background:var(--paper);color:var(--navy);padding:8px 12px;border-radius:2px;cursor:pointer}
.share a:hover,.share button:hover{border-color:var(--teal);color:var(--teal);text-decoration:none}
.more-posts{margin-top:56px}
.more-posts h3{font-size:22px;margin-bottom:16px}
.post-nav{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase}

DASHCSS_PLACEHOLDER
/* people */
.pi-card{background:var(--paper);border:1px solid var(--line);border-radius:3px;display:grid;grid-template-columns:220px 1fr;gap:0;overflow:hidden;margin-bottom:48px}
.avatar{background:var(--navy);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;aspect-ratio:1/1}
.avatar img{width:100%;height:100%;object-fit:cover;object-position:50% 15%}
.avatar .ini{font-family:var(--serif);font-size:56px;color:rgba(255,255,255,.9);letter-spacing:-2px;position:relative;z-index:1}
.avatar svg.bg{position:absolute;inset:0;width:100%;height:100%;opacity:.25}
.pi-body{padding:28px 32px;display:flex;flex-direction:column;gap:10px}
.pi-body h3{font-size:28px}
.pi-body .role{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}
.pi-body p{font-size:15px;max-width:70ch}
.pi-links{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;align-items:center;margin-top:6px}
@media(max-width:700px){.pi-card{grid-template-columns:1fr}.avatar{max-width:220px}}
.grid.people{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.person{background:var(--paper);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.person .avatar{aspect-ratio:4/3}
.person .avatar .ini{font-size:46px}
.person-body{padding:18px 20px 22px}
.person h3{font-size:20px;margin-bottom:4px}
.person .role{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}
.person p{font-size:14px;margin-top:8px}

/* publications */
.pub-group{margin-bottom:44px}
.pub-group h2{font-size:26px;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--navy)}
.pub{display:grid;grid-template-columns:64px 1fr;gap:18px;padding:18px 0;border-bottom:1px solid var(--line)}
.pub .year{font-family:var(--serif);font-size:24px;color:var(--navy);line-height:1.2;font-variant-numeric:tabular-nums}
.pub .title{font-family:var(--serif);font-size:18px;color:var(--ink);line-height:1.35}
.pub .title a{color:var(--ink)}
.pub .title a:hover{color:var(--teal)}
.pub .authors{font-size:14px;color:var(--body);margin-top:4px}
.pub .venue{font-size:13.5px;color:var(--amber);font-style:italic;margin-top:2px}
.pub .links{margin-top:6px;gap:14px}
.pub .links a{font-size:10.5px;border:none;padding:0}
@media(max-width:520px){.pub{grid-template-columns:1fr;gap:4px}}

/* theme page */
.theme-cols{display:grid;grid-template-columns:1.2fr .8fr;gap:56px;align-items:start}
.theme-cols .min{min-width:0}
.issues{list-style:none;display:grid;gap:12px;margin-top:16px}
.issues li{padding:14px 18px;background:var(--paper);border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:2px;font-size:15px}
.side h3{font-size:20px;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.side .pub{grid-template-columns:1fr;gap:2px;padding:12px 0}
.side .pub .title{font-size:16px}
.side ul{list-style:none;display:grid;gap:10px}
.side li a{font-size:15px}
.side .empty{font-size:14px;color:var(--muted)}
.side + .side{margin-top:36px}
@media(max-width:820px){.theme-cols{grid-template-columns:1fr;gap:40px}}

/* events */
.event{background:var(--paper);border:1px solid var(--line);border-radius:3px;display:grid;grid-template-columns:260px 1fr;gap:0;overflow:hidden;margin-bottom:24px}
.event .poster{background:var(--mist);border-right:1px solid var(--line)}
.event .poster img{width:100%;height:100%;object-fit:cover}
.event-body{padding:26px 30px;display:flex;flex-direction:column;gap:10px;min-width:0}
.event-body h3{font-size:24px}
.event .when{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber)}
.event p{font-size:15px;max-width:70ch}
.speakers{display:grid;gap:6px;margin-top:4px}
.speakers div{font-size:14.5px}
.speakers strong{color:var(--ink);font-weight:500}
.event .fine{font-size:13px;color:var(--muted)}
.event .fine a{font-size:13px}
@media(max-width:700px){.event{grid-template-columns:1fr}.event .poster{max-height:360px;border-right:none;border-bottom:1px solid var(--line)}.event .poster img{object-position:top}}
.news-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.news{border-top:2px solid var(--navy);padding-top:14px}
.news .kind{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber)}
.news h3{font-size:19px;margin:6px 0}
.news p{font-size:14px}

/* timeline + talks */
.timeline{list-style:none;display:grid;gap:0;border-left:2px solid var(--line);margin-left:6px}
.timeline li{position:relative;padding:0 0 22px 26px;font-size:15px}
.timeline li::before{content:"";position:absolute;left:-7px;top:7px;width:12px;height:12px;border-radius:50%;background:var(--amber);border:2px solid var(--cream)}
.timeline .d{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:2px}
.talk{display:grid;grid-template-columns:110px 1fr;gap:18px;padding:16px 0;border-bottom:1px solid var(--line)}
.talk .d{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);padding-top:4px}
.talk .t{font-family:var(--serif);font-size:18px;color:var(--ink);line-height:1.35}
.talk .v{font-size:14px;color:var(--body);margin-top:3px}
.talk .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:4px}
.past .talk{grid-template-columns:200px 1fr}
@media(max-width:520px){.talk,.past .talk{grid-template-columns:1fr;gap:4px}}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
@media(max-width:820px){.two-col{grid-template-columns:1fr}}
.subhead{font-size:26px;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid var(--navy)}

/* teaching */
.course{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:22px 26px;display:grid;grid-template-columns:120px 1fr;gap:20px}
.course .code{font-family:var(--mono);font-size:12px;letter-spacing:.1em;color:var(--navy);padding-top:6px}
.course .code small{display:block;font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:.12em;text-transform:uppercase}
.course h3{font-size:22px;margin-bottom:6px}
.course p{font-size:15px}
@media(max-width:520px){.course{grid-template-columns:1fr;gap:8px}}

/* ongoing (home) */
.grid.wips{grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}
.wip{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:22px 24px;display:flex;flex-direction:column;gap:8px}
.wip h3{font-size:21px}
.wip .om{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.wip p{font-size:14.5px}
.wip .cta{margin-top:auto;padding-top:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}

/* ongoing */
.ongoing{display:grid;gap:12px;margin-top:16px}
.ongoing div{padding:14px 18px;background:var(--cream);border:1px dashed var(--line);border-radius:2px;font-size:15px}
.ongoing strong{display:block;color:var(--ink);font-weight:500;font-family:var(--serif);font-size:19px;margin-bottom:2px}
.ongoing .om{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:8px}

/* opportunities */
.openings{display:grid;gap:16px;margin-bottom:40px}
.opening{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--amber);border-radius:3px;padding:22px 26px}
.opening h3{font-size:21px;margin-bottom:6px}
.opening p{font-size:15px}

/* contact */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.c-item{display:grid;grid-template-columns:52px 1fr;gap:14px;margin-bottom:22px}
.c-item .ic{width:44px;height:44px;background:var(--navy);color:var(--amber);font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;display:flex;align-items:center;justify-content:center;border-radius:2px}
.c-item strong{display:block;font-size:13px;color:var(--ink);margin-bottom:2px}
.c-item span{font-size:14.5px}
.placeholder{color:var(--muted);font-style:italic}
.note{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:28px 30px}
.note h3{font-size:22px;margin-bottom:10px}
.note p{font-size:15px}
@media(max-width:820px){.contact-grid{grid-template-columns:1fr}}

/* contact form */
.cform{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:30px 32px}
.cform h3{font-size:22px;margin-bottom:6px}
.cform .hint{font-size:14px;color:var(--muted);margin-bottom:20px}
.fg{margin-bottom:16px}
.fg label{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.fg input,.fg select,.fg textarea{width:100%;padding:12px 13px;border:1.5px solid var(--line);border-radius:2px;background:var(--cream);font-family:var(--sans);font-size:15px;color:var(--ink);outline:none}
.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:var(--teal)}
.fg textarea{min-height:140px;resize:vertical}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:600px){.frow{grid-template-columns:1fr}}
.fmsg{font-size:14px;margin-top:12px}
.fmsg.ok{color:var(--teal)}.fmsg.err{color:#b5541c}
.hp{position:absolute;left:-9999px}

/* footer */
footer{background:var(--ink);color:rgba(255,255,255,.55);padding-block:36px;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
footer .mono{font-size:22px}
footer .mono .e{color:#fff}
footer a{color:rgba(255,255,255,.75)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}html{scroll-behavior:auto}}
"""

# ───────────────────────── SVG thumbnails ─────────────────────────
PAL = {"r": "#a8c5da", "c": "#e8a020", "g": "#5a9e6f", "w": "#4a90c4", "i": "#9b8ea0", "rd": "#d4cfc8",
       "navy": "#1a3a5c", "teal": "#0e7c7b", "amber": "#d9901a", "mist": "#e6e0d6", "cream": "#f7f4ee"}

def svg_wrap(body, w=300, h=200, bg=PAL["cream"]):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-hidden="true">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')

def thumb_growth():
    rnd = random.Random(1); b = []
    cx, cy = 150, 100
    for gx in range(0, 300, 15):
        for gy in range(0, 200, 15):
            d = math.hypot(gx + 7 - cx, gy + 7 - cy)
            p = max(0, 1 - d / 150) + rnd.uniform(-.18, .18)
            if p > .62: col = PAL["navy"]; op = .95
            elif p > .42: col = PAL["teal"]; op = .75
            elif p > .28: col = PAL["r"]; op = .9
            else: continue
            b.append(f'<rect x="{gx+1}" y="{gy+1}" width="13" height="13" fill="{col}" opacity="{op}"/>')
    for r in (55, 95, 135):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PAL["amber"]}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    return svg_wrap("".join(b))

def thumb_access():
    b = []
    for x in range(0, 300, 30): b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="200" stroke="{PAL["mist"]}" stroke-width="1.5"/>')
    for y in range(0, 200, 30): b.append(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="{PAL["mist"]}" stroke-width="1.5"/>')
    fac = [(75, 70, PAL["teal"]), (200, 55, PAL["amber"]), (150, 140, PAL["navy"]), (245, 150, PAL["teal"])]
    for x, y, c in fac:
        for r, op in ((70, .10), (46, .16), (24, .26)):
            b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}"/>')
    rnd = random.Random(3)
    for _ in range(70):
        x, y = rnd.randint(8, 292), rnd.randint(8, 192)
        near = min(math.hypot(x - fx, y - fy) for fx, fy, _ in fac)
        col = PAL["navy"] if near < 60 else PAL["i"]
        b.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{col}" opacity=".8"/>')
    for x, y, c in fac:
        b.append(f'<rect x="{x-7}" y="{y-7}" width="14" height="14" fill="{c}" stroke="#fff" stroke-width="2"/>')
    return svg_wrap("".join(b))

def thumb_commute():
    b = []
    blocks = [(20, 30, PAL["r"]), (20, 120, PAL["r"]), (120, 20, PAL["i"]), (250, 40, PAL["c"]), (235, 130, PAL["c"]), (120, 140, PAL["g"])]
    for x, y, c in blocks:
        for i in range(3):
            for j in range(2):
                b.append(f'<rect x="{x+i*14}" y="{y+j*14}" width="11" height="11" fill="{c}" opacity=".85"/>')
    hub = (160, 95)
    for x, y, c in blocks:
        sx, sy = x + 20, y + 14
        mx, my = (sx + hub[0]) / 2, (sy + hub[1]) / 2 - 25
        b.append(f'<path d="M{sx} {sy} Q{mx} {my} {hub[0]} {hub[1]}" fill="none" stroke="{PAL["navy"]}" stroke-width="2.2" opacity=".55"/>')
        b.append(f'<circle cx="{sx}" cy="{sy}" r="3.5" fill="{PAL["navy"]}"/>')
    b.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="11" fill="{PAL["teal"]}" stroke="#fff" stroke-width="3"/>')
    return svg_wrap("".join(b))

def thumb_housing():
    b = []; rnd = random.Random(7)
    cols = 12; w = 300 / cols
    for i in range(cols):
        x = i * w
        hgt = 40 + rnd.randint(0, 80)
        price = i / (cols - 1)
        col = PAL["teal"] if price < .35 else (PAL["amber"] if price < .7 else PAL["navy"])
        b.append(f'<rect x="{x+3}" y="{170-hgt}" width="{w-6}" height="{hgt}" fill="{col}" opacity=".8"/>')
        b.append(f'<path d="M{x+1} {170-hgt} L{x+w/2} {170-hgt-12} L{x+w-1} {170-hgt} Z" fill="{col}"/>')
        for wy in range(int(170 - hgt + 8), 165, 12):
            b.append(f'<rect x="{x+w/2-2}" y="{wy}" width="4" height="5" fill="#fff" opacity=".8"/>')
    b.append(f'<line x1="0" y1="172" x2="300" y2="172" stroke="{PAL["navy"]}" stroke-width="2"/>')
    b.append(f'<path d="M20 190 L280 190" stroke="{PAL["amber"]}" stroke-width="3" stroke-dasharray="2 6" opacity=".9"/>')
    return svg_wrap("".join(b))

def thumb_agglom():
    b = []; rnd = random.Random(11)
    centers = [(90, 90, 46, PAL["navy"]), (215, 70, 30, PAL["teal"]), (200, 150, 22, PAL["amber"])]
    for cx, cy, R, col in centers:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{R+18}" fill="{col}" opacity=".10"/>')
        for _ in range(int(R * 1.3)):
            a = rnd.uniform(0, 6.283); r = R * math.sqrt(rnd.random())
            s = rnd.uniform(1.8, 4.2)
            b.append(f'<circle cx="{cx+r*math.cos(a):.1f}" cy="{cy+r*math.sin(a):.1f}" r="{s:.1f}" fill="{col}" opacity=".85"/>')
    for _ in range(25):
        b.append(f'<circle cx="{rnd.randint(5,295)}" cy="{rnd.randint(5,195)}" r="1.8" fill="{PAL["i"]}" opacity=".6"/>')
    b.append(f'<path d="M90 90 L215 70 L200 150 Z" fill="none" stroke="{PAL["navy"]}" stroke-width="1.2" stroke-dasharray="3 4" opacity=".6"/>')
    return svg_wrap("".join(b))

def thumb_landuse():
    rnd = random.Random(5); b = []
    pattern = "r r r g g w w c c r r i i r r g g c c r".split()
    cell = 15
    for gy in range(0, 200, cell):
        for gx in range(0, 300, cell):
            k = pattern[(gx // cell + (gy // cell) * 3) % len(pattern)]
            if rnd.random() < .12: k = "rd"
            b.append(f'<rect x="{gx+1}" y="{gy+1}" width="{cell-2}" height="{cell-2}" fill="{PAL[k]}" opacity=".9"/>')
    b.append(f'<rect x="90" y="55" width="120" height="90" fill="none" stroke="{PAL["navy"]}" stroke-width="2.5"/>')
    b.append(f'<rect x="90" y="55" width="120" height="90" fill="{PAL["navy"]}" opacity=".08"/>')
    return svg_wrap("".join(b))

def thumb_finance():
    rnd = random.Random(9); b = []
    b.append(f'<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{PAL["amber"]}" stroke-width="2"/></pattern></defs>')
    for gy in range(10, 190, 36):
        x = 10
        while x < 290:
            w = rnd.choice([28, 40, 52, 64])
            if x + w > 290: w = 290 - x
            st = rnd.random()
            if st < .55: fill = PAL["r"]
            elif st < .8: fill = "url(#hatch)"
            else: fill = PAL["mist"]
            b.append(f'<rect x="{x}" y="{gy}" width="{w}" height="30" fill="{fill}" stroke="{PAL["navy"]}" stroke-width="1"/>')
            x += w + 4
    b.append(f'<rect x="10" y="10" width="280" height="180" fill="none" stroke="{PAL["navy"]}" stroke-width="2"/>')
    return svg_wrap("".join(b))

THUMBS = {
    "urban-growth-simulation": thumb_growth,
    "facility-mapping-accessibility": thumb_access,
    "commuting-built-environment-typologies": thumb_commute,
    "housing-affordability-segregation": thumb_housing,
    "industrial-agglomeration-growth": thumb_agglom,
    "land-use-optimisation": thumb_landuse,
    "municipal-finance-property-tax": thumb_finance,
}

def hero_art():
    # network of city nodes over faint grid
    b = []
    for x in range(0, 320, 20): b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="320" stroke="{PAL["mist"]}" stroke-width="1"/>')
    for y in range(0, 320, 20): b.append(f'<line x1="0" y1="{y}" x2="320" y2="{y}" stroke="{PAL["mist"]}" stroke-width="1"/>')
    nodes = [(160, 50, 14, PAL["amber"]), (70, 130, 11, PAL["navy"]), (260, 120, 11, PAL["navy"]), (160, 170, 18, PAL["teal"]),
             (110, 260, 10, PAL["navy"]), (230, 255, 10, PAL["navy"]), (40, 230, 7, PAL["i"]), (290, 215, 7, PAL["i"])]
    edges = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 4), (3, 5), (1, 4), (2, 5), (4, 6), (5, 7), (1, 6), (2, 7)]
    for i, j in edges:
        a, c = nodes[i], nodes[j]
        b.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="{PAL["navy"]}" stroke-width="1.6" opacity=".45"/>')
    for x, y, r, col in nodes:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="{col}" opacity=".12"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
    return svg_wrap("".join(b), 320, 320, "none").replace('<rect width="320" height="320" fill="none"/>', "")

def avatar_bg(seed):
    rnd = random.Random(seed); b = []
    keys = ["r", "c", "g", "w", "i", "rd"]
    for gy in range(0, 120, 12):
        for gx in range(0, 120, 12):
            b.append(f'<rect x="{gx}" y="{gy}" width="11" height="11" fill="{PAL[rnd.choice(keys)]}"/>')
    return f'<svg class="bg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{"".join(b)}</svg>'

# ───────────────────────── Templates ─────────────────────────
NAV = [("index.html", "Home"), ("research.html", "Research"), ("projects.html", "Projects"),
       ("people.html", "People"), ("publications.html", "Publications"), ("events.html", "News"),
       ("teaching.html", "Teaching"), ("blog.html", "Blog"), ("data.html", "Data"), ("opportunities.html", "Join us"), ("contact.html", "Contact")]

def page(title, body, active, depth=0, desc=None, image=None):
    root = "../" * depth
    desc = desc or LAB["description"][:155]
    links = "".join(f'<li><a href="{root}{href}"{" class=\"active\"" if href == active else ""}>{lab}</a></li>' for href, lab in NAV)
    brand = (f'<a class="brand" href="{root}index.html"><span class="mono"><span class="c">C</span><span class="e">E</span><span class="l">L</span></span>'
             f'<span class="brand-text"><strong>{LAB["short"]}</strong>{LAB["inst"]}</span></a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {LAB["short"]}, {LAB["inst"]}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)} · {LAB["short"]}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
{f'<meta property="og:image" content="https://{LAB["domain"]}/{image}">' if image else ""}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@300;400;500;600&family=Space+Mono:wght@400;700&family=Noto+Serif+Devanagari:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<header class="nav"><div class="wrap">
  {brand}
  <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="navLinks">Menu</button>
  <ul class="links" id="navLinks">{links}</ul>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <div><span class="mono"><span class="c">C</span><span class="e">E</span><span class="l">L</span></span></div>
  <div>{LAB["name"]} · {LAB["inst"]}</div>
  <div>© {LAB["year"]} {LAB["short"]}</div>
</div></footer>
<script>
(function(){{var b=document.getElementById('menuBtn'),l=document.getElementById('navLinks');
b.addEventListener('click',function(){{var o=l.classList.toggle('open');b.setAttribute('aria-expanded',o);b.textContent=o?'Close':'Menu';}});}})();
</script>
</body>
</html>
"""

def theme_card(t, root=""):
    return (f'<a class="card" href="{root}research/{t["slug"]}.html"><div class="thumb">{THUMBS[t["slug"]]()}</div>'
            f'<div class="card-body"><h3>{e(t["title"])}</h3><p>{e(t["short"])}</p><span class="cta">Read more →</span></div></a>')

def pub_html(p, root="", compact=False):
    title = f'<a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])}</a>' if p["url"] else e(p["title"])
    yr = "" if compact else f'<div class="year">{p["year"]}</div>'
    auth = f'{e(p["authors"])} ({p["year"]})' if compact else e(p["authors"])
    return (f'<div class="pub">{yr}<div><div class="title">{title}</div><div class="authors">{auth}</div>'
            f'<div class="venue">{e(p["venue"])}</div></div></div>')

def project_html(pr, root=""):
    th = ", ".join(f'<a href="{root}research/{s}.html">{e(THEME_BY_SLUG[s]["title"])}</a>' for s in pr["themes"])
    tags = (f'<span class="tag role">{e(pr["role"])}</span>' if pr.get("role") else "") + \
           (f'<span class="tag">{e(pr["years"])}</span>' if pr.get("years") else "") + \
           (f'<span class="tag">Funded by {e(pr["funder"])}</span>' if pr.get("funder") else "") + \
           (f'<span class="tag">Partner: {e(pr["partner"])}</span>' if pr.get("partner") else "")
    role = f'<div class="meta">{tags}</div>' if tags else ""
    return (f'<article class="proj">{role}'
            f'<h3>{e(pr["title"])}</h3><p>{e(pr["summary"])}</p><div class="themes muted">Theme: {th}</div></article>')

ALL_PUBS = [p for g in PUBLICATIONS for p in g["items"]]
EVENTS_SORTED = sorted(EVENTS, key=lambda ev: ev["date"], reverse=True)

def event_html(ev, root=""):
    poster = f'<div class="poster"><img src="{root}{ev["poster"]}" alt="Poster: {e(ev["title"])}" loading="lazy"></div>' if ev.get("poster") else ""
    speakers = "".join(f'<div><strong>{e(s["name"])}</strong> — {e(s["aff"])}</div>' for s in ev.get("speakers", []))
    fine = " · ".join(x for x in [f'Convener: {e(ev["convener"])}' if ev.get("convener") else "", e(ev.get("support", ""))] if x)
    return (f'<article class="event">{poster}<div class="event-body">'
            f'<div class="when">{e(ev["kind"])} · {e(ev["date_text"])}</div><h3>{e(ev["title"])}</h3>'
            f'<p>{e(ev["summary"])}</p><div class="speakers">{speakers}</div>'
            f'<p class="fine">{e(ev["venue"])}</p><p class="fine">{fine}</p></div></article>')

# ───────────────────────── Pages ─────────────────────────
def build_index():
    posts = load_posts()
    # compact theme strip
    tiles = "".join(f'<a class="tile" href="research/{t["slug"]}.html"><div class="tthumb">{THUMBS[t["slug"]]()}</div><span>{e(t["title"])}</span></a>' for t in THEMES)
    # latest writing (left column)
    if posts:
        f = posts[0]
        lead = (f'<a class="lead-post" href="blog/{f["slug"]}.html">' + (f'<img src="{f["image"]}" alt="">' if f["image"] else "") +
                f'<div class="lp-body"><div class="pmeta"><span class="tagc">{e(BLOG["label"])}</span><span>{e(nice_date(f["date"]))}</span><span>{f["minutes"]} min read</span></div>'
                f'<h3>{e(f["title"])}</h3><p>{e(f["summary"])}</p></div></a>')
        others = "".join(f'<li><a href="blog/{p["slug"]}.html">{e(p["title"])}</a><span>{e(nice_date(p["date"]))}</span></li>' for p in posts[1:4])
        writing = lead + (f'<ul class="mini">{others}</ul>' if others else "")
    else:
        writing = '<p class="muted">No posts yet.</p>'
    # right column: activity lists
    data_items = "".join(f'<a class="card" href="{d["href"]}"><div class="thumb" style="aspect-ratio:16/9;background:var(--paper)"><img src="{d["thumb"]}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:top"></div>'
                         f'<div class="card-body"><div class="eyebrow amber">{e(d["kind"])}</div><h3 style="font-size:19px">{e(d["title"])}</h3><p>{e(d["desc"])}</p><span class="cta">Open →</span></div></a>' for d in DATA_ITEMS if d["kind"] != "Data story")
    wip = "".join(f'<li><a href="research/{o["theme"]}.html">{e(o["title"])}</a><span>{e(o.get("authors",""))}</span></li>' for o in ONGOING[:4])
    proj = "".join(f'<li><a href="projects.html">{e(p["title"])}</a><span>{e(p.get("role",""))}' + (f' · {e(p["funder"])}' if p.get("funder") else (f' · with {e(p["partner"])}' if p.get("partner") else "")) + '</span></li>' for p in [q for q in PROJECTS if q.get("status","ongoing")=="ongoing"][:3])
    news = "".join(f'<li><a href="{n["link"]}">{e(n["text"])}</a><span>{e(n["date_text"])}</span></li>' for n in sorted(NEWS, key=lambda n: n["date"], reverse=True)[:3])
    recent = "".join(f'<li><a href="{p["url"] or "publications.html"}"{" target=\"_blank\" rel=\"noopener\"" if p["url"] else ""}>{e(p["title"])}</a><span>{e(p["venue"])}, {p["year"]}</span></li>' for p in sorted(ALL_PUBS, key=lambda p: -p["year"])[:3])
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    <div class="eyebrow">{e(LAB["name"])}</div>
    <h1>Cities as places to <em>experiment</em> and <em>learn</em></h1>
    <p>{e(LAB["description"])}</p>
    <div class="hero-actions"><a class="btn primary" href="research.html">Research themes</a><a class="btn" href="people.html">Meet the team</a></div>
  </div>
  <div class="hero-art">{hero_art()}</div>
</div></section>

<section class="strip"><div class="wrap">
  <div class="strip-head"><span class="eyebrow">Seven research themes</span><a class="more" href="research.html">About our research →</a></div>
  <div class="tiles">{tiles}</div>
</div></section>

<section class="block"><div class="wrap home-cols">
  <div class="col-main">
    <div class="sec-head"><div><div class="eyebrow">Latest writing</div><h2>From the blog</h2></div><a class="more" href="blog.html">All posts →</a></div>
    {writing}
    <div class="sec-head" style="margin-top:44px"><div><div class="eyebrow">Data &amp; visuals</div><h2>Explore the data</h2></div><a class="more" href="data.html">All data &amp; visuals →</a></div>
    <div class="grid data-cards">{data_items}</div>
  </div>
  <aside class="col-side">
    <div class="side-block"><h3>Work in progress</h3><ul class="mini">{wip}</ul><a class="more" href="research.html#ongoing">All ongoing work →</a></div>
    <div class="side-block"><h3>Projects</h3><ul class="mini">{proj}</ul><a class="more" href="projects.html">Project details →</a></div>
    <div class="side-block"><h3>Recent publications</h3><ul class="mini">{recent}</ul><a class="more" href="publications.html">All publications →</a></div>
    <div class="side-block"><h3>News</h3><ul class="mini">{news}</ul><a class="more" href="events.html">News &amp; talks →</a></div>
  </aside>
</div></section>
"""
    return page("Home", body, "index.html")

def build_research():
    themes = "".join(theme_card(t) for t in THEMES)
    ongoing_sec = ""
    if ONGOING:
        items = "".join(ongoing_html(o).replace("</strong>", f'</strong><a class="muted" style="font-size:13px" href="research/{o["theme"]}.html">{e(THEME_BY_SLUG[o["theme"]]["title"])}</a>', 1) for o in ONGOING)
        ongoing_sec = (f'<section class="block alt" id="ongoing"><div class="wrap"><div class="sec-head"><div><div class="eyebrow">Ongoing research</div><h2>Work in progress</h2></div></div>'
                       f'<p class="muted" style="font-size:14.5px;margin:-16px 0 18px;max-width:70ch">Papers in preparation. Drafts are circulated once they are ready; write to us if you are working on related questions.</p>'
                       f'<div class="ongoing" style="margin-top:0">{items}</div></div></section>')
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Research</div><h1>Seven questions about Indian cities</h1>
  <p>Our work is organised around seven themes. Each page describes what the theme is about, the issues we tackle, and the projects and publications that sit under it.</p>
</div></div></section>
<section class="block"><div class="wrap"><div class="grid themes">{themes}</div></div></section>
{ongoing_sec}
"""
    return page("Research", body, "research.html")

def ongoing_html(o, root=""):
    meta = " · ".join(x for x in [e(o.get("authors", "")), e(o.get("status", ""))] if x)
    return f'<div><strong>{e(o["title"])}</strong><span class="om">{meta}</span>{e(o["note"])}</div>'

def build_theme(t):
    pubs = [p for p in ALL_PUBS if t["slug"] in p["themes"]]
    projs = [p for p in PROJECTS if t["slug"] in p["themes"]]
    issues = "".join(f"<li>{e(i)}</li>" for i in t["issues"])
    talks = [tk for tk in TALKS if t["slug"] in tk.get("themes", [])]
    talk_side = ('<div class="side"><h3>Talks</h3><ul>' + "".join(f'<li><a href="../events.html">{e(tk["title"])}</a> <span class="muted">({e(tk["venue"].split(",")[0])}, {e(tk["date_text"])})</span></li>' for tk in talks) + "</ul></div>") if talks else ""
    pub_block = "".join(pub_html(p, "../", compact=True) for p in pubs) or '<p class="empty">No publications under this theme yet.</p>'
    ongoing = [o for o in ONGOING if o["theme"] == t["slug"]]
    ongoing_block = ""
    if ongoing:
        ongoing_block = ('<h2 style="font-size:26px;margin-top:40px">Work in progress</h2><div class="ongoing">' +
                         "".join(ongoing_html(o) for o in ongoing) + "</div>")
    proj_block = ("<ul>" + "".join(f'<li><a href="../projects.html">{e(p["title"])}</a> <span class="muted">({e(p["role"])})</span></li>' for p in projs) + "</ul>") if projs else '<p class="empty">No active projects under this theme yet.</p>'
    body = f"""
<section class="page-head"><div class="wrap">
  <div><div class="eyebrow"><a href="../research.html">Research</a> / Theme</div><h1>{e(t["title"])}</h1><p>{e(t["short"])}</p></div>
  <div class="thumb">{THUMBS[t["slug"]]()}</div>
</div></section>
<section class="block"><div class="wrap theme-cols">
  <div class="min">
    <div class="eyebrow">About this theme</div>
    <p class="lead" style="margin-top:10px">{e(t["intro"])}</p>
    <h2 style="font-size:26px;margin-top:40px">Issues we tackle</h2>
    <ul class="issues">{issues}</ul>
    {ongoing_block}
  </div>
  <aside class="min">
    <div class="side"><h3>Related projects</h3>{proj_block}</div>
    <div class="side"><h3>Related publications</h3>{pub_block}</div>
    {talk_side}
    <div class="side"><h3>People</h3><ul><li><a href="../people.html">{e(PEOPLE["pi"]["name"])}</a> <span class="muted">(PI)</span></li></ul></div>
  </aside>
</div></section>
"""
    return page(t["title"], body, "research.html", depth=1, desc=t["short"])

THEME_COLORS = {"urban-growth-simulation": "#1a3a5c", "facility-mapping-accessibility": "#0e7c7b",
                "commuting-built-environment-typologies": "#4a90c4", "housing-affordability-segregation": "#d9901a",
                "industrial-agglomeration-growth": "#9b8ea0", "land-use-optimisation": "#5a9e6f",
                "municipal-finance-property-tax": "#b5541c"}

def ym(s):
    y, m = s.split("-"); return int(y) + (int(m) - 1) / 12

def project_timeline(projects):
    dated = [p for p in projects if p.get("start")]
    if not dated: return ""
    today = datetime.date.today(); now = today.year + (today.month - 1) / 12
    y0 = int(min(ym(p["start"]) for p in dated)); y1 = int(max([ym(p["end"]) if p.get("end") else now for p in dated])) + 1
    left, right, top, rowh = 300, 20, 34, 34
    W = 1100; H = top + rowh * len(dated) + 14
    def X(v): return left + (v - y0) / (y1 - y0) * (W - left - right)
    s = []
    for y in range(y0, y1 + 1):
        x = X(y)
        s.append(f'<line x1="{x:.1f}" y1="{top-10}" x2="{x:.1f}" y2="{H-10}" stroke="{PAL["mist"]}" stroke-width="1"/>')
        if y < y1: s.append(f'<text x="{X(y+.5):.1f}" y="18" text-anchor="middle" font-family="Space Mono,monospace" font-size="11" fill="{PAL["i"]}">{y}</text>')
    xn = X(now)
    s.append(f'<line x1="{xn:.1f}" y1="{top-10}" x2="{xn:.1f}" y2="{H-10}" stroke="{PAL["amber"]}" stroke-width="1.5" stroke-dasharray="3 3"/>')
    s.append(f'<text x="{xn+4:.1f}" y="{H-2}" font-family="Space Mono,monospace" font-size="9" fill="{PAL["amber"]}">TODAY</text>')
    for i, p in enumerate(sorted(dated, key=lambda p: p["start"])):
        y = top + i * rowh
        xs = X(ym(p["start"])); xe = X(ym(p["end"])) if p.get("end") else xn
        col = THEME_COLORS.get(p["themes"][0], PAL["navy"])
        title = p["title"]; short = title if len(title) <= 46 else title[:44].rsplit(" ", 1)[0] + "…"
        s.append(f'<text x="{left-12}" y="{y+16}" text-anchor="end" font-family="Outfit,sans-serif" font-size="13" fill="{PAL["navy"]}">{e(short)}</text>')
        s.append(f'<rect x="{xs:.1f}" y="{y+4}" width="{max(xe-xs,6):.1f}" height="18" rx="2" fill="{col}" opacity=".9"/>')
        if not p.get("end"):
            s.append(f'<rect x="{xe-6:.1f}" y="{y+4}" width="6" height="18" fill="{PAL["cream"]}" opacity=".55"/>')
        s.append(f'<text x="{xs+6:.1f}" y="{y+17}" font-family="Space Mono,monospace" font-size="9.5" fill="#fff">{e(p["role"])}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Project timeline">{"".join(s)}</svg>'
    used = []
    for p in dated:
        t = p["themes"][0]
        if t not in used: used.append(t)
    legend = "".join(f'<span><i style="background:{THEME_COLORS[t]}"></i>{e(THEME_BY_SLUG[t]["title"])}</span>' for t in used)
    return f'<div class="tl-wrap">{svg}<div class="tl-legend">{legend}<span><i style="background:transparent;border:1.5px dashed {PAL["amber"]}"></i>Today · faded end = ongoing</span></div></div>'

def pcard(p, root=""):
    yrs = p.get("years") or ((p["start"][:4] + " – " + (p["end"][:4] if p.get("end") else "present")) if p.get("start") else "")
    meta = " · ".join(x for x in [f'<b>{e(p["role"])}</b>' if p.get("role") else "", e(yrs), e(p.get("funder", "")), (f'with {e(p["partner"])}' if p.get("partner") else "")] if x)
    th = ", ".join(f'<a href="{root}research/{s}.html">{e(THEME_BY_SLUG[s]["title"])}</a>' for s in p["themes"])
    col = THEME_COLORS.get(p["themes"][0], PAL["navy"])
    return (f'<article class="pcard" style="border-top-color:{col}"><div class="meta">{meta}</div><h3>{e(p["title"])}</h3>'
            f'<p>{e(p["summary"])}</p><div class="themes muted">Theme: {th}</div></article>')

def build_projects():
    groups = [("ongoing", "Ongoing projects", "Funded research led or co-led by the lab."),
              ("collaboration", "Collaborations", "Joint work with partner institutions."),
              ("completed", "Completed projects", "")]
    blocks = ""
    for key, title, sub in groups:
        ps = [p for p in PROJECTS if p.get("status", "ongoing") == key]
        if not ps: continue
        blocks += (f'<div class="pgroup"><h2>{title}</h2>' + (f'<p class="sub">{sub}</p>' if sub else "") +
                   f'<div class="grid projects">{"".join(pcard(p) for p in ps)}</div></div>')
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Projects</div><h1>Funded and partnered research</h1>
  <p>Projects led or co-led by CEL Lab, working with state and city governments and partner institutions on evidence they can act on.</p>
</div></div></section>
<section class="block"><div class="wrap">{project_timeline(PROJECTS)}{blocks}</div></section>
"""
    return page("Projects", body, "projects.html")

def build_people():
    pi = PEOPLE["pi"]
    av = f'<img src="{pi["photo"]}" alt="{e(pi["name"])}">' if pi["photo"] else f'{avatar_bg(1)}<span class="ini">{pi["initials"]}</span>'
    links = "".join((f'<a class="btn" href="{l["url"]}" download>{e(l["label"])}</a>' if l["url"].lower().endswith(".pdf")
                     else f'<a href="{l["url"]}" target="_blank" rel="noopener">{e(l["label"])} ↗</a>') for l in pi["links"])
    scholars = ""
    for i, s in enumerate(PEOPLE["scholars"]):
        sav = f'<img src="{s["photo"]}" alt="{e(s["name"])}">' if s["photo"] else f'{avatar_bg(10+i)}<span class="ini">{s["initials"]}</span>'
        topic = f'<p>{e(s["topic"])}</p>' if s["topic"] else ""
        scholars += f'<div class="person"><div class="avatar">{sav}</div><div class="person-body"><h3>{e(s["name"])}</h3><div class="role">{e(s["role"])}</div>{topic}</div></div>'
    interns = ""
    for i, s in enumerate(PEOPLE.get("interns", [])):
        sav = f'<img src="{s["photo"]}" alt="{e(s["name"])}">' if s.get("photo") else f'{avatar_bg(20+i)}<span class="ini">{s["initials"]}</span>'
        topic = f'<p>{e(s["topic"])}</p>' if s.get("topic") else ""
        interns += f'<div class="person"><div class="avatar">{sav}</div><div class="person-body"><h3>{e(s["name"])}</h3><div class="role">{e(s["role"])}</div>{topic}</div></div>'
    intern_block = f'<div class="eyebrow" style="margin:48px 0 14px">Research Interns</div><div class="grid people">{interns}</div>' if interns else ""
    current_theses = [t for t in THESES if not t["title"]]
    past_theses = [t for t in THESES if t["title"]]
    ts = "".join(f'<div class="talk"><div class="d">{e(t["prog"])} · {e(t["year"])}</div><div><div class="t">{e(t["name"])}</div><div class="v">Thesis in progress</div></div></div>' for t in current_theses)
    thesis_block = f'<div class="eyebrow" style="margin:48px 0 6px">Thesis Students</div><div class="past">{ts}</div>' if ts else ""
    past = [{"name": a["name"], "d": a["role"], "v": a["affil"] + (f' · {a["topic"]}' if a.get("topic") else "")} for a in PEOPLE.get("alumni", [])]
    past += [{"name": t["name"], "d": f'Thesis student · {t["prog"]} · {t["year"]}', "v": t["title"]} for t in past_theses]
    alumni = "".join(f'<div class="talk"><div class="d">{e(a["d"])}</div><div><div class="t">{e(a["name"])}</div><div class="v">{e(a["v"])}</div></div></div>' for a in past)
    alumni_block = (f'<div class="eyebrow" style="margin:48px 0 6px">Past Team Members</div>'
                    f'<p class="muted" style="font-size:14px;margin-bottom:6px">Interns hosted under the SPARK and IKS (Indian Knowledge Systems) programmes at IIT Roorkee, and M.Sc. / BS-MS Economics thesis students supervised at the lab.</p><div class="past">{alumni}</div>') if alumni else ""
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">People</div><h1>The team</h1>
  <p>A small group of urban economists and spatial analysts at {LAB["inst"]}.</p>
</div></div></section>
<section class="block"><div class="wrap">
  <div class="eyebrow" style="margin-bottom:14px">Principal Investigator</div>
  <div class="pi-card"><div class="avatar">{av}</div><div class="pi-body">
    <h3>{e(pi["name"])}</h3><div class="role">{e(pi["role"])} · {e(pi["degree"])}</div>
    <p>{e(pi["bio"])}</p><div class="pi-links">{links}</div>
  </div></div>
  <div class="eyebrow" style="margin-bottom:14px">Research Scholars</div>
  <div class="grid people">{scholars}</div>
  {intern_block}
  {thesis_block}
  {alumni_block}
</div></section>
"""
    return page("People", body, "people.html")

def build_publications():
    groups = ""
    for g in PUBLICATIONS:
        items = "".join(pub_html(p) for p in sorted(g["items"], key=lambda p: -p["year"]))
        groups += f'<div class="pub-group"><h2>{e(g["type"])}</h2>{items}</div>'
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Publications</div><h1>Papers, working papers and cases</h1>
  <p>Research output from CEL Lab and its members. Titles link to the publisher's page where available.</p>
</div></div></section>
<section class="block"><div class="wrap">{groups}</div></section>
"""
    return page("Publications", body, "publications.html")

def build_contact():
    email = f'<span>{e(LAB["email"])}</span>' if LAB["email"] else '<span class="placeholder">Email address to be added</span>'
    endpoint = LAB.get("form_endpoint", "") if LAB.get("form_access_key") or "web3forms" not in LAB.get("form_endpoint", "") else ""
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Contact</div><h1>Get in touch</h1>
  <p>For research collaborations, PhD and internship enquiries, or requests from city and state governments.</p>
</div></div></section>
<section class="block"><div class="wrap contact-grid">
  <div>
    <div class="c-item"><div class="ic">MAIL</div><div><strong>Email</strong>{email}</div></div>
    <div class="c-item"><div class="ic">LOC</div><div><strong>Address</strong><span>{e(LAB["address"])}</span></div></div>
    <div class="c-item"><div class="ic">WEB</div><div><strong>Web</strong><span>{LAB["domain"]}</span></div></div>
  </div>
  <form class="cform" id="contactForm" method="POST" action="{endpoint}" novalidate>
    <h3>Send a message</h3>
    <p class="hint">We reply to most enquiries within a week.</p>
    <div class="frow">
      <div class="fg"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div class="fg"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="frow">
      <div class="fg"><label for="f-org">Organisation (optional)</label><input id="f-org" name="organisation" type="text" autocomplete="organization"></div>
      <div class="fg"><label for="f-type">Enquiry type</label>
        <select id="f-type" name="enquiry_type">
          <option>Research collaboration</option><option>PhD / internship enquiry</option><option>Government / municipal request</option><option>Media</option><option>Other</option>
        </select></div>
    </div>
    <div class="fg"><label for="f-msg">Your query</label><textarea id="f-msg" name="message" required></textarea></div>
    {('<input type="hidden" name="access_key" value="' + e(LAB["form_access_key"]) + '">') if LAB.get("form_access_key") else ""}
    <input type="hidden" name="subject" value="New enquiry via cel-lab.in contact form">
    <input type="hidden" name="from_name" value="CEL Lab website">
    <input type="hidden" name="redirect" id="f-redirect" value="">
    <input type="checkbox" class="hp" name="botcheck" tabindex="-1" autocomplete="off">
    <button class="btn primary" type="submit" id="f-send">Send message</button>
    <div class="fmsg" id="f-status" aria-live="polite"></div>
  </form>
</div></section>
<script>
(function(){{
  var f=document.getElementById('contactForm'),st=document.getElementById('f-status'),btn=document.getElementById('f-send');
  var endpoint={endpoint!r}, to={LAB["email"]!r};
  var here=location.href.split('?')[0].split('#')[0];
  document.getElementById('f-redirect').value=here+'?sent=1';
  if(location.search.indexOf('sent=1')>-1){{st.className='fmsg ok';st.textContent='Thank you — your message has been sent.';f.scrollIntoView();}}
  f.addEventListener('submit',function(ev){{
    if(f.dataset.native==='1'){{return;}}
    ev.preventDefault();
    if(!f.checkValidity()){{st.className='fmsg err';st.textContent='Please fill in your name, email and query.';return;}}
    var d=new FormData(f);
    if(!endpoint){{
      var NL=String.fromCharCode(10);
      var body='Name: '+d.get('name')+NL+'Email: '+d.get('email')+NL+'Organisation: '+(d.get('organisation')||'-')+NL+'Enquiry type: '+d.get('enquiry_type')+NL+NL+d.get('message');
      window.location.href='mailto:'+to+'?subject='+encodeURIComponent('[CEL Lab] '+d.get('enquiry_type')+' - '+d.get('name'))+'&body='+encodeURIComponent(body);
      st.className='fmsg ok';st.textContent='Your email app should open with the message filled in. If it does not, write to '+to+'.';return;
    }}
    btn.disabled=true;st.className='fmsg';st.textContent='Sending…';
    var obj={{}};d.forEach(function(v,k){{obj[k]=v;}});delete obj.redirect;
    fetch(endpoint,{{method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},body:JSON.stringify(obj)}}).then(function(r){{return r.json();}}).then(function(j){{
      if(j&&j.success){{f.reset();st.className='fmsg ok';st.textContent='Thank you — your message has been sent.';btn.disabled=false;}}
      else{{throw new Error(j&&j.message||'failed');}}
    }}).catch(function(){{ /* fall back to a normal form post; Web3Forms redirects back here */ btn.disabled=false; f.dataset.native='1'; HTMLFormElement.prototype.submit.call(f); }});
  }});
}})();
</script>
"""
    return page("Contact", body, "contact.html")

def talk_html(t, root=""):
    return (f'<div class="talk"><div class="d">{e(t["date_text"])}</div><div><div class="k">{e(t["kind"])}</div>'
            f'<div class="t">{e(t["title"])}</div><div class="v">{e(t["venue"])}</div></div></div>')

def load_posts():
    posts = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), BLOG["dir"], "*.md"))):
        if os.path.basename(f).lower() == "readme.md": continue
        txt = open(f, encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", txt, re.S)
        if not m: continue
        meta = {}; key = None
        for ln in m.group(1).splitlines():
            if re.match(r"^\s+-\s+", ln) and key:
                meta.setdefault(key + "_list", []).append(re.sub(r"^\s+-\s+", "", ln).strip())
            elif ":" in ln:
                key, v = ln.split(":", 1); key = key.strip(); meta[key] = v.strip()
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.splitext(os.path.basename(f))[0])
        body_md = m.group(2)
        words = len(re.findall(r"\w+", body_md))
        posts.append({"slug": slug, "title": meta.get("title", slug), "date": meta.get("date", ""), "author": meta.get("author", ""),
                      "summary": meta.get("summary", ""), "image": meta.get("image", ""), "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                      "highlights": meta.get("highlights_list", []), "minutes": max(1, round(words / 220)),
                      "html": markdown.markdown(body_md, extensions=["extra", "smarty", "attr_list"])})
    return sorted(posts, key=lambda p: p["date"], reverse=True)

def nice_date(s):
    try: return datetime.date.fromisoformat(s).strftime("%-d %B %Y")
    except Exception: return s

def post_meta(p, root=""):
    tags = " ".join(f'<span class="tagc">{e(t)}</span>' for t in p["tags"])
    return f'<div class="pmeta">{tags}<span>{e(nice_date(p["date"]))}</span><span>{p["minutes"]} min read</span></div>'

def post_card(p, root=""):
    cov = f'<a class="cov" href="{root}blog/{p["slug"]}.html"><img src="{root}{p["image"]}" alt="" loading="lazy"></a>' if p["image"] else ""
    return (f'<article class="pcard2">{cov}<div class="pb">{post_meta(p)}<h3><a href="{root}blog/{p["slug"]}.html">{e(p["title"])}</a></h3>'
            f'<p>{e(p["summary"])}</p></div></article>')

def build_blog(posts):
    if not posts:
        body_main = '<p class="muted">No posts yet.</p>'
    else:
        f = posts[0]
        cov = f'<a class="cov" href="blog/{f["slug"]}.html"><img src="{f["image"]}" alt=""></a>' if f["image"] else ""
        featured = (f'<article class="featured">{cov}<div class="fb">{post_meta(f)}<h2><a href="blog/{f["slug"]}.html">{e(f["title"])}</a></h2>'
                    f'<p>{e(f["summary"])}</p><div class="pmeta"><span>By {e(f["author"])}</span></div></div></article>')
        rest = "".join(post_card(p) for p in posts[1:])
        body_main = featured + (f'<div class="grid posts">{rest}</div>' if rest else "")
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">{e(BLOG["label"])}</div><h1>Notes from the lab</h1><p>{e(BLOG["intro"])}</p>
</div></div></section>
<section class="block"><div class="wrap">{body_main}</div></section>
"""
    return page(BLOG["label"], body, "blog.html")

def build_post(p, posts):
    pi = PEOPLE["pi"]
    is_pi = p["author"].replace("Dr. ", "") in pi["name"]
    av = f'<img src="../{pi["photo"]}" alt="">' if (is_pi and pi.get("photo")) else f'<div class="ini">{"".join(w[0] for w in p["author"].replace("Dr. ", "").split()[:2])}</div>'
    role = pi["role"].split(" · ")[-1] + ", " + LAB["inst"] if is_pi else LAB["short"]
    cover = f'<div class="post-cover"><img src="../{p["image"]}" alt=""></div>' if p["image"] else ""
    hl = ""
    if p["highlights"]:
        hl = '<div class="keybox"><div class="kh">In brief</div><ul>' + "".join(f"<li>{e(h)}</li>" for h in p["highlights"]) + "</ul></div>"
    bio = pi["bio"] if is_pi else ""
    author_box = (f'<div class="author-box">{av.replace("<div class=", "<div class=")}<div><b>{e(p["author"])}</b><p>{e(bio)}</p></div></div>') if bio else ""
    others = [q for q in posts if q["slug"] != p["slug"]][:3]
    more = (f'<div class="more-posts"><h3>More from the blog</h3><div class="grid posts">{"".join(post_card(q, "../") for q in others)}</div></div>') if others else ""
    url = f'https://{LAB["domain"]}/blog/{p["slug"]}.html'
    body = f"""
<section class="post-hero"><div class="wrap">
  <div class="pmeta"><a href="../blog.html" style="color:inherit">{e(BLOG["label"])}</a>{"".join(f'<span class="tagc">{e(t)}</span>' for t in p["tags"])}</div>
  <h1>{e(p["title"])}</h1>
  <p class="dek">{e(p["summary"])}</p>
  <div class="byline">{av}<div><b>{e(p["author"])}</b><span>{e(role)} · {e(nice_date(p["date"]))} · {p["minutes"]} min read</span></div></div>
</div></section>
{cover}
<div class="post-wrap"><article class="post">
{hl}
{p["html"]}
<div class="share"><span>Share</span>
  <a href="https://twitter.com/intent/tweet?text={html.escape(p["title"])}&url={url}" target="_blank" rel="noopener">X / Twitter</a>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener">LinkedIn</a>
  <a href="https://wa.me/?text={html.escape(p["title"])}%20{url}" target="_blank" rel="noopener">WhatsApp</a>
  <button type="button" id="copyLink" data-url="{url}">Copy link</button></div>
{author_box}
{more}
<div class="post-nav"><a href="../blog.html">← All posts</a></div>
</article></div>
<script>
(function(){{var c=document.getElementById('copyLink');if(!c)return;c.addEventListener('click',function(){{var u=location.href.split('#')[0];
(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{c.textContent='Copied';setTimeout(function(){{c.textContent='Copy link';}},1800);}},function(){{window.prompt('Copy this link',u);}});}});}})();
</script>
"""
    return page(p["title"], body, "blog.html", depth=1, desc=p["summary"], image=p["image"] or None)

DATA_ITEMS = [
    {"kind": "Interactive dashboard", "title": "Vacant land tax across Indian cities", "href": "data/vlt-dashboard.html",
     "thumb": "assets/blog/cover-plot-empty.jpg",
     "desc": "38 cities, 16 states, 2011–2025. Map, ranking and city-by-city formulas for what it costs to hold a residential plot empty."},
    {"kind": "Interactive explorer", "title": "District urban hierarchy explorer", "href": "data/district-hierarchy.html",
     "thumb": "assets/blog/zipf-district-map.jpg",
     "desc": "Zipf's exponent for the towns in 415 districts: search any district, see how top-heavy its urban system is, and compare it with its state and the country."},
    {"kind": "Data story", "title": "One big town, or many small ones?", "href": "blog/one-big-town-or-many-small-ones.html",
     "thumb": "assets/blog/zipf-by-state.svg", "desc": "District-level urban hierarchy by state: Kerala and Tamil Nadu flat, Bihar, Haryana and Gujarat top-heavy."},
    {"kind": "Data story", "title": "What does it cost to leave a plot empty in India?", "href": "blog/what-it-costs-to-leave-a-plot-empty.html",
     "thumb": "assets/blog/vlt-38-cities-2025.svg", "desc": "A 400-fold spread in the holding cost of the same plot, and the four tax designs behind it."},
    {"kind": "Data story", "title": "The frozen tax", "href": "blog/the-frozen-tax.html",
     "thumb": "assets/blog/vlt-frozen-rates.svg", "desc": "Nine cities whose rates did not move for a decade or more, and what happened when they finally did."},
    {"kind": "Data story", "title": "Who really pays?", "href": "blog/who-really-pays.html",
     "thumb": "assets/blog/vlt-core-periphery-ratio.svg", "desc": "Core-to-periphery tax ratios for 36 cities, from 9× in Amritsar to below 1 in Kalaburagi."},
]

def build_data_index():
    cards = "".join(f'<a class="card" href="{d["href"]}"><div class="thumb" style="aspect-ratio:16/9;background:var(--paper)"><img src="{d["thumb"]}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:top"></div>'
                    f'<div class="card-body"><div class="eyebrow amber">{e(d["kind"])}</div><h3>{e(d["title"])}</h3><p>{e(d["desc"])}</p><span class="cta">Open →</span></div></a>' for d in DATA_ITEMS)
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Data &amp; visuals</div><h1>Datasets, dashboards and charts</h1>
  <p>Interactive views and single-chart stories built from the datasets the lab assembles. We publish aggregates and visuals here; underlying data are released with the papers or on request.</p>
</div></div></section>
<section class="block"><div class="wrap"><div class="grid themes ds-grid">{cards}</div></div></section>
"""
    return page("Data & Visuals", body, "data.html")

def build_zipf_explorer():
    return page("District urban hierarchy explorer", dashboard_zipf.BODY, "data.html", depth=1,
                desc="Zipf's exponent for the towns in 415 Indian districts: how top-heavy is each district's urban system?")

def build_vlt_dashboard():
    return page("Vacant land tax dashboard", dashboard_vlt.BODY, "data.html", depth=1,
                desc="Interactive dashboard: vacant land tax on a standard plot across 38 Indian cities, 2011–2025.")

def build_events():
    items = "".join(event_html(ev) for ev in EVENTS_SORTED)
    news = "".join(f'<li><span class="d">{e(n["date_text"])}</span>{e(n["text"])}</li>' for n in sorted(NEWS, key=lambda n: n["date"], reverse=True))
    talks = "".join(talk_html(t) for t in sorted(TALKS, key=lambda t: t["date"], reverse=True))
    confs = "".join(f'<div class="talk"><div class="d">{e(c["date_text"])}</div><div><div class="t">{e(c["title"])}</div>'
                    f'<div class="v">{e(c["venue"])}{(" · " + e(c["note"])) if c.get("note") else ""}</div></div></div>'
                    for c in sorted(CONFERENCES, key=lambda c: c["date"], reverse=True))
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">News &amp; talks</div><h1>News, seminars and talks</h1>
  <p>What the lab has been doing: events we have organised, papers presented and invited talks, and conferences attended.</p>
</div></div></section>
<section class="block"><div class="wrap">
  <h2 class="subhead">Events organised</h2>{items}
</div></section>
<section class="block alt"><div class="wrap two-col">
  <div class="min"><h2 class="subhead">Papers presented and invited talks</h2>{talks}
    <h2 class="subhead" style="margin-top:40px">Conferences attended</h2>{confs}</div>
  <div class="min"><h2 class="subhead">News</h2><ul class="timeline">{news}</ul></div>
</div></section>
"""
    return page("News & Talks", body, "events.html")

def build_teaching():
    courses = "".join(f'<div class="course"><div class="code">{e(c["code"])}<small>{e(c["term"])} · {e(c["level"])}</small></div>'
                      f'<div><h3>{e(c["title"])}</h3><p>{e(c["desc"])}</p></div></div>' for c in TEACHING)
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Teaching</div><h1>Courses at IIT Roorkee</h1>
  <p>Courses taught by lab members in the Department of Humanities &amp; Social Sciences. Students interested in a thesis or project in urban economics are welcome to get in touch; current and past thesis students are listed on the <a href="people.html">People</a> page.</p>
</div></div></section>
<section class="block"><div class="wrap"><div class="proj-list">{courses}</div></div></section>
"""
    return page("Teaching", body, "teaching.html")

def build_opportunities():
    ops = OPPORTUNITIES["openings"]
    openings = ("".join(f'<div class="opening"><h3>{e(o["title"])}</h3><p>{e(o["note"])}</p>' +
                        (f'<p class="muted" style="margin-top:6px">Deadline: {e(o["deadline"])}</p>' if o.get("deadline") else "") + "</div>" for o in ops)
                if ops else '<div class="opening"><h3>No funded openings at the moment</h3><p>New positions are announced here as projects are funded.</p></div>')
    body = f"""
<section class="page-head"><div class="wrap"><div>
  <div class="eyebrow">Join us</div><h1>Opportunities</h1>
  <p>PhD positions, research fellowships and internships at CEL Lab.</p>
</div></div></section>
<section class="block"><div class="wrap">
  <div class="eyebrow" style="margin-bottom:14px">Current openings</div>
  <div class="openings">{openings}</div>
  <div class="note"><h3>Prospective students and interns</h3><p>{e(OPPORTUNITIES["standing"])}</p>
  <p style="margin-top:14px"><a class="btn" href="contact.html">Contact the lab</a></p></div>
</div></section>
"""
    return page("Opportunities", body, "opportunities.html")

FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="{PAL["navy"]}"/><text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="34" fill="#fff">C</text></svg>'

def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets")); os.makedirs(os.path.join(OUT, "research")); os.makedirs(os.path.join(OUT, "blog")); os.makedirs(os.path.join(OUT, "data"))
    w = lambda rel, s: open(os.path.join(OUT, rel), "w", encoding="utf-8").write(s)
    w("assets/style.css", CSS.replace('DASHCSS_PLACEHOLDER', dashboard_vlt.CSS + dashboard_zipf.CSS).strip() + "\n")
    w("assets/favicon.svg", FAVICON)
    w("index.html", build_index()); w("research.html", build_research()); w("projects.html", build_projects())
    w("people.html", build_people()); w("publications.html", build_publications()); w("contact.html", build_contact())
    w("events.html", build_events()); w("opportunities.html", build_opportunities()); w("teaching.html", build_teaching())
    src_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site-src-assets")
    if os.path.isdir(src_assets):
        shutil.copytree(src_assets, os.path.join(OUT, "assets"), dirs_exist_ok=True)
    for t in THEMES: w(f"research/{t['slug']}.html", build_theme(t))
    w("data.html", build_data_index()); w("data/vlt-dashboard.html", build_vlt_dashboard()); w("data/district-hierarchy.html", build_zipf_explorer())
    posts = load_posts(); w("blog.html", build_blog(posts))
    for p in posts: w(f"blog/{p['slug']}.html", build_post(p, posts))
    if LAB.get("cname_live"): w("CNAME", LAB["domain"] + "\n")  # only once DNS for the domain points at GitHub
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files in", OUT)

if __name__ == "__main__":
    main()
