---
term: "Indexierung"
slug: "indexing"
definition: "Indexierung ist der Prozess, bei dem Webseiten in die Datenbank einer Suchmaschine aufgenommen werden. Erfahren Sie, wie Indexierung funktioniert, wie Sie indexierte Seiten prüfen und Probleme beheben."
category: "SEO"
difficulty: "Beginner"
keyword: "Indexierung"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "google-search-console"
  - "xml-sitemap"
  - "noindex"
  - "de-index"
---

## Was ist Indexierung?

Indexierung ist der Prozess, bei dem Google den Inhalt einer Webseite in seiner riesigen Datenbank speichert, organisiert und katalogisiert, damit er abgerufen und gerankt werden kann, wenn jemand eine relevante Anfrage sucht.

Nachdem Googlebot eine Seite [gecrawlt](/glossary/crawling) hat – die URL besucht und ihren Inhalt gelesen – sendet er diese Informationen zurück an Googles Server. Indexierung ist, was als Nächstes passiert. Google analysiert den Inhalt, bestimmt, welche Themen und [Keywords](/glossary/keyword) die Seite abdeckt, und legt sie an der entsprechenden Stelle innerhalb seines Index ab. Ohne Indexierung ist Ihre Seite für Suchende unsichtbar, egal wie gut sie ist.

Googles Index enthält Hunderte Milliarden Seiten und ist über 100 Millionen Gigabyte groß. Aber hier ist der Teil, der die Leute auf dem falschen Fuß erwischt: Google crawlt weit mehr Seiten, als es indexiert. 2023 bestätigte Googles eigene Dokumentation, dass „nicht alle Seiten, die gecrawlt werden, indexiert werden." Gecrawlt zu werden ist Schritt eins. Indexiert zu werden ist, wo die echte Arbeit passiert.

## Warum ist Indexierung wichtig?

Kein Index = keine Rankings = kein [organischer Traffic](/glossary/organic-traffic). So einfach ist das.

- **Es ist die Voraussetzung für Rankings**. Ihre Seite kann nur in Suchergebnissen erscheinen, wenn sie in Googles Index ist. Alles andere – Inhaltsqualität, [Backlinks](/glossary/backlinks), [OnPage-SEO](/glossary/on-page-seo) – ist irrelevant, wenn die Seite nicht indexiert ist.
- **Indexierung ist nicht automatisch**. Google ist zunehmend selektiv. Der Status „Gecrawlt – aktuell nicht indexiert" in der [Google Search Console](/glossary/google-search-console) ist eines der häufigsten SEO-Probleme geworden und betrifft Sites jeder Größe.
- **Geschwindigkeit der Indexierung beeinflusst Wettbewerbsfähigkeit**. Bei zeitlich relevanten Inhalten (Nachrichten, Events, Trending-Themen) kann der Unterschied, in Stunden statt Wochen indexiert zu werden, den Unterschied zwischen Traffic-Erfassung und verpasstem Fenster bedeuten.
- **Index-Bloat verschwendet Ressourcen**. Zu viele minderwertige Seiten in Googles Index verwässern die Gesamtqualitätssignale Ihrer Site und können Rankings für Ihre wichtigen Seiten potenziell nach unten ziehen.

Für Unternehmen, die regelmäßig Inhalte veröffentlichen, ist das Verständnis von Indexierung essentiell. Wenn Sie 30 Artikel pro Monat veröffentlichen, aber nur 20 indexiert werden, lassen Sie 33 % Ihrer Investition liegen.

## Wie Indexierung funktioniert

Indexierung ist ein mehrstufiger Prozess, der nach dem [Crawling](/glossary/crawling), aber vor dem Ranking stattfindet.

### Inhaltsverarbeitung

Wenn Googlebot den Inhalt einer Seite zurück an Googles Server sendet, analysiert das Indexierungssystem alles: den Text, [Überschriften-Tags](/glossary/heading-tags), Bilder, Links, [Schema Markup](/glossary/schema-markup) und Metadaten. Google bestimmt, in welcher Sprache der Inhalt ist, welche Themen er abdeckt und wie er sich zu anderen Seiten Ihrer Site und im Web verhält.

### Qualitätsbewertung

Nicht jede gecrawlte Seite schafft es in den Index. Google bewertet, ob der Inhalt einzigartig, nützlich und substantiell genug ist, um eine Aufnahme zu rechtfertigen. Dünner Inhalt, exakter [doppelter Inhalt](/glossary/duplicate-content) und Seiten, die keinen Mehrwert zu dem hinzufügen, was bereits im Index ist, werden möglicherweise gecrawlt, aber absichtlich ausgeschlossen.

### Index-Speicherung

Seiten, die die Qualitätsprüfung bestehen, werden in Googles Index gespeichert, zusammen mit allen Signalen, die später für das Ranking verwendet werden. Textinhalt, Linkbeziehungen, strukturierte Daten, Aktualitätssignale und Page-Experience-Daten. Der Index wird ständig aktualisiert, während Seiten neu gecrawlt und neu bewertet werden.

