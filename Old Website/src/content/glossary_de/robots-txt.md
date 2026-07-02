---
term: "robots.txt"
slug: "robots-txt"
definition: "robots.txt ist eine Klartextdatei im Stammverzeichnis Ihrer Website, die Suchmaschinen-Crawlern mitteilt, welche URLs sie aufrufen dürfen und welche nicht."
category: "SEO"
difficulty: "Intermediate"
keyword: "robots.txt Datei"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## Was ist robots.txt?

**Eine robots.txt Datei liegt im Stammverzeichnis Ihrer Domain (ihre-seite.de/robots.txt) und legt fest, welche Seiten oder Bereiche Ihrer Website Suchmaschinen-Crawler aufrufen dürfen.**

Jede große Suchmaschine. Google, Bing, Yahoo. Sie alle prüfen diese Datei, bevor sie Ihre Seite [crawlen](/glossary/crawling). Stellen Sie sich das wie die Liste eines Türstehers vor. Kein Schloss an der Tür, sondern eine klare Anweisung, an die sich jeder anständige Bot hält.

Laut Googles eigener Dokumentation ruft Googlebot die robots.txt ab, bevor er irgendeine andere Anfrage an Ihren Server schickt. Bei Sites mit Tausenden von Seiten wird diese Datei zu einem der wichtigsten Bausteine Ihrer [technischen SEO](/glossary/technical-seo).

## Warum ist die robots.txt wichtig?

Eine fehlerhafte robots.txt kann Ihre Rankings über Nacht zerstören. Eine einzige falsch platzierte Anweisung – und Google sieht Ihre wichtigsten Seiten nicht mehr.

- **Schutz des Crawl-Budgets**. Große Sites haben ein begrenztes [Crawl-Budget](/glossary/crawl-budget). Wer Admin-Bereiche, Staging-Umgebungen oder doppelte Filter-URLs sperrt, hält Googlebot bei dem, was zählt.
- **Schutz sensibler Bereiche vor der Indexierung**. Interne Suchergebnisse, Login-Seiten und Warenkorb-URLs gehören nicht in die [SERP](/glossary/serp). robots.txt hält Bots draußen.
- **Schnellere Entdeckung neuer Inhalte**. Wenn Crawler keine Anfragen an Müllseiten verschwenden, finden sie neue Blogbeiträge und Produktseiten schneller.
- **Entlastung des Servers**. Aggressive Bots können kleine Server in die Knie zwingen. Unnötiges Crawlen zu blockieren spart Ressourcen.

Wer regelmäßig publiziert. Egal ob 5 Seiten oder 30 Artikel pro Monat. Der braucht Crawler, die ihre Zeit auf den richtigen URLs verbringen.

## So funktioniert die robots.txt

Die Syntax ist denkbar einfach. Drei Kerndirektiven decken die meisten Anwendungsfälle ab.

### User-agent

Diese Zeile gibt an, für welchen Crawler die Regel gilt. `User-agent: *` adressiert alle Bots. `User-agent: Googlebot` nur Googles Crawler. Sie können mehrere Regeln für verschiedene Bots in derselben Datei stapeln.

### Disallow

Die `Disallow`-Anweisung sperrt einen bestimmten Pfad. `Disallow: /admin/` verhindert, dass Crawler etwas unterhalb des /admin/-Verzeichnisses aufrufen. Lassen Sie sie leer (`Disallow:`), erlauben Sie alles. Ein einzelner Schrägstrich (`Disallow: /`) blockiert die gesamte Site.

### Allow und Sitemap

`Allow` hebt eine umfassendere Disallow-Regel für einzelne Pfade auf. Praktisch, wenn Sie ein Verzeichnis sperren, aber eine Seite darin freigeben wollen. Die `Sitemap`-Direktive verweist Crawler auf Ihre [XML-Sitemap](/glossary/xml-sitemap), damit sie alle wichtigen URLs finden, ohne raten zu müssen.

### Wie Google die Datei verarbeitet

Googlebot ruft Ihre robots.txt ab, bevor er irgendetwas anderes crawlt. Liefert die Datei einen 200-Status, hält sich Google an die Regeln. Eine 404 bedeutet „keine Einschränkungen". Alles wird gecrawlt. Ein 5xx-Fehler macht Google vorsichtig und drosselt das Crawling, bis die Datei wieder erreichbar ist.

## Arten von robots.txt-Direktiven

robots.txt-Direktiven lassen sich in 4 Hauptkategorien einteilen:

- **Zugriffsdirektiven (Allow/Disallow)**. Sie regeln, welche Pfade Bots aufrufen dürfen. Die Grundlage jeder robots.txt.
- **User-agent-Direktiven**. Sie richten Regeln gezielt an einzelne Bots. Sie könnten SemrushBot blockieren, während Googlebot vollen Zugriff erhält.
- **Crawl-delay-Direktiven**. Sie weisen Bots an, zwischen Anfragen zu warten. Google ignoriert das (nutzen Sie stattdessen die Google Search Console), aber Bing und Yandex respektieren es.
- **Sitemap-Direktiven**. Sie verweisen auf Ihre Sitemap-Datei. Technisch keine „Regel", sondern ein Discovery-Mechanismus, auf den sich Bots verlassen.

Die meisten kleinen und mittelgroßen Sites brauchen nur Zugriffsdirektiven und einen Sitemap-Verweis. Crawl-delay wird erst bei großen Sites mit Server-Engpässen relevant.

## Beispiele für robots.txt

