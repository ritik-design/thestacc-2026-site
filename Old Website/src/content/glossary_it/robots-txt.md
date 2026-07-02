---
term: "robots.txt"
slug: "robots-txt"
definition: "robots.txt è un file di testo nella radice del tuo sito che indica ai crawler dei motori di ricerca quali URL possono o non possono visitare."
category: "SEO"
difficulty: "Intermediate"
keyword: "cos'è robots.txt"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "technical-seo"
  - "xml-sitemap"
  - "meta-robots-tag"
---

## Cos'è robots.txt?

**Il file robots.txt si trova nella directory radice del tuo dominio (tuosito.com/robots.txt) e indica ai crawler dei motori di ricerca quali pagine o sezioni del sito possono visitare.**

Tutti i grandi motori di ricerca. Google, Bing, Yahoo. Controllano questo file prima di [scansionare](/glossary/crawling) il tuo sito. Pensalo come la lista del buttafuori. Non è una serratura sulla porta, ma una serie di istruzioni chiare che i bot beneducati seguono.

Secondo la documentazione di Google, Googlebot legge il robots.txt prima di fare qualsiasi richiesta al tuo server. Sui siti con migliaia di pagine, quel file diventa uno dei pezzi più importanti della tua [SEO tecnica](/glossary/technical-seo).

## Perché robots.txt è importante

Sbagliare il robots.txt può affossare il tuo posizionamento da un giorno all'altro. Una direttiva fuori posto e Google non vede più le pagine che contano davvero.

- **Protezione del crawl budget**. I siti grandi hanno un [crawl budget](/glossary/crawl-budget) limitato. Bloccare le pagine a basso valore (pannelli di amministrazione, ambienti di staging, filtri duplicati) tiene Googlebot concentrato su ciò che conta.
- **Evita l'indicizzazione di zone sensibili**. Risultati di ricerca interni, pagine di login e carrelli non hanno nulla da fare nella [SERP](/glossary/serp). robots.txt tiene i bot fuori.
- **Scoperta più rapida dei nuovi contenuti**. Quando i crawler non sprecano richieste su pagine inutili, trovano i nuovi articoli e le schede prodotto più in fretta.
- **Gestione del carico server**. I bot aggressivi possono mettere in ginocchio i server piccoli. Bloccare il crawling superfluo riduce il consumo di risorse.

Se pubblichi contenuti con regolarità. Che siano 5 pagine o 30 articoli al mese. Hai bisogno che i crawler spendano il loro tempo sulle URL giuste.

## Come funziona robots.txt

Il file usa una sintassi semplice. Tre direttive principali coprono la maggior parte dei casi.

### User-agent

Questa riga indica a quale crawler si applica la regola. `User-agent: *` colpisce tutti i bot. `User-agent: Googlebot` solo il crawler di Google. Puoi impilare più regole per bot diversi nello stesso file.

### Disallow

La direttiva `Disallow` blocca un percorso specifico. `Disallow: /admin/` impedisce ai crawler di accedere a qualsiasi cosa dentro la directory /admin/. Lasciala vuota (`Disallow:`) e permetti tutto. Una singola barra (`Disallow: /`) blocca l'intero sito.

### Allow e Sitemap

`Allow` sovrascrive una regola Disallow più ampia per percorsi specifici. Utile quando blocchi una directory ma vuoi che una pagina al suo interno venga scansionata. La direttiva `Sitemap` indirizza i crawler verso la tua [sitemap XML](/glossary/xml-sitemap) e li aiuta a trovare tutte le URL importanti senza tirare a indovinare.

### Come Google lo elabora

Googlebot scarica il tuo robots.txt prima di scansionare qualunque altra cosa. Se il file restituisce uno stato 200, Google segue le regole. Un 404 significa "nessuna restrizione". Tutto viene scansionato. Un errore 5xx rende Google temporaneamente cauto: limita il crawling finché il file non torna accessibile.

## Tipi di direttive robots.txt

Le direttive del robots.txt si dividono in 4 categorie principali:

- **Direttive di accesso (Allow/Disallow)**. Controllano quali percorsi i bot possono visitare. La base di ogni file robots.txt.
- **Direttive user-agent**. Indirizzano regole verso bot specifici. Potresti bloccare SemrushBot lasciando a Googlebot pieno accesso.
- **Direttive crawl-delay**. Dicono ai bot di attendere tra una richiesta e l'altra. Google le ignora (usa Google Search Console al suo posto), ma Bing e Yandex le rispettano.
- **Direttive sitemap**. Puntano al file sitemap. Tecnicamente non è una "regola" ma un meccanismo di scoperta su cui i bot si appoggiano.

La maggior parte dei siti piccoli e medi ha bisogno solo di direttive di accesso e di un riferimento alla sitemap. Il crawl-delay diventa importante sui siti molto grandi con vincoli di server.

## Esempi di robots.txt

