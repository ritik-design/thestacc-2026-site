---
term: "Redirect 301"
slug: "301-redirect"
definition: "Un redirect 301 invia definitivamente utenti e motori di ricerca da un URL a un altro. Scopri quando usare i redirect 301, come implementarli e il loro impatto sulla SEO."
category: "SEO"
difficulty: "Intermediate"
keyword: "cos'è un redirect 301"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "302-redirect"
  - "canonical-url"
  - "link-equity"
  - "crawling"
  - "domain-authority"
---

## Cos'è un Redirect 301?

Un redirect 301 è un codice di stato HTTP che reindirizza in modo permanente un URL verso un altro. Comunica a browser e motori di ricerca che l'indirizzo originale si è spostato definitivamente.

Quando Googlebot o un visitatore accede a un URL con redirect 301, viene automaticamente inviato al nuovo URL. Nessuna pagina rotta. Nessun vicolo cieco. Il "301" fa riferimento al codice di risposta HTTP specifico. È il modo del web di dire "questa pagina si è spostata definitivamente in una nuova posizione." Esiste un [redirect 302](/glossary/302-redirect) per gli spostamenti temporanei, ma il 301 è quello che conta per la [SEO](/glossary/seo).

Ecco perché è fondamentale: le ricerche di Moz mostrano che i redirect 301 trasmettono circa il 95-99% della [link equity](/glossary/link-equity) all'URL di destinazione. Ciò significa che il potere di ranking che il tuo vecchio URL aveva guadagnato grazie ai [backlink](/glossary/backlinks) non scompare. Si trasferisce alla nuova pagina. Configurare i redirect 301 in modo errato significa buttare via anni di autorità accumulata.

## Perché un Redirect 301 è Importante?

Ogni volta che un URL cambia senza un redirect adeguato, qualcosa si rompe. Posizioni, traffico, esperienza utente. Scegli pure due dei tre.

- **Preserva le posizioni nei motori di ricerca**. Senza un redirect 301, Google tratta il nuovo URL come una pagina completamente nuova con zero autorità. Le tue posizioni svaniscono da un giorno all'altro.
- **Trasferisce la link equity**. Quei [backlink](/glossary/backlinks) che hai guadagnato? Un redirect 301 trasmette il loro valore al nuovo URL. Senza di esso, quella link equity evapora.
- **Previene gli errori 404**. Gli utenti che hanno salvato il vecchio URL nei preferiti o cliccano su un link esterno trovano una pagina funzionante invece di un [errore 404](/glossary/404-error). Migliore esperienza, minore [bounce rate](/glossary/bounce-rate).
- **Consolida i contenuti duplicati**. Più URL che servono lo stesso contenuto diluiscono la tua autorità. I redirect 301 li fondono in un'unica pagina più forte.

Se hai mai spostato un sito web, cambiato la struttura degli URL o unito due pagine, avevi bisogno di redirect 301. Saltarli è uno degli errori di [SEO tecnica](/glossary/technical-seo) più comuni e costosi.

## Come Funziona un Redirect 301

Il processo avviene in millisecondi, ma ecco cosa succede effettivamente sotto il cofano.

### Il Ciclo di Richiesta HTTP

Un utente o uno spider dei motori di ricerca richiede il vecchio URL. Il server risponde con il codice di stato HTTP 301 e un'intestazione "Location" che punta al nuovo URL. Il browser richiede automaticamente il nuovo URL. L'utente vede la pagina finale. Potrebbe nemmeno accorgersi che è avvenuto un redirect.

### Come Google Elabora i Redirect 301

Quando [Googlebot](/glossary/crawling) incontra un redirect 301, fa tre cose: segue il redirect verso il nuovo URL, trasferisce la maggior parte dei segnali di ranking della vecchia pagina alla nuova pagina e alla fine rimuove il vecchio URL dal suo indice. Questo processo può richiedere giorni o settimane a seconda della frequenza con cui Google scansiona il tuo sito.

### Implementazione a Livello di Server vs. a Livello di Pagina

