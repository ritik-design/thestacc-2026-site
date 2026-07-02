---
term: "Canonical URL / Kanonisierung"
slug: "canonical-url"
definition: "Eine Canonical URL teilt Suchmaschinen mit, welche Version einer Seite die Hauptkopie ist. Erfahren Sie, wie Kanonisierung Probleme mit doppeltem Inhalt verhindert und wie Sie sie korrekt einsetzen."
category: "SEO"
difficulty: "Intermediate"
keyword: "Canonical URL"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "301-redirect"
  - "indexing"
  - "crawl-budget"
  - "technical-seo"
---

## Was ist eine Canonical URL?

Eine Canonical URL ist ein HTML-Element, das Suchmaschinen mitteilt, welche Version einer Seite die bevorzugte, autoritative Kopie ist, wenn mehrere URLs denselben oder sehr ähnlichen Inhalt liefern.

Im `<head>` einer Seite sieht es so aus: `<link rel="canonical" href="https://example.com/preferred-page">`. Warum existiert das? Weil im modernen Web ein einzelner Inhalt oft unter mehreren URLs lebt. Dieselbe Produktseite ist mit und ohne www erreichbar, mit und ohne abschließenden Schrägstrich, mit Tracking-Parametern, durch gefilterte Navigation. Google sieht jede URL als separate Seite. Ohne Canonical-Tag muss Google raten, welche indexiert werden soll. Und es rät oft falsch.

Daten von Semrush aus einer Studie von 150.000 Websites zeigen, dass 65 % der Domains irgendeine Form von Problem mit [doppeltem Inhalt](/glossary/duplicate-content) haben. Canonical-Tags sind das wichtigste Werkzeug, um dies in großem Maßstab zu lösen, ohne Ihre gesamte Website umstrukturieren zu müssen.

## Warum ist Kanonisierung wichtig?

Doppelter Inhalt ist keine Strafe. Google hat das klar gesagt. Aber er erzeugt echte SEO-Probleme, die Sie Traffic und Rankings kosten.

- **Link-Equity wird aufgesplittet**. Wenn 30 Seiten auf Ihre Seite verlinken, aber die Hälfte auf `example.com/page` und die andere Hälfte auf `example.com/page/`, ist die Autorität geteilt. Ein Canonical konsolidiert alle Signale auf eine URL und macht sie stärker.
- **[Crawl-Budget](/glossary/crawl-budget) wird verschwendet**. Googlebot hat ein begrenztes Crawl-Budget für Ihre Website. Jede doppelte URL, die er crawlt, ist eine Seite, die er nicht gecrawlt hat. Bei großen Sites mit Tausenden Seiten wirkt sich das direkt darauf aus, wie schnell neue Inhalte [indexiert](/glossary/indexing) werden.
- **Die falsche Seite könnte ranken**. Ohne Kanonisierung wählt Google die Version aus, die es für am besten hält. Das könnte Ihre mobile URL sein, eine parameterlastige URL oder eine gefilterte Kategorieseite. Nicht die saubere, optimierte Version, die Sie ranken sehen wollen.
- **Analytics werden fragmentiert**. Traffic- und Engagement-Daten verteilen sich auf mehrere URLs. Ihre tatsächliche Performance sieht schwächer aus, als sie ist, weil die Metriken aufgeteilt sind.

Wenn Ihre Website mehr als eine Handvoll Seiten hat, haben Sie mit ziemlicher Sicherheit doppelte Inhalte, die Kanonisierung beheben würde.

## Wie Kanonisierung funktioniert

Das Canonical-Tag ist ein Hinweis, keine Anweisung. Google respektiert es meist. Aber nicht immer.

### Selbstreferenzierende Canonicals

Jede Seite Ihrer Website sollte ihr Canonical-Tag auf sich selbst zeigen. Das nennt man ein selbstreferenzierendes Canonical. Es teilt Google mit: „Dies ist die bevorzugte URL für diesen Inhalt, auch wenn du sie über einen anderen Pfad entdeckst." Die meisten [CMS-Plattformen](/glossary/content-management-system) und [technischen SEO](/glossary/technical-seo)-Plugins handhaben das automatisch.

### Domain-übergreifende Canonicals

Wenn Sie Inhalte syndizieren – denselben Artikel auf Ihrem Blog und auf Medium oder LinkedIn veröffentlichen – können Sie ein domain-übergreifendes Canonical setzen, das von der syndizierten Version auf Ihr Original zurückzeigt. Damit weisen Sie Google an, die [Link-Equity](/glossary/link-equity) und Rankingsignale Ihrer Domain gutzuschreiben, nicht der syndizierten Kopie.

### Canonical vs. Googles Wahl

