---
title: "301-Weiterleitungen einrichten (Schritt für Schritt)"
description: "Lernen Sie, wie Sie 301-Weiterleitungen für SEO einrichten. Mit Anleitungen für WordPress, .htaccess, Nginx, Shopify und Cloudflare. Inkl. Testschritte. Aktualisiert März 2026."
slug: "301-redirects-guide"
keyword: "301-Weiterleitungen"
author: "Siddharth Gangal"
date: "2026-04-26"
category: "SEO Tips"
image: "/blogs-preview-images/301-redirects-guide.webp"
---

Sie haben eine URL geändert. Vielleicht sind Sie auf eine neue Domain umgezogen. Vielleicht haben Sie 3 Seiten zu einer zusammengeführt. Jetzt erhalten Besucher einen 404-Fehler, und Google lässt Ihre Rankings über Nacht einbrechen.

Jede defekte URL verliert Link-Equity, die Sie monatelang aufgebaut haben. Nutzer springen ab. Google stuft Ihre Website als schlecht gewartet ein. Eine einzige Migration ohne 301-Weiterleitungen kann Ihren organischen Traffic innerhalb einer Woche um 40 % oder mehr vernichten.

Diese Anleitung führt Sie in 7 Schritten durch die korrekte Einrichtung von 301-Weiterleitungen. Sie lernen den genauen Ablauf für WordPress, Apache `.htaccess`, Nginx, Shopify und Cloudflare. Kein Rätselraten. Keine defekten Links. Keine verlorenen Rankings.

Wir veröffentlichen monatlich 3.500+ Blogartikel in über 70 Branchen. URL-Änderungen, Seitenkonsolidierungen und Domain-Migrationen sind Aufgaben, die wir jede Woche durchführen. Die folgenden Schritte sind dieselben, die wir für unsere eigenen Websites und die unserer Kunden anwenden.

Das werden Sie lernen:

- Wie Sie jede URL finden, die eine Weiterleitung benötigt
- Wie Sie alte URLs den richtigen neuen Zielen zuordnen
- Wie Sie 301-Weiterleitungen auf 5 verschiedenen Plattformen einrichten
- Wie Sie Weiterleitungsketten und -schleifen beheben, bevor sie Ihre Ladegeschwindigkeit beeinträchtigen
- Wie Sie Weiterleitungen vor und nach dem Start testen
- Wie Sie die Weiterleitungsgesundheit in der Google Search Console überwachen

---

## Überblick

- **Benötigte Zeit:** 10 bis 30 Minuten (abhängig von der Anzahl der Weiterleitungen)
- **Schwierigkeitsgrad:** Einsteiger bis Fortgeschrittene
- **Was Sie benötigen:** Zugriff auf Ihr CMS, Hosting-Panel oder Server-Konfigurationsdateien

---

## Was ist eine 301-Weiterleitung?

Ein `301`-Statuscode teilt Browsern und Suchmaschinen mit, dass eine Seite dauerhaft zu einer neuen URL umgezogen ist. Der Browser leitet Besucher automatisch zur neuen Adresse weiter. Google überträgt die Link-Equity von der alten URL auf die neue.