I redirect 301 sono configurati a livello di server. Non nell'HTML. I metodi più comuni:

- **Apache (.htaccess):** `Redirect 301 /vecchia-pagina https://esempio.com/nuova-pagina`
- **Nginx:** `rewrite ^/vecchia-pagina$ /nuova-pagina permanent;`
- **Plugin WordPress:** Yoast, Redirection o Rank Math gestiscono questo tramite il pannello di controllo
- **Cloudflare:** Regole di pagina o Redirect in blocco per modifiche a livello di dominio

Esistono redirect meta refresh a livello di pagina, ma sono più lenti e non trasmettono la link equity in modo altrettanto affidabile. Usa sempre redirect 301 a livello di server.

## Tipi di Redirect

Comprendere le differenze previene errori costosi:

- **301 (Permanente)**. La pagina si è spostata definitivamente. Trasmette circa il 95-99% della link equity. Da usare per cambi di URL, migrazioni di dominio e consolidamento dei contenuti.
- **[302 (Temporaneo)](/glossary/302-redirect)**. La pagina si è spostata temporaneamente. Google potrebbe o meno trasmettere la link equity. Da usare per test A/B, pagine di manutenzione o contenuti stagionali.
- **307 (Temporaneo, HTTP/1.1)**. Uguale al 302, ma preserva rigorosamente il metodo di richiesta (POST rimane POST). Solo per casi d'uso tecnici.
- **308 (Permanente, HTTP/1.1)**. Uguale al 301 con conservazione rigorosa del metodo. Raramente usato in ambito SEO.
- **Meta refresh**. Redirect basato su HTML. Lento, scarso valore SEO. Da evitare.

In caso di dubbio, usa un redirect 301. È la scelta sicura per i cambi di URL permanenti.

## Esempi di Redirect 301

**Esempio 1: Un'azienda locale che ridisegna il proprio sito**
Uno studio legale ridisegna il proprio sito e cambia la struttura URL da `/servizi/avvocato-infortunistica` a `/aree-pratiche/infortunistica`. Senza un redirect 301, la vecchia pagina — che era posizionata al #3 per "avvocato infortunistica [città]" — restituisce un 404. Con il redirect, il nuovo URL eredita la posizione in classifica e i 47 [backlink](/glossary/backlinks) che puntano alla vecchia pagina continuano a funzionare.

**Esempio 2: Unire due articoli del blog in un'unica pagina più forte**
Un'azienda idraulica ha due articoli brevi: "Come riparare un rubinetto che perde" e "Guida alla riparazione dei rubinetti che perdono." Nessuno dei due si posiziona bene. Li unisce in un'unica guida dettagliata sull'URL più forte e fa un redirect 301 di quello più debole. I segnali combinati di [domain authority](/glossary/domain-authority) portano la pagina unita dalla posizione 12 alla posizione 4 nell'arco di 6 settimane.

**Esempio 3: Una migrazione di dominio andata storta**
Un negozio e-commerce si sposta da vecchiodominio.com a nuovodominio.com ma reindirizza solo la homepage. Le 2.400 pagine prodotto e i 180 articoli del blog restituiscono tutti 404. Il [traffico organico](/glossary/organic-traffic) cala del 78% in 2 settimane. Ogni singolo URL aveva bisogno di un redirect 301 uno a uno. Questo errore richiede mesi per essere recuperato, se viene individuato rapidamente.

## Redirect 301 vs. URL Canonical

Entrambi affrontano i contenuti duplicati, ma funzionano in modo diverso.

| | Redirect 301 | [URL Canonical](/glossary/canonical-url) |
|---|---|---|
| **Cosa fa** | Invia utenti e bot a un nuovo URL | Indica a Google quale URL è la copia "principale" |
| **Esperienza utente** | L'utente vede la nuova pagina (redirect automatico) | L'utente può ancora accedere alla pagina originale |
| **Quando usarlo** | La vecchia pagina non deve più esistere | Entrambe le pagine devono rimanere accessibili |
| **Link equity** | Trasmette circa il 95-99% | Consolida i segnali verso il canonical |
| **Esempio** | Vecchio URL del blog spostato nella nuova struttura URL | Pagina prodotto accessibile tramite 3 URL diversi |

