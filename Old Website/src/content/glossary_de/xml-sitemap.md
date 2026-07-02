---
term: "XML Sitemap"
slug: "xml-sitemap"
definition: "Eine XML Sitemap ist eine Datei, die alle wichtigen URLs Ihrer Website auflistet und Suchmaschinen wie Google hilft, Ihre Seiten schneller zu entdecken, zu crawlen und zu indexieren."
category: "SEO"
difficulty: "Intermediate"
keyword: "Sitemap erstellen"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "technical-seo"
  - "google-search-console"
---

## Was ist eine XML Sitemap?

**Eine XML Sitemap ist eine strukturierte Datei (im XML-Format), die Suchmaschinen eine vollständige Liste der URLs Ihrer Website liefert, die gecrawlt und indexiert werden sollen.**

Im Grunde ist sie eine Wegbeschreibung für [Crawler](/glossary/crawling). Ohne sie muss Googlebot Ihre Seiten entdecken, indem er Links folgt. Das funktioniert – nur langsam und unvollständig. Verwaiste Seiten ohne interne Links werden möglicherweise nie gefunden.

Googles eigene Dokumentation bezeichnet Sitemaps als „besonders hilfreich" für große Websites, neue Websites mit wenigen externen Links und Seiten mit umfangreichen Medieninhalten. Eine Studie von Oncrawl zeigte, dass in einer XML Sitemap aufgeführte Seiten im Durchschnitt 8- bis 10-mal schneller indexiert werden als nicht enthaltene Seiten.

## Warum ist eine XML Sitemap wichtig?

Findet Google Ihre Seiten nicht, kann es sie auch nicht ranken. Eine XML Sitemap räumt das Rätselraten beiseite.

- **Schnellere Indexierung neuer Inhalte**. Wenn Sie einen neuen Blogbeitrag oder eine Landingpage veröffentlichen, weiß Google sofort Bescheid. Niemand muss warten, bis Googlebot die Seite zufällig über einen Link findet.
- **Abdeckung verwaister Seiten**. Seiten ohne interne Links sind für Crawler unsichtbar. Die Sitemap fängt sie auf. Ein typisches Problem bei großen E-Commerce-Shops mit filtergenerierten Seiten.
- **Aktualitäts- und Prioritätssignale**. Sitemaps enthalten `<lastmod>`-Tags, die Google verraten, wann eine Seite zuletzt aktualisiert wurde. Frische Inhalte werden schneller erneut gecrawlt.
- **Diagnostischer Wert**. Wer seine Sitemap an die [Google Search Console](/glossary/google-search-console) übermittelt, erhält einen Indexierungsbericht. Sie sehen exakt, welche Seiten Google indexiert hat – und welche nicht. Und warum.

Für jede Website, die regelmäßig Inhalte veröffentlicht, ist eine XML Sitemap nicht verhandelbar.

## Wie eine XML Sitemap funktioniert

Der Ablauf ist simpel: Datei erstellen, Google den Pfad mitteilen, aktuell halten.

### Dateistruktur

Eine XML Sitemap besteht aus einer Liste von `<url>`-Einträgen, eingebettet in einem `<urlset>`-Tag. Jeder Eintrag enthält die URL (`<loc>`), das Datum der letzten Änderung (`<lastmod>`), die Änderungsfrequenz (`<changefreq>`) und die Priorität (`<priority>`). Google ignoriert offiziell `changefreq` und `priority`. Was zählt, sind URL und `lastmod`.

### Übermittlungsmethoden

Es gibt drei Wege, Ihre Sitemap an Google zu übermitteln. Erstens: Direktübermittlung über die [Google Search Console](/glossary/google-search-console). Zweitens: Verweis in Ihrer [robots.txt](/glossary/robots-txt) mit `Sitemap: https://ihresite.de/sitemap.xml`. Drittens: Die Ping-API, um Google über Updates zu informieren. Die meisten Websites kombinieren die ersten beiden Methoden.

