from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import html as html_lib
import json
import re

ROOT = Path('.')
ROTH = 'https://www.roth-hydraulics.de'
TECH = f'{ROTH}/en/infocenter/technical-documents'
ACCESSORIES = f'{ROTH}/en/infocenter/technical-documents-accessories'
PRODUCT_INFO = f'{ROTH}/en/infocenter/product-and-information'
CERTIFICATES = f'{ROTH}/en/infocenter/certificates'


def fetch(url):
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; RothHydraulicsNL/1.0)'})
        return urlopen(request, timeout=30).read().decode('utf-8', 'ignore')
    except Exception as exc:
        print('WARN fetch', url, exc)
        return ''


def find_pdf(page_html, filename, fallback):
    if page_html:
        pattern = r'href=["\']([^"\']*' + re.escape(filename) + r')["\']'
        match = re.search(pattern, page_html, re.I)
        if match:
            return urljoin(ROTH, html_lib.unescape(match.group(1)))
    return fallback


tech_html = fetch(TECH)
accessory_html = fetch(ACCESSORIES)
info_html = fetch(PRODUCT_INFO)

docs = [
    ('Productcatalogus Roth Hydraulics', 'Engels', 'Productcatalogus', 'Roth_Hydraulics_Product_catalogue_EN.pdf', find_pdf(info_html, 'Roth_Hydraulics_Product_catalogue_EN.pdf', PRODUCT_INFO)),
    ('Membraanaccumulator CE', 'Engels · actuele 2026-editie', 'Handleiding', 'BA-MEAK-CE-EN_01-2026_00.pdf', find_pdf(tech_html, 'BA-MEAK-CE-EN_01-2026_00.pdf', TECH)),
    ('Blaasaccumulator CE', 'Nederlands', 'Handleiding', 'BA-BLAK-CE-NL_02-2017_01.pdf', find_pdf(tech_html, 'BA-BLAK-CE-NL_02-2017_01.pdf', TECH)),
    ('Zuigeraccumulator CE', 'Nederlands', 'Handleiding', 'BA-AK-CE-NL_09-2016_01.pdf', find_pdf(tech_html, 'BA-AK-CE-NL_09-2016_01.pdf', TECH)),
    ('Drukvat / drukapparaat CE', 'Nederlands', 'Handleiding', 'BA-DB-CE-NL_01-2018_00.pdf', find_pdf(tech_html, 'BA-DB-CE-NL_01-2018_00.pdf', TECH)),
    ('Drukverhoger CE', 'Nederlands', 'Handleiding', 'BA-D-CE-NL_11-2016_01.pdf', find_pdf(tech_html, 'BA-D-CE-NL_11-2016_01.pdf', TECH)),
    ('Vul- en testapparatuur', 'Nederlands', 'Handleiding', 'BA-FPE-NL_12-2016_01.pdf', find_pdf(accessory_html, 'BA-FPE-NL_12-2016_01.pdf', ACCESSORIES)),
    ('N₂-laadunit', 'Engels', 'Handleiding', 'BA-AGGR-CE-EN-36X5095_10-2021_00_kpl.pdf', find_pdf(accessory_html, 'BA-AGGR-CE-EN-36X5095_10-2021_00_kpl.pdf', ACCESSORIES)),
]

# Add Downloads to all existing site navigation/footer sets.
for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    if 'href="downloads.html"' not in text:
        text = text.replace(
            '<a href="service.html">Service & advies</a><a href="over-roth.html">',
            '<a href="service.html">Service & advies</a><a href="downloads.html">Downloads</a><a href="over-roth.html">'
        )
        text = text.replace(
            '<a href="service.html">Service &amp; advies</a><a href="over-roth.html">',
            '<a href="service.html">Service &amp; advies</a><a href="downloads.html">Downloads</a><a href="over-roth.html">'
        )
    path.write_text(text, encoding='utf-8')

