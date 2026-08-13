# Roth Hydraulics Nederland

Nederlandstalige product- en leadgeneratiewebsite voor Roth Hydraulics in Nederland, beheerd via de officiële Nederlandse distributieroute van Hobo Hydrauliek B.V.

## Productcatalogus

`producten.html` bevat een uitgebreide, doorzoekbare Roth-catalogus met **46 publiek benoemde producten, productvarianten, opties en oplossingen**, verdeeld over:

- hydraulische accumulatoren;
- zuigeropties en positie-/conditiemonitoring;
- speciale accumulatoren;
- drukvaten;
- accumulatorsystemen;
- accumulatoraccessoires;
- innovaties zoals de N₂-laadunit en Roth DURALOCK®;
- publiek benoemde klantspecifieke Roth-oplossingen.

De catalogus is gebaseerd op de actuele officiële Roth Hydraulics productsite plus expliciet benoemde producten uit officiële eerdere Roth-productdocumentatie. Er worden geen niet-gepubliceerde artikelnummers of specificaties verzonnen.

## Lokale productafbeeldingen

Productbeelden worden lokaal vanuit `assets/products/` geladen; de productpagina gebruikt geen externe image-hotlinks. Exacte officiële Roth-productfoto's worden gebruikt waar Roth die publiek beschikbaar stelt. Wanneer voor een specifieke optie of speciale variant geen afzonderlijke foto wordt gepubliceerd, gebruikt de catalogus een lokaal opgeslagen officiële Roth-familiefoto en wordt deze expliciet als **representatief** aangeduid.

De bronadministratie staat in `assets/products/SOURCES.md`. De workflow `.github/workflows/localize-roth-product-images.yml` kan de officiële Roth-productbeelden opnieuw lokaliseren wanneer de bronwebsite verandert.

## Publiceren op Cloudflare Pages

- Framework preset: **None**
- Build command: leeg laten
- Build output directory: `/`
- Root directory: `/`

De site is statisch en gebruikt alleen HTML, CSS en JavaScript. Het aanvraagformulier stelt een e-mail aan `info@hobohydrauliek.nl` op in het e-mailprogramma van de bezoeker.

## Overige inhoud

- Markt- en toepassingsgebieden
- Engineering, selectie, service en advies
- Roth-bedrijfs- en achtergrondinformatie
- Nederlandse offerte- en contactroute via Hobo Hydrauliek B.V.
- SEO, sitemap, redirects en security headers
- Responsieve desktop-, tablet- en mobiele vormgeving


## Catalogus UX

- 46 benoemde Roth-producten, opties en oplossingen
- Zoeken en filteren
- Multi-product shortlist voor één technische aanvraag
- Vergelijking van geselecteerde catalogusitems op gepubliceerde kerngegevens
- Contextuele links naar relevante aangrenzende productgroepen
- Technische downloadhub met actuele links naar officiële Roth Hydraulics-documentatie
