---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "Core Web Vitals sind Googles drei Metriken für Page Experience: LCP, INP und CLS. Erfahren Sie, was sie messen und wie Sie sie verbessern."
category: "SEO"
difficulty: "Intermediate"
keyword: "Core Web Vitals optimieren"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## Was sind Core Web Vitals?

Core Web Vitals sind drei spezifische Metriken, mit denen Google misst, wie schnell, reaktionsfreudig und visuell stabil sich eine Webseite für echte Nutzer anfühlt.

Google hat sie 2020 eingeführt und 2021 zu einem offiziellen Ranking-Signal gemacht. Sie sind Teil der breiteren Diskussion rund um [Seitengeschwindigkeit](/glossary/page-speed) – aber präziser. Statt eines einzelnen „Speed Score" zerlegen Core Web Vitals die Nutzererfahrung in drei messbare Komponenten: Ladezeit, Interaktivität und visuelle Stabilität.

Laut Googles eigenen Daten verzeichnen Seiten, die alle drei Schwellenwerte erreichen, 24 % weniger Seitenabbrüche. Das ist keine kleine UX-Verbesserung. Es ist eine direkte Verbindung zu mehr Conversions und besserem [organischem Traffic](/glossary/organic-traffic).

## Warum sind Core Web Vitals wichtig?

Core Web Vitals zu ignorieren ruiniert Ihre Rankings nicht über Nacht. Aber bei sonst gleichen Bedingungen bevorzugt Google Seiten, die diese Benchmarks bestehen, gegenüber jenen, die es nicht tun.

- **Ranking-Faktor seit 2021**. Google hat Core Web Vitals als Teil seiner Page-Experience-Signale bestätigt – sie beeinflussen direkt, wo Sie in den [Suchergebnissen](/glossary/serp) erscheinen
- **24 % weniger Abbrüche**. Seiten, die alle drei Schwellenwerte bestehen, halten Nutzer deutlich länger auf der Seite (Google, 2021)
- **Mobile-First-Effekt**. Mit [Mobile-First-Indexing](/glossary/mobile-first-indexing) als Standard trifft es langsame Mobilseiten am härtesten
- **Korrelation mit Werbeerlösen**. Publisher, die ihre CWV-Werte verbesserten, sahen bis zu 15 % mehr Werbeumsatz durch längere Sitzungsdauern

Wenn Sie ein lokales Unternehmen oder ein kleines Team führen, ist das wichtig: Ihre Konkurrenten optimieren wahrscheinlich auch nicht für CWV. Eine bestandene Bewertung zu erreichen, während sie es nicht tun, ist ein echter Vorteil.

## Wie Core Web Vitals funktionieren

Google sammelt Core-Web-Vitals-Daten von echten Chrome-Nutzern über den Chrome User Experience Report (CrUX). Das heißt: Ihre Werte stammen von tatsächlichen Besuchern. Keine Laborsimulation.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) misst, wie lange das größte sichtbare Element Ihrer Seite zum Laden braucht. Denken Sie an: das Hero-Bild, einen großen Textblock oder ein Video-Thumbnail. Google will dies unter 2,5 Sekunden. Alles über 4 Sekunden gilt als „schlecht".

Die Lösung ist meist klar: Bilder komprimieren, ein [CDN](/glossary/content-delivery-network-cdn) nutzen, Offscreen-Ressourcen verzögern und die Server-Antwortzeit verbessern.

### Interaction to Next Paint (INP)

INP hat First Input Delay (FID) im März 2024 abgelöst. Es misst, wie schnell Ihre Seite auf Nutzerinteraktionen reagiert. Klicks, Taps und Tasteneingaben. Über den gesamten Besuch hinweg, nicht nur die erste Interaktion.

Ein guter INP liegt unter 200 Millisekunden. Wenn Ihre Seite eine halbe Sekunde einfriert, sobald jemand einen Button klickt, ist das eine durchgefallene Bewertung. Schweres JavaScript ist meist der Übeltäter.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) misst die visuelle Stabilität. Schon mal versucht, einen Button anzutippen, nur damit er wegspringt, weil eine Anzeige oder ein Bild zu spät lädt? Genau das ist Layout Shift.

Google möchte einen CLS-Wert unter 0,1. Häufigste Ursachen: Bilder ohne definierte Maße, Anzeigen, die über dem Inhalt eingefügt werden, und Webfonts, die während des Ladens die Größe wechseln.

## Arten von Core-Web-Vitals-Messungen

Core-Web-Vitals-Daten kommen in zwei Varianten – und sie erzählen oft unterschiedliche Geschichten:

- **Felddaten (RUM)**. Real User Metrics, gesammelt von echten Besuchern via CrUX. Diese nutzt Google für Ranking-Entscheidungen. Sichtbar in der [Google Search Console](/glossary/google-search-console) und PageSpeed Insights.
- **Labordaten**. Simulierte Performance-Tests aus Tools wie Lighthouse, WebPageTest und Chrome DevTools. Hilfreich zum Debuggen, aber nicht direkt für Rankings verwendet.
- **Origin- vs. URL-Ebene**. Google bewertet CWV auf Domain- und Einzelseitenebene. Wenn Ihre Site insgesamt besteht, eine wichtige Landingpage aber durchfällt, kann diese Seite trotzdem betroffen sein.
- **Mobil vs. Desktop**. Werte werden separat für Mobil und Desktop gemessen. Die meisten Sites schneiden mobil schlechter ab – und das ist die Version, die Google priorisiert.