# Generate download hub.
doc_cards = ''.join(
    f'<article class="download-doc"><div class="download-doc-type">{html_lib.escape(kind)}</div>'
    f'<h3>{html_lib.escape(title)}</h3><p>{html_lib.escape(lang)}</p>'
    f'<span>{html_lib.escape(filename)}</span>'
    f'<a href="{html_lib.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">Open bij Roth Hydraulics →</a></article>'
    for title, lang, kind, filename, url in docs
)
itemlist = [
    {'@type': 'ListItem', 'position': i, 'name': item[0], 'url': item[4]}
    for i, item in enumerate(docs, 1)
]
schema = json.dumps({
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    'name': 'Officiële Roth Hydraulics technische downloads',
    'numberOfItems': len(itemlist),
    'itemListElement': itemlist,
}, ensure_ascii=False, separators=(',', ':'))

downloads = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Roth Hydraulics downloads | Catalogus, handleidingen en certificaten</title>
<meta name="description" content="Officiële Roth Hydraulics productcatalogus, Nederlandstalige technische handleidingen, accessoiresdocumentatie en certificaten voor Nederlandse gebruikers via Hobo Hydrauliek.">
<link rel="canonical" href="https://rothhydraulics.nl/downloads.html"><meta name="theme-color" content="#cf101a">
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="downloads.css">
<script type="application/ld+json">{schema}</script>
</head><body>
<div class="topbar"><div class="container"><div><strong>Roth Hydraulics Nederland</strong> · officiële distributeur voor Nederland: Hobo Hydrauliek B.V.</div><div class="topbar-links"><a href="tel:+31591314163">0591 31 41 63</a><a href="mailto:info@hobohydrauliek.nl">info@hobohydrauliek.nl</a></div></div></div>
<header class="site-header"><div class="container nav"><a class="brand" href="index.html"><span class="brand-mark">R</span><span class="brand-copy"><strong>ROTH HYDRAULICS</strong><span>Nederland · via Hobo Hydrauliek</span></span></a><nav class="main-nav" aria-label="Hoofdnavigatie"><a href="index.html">Home</a><a href="producten.html">Producten</a><a href="toepassingen.html">Toepassingen</a><a href="service.html">Service & advies</a><a class="active" href="downloads.html">Downloads</a><a href="over-roth.html">Over Roth</a><a class="nav-cta" href="contact.html">Offerte aanvragen</a></nav><button class="mobile-toggle" aria-label="Menu openen" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button><nav class="mobile-menu" aria-label="Mobiele navigatie"><a href="index.html">Home</a><a href="producten.html">Producten</a><a href="toepassingen.html">Toepassingen</a><a href="service.html">Service & advies</a><a href="downloads.html">Downloads</a><a href="over-roth.html">Over Roth</a><a href="contact.html">Offerte aanvragen</a></nav></div></header>
<main>
<section class="page-hero downloads-hero"><div class="container"><div class="breadcrumbs"><a href="index.html">Home</a> / Downloads</div><h1>Technische Roth-documentatie, rechtstreeks van de fabrikant.</h1><p>Productcatalogus, handleidingen, certificaten en technische documenten voor selectie, installatie en service. De documenten blijven bewust op de officiële Roth Hydraulics-omgeving zodat u altijd de fabrikantversie opent.</p><div class="actions"><a class="btn btn-primary" href="producten.html">Naar de complete productcatalogus →</a><a class="btn btn-secondary" href="contact.html">Technische vraag aan Hobo</a></div></div></section>
<section class="section"><div class="container"><div class="downloads-intro"><div><div class="section-label">Geselecteerde documenten</div><h2>De belangrijkste documenten voor Nederlandse gebruikers.</h2></div><p>Roth publiceert manuals per producttype, certificering en taal. Hieronder staan de belangrijkste ingangen voor Nederland; bij twijfel gebruikt u het officiële Infocenter.</p></div><div class="download-doc-grid">{doc_cards}</div></div></section>
<section class="section section-soft"><div class="container"><div class="downloads-source-grid"><article><h2>Alle technische documenten</h2><p>Complete fabrikantindex met CE- en ASME-handleidingen, verklaringen en aanvullende documentatie.</p><a class="btn btn-secondary" href="{TECH}" target="_blank" rel="noopener noreferrer">Open technisch Infocenter →</a></article><article><h2>Accessoires & service</h2><p>Handleidingen voor vul-/testapparatuur, N₂-laadunit en veiligheids-/afsluitblokken.</p><a class="btn btn-secondary" href="{ACCESSORIES}" target="_blank" rel="noopener noreferrer">Open accessoiredocumentatie →</a></article><article><h2>Certificaten</h2><p>Bedrijfs- en productcertificaten en bijzondere goedkeuringen worden door Roth centraal bijgehouden.</p><a class="btn btn-secondary" href="{CERTIFICATES}" target="_blank" rel="noopener noreferrer">Open certificaten →</a></article></div><div class="downloads-legal"><strong>Waarom geen lokale PDF-kopieën?</strong><p>De Nederlandse site verwijst rechtstreeks naar de fabrikantdocumenten. Zo blijft versiebeheer bij Roth Hydraulics en voorkomen we dat een verouderde of niet-vrij verspreidbare handleiding lokaal blijft circuleren.</p></div></div></section>
<section class="section"><div class="container contact-strip"><div><h2>Niet zeker welk document bij uw accumulator hoort?</h2><p>Stuur typeaanduiding, serienummer of een foto van het typeplaatje naar Hobo Hydrauliek.</p></div><a class="btn" href="contact.html">Vraag documenthulp →</a></div></section>
</main>
<footer class="footer"><div class="container"><div class="footer-grid"><div><div class="footer-brand"><span class="brand-mark">R</span><div><strong>Roth Hydraulics Nederland</strong><br><small>Distributie & ondersteuning via Hobo Hydrauliek B.V.</small></div></div><p>Nederlandse productinformatie, technische documentatie en offertebegeleiding voor Roth Hydraulics.</p></div><div><h4>Producten</h4><a href="producten.html#membraanaccumulatoren">Membraanaccumulatoren</a><a href="producten.html#blaasaccumulatoren">Blaasaccumulatoren</a><a href="producten.html#zuigeraccumulatoren">Zuigeraccumulatoren</a><a href="producten.html#systemen">Accumulatorsystemen</a></div><div><h4>Informatie</h4><a href="toepassingen.html">Toepassingen</a><a href="service.html">Service & advies</a><a href="downloads.html">Downloads</a><a href="over-roth.html">Over Roth</a><a href="privacy.html">Privacy</a></div><div><h4>Hobo Hydrauliek B.V.</h4><p>Roald Amundsenstraat 25<br>7825 AP Emmen</p><a href="tel:+31591314163">0591 31 41 63</a><a href="mailto:info@hobohydrauliek.nl">info@hobohydrauliek.nl</a></div></div><div class="footer-bottom"><span>© 2026 Roth Hydraulics Nederland / Hobo Hydrauliek B.V.</span><span>Externe documentlinks openen de officiële Roth Hydraulics-omgeving.</span></div></div></footer>
<script src="script.js" defer></script></body></html>'''
Path('downloads.html').write_text(downloads, encoding='utf-8')

Path('downloads.css').write_text('''
.downloads-hero{background:radial-gradient(circle at 80% 20%,rgba(207,16,26,.08),transparent 32%),linear-gradient(180deg,#fff,#f5f6f7)}
.downloads-intro{display:grid;grid-template-columns:1.1fr .9fr;gap:52px;align-items:end;margin-bottom:34px}.downloads-intro h2{font-size:clamp(34px,4vw,52px)}.downloads-intro p{margin:0;color:var(--muted);font-size:17px}
.download-doc-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.download-doc{border:1px solid var(--line);border-radius:18px;padding:24px;background:#fff;min-height:245px;display:flex;flex-direction:column;transition:.2s ease}.download-doc:hover{transform:translateY(-3px);box-shadow:var(--shadow-sm);border-color:#d5d9dd}.download-doc-type{color:var(--roth);font-size:10px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}.download-doc h3{font-size:22px;margin-top:14px}.download-doc p{color:var(--ink-2);font-weight:700;margin:9px 0 0}.download-doc span{display:block;color:var(--muted);font-size:11px;overflow-wrap:anywhere;margin:12px 0 18px}.download-doc a{margin-top:auto;color:var(--roth);font-weight:800;font-size:13px}
.downloads-source-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.downloads-source-grid article{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px}.downloads-source-grid h2{font-size:24px}.downloads-source-grid p{color:var(--muted);min-height:72px}.downloads-legal{margin-top:24px;border-left:3px solid var(--roth);padding:18px 20px;background:#fff}.downloads-legal p{margin:6px 0 0;color:var(--muted)}
@media(max-width:980px){.download-doc-grid{grid-template-columns:repeat(2,1fr)}.downloads-source-grid,.downloads-intro{grid-template-columns:1fr}}
@media(max-width:620px){.download-doc-grid,.downloads-source-grid{grid-template-columns:1fr}.download-doc{min-height:0}}
''', encoding='utf-8')

# Product page resource rail, compare action and dialog.
product_path = Path('producten.html')
product = product_path.read_text(encoding='utf-8')
if 'catalogue-resource-rail' not in product:
    rail = '<section class="catalogue-resource-rail"><div class="container"><div><strong>Technische documenten nodig?</strong><span>Open officiële Roth-handleidingen, productcatalogus en certificaten.</span></div><a href="downloads.html">Naar Downloads →</a></div></section>'
    product = product.replace('<div class="catalogue-toolbar">', rail + '<div class="catalogue-toolbar">', 1)
if 'id="catalogue-compare"' not in product:
    product = product.replace(
        '<a class="btn btn-primary" id="catalogue-shortlist-request" href="contact.html?shortlist=1">',
        '<button type="button" class="btn btn-secondary" id="catalogue-compare">Vergelijk selectie</button><a class="btn btn-primary" id="catalogue-shortlist-request" href="contact.html?shortlist=1">',
        1
    )
if 'id="catalogue-compare-dialog"' not in product:
    dialog = '<dialog class="catalogue-compare-dialog" id="catalogue-compare-dialog" aria-labelledby="catalogue-compare-title"><div class="compare-head"><div><span>Technische voorselectie</span><h2 id="catalogue-compare-title">Vergelijk geselecteerde Roth-producten</h2></div><button type="button" id="catalogue-compare-close" aria-label="Vergelijking sluiten">×</button></div><p class="compare-note">De vergelijking toont alleen gegevens die al in deze catalogus staan. Het is geen compatibiliteits- of dimensioneringsbevestiging.</p><div class="compare-table-wrap"><table><thead><tr><th>Product</th><th>Type</th><th>Gepubliceerde kerngegevens</th><th></th></tr></thead><tbody id="catalogue-compare-body"></tbody></table></div><div class="compare-footer"><a class="btn btn-primary" href="contact.html?shortlist=1">Laat Hobo de selectie beoordelen →</a></div></dialog>'
    product = product.replace('<footer class="footer">', dialog + '<footer class="footer">', 1)
product_path.write_text(product, encoding='utf-8')

# New catalogue UI styling.
polish_path = Path('catalogue-polish.css')
polish = polish_path.read_text(encoding='utf-8')
if '.catalogue-resource-rail' not in polish:
    polish += '''
.catalogue-resource-rail{background:#17191d;color:#fff;border-bottom:1px solid #2c3035}.catalogue-resource-rail .container{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}.catalogue-resource-rail strong{display:block;font-size:14px}.catalogue-resource-rail span{display:block;color:#aeb4bb;font-size:12px;margin-top:2px}.catalogue-resource-rail a{color:#fff;font-size:13px;font-weight:800;white-space:nowrap}
.catalogue-related{border-top:1px solid #edf0f2;margin-top:16px;padding-top:13px}.catalogue-related>span{display:block;font-size:10px;font-weight:850;letter-spacing:.1em;text-transform:uppercase;color:#8a9199;margin-bottom:7px}.catalogue-related-links{display:flex;flex-wrap:wrap;gap:5px 10px}.catalogue-related a{font-size:11px;font-weight:750;color:#525961;text-decoration:underline;text-decoration-color:#d2d6da;text-underline-offset:3px}.catalogue-related a:hover{color:var(--roth);text-decoration-color:var(--roth)}
.catalogue-compare-dialog{width:min(980px,calc(100% - 30px));max-height:min(780px,calc(100vh - 40px));border:0;border-radius:22px;padding:0;box-shadow:0 32px 90px rgba(10,13,17,.32);color:var(--ink)}.catalogue-compare-dialog::backdrop{background:rgba(12,15,18,.62);backdrop-filter:blur(4px)}.compare-head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;padding:28px 30px 20px;border-bottom:1px solid var(--line)}.compare-head span{display:block;color:var(--roth);font-size:10px;font-weight:850;letter-spacing:.12em;text-transform:uppercase;margin-bottom:6px}.compare-head h2{font-size:clamp(26px,3vw,38px)}.compare-head button{border:1px solid var(--line);background:#fff;border-radius:10px;width:42px;height:42px;font-size:25px;line-height:1;cursor:pointer}.compare-note{margin:0;padding:15px 30px;background:#fff7f7;color:#636a72;font-size:12px}.compare-table-wrap{overflow:auto;max-height:480px}.catalogue-compare-dialog table{width:100%;border-collapse:collapse;min-width:760px}.catalogue-compare-dialog th,.catalogue-compare-dialog td{text-align:left;padding:15px 18px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13px}.catalogue-compare-dialog th{position:sticky;top:0;background:#f5f6f7;font-size:10px;letter-spacing:.08em;text-transform:uppercase;z-index:1}.catalogue-compare-dialog td:first-child{font-weight:800}.catalogue-compare-dialog td a{color:var(--roth);font-weight:800;white-space:nowrap}.compare-footer{padding:18px 30px 26px;display:flex;justify-content:flex-end}.catalogue-shortlist-actions{flex-wrap:wrap}
@media(max-width:680px){.catalogue-resource-rail .container{align-items:flex-start;flex-direction:column;padding-top:14px;padding-bottom:14px;gap:8px}.catalogue-shortlist-actions{grid-template-columns:1fr 1fr}.catalogue-shortlist-actions #catalogue-shortlist-request{grid-column:1/-1}.compare-head{padding:22px 20px 16px}.compare-note{padding:13px 20px}.compare-footer{padding:16px 20px 22px}.catalogue-compare-dialog{max-height:calc(100vh - 20px)}}
'''
polish_path.write_text(polish, encoding='utf-8')

# Add related-product links and comparison logic to catalogue JS.
js_path = Path('catalogue.js')
js = js_path.read_text(encoding='utf-8')
if 'relatedByCategory' not in js:
    addon = r'''
  const relatedByCategory={
    accumulatoren:['veiligheids-en-afsluitblokken','vul-en-testapparatuur-voor-stikstof','klemmen-en-beugels'],
    zuigeropties:['zuigeraccumulatoren','roth-duralock-schroefdraad','zuigeraccumulatorsysteem-standaardbouw'],
    speciaal:['zuigeraccumulatoren','blaasaccumulatoren','membraanaccumulatoren'],
    drukvaten:['zuigeraccumulatorsysteem-standaardbouw','zuigeraccumulatorsysteem-modulaire-bouw','veiligheids-en-afsluitblokken'],
    systemen:['standaard-drukvat','veiligheids-en-afsluitblokken','druksensoren'],
    accessoires:['membraanaccumulatoren','blaasaccumulatoren','zuigeraccumulatoren'],
    innovaties:['vul-en-testapparatuur-voor-stikstof','zuigeraccumulatoren','veiligheids-en-afsluitblokken'],
    maatwerk:['combinatie-zuiger-en-blaasaccumulator','zuigeraccumulatoren','zuigeraccumulatorsysteem-modulaire-bouw']
  };
  cards.forEach(card=>{if(card.querySelector('.catalogue-related'))return;const ids=(relatedByCategory[card.dataset.category]||[]).filter(id=>id!==card.id&&document.getElementById(id)).slice(0,3);if(!ids.length)return;const nav=document.createElement('nav');nav.className='catalogue-related';nav.setAttribute('aria-label','Gerelateerde productgroepen');const label=document.createElement('span');label.textContent='Ook bekijken';const links=document.createElement('div');links.className='catalogue-related-links';ids.forEach(id=>{const target=document.getElementById(id);const title=target?.querySelector('h3')?.textContent?.trim();if(!title)return;const a=document.createElement('a');a.href=`#${id}`;a.textContent=title;links.appendChild(a)});nav.append(label,links);card.querySelector('.catalogue-body')?.appendChild(nav)});
  const compareButton=document.querySelector('#catalogue-compare');const compareDialog=document.querySelector('#catalogue-compare-dialog');const compareClose=document.querySelector('#catalogue-compare-close');const compareBody=document.querySelector('#catalogue-compare-body');
  function buildComparison(){if(!compareBody)return;compareBody.innerHTML='';shortlist.forEach(name=>{const button=shortlistButtons.find(item=>item.dataset.product===name);const card=button?.closest('.catalogue-card');if(!card)return;const row=document.createElement('tr');const productCell=document.createElement('td');productCell.textContent=name;const typeCell=document.createElement('td');typeCell.textContent=card.querySelector('.catalogue-tag')?.textContent?.trim()||card.dataset.category||'';const specCell=document.createElement('td');const specs=[...card.querySelectorAll('.catalogue-specs span')].map(el=>el.textContent.trim()).join(' · ');specCell.textContent=specs||'Toepassingsspecifiek';const linkCell=document.createElement('td');const link=document.createElement('a');link.href=`#${card.id}`;link.textContent='Bekijk kaart';link.addEventListener('click',()=>compareDialog?.close());linkCell.appendChild(link);row.append(productCell,typeCell,specCell,linkCell);compareBody.appendChild(row)})}
  compareButton?.addEventListener('click',()=>{if(!shortlist.length)return;buildComparison();compareDialog?.showModal()});compareClose?.addEventListener('click',()=>compareDialog?.close());compareDialog?.addEventListener('click',event=>{if(event.target===compareDialog)compareDialog.close()});
'''
    marker = '  applyFilters();renderShortlist();\n})();'
    if marker not in js:
        raise SystemExit('Could not locate catalogue JS insertion marker')
    js = js.replace(marker, addon + '\n' + marker)
js_path.write_text(js, encoding='utf-8')

# Homepage bridge into the catalogue and downloads.
index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
if 'catalogue-home-bridge' not in index:
    bridge = '<section class="catalogue-home-bridge reveal"><div class="container"><div><strong>Complete Roth-programma</strong><h2>46 publiek benoemde producten, opties en oplossingen in één Nederlandse catalogus.</h2></div><div><p>Zoek, filter, vergelijk en verzamel producten voor één technische aanvraag aan Hobo Hydrauliek. Officiële Roth-handleidingen zijn apart ontsloten via Downloads.</p><div class="actions"><a class="btn btn-primary" href="producten.html">Open volledige catalogus →</a><a class="btn btn-secondary" href="downloads.html">Technische downloads</a></div></div></div></section>'
    index = index.replace('<section class="section section-soft reveal">', bridge + '<section class="section section-soft reveal">', 1)
index_path.write_text(index, encoding='utf-8')

styles_path = Path('styles.css')
styles = styles_path.read_text(encoding='utf-8')
if '.catalogue-home-bridge' not in styles:
    styles += '''
.catalogue-home-bridge{padding:0 0 88px}.catalogue-home-bridge>.container{display:grid;grid-template-columns:1.05fr .95fr;gap:70px;padding:38px 42px;border-radius:22px;background:#17191d;color:#fff;align-items:center}.catalogue-home-bridge strong{color:#f25a61;font-size:11px;letter-spacing:.12em;text-transform:uppercase}.catalogue-home-bridge h2{font-size:clamp(30px,3.5vw,45px);margin-top:10px}.catalogue-home-bridge p{margin:0;color:#bbc1c7;font-size:16px}.catalogue-home-bridge .btn-secondary{background:transparent;border-color:#4a4f56;color:#fff}@media(max-width:780px){.catalogue-home-bridge>.container{grid-template-columns:1fr;gap:22px;padding:28px}.catalogue-home-bridge{padding-bottom:58px}}
'''
styles_path.write_text(styles, encoding='utf-8')

# Sitemap and README.
sitemap_path = Path('sitemap.xml')
sitemap = sitemap_path.read_text(encoding='utf-8')
if 'downloads.html' not in sitemap:
    sitemap = sitemap.replace('</urlset>', '  <url><loc>https://rothhydraulics.nl/downloads.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
sitemap_path.write_text(sitemap, encoding='utf-8')

readme_path = Path('README.md')
readme = readme_path.read_text(encoding='utf-8')
if 'Technische downloadhub' not in readme:
    readme += '''

## Catalogus UX

- 46 benoemde Roth-producten, opties en oplossingen
- Zoeken en filteren
- Multi-product shortlist voor één technische aanvraag
- Vergelijking van geselecteerde catalogusitems op gepubliceerde kerngegevens
- Contextuele links naar relevante aangrenzende productgroepen
- Technische downloadhub met actuele links naar officiële Roth Hydraulics-documentatie
'''
readme_path.write_text(readme, encoding='utf-8')

print('Product depth pass applied:', len(docs), 'curated official Roth document links.')