**Esempio 1: idraulico locale**
Un idraulico di Milano ha un sito WordPress con le directory /wp-admin/, /carrello/ e /listini-interni/. Il suo robots.txt blocca tutte e tre e include un riferimento alla sitemap. Risultato: Googlebot passa il tempo sulle pagine di servizio e sugli articoli del blog. Non sui pannelli di amministrazione.

**Esempio 2: e-commerce con pagine filtrate**
Un retailer online ha 50 prodotti ma 3.000 combinazioni di filtri (taglia + colore + prezzo). Senza un robots.txt che blocchi `/prodotti?filtro=`, Googlebot spreca [crawl budget](/glossary/crawl-budget) su pagine filtrate duplicate. Una sola riga Disallow risolve il problema.

**Esempio 3: bloccare per sbaglio l'intero sito**
Un'agenzia di marketing è passata da staging a produzione lasciando `Disallow: /` nel robots.txt. Per 3 settimane non è stato [indicizzato](/glossary/indexing) nulla. Il traffico è precipitato a zero. Un solo carattere ha causato tutto. La barra dopo Disallow.

## robots.txt vs meta tag robots

Questi due strumenti fanno lavori diversi in momenti diversi. robots.txt ferma i crawler prima che raggiungano una pagina. Il [meta tag robots](/glossary/meta-robots-tag) dà istruzioni dopo che un crawler vi ha già acceduto.

| | robots.txt | Meta tag robots |
|---|---|---|
| **Dove vive** | File nella directory radice | `<head>` HTML delle singole pagine |
| **Quando agisce** | Prima del crawling | Dopo il crawling |
| **Ambito** | Intere directory o percorsi | Singole pagine |
| **Impedisce l'indicizzazione?** | No. Blocca solo il crawling | Sì, `noindex` rimuove dalla ricerca |
| **Ideale per** | Bloccare sezioni di un sito | Rimuovere singole pagine dalla ricerca |

Ecco il punto: se blocchi una pagina con robots.txt, Google non può vedere un tag noindex su quella pagina. Quindi può comunque comparire nei risultati (senza snippet) perché Google ha trovato un link altrove. Per rimuovere davvero una pagina dalla ricerca usa il meta tag robots. Non robots.txt.

## Best practice per robots.txt

- **Includi sempre una direttiva Sitemap**. Punta alla tua [sitemap XML](/glossary/xml-sitemap) per dare ai crawler una mappa completa. Una riga: `Sitemap: https://tuosito.com/sitemap.xml`.
- **Non bloccare mai i file CSS o JavaScript**. Google ha bisogno di renderizzare le pagine per capirle. Bloccare queste risorse danneggia la tua [SEO on-page](/glossary/on-page-seo).
- **Testa prima di pubblicare**. Usa il tester robots.txt di Google Search Console per controllare le regole. Un refuso può bloccare l'intero sito.
- **Rivedilo ogni trimestre**. Mentre il sito cresce compaiono nuove directory. Ciò che aveva senso 6 mesi fa potrebbe oggi bloccare contenuti importanti.
- **Abbinalo a una strategia di contenuti**. robots.txt gestisce cosa viene scansionato, ma servono comunque pagine che meritino di esserlo. Servizi come theStacc pubblicano 30 articoli ottimizzati SEO al mese, regalando a Googlebot contenuti freschi a ogni visita.

## Domande frequenti

### robots.txt impedisce alle pagine di apparire su Google?

Non direttamente. robots.txt blocca il crawling, non l'[indicizzazione](/glossary/indexing). Se altri siti linkano una pagina bloccata, Google può comunque mostrarla. Solo senza snippet descrittivo. Usa un meta tag noindex per rimuovere completamente una pagina dalla ricerca.

### Dove devo mettere il file robots.txt?

Posizionalo nella radice del tuo dominio: `https://tuosito.com/robots.txt`. Metterlo in una sottodirectory non funziona. Ogni sottodominio ha bisogno di un proprio robots.txt.

### robots.txt può migliorare il mio posizionamento?

Indirettamente, sì. Bloccare le pagine a basso valore preserva il crawl budget per i contenuti che contano. Sui siti grandi questo significa scoperta e indicizzazione più rapide delle nuove pagine. Cosa che può accelerare i miglioramenti di ranking.

### Tutti i bot rispettano robots.txt?

I bot legittimi dei motori di ricerca (Googlebot, Bingbot) rispettano robots.txt. I bot malevoli e gli scraper di solito lo ignorano. Non affidarti a robots.txt per la sicurezza. È una linea guida, non un firewall.

---

Vuoi essere sicuro che i tuoi contenuti SEO vengano davvero scansionati e posizionati? theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. Automaticamente. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: specifiche robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google Search Central: come Google interpreta robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- [Moz: Robots.txt. Learn SEO](https://moz.com/learn/seo/robotstxt)
- [Ahrefs: Robots.txt. The Ultimate Guide](https://ahrefs.com/blog/robots-txt/)
