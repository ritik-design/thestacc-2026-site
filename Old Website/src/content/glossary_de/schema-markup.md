---
term: "Schema Markup"
slug: "schema-markup"
definition: "Schema Markup ist standardisierter Code (meist JSON-LD), den Sie in Webseiten einbetten, damit Suchmaschinen Ihre Inhalte verstehen und Rich Results ausspielen."
category: "SEO"
difficulty: "Intermediate"
keyword: "strukturierte Daten"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "rich-results"
  - "serp"
  - "technical-seo"
  - "json-ld"
  - "e-e-a-t"
---

## Was ist Schema Markup?

**Schema Markup ist ein Vokabular für strukturierte Daten, das Sie in Ihr HTML einfügen, um Suchmaschinen exakt zu sagen, was Ihr Inhalt darstellt – ein Produkt, ein Rezept, ein Event, ein Unternehmen, eine FAQ.**

Ohne Schema muss Google raten, worum es auf Ihrer Seite geht. Mit Schema reichen Sie Google ein beschriftetes Diagramm. Das Markup folgt dem Schema.org-Standard, der gemeinsam von Google, Microsoft, Yahoo und Yandex gepflegt wird.

Eine Studie von Milestone Research hat gezeigt, dass Seiten mit Schema Markup im Schnitt 4 Positionen höher ranken als Seiten ohne. Nicht weil Schema ein direkter Rankingfaktor wäre – Google hat das ausdrücklich verneint. Aber [Rich Results](/glossary/rich-results), die durch Schema entstehen, heben die Klickrate massiv an, und höhere CTR beeinflusst Rankings über die Zeit.

## Warum sind strukturierte Daten wichtig?

Die meisten Websites verzichten noch immer auf Schema. Eine Chance für jeden, der bereit ist, 30 Minuten in die Implementierung zu investieren.

- **Rich Results in der Suche**. Sternebewertungen, FAQ-Aufklapper, Preisspannen und Eventdaten erscheinen direkt in der [SERP](/glossary/serp). Diese auffälligen Elemente können die CTR um 20–30 % steigern.
- **Bessere KI-Sichtbarkeit**. Googles AI Overviews und andere KI-getriebene Sucherlebnisse ziehen sich aus strukturierten Daten. Schema macht Ihre Inhalte für Maschinen leichter zitierbar.
- **Stärkere lokale Präsenz** – [LocalBusiness Schema](/glossary/localbusiness-schema) gibt Öffnungszeiten, Adresse und Bewertungen direkt an Googles Knowledge Panels und das [Local Pack](/glossary/local-pack) weiter.
- **Sprachsuche-tauglich**. Wenn jemand einen Sprachassistenten etwas fragt, helfen strukturierte Daten dabei, Ihre Antwort hochzuholen. FAQ- und How-To-Schema sind hier besonders wertvoll.

Wer in [SEO](/glossary/seo)-Inhalte investiert, aber kein Schema einbaut, verschenkt Sichtbarkeit.

## Wie Schema Markup funktioniert

Schema steckt im HTML Ihrer Seite. Crawler lesen es, validieren es und nutzen es, um angereicherte Suchergebnisse zu erzeugen.

### Das Code-Format

Drei Formate existieren: JSON-LD, Microdata und RDFa. Google empfiehlt JSON-LD. Es ist ein Script-Block, den Sie in den `<head>`-Bereich legen. Er vermischt sich nicht mit Ihrem sichtbaren HTML, lässt sich sauberer pflegen und bricht das Layout nicht.

### Der Validierungsprozess

Nachdem Sie Schema eingefügt haben, zeigt der Bericht „Rich-Suchergebnisse" in der Google Search Console, ob Ihr Markup gültig ist. Fehler – fehlende Pflichtfelder, falsche Typen – verhindern, dass Rich Results erscheinen. Mit Googles Rich Results Test prüfen Sie einzelne URLs, bevor Sie sitewide ausrollen.

### Wie Google es rendert

Googlebot crawlt Ihre Seite, parst das JSON-LD und gleicht es mit bekannten Schema-Typen ab. Wenn alles passt und Ihre Seite den Qualitätsrichtlinien entspricht, erscheint das angereicherte Listing innerhalb weniger Tage bis Wochen in der Suche. Nicht jedes valide Schema löst ein Rich Result aus. Google entscheidet auf Basis von Anfrage-Kontext und Seitenqualität.

## Arten von Schema Markup

Schema.org listet über 800 Typen. Für die meisten Unternehmen decken eine Handvoll davon 90 % der Anwendungsfälle ab:

- **Article Schema**. Sagt Google, dass diese Seite ein Blogpost oder ein Nachrichtenartikel ist. Hilft bei Google Discover und News-Karussells.
- **FAQ Schema**. Fügt aufklappbare Frage-Antwort-Paare direkt in Ihr Suchergebnis ein. Starke Wirkung bei informationalen Anfragen.
- **LocalBusiness Schema**. Liefert Firmennamen, Adresse, Öffnungszeiten und Bewertungen an Google. Pflicht für [Lokales SEO](/glossary/local-seo).
- **Product Schema**. Zeigt Preis, Verfügbarkeit und Bewertungen in der Suche. Im E-Commerce unverzichtbar.
- **How-To Schema**. Stellt Schritt-für-Schritt-Anleitungen mit Bildern in den Suchergebnissen dar. Funktioniert gut für Tutorial-Inhalte.
- **Review/Rating Schema**. Die gelben Sterne unter Ihren Suchtreffern. Steigert die CTR deutlich.

Welches Schema das richtige ist, hängt vom Seitentyp ab. Die Service-Seite eines Klempners braucht LocalBusiness. Ein Blogpost braucht Article und gegebenenfalls FAQ.

