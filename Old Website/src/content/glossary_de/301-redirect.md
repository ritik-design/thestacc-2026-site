---
term: "301-Weiterleitung"
slug: "301-redirect"
definition: "Eine 301-Weiterleitung leitet Nutzer und Suchmaschinen dauerhaft von einer URL zu einer anderen weiter. Erfahren Sie, wann Sie 301-Weiterleitungen einsetzen, wie Sie sie implementieren und welche SEO-Auswirkungen sie haben."
category: "SEO"
difficulty: "Intermediate"
keyword: "was ist eine 301-Weiterleitung"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## Was ist eine 301-Weiterleitung?

Eine 301-Weiterleitung ist ein HTTP-Statuscode, der eine URL dauerhaft an eine andere weiterleitet. Er teilt Browsern und Suchmaschinen mit, dass die ursprüngliche Adresse endgültig umgezogen ist.

Wenn Googlebot oder ein Besucher auf eine 301 trifft, wird er automatisch zur neuen URL geschickt. Keine defekte Seite. Keine Sackgasse. Die „301" bezieht sich auf den spezifischen HTTP-Antwortcode. Es ist die Methode des Webs, um zu sagen: „Diese Seite ist dauerhaft an einen neuen Ort umgezogen." Es gibt eine [302-Weiterleitung](/glossary/302-redirect) für temporäre Verschiebungen, aber für [SEO](/glossary/seo) ist die 301 die entscheidende.

Hier ist der Grund, warum das kritisch ist: Moz-Forschungen zeigen, dass 301-Weiterleitungen ungefähr 95–99 % der [Link-Equity](/glossary/link-equity) an die Ziel-URL weitergeben. Das bedeutet, die Ranking-Power, die Ihre alte URL durch [Backlinks](/glossary/backlinks) erworben hat, verschwindet nicht. Sie wird auf die neue Seite übertragen. Wenn Sie 301-Weiterleitungen falsch einsetzen, werfen Sie jahrelang angehäufte Autorität weg.

## Warum ist eine 301-Weiterleitung wichtig?

Jedes Mal, wenn eine URL ohne korrekte Weiterleitung geändert wird, passiert etwas Schlechtes. Rankings, Traffic, Nutzererfahrung. Suchen Sie sich zwei aus.

- **Erhält Suchrankings.** Ohne eine 301 behandelt Google die neue URL als brandneue Seite mit null Autorität. Ihre Rankings verschwinden über Nacht.
- **Überträgt Link-Equity.** Die [Backlinks](/glossary/backlinks), die Sie erworben haben? Eine 301 übergibt ihren Wert an die neue URL. Ohne sie verdampft dieser Link-Juice.
- **Verhindert 404-Fehler.** Nutzer, die die alte URL gespeichert haben oder auf einen externen Link klicken, erhalten eine funktionierende Seite statt eines [404-Fehlers](/glossary/404-error). Bessere Erfahrung, niedrigere [Absprungrate](/glossary/bounce-rate).
- **Konsolidiert doppelten Inhalt.** Mehrere URLs mit demselben Inhalt verwässern Ihre Autorität. 301-Weiterleitungen führen sie zu einer starken Seite zusammen.

Wenn Sie jemals eine Website umgezogen haben, eine URL-Struktur geändert haben oder zwei Seiten zusammengeführt haben, benötigten Sie 301-Weiterleitungen. Sie zu überspringen ist einer der häufigsten und kostspieligsten Fehler im [technischen SEO](/glossary/technical-seo).

## Wie funktioniert eine 301-Weiterleitung?

Der Vorgang dauert Millisekunden, aber so läuft er im Hintergrund ab.

### Der HTTP-Anfragezyklus

Ein Nutzer oder ein Suchmaschinen-Crawler fordert die alte URL an. Der Server antwortet mit HTTP-Statuscode 301 und einem „Location"-Header, der auf die neue URL zeigt. Der Browser fordert dann automatisch die neue URL an. Der Nutzer sieht die endgültige Seite. Er bemerkt die Weiterleitung vielleicht nicht einmal.

### Wie Google 301-Weiterleitungen verarbeitet

Wenn [Googlebot](/glossary/crawling) auf eine 301 trifft, tut er drei Dinge: Er folgt der Weiterleitung zur neuen URL, überträgt die meisten Ranking-Signale der alten Seite auf die neue Seite und entfernt schließlich die alte URL aus seinem Index. Dieser Prozess kann je nachdem, wie häufig Google Ihre Website crawlt, Tage bis Wochen dauern.

### Implementierung auf Server-Ebene vs. Seitenebene

