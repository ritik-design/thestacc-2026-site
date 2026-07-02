---
term: "Crawl budget"
slug: "crawl-budget"
definition: "Il crawl budget è il numero di pagine che un bot di motore di ricerca scansionerà sul tuo sito entro un certo periodo. Gestirlo bene assicura che le tue pagine più importanti siano priorizzate."
category: "SEO"
difficulty: "Intermediate"
keyword: "crawl budget"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "crawling"
  - "indexing"
  - "robots-txt"
  - "site-architecture"
  - "xml-sitemap"
---

## Cosa è il crawl budget?

Il crawl budget è il numero totale di URL che Googlebot recupererà dal tuo sito durante un dato periodo, determinato da una combinazione di limite di tasso di scansione e domanda di scansione.

Google non dà attenzione illimitata a ogni sito. Googlebot alloca risorse basate sulla dimensione, salute e importanza percepita del tuo sito. Per la maggior parte dei siti piccoli e medi (sotto le 10.000 pagine), il crawl budget non è una preoccupazione. Ma per siti più grandi. Negozi e-commerce, editori, directory. Può essere la differenza tra contenuto nuovo indicizzato in ore o settimane.

Gary Illyes di Google ha dichiarato che il crawl budget "non è qualcosa di cui la maggior parte dei siti debba preoccuparsi", ma ha anche confermato che sprecarlo su URL di basso valore può ritardare l'[indicizzazione](/glossary/indexing) di pagine importanti.

## Perché il crawl budget è importante?

Se Googlebot non può raggiungere le tue pagine chiave, non possono posizionarsi. Punto.

- **Indicizzazione più veloce**. L'uso efficiente del crawl budget significa che il contenuto nuovo viene scoperto e indicizzato prima
- **Pagine prioritizzate**. Quando Googlebot spreca budget su [contenuto duplicato](/glossary/duplicate-content), pagine 404 o URL parametriche, le tue pagine principali potrebbero non essere scansionate affatto durante quel ciclo
- **Segnale di salute del sito**. Un sito facile da scansionare segnala qualità ai sistemi di Google, mentre trappole di scansione ed errori fanno l'opposto
- **Scalare il contenuto**. Siti che pubblicano 30+ pagine al mese hanno bisogno che Googlebot tenga il passo con il nuovo contenuto, rendendo l'efficienza di scansione critica

Qualsiasi sito con più di alcune migliaia di pagine dovrebbe gestire attivamente il crawl budget.

## Come funziona il crawl budget

### Limite di tasso di scansione

Google imposta una velocità massima di scansione per evitare di sovraccaricare il tuo server. Se il tuo server risponde lentamente o restituisce errori, Googlebot si ritira. Hosting veloce e affidabile aumenta direttamente il tuo limite di tasso di scansione.

### Domanda di scansione

Anche se Googlebot *potesse* scansionare di più, lo farà solo se ha una ragione. Pagine popolari con molti [backlink](/glossary/backlinks) vengono ri-scansionate frequentemente. Pagine obsolete e di bassa autorità potrebbero passare mesi tra le visite. Aggiornare il contenuto e guadagnare link aumenta la domanda di scansione per URL specifiche.

### Sprechi comuni di crawl budget

Navigazione faceted, ID di sessione negli URL, scroll infinito senza paginazione adeguata, [link rotti](/glossary/broken-link) che restituiscono [errori 404](/glossary/404-error) e contenuto duplicato attraverso variazioni di parametri tutti consumano crawl budget. Usa [robots.txt](/glossary/robots-txt) e [tag noindex](/glossary/noindex) per impedire a Googlebot di sprecare tempo su queste pagine.

## Esempi di crawl budget

**Esempio 1: Un e-commerce con URL di filtro**
Il sito di un negozio di mobili genera 50.000 URL uniche da combinazioni di filtri (colore, dimensione, materiale, prezzo). Solo 3.000 sono pagine prodotto effettive. Senza bloccare gli URL di filtro tramite robots.txt, Googlebot spende il 94 % del suo crawl budget su pagine che non dovrebbero essere indicizzate.

**Esempio 2: Un blog ricco di contenuto**
Un'azienda pubblica 30 articoli al mese tramite theStacc. Con un'[architettura del sito](/glossary/site-architecture) pulita e sitemap XML, Googlebot scopre e indicizza i nuovi post entro 48 ore. Un concorrente che pubblica lo stesso volume su un sito mal strutturato aspetta 2-3 settimane per l'indicizzazione.

### Strumenti e risorse

| Strumento | Scopo | Prezzo |
|---|---|---|
| **[Google Search Console](/glossary/google-search-console)** | Dati di performance di ricerca | Gratis |
| **Ahrefs** | Backlink, parole chiave, audit del sito | Da $99/mese |
| **Semrush** | Piattaforma SEO all-in-one | Da $130/mese |
| **Screaming Frog** | Analisi tecnica della scansione | Gratis (500 URL) |
| **theStacc** | Pubblicazione automatizzata di contenuti SEO | Da $99/mese |

## Domande frequenti

### Come controllo il mio crawl budget?

Il report Statistiche di scansione di Google Search Console mostra quante pagine Googlebot scansiona al giorno, tempo medio di risposta e tendenze di richieste di scansione. Controllalo in Impostazioni > Statistiche di scansione. Cerca pattern. Una caduta improvvisa nel tasso di scansione spesso segnala problemi del server.

### Il crawl budget influenza i siti piccoli?

Per siti sotto le 1.000 pagine, il crawl budget raramente conta. Googlebot può facilmente gestire siti piccoli in una singola sessione di scansione. Inizia a prestare attenzione quando superi le 10.000 URL indicizzabili o noti un'indicizzazione lenta del nuovo contenuto.

### Come miglioro il crawl budget?

Rimuovi o noindexa pagine di basso valore, ripara errori di scansione, migliora i tempi di risposta del server, invia una [sitemap XML](/glossary/xml-sitemap) aggiornata e costruisci link interni a pagine importanti. Rendi facile per Googlebot trovare e accedere velocemente al tuo miglior contenuto.

---

Stai pubblicando contenuto in modo coerente? Assicurati che Google possa tenere il passo. theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. Automaticamente. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: Gestione del crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central Blog: Cosa significa crawl budget](https://developers.google.com/search/blog/2017/01/what-crawl-budget-means-for-googlebot)
- [Ahrefs: Crawl budget e SEO](https://ahrefs.com/blog/crawl-budget/)
- [Moz: Crawl budget spiegato](https://moz.com/blog/crawl-budget)