### Rendering (für JavaScript-Sites)

Seiten, die für das Rendering auf JavaScript angewiesen sind, durchlaufen einen zusätzlichen Schritt. Googlebot indexiert zuerst das rohe HTML, rendert dann später das JavaScript, um den endgültigen Inhalt zu sehen. Dieser „Two-Wave-Indexing"-Prozess bedeutet, dass [JavaScript-lastige Sites](/glossary/javascript-seo) Verzögerungen erleben können. Manchmal Wochen. Bevor ihr vollständiger Inhalt indexiert ist.

## Arten von Indexierungsstatus

Die Google Search Console meldet Seiten unter mehreren Indexierungskategorien:

- **Indexiert**. Die Seite ist in Googles Index und berechtigt, in Suchergebnissen zu erscheinen. Das ist das Ziel.
- **Gecrawlt – aktuell nicht indexiert**. Google hat die Seite gefunden und gelesen, sich aber entschieden, sie nicht aufzunehmen. Üblicherweise ein Inhaltsqualitätsproblem. Das ist der Status, den SEOs am meisten fürchten.
- **Gefunden – aktuell nicht gecrawlt**. Google weiß, dass die URL existiert (in einer Sitemap oder einem Link gefunden), hat sie aber noch nicht besucht.
- **Durch Noindex-Tag ausgeschlossen**. Die Seite hat eine [Noindex](/glossary/noindex)-Direktive, die Google anweist, sie nicht aufzunehmen. Das ist beabsichtigt für Seiten wie Danke-Seiten oder interne Suchergebnisse.
- **Duplikat – Eingereichte URL nicht als kanonisch ausgewählt**. Google hat die Seite gefunden, hält aber eine andere URL für die [kanonische](/glossary/canonical-url) Version, sodass nur diese indexiert wird.
- **Durch robots.txt blockiert**. Google kann die Seite nicht crawlen, weil [robots.txt](/glossary/robots-txt) sie blockiert, sodass eine Indexierung unmöglich ist.

Diese Status regelmäßig in der GSC zu prüfen, ist der schnellste Weg, Indexierungsprobleme zu erkennen, bevor sie Sie Traffic kosten.

## Beispiele für Indexierung

**Beispiel 1: Die neue Menüseite eines Restaurants**
Ein lokales Restaurant fügt eine saisonale Menüseite zu seiner Website hinzu. Zwei Wochen später sucht der Inhaber bei Google danach. Nichts. Sie prüfen die [Google Search Console](/glossary/google-search-console) und sehen „Gefunden – aktuell nicht gecrawlt." Die Seite hat keine [internen Links](/glossary/internal-link), die auf sie zeigen, und ist nicht in der Sitemap. Nach dem Hinzufügen eines Links von der Homepage und dem Einreichen der URL in der GSC indexiert Google sie innerhalb von 3 Tagen.

**Beispiel 2: Ein Blog verliert Seiten an „Gecrawlt – nicht indexiert"**
Eine Marketingagentur bemerkt, dass 40 % ihrer Blogbeiträge in der GSC „Gecrawlt – aktuell nicht indexiert" zeigen. Die Beiträge sind 300–400 Wörter generischer Ratschläge ohne originelle Einsichten. Google hat entschieden, dass sie nicht genug Mehrwert hinzufügen. Die Agentur schreibt die schwächsten Beiträge mit mehr Tiefe, Daten und Expertenkommentaren neu. Die Re-Indexierung folgt im nächsten Crawl-Zyklus.

**Beispiel 3: Veröffentlichung in großem Maßstab mit korrekter Indexierung**
Ein Unternehmen für Hausdienstleistungen nutzt theStacc, um 30 Artikel pro Monat zu veröffentlichen. Jeder Artikel wird automatisch zu einer aktualisierten [XML-Sitemap](/glossary/xml-sitemap) hinzugefügt, intern mit verwandten Inhalten verlinkt und mit ausreichend Tiefe geschrieben, um Googles Qualitätsschwelle zu bestehen. Die Indexierungsraten bleiben über 90 %, weil die Grundlagen von Anfang an gehandhabt werden.

## Indexierung vs. Crawling

Diese beiden Schritte sind eng verbunden, lösen aber unterschiedliche Probleme.

| | Indexierung | [Crawling](/glossary/crawling) |
|---|---|---|
| **Was passiert** | Google fügt die Seite seiner suchbaren Datenbank hinzu | Google besucht und liest die Seite |
| **Analogie** | Eine Bibliothekarin stellt ein Buch ins Regal | Eine Bibliothekarin nimmt das Buch in die Hand |
| **Kann unabhängig fehlschlagen** | Ja. Gecrawlte Seiten werden oft nicht indexiert | Ja. Nicht gecrawlte Seiten können nicht indexiert werden |
| **Sie kontrollieren es mit** | Inhaltsqualität, [Noindex](/glossary/noindex)-Tags, kanonischen URLs | [Robots.txt](/glossary/robots-txt), [Sitemap](/glossary/xml-sitemap), interne Links |
| **Status prüfen in** | GSC-Seitenbericht, „site:"-Suchoperator | GSC-Crawl-Statistiken, Server-Logs |
| **Häufiges Problem** | „Gecrawlt – aktuell nicht indexiert" | Seiten von Googlebot nie entdeckt |