Google behandelt Canonical-Tags als starken Hinweis, nicht als Befehl. Wenn das Canonical-Tag mit anderen Signalen kollidiert (Sitemaps, interne Links, Weiterleitungsmuster), kann Google Ihre Präferenz überschreiben. Deshalb ist Konsistenz wichtig. Ihr Canonical, Ihre [internen Links](/glossary/internal-link), Ihre Sitemap und Ihre [301-Weiterleitungen](/glossary/301-redirect) sollten alle auf dieselbe bevorzugte URL zeigen.

### Häufige Variationen von Canonical URLs

Dies sind die häufigsten Szenarien doppelter Inhalte, die Kanonisierung löst:

- `http://` vs. `https://`
- `www.example.com` vs. `example.com`
- `/page` vs. `/page/` (abschließender Schrägstrich)
- `/page` vs. `/page?utm_source=google&utm_medium=cpc`
- `/page` vs. `/page?ref=homepage`
- Mobile URLs (`m.example.com`) vs. Desktop URLs

Jede Variante ist für Google eine separate URL. Canonical-Tags fassen sie zu einer zusammen.

## Arten der Kanonisierung

Es gibt mehrere Möglichkeiten, Ihre bevorzugte URL zu signalisieren. Das Canonical-Tag ist die häufigste, aber nicht die einzige Option.

- **HTML-Canonical-Tag**. Das `<link rel="canonical">`-Tag im `<head>` der Seite. Am flexibelsten, funktioniert auf jeder Seite, leicht zu implementieren.
- **HTTP-Header-Canonical**. Wird als `Link:`-Header in der HTTP-Antwort gesendet. Wird für Nicht-HTML-Dateien (PDFs, Bilder) verwendet, bei denen Sie keine HTML-Tags hinzufügen können.
- **[301-Weiterleitung](/glossary/301-redirect)**. Leitet doppelte URLs dauerhaft zur bevorzugten Version um. Stärker als ein Canonical-Tag, da Nutzer und Bots nur auf die bevorzugte URL zugreifen können.
- **[XML-Sitemap](/glossary/xml-sitemap)-Signale**. Nur Canonical-URLs in Ihre Sitemap aufzunehmen, verstärkt, welche Versionen Sie bevorzugen. Keine direkte Kanonisierungsmethode, aber ein unterstützendes Signal.
- **Konsistenz der internen Verlinkung**. Immer auf dieselbe Version einer URL über Ihre Website zu verlinken, sendet Google ein klares Signal über Ihre bevorzugte Version.

Für die meisten Sites deckt das HTML-Canonical-Tag in Kombination mit konsistenter interner Verlinkung über 90 % der Fälle ab.

## Beispiele für Canonical URLs

**Beispiel 1: Ein Onlineshop mit parameterlastigen URLs**
Die Produktseite eines Bekleidungsgeschäfts liegt unter `/blue-running-shoes`. Aber das Filtern nach Größe erzeugt `/blue-running-shoes?size=10`, und Tracking-Codes fügen `/blue-running-shoes?utm_source=email` hinzu. Alle drei zeigen dasselbe Produkt. Ohne Canonical-Tags könnte Google die Parameter-URL statt der sauberen indexieren. Das Hinzufügen von `<link rel="canonical" href="/blue-running-shoes">` zu allen drei Versionen löst es sofort.

**Beispiel 2: Ein Unternehmen mit mehreren Standorten und doppelten Serviceseiten**
Eine Klempner-Franchise hat Serviceseiten für jede Stadt: `/hamburg/rohrreinigung`, `/berlin/rohrreinigung`, `/muenchen/rohrreinigung`. Der Inhalt ist zu 90 % identisch, nur der Stadtname ist getauscht. Diese Seiten sollten nicht aufeinander kanonisieren (sie zielen auf unterschiedliche [lokale Keywords](/glossary/local-keywords) ab), aber sich jeweils selbst referenzieren. Die echte Lösung besteht darin, jede Seite mit stadtspezifischem Inhalt wirklich einzigartig zu machen. Etwas, das theStacc übernimmt, indem es automatisch standortspezifische Artikel generiert.

**Beispiel 3: Ein Blog, der Inhalte auf Medium syndiziert**
Ein B2B-Unternehmen veröffentlicht seine Blogbeiträge zur zusätzlichen Sichtbarkeit auch auf Medium. Ohne Canonical-Tag könnte Google die Medium-Version statt des Originals ranken. Durch Hinzufügen einer Canonical URL, die auf den Unternehmensblog zurückzeigt, in jedem Medium-Beitrag (Medium unterstützt das in den Einstellungen) fließen alle Rankingsignale zur Originaldomain. [Organischer Traffic](/glossary/organic-traffic) geht zu Ihrer Website, nicht zu Medium.

## Canonical URL vs. 301-Weiterleitung

Beide lösen Probleme mit doppeltem Inhalt. Die richtige Wahl hängt davon ab, ob die doppelte Seite zugänglich bleiben soll.