## Beispiele für Schema Markup

**Beispiel 1: Zahnarztpraxis mit FAQ-Schema**
Eine Zahnärztin in München fügt FAQ-Schema mit fünf typischen Patientenfragen auf ihrer Service-Seite „Bleaching" ein. Ihr Suchergebnis zeigt jetzt aufklappbare Q&A-Paare und nimmt das Dreifache des sichtbaren Platzes der Konkurrenz ein. Die Klicks auf diese Seite steigen in 2 Monaten um 35 %.

**Beispiel 2: Heizungsbauer mit LocalBusiness-Schema**
Ein Heizungs- und Klimabetrieb ergänzt LocalBusiness-Schema mit Servicegebiet, Öffnungszeiten und Gesamtbewertung (4,8 Sterne aus über 200 Rezensionen). Google zeigt die Sternebewertung direkt in den organischen Treffern – nicht nur im Map Pack. Das Unternehmen verzeichnet einen spürbaren Anstieg an Anrufen aus der organischen Suche.

**Beispiel 3: SaaS-Blog mit Article-Schema**
Ein B2B-Software-Anbieter veröffentlicht wöchentlich How-To-Guides. Nachdem das Team Article-Schema mit Autoreninfo und Veröffentlichungsdaten einbaut, tauchen die Beiträge in Google Discover auf. Allein der Discover-Traffic addiert 15 % auf die monatlichen organischen Besuche.

## Schema Markup vs. Rich Snippets

Beide Begriffe werden synonym genutzt. Das sollten sie nicht.

| | Schema Markup | Rich Snippets / Rich Results |
|---|---|---|
| **Was es ist** | Code, den Sie in Ihre Seiten einbauen | Angereicherte Suchergebnisse, die Google ausspielt |
| **Wer kontrolliert es** | Sie (der Webmaster) | Google (entscheidet, ob es angezeigt wird) |
| **Garantiert?** | Markup können Sie immer einbauen | Google kann Rich Results zeigen oder eben nicht |
| **Zweck** | Bedeutung der Seite an Crawler kommunizieren | Optische Darstellung in [SERPs](/glossary/serp) verbessern |
| **Beispiel** | JSON-LD-Skript in Ihrem HTML | Sternebewertungen unter Ihrem Treffer |

Schema Markup ist der Input. Rich Results sind das (mögliche) Output. Markup einzubauen garantiert kein angereichertes Listing. Aber ohne Markup bekommen Sie nie eines.

## Best Practices für strukturierte Daten

- **Mit dem Wichtigsten anfangen**. Versuchen Sie nicht, jeden Schema-Typ auf einmal einzubauen. Lokales Unternehmen? Starten Sie mit LocalBusiness und FAQ. Den Rest ergänzen Sie nach und nach.
- **JSON-LD nutzen, nicht Microdata**. Google bevorzugt es. Es ist einfacher zu implementieren, leichter zu debuggen und verkleidert Ihr HTML nicht.
- **Jede Seite validieren**. Schicken Sie neues Schema vor der Veröffentlichung durch Googles Rich Results Test. Ein fehlendes Feld kann den ganzen Block ungültig machen.
- **Schema aktuell halten**. Ändern sich Öffnungszeiten, ändern Sie das Schema. Falsche strukturierte Daten verstoßen gegen Googles Richtlinien und können dazu führen, dass Rich Results entzogen werden.
- **Schema mit hochwertigen Inhalten kombinieren**. Schema auf dünnen Seiten erzeugt keine Rich Results. Dienste wie theStacc veröffentlichen monatlich 30 SEO-optimierte Artikel. Jeder einzelne ist eine Gelegenheit, Article- und FAQ-Schema einzusetzen, das tatsächlich Rich Results verdient.

## Häufig gestellte Fragen

### Sind strukturierte Daten ein Rankingfaktor?

Google sagt: Schema ist kein direkter Rankingfaktor. Aber Seiten mit Schema bekommen [Rich Results](/glossary/rich-results), die die CTR steigern. Höhere CTR sendet positive Engagement-Signale, was Rankings indirekt verbessern kann.

### Wie füge ich Schema auf meiner Website ein?

Der einfachste Weg ist JSON-LD – ein Script-Block im `<head>`-Bereich der Seite. WordPress-Plugins wie Yoast und RankMath generieren ihn automatisch. Für individuelle Sites nutzen Sie Googles Structured Data Markup Helper.

### Funktioniert Schema auch für kleine Unternehmen?

Absolut. Lokale Unternehmen sehen oft den größten Effekt, weil LocalBusiness- und FAQ-Schema bei kleinen Wettbewerbern selten genutzt werden. Basis-Schema auf einer 10-seitigen lokalen Site ist in unter einer Stunde gesetzt.

### Wie lange dauert es bis zu Rich Results?

Nach dem Einbau gültigen Schemas verarbeitet Google es in der Regel innerhalb weniger Tage bis 2 Wochen. Den Status verfolgen Sie im Bericht „Rich-Suchergebnisse" der Google Search Console.

---

Sie wollen SEO-Inhalte optimiert und veröffentlicht – ohne selbst einen Finger zu rühren? theStacc publiziert jeden Monat 30 Artikel auf Ihrer Website. Automatisch. [Für 1 $ starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: So funktionieren strukturierte Daten](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
- [Milestone Research: Wirkung von Schema Markup auf Rankings](https://www.milestoneinternet.com/thought-leadership/research/schema-markup-drives-results)
- [Moz: Der Anfängerleitfaden zu strukturierten Daten](https://moz.com/blog/beginners-guide-to-structured-data)