Crawling betrifft Zugang. Indexierung betrifft Würdigkeit. Sie brauchen beides, um zu ranken.

## Best Practices für Indexierung

- **Reichen Sie eine XML-Sitemap ein und halten Sie sie aktuell**. Ihre [Sitemap](/glossary/xml-sitemap) ist das klarste Signal, das Sie senden können, welche Seiten Sie indexiert haben möchten. Reichen Sie sie über die Google Search Console ein und aktualisieren Sie sie automatisch, wann immer Sie Inhalte veröffentlichen oder entfernen.
- **Bauen Sie interne Links zu jeder wichtigen Seite**. Seiten ohne [interne Links](/glossary/internal-link) (verwaiste Seiten) sind für Google schwerer zu entdecken und werden seltener indexiert. Jede Seite sollte innerhalb von 3 Klicks von Ihrer Homepage erreichbar sein.
- **Verbessern Sie dünnen Inhalt, statt mehr zu veröffentlichen**. Wenn Google Ihre Seiten nicht indexiert, hilft mehr veröffentlichen nicht. Beheben Sie zuerst das Qualitätsproblem. Fügen Sie Tiefe, originelle Einsichten und Daten zu bestehenden Seiten hinzu.
- **Verwenden Sie das URL-Inspection-Tool für vorrangige Seiten**. Nach dem Veröffentlichen einer wichtigen Seite fordern Sie die Indexierung direkt über die GSC an. Das kann die Indexierung von Wochen auf Tage beschleunigen. theStaccs Veröffentlichungs-Workflow ist darauf ausgelegt, die Indexierungsgeschwindigkeit zu maximieren. Mit korrekten Sitemaps, interner Verlinkung und Inhaltstiefe in jedem Artikel.
- **Überwachen Sie Indexierungsraten monatlich**. Verfolgen Sie das Verhältnis von indexierten zu eingereichten Seiten in der GSC. Eine sinkende Indexierungsrate ist ein frühes Warnzeichen, dass Google das Vertrauen in Ihre Inhaltsqualität verliert.

## Häufig gestellte Fragen

### Wie lange dauert die Indexierung?

Bei etablierten Sites mit guter Autorität werden neue Seiten typischerweise innerhalb von 2–7 Tagen indexiert. Brandneue Sites können 2–4 Wochen warten. Sie können es beschleunigen, indem Sie die URL in der Google Search Console einreichen und sicherstellen, dass sie von bestehenden indexierten Seiten verlinkt ist.

### Warum wird meine Seite nicht indexiert?

Die häufigsten Gründe: dünner oder doppelter Inhalt, versehentlich gesetztes Noindex-Tag, durch robots.txt blockierte Seite, Seite hat keine internen oder externen eingehenden Links oder der Inhalt fügt nicht genug einzigartigen Wert zu dem hinzu, was bereits in Googles Index ist. Prüfen Sie den Seitenbericht in der [Google Search Console](/glossary/google-search-console) für den spezifischen Grund.

### Wie überprüfe ich, ob eine Seite indexiert ist?

Zwei schnelle Methoden: Suchen Sie `site:ihresite.com/seite-url` bei Google, um zu sehen, ob sie erscheint, oder verwenden Sie das URL-Inspection-Tool in der Google Search Console für eine endgültige Antwort mit Details zum Indexierungsstatus.

### Kann ich eine Seite aus Googles Index entfernen?

Ja. Fügen Sie ein [Noindex](/glossary/noindex)-Meta-Tag zur Seite hinzu, verwenden Sie das Removals-Tool in der Google Search Console für temporäre Entfernung, oder [de-indexieren](/glossary/de-index) Sie sie, indem Sie einen 404- oder 410-Statuscode zurückgeben. Die Noindex-Methode ist die zuverlässigste für eine permanente Entfernung.

---

Möchten Sie jeden Artikel ohne manuellen Aufwand indexiert und rankend? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Wie Suchindexierung funktioniert](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Google Search Central: URL-Inspection-Tool](https://support.google.com/webmasters/answer/9012289)
- [Google Search Central: Warum Seiten möglicherweise nicht indexiert werden](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)
- [Ahrefs: So bekommt man Google dazu, Ihre Site zu indexieren](https://ahrefs.com/blog/google-index/)
- [Moz: Anfängerleitfaden zu SEO. Crawling und Indexierung](https://moz.com/beginners-guide-to-seo/how-search-engines-operate)