Vor 2016 verursachten 301-Weiterleitungen pro Hop einen PageRank-Verlust von etwa 15 %. Das ist nicht mehr der Fall. [Google hat bestätigt, dass 30x-Weiterleitungen den PageRank nicht mehr verwässern](https://searchengineland.com/google-no-pagerank-dilution-using-301-302-30x-redirects-anymore-254608). Heute überträgt eine korrekt konfigurierte `301`-Weiterleitung laut Moz 90 bis 99 % der Link-Equity.

Damit ist die 301-Weiterleitung das wichtigste Werkzeug zur Bewahrung Ihres SEOs bei jeder URL-Änderung. Verzichten Sie darauf, fangen Sie bei null an.

---

## Schritt 1: Ermitteln Sie, welche URLs Weiterleitungen benötigen

Sie können nicht weiterleiten, was Sie nicht gefunden haben. Der erste Schritt ist, eine vollständige Liste der URLs zu erstellen, die Fehler zurückgeben oder geändert wurden.

Beginnen Sie mit der **Google Search Console**. Gehen Sie zum Seitenbericht und filtern Sie nach „Nicht gefunden (404)". Dort sehen Sie jede URL, die Google gecrawlt hat, aber nicht erreichen konnte. Exportieren Sie die gesamte Liste.

Prüfen Sie als Nächstes **Google Analytics** (GA4). Schauen Sie sich den Bericht „Landingpages" an, um Seiten zu finden, die plötzlich Traffic verloren haben. Ein starker Rückgang nach einer URL-Änderung ist ein deutliches Signal, dass eine Weiterleitung fehlt.

Führen Sie ein **Site-Crawl** mit einem Tool wie Screaming Frog, Sitebulb oder Ahrefs Site Audit durch. Diese Tools finden defekte interne Links, verwaiste Seiten und 404-Antworten, die die Google Search Console möglicherweise übersieht. Ein vollständiges [SEO-Audit](/blog/how-to-do-seo-audit) deckt diese Probleme schnell auf.

Drei häufige Szenarien, die 301-Weiterleitungen erfordern:

1. **URL-Slug-Änderung.** Sie haben `/blog/alter-beitrag` in `/blog/neuer-beitrag` umbenannt
2. **Domain-Migration.** Sie sind von `altedomain.de` zu `neuedomain.de` umgezogen
3. **Seitenkonsolidierung.** Sie haben 3 dünne Seiten zu 1 stärkeren Seite zusammengefasst, um [Thin Content zu beheben](/blog/fix-thin-content)

### Wann 301 vs. 404 vs. 410 vs. Canonical verwenden

Nicht jede tote URL braucht eine Weiterleitung. Nutzen Sie diesen Entscheidungsrahmen.

| Szenario | Maßnahme | Warum |
|---|---|---|
| Seite zu neuer URL umgezogen | `301`-Weiterleitung | Erhält Link-Equity und Nutzererfahrung |
| Seite gelöscht, kein Ersatz vorhanden | `410` Gone | Weist Google schneller an, die Seite zu entindizieren als ein `404` |
| Seite gelöscht, könnte zurückkehren | `404` Not Found | Standardantwort für vorübergehend fehlende Seiten |
| Doppelter Inhalt, beide Seiten bleiben aktiv | `canonical`-Tag | Konsolidiert Signale, ohne die Seite zu entfernen |
| Alte Domain zu neuer Domain | `301`-Weiterleitung (auf Domain-Ebene) | Überträgt alle Equity auf die neue Domain |

![Wann 301-Weiterleitungen vs. 404 vs. 410 vs. Canonical einsetzen](/images/blog/301-redirect-decision-framework.webp)

**Warum dieser Schritt wichtig ist:** Fehlende Weiterleitungen sind unsichtbar. Nutzer sehen einen 404 und verlassen die Seite. Google sieht eine tote URL und entfernt sie aus dem Index. Sie verlieren Rankings ohne jede Warnung in Ihrem Analytics-Dashboard.

**Profi-Tipp:** Exportieren Sie Ihre vollständige Sitemap-XML, bevor Sie URL-Änderungen vornehmen. Vergleichen Sie sie mit dem Crawl nach der Änderung, um jede Abweichung zu finden.

---

## Schritt 2: Alte URLs den neuen Zielen zuordnen

Eine Weiterleitung ist nur so gut wie ihr Ziel. Alle alten URLs auf die Startseite umzuleiten, ist ein häufiger Fehler. Google behandelt Startseiten-Weiterleitungen von tiefen Seiten als [Soft-404s](https://developers.google.com/search/docs/crawling-indexing/301-redirects). Sie verlieren die Equity trotzdem.

Erstellen Sie eine Tabelle mit 4 Spalten:

| Alte URL | Neue URL | Weiterleitungstyp | Hinweise |
|---|---|---|---|
| `/blog/alter-seo-leitfaden` | `/blog/onpage-seo-leitfaden` | 301 | Inhalte zusammengeführt |
| `/leistungen/webdesign` | `/leistungen/design` | 301 | Slug gekürzt |
| `/blog/veralteter-beitrag` | — | 410 | Kein Ersatz |

Befolgen Sie diese Zuordnungsregeln:

- **Verweisen Sie immer auf die relevanteste Seite.** Passen Sie Thema und Suchintention an, nicht nur die Kategorie.
- **Bei Domain-Migrationen die URL-Struktur spiegeln.** Wenn `/ueber-uns` auf der alten Domain existierte, leiten Sie es zu `/ueber-uns` auf der neuen Domain weiter.
- **Weiterleitungen nach Typ gruppieren.** Massenhafte URL-Änderungen (z. B. Entfernen von `/blog/` aus Pfaden) können musterbasierte Regeln statt einzelner Einträge verwenden.
- **Seiten mit vielen Backlinks kennzeichnen.** Verwenden Sie Ahrefs oder den Google Search Console Links-Bericht, um Ihre meistverlinkte Seiten zu identifizieren. Diese haben bei der genauen Zuordnung höchste Priorität.

Ein [Content-Audit](/blog/how-to-content-audit) hilft Ihnen, zu entscheiden, welche Seiten zusammengeführt und welche aufgegeben werden sollen. Führen Sie ihn durch, bevor Sie mit der Zuordnung beginnen.

**Warum dieser Schritt wichtig ist:** Falsche Zuordnungen senden Nutzer und Link-Equity auf irrelevante Seiten. Google bemerkt die Diskrepanz und ignoriert die Weiterleitung möglicherweise vollständig. Eine schlechte Zuordnung kann Monate der [thematischen Autorität](/blog/build-topical-authority) zunichtemachen, die Sie rund um ein Keyword-Cluster aufgebaut haben.

---

## Schritt 3: 301-Weiterleitungen auf Ihrer Plattform einrichten

Die Implementierung hängt von Ihrem Tech-Stack ab. Im Folgenden finden Sie genaue Anleitungen für 5 Plattformen.

### WordPress (Plugin-Methode)

Die schnellste Option für WordPress-Websites. Drei Plugins verwalten Weiterleitungen zuverlässig:

- **Redirection** (kostenlos). Das beliebteste Weiterleitungs-Plugin. Unterstützt Regex, protokolliert 404-Fehler und importiert CSV-Dateien.
- **Rank Math** (kostenlos/pro). Eingebauter Weiterleitungsmanager unter Rank Math > Weiterleitungen.
- **Yoast SEO Premium**. Schlägt automatisch Weiterleitungen vor, wenn Sie einen Slug ändern.

So fügen Sie eine Weiterleitung in **Redirection** hinzu:

1. Gehen Sie zu Tools > Redirection
2. Geben Sie die Quell-URL (alter Pfad) ein
3. Geben Sie die Ziel-URL (neuer Pfad) ein
4. Wählen Sie „301 Moved Permanently"
5. Klicken Sie auf „Weiterleitung hinzufügen"

Für Massen-Weiterleitungen nutzen Sie die CSV-Importfunktion. Format: `Quell-URL, Ziel-URL, 301`.

### Apache (.htaccess)

Wenn Sie Apache verwenden, fügen Sie Weiterleitungsregeln in Ihre `.htaccess`-Datei im Website-Stammverzeichnis ein.

Einzelne Weiterleitung:

```
Redirect 301 /alte-seite https://example.com/neue-seite
```

Musterbasierte Weiterleitung mit `mod_rewrite`:

```
RewriteEngine On
RewriteRule ^altes-verzeichnis/(.*)$ /neues-verzeichnis/$1 [R=301,L]
```

Domain-Weiterleitung (gesamte Website):

```
RewriteEngine On
RewriteCond %{HTTP_HOST} ^altedomain\.de$ [NC]
RewriteRule ^(.*)$ https://neuedomain.de/$1 [R=301,L]
```

Sichern Sie Ihre `.htaccess`-Datei immer vor der Bearbeitung. Ein Syntaxfehler legt die gesamte Website lahm.

### Nginx

Nginx verwendet den `server`-Block in Ihrer Konfigurationsdatei (üblicherweise `/etc/nginx/sites-available/`).

Einzelne Weiterleitung:

```
location = /alte-seite {
    return 301 https://example.com/neue-seite;
}
```

Musterbasierte Weiterleitung:

```
location /altes-verzeichnis/ {
    rewrite ^/altes-verzeichnis/(.*)$ /neues-verzeichnis/$1 permanent;
}
```

Testen Sie nach der Bearbeitung die Konfiguration mit `nginx -t` und laden Sie sie mit `systemctl reload nginx` neu.

### Shopify

Shopify verfügt über ein eingebautes Weiterleitungs-Tool. Keine Plugins erforderlich.

1. Gehen Sie zu **Einstellungen > Navigation > URL-Weiterleitungen**
2. Klicken Sie auf „URL-Weiterleitung hinzufügen"
3. Geben Sie den alten und neuen Pfad ein
4. Speichern

Für Massen-Weiterleitungen klicken Sie auf „Importieren" und laden Sie eine CSV mit 2 Spalten hoch: `Weiterleitung von` und `Weiterleitung zu`.

Shopify-Einschränkung: Mit diesem Tool können keine Weiterleitungen zu externen Domains erstellt werden. Für Domain-Migrationen weg von Shopify benötigen Sie DNS-Weiterleitungen.

### Cloudflare (Edge-Ebene)

Cloudflare-Weiterleitungen erfolgen am CDN-Edge. Sie sind die schnellste Option, da die Weiterleitung ausgelöst wird, bevor die Anfrage überhaupt Ihren Server erreicht.

1. Gehen Sie zu **Regeln > Weiterleitungsregeln**
2. Erstellen Sie eine neue Regel
3. Legen Sie die Übereinstimmungsbedingung fest (Hostname, URI-Pfad oder Wildcard)
4. Setzen Sie die Aktion auf „Dynamische Weiterleitung" oder „Statische Weiterleitung"
5. Wählen Sie `301` als Statuscode
6. Bereitstellen

Cloudflare unterstützt Wildcard-Muster und ist daher ideal für Massen-Domain-Migrationen.

### Plattformvergleich

| Plattform | Schwierigkeit | Massenunterstützung | Geschwindigkeit | Am besten für |
|---|---|---|---|---|
| WordPress-Plugin | Einfach | CSV-Import | Standard | Blog- und Content-Websites |
| `.htaccess` | Mittel | Regex-Muster | Standard | Apache Shared Hosting |
| Nginx | Mittel | Rewrite-Regeln | Schnell | VPS und dedizierte Server |
| Shopify | Einfach | CSV-Import | Standard | E-Commerce-Shops |
| Cloudflare | Einfach | Wildcard-Regeln | Am schnellsten | Jede Website mit Cloudflare |

![301-Weiterleitung einrichten auf WordPress, Apache, Nginx, Shopify und Cloudflare](/images/blog/301-redirect-platforms.webp)

**Warum dieser Schritt wichtig ist:** Falsche Syntax bricht die gesamte Website. Eine falsch konfigurierte `.htaccess`-Datei gibt einen 500-Fehler zurück. Eine fehlerhafte Nginx-Regel erzeugt eine Weiterleitungsschleife. Testen Sie nach Möglichkeit zuerst in einer Staging-Umgebung.

---

## Schritt 4: Weiterleitungsketten und -schleifen beheben

Eine Weiterleitungskette entsteht, wenn URL A auf URL B weiterleitet, die wiederum auf URL C weiterleitet. Statt 1 Hop macht der Browser 2 oder mehr. Jeder Hop fügt 50 bis 100 Millisekunden Latenz hinzu.

Eine Weiterleitungsschleife entsteht, wenn URL A auf URL B weiterleitet und URL B zurück auf URL A. Der Browser steckt in einem unendlichen Zyklus fest und zeigt schließlich eine Fehlerseite.

Google crawlt maximal 5 Hops in einer Weiterleitungskette. Darüber hinaus folgt Google nicht weiter. Die Zielseite wird nie gecrawlt oder indexiert.

### Ketten und Schleifen finden

Führen Sie einen Crawl mit Screaming Frog oder Ahrefs durch. Filtern Sie nach Weiterleitungsketten (3xx > 3xx). Sie können auch den kostenlosen [Redirect Checker von httpstatus.io](https://httpstatus.io) verwenden, um einzelne URLs zu testen.

### Ketten auflösen

Wenn die Kette A → B → C ist, aktualisieren Sie A, damit es direkt auf C zeigt. Entfernen Sie den Zwischenhop.

Vorher:
```
/alte-seite → /umbenannte-seite → /endseite
```

Nachher:
```
/alte-seite → /endseite
/umbenannte-seite → /endseite
```

Beide alten URLs zeigen jetzt direkt auf das Ziel. Je ein Hop.

### Schleifen beheben

Schleifen entstehen meist, wenn 2 Weiterleitungsregeln in Konflikt geraten. Überprüfen Sie Ihre Weiterleitungsregeln auf zirkuläre Verweise. Die Lösung ist immer dieselbe: Entscheiden Sie, welche URL das kanonische Ziel ist, und lassen Sie alle anderen URLs darauf zeigen.

Wenn Sie sowohl Server-Weiterleitungen (`.htaccess`) als auch Plugin-Weiterleitungen (Redirection) verwenden, überprüfen Sie beide. Widersprüchliche Regeln zwischen den Ebenen sind die häufigste Ursache für Schleifen.

![Vergleich Weiterleitungskette vs. direkte Weiterleitung](/images/blog/redirect-chain-vs-direct.webp)

**Warum dieser Schritt wichtig ist:** Ketten verschwenden Crawl-Budget und verlangsamen Seitenladevorgänge. Eine 3-Hop-Kette fügt 150 bis 300 ms Latenz hinzu, bevor der Nutzer überhaupt Inhalte sieht. Schleifen sind noch schlimmer. Sie blockieren den Zugriff vollständig und verbrennen Crawl-Budget für Seiten, die nie aufgelöst werden.

---

> **Überlassen Sie uns die technische Arbeit. Behalten Sie Ihre Rankings.** Stacc verwaltet URL-Struktur, Weiterleitungen und SEO-Wartung für 30+ Artikel pro Monat.
> [Für $1 starten →](/pricing)

---

## Schritt 5: Jede Weiterleitung vor dem Start testen

Ungetestete Weiterleitungen verursachen stille Rankingverluste. Eine Weiterleitung, die `302` statt `301` zurückgibt, überträgt Link-Equity nicht auf dieselbe Weise. Eine Weiterleitung, die auf einen 404 zeigt, ist schlimmer als gar keine Weiterleitung.

### Mit curl testen

Öffnen Sie Ihr Terminal und führen Sie aus:

```bash
curl -I https://example.com/alte-seite
```

Suchen Sie nach `HTTP/1.1 301 Moved Permanently` und dem `Location:`-Header, der auf die korrekte neue URL zeigt.

Zum Testen einer Kette verwenden Sie das `-L`-Flag, um allen Weiterleitungen zu folgen:

```bash
curl -IL https://example.com/alte-seite
```

Dies zeigt jeden Hop in der Kette mit seinem Statuscode.

### Mit Chrome DevTools testen

1. Öffnen Sie Chrome und drücken Sie `F12`, um DevTools zu öffnen
2. Gehen Sie zum Tab **Netzwerk**
3. Aktivieren Sie „Log beibehalten" (damit Weiterleitungen sichtbar bleiben)
4. Geben Sie die alte URL in die Adressleiste ein
5. Schauen Sie sich die erste Anfrage an. Die Spalte „Status" sollte `301` anzeigen. Die Antwortheader sollten die korrekte `Location` anzeigen.

### Mit Online-Tools testen

Kostenlose Redirect-Checker wie [httpstatus.io](https://httpstatus.io) oder der [Redirect Checker von Ahrefs](https://ahrefs.com/blog/301-redirects/) ermöglichen Tests ohne Terminal.

### Häufige Testfehler

- **HTTP vs. HTTPS-Konflikt.** Testen Sie sowohl die `http://`- als auch die `https://`-Version der alten URL. Das Fehlen einer Weiterleitung bei einem Protokoll hinterlässt eine Lücke.
- **Inkonsistente abschließende Schrägstriche.** `/alte-seite` und `/alte-seite/` sind unterschiedliche URLs. Beide benötigen Weiterleitungen.
- **www vs. non-www.** Stellen Sie sicher, dass `www.example.com/alte-seite` und `example.com/alte-seite` beide korrekt weiterleiten.

![So testen Sie 301-Weiterleitungen mit curl und Chrome DevTools](/images/blog/test-301-redirects.webp)

**Warum dieser Schritt wichtig ist:** Sie können eine defekte Weiterleitung nicht erkennen, indem Sie Ihre Website normal durchsuchen. Die alten URLs befinden sich nicht in Ihrer Navigation. Nur ein gezielter Test oder ein Google Search Console-Alert wird das Problem aufdecken. Bis dahin haben Sie möglicherweise bereits wochenlang Rankings verloren.

---

## Schritt 6: Interne Links auf neue URLs aktualisieren

Weiterleitungen sind ein Sicherheitsnetz. Sie sind kein dauerhafter Ersatz für korrekte [interne Verlinkung](/blog/internal-linking-blog-posts).

Jeder interne Link, der durch eine Weiterleitung führt, fügt einen unnötigen Hop hinzu. Google folgt dem Link zwar, aber jede Weiterleitung verbraucht Crawl-Budget. Auf einer großen Website mit Tausenden von internen Links summiert sich das schnell.

### Was aktualisiert werden muss

- **Fließtextlinks.** Jeder Blogartikel oder jede Seite, die auf die alte URL verlinkt
- **Navigationsmenüs.** Header-, Footer- und Sidebar-Links
- **XML-Sitemap.** Alte URLs entfernen und neue hinzufügen. Hilfe dabei finden Sie in unserem Leitfaden [zum Erstellen und Optimieren Ihrer XML-Sitemap](/blog/create-xml-sitemap).
- **Strukturierte Daten.** Jedes [Schema-Markup](/blog/schema-markup-for-blog-posts), das auf alte URLs verweist, aktualisieren
- **Canonical-Tags.** Stellen Sie sicher, dass der Canonical auf der neuen Seite auf sich selbst zeigt, nicht auf die alte URL

### Wie Sie eine seitenweite Suche und Ersetzen durchführen

Für WordPress verwenden Sie das Plugin **Better Search Replace**. Geben Sie das alte URL-Muster und das neue ein. Führen Sie zunächst einen Probelauf durch, um Änderungen in der Vorschau zu sehen. Dann ausführen.

Für statische Websites oder benutzerdefinierte CMS-Plattformen verwenden Sie die Suchen-und-Ersetzen-Funktion Ihres Code-Editors über das gesamte Projektverzeichnis.

Nachdem Sie die Updates vorgenommen haben, [reichen Sie Ihre aktualisierte Sitemap bei Google ein](/blog/submit-website-google), um die Neu-Indexierung zu beschleunigen.

**Warum dieser Schritt wichtig ist:** Interne Links durch Weiterleitungen verschwenden Crawl-Budget und fügen Latenz hinzu. Direkte Links sind immer schneller und effizienter. Bereinigen Sie die Quelle und behalten Sie Weiterleitungen nur als Fallback für externe Links, die Sie nicht kontrollieren können.

---

## Schritt 7: In der Google Search Console überwachen

Die Weiterleitung ist live. Die Tests sind bestanden. Aber 301-Weiterleitungen können bei Deployments, CMS-Updates oder Änderungen der Server-Konfiguration still brechen. Laufendes Monitoring erkennt Probleme, bevor sie sich auf Rankings auswirken.

### Den Seitenbericht prüfen

Gehen Sie in der Google Search Console zu **Seiten** (unter Indexierung). Filtern Sie nach:

- **Nicht gefunden (404).** Neue 404-Fehler nach dem Start Ihrer Weiterleitung bedeuten, dass etwas falsch konfiguriert ist.
- **Weiterleitungsfehler.** Google hat eine Schleife, Kette oder defekte Weiterleitung erkannt.
- **Gecrawlt. Derzeit nicht indexiert.** Die neue Zielseite ist möglicherweise noch nicht indexiert.

### Das URL-Inspektionstool verwenden

Geben Sie die alte URL in das URL-Inspektionstool ein. Google sollte „Seite ist nicht im Index" anzeigen mit einem Hinweis, dass sie auf die neue URL weiterleitet. Wenn Google die alte URL weiterhin als indexiert anzeigt, beantragen Sie die Indexierung für die neue URL.

### Core Web Vitals prüfen

Weiterleitungsketten erhöhen die Time to First Byte (TTFB). Überprüfen Sie nach der Implementierung von Weiterleitungen die **Core Web Vitals** in der Search Console auf Latenzschwankungen. Jeder Hop fügt 50 bis 100 ms hinzu. Wenn Ihre TTFB gestiegen ist, haben Sie wahrscheinlich eine nicht aufgelöste Kette.

Sie können dies auch als Teil einer umfassenderen Strategie zur [Verbesserung der Core Web Vitals](/blog/improve-core-web-vitals) auf Ihrer Website nutzen.

### Kontrollzeitpunkte festlegen

- **Tag 7:** Neue 404-Fehler in der GSC prüfen. Verifizieren, dass alte URLs korrekt auflösen.
- **Tag 30:** Organischen Traffic vor und nach der Weiterleitung vergleichen. Den Performance-Bericht nach der neuen URL gefiltert verwenden.
- **Tag 90:** Bestätigen, dass sich Rankings stabilisiert haben. Websites mit sauberen 301-Weiterleitungen behalten 95 % oder mehr ihres organischen Traffics innerhalb von 2 bis 3 Monaten.

**Warum dieser Schritt wichtig ist:** Weiterleitungen können still brechen. Ein CMS-Update könnte Ihre `.htaccess`-Datei überschreiben. Ein Plugin-Update könnte Weiterleitungsregeln zurücksetzen. Ohne Monitoring merken Sie nichts davon, bis Rankings fallen.

---

## Ergebnisse: Was Sie erwarten können

Google verarbeitet die meisten 301-Weiterleitungen innerhalb von 1 bis 2 Wochen. Sie sehen, wie die alte URL aus den Suchergebnissen verschwindet und die neue URL deren Platz einnimmt.

Rankings stabilisieren sich nach einer Migration typischerweise innerhalb von 2 bis 3 Monaten. [Websites mit sauberen 301-Weiterleitungen behielten 95 % oder mehr ihres organischen Traffics](https://ahrefs.com/blog/301-redirects/) in diesem Zeitraum.

Google empfiehlt, 301-Weiterleitungen mindestens 1 Jahr lang aktiv zu halten. Eine zu frühe Entfernung schickt zurückkehrende Besucher und alte Backlinks auf einen 404.

Der vollständige Zeitplan:

| Meilenstein | Zeitrahmen |
|---|---|
| Google beginnt mit der Verarbeitung der Weiterleitung | 1 bis 3 Tage |
| Alte URL aus dem Index entfernt | 1 bis 2 Wochen |
| Neue URL rankt an der Position der alten URL | 2 bis 4 Wochen |
| Traffic vollständig stabilisiert | 2 bis 3 Monate |
| Weiterleitung sicher entfernen | Mindestens 1 Jahr |

![SEO-Auswirkungszeitplan der 301-Weiterleitung](/images/blog/301-redirect-timeline.webp)

Kombinieren Sie saubere Weiterleitungen mit konsistenter Content-Veröffentlichung, um [organischen Traffic zu steigern](/blog/increase-organic-traffic), während sich Ihre Weiterleitungen einpendeln.

---

## Fehlerbehebung: 5 häufige 301-Weiterleitungsprobleme

### Problem 1: Weiterleitung gibt 302 statt 301 zurück

Eine `302` ist eine temporäre Weiterleitung. Sie überträgt Link-Equity nicht auf dieselbe Weise wie eine `301`. Das passiert häufig, wenn ein Plugin standardmäßig `302` verwendet oder die Server-Konfiguration `Redirect` ohne Angabe des Statuscodes nutzt.

**Lösung:** Überprüfen Sie Ihre Weiterleitungsregel. Verwenden Sie für `.htaccess` explizit `Redirect 301` oder `[R=301,L]`. Prüfen Sie in Ihrem CMS-Plugin, ob der Weiterleitungstyp auf „Permanent (301)" gesetzt ist.

### Problem 2: Weiterleitungskette (3+ Hops)

Sie haben A letztes Jahr auf B weitergeleitet. Dieses Jahr haben Sie B auf C weitergeleitet. Jetzt läuft A durch 2 Hops, um C zu erreichen. Google folgt zwar, aber die Latenz beeinträchtigt die Performance.

**Lösung:** Aktualisieren Sie die Regel für A, damit sie direkt auf C zeigt. Aktualisieren Sie dann B, damit es direkt auf C zeigt. Lösen Sie jede Kette auf einen einzigen Hop auf.

### Problem 3: Weiterleitungsschleife

URL A leitet auf B weiter. URL B leitet zurück auf A. Der Browser zeigt „ERR_TOO_MANY_REDIRECTS" und nichts lädt.

**Lösung:** Öffnen Sie Ihre Weiterleitungsregeln und suchen Sie nach zirkulären Verweisen. Wenn Sie sowohl ein Plugin als auch Server-Weiterleitungen verwenden, überprüfen Sie beide Ebenen. Entfernen Sie die konfliktverursachende Regel.

### Problem 4: Gemischte HTTP- und HTTPS-Weiterleitung

Die HTTP-Version der alten URL leitet auf die HTTP-Version der neuen URL weiter, die dann auf HTTPS weiterleitet. Das ist eine 2-Hop-Kette, die 1 Hop sein sollte.

**Lösung:** Alle Weiterleitungen sollten direkt auf die HTTPS-Version der Ziel-URL zeigen. Aktualisieren Sie jede Regel, damit sie `https://` im Ziel verwendet.

### Problem 5: Soft-404 nach der Weiterleitung

Die Weiterleitung funktioniert. Der Statuscode ist `301`. Aber die Zielseite hat dünnen oder leeren Inhalt. Google behandelt dies als „Soft-404" und überträgt möglicherweise keine Link-Equity. Das passiert häufig, wenn Sie auf eine [Thin-Content](/blog/fix-thin-content)-Seite oder eine generische Kategorieseite weiterleiten.

**Lösung:** Stellen Sie sicher, dass jedes Weiterleitungsziel eine echte, substanzielle Seite mit einzigartigem Inhalt ist. Falls die Zielseite noch nicht existiert, erstellen Sie sie, bevor Sie die Weiterleitung aktivieren.

![Häufige 301-Weiterleitungsprobleme und Lösungen](/images/blog/301-redirect-problems.webp)

---

> **Ihr SEO-Team. 99 $ pro Monat.** 30 optimierte Artikel, veröffentlicht und gewartet. Weiterleitungen, interne Links und technisches SEO inklusive.
> [Für $1 starten →](/pricing)

---

## Häufig gestellte Fragen

**Wie lange sollten 301-Weiterleitungen aktiv bleiben?**

Google empfiehlt, 301-Weiterleitungen mindestens 1 Jahr lang aktiv zu halten. Externe Websites, die auf Ihre alte URL verlinken, senden weiterhin Traffic durch diese Weiterleitung. Eine zu frühe Entfernung, bevor diese externen Links aktualisiert werden (die meisten werden es nie tun), schickt deren Besucher auf einen 404. Wenn Sie unsicher sind, behalten Sie die Weiterleitung dauerhaft. Der Server-Overhead ist vernachlässigbar.

**Schaden 301-Weiterleitungen dem SEO?**

Nein. Google hat 2016 bestätigt, dass 30x-Weiterleitungen keinen PageRank-Verlust verursachen. Eine korrekt konfigurierte `301` überträgt 90 bis 99 % der Link-Equity auf die Ziel-URL. Das einzige Risiko sind Implementierungsfehler wie Ketten, Schleifen oder Weiterleitungen auf irrelevante Seiten.

**Was ist der Unterschied zwischen einer 301- und einer 302-Weiterleitung?**

Eine [301-Weiterleitung](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301) signalisiert eine dauerhafte Verschiebung. Google überträgt Link-Equity und entindiziert schließlich die alte URL. Eine `302` signalisiert eine vorübergehende Verschiebung. Google behält die alte URL im Index und überträgt möglicherweise keine vollständige Equity. Verwenden Sie `301` für jede dauerhafte URL-Änderung.

**Können zu viele 301-Weiterleitungen meine Website verlangsamen?**

Einzelne Weiterleitungen fügen minimale Latenz hinzu (unter 100 ms). Das Problem sind Weiterleitungsketten. Jeder Hop fügt 50 bis 100 ms hinzu. Eine 3-Hop-Kette fügt 150 bis 300 ms hinzu, bevor die Seite überhaupt zu laden beginnt. Halten Sie jede Weiterleitung auf einen einzigen Hop, und die Performance-Auswirkung bleibt vernachlässigbar.

**Wie überprüfe ich, ob meine 301-Weiterleitungen funktionieren?**

Verwenden Sie `curl -I [URL]` in Ihrem Terminal. Die Antwort sollte `HTTP/1.1 301 Moved Permanently` mit einem `Location:`-Header anzeigen, der auf das korrekte Ziel zeigt. Sie können auch Chrome DevTools (Netzwerk-Tab mit aktiviertem „Log beibehalten") oder kostenlose Online-Tools wie httpstatus.io verwenden.

**Soll ich eine 301-Weiterleitung oder ein Canonical-Tag verwenden?**

Verwenden Sie eine `301`, wenn Sie die alte Seite vollständig entfernen. Verwenden Sie ein `canonical`-Tag, wenn beide Seiten aktiv bleiben, Sie Google aber anweisen möchten, Ranking-Signale auf eine Version zu konsolidieren. Ein häufiges Beispiel: Produktseiten mit URL-Parametern. Die gefilterte URL bleibt zugänglich, aber der Canonical zeigt auf die saubere URL. Bei [Keyword-Kannibalismus](/blog/fix-keyword-cannibalization) zwischen 2 aktiven Seiten ist ein Canonical-Tag häufig der bessere erste Schritt.

---

301-Weiterleitungen schützen die Link-Equity und Rankings, die Sie bereits erworben haben. Jede URL-Änderung ohne Weiterleitung ist ein Leck in Ihrem SEO-Fundament.

Richten Sie Weiterleitungen korrekt ein, testen Sie sie, überwachen Sie sie und kombinieren Sie die Arbeit mit konsistenter Content-Veröffentlichung. So [ranken Sie höher bei Google](/blog/how-to-rank-higher-google) und behalten die Positionen, die Sie gewinnen.
