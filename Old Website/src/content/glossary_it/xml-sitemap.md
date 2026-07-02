---
term: "Sitemap XML"
slug: "xml-sitemap"
definition: "Una sitemap XML è un file che elenca tutti gli URL importanti del tuo sito e aiuta i motori come Google a scoprire, scansionare e indicizzare le pagine più velocemente."
category: "SEO"
difficulty: "Intermediate"
keyword: "cos'è una sitemap xml"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "technical-seo"
  - "google-search-console"
---

## Cos'è una sitemap XML?

**Una sitemap XML è un file strutturato (in formato XML) che fornisce ai motori di ricerca l'elenco completo degli URL del sito che vuoi vengano scansionati e indicizzati.**

In pratica è una mappa stradale per i [crawler](/glossary/crawling). Senza, Googlebot deve scoprire le pagine seguendo i link. Funziona, ma è lento e incompleto. Le pagine orfane — quelle senza link interni che puntano a loro — rischiano di non essere mai trovate.

La documentazione ufficiale di Google definisce le sitemap «particolarmente utili» per siti grandi, siti nuovi con pochi link esterni e siti con molti contenuti multimediali. Uno studio di Oncrawl ha mostrato che le pagine inserite in una sitemap XML vengono indicizzate in media 8-10 volte più velocemente di quelle escluse.

## Perché conta una sitemap XML?

Se Google non trova le tue pagine, non può posizionarle. Una sitemap XML elimina ogni dubbio.

- **Indicizzazione più rapida dei nuovi contenuti**. Quando pubblichi un articolo o una landing page, la sitemap segnala subito a Google la sua esistenza. Niente attesa che Googlebot ci arrivi seguendo qualche link.
- **Copertura delle pagine orfane**. Le pagine senza link interni sono invisibili ai crawler. La sitemap le recupera. È un classico nei grandi e-commerce con pagine generate dai filtri.
- **Segnali di priorità e freschezza**. Le sitemap includono i tag `<lastmod>` che indicano a Google quando una pagina è stata aggiornata. I contenuti freschi vengono ri-scansionati prima.
- **Valore diagnostico**. Inviare la sitemap a [Google Search Console](/glossary/google-search-console) ti dà un report di indicizzazione. Vedi esattamente quali pagine Google ha indicizzato e quali ha scartato. E perché.

Per qualunque sito che pubblica contenuti regolarmente, una sitemap XML non è negoziabile.

## Come funziona una sitemap XML

Il processo è lineare. Crei il file, dici a Google dov'è, lo tieni aggiornato.

### Struttura del file

Una sitemap XML è una lista di voci `<url>` racchiuse in un tag `<urlset>`. Ogni voce contiene l'URL (`<loc>`), la data dell'ultima modifica (`<lastmod>`), la frequenza di cambiamento (`<changefreq>`) e la priorità (`<priority>`). Google ignora ufficialmente `changefreq` e `priority`. Quello che conta sono URL e `lastmod`.

### Metodi di invio

Tre modi per far arrivare la sitemap a Google. Primo: inviarla direttamente da [Google Search Console](/glossary/google-search-console). Secondo: referenziarla nel file [robots.txt](/glossary/robots-txt) con `Sitemap: https://tuosito.it/sitemap.xml`. Terzo: la Ping API per notificare gli aggiornamenti. La maggior parte dei siti combina i primi due.

### File indice di sitemap

Una singola sitemap arriva al massimo a 50.000 URL o 50 MB (non compressi). I siti più grandi usano un file indice — una sitemap che punta ad altre sitemap. Un sito da 200.000 pagine avrà un indice che punta a 4 sitemap da 50.000 URL ciascuna.

### Generazione automatica

La maggior parte dei CMS (WordPress, Webflow, Shopify) genera le sitemap XML in automatico. WordPress la crea di default in `/wp-sitemap.xml`. Plugin SEO come Yoast e RankMath offrono più controllo su quali pagine includere.

## Tipi di sitemap XML

Non tutte le sitemap servono allo stesso scopo:

- **Sitemap XML standard**. Elenca le pagine HTML. Il tipo più comune — e quello a cui pensa la maggior parte delle persone quando dice «sitemap».
- **Sitemap di immagini**. Elenca le immagini del sito per Google Immagini. Utile a fotografi, e-commerce e siti visivamente densi.
- **Sitemap video**. Fornisce metadati sui contenuti video (titolo, descrizione, anteprima, durata). Aiuta a comparire nei caroselli video di Google.
- **Sitemap news**. Riservata agli editori Google News. Include data di pubblicazione, titolo e lingua. Solo per i siti approvati come fonti di notizie.
- **Indice di sitemap**. Un file principale che collega più sitemap. Obbligatorio per i siti che superano il limite delle 50.000 URL.

Le PMI nella maggior parte dei casi hanno bisogno solo di una sitemap XML standard. Aggiungi quelle di immagini o video se i contenuti visivi sono centrali nella strategia.