### Sitemap-Index-Dateien

Eine einzelne Sitemap fasst maximal 50.000 URLs oder 50 MB (unkomprimiert). Größere Websites nutzen eine Index-Datei – eine Sitemap, die auf weitere Sitemaps verweist. Eine Site mit 200.000 Seiten hat dann etwa einen Index, der auf vier Sitemaps mit je 50.000 URLs zeigt.

### Auto-Generierung

Die meisten CMS-Plattformen (WordPress, Webflow, Shopify) erzeugen XML Sitemaps automatisch. WordPress legt sie standardmäßig unter `/wp-sitemap.xml` an. SEO-Plugins wie Yoast und RankMath geben Ihnen mehr Kontrolle darüber, welche Seiten enthalten sind.

## Arten von XML Sitemaps

Nicht jede Sitemap erfüllt denselben Zweck:

- **Standard-XML-Sitemap**. Listet Ihre HTML-Seiten. Der häufigste Typ – und der, den die meisten meinen, wenn sie „Sitemap" sagen.
- **Bilder-Sitemap**. Listet die Bilder Ihrer Website für die Auffindbarkeit in Google Bilder. Sinnvoll für Fotografen, Online-Shops und visuell geprägte Seiten.
- **Video-Sitemap**. Liefert Metadaten zu Videoinhalten (Titel, Beschreibung, Thumbnail, Dauer). Hilft dabei, in Googles Video-Karussells aufzutauchen.
- **News-Sitemap**. Speziell für Google-News-Publisher. Enthält Veröffentlichungsdatum, Titel und Sprache. Nur für als Newsquelle zugelassene Seiten.
- **Sitemap-Index**. Eine Master-Datei, die auf mehrere Sitemaps verweist. Pflicht für große Websites, die das 50.000-URL-Limit überschreiten.

Die meisten kleinen und mittleren Unternehmen brauchen nur eine Standard-XML-Sitemap. Bilder- oder Video-Sitemaps lohnen sich, wenn visuelle Inhalte eine zentrale Rolle spielen.

## Beispiele für XML Sitemaps

**Beispiel 1: Neue Website eines lokalen Unternehmens**
Ein neu gegründeter Klempnerbetrieb in München hat 15 Seiten und null [Backlinks](/glossary/backlinks). Ohne Sitemap kann es Wochen dauern, bis Google alle Seiten allein über Linkverfolgung entdeckt. Nach Übermittlung einer Sitemap an die Search Console sind alle 15 Seiten innerhalb von 5 Tagen indexiert.

**Beispiel 2: Online-Shop mit 10.000 Produkten**
Ein Händler stellt wöchentlich 50 neue Produkte ein. Seine Sitemap aktualisiert sich automatisch über Shopify – `<lastmod>`-Daten werden bei jeder Produktanlage angepasst. Google crawlt die Sitemap regelmäßig erneut und entdeckt neue Produkte innerhalb weniger Tage. Nicht Wochen.

**Beispiel 3: Blog mit 30 Beiträgen pro Monat**
Ein Unternehmen, das theStacc nutzt, veröffentlicht monatlich 30 SEO-optimierte Artikel. Jeder neue Beitrag erscheint automatisch in der XML Sitemap. Der Indexabdeckungsbericht der Google Search Console zeigt konstantes Wachstum bei den indexierten Seiten. Manuelle Sitemap-Pflege? Entfällt.

## XML Sitemap vs. HTML-Sitemap

Unterschiedliche Dateien für unterschiedliche Zielgruppen.