301-Weiterleitungen werden auf Server-Ebene konfiguriert. Nicht in Ihrem HTML. Die gängigsten Methoden:

- **Apache (.htaccess):** `Redirect 301 /alte-seite https://example.com/neue-seite`
- **Nginx:** `rewrite ^/alte-seite$ /neue-seite permanent;`
- **WordPress-Plugins:** Yoast, Redirection oder Rank Math verwalten dies über das Dashboard
- **Cloudflare:** Page Rules oder Bulk Redirects für Domain-Weiterleitungen

Meta-Refresh-Weiterleitungen auf Seitenebene existieren, sind aber langsamer und übertragen Link-Equity weniger zuverlässig. Verwenden Sie immer Server-seitige 301-Weiterleitungen.

## Arten von Weiterleitungen

Das Verstehen der Unterschiede verhindert kostspielige Fehler:

- **301 (Permanent).** Die Seite ist dauerhaft umgezogen. Überträgt ~95–99 % der Link-Equity. Verwenden Sie diese für URL-Änderungen, Domain-Migrationen und Content-Konsolidierung.
- **[302 (Temporär)](/glossary/302-redirect).** Die Seite ist vorübergehend umgezogen. Google überträgt Link-Equity möglicherweise oder auch nicht. Verwenden Sie diese für A/B-Tests, Wartungsseiten oder saisonale Inhalte.
- **307 (Temporär, HTTP/1.1).** Wie 302, aber bewahrt die Anfragemethode strikt (POST bleibt POST). Nur für technische Anwendungsfälle.
- **308 (Permanent, HTTP/1.1).** Wie 301 mit strikter Methodenbewahrung. Wird im SEO-Kontext selten verwendet.
- **Meta Refresh.** HTML-basierte Weiterleitung. Langsam, schlechter SEO-Wert. Vermeiden.

Im Zweifel verwenden Sie eine 301. Sie ist die sichere Wahl für dauerhafte URL-Änderungen.

## 301-Weiterleitung — Beispiele

**Beispiel 1: Ein lokales Unternehmen gestaltet seine Website neu**
Eine Anwaltskanzlei gestaltet ihre Website neu und ändert ihre URL-Struktur von `/leistungen/personenschaden-anwalt` zu `/praxisbereiche/personenschaden`. Ohne eine 301 würde die alte Seite — die für „Personenschaden Anwalt [Stadt]" auf Platz 3 rankst — einen 404 zurückgeben. Mit der Weiterleitung erbt die neue URL die Ranking-Position, und die 47 [Backlinks](/glossary/backlinks), die auf die alte Seite zeigen, funktionieren weiterhin.

**Beispiel 2: Zwei Blogartikel zu einer stärkeren Seite zusammenführen**
Ein Klempnerunternehmen hat zwei dünne Artikel: „Wie man einen undichten Wasserhahn repariert" und „Reparaturanleitung für undichte Wasserhähne". Keiner rankt gut. Sie führen beide zu einem detaillierten Leitfaden auf der stärkeren URL zusammen und leiten die schwächere mit einer 301 weiter. Die kombinierten [Domain-Authority](/glossary/domain-authority)-Signale schieben die zusammengeführte Seite innerhalb von 6 Wochen von Position 12 auf Position 4.

**Beispiel 3: Domain-Migration schiefgelaufen**
Ein E-Commerce-Shop wechselt von altedomain.de zu neuedomain.de, leitet aber nur die Startseite weiter. Die 2.400 Produktseiten und 180 Blogbeiträge geben alle 404-Fehler zurück. Der [organische Traffic](/glossary/organic-traffic) bricht in 2 Wochen um 78 % ein. Jede einzelne URL hätte eine 1:1 301-Weiterleitung gebraucht. Dieser Fehler kostet Monate der Erholung — wenn er schnell bemerkt wird.

## 301-Weiterleitung vs. Canonical-URL

Beide befassen sich mit doppeltem Inhalt, funktionieren aber unterschiedlich.

| | 301-Weiterleitung | [Canonical-URL](/glossary/canonical-url) |
|---|---|---|
| **Was sie tut** | Schickt Nutzer und Bots zu einer neuen URL | Teilt Google mit, welche URL die „Masterversion" ist |
| **Nutzererfahrung** | Nutzer sieht die neue Seite (automatische Weiterleitung) | Nutzer kann weiterhin auf die Originalseite zugreifen |
| **Wann verwenden** | Alte Seite soll nicht mehr existieren | Beide Seiten sollen zugänglich bleiben |
| **Link-Equity** | Überträgt ~95–99 % | Konsolidiert Signale auf Canonical |
| **Beispiel** | Alte Blog-URL zu neuer URL-Struktur umgezogen | Produktseite über 3 verschiedene URLs erreichbar |