Für [technische SEO](/glossary/technical-seo)-Audits sollten Sie immer mit Felddaten beginnen. Labordaten helfen, das Problem zu finden. Felddaten zeigen, ob das Problem echte Besucher tatsächlich stört.

## Core-Web-Vitals-Beispiele

**Beispiel 1: Die langsame Startseite eines Klempnerbetriebs**
Ein Münchner Klempner hat eine Startseite mit 4,8 Sekunden LCP wegen eines unkomprimierten Hero-Bildes (3,2 MB). Nach Konvertierung in WebP und korrekter Größenanpassung sinkt der LCP auf 1,9 Sekunden. Die Bounce-Rate fällt im folgenden Monat um 18 %.

**Beispiel 2: Ein E-Commerce-Shop mit Layout Shift**
Ein Shopify-Shop für Tierbedarf hat einen CLS-Wert von 0,34, weil Produktbilder ohne Width/Height-Attribute laden. Explizite Maße in jedem Image-Tag bringen den CLS auf 0,04. Keine versehentlichen „In den Warenkorb"-Klicks mehr von genervten Käufern.

**Beispiel 3: Ein Blog mit zu viel JavaScript**
Der Blog einer Marketing-Agentur nutzt 14 Drittanbieter-Skripte. Analytics, Chat-Widgets, Social Embeds, Anzeigen-Tracker. INP liegt bei 480 ms. Nach einem Audit und der Entfernung von 6 ungenutzten Skripten fällt INP auf 160 ms. Seiten, die über theStacc erstellt und veröffentlicht werden, kommen bereits mit sauberem, optimiertem Code. Kein aufgeblähtes Skript-Chaos.

## Core Web Vitals vs. Seitengeschwindigkeit

Beide Begriffe werden synonym verwendet. Sollten sie nicht.

| | Core Web Vitals | Seitengeschwindigkeit |
|---|---|---|
| **Was es misst** | 3 spezifische UX-Metriken (LCP, INP, CLS) | Gesamtladezeit und Performance-Score |
| **Datenquelle** | Echte Nutzerdaten (CrUX) | Laborsimulationen (Lighthouse) |
| **Google-Ranking-Signal** | Ja, direkt | Indirekt (über CWV) |
| **Umfang** | Fokus auf wahrgenommene Erfahrung | Breiteres Performance-Dach |
| **Beispielmetrik** | LCP: 2,1 s | PageSpeed-Score: 74/100 |

[Seitengeschwindigkeit](/glossary/page-speed) ist das übergeordnete Konzept. Core Web Vitals sind die konkreten Metriken, die Google tatsächlich nutzt.

## Best Practices für Core Web Vitals

- **Bilder komprimieren und in der richtigen Größe ausliefern**. WebP- oder AVIF-Format verwenden und immer explizite Width- und Height-Attribute setzen, um Layout Shift zu verhindern
- **Drittanbieter-Skripte minimieren**. Jedes externe Skript (Chat-Widgets, Analytics, Anzeigen-Tracker) erhöht den INP. Rigoros prüfen und entfernen, was nicht gebraucht wird.
- **Ein CDN für statische Assets nutzen**. Bilder und CSS von Edge-Servern in der Nähe Ihrer Besucher auszuliefern, senkt den LCP drastisch
- **Nicht-kritisches JavaScript verzögern**. Above-the-Fold-Inhalte zuerst laden, dann sekundäre Skripte nach Erreichen der Interaktivität
- **Felddaten monatlich in der Google Search Console überwachen**. Laborwerte schwanken, aber Felddaten zeigen, ob echte Besucher eine gute Erfahrung machen. Dienste wie theStacc veröffentlichen Inhalte, die saubere HTML-Best-Practices folgen – CWV-Probleme treten so von Anfang an seltener auf.

## Häufig gestellte Fragen

### Sind Core Web Vitals ein Ranking-Faktor?

Google hat Core Web Vitals im Juni 2021 als Ranking-Signal bestätigt. Sie sind Teil des Page-Experience-Systems. Der Effekt ist real, aber sekundär gegenüber Inhaltsrelevanz und [Backlinks](/glossary/backlinks). Eher Tiebreaker als Dealbreaker.

### Was hat First Input Delay ersetzt?

Interaction to Next Paint (INP) hat FID im März 2024 offiziell als Core Web Vital abgelöst. INP misst die Reaktionsfähigkeit über alle Interaktionen eines Besuchs hinweg, nicht nur den ersten Klick.

### Wie prüfe ich meine Core Web Vitals?

Nutzen Sie den Core-Web-Vitals-Bericht der Google Search Console für Felddaten. PageSpeed Insights liefert Feld- und Labordaten für jede URL. Chrome DevTools und Lighthouse eignen sich für lokale Tests während der Entwicklung.

### Was ist ein guter LCP-Wert?

Google bewertet LCP unter 2,5 Sekunden als „gut", zwischen 2,5 und 4 Sekunden als „verbesserungswürdig" und über 4 Sekunden als „schlecht". Die meisten Sites kämpfen mit dem LCP wegen unoptimierter Bilder und langsamer Server-Antwortzeit.

---

Möchten Sie schnell ladende, gut rankende Inhalte – ohne sich um technische Details zu kümmern? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google: Web Vitals](https://web.dev/vitals/)
- [Google Search Central: Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev: Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs: Core Web Vitals und SEO](https://ahrefs.com/blog/core-web-vitals/)
