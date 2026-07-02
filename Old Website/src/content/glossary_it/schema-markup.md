---
term: "Schema Markup"
slug: "schema-markup"
definition: "Schema Markup è codice standardizzato (in genere JSON-LD) che aggiungi alle pagine perché i motori di ricerca capiscano i contenuti e mostrino risultati ricchi."
category: "SEO"
difficulty: "Intermediate"
keyword: "cos'è schema markup"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "rich-results"
  - "serp"
  - "technical-seo"
  - "json-ld"
  - "e-e-a-t"
---

## Cos'è lo Schema Markup?

**Schema Markup è un vocabolario di dati strutturati che aggiungi al tuo HTML per dire ai motori di ricerca cosa rappresenta esattamente il tuo contenuto: un prodotto, una ricetta, un evento, un'attività, una FAQ.**

Senza schema, Google deve indovinare di cosa parla la tua pagina. Con schema, gli consegni un diagramma con etichette. Il markup segue lo standard Schema.org, mantenuto congiuntamente da Google, Microsoft, Yahoo e Yandex.

Uno studio di Milestone Research ha rilevato che le pagine con schema markup si posizionano in media 4 posizioni più in alto rispetto a quelle senza. Non perché schema sia un fattore di ranking diretto – Google ha detto che non lo è. Ma i [risultati ricchi](/glossary/rich-results) generati da schema fanno schizzare in alto il tasso di clic, e un CTR migliore col tempo influisce davvero sui posizionamenti.

## Perché i dati strutturati contano?

La maggior parte dei siti ancora non usa schema. Un'opportunità per chi è disposto a dedicare 30 minuti all'implementazione.

- **Risultati ricchi nella ricerca**. Stelle di valutazione, FAQ a tendina, fasce di prezzo e date di eventi compaiono direttamente nella [SERP](/glossary/serp). Questi elementi visivi possono aumentare il CTR del 20–30 %.
- **Migliore visibilità in AI**. Le AI Overviews di Google e altre esperienze guidate dall'intelligenza artificiale attingono ai dati strutturati. Schema rende i tuoi contenuti più facili da citare per le macchine.
- **Presenza locale rafforzata** – lo [schema LocalBusiness](/glossary/localbusiness-schema) invia orari, indirizzo e recensioni direttamente ai pannelli di conoscenza di Google e al [local pack](/glossary/local-pack).
- **Pronto per la ricerca vocale**. Quando qualcuno fa una domanda a un assistente vocale, i dati strutturati aiutano la tua risposta a emergere. FAQ e How-To schema brillano qui.

Se stai investendo in contenuti [SEO](/glossary/seo) ma non aggiungi schema, stai lasciando visibilità sul tavolo.

## Come funziona lo Schema Markup

Schema vive nell'HTML della tua pagina. I crawler lo leggono, lo validano e lo usano per generare risultati di ricerca arricchiti.

### Il formato del codice

Esistono tre formati: JSON-LD, Microdata e RDFa. Google raccomanda JSON-LD. È un blocco di script che inserisci nella sezione `<head>`. Non si mescola con l'HTML visibile, quindi è più pulito da gestire e meno propenso a rompere il layout.

### Il processo di validazione

Dopo aver aggiunto schema, il report Risultati Multimediali di Google Search Console mostra se il markup è valido. Gli errori – campi obbligatori mancanti, tipi sbagliati – impediscono ai risultati ricchi di apparire. Lo strumento Rich Results Test di Google ti permette di controllare singoli URL prima di un rilascio su tutto il sito.

### Come Google lo elabora

Googlebot esegue la scansione della pagina, analizza il JSON-LD e lo confronta con i tipi di schema noti. Se tutto torna e la pagina rispetta le linee guida di qualità, l'elenco arricchito appare nella ricerca entro pochi giorni o settimane. Non ogni schema valido attiva un risultato ricco. Google decide in base al contesto della query e alla qualità della pagina.

## Tipi di Schema Markup

Schema.org elenca oltre 800 tipi. Ma per la maggior parte delle aziende, una manciata copre il 90 % dei casi d'uso:

- **Article schema**. Dice a Google che la pagina è un post di blog o un articolo di news. Aiuta con Google Discover e i caroselli di notizie.
- **FAQ schema**. Aggiunge coppie domanda-risposta espandibili direttamente nel tuo risultato. Forte impatto per query informazionali.
- **LocalBusiness schema**. Invia nome, indirizzo, orari e recensioni a Google. Imprescindibile per la [SEO locale](/glossary/local-seo).
- **Product schema**. Mostra prezzo, disponibilità e valutazioni nella ricerca. Critico per l'eCommerce.
- **How-To schema**. Visualizza istruzioni passo-passo con immagini nei risultati. Funziona benissimo per i tutorial.
- **Review/Rating schema**. Quelle stelline gialle che vedi sotto i risultati. Aumentano il CTR in modo netto.