Verwenden Sie 301-Weiterleitungen, wenn die alte Seite tot ist. Verwenden Sie Canonicals, wenn beide Seiten existieren müssen, Sie aber möchten, dass Google eine priorisiert.

## Best Practices für 301-Weiterleitungen

- **Jede alte URL einer relevanten neuen URL zuordnen.** Leiten Sie nicht alles auf die Startseite weiter. Leiten Sie jede alte Seite auf ihr nächstes Äquivalent weiter. Google behandelt Massen-Weiterleitungen auf die Startseite als Soft-404s.
- **Bei Website-Migrationen 1:1-Weiterleitungen einrichten.** Crawlen Sie vor dem Launch einer neuen Website die alte, exportieren Sie jede URL und erstellen Sie eine Weiterleitungskarte. Versäumen Sie diesen Schritt, werden Sie beobachten, wie der [organische Traffic](/glossary/organic-traffic) einbricht.
- **Weiterleitungsketten vermeiden.** A > B > C > D verlangsamt den Nutzer, verschwendet [Crawl-Budget](/glossary/crawl-budget) und kann bei jedem Hop Link-Equity verlieren. Jede Weiterleitung sollte direkt auf das Endziel zeigen.
- **Mit der Google Search Console überwachen.** Überprüfen Sie nach der Implementierung von Weiterleitungen den Abdeckungsbericht auf Crawl-Fehler. [Google Search Console](/glossary/google-search-console) zeigt, welche Seiten 404-Fehler zurückgeben, damit Sie fehlende Weiterleitungen schnell erkennen.
- **Weiterleitungen vierteljährlich prüfen.** Alte Weiterleitungen, die auf nicht mehr existierende Seiten zeigen, erzeugen Ketten. Dienste wie theStacc berücksichtigen in jedem veröffentlichten Artikel korrekte URL-Strukturen, aber wenn Sie Inhalte migrieren oder reorganisieren, planen Sie regelmäßige Weiterleitungsprüfungen ein, um alles sauber zu halten.

## Häufig gestellte Fragen

### Schaden 301-Weiterleitungen dem SEO?

Nicht, wenn sie korrekt eingesetzt werden. Eine korrekt implementierte 301 übergibt nahezu die gesamte Link-Equity an die neue URL. Googles John Mueller hat bestätigt, dass 301-Weiterleitungen keinen Rankingverlust verursachen. Das Risiko entsteht durch falsche Implementierung: Weiterleitungsketten, Massen-Weiterleitungen auf die Startseite oder vollständig fehlende Seiten.

### Wie lange sollten Sie eine 301-Weiterleitung behalten?

Auf unbestimmte Zeit, oder mindestens ein Jahr. Google braucht Zeit, die alte URL erneut zu crawlen, die Weiterleitung zu verarbeiten und seinen Index zu aktualisieren. Eine zu frühe Entfernung der 301 bedeutet, dass externe Links auf die alte URL wieder 404-Fehler ergeben.

### Können zu viele 301-Weiterleitungen eine Website verlangsamen?

Einzelne Weiterleitungen fügen Millisekunden hinzu. Aber Weiterleitungsketten (Seite A > B > C) multiplizieren diese Verzögerung. Halten Sie Weiterleitungen auf maximal einen Hop. Eine Website mit Tausenden sauberer 301-Weiterleitungen ist kein Problem. Es sind Ketten und Schleifen, die Probleme verursachen.

### Was ist der Unterschied zwischen einer 301 und einer 302?

Eine [301 ist permanent](/glossary/301-redirect); eine [302 ist temporär](/glossary/302-redirect). Verwenden Sie 301, wenn die alte URL dauerhaft weg ist. Verwenden Sie 302, wenn die Originalseite zurückkehren wird (saisonale Inhalte, temporäre Wartung). Google überträgt Link-Equity zuverlässiger durch 301-Weiterleitungen.

---

Möchten Sie eine von Anfang an SEO-gerechte Website-Architektur? theStacc veröffentlicht monatlich 30 SEO-optimierte Artikel auf Ihrer Website mit sauberen URL-Strukturen und korrekter interner Verlinkung. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Weiterleitungen und Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz: Weiterleitungsleitfaden](https://moz.com/learn/seo/redirection)
- [Ahrefs: 301-Weiterleitungen für SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal: 301 vs. 302-Weiterleitungen](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Google Search Console Hilfe: Crawl-Fehler beheben](https://support.google.com/webmasters/answer/7440203)