**Beispiel 1: Lokaler Klempnerbetrieb**
Ein Klempner in München betreibt eine WordPress-Site mit den Verzeichnissen /wp-admin/, /warenkorb/ und /interne-preise/. Seine robots.txt sperrt alle drei und enthält einen Sitemap-Verweis. Ergebnis: Googlebot verbringt seine Zeit auf Leistungs- und Blogseiten. Nicht im Admin-Panel.

**Beispiel 2: Online-Shop mit Filterseiten**
Ein Onlinehändler hat 50 Produkte, aber 3.000 Filterkombinationen (Größe + Farbe + Preis). Ohne ein Disallow für `/produkte?filter=` verschwendet Googlebot [Crawl-Budget](/glossary/crawl-budget) auf duplizierte Filterseiten. Eine einzige Disallow-Zeile löst das Problem.

**Beispiel 3: Versehentliche Sperrung der gesamten Site**
Eine Marketingagentur ging vom Staging in die Produktion und ließ `Disallow: /` in der robots.txt stehen. Drei Wochen lang wurde nichts mehr [indexiert](/glossary/indexing). Der Traffic fiel auf null. Ein einzelnes Zeichen war schuld. Der Schrägstrich nach Disallow.

## robots.txt vs. Meta-Robots-Tag

Beide erledigen unterschiedliche Aufgaben in unterschiedlichen Phasen. Die robots.txt stoppt Crawler, bevor sie eine Seite erreichen. Das [Meta-Robots-Tag](/glossary/meta-robots-tag) gibt Anweisungen, nachdem ein Crawler die Seite bereits aufgerufen hat.

| | robots.txt | Meta-Robots-Tag |
|---|---|---|
| **Wo es liegt** | Datei im Stammverzeichnis | HTML-`<head>` einzelner Seiten |
| **Wann es greift** | Vor dem Crawling | Nach dem Crawling |
| **Geltungsbereich** | Ganze Verzeichnisse oder Pfade | Einzelne Seiten |
| **Verhindert Indexierung?** | Nein. Nur Crawling | Ja, `noindex` entfernt aus der Suche |
| **Am besten für** | Sperren von Site-Bereichen | Einzelne Seiten aus der Suche entfernen |

Hier liegt der Haken: Sperren Sie eine Seite per robots.txt, kann Google ein noindex-Tag auf dieser Seite nicht sehen. Die Seite kann also trotzdem in den Suchergebnissen auftauchen (ohne Snippet), weil Google einen Link von außen gefunden hat. Wer eine Seite wirklich aus der Suche entfernen will, nutzt das Meta-Robots-Tag. Nicht die robots.txt.

## Best Practices für die robots.txt erstellen

- **Immer eine Sitemap-Direktive einfügen**. Verweisen Sie auf Ihre [XML-Sitemap](/glossary/xml-sitemap), damit Crawler eine vollständige Karte Ihrer Site haben. Eine Zeile genügt: `Sitemap: https://ihre-seite.de/sitemap.xml`.
- **Niemals CSS- oder JavaScript-Dateien sperren**. Google muss Ihre Seiten rendern, um sie zu verstehen. Diese Ressourcen zu blockieren schadet Ihrer [OnPage-SEO](/glossary/on-page-seo).
- **Vor dem Deployment testen**. Nutzen Sie den robots.txt-Tester der Google Search Console, um Ihre Regeln zu prüfen. Ein Tippfehler kann Ihre gesamte Site sperren.
- **Vierteljährlich überprüfen**. Mit dem Wachstum Ihrer Site entstehen neue Verzeichnisse. Was vor 6 Monaten sinnvoll war, blockiert heute vielleicht wichtige Inhalte.
- **Mit einer Content-Strategie kombinieren**. Die robots.txt steuert, was gecrawlt wird – aber Sie brauchen trotzdem Seiten, die das Crawlen wert sind. Dienste wie theStacc veröffentlichen 30 SEO-optimierte Artikel pro Monat und liefern Googlebot bei jedem Besuch frische Inhalte.

## Häufig gestellte Fragen

### Verhindert robots.txt das Erscheinen in Google?

Nicht direkt. robots.txt verhindert das Crawling, nicht die [Indexierung](/glossary/indexing). Verlinken andere Seiten auf eine gesperrte URL, kann Google sie weiterhin anzeigen. Nur eben ohne Beschreibungs-Snippet. Für die vollständige Entfernung aus der Suche brauchen Sie ein noindex-Meta-Tag.

### Wo lege ich die robots.txt ab?

Platzieren Sie sie im Stammverzeichnis Ihrer Domain: `https://ihre-seite.de/robots.txt`. In Unterverzeichnissen funktioniert die Datei nicht. Jede Subdomain braucht eine eigene robots.txt.

### Kann robots.txt meine Rankings verbessern?

Indirekt, ja. Wer minderwertige Seiten sperrt, schont das Crawl-Budget für wichtige Inhalte. Auf großen Sites bedeutet das schnellere Entdeckung und Indexierung neuer Seiten. Was wiederum die Ranking-Verbesserung beschleunigen kann.

### Halten sich alle Bots an robots.txt?

Seriöse Suchmaschinen-Bots (Googlebot, Bingbot) respektieren die robots.txt. Schädliche Bots und Scraper ignorieren sie meist. Verlassen Sie sich nicht auf robots.txt als Sicherheitslösung. Sie ist eine Richtlinie, keine Firewall.

---

Wollen Sie sicherstellen, dass Ihre SEO-Inhalte auch wirklich gecrawlt und gerankt werden? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Robots.txt-Spezifikationen](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central: Wie Google die robots.txt interpretiert](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz: Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs: Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
