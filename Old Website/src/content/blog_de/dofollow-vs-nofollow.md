---
title: "Dofollow vs Nofollow Links (2026): Strategien, Taktiken und Beispiele"
description: "Dofollow vs Nofollow im vollständigen Guide 2026: Unterschiede, Strategien, praktische Beispiele und Schritt-für-Schritt-Anleitungen für bessere Rankings."
slug: "dofollow-vs-nofollow"
keyword: "dofollow vs nofollow"
author: "Siddharth Gangal"
date: "2026-06-08"
category: "SEO Tips"
image: "/blogs-preview-images/dofollow-vs-nofollow.webp"
---

Jeder Link im Internet gehört zu einer von zwei Kategorien. Dofollow-Links übertragen Ranking-Autorität. Nofollow-Links signalisieren Google, dass der Link nicht als Empfehlung gewertet werden soll.

Der Unterschied zwischen Dofollow und Nofollow bestimmt, wie Sie Backlinks aufbauen, interne Links strukturieren und Ihr Linkprofil prüfen. Wer das Prinzip missversteht, verschwendet Monate damit, Links zu verfolgen, die keine Rankings verbessern. Oder noch schlimmer: Er löst eine Google-Strafe aus, weil das Linkprofil unnatürlich wirkt.

89,4 Prozent aller Backlinks der 110.000 größten Websites sind Dofollow-Links. Die restlichen 10,6 Prozent sind Nofollow-Links. Doch ein gesundes Linkprofil braucht beide Typen. Google erwartet eine natürliche Mischung.

Wir haben über 3.500 SEO-Artikel in mehr als 70 Branchen veröffentlicht. Linkstrategie ist Teil jeder Kampagne. Dieser Guide behandelt alles, was Sie über Dofollow- und Nofollow-Links wissen müssen – inklusive des Google-Updates von 2019, das die Funktionsweise von Nofollow grundlegend verändert hat.

Hier ist, was Sie lernen:

- Der genaue Unterschied zwischen Dofollow- und Nofollow-Links
- Wie Google Nofollow 2019 von einer Direktive zu einem "Hinweis" gemacht hat
- Wann Sie `rel="nofollow"`, `rel="sponsored"` und `rel="ugc"` verwenden
- Wie Sie den Follow-Status jedes Links in Sekunden prüfen
- Das ideale Dofollow-zu-Nofollow-Verhältnis für ein natürliches Profil
- Häufige Fehler, die Google-Strafen auslösen

![Dofollow vs Nofollow Links Vergleich, der zeigt, wie jeder Typ das SEO beeinflusst](/images/blog/dofollow-vs-nofollow-comparison.webp)

---

## Was sind Dofollow-Links?

Ein Dofollow-Link ist ein standardmäßiger HTML-Link, der Link-Equity (auch "Link Juice" oder PageRank genannt) von einer Seite zur anderen überträgt. Es gibt kein `rel="dofollow"`-Attribut in HTML. "Dofollow" ist ein branchenüblicher Kurzbegriff für einen Link, auf den kein Nofollow-Attribut angewendet wurde.

So sieht ein Dofollow-Link im HTML aus:

```html
<a href="https://example.com">Ankertext</a>
```

Kein spezielles Attribut nötig. Jeder Link ist standardmäßig Dofollow.

Wenn Google einen Dofollow-Link crawlt, passieren drei Dinge:

1. Google folgt dem Link zur Zielseite
2. Google überträgt einen Teil der Autorität der Quellseite auf die Zielseite
3. Google verwendet den Link als Ranking-Signal für die Zielseite