| | Canonical URL | [301-Weiterleitung](/glossary/301-redirect) |
|---|---|---|
| **Was Nutzer sehen** | Beide Seiten sind zugänglich | Nutzer wird zur bevorzugten Seite gesendet |
| **Signalstärke** | Starker Hinweis (Google kann überschreiben) | Endgültig (erzwungene Weiterleitung) |
| **Verwenden, wenn** | Beide URLs müssen existieren (Parameter, Syndizierung) | Alte URL soll nicht mehr besucht werden |
| **Link-Equity** | Konsolidiert auf Canonical URL | Übergibt ~95–99 % an das Ziel |
| **Beispiel** | Produktseite mit Filterparametern | Alte Blog-URL zu neuer URL-Struktur verschoben |

Wenn die doppelte Seite zugänglich bleiben muss (getrackte URLs, gefilterte Ergebnisse, syndizierte Inhalte), verwenden Sie ein Canonical. Wenn die alte URL tot ist, verwenden Sie eine 301.

## Best Practices für Canonical URLs

- **Selbstreferenzieren Sie jede Seite**. Selbst Seiten ohne Duplikate sollten ein selbstreferenzierendes Canonical-Tag haben. Es ist ein Sicherheitsnetz gegen unerwartete doppelte URLs aus Parametern, Session-IDs oder CMS-Eigenheiten.
- **Verwenden Sie absolute URLs, keine relativen**. Schreiben Sie immer die vollständige URL: `https://example.com/page`. Nicht `/page`. Relative Canonicals können Probleme bei der Auflösung von Protokoll und Domain verursachen.
- **Lassen Sie Canonicals auf indexierbare Seiten zeigen**. Setzen Sie niemals ein Canonical auf eine Seite, die [noindexiert](/glossary/noindex) ist, weitergeleitet wird oder einen [404](/glossary/404-error) zurückgibt. Das verwirrt Google und vereitelt den Zweck.
- **Prüfen Sie Canonicals nach Website-Migrationen**. CMS-Wechsel, Domain-Umzüge und Redesigns brechen häufig Canonical-Tags. Führen Sie nach dem Launch einen Crawl mit Screaming Frog oder Sitebulb durch, um zu überprüfen, dass jede Seite auf das richtige Canonical zeigt.
- **Halten Sie Ihre Signale konsistent**. Ihr Canonical-Tag, Sitemap, interne Links und Hreflang (für internationale Sites) sollten sich alle auf die bevorzugte URL einigen. Wenn Signale kollidieren, trifft Google seine eigene Wahl. Und es ist möglicherweise nicht die, die Sie wollen. theStacc veröffentlicht alle Artikel mit korrekten Canonical-Tags und sauberen URL-Strukturen.

## Häufig gestellte Fragen

### Übergeben Canonical-Tags Link-Equity?

Ja. Google konsolidiert Rankingsignale von doppelten Seiten auf die Canonical URL. Wenn 10 Seiten auf eine Parameter-Version Ihrer Seite verlinken und das Canonical auf die saubere Version zeigt, profitiert die saubere Version von diesen Links.

### Kann ich auf eine andere Domain kanonisieren?

Ja. Domain-übergreifende Canonicals sagen Google, dass der Originalinhalt auf einer anderen Domain lebt. Häufiger Anwendungsfall: Inhalte auf Medium, LinkedIn oder Partner-Seiten syndizieren und dabei Ihre Domain als Canonical-Quelle behalten.

### Was passiert, wenn mein Canonical-Tag falsch ist?

Google ignoriert es möglicherweise. Wenn das Canonical auf eine Seite mit komplett anderem Inhalt zeigt, erkennt Google die Diskrepanz und indexiert die URLs unabhängig. Canonical-Tags funktionieren nur, wenn die Seiten weitgehend ähnlichen Inhalt haben.

### Wie überprüfe ich meine Canonical-Tags?

Quelltext der Seite anzeigen und nach `rel="canonical"` suchen. Oder die [Google Search Console](/glossary/google-search-console) verwenden. Das URL-Inspection-Tool zeigt, welches Canonical Google für eine Seite ausgewählt hat. Wenn Googles gewähltes Canonical von Ihrem abweicht, gibt es einen Konflikt in Ihren Signalen.

---

Möchten Sie jeden Artikel mit korrekten Canonical-Tags, sauberen URLs und automatisch gehandhabter [technischer SEO](/glossary/technical-seo) veröffentlichen? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Doppelte URLs konsolidieren](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Moz: Leitfaden zum Canonical URL Tag](https://moz.com/learn/seo/canonicalization)
- [Ahrefs: Canonical-Tags für SEO](https://ahrefs.com/blog/canonical-tags/)
- [Semrush: Studie zu doppeltem Inhalt](https://www.semrush.com/blog/duplicate-content/)
- [Google Search Console: URL-Inspection-Tool](https://support.google.com/webmasters/answer/9012289)