## Esempi di sitemap XML

**Esempio 1: sito nuovo di un'attività locale**
Un'azienda di idraulica appena lanciata a Milano ha 15 pagine e zero [backlink](/glossary/backlinks). Senza sitemap, Google potrebbe impiegare settimane per scoprire tutte le pagine seguendo solo i link. Dopo aver inviato la sitemap a Search Console, tutte e 15 le pagine vengono indicizzate in 5 giorni.

**Esempio 2: e-commerce con 10.000 prodotti**
Un retailer aggiunge 50 nuovi prodotti a settimana. La sitemap si auto-genera tramite Shopify, aggiornando le date `<lastmod>` a ogni nuovo prodotto. Google ri-scansiona la sitemap regolarmente e trova i nuovi prodotti in pochi giorni. Non settimane.

**Esempio 3: blog che pubblica 30 articoli al mese**
Un'azienda che usa theStacc pubblica 30 articoli ottimizzati per la SEO ogni mese. Ogni nuovo post compare automaticamente nella sitemap XML. Il report di copertura di Search Console mostra una crescita costante delle pagine indicizzate. Senza alcun aggiornamento manuale.

## Sitemap XML vs sitemap HTML

File diversi per pubblici diversi.

| | Sitemap XML | Sitemap HTML |
|---|---|---|
| **Pubblico** | Crawler dei motori di ricerca | Visitatori umani |
| **Formato** | Codice XML | Pagina web normale con link |
| **Posizione** | `/sitemap.xml` | Di solito `/sitemap` o nel footer |
| **Scopo** | Aiutare i crawler a scoprire tutte le pagine | Aiutare l'utente a navigare |
| **Impatto SEO** | Migliora direttamente l'efficienza di scansione | Minimo. È più una funzione UX |
| **Obbligatoria?** | Fortemente consigliata | Opzionale, è un di più |

Entrambe sono utili, ma è la sitemap XML quella che incide direttamente sulla [SEO](/glossary/seo). Se ne implementi solo una, scegli la versione XML.

## Best practice per la sitemap XML

- **Inserisci solo pagine indicizzabili**. Niente pagine con tag [noindex](/glossary/noindex), URL reindirizzati o pagine bloccate da robots.txt. Una sitemap pulita costruisce fiducia con Google.
- **Tieni accurate le date `<lastmod>`**. Aggiorna il lastmod solo quando il contenuto cambia davvero. Fingere freschezza modificando le date senza modifiche reali erode la fiducia di Google nei tuoi segnali.
- **Inviala da Google Search Console**. L'invio manuale ti dà accesso al report di indicizzazione che mostra esattamente come Google processa la sitemap. Da controllare ogni mese.
- **Limita a 50.000 URL per file**. Oltre questa soglia, usa un indice di sitemap. Una sitemap enorme che fallisce nel caricamento è peggio di nessuna sitemap.
- **Abbinala a una pubblicazione costante**. Una sitemap dà il meglio quando il sito aggiunge nuovi contenuti che meritano l'[indicizzazione](/glossary/indexing). theStacc pubblica 30 articoli SEO al mese — così Google ha un motivo concreto per ri-scansionare spesso la tua sitemap e scoprire pagine fresche.

## Domande frequenti

### Ogni sito ha bisogno di una sitemap XML?

Tecnicamente no. I siti piccoli con un buon [linking interno](/glossary/internal-link) possono cavarsela senza. Ma non c'è alcun rovescio della medaglia, e i benefici in velocità di indicizzazione e dati diagnostici giustificano lo sforzo minimo per qualsiasi sito.

### Come si crea una sitemap XML?

La maggior parte dei CMS la genera in automatico. WordPress, Webflow e Shopify creano sitemap di default. Per i siti custom, strumenti come Screaming Frog o XML-Sitemaps.com producono il file. Poi lo invii da Google Search Console.

### Ogni quanto aggiornare la sitemap?

Idealmente la sitemap si aggiorna da sola quando pubblichi o modifichi contenuti. Le sitemap generate dal CMS lo fanno. Se gestisci una sitemap manuale, aggiornala ogni volta che aggiungi, rimuovi o modifichi pagine in modo significativo.

### Una sitemap fatta male può danneggiare la SEO?

Una sitemap con URL rotti, pagine in noindex o date lastmod sbagliate manda segnali contraddittori a Google. Non scatena penalizzazioni, ma spreca il [crawl budget](/glossary/crawl-budget) e rallenta l'indicizzazione delle pagine importanti.

---

Vuoi contenuti freschi che Google indicizzi davvero? theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. In automatico. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: scopri le sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google Search Central: creare e inviare una sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Ahrefs: sitemap XML, la guida completa](https://ahrefs.com/blog/xml-sitemap/)
- [Moz: sitemap XML](https://moz.com/learn/seo/xml-sitemaps)
