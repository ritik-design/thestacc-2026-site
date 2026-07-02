---
term: "Alt-Text (Alt-Attribut)"
slug: "alt-text"
definition: "Alt-Text (Alternativtext) beschreibt Bilder für Suchmaschinen und Screenreader. Erfahren Sie, wie Sie effektiven Alt-Text schreiben, sehen Sie Beispiele und warum er für SEO wichtig ist."
category: "SEO"
difficulty: "Beginner"
keyword: "Alt-Text"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## Was ist Alt-Text?

Alt-Text (Alternativtext) ist ein HTML-Attribut, das eine schriftliche Beschreibung eines Bildes liefert. Wird von Screenreadern für sehbehinderte Nutzer und von Suchmaschinen verwendet, um zu verstehen, was ein Bild zeigt.

Sie haben es wahrscheinlich im Code gesehen: `<img src="foto.jpg" alt="Beschreibung hier">`. Diese Beschreibung ist der Alt-Text. Er bedient zwei Zielgruppen gleichzeitig. Für Personen, die das Bild nicht sehen können – sei es, weil sie einen Screenreader benutzen, eine langsame Verbindung haben oder das Bild nicht lädt – sagt der Alt-Text ihnen, was dort ist. Für Google ist es eines der wichtigsten Signale zur Indexierung und zum Ranking von Bildern in der Google-Bildersuche.

Die WebAIM-Barrierefreiheitsanalyse von 2024 ergab, dass bei 54,5 % der Bilder im Web der Alt-Text fehlt. Über die Hälfte. Das ist sowohl ein [Barrierefreiheits](/glossary/accessibility-content)-Versagen als auch eine SEO-Chance, die direkt für jeden bereitliegt, der bereit ist, ein Textfeld auszufüllen.

## Warum ist Alt-Text wichtig?

Alt-Text steht am Schnittpunkt von Barrierefreiheit, [SEO](/glossary/seo) und Nutzererfahrung. Ignorieren Sie ihn, und Sie verlieren auf allen drei Ebenen.

- **Barrierefreiheits-Compliance**. Die ADA- und WCAG-2.1-Richtlinien verlangen Alt-Text auf bedeutsamen Bildern. Klagen wegen Web-Barrierefreiheit haben seit 2018 um über 300 % zugenommen. Es ist nicht optional.
- **Bildersuche-Traffic**. Die Google-Bildersuche treibt erheblichen [organischen Traffic](/glossary/organic-traffic) an. Ohne Alt-Text kann Google Ihre Bilder nicht richtig indexieren, und Ihnen entgeht dieser Traffic vollständig.
- **[OnPage-SEO](/glossary/on-page-seo)-Signale**. Alt-Text gibt Google zusätzlichen Kontext zu den Inhalten Ihrer Seite. Ein Artikel über Küchenrenovierung mit korrekt beschriebenen Bildern verstärkt die thematische Relevanz der Seite.
- **Fallback bei kaputten Bildern**. Wenn ein Bild nicht lädt (langsame Verbindung, kaputte URL, E-Mail-Clients, die Bilder blockieren), erscheint stattdessen der Alt-Text. Nutzer verstehen trotzdem, was dort sein sollte.

Jedes Bild auf Ihrer Website sollte Alt-Text haben. Dekorative Bilder (Rahmen, Abstandshalter) bekommen ein leeres Alt-Attribut (`alt=""`). Alles andere bekommt eine Beschreibung.

## Wie Alt-Text funktioniert

Alt-Text zu schreiben ist im Konzept einfach. Es gut zu machen, erfordert das Verständnis dessen, was verschiedene Systeme davon brauchen.

### Wie Screenreader ihn verwenden

Wenn ein Screenreader auf ein Bild trifft, liest er den Alt-Text laut vor. Wenn der Alt-Text „Stockfoto eines Geschäftstreffens" lautet, hört der Nutzer das. Nutzlos. Wenn er „5 Teammitglieder, die einen Marketingbericht an einem Konferenztisch durchgehen" lautet, versteht der Nutzer den Kontext. Schreiben Sie für die zuhörende Person, nicht für eine Suchmaschine.

### Wie Google ihn verwendet

Googlebot kann Bilder nicht so „sehen" wie Menschen. Es verlässt sich auf Alt-Text, umgebenden Text, Dateinamen und strukturierte Daten, um den Bildinhalt zu verstehen. Googles eigene Dokumentation gibt an, dass Alt-Text „extrem nützlich" für das Ranking in der Google-Bildersuche ist. Es ist eines der stärksten [Bild-SEO](/glossary/image-seo)-Signale, das Sie kontrollieren können.

