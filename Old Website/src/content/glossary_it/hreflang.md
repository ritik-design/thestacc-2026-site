---
term: "hreflang"
slug: "hreflang"
definition: "hreflang è un attributo HTML che indica ai motori di ricerca quale versione linguistica o regionale di una pagina servire a ciascun utente, evitando contenuti duplicati."
category: "SEO"
difficulty: "Advanced"
keyword: "tag hreflang"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "geotargeting"
  - "canonical-url"
  - "meta-robots-tag"
  - "hreflang"
---

## Cos'è hreflang?

hreflang è un attributo HTML (`rel="alternate" hreflang="x"`) che comunica a Google e agli altri motori di ricerca quale lingua e quale paese sono destinatari di una specifica versione di una pagina.

Se il tuo sito ha pagine in più lingue o varianti regionali — italiano per l'Italia e italiano per la Svizzera, ad esempio — il tag hreflang impedisce a Google di considerarle [contenuti duplicati](/glossary/duplicate-content). Senza, Google sceglie una versione e la mostra ovunque. Raramente quella giusta per ciascun pubblico.

Uno studio di Ahrefs ha rilevato che solo il 19 % dei siti multilingue implementa hreflang correttamente. Il restante 81 % presenta errori: tag di ritorno mancanti, URL rotti, codici sbagliati. È uno degli elementi di SEO tecnico configurati male più di frequente.

## Perché hreflang è importante?

Una corretta implementazione di hreflang determina se il pubblico giusto vedrà la pagina giusta.

- **Distribuzione linguistica corretta**. Chi cerca da Milano vede la versione italiana, chi cerca da Lugano vede quella svizzera — senza redirect manuali né JavaScript
- **Protezione dal filtro dei duplicati**. Google capisce che le tue pagine `/it/` e `/de/` non sono copie ma traduzioni intenzionali
- **Esperienza utente migliore**. Atterrare su una pagina nella propria lingua riduce il bounce rate e aumenta la conversione
- **Prezzi e cataloghi regionali**. Gli e-commerce con prezzi, valute o prodotti diversi per paese hanno bisogno di hreflang per servire la versione corretta in ogni mercato

Qualsiasi azienda che opera in più paesi o lingue ha bisogno di hreflang. Senza eccezioni.

## Come funziona hreflang

### Metodi di implementazione

Esistono tre modi per implementare hreflang: tag `<link>` nell'`<head>` HTML, intestazioni HTTP (per PDF e file non HTML), oppure voci nella tua [sitemap XML](/glossary/xml-sitemap). Google consiglia di scegliere un metodo e mantenerlo. L'approccio via sitemap è il più gestibile per siti grandi con centinaia di varianti linguistiche.

### La regola del ritorno bidirezionale

Ogni annotazione hreflang deve essere reciproca. Se la pagina A afferma "il mio equivalente francese è la pagina B", la pagina B deve dichiarare "il mio equivalente italiano è la pagina A". I tag di ritorno mancanti sono l'errore di implementazione numero uno. Senza reciprocità, Google ignora completamente le annotazioni.

### Il tag x-default

Il valore `x-default` dice a Google quale versione mostrare quando non c'è una corrispondenza precisa di lingua o regione. Il tuo piano B. Di solito la versione inglese o quella del mercato principale. Senza `x-default`, Google decide da solo. E non sempre azzecca.

## Esempi di hreflang

**Esempio 1: un negozio online con versioni Italia e Svizzera**
Un retailer milanese gestisce `example.com/it-it/scarpe` (prezzi in euro, IVA italiana) e `example.com/it-ch/scarpe` (prezzi in franchi, normativa svizzera, costi di spedizione differenti). Senza hreflang, Google potrebbe servire la versione italiana a un utente di Lugano. Con il tag hreflang corretto, ogni pubblico vede prezzi e logistica adeguati. L'[URL canonico](/glossary/canonical-url) resta indipendente per ogni versione.

**Esempio 2: un'azienda SaaS con pagine tradotte**
Uno strumento di project management ha la home page in 8 lingue. Il team implementa hreflang tramite sitemap XML, con ogni versione che rimanda a tutte le altre. Chi cerca in tedesco arriva su `/de/`, chi cerca in spagnolo su `/es/`, e tutti gli altri ricadono sulla versione inglese marcata `x-default`.

Vuoi pubblicare contenuti internazionali senza scervellarti con il cablaggio di hreflang? theStacc pubblica 30 articoli ottimizzati per la SEO sul tuo sito ogni mese. Automaticamente. [Inizia con 1 $ →](https://app.thestacc.com)

## Domande frequenti

### hreflang influisce sul ranking?

hreflang non migliora il ranking direttamente. Decide soltanto quale versione appare in ciascun mercato. Ma servire la lingua giusta al pubblico giusto migliora i segnali di engagement — bounce rate più basso, [tempo di permanenza](/glossary/dwell-time) più lungo — che possono influenzare il posizionamento nel tempo.

### hreflang funziona per la stessa lingua in paesi diversi?

Sì. È proprio uno dei suoi usi migliori. Inglese USA (`en-us`), inglese Regno Unito (`en-gb`) e inglese Australia (`en-au`) possono coesistere con annotazioni separate. Google usa il codice paese, non solo quello di lingua, per scegliere la versione da servire.

### Cosa succede se hreflang è implementato male?

Google ignora completamente le annotazioni e decide da solo quale versione mostrare. Nessuna penalizzazione. Solo perdita di controllo su quale pagina compare in ciascun mercato. Il report Targeting internazionale della Google Search Console aiuta a individuare gli errori hreflang in dettaglio.

---

Vuoi guadagnare visibilità internazionale senza costruire un team SEO in ogni paese? theStacc pubblica 30 articoli ottimizzati per la SEO sul tuo sito ogni mese. Automaticamente. [Inizia con 1 $ →](https://app.thestacc.com)

## Fonti

- [Google Search Central: implementazione di hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Ahrefs: guida ai tag hreflang](https://ahrefs.com/blog/hreflang-tags/)
- [Moz: la guida definitiva a hreflang](https://moz.com/learn/seo/hreflang-tag)