Dofollow-Links sind das Fundament des ursprünglichen Google-PageRank-Algorithmus. Je mehr Dofollow-Links von autoritativen Quellen auf eine Seite verweisen, desto höher rankt diese Seite in der Regel. [Websites mit starken Backlink-Profilen](https://ahrefs.com/blog/backlink-growth-study/) erhalten 67 Prozent mehr organischen Traffic als Seiten mit schwachen Profilen.

Deshalb bleibt Linkaufbau einer der wichtigsten (und schwierigsten) Bestandteile von SEO. 41 Prozent der Marketer geben an, dass der Aufbau qualitativer [Backlinks](/glossary/backlinks) die schwierigste SEO-Aufgabe ist, der sie gegenüberstehen.

---

## Was sind Nofollow-Links?

Ein Nofollow-Link enthält das Attribut `rel="nofollow"`. Dieses Attribut sagt Suchmaschinen: "Verwenden Sie diesen Link nicht als Ranking-Signal."

So sieht ein Nofollow-Link im HTML aus:

```html
<a href="https://example.com" rel="nofollow">Ankertext</a>
```

Google führte das Nofollow-Attribut 2005 ein, um Kommentar-Spam zu bekämpfen. Spammer überschwemmten Blog-Kommentare und Foren mit Links, um ihre Rankings zu verbessern. Nofollow gab Website-Betreibern die Möglichkeit, zu verlinken, ohne Autorität zu übertragen.

### Wo Nofollow-Links natürlicherweise auftreten

Die meisten Links im Internet sind auf folgenden Plattformen standardmäßig Nofollow:

- **Social Media:** Links von Facebook, X (Twitter), LinkedIn, Instagram, Pinterest und TikTok
- **Foren und Communities:** Reddit, Quora, Stack Overflow und die meisten Foren-Softwares
- **Blog-Kommentare:** WordPress und die meisten CMS setzen Kommentar-Links automatisch auf Nofollow
- **Wikipedia:** Alle externen Links tragen Nofollow
- **Pressemitteilungen:** Die meisten Pressemitteilungs-Dienste verwenden Nofollow
- **Nutzer-generierte Verzeichnisse:** Yelp, Google-Business-Profile-Links und Bewertungsplattformen

Nofollow-Links verbessern Rankings nicht direkt. Aber sie erfüllen andere Zwecke. Sie generieren Referral-Traffic, bauen Markenbekanntheit auf und signalisieren Google, dass Ihre Website eine natürliche Linkvielfalt besitzt.

---

## Dofollow vs Nofollow: Die wichtigsten Unterschiede

Der Unterschied lässt sich auf eine Frage reduzieren: Überträgt der Link Ranking-Autorität?

| Merkmal | Dofollow | Nofollow |
|---|---|---|
| Überträgt Link-Equity | Ja | Nein (aber Google kann es überschreiben) |
| HTML-Attribut | Keines (Standardverhalten) | `rel="nofollow"` |
| Direkter SEO-Effekt | Ja. Verbessert Rankings | Kein direkter Effekt |
| Referral-Traffic | Ja | Ja |
| Google-Crawling | Immer gefolgt und gecrawlt | Kann gecrawlt werden oder auch nicht |
| Markensichtbarkeit | Ja | Ja |
| Natürlicher Profilbedarf | 60–80 Prozent aller Links | 20–40 Prozent aller Links |
| Risiko einer Überoptimierung | Hoch bei 100 Prozent Dofollow | Gering |

Das kritische Detail, das die meisten Guides übersehen: Seit 2019 behandelt Google Nofollow als "Hinweis", nicht als Direktive. Google kann entscheiden, einen Nofollow-Link zu folgen und zu zählen, wenn seine Algorithmen den Link als relevant und vertrauenswürdig einstufen. Mehr dazu im nächsten Abschnitt.

> Dofollow-Links bauen Ranking-Autorität auf. Nofollow-Links sorgen für ein natürliches Profil. Beide sind nötig.

---

## Das Google-Update von 2019: Nofollow wurde zu einem Hinweis

Am 10. September 2019 veröffentlichte Google einen Blogpost mit dem Titel ["Evolving nofollow"](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify), der die Funktionsweise von Nofollow-Links veränderte. Dieses Update ist die wichtigste Entwicklung in der Link-Attribution seit über einem Jahrzehnt. Viele SEO-Guides liefern das Thema immer noch falsch ab.

### Was sich geändert hat

**Vor 2019:** Nofollow war eine Direktive. Google befolgte sie absolut. Ein Nofollow-Link übertrug null Autorität, null Crawl-Signale und null Ranking-Vorteil. Punkt.

**Nach 2019:** Nofollow wurde zu einem Hinweis. Google behält sich das Recht vor, Nofollow-Links als Ranking-Signale zu betrachten, wenn seine Algorithmen sie als relevant einstufen. Google kann neue Seiten auch über Nofollow-Links entdecken und indexieren.

### Drei neue Link-Attribute

Google führte zwei neue Attribute neben Nofollow ein:

| Attribut | Anwendungsfall | Beispiel |
|---|---|---|
| `rel="sponsored"` | Bezahlte Links, Werbeanzeigen, Sponsoring | Affiliate-Links, bezahlte Platzierungen, Banner-Werbelinks |
| `rel="ugc"` | Nutzer-generierte Inhalte | Blog-Kommentare, Forenbeiträge, Community-Einreichungen |
| `rel="nofollow"` | Allgemeines "keine Empfehlung"-Signal | Jeder Link, für den Sie sich nicht verbürgen möchten |

Sie können Attribute kombinieren: `rel="nofollow sponsored"` oder `rel="nofollow ugc"`. Google empfiehlt, das spezifischste verfügbare Attribut zu verwenden.

![Googles Nofollow-Evolution von Direktive zu Hinweis mit den neuen sponsored- und ugc-Attributen](/images/blog/google-nofollow-hint-evolution.webp)

### Was das in der Praxis bedeutet

**Für Linkbuilder:** Nofollow-Links von autoritativen Seiten (Wikipedia, große Publikationen, Reddit) können nun einen gewissen Ranking-Wert besitzen. Sie sollten diese Links nicht ignorieren.

**Für Website-Betreiber:** Verwenden Sie `rel="sponsored"` bei bezahlten Links. Verwenden Sie `rel="ugc"` bei nutzergenerierten Links. Verwenden Sie `rel="nofollow"` bei Links, denen Sie nicht vertrauen oder die Sie nicht unterstützen. Bestehende Nofollow-Links müssen nicht geändert werden.

**Für SEO-Audits:** Ein [Backlink-Audit](/blog/backlink-audit-guide) sollte Nofollow-Links von hochautoritativen Domains jetzt separat analysieren. Diese können zu Rankings beitragen, auch ohne traditionelle Link-Equity zu übertragen.

78,8 Prozent der SEO-Experten glauben heute, dass Nofollow-Links in gewissem Maße Rankings beeinflussen. Das "Hinweis"-Modell bedeutet, dass Googles Behandlung von Nofollow nicht mehr binär ist.

---

> **Hören Sie auf zu schreiben. Fangen Sie an zu ranken.** Stacc veröffentlicht 30 SEO-Artikel pro Monat für 99 Dollar. Jeder Artikel baut Ihre [Domain-Autorität](/blog/domain-authority-guide) mit internen und externen Links auf.
> [Starten Sie für 1 Dollar →](/pricing)

---

## Wann Sie jeden Link-Typ verwenden

Die richtige Anwendung von Dofollow- und Nofollow-Attributen verhindert Strafen und maximiert den Linkwert.

### Wann Sie Dofollow verwenden (Standard)

Lassen Sie Links als Dofollow, wenn Sie das Ziel wirklich empfehlen:

- **Editorial Links in eigenen Inhalten:** Links zu Quellen, Referenzen und Ressourcen, die Sie empfehlen
- **Interne Links:** Alle [internen Links](/blog/internal-linking-blog-posts) sollten Dofollow sein (mit seltenen Ausnahmen)
- **Gastbeitrag-Autoren-Bio-Links:** Standardpraxis für legitime Gastbeiträge
- **Ressourcen-Seiten-Links:** Kuratierte Listen von Tools, Guides oder Referenzen, denen Sie vertrauen
- **Partner- und Lieferanten-Links:** Wenn die Beziehung echt ist und nicht bezahlt

### Wann Sie Nofollow verwenden

Setzen Sie `rel="nofollow"`, wenn Sie sich für das Ziel nicht verbürgen möchten:

- **Nicht vertrauenswürdige Inhalte:** Links zu Seiten, die Sie nicht persönlich geprüft haben
- **Kommentarbereiche:** Jeder Link, der von Nutzern eingereicht wurde (die meisten CMS erledigen das automatisch)
- **Login- oder Registrierungslinks:** Google muss diese Seiten nicht crawlen

### Wann Sie rel="sponsored" verwenden

Setzen Sie `rel="sponsored"` bei jedem Link, der eine Geldzahlung involviert:

- **Affiliate-Links:** Produktempfehlungen mit Tracking-Parametern
- **Bezahlte Platzierungen:** Gesponserte Inhalte, Advertorials, bezahlte Verzeichniseinträge
- **Banner-Werbelinks:** Display-Werbung, die auf externe Seiten verlinkt
- **Influencer-Partnerschaften:** Produktbewertungs-Links mit Vergütung

Google hat ausdrücklich festgestellt, dass das Fehlen von `rel="sponsored"` oder `rel="nofollow"` bei bezahlten Links zu einer manuellen Strafe führen kann. Das gilt sowohl für die verlinkende als auch für die verlinkte Seite.

### Wann Sie rel="ugc" verwenden

Setzen Sie `rel="ugc"` bei Links, die von Ihren Nutzern erstellt wurden:

- **Blog-Kommentare:** Nutzer-eingereichte Kommentare mit Links
- **Forenbeiträge:** Community-generierte Inhalte
- **Nutzerbewertungen:** Von Kunden eingereichte Produkt- oder Servicebewertungen
- **Wiki-artige Inhalte:** Von Community-Mitgliedern bearbeitbare Seiten

### Schnelle Entscheidungshilfe

| Linkszenario | Zu verwendendes Attribut |
|---|---|
| Sie haben den Link geschrieben und empfehlen das Ziel | Dofollow (kein Attribut) |
| Ein Nutzer hat den Link eingereicht | `rel="ugc"` |
| Eine Zahlung war involviert | `rel="sponsored"` |
| Sie vertrauen dem Ziel nicht | `rel="nofollow"` |
| Interner Link auf der eigenen Website | Dofollow (kein Attribut) |
| Affiliate-Link mit Tracking | `rel="sponsored"` |

---

## Wie Sie prüfen, ob ein Link Dofollow oder Nofollow ist

Sie können den Follow-Status jedes Links auf drei Arten prüfen – von der manuellen Inspektion bis zum Bulk-Audit mit Tools.

### Methode 1: Element untersuchen (manuell)

Klicken Sie mit der rechten Maustaste auf einen Link in Ihrem Browser und wählen Sie "Untersuchen" oder "Element untersuchen". Suchen Sie im HTML nach dem `<a>`-Tag.

**Dofollow-Beispiel:**
```html
<a href="https://example.com">Linktext</a>
```
Kein `rel="nofollow"`-Attribut vorhanden. Der Link ist Dofollow.

**Nofollow-Beispiel:**
```html
<a href="https://example.com" rel="nofollow">Linktext</a>
```
Das `rel="nofollow"`-Attribut sagt Google, keine Autorität zu übertragen.

Diese Methode funktioniert für die Prüfung einzelner Links. Sie skaliert nicht für ein vollständiges Website-Audit.

### Methode 2: Browser-Erweiterungen (schnelle Prüfung)

Installieren Sie eine Browser-Erweiterung, die Link-Typen automatisch hervorhebt:

- **NoFollow** (Chrome): Hebt Nofollow-Links mit einem rot gepunkteten Rahmen hervor
- **SEOquake** (Chrome/Firefox): Zeigt den Follow-Status in einer Toolbar an
- **MozBar** (Chrome): Zeigt Link-Attribute zusammen mit DA/PA-Metriken an

Diese Erweiterungen funktionieren auf jeder Webseite. Sie sind nützlich für schnelle Wettbewerbsanalysen und Stichproben auf Ihren eigenen Inhalten.

### Methode 3: Crawling-Tools (Bulk-Audit)

Für ein vollständiges Website-Audit verwenden Sie ein Crawling-Tool, das alle Links analysiert:

- **Screaming Frog:** Crawlt Ihre gesamte Website und exportiert alle Links mit ihren Attributen
- **Ahrefs Site Audit:** Ermittelt Ihr Dofollow-Nofollow-Verhältnis über alle Seiten
- **Semrush Backlink Audit:** Analysiert Ihr eingehendes Linkprofil nach Follow-Status

Ein vollständiges [SEO-Audit](/blog/how-to-do-seo-audit) sollte eine Link-Attribut-Analyse enthalten. Das zeigt, ob Ihr Profil natürlich oder überoptimiert wirkt.

---

## Ein natürliches Linkprofil aufbauen

Google erwartet eine natürliche Mischung aus Dofollow- und Nofollow-Links. Ein Profil mit 100 Prozent Dofollow-Links signalisiert Manipulation. Ein Profil mit zu vielen Nofollow-Links deutet auf geringe Autorität hin.

### Das ideale Verhältnis

| Profiltyp | Dofollow % | Nofollow % | Risikostufe |
|---|---|---|---|
| Natürlich / Gesund | 60–80 % | 20–40 % | Gering |
| Leicht aggressiv | 80–90 % | 10–20 % | Mittel |
| Überoptimiert | 90–100 % | 0–10 % | Hoch |
| Autoritätsdefizit | Unter 50 % | Über 50 % | Mittel |

Der Durchschnitt über die 110.000 größten Websites liegt bei 89,4 Prozent Dofollow und 10,6 Prozent Nofollow. Aber dieser Durchschnitt ist nach oben verzerrt, weil große Autoritätsseiten naturgemäß mehr Dofollow-Editorial-Links anziehen.

![Natürliche Linkprofil-Verhältnisse mit Dofollow- und Nofollow-Prozentsätzen und Risikostufen](/images/blog/dofollow-nofollow-link-profile-ratio.webp)

Für kleine und mittlere Unternehmen ist eine 70-zu-30-Aufteilung ein gesundes Ziel. Erreichen Sie das, indem Sie qualitativ hochwertige Dofollow-Links durch Inhalte und Outreach aufbauen und gleichzeitig Nofollow-Links von Social Media, Foren und Verzeichnissen natürlich ansammeln.

### Wie Sie Dofollow-Links aufbauen

Die besten Dofollow-Links stammen von Editorial-Mentions. Jemand liest Ihre Inhalte, findet sie wertvoll und verlinkt sie, ohne danach gefragt zu werden. Hier sind Strategien, die Editorial-Dofollow-Links generieren:

- **Veröffentlichen Sie eigene Recherchen oder Daten.** Datenstudien ziehen Zitationen an. Journalisten und Blogger verlinken auf originelle Statistiken.
- **Erstellen Sie hochnutzliche Guides.** Schritt-für-Schritt-Anleitungen, die echte Probleme lösen, verdienen Links von Ressourcen-Seiten.
- **Entwickeln Sie kostenlose Tools.** Ein nützliches kostenloses Tool verdient natürliche Links von jedem, der es empfiehlt. Sehen Sie sich unsere [SEO-Tools](/tools/seo-audit) als Beispiele an.
- **Gastbeiträge auf relevanten Seiten.** Schreiben Sie für Seiten in Ihrer Branche. Fügen Sie einen natürlichen Dofollow-Link in den Inhalt ein (nicht nur in der Bio).
- **Reparieren Sie defekte Links.** Finden Sie defekte ausgehende Links auf Autoritätsseiten und bieten Sie Ihre Inhalte als Ersatz an. Das nennt man [Broken Link Building](/blog/fix-broken-links).
- **Erhalten Sie Presse-Mentions.** Antworten Sie auf Journalisten-Anfragen auf Plattformen wie HARO, Connectively oder Qwoted.

### Wie Sie Nofollow-Links natürlich verdienen

Nofollow-Links sammeln sich durch normale Geschäftsaktivitäten an:

- Teilen Sie Ihre Inhalte auf Social-Media-Plattformen (alle Social-Links sind Nofollow)
- Beteiligen Sie sich an relevanten Reddit- und Quora-Diskussionen
- Pflegen Sie Geschäftseinträge in Verzeichnissen und auf Bewertungsplattformen
- Ermutigen Sie Kundenbewertungen, die auf Ihre Website verlinken
- Kommentieren Sie Branchen-Blogs mit echten Einblicken (kein Spam)

---

> **Ihr SEO-Team. 99 Dollar pro Monat.** 30 optimierte Artikel, automatisch veröffentlicht. Jeder Artikel verdient Backlinks und baut [topische Autorität](/blog/build-topical-authority) über Zeit auf.
> [Starten Sie für 1 Dollar →](/pricing)

---

## Häufige Dofollow- und Nofollow-Fehler

Diese Fehler kosten Rankings und lösen manchmal Strafen aus. Vermeiden Sie sie alle.

**Fehler 1: Eigene interne Links auf Nofollow setzen.**
Interne Links sollten fast immer Dofollow sein. Das Hinzufügen von Nofollow zu internen Links blockiert den PageRank-Fluss innerhalb Ihrer eigenen Website. Das nennt man "PageRank Sculpting", und [Google bestätigte 2009](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify), dass es nicht funktioniert. Der PageRank, der durch einen nofollowed internen Link geflossen wäre, verdampft. Er wird nicht auf andere Links umverteilt.

**Fehler 2: 100 Prozent Dofollow-Links aufbauen.**
Ein rein aus Dofollow-Links bestehendes Profil wirkt konstruiert. Googles Algorithmen erkennen unnatürliche Muster. Ein gesundes Profil enthält Nofollow-Links von Social-Plattformen, Verzeichnissen und nutzergenerierten Inhalten. Zielen Sie auf ein 70-zu-30-Dofollow-zu-Nofollow-Verhältnis ab.

**Fehler 3: Bezahlte Links nicht als sponsored kennzeichnen.**
Google verlangt `rel="sponsored"` oder `rel="nofollow"` bei jedem Link, der eine Zahlung involviert. Das Fehlen dieser Kennzeichnung kann zu einer manuellen Maßnahme gegen beide Seiten führen. Das umfasst Affiliate-Links, gesponserte Beiträge und bezahlte Verzeichniseinträge.

**Fehler 4: Nofollow-Links in der Backlink-Analyse ignorieren.**
Nach dem Update von 2019 können Nofollow-Links von hochautoritativen Domains einen Ranking-Wert besitzen. Ein vollständiges [Backlink-Audit](/blog/backlink-audit-guide) sollte beide Link-Typen analysieren. Alle Nofollow-Links zu ignorieren bedeutet, potenzielle Ranking-Signale zu übersehen.

**Fehler 5: Sich auf einzelne Link-Attribute zu fixieren.**
Ein Dofollow-Link von einer schwachen Spam-Seite schadet mehr als er nützt. Ein Nofollow-Link von der New York Times bringt Tausende Referral-Besucher. Qualität und Relevanz sind wichtiger als der Follow-Status. Konzentrieren Sie sich darauf, Links von relevanten, autoritativen Quellen zu verdienen – unabhängig von deren Nofollow-Richtlinie.

**Fehler 6: Nofollow auf ausgehende Editorial-Links setzen.**
Manche Website-Betreiber setzen jeden ausgehenden Link auf Nofollow, um PageRank "zu horten". Das ist unnötig und potenziell schädlich. Google erwartet natürliches ausgehendes Linking. Jedem externen Link Nofollow zu verpassen, lässt Ihre Inhalte verdächtig wirken. Verlinken Sie mit Dofollow auf autoritative Quellen. Das schadet Ihren Rankings nicht.

---

## Dofollow vs Nofollow und internes Linking

Interne Links verdienen besondere Aufmerksamkeit. Sie funktionieren anders als externe Backlinks.

Jeder [interne Link](/blog/internal-linking-blog-posts) auf Ihrer Website sollte Dofollow sein. Interne Links verteilen PageRank über Ihre Seiten. Sie helfen Google, neue Inhalte zu entdecken und zu indexieren. Sie signalisieren, welche Seiten Sie für am wichtigsten halten.

Die einzige Ausnahme: Login-Seiten, Warenkörbe oder andere Seiten, die Sie nicht priorisieren möchten. Aber selbst diese brauchen selten Nofollow. Google regelt das meiste über `robots.txt` und `noindex`-Tags.

Eine starke interne Linkstruktur multipliziert den Wert jedes Dofollow-Backlinks, den Ihre Website verdient. Wenn ein externer Dofollow-Link auf Ihre Homepage verweist, verteilen interne Links diese Autorität auf Ihre Blogposts, Produktseiten und Service-Seiten.

Verwenden Sie [Ankertext-Optimierung](/blog/anchor-text-optimization) für interne Links. Beschreibender Ankertext sagt Google, worum es auf der Zielseite geht. Vermeiden Sie generische Formulierungen wie "hier klicken" oder "mehr lesen".

---

## Der Unterschied zwischen Nofollow und Noindex

Anfänger verwechseln Nofollow oft mit Noindex. Die beiden dienen völlig unterschiedlichen Zwecken.

| Attribut | Was es tut | Geltungsbereich |
|---|---|---|
| `rel="nofollow"` | Sagt Google, keine Autorität durch einen bestimmten Link zu übertragen | Link-Ebene |
| `<meta name="robots" content="noindex">` | Sagt Google, eine Seite nicht in die Suchergebnisse aufzunehmen | Seiten-Ebene |

Ein Nofollow-Link erlaubt Google weiterhin, die Zielseite zu sehen und potenziell zu crawlen. Er beeinflusst nur, ob Autorität durch diesen spezifischen Link übertragen wird.

Ein Noindex-Tag verbirgt eine ganze Seite vor den Suchergebnissen. Die Seite existiert weiterhin und lädt für Besucher. Aber Google entfernt sie aus dem Index.

Diese beiden Attribute lösen unterschiedliche Probleme. Verwenden Sie Nofollow, wenn Sie nicht möchten, dass ein Link Autorität überträgt. Verwenden Sie Noindex, wenn Sie nicht möchten, dass eine Seite in den Suchergebnissen erscheint. Sie können zusammen auf derselben Seite für maximale Kontrolle verwendet werden.

Für mehr Informationen darüber, wie Google Indexierungs-Direktiven behandelt, sehen Sie sich unsere [technische SEO-Checkliste](/blog/technical-seo-checklist) an.

---

> **Über 3.500 Blogs veröffentlicht. 92 Prozent durchschnittlicher SEO-Score.** Sehen Sie, was Stacc für Ihre Linkbuilding-Strategie tun kann. Wir veröffentlichen Inhalte, die Backlinks verdienen.
> [Starten Sie für 1 Dollar →](/pricing)

---

## FAQ

**Was ist der Unterschied zwischen Dofollow- und Nofollow-Links?**

Ein Dofollow-Link überträgt Ranking-Autorität (PageRank) von einer Seite zur anderen. Ein Nofollow-Link enthält `rel="nofollow"`, das Google anweist, den Link nicht als Ranking-Signal zu zählen. Dofollow verbessert das SEO direkt. Nofollow generiert Traffic und Markensichtbarkeit ohne direkten Ranking-Effekt.

**Sind Nofollow-Links wertlos?**

Nein. Nofollow-Links übertragen keine Ranking-Autorität direkt. Aber sie tragen zu einem natürlichen Linkprofil bei, generieren Referral-Traffic und bauen Markenbekanntheit auf. Seit Googles Update von 2019 ist Nofollow ein "Hinweis" statt einer Direktive. Google kann entscheiden, einige Nofollow-Links als Ranking-Signale zu zählen. 78,8 Prozent der SEO-Experten glauben, dass Nofollow-Links Rankings immer noch beeinflussen.

**Wie erkennt man, ob ein Link Dofollow oder Nofollow ist?**

Klicken Sie mit der rechten Maustaste auf den Link und wählen Sie "Untersuchen". Suchen Sie im HTML nach dem `<a>`-Tag. Wenn das Attribut `rel="nofollow"` vorhanden ist, ist der Link Nofollow. Wenn kein solches Attribut vorhanden ist, ist der Link standardmäßig Dofollow. Für Bulk-Analysen verwenden Sie Tools wie Screaming Frog, Ahrefs oder Semrush.

**Sind LinkedIn-Links Dofollow oder Nofollow?**

LinkedIn-Links sind fast immer Nofollow oder UGC. Sie übertragen keinen PageRank im klassischen Sinne. Dennoch bringen LinkedIn-Links Referral-Traffic und stärken Ihre Markenpräsenz. Sie sollten LinkedIn als Traffic-Quelle nutzen, nicht als direkte Linkbuilding-Plattform.

**Ist Nofollow gut für SEO?**

Ja, indirekt. Nofollow-Links bauen keinen PageRank direkt auf, aber sie signalisieren Google ein natürliches Linkprofil. Ein Profil mit 100 Prozent Dofollow-Links wirkt manipuliert. Nofollow-Links von Social Media, Foren und Verzeichnissen zeigen Google, dass Ihre Website auf natürliche Weise erwähnt wird. Seit 2019 behandelt Google Nofollow als Hinweis und kann einige Nofollow-Links als Ranking-Signale verwerten.

**Was ist das ideale Verhältnis von Dofollow zu Nofollow-Links?**

Ein gesundes Linkprofil enthält 60 bis 80 Prozent Dofollow-Links und 20 bis 40 Prozent Nofollow-Links. Der Durchschnitt über die größten Websites liegt bei 89,4 Prozent Dofollow. Für kleine und mittlere Unternehmen ist eine 70-zu-30-Aufteilung ein gesundes Ziel. Ein Profil mit 100 Prozent Dofollow-Links wirkt konstruiert und birgt das Risiko einer Google-Strafe.

**Sind Social-Media-Links Dofollow oder Nofollow?**

Alle großen Social-Media-Plattformen verwenden Nofollow-Links. Das umfasst Facebook, X (Twitter), LinkedIn, Instagram, Pinterest und TikTok. Social-Media-Links übertragen keine direkte Ranking-Autorität. Sie generieren aber Referral-Traffic und tragen zu Ihrem Nofollow-Link-Anteil bei.

**Was ist der Unterschied zwischen Nofollow und Noindex?**

Nofollow ist ein Link-Level-Attribut, das verhindert, dass Autorität durch einen bestimmten Link übertragen wird. Noindex ist eine Seiten-Level-Direktive, die verhindert, dass eine ganze Seite in den Suchergebnissen erscheint. Sie lösen unterschiedliche Probleme. Verwenden Sie Nofollow bei Links, die Sie nicht unterstützen. Verwenden Sie Noindex bei Seiten, die nicht indexiert werden sollen.

**Sollte ich alle ausgehenden Links auf Nofollow setzen?**

Nein. Jedem ausgehenden Link Nofollow zu verpassen ist unnötig und wirkt unnatürlich. Verlinken Sie auf autoritative Quellen mit Dofollow, wenn Sie die Inhalte wirklich empfehlen. Google erwartet natürliches ausgehendes Linking. Verwenden Sie Nofollow nur bei Links, denen Sie nicht vertrauen, bezahlten Links oder nutzergenerierten Inhalten.

**Was sind rel="sponsored" und rel="ugc"?**

Google führte diese Attribute im September 2019 zusammen mit der Nofollow-"Hinweis"-Änderung ein. Verwenden Sie `rel="sponsored"` bei jedem Link, der eine Geldzahlung involviert (Affiliate-Links, bezahlte Platzierungen, Sponsoring). Verwenden Sie `rel="ugc"` bei nutzergenerierten Inhalten (Kommentare, Forenbeiträge, Bewertungen). Beide sagen Google, keine Ranking-Autorität durch den Link zu übertragen.

---

Dofollow- und Nofollow-Links erfüllen unterschiedliche Zwecke. Beide sind für eine gesunde SEO-Strategie unverzichtbar. Bauen Sie Dofollow-Links für Ranking-Autorität auf. Verdienen Sie Nofollow-Links für Traffic, Vielfalt und natürliche Signale. Überwachen Sie Ihr Verhältnis, kennzeichnen Sie bezahlte Links korrekt und denken Sie daran, dass Google Nofollow als Hinweis behandelt – nicht als Befehl.