### Die HTML-Implementierung

Alt-Text lebt im `alt`-Attribut des `<img>`-Tags:

`<img src="zahnarztpraxis-rezeption.jpg" alt="Moderne Zahnarztpraxis-Rezeption mit Personal, das einen Patienten begrüßt">`

Die meisten CMS-Plattformen (WordPress, Webflow, Ghost) haben dedizierte Alt-Text-Felder in ihren Bild-Upload-Oberflächen. Sie müssen kein HTML direkt bearbeiten.

### Was passiert ohne Alt-Text

Wenn ein Bild gar kein Alt-Attribut hat, lesen Screenreader möglicherweise stattdessen den Dateinamen. So etwas wie „IMG_4392.jpg." Nutzlos. Wenn das Alt-Attribut vorhanden, aber leer ist (`alt=""`), überspringen Screenreader das Bild komplett – was für dekorative Bilder korrektes Verhalten ist, für bedeutsame aber falsch.

## Arten von Alt-Text

Nicht jedes Bild braucht dieselbe Behandlung:

- **Informativer Alt-Text**. Beschreibt, was das Bild zeigt und warum es wichtig ist. Wird für Fotos, Illustrationen, Diagramme und Grafiken verwendet, die Informationen vermitteln. „Balkendiagramm zeigt 40 % Anstieg des organischen Traffics von Januar bis Juni 2025."
- **Funktionaler Alt-Text**. Beschreibt, was ein anklickbares Bild tut. Wird für Buttons, Icons und verlinkte Bilder verwendet. „Suchen-Button" oder „PDF-Bericht herunterladen."
- **Dekorativer Alt-Text (leer)**. Wird für rein dekorative Bilder verwendet, die keine Information hinzufügen. Setzen Sie `alt=""`, damit Screenreader sie überspringen. Hintergrundmuster, Trennlinien und dekorative Icons fallen hierunter.
- **Komplexer Alt-Text**. Wird für Diagramme, Grafiken und Infografiken verwendet, die dichte Daten enthalten. Der Alt-Text liefert eine Zusammenfassung, und eine längere Beschreibung kommt in ein `longdesc`-Attribut oder umliegenden Text.

Den richtigen Typ zu treffen, ist wichtig. Dekorative Bilder über zu beschreiben, überfrachtet das Screenreader-Erlebnis. Informative Bilder unter zu beschreiben, verliert sowohl Barrierefreiheit als auch SEO-Wert.

## Beispiele für Alt-Text

**Beispiel 1: Die Menüseite eines Restaurants**
Schlechter Alt-Text: „Essen" oder „Gerichtsfoto" oder gar kein Alt-Text. Guter Alt-Text: „Gegrillter Lachs mit gerösteten Gemüsen und Zitronen-Buttersauce auf einem weißen Teller serviert." Die beschreibende Version hilft Google, das Bild für „gegrillter Lachs"-Suchen zu ranken, und hilft sehbehinderten Nutzern, das Menüelement zu verstehen.

**Beispiel 2: Eine Immobilienanzeige**
Schlecht: „Hausäußeres." Gut: „Zweistöckiges Kolonialhaus mit roter Backsteinfassade, weißen Säulen und gepflegtem Vorgarten in der Beispielstraße 123." Ein [lokaler SEO](/glossary/local-seo)-Gewinn. Die detaillierte Beschreibung enthält Immobilienmerkmale, die Hauskäufer in der Google-Bildersuche suchen.

**Beispiel 3: Eine E-Commerce-Produktseite**
Schlecht: „Produktbild 1." Gut: „Nike Air Max 90 Laufschuh in Weiß und Grau, Seitenansicht." Dieser Alt-Text enthält Marke, Produktnamen, Farbe und Winkel. Genau das, was Google braucht, um es in Shopping- und Bildsuche-Ergebnissen anzuzeigen. Mit über theStacc veröffentlichten Blog-Inhalten neben korrekt optimierten Produktbildern entsteht ein starkes [OnPage-SEO](/glossary/on-page-seo)-Fundament.

## Alt-Text vs. Title-Text

Diese werden ständig verwechselt, aber sie dienen völlig unterschiedlichen Zwecken.

| | Alt-Text | Title-Text |
|---|---|---|
| **Zweck** | Beschreibt das Bild für Barrierefreiheit und SEO | Liefert ergänzende Infos beim Hover |
| **Erforderlich** | Ja (WCAG-Konformität) | Nein |
| **SEO-Auswirkung** | Stark (primäres Bild-Rankingsignal) | Minimal |
| **Screenreader** | Wird automatisch vorgelesen | Wird manchmal gelesen, hängt von Einstellungen ab |
| **Sichtbarkeit** | Wird angezeigt, wenn das Bild nicht lädt | Wird als Tooltip beim Mouseover angezeigt |