Usa i redirect 301 quando la vecchia pagina è definitivamente rimossa. Usa i canonical quando entrambe le pagine devono esistere ma vuoi che Google dia priorità a una.

## Best Practice per i Redirect 301

- **Mappa ogni vecchio URL verso un nuovo URL pertinente**. Non reindirizzare tutto alla homepage. Reindirizza ogni vecchia pagina al suo equivalente più vicino. Google tratta i redirect in massa verso la homepage come soft 404.
- **Implementa redirect 1 a 1 durante le migrazioni del sito**. Prima di lanciare un nuovo sito, scansiona quello vecchio, esporta ogni URL e crea una mappa di redirect. Salta questo passaggio e guarderai il [traffico organico](/glossary/organic-traffic) crollare.
- **Evita le catene di redirect**. A > B > C > D rallenta l'utente, spreca il [budget di crawl](/glossary/crawl-budget) e può perdere link equity a ogni hop. Ogni redirect deve puntare direttamente alla destinazione finale.
- **Monitora con Google Search Console**. Controlla il report di copertura per gli errori di scansione dopo aver implementato i redirect. [Google Search Console](/glossary/google-search-console) mostra quali pagine restituiscono 404 in modo da poter individuare rapidamente i redirect mancanti.
- **Audit dei redirect ogni trimestre**. I vecchi redirect che puntano a pagine non più esistenti creano catene. Servizi come theStacc includono strutture URL corrette in ogni articolo pubblicato, ma se stai migrando o riorganizzando i contenuti, pianifica audit periodici dei redirect per mantenere tutto in ordine.

## Domande Frequenti

### I redirect 301 danneggiano la SEO?

Non quando vengono usati correttamente. Un redirect 301 correttamente implementato trasmette quasi tutta la link equity al nuovo URL. John Mueller di Google ha confermato che i redirect 301 non causano perdita di ranking. Il rischio viene dall'implementarli in modo errato: catene di redirect, redirect in massa verso la homepage o pagine mancanti.

### Per quanto tempo dovresti mantenere un redirect 301?

A tempo indeterminato, o almeno un anno. Google ha bisogno di tempo per riscansionare il vecchio URL, elaborare il redirect e aggiornare il proprio indice. Rimuovere un redirect 301 troppo presto significa che i link esterni al vecchio URL torneranno a generare 404.

### Troppi redirect 301 possono rallentare un sito?

I redirect individuali aggiungono millisecondi. Ma le catene di redirect (pagina A > B > C) moltiplicano quel ritardo. Mantieni i redirect a un hop massimo. Un sito con migliaia di redirect 301 puliti è a posto. Sono le catene e i loop a causare problemi.

### Qual è la differenza tra un redirect 301 e un 302?

Un [redirect 301 è permanente](/glossary/301-redirect); un [redirect 302 è temporaneo](/glossary/302-redirect). Usa il 301 quando il vecchio URL è andato per sempre. Usa il 302 quando la pagina originale tornerà (contenuti stagionali, manutenzione temporanea). Google trasmette la link equity in modo più affidabile attraverso i redirect 301.

---

Vuoi un'architettura del sito costruita per la SEO fin dal primo giorno? theStacc pubblica 30 articoli SEO-ottimizzati sul tuo sito ogni mese con strutture URL pulite e link interni corretti. Automaticamente. [Inizia a $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: Reindirizzamenti e Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Moz: Guida ai Reindirizzamenti](https://moz.com/learn/seo/redirection)
- [Ahrefs: Redirect 301 per la SEO](https://ahrefs.com/blog/301-redirects/)
- [Search Engine Journal: Redirect 301 vs 302](https://www.searchenginejournal.com/301-vs-302-redirects/299843/)
- [Google Search Console Help: Correggere gli errori di scansione](https://support.google.com/webmasters/answer/7440203)