| | XML Sitemap | HTML-Sitemap |
|---|---|---|
| **Zielgruppe** | Suchmaschinen-Crawler | Menschliche Besucher |
| **Format** | XML-Code | Normale Webseite mit Links |
| **Speicherort** | `/sitemap.xml` | Meist `/sitemap` oder im Footer verlinkt |
| **Zweck** | Crawlern alle Seiten zugänglich machen | Nutzern die Navigation erleichtern |
| **SEO-Wirkung** | Verbessert direkt die Crawl-Effizienz | Gering. Eher ein UX-Feature |
| **Pflicht?** | Dringend empfohlen | Optional, nice to have |

Beide haben ihren Nutzen, doch nur die XML Sitemap wirkt sich direkt auf [SEO](/glossary/seo) aus. Wenn Sie nur eine umsetzen, dann die XML-Variante.

## Best Practices für XML Sitemaps

- **Nur indexierbare Seiten aufnehmen**. Keine Seiten mit [Noindex](/glossary/noindex)-Tag, keine Weiterleitungen, keine durch robots.txt blockierten URLs. Eine saubere Sitemap stärkt Googles Vertrauen.
- **`<lastmod>`-Daten korrekt halten**. Aktualisieren Sie das Datum nur, wenn sich der Seiteninhalt tatsächlich geändert hat. Wer Aktualität vortäuscht, untergräbt das Vertrauen in seine Sitemap-Signale.
- **Über die Google Search Console übermitteln**. Die manuelle Übermittlung gibt Ihnen Zugriff auf den Indexierungsbericht – Sie sehen exakt, wie Google Ihre Sitemap verarbeitet. Monatlich prüfen.
- **Maximal 50.000 URLs pro Datei**. Mehr? Sitemap-Index nutzen. Eine zu große, fehlerhafte Sitemap richtet mehr Schaden an als gar keine.
- **Mit konstanter Veröffentlichung kombinieren**. Eine Sitemap entfaltet ihren Wert erst, wenn Ihre Seite regelmäßig neue Inhalte fürs [Indexieren](/glossary/indexing) liefert. theStacc veröffentlicht 30 SEO-Artikel pro Monat – damit hat Google einen klaren Grund, Ihre Sitemap häufig zu crawlen und frische Seiten zu finden.

## Häufig gestellte Fragen

### Braucht jede Website eine XML Sitemap?

Nicht zwingend. Kleine Websites mit starker [interner Verlinkung](/glossary/internal-link) kommen auch ohne aus. Aber es gibt keinen Nachteil – und der Vorteil bei Indexierungsgeschwindigkeit und Diagnose-Daten lohnt den minimalen Aufwand für jede Seite.

### Wie erstelle ich eine XML Sitemap?

Die meisten CMS-Plattformen erstellen sie automatisch. WordPress, Webflow und Shopify legen Sitemaps standardmäßig an. Für individuelle Websites generieren Tools wie Screaming Frog oder XML-Sitemaps.com die Datei. Anschließend über die Google Search Console übermitteln.

### Wie oft sollte ich meine Sitemap aktualisieren?

Idealerweise aktualisiert sich Ihre Sitemap automatisch, wenn Sie Inhalte veröffentlichen oder ändern. CMS-generierte Sitemaps erledigen das. Wer manuell pflegt, sollte sie bei jedem Hinzufügen, Entfernen oder größeren Umbau einer Seite aktualisieren.

### Kann eine schlechte Sitemap meinem SEO schaden?

Eine Sitemap mit defekten URLs, noindexierten Seiten oder falschen lastmod-Daten sendet widersprüchliche Signale an Google. Eine direkte Strafe gibt es nicht – aber sie verschwendet [Crawl Budget](/glossary/crawl-budget) und verlangsamt die Indexierung Ihrer wichtigen Seiten.

---

Wollen Sie frische Inhalte, die Google tatsächlich indexiert? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Sitemaps verstehen](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google Search Central: Sitemap erstellen und übermitteln](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Ahrefs: XML Sitemaps – der komplette Leitfaden](https://ahrefs.com/blog/xml-sitemap/)
- [Moz: XML Sitemaps](https://moz.com/learn/seo/xml-sitemaps)