Alt-Text ist verpflichtend. Title-Text ist optional und meist kosmetisch. Konzentrieren Sie Ihre Bemühungen auf den Alt-Text.

## Best Practices für Alt-Text

- **Seien Sie spezifisch und prägnant**. Beschreiben Sie, was im Bild ist, in 125 Zeichen oder weniger. Screenreader können längere Beschreibungen abschneiden. „Golden Retriever fängt eine Frisbee in einem Park" schlägt „Hund" jedes Mal.
- **Binden Sie Keywords natürlich ein, nicht erzwungen**. Wenn das Bild auf einer Seite über [Keyword-Recherche](/glossary/keyword-research) ist und das Bild ein Keyword-Analyse-Tool zeigt, erwähnen Sie das. Aber stopfen Sie nicht: „Keyword-Recherche Keyword-Tool beste Keyword-Recherche SEO-Keywords" ist Spam.
- **Beginnen Sie nicht mit „Bild von" oder „Foto von"**. Screenreader kündigen bereits an, dass es sich um ein Bild handelt. Mit „Bild von" zu beginnen, ist überflüssig. Springen Sie direkt zur Beschreibung.
- **Beschreiben Sie die Funktion bei anklickbaren Bildern**. Wenn ein Bild ein Link oder Button ist, sollte der Alt-Text die Aktion beschreiben, nicht das Bild. Ein Lupensymbol, das die Suche auslöst, sollte `alt="Suchen"` haben. Nicht `alt="Lupe"`.
- **Automatisieren Sie, wo möglich**. Beim Veröffentlichen in großem Maßstab wird konsistenter Alt-Text schwer zu pflegen. theStacc fügt jedem veröffentlichten Artikel optimierten Alt-Text hinzu, sodass Bilder von Tag eins an barrierefrei und SEO-bereit sind.

## Häufig gestellte Fragen

### Wie lang sollte Alt-Text sein?

Halten Sie ihn unter 125 Zeichen. Die meisten Screenreader schneiden Alt-Text um diese Länge ab. Bei komplexen Bildern wie Infografiken liefern Sie eine kurze Alt-Text-Zusammenfassung und fügen eine längere Beschreibung im umliegenden Seiteninhalt hinzu.

### Beeinflusst Alt-Text Google-Rankings?

Ja. Alt-Text ist ein bestätigter Rankingfaktor für Google-Bilder und liefert unterstützenden Kontext für Web-Suchrankings. Die Search-Central-Dokumentation von Google empfiehlt ausdrücklich, beschreibenden Alt-Text für [OnPage-SEO](/glossary/on-page-seo) zu schreiben.

### Sollte jedes Bild Alt-Text haben?

Jedes bedeutsame Bild braucht Alt-Text. Dekorative Bilder (Abstandshalter, Hintergrundmuster, visuelle Verzierungen) sollten leere Alt-Attribute (`alt=""`) haben, damit Screenreader sie überspringen. Die Schlüsselfrage: Vermittelt dieses Bild Information? Wenn ja, beschreiben Sie es.

### Kann Alt-Text zu lang sein?

Ja. Übermäßig langer Alt-Text ist frustrierend für Screenreader-Nutzer und kann für Google nach [Keyword-Stuffing](/glossary/keyword-stuffing) aussehen. Halten Sie Beschreibungen fokussiert. Wenn ein Bild eine Erklärung in Absatzlänge benötigt, packen Sie das in den Body-Text in der Nähe des Bildes. Nicht in das Alt-Attribut.

---

Möchten Sie jeden Blogbeitrag mit korrektem Alt-Text, [Überschriften-Tags](/glossary/heading-tags) und integriertem OnPage-SEO veröffentlichen? theStacc veröffentlicht jeden Monat 30 SEO-optimierte Artikel auf Ihrer Website. Automatisch. [Für $1 starten →](https://app.thestacc.com)

## Quellen

- [Google Search Central: Best Practices für Bild-SEO](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM: Leitfaden zu Alternativtext](https://webaim.org/techniques/alttext/)
- [WebAIM: Die WebAIM Million (jährlicher Barrierefreiheitsbericht)](https://webaim.org/projects/million/)
- [W3C: WCAG 2.1 Bildanforderungen](https://www.w3.org/WAI/tutorials/images/)
- [Moz: Bild-SEO-Leitfaden](https://moz.com/learn/seo/image-seo)
