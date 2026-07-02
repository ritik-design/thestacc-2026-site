---
term: "hreflang"
slug: "hreflang"
definition: "hreflang ist ein HTML-Attribut, das Suchmaschinen mitteilt, welche Sprach- und Länderversion einer Seite jeweils ausgeliefert werden soll – ohne doppelte Inhalte."
category: "SEO"
difficulty: "Advanced"
keyword: "hreflang Tag"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## Was ist hreflang?

hreflang ist ein HTML-Attribut (`rel="alternate" hreflang="x"`), das Google und anderen Suchmaschinen signalisiert, auf welche Sprache und welches Land eine bestimmte Seitenversion abzielt.

Wer eine Website mit mehreren Sprachen oder regionalen Varianten betreibt – etwa Englisch für die USA und Englisch für Großbritannien –, verhindert mit einem korrekten hreflang Tag, dass Google die Seiten als [Duplicate Content](/glossary/duplicate-content) interpretiert. Ohne diese Auszeichnung wählt Google eine Version aus und zeigt sie weltweit an. Selten die richtige.

Eine Ahrefs-Studie hat ergeben, dass nur 19 % der mehrsprachigen Websites hreflang korrekt umsetzen. Bei den restlichen 81 % treten Fehler auf – von fehlenden Rückverweisen bis zu defekten URLs. Es ist eines der am häufigsten falsch konfigurierten Elemente im technischen SEO.

## Warum ist hreflang wichtig?

Eine saubere hreflang Implementation entscheidet darüber, ob die richtige Zielgruppe die richtige Seite zu sehen bekommt.

- **Korrekte Sprachauslieferung**. Nutzer in Frankreich sehen die französische Version, Nutzer in Deutschland die deutsche – ohne manuelle Weiterleitungen oder JavaScript-Tricks
- **Schutz vor Duplicate-Content-Filterung**. Google erkennt, dass Ihre `/en/`- und `/de/`-Seiten keine Duplikate sind, sondern bewusste Übersetzungen
- **Bessere Nutzererfahrung**. Wer eine Seite in seiner Muttersprache aufruft, bleibt länger und konvertiert eher
- **Regionale Preise und Inhalte**. E-Commerce-Shops mit länderspezifischen Preisen oder Produkten brauchen hreflang, damit in jedem Markt die passende Version erscheint

Jedes Unternehmen, das in mehreren Ländern oder Sprachen aktiv ist, kommt um hreflang nicht herum. Punkt.

## So funktioniert hreflang

### Implementierungsmethoden

Es gibt drei Wege, hreflang zu implementieren: HTML-Link-Tags im `<head>`, HTTP-Header (für PDFs und andere Nicht-HTML-Dateien) oder Einträge in Ihrer [XML-Sitemap](/glossary/xml-sitemap). Google empfiehlt, sich auf eine Methode festzulegen. Bei großen Sites mit Hunderten von Sprachvarianten ist die Sitemap-Variante meist am pflegeleichtesten.

### Die Regel des Rückverweises

Jede hreflang-Annotation muss bidirektional sein. Sagt Seite A „meine französische Entsprechung ist Seite B", muss Seite B im Gegenzug sagen „meine englische Entsprechung ist Seite A". Fehlende Rückverweise sind der Implementierungsfehler Nummer eins. Ohne sie ignoriert Google die Annotation komplett.

### Das x-default-Tag

Der hreflang-Wert `x-default` weist Google an, welche Version ausgespielt werden soll, wenn keine spezifische Sprach- oder Länderkombination passt. Ihr Fallback. Üblicherweise die englische Version oder die Ihres Hauptmarktes. Ohne `x-default` rät Google – und rät nicht immer richtig.

## hreflang-Beispiele

**Beispiel 1: Ein Online-Shop mit Versionen für Deutschland und Österreich**
Ein Modehändler aus München führt `example.com/de-de/schuhe` (Preise in Euro, deutsche MwSt.) und `example.com/de-at/schuhe` (Preise in Euro, österreichische MwSt., abweichende Versandkosten). Ohne hreflang Tag könnte Google österreichischen Suchenden die deutsche Version zeigen. Mit korrekter Auszeichnung sieht jede Zielgruppe die richtigen Preise und Versandinformationen. Die [Canonical URL](/glossary/canonical-url) bleibt für jede Version eigenständig.

**Beispiel 2: Ein SaaS-Anbieter mit übersetzten Seiten**
Ein Projektmanagement-Tool hat seine Startseite in 8 Sprachen. Das Team setzt hreflang über die XML-Sitemap um, jede Sprachvariante verweist auf alle anderen. Deutsche Suchende landen auf `/de/`, spanische auf `/es/`, alle übrigen auf der englischen `x-default`-Version.

Möchten Sie internationale Inhalte ausspielen, ohne sich um die hreflang-Verdrahtung zu kümmern? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Häufig gestellte Fragen

### Wirkt sich hreflang auf das Ranking aus?

hreflang verbessert Rankings nicht direkt. Es entscheidet, welche Version in welchem Markt erscheint. Doch wer die passende Sprache an die passende Zielgruppe ausliefert, verbessert Engagement-Signale wie Absprungrate und [Verweildauer](/glossary/dwell-time). Diese können Rankings indirekt beeinflussen.

### Funktioniert hreflang für dieselbe Sprache in verschiedenen Ländern?

Ja. Genau dafür ist hreflang gemacht. Englisch für die USA (`en-us`), Englisch für UK (`en-gb`) und Englisch für Australien (`en-au`) lassen sich getrennt auszeichnen. Google nutzt nicht nur den Sprachcode, sondern auch den Ländercode, um die passende Version zu wählen.

### Was passiert bei fehlerhafter Implementierung?

Google ignoriert die Annotationen vollständig und entscheidet selbst, welche Version ausgespielt wird. Keine Strafe. Nur verlorene Kontrolle über den jeweiligen Markt. Der Bericht „Internationale Ausrichtung" in der Google Search Console zeigt hreflang-Fehler im Detail.

---

Möchten Sie internationale Suchsichtbarkeit, ohne für jeden Markt ein eigenes Content-Team aufzubauen? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: hreflang-Implementierung](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs: Leitfaden zu hreflang Tags](https://ahrefs.com/blog/hreflang-tags/)
- [Moz: Der ultimative Leitfaden zu hreflang](https://moz.com/learn/seo/hreflang-tag)