Lo schema giusto dipende dal tipo di pagina. La pagina di servizio di un idraulico ha bisogno di LocalBusiness. Un post di blog ha bisogno di Article ed eventualmente di FAQ.

## Esempi di Schema Markup

**Esempio 1: Studio dentistico con FAQ schema**
Una dentista a Milano aggiunge FAQ schema alla pagina del servizio "Sbiancamento denti" con 5 domande tipiche dei pazienti. Il suo risultato nella ricerca ora mostra Q&A espandibili, occupando 3 volte lo spazio visivo dei concorrenti. I clic verso quella pagina salgono del 35 % in 2 mesi.

**Esempio 2: Azienda di climatizzazione con LocalBusiness schema**
Un'azienda di impianti di climatizzazione aggiunge LocalBusiness schema con area di servizio, orari e valutazione aggregata (4,8 stelle da oltre 200 recensioni). Google mostra le stelle direttamente nei risultati organici – non solo nel map pack. L'azienda registra un aumento evidente delle chiamate dalla ricerca organica.

**Esempio 3: Blog SaaS con Article schema**
Un'azienda software B2B pubblica guide how-to ogni settimana. Dopo aver aggiunto Article schema con informazioni autore e date di pubblicazione, i suoi post iniziano a comparire in Google Discover. Il solo traffico da Discover aggiunge il 15 % alle visite organiche mensili.

## Schema Markup vs. Rich Snippets

I due termini vengono usati come sinonimi. Non dovrebbero esserlo.

| | Schema Markup | Rich Snippets / Risultati ricchi |
|---|---|---|
| **Cos'è** | Codice che aggiungi alle tue pagine | Elenchi arricchiti che Google mostra |
| **Chi lo controlla** | Tu (il webmaster) | Google (decide se mostrarli) |
| **Garantito?** | Il markup puoi sempre aggiungerlo | Google può mostrarli oppure no |
| **Scopo** | Comunicare il significato della pagina ai crawler | Migliorare l'aspetto visivo nelle [SERP](/glossary/serp) |
| **Esempio** | Script JSON-LD nel tuo HTML | Stelle di valutazione sotto il tuo risultato |

Schema markup è l'input. I risultati ricchi sono il (possibile) output. Aggiungere il markup non garantisce elenchi arricchiti. Ma senza, non li avrai mai.

## Best practice per Schema Markup

- **Parti da ciò che conta di più**. Non provare ad aggiungere tutti i tipi di schema in una volta. Sei un'attività locale? Inizia da LocalBusiness e FAQ. Aggiungi il resto strada facendo.
- **Usa JSON-LD, non Microdata**. Google lo preferisce. È più semplice da implementare, più facile da debuggare e non sporca l'HTML.
- **Valida ogni pagina**. Fai passare ogni nuovo schema dal Rich Results Test di Google prima di pubblicare. Un campo mancante può invalidare l'intero blocco.
- **Tieni schema accurato**. Se cambiano gli orari, aggiorna lo schema. Dati strutturati inesatti violano le linee guida di Google e possono farti revocare i risultati ricchi.
- **Abbina schema a contenuti di qualità**. Schema su pagine povere non genera risultati ricchi. Servizi come theStacc pubblicano 30 articoli ottimizzati SEO al mese. Ognuno è un'occasione per aggiungere Article e FAQ schema che davvero conquistino i rich results.

## Domande frequenti

### Schema markup è un fattore di ranking?

Google dice che schema non è un fattore di ranking diretto. Ma le pagine con schema ottengono [risultati ricchi](/glossary/rich-results), che alzano il CTR. Un CTR più alto invia segnali di engagement positivi, che possono migliorare i posizionamenti in modo indiretto.

### Come aggiungo schema al mio sito?

Il metodo più semplice è JSON-LD: un blocco script nella sezione `<head>` della pagina. Plugin WordPress come Yoast e RankMath lo generano in automatico. Per siti su misura, usa lo Structured Data Markup Helper di Google.

### Schema funziona per le piccole imprese?

Assolutamente. Le attività locali vedono spesso l'impatto maggiore perché LocalBusiness e FAQ schema sono sottoutilizzati dai concorrenti piccoli. Aggiungere uno schema base a un sito locale di 10 pagine richiede meno di un'ora.

### Quanto tempo per vedere i risultati ricchi?

Dopo aver aggiunto schema valido, Google di solito lo elabora in pochi giorni o entro 2 settimane. Controlla lo stato nel report Risultati Multimediali di Google Search Console.

---

Vuoi contenuti SEO ottimizzati e pubblicati senza muovere un dito? theStacc pubblica 30 articoli sul tuo sito ogni mese. Automaticamente. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: Come funzionano i dati strutturati](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Schema.org](https://schema.org/)
- [Milestone Research: L'impatto di Schema Markup sui ranking](https://www.milestoneinternet.com/thought-leadership/research/schema-markup-drives-results)
- [Moz: Guida per principianti ai dati strutturati](https://moz.com/blog/beginners-guide-to-structured-data)
