---
term: "Core Web Vitals"
slug: "core-web-vitals"
definition: "I Core Web Vitals sono le tre metriche di Google per misurare la page experience: LCP, INP e CLS. Scopri cosa misurano e come migliorarle."
category: "SEO"
difficulty: "Intermediate"
keyword: "cosa sono core web vitals"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "page-speed"
  - "technical-seo"
  - "google-search-console"
  - "largest-contentful-paint-lcp"
  - "cumulative-layout-shift-cls"
---

## Cosa sono i Core Web Vitals?

I Core Web Vitals sono un insieme di tre metriche specifiche che Google usa per misurare quanto una pagina web risulti veloce, reattiva e visivamente stabile per gli utenti reali.

Google le ha introdotte nel 2020 e le ha rese un segnale di ranking ufficiale nel 2021. Fanno parte del discorso più ampio sulla [velocità di pagina](/glossary/page-speed), ma sono più precise. Invece di un singolo "punteggio di velocità", i Core Web Vitals scompongono l'esperienza utente in tre componenti misurabili. Caricamento, interattività e stabilità visiva.

Secondo i dati di Google, le pagine che rispettano tutte e tre le soglie registrano il 24 % in meno di abbandoni. Non è un miglioramento UX di poco conto. È una via diretta verso più conversioni e [traffico organico](/glossary/organic-traffic) migliore.

## Perché i Core Web Vitals sono importanti?

Ignorare i Core Web Vitals non distruggerà i tuoi ranking dall'oggi al domani. Ma, a parità di condizioni, Google preferirà le pagine che superano queste soglie a quelle che non lo fanno.

- **Fattore di ranking dal 2021**. Google ha confermato i Core Web Vitals come parte dei suoi segnali di page experience, e questo influisce direttamente sulla tua posizione nei [risultati di ricerca](/glossary/serp)
- **24 % di abbandoni in meno**. Le pagine che superano tutte e tre le soglie trattengono gli utenti molto più a lungo (Google, 2021)
- **Impatto mobile-first**. Con l'[indicizzazione mobile-first](/glossary/mobile-first-indexing) come standard, le pagine mobili lente sono le più colpite
- **Correlazione con i ricavi pubblicitari**. Gli editori che hanno migliorato i punteggi CWV hanno visto fino al 15 % in più di entrate pubblicitarie grazie a sessioni più lunghe

Se gestisci una piccola attività o un'impresa locale, questo conta perché probabilmente nemmeno i tuoi concorrenti stanno ottimizzando i CWV. Ottenere un punteggio che passa quando loro non lo fanno è un vantaggio reale.

## Come funzionano i Core Web Vitals

Google raccoglie i dati dei Core Web Vitals dagli utenti reali di Chrome tramite il Chrome User Experience Report (CrUX). Significa che i tuoi punteggi vengono da visitatori reali. Non da una simulazione di laboratorio.

### Largest Contentful Paint (LCP)

[LCP](/glossary/largest-contentful-paint-lcp) misura quanto tempo impiega a caricarsi l'elemento visibile più grande della tua pagina. Pensa: l'immagine hero, un grande blocco di testo o la miniatura di un video. Google lo vuole sotto i 2,5 secondi. Oltre i 4 secondi è considerato "scarso".

La soluzione di solito è semplice: comprimi le immagini, usa una [CDN](/glossary/content-delivery-network-cdn), rinvia le risorse fuori schermo e migliora il tempo di risposta del server.

### Interaction to Next Paint (INP)

INP ha sostituito il First Input Delay (FID) a marzo 2024. Misura quanto velocemente la tua pagina risponde alle interazioni dell'utente. Click, tap e pressioni di tasti. Per l'intera visita, non solo la prima interazione.

Un buon INP è sotto i 200 millisecondi. Se la tua pagina si congela per mezzo secondo quando qualcuno clicca un pulsante, è un punteggio bocciato. JavaScript pesante è il colpevole abituale.

### Cumulative Layout Shift (CLS)

[CLS](/glossary/cumulative-layout-shift-cls) misura la stabilità visiva. Hai mai provato a toccare un pulsante e la pagina è saltata perché un annuncio o un'immagine si è caricata in ritardo? Quello è layout shift.

Google vuole un CLS sotto 0,1. Le cause più comuni: immagini senza dimensioni definite, annunci iniettati sopra il contenuto e font web che cambiano dimensione durante il caricamento.

## Tipi di valutazione dei Core Web Vitals

I dati dei Core Web Vitals arrivano in due varianti, e spesso raccontano storie diverse:

- **Dati di campo (RUM)**. Real User Metrics raccolte dai visitatori reali tramite CrUX. È ciò che Google usa per le decisioni di ranking. Le vedi in [Google Search Console](/glossary/google-search-console) e PageSpeed Insights.
- **Dati di laboratorio**. Test di performance simulati con strumenti come Lighthouse, WebPageTest e Chrome DevTools. Utili per il debug, ma non usati direttamente per i ranking.
- **Livello origine vs. livello URL**. Google valuta i CWV sia a livello di dominio completo sia di singola pagina. Se il sito complessivamente passa ma una landing chiave fallisce, quella pagina può comunque essere penalizzata.
- **Mobile vs. desktop**. I punteggi sono misurati separatamente per mobile e desktop. La maggior parte dei siti rende peggio su mobile, che è la versione che Google privilegia.

Per gli audit di [SEO tecnica](/glossary/technical-seo), parti sempre dai dati di campo. I dati di laboratorio aiutano a trovare il problema, ma quelli di campo ti dicono se il problema sta davvero danneggiando i visitatori reali.

## Esempi di Core Web Vitals

**Esempio 1: la home page lenta di un idraulico**
Un idraulico locale di Milano ha una home con LCP di 4,8 secondi a causa di un'immagine hero non compressa (3,2 MB). Dopo la conversione in WebP e il ridimensionamento corretto, l'LCP scende a 1,9 secondi. Il bounce rate cala del 18 % nel mese successivo.

**Esempio 2: un e-commerce con layout shift**
Uno store Shopify di prodotti per animali ha un CLS di 0,34 perché le immagini prodotto vengono caricate senza attributi width/height. Aggiungere dimensioni esplicite a ogni tag immagine porta il CLS a 0,04. Niente più click accidentali su "Aggiungi al carrello" da parte di acquirenti irritati.

**Esempio 3: un blog appesantito dal JavaScript**
Il blog di un'agenzia di marketing usa 14 script di terze parti. Analytics, widget di chat, embed social, tracker pubblicitari. L'INP è a 480 ms. Dopo un audit e la rimozione di 6 script inutilizzati, l'INP scende a 160 ms. Le pagine create e pubblicate tramite theStacc partono già con codice pulito e ottimizzato. Niente script gonfiati.

## Core Web Vitals vs. velocità di pagina

Si usano come sinonimi. Non dovrebbero esserlo.

| | Core Web Vitals | Velocità di pagina |
|---|---|---|
| **Cosa misura** | 3 metriche UX specifiche (LCP, INP, CLS) | Tempo di caricamento complessivo e punteggio di performance |
| **Fonte dei dati** | Dati utenti reali (CrUX) | Simulazioni in laboratorio (Lighthouse) |
| **Segnale di ranking Google** | Sì, direttamente | Indirettamente (tramite i CWV) |
| **Ambito** | Focalizzato sull'esperienza percepita | Ombrello più ampio della performance |
| **Metrica di esempio** | LCP: 2,1 s | Punteggio PageSpeed: 74/100 |

La [velocità di pagina](/glossary/page-speed) è il concetto più ampio. I Core Web Vitals sono le metriche specifiche che Google effettivamente usa.

## Best practice per i Core Web Vitals

- **Comprimi e dimensiona correttamente tutte le immagini**. Usa i formati WebP o AVIF, e imposta sempre attributi width e height espliciti per evitare il layout shift
- **Riduci al minimo gli script di terze parti**. Ogni script esterno (widget di chat, analytics, tracker pubblicitari) alza l'INP. Fai un audit senza pietà e rimuovi ciò che non serve.
- **Usa una CDN per le risorse statiche**. Servire immagini e CSS da edge server vicini ai tuoi visitatori riduce drasticamente l'LCP
- **Rinvia il JavaScript non critico**. Carica prima il contenuto above-the-fold, poi lascia che gli script secondari si carichino dopo che la pagina è interattiva
- **Monitora i dati di campo ogni mese in Google Search Console**. I punteggi di laboratorio oscillano, ma i dati di campo mostrano se i visitatori reali stanno avendo una buona esperienza. Servizi come theStacc pubblicano automaticamente contenuti che seguono buone pratiche di HTML pulito, riducendo i problemi CWV fin dall'inizio.

## Domande frequenti

### I Core Web Vitals sono un fattore di ranking?

Google ha confermato i Core Web Vitals come segnale di ranking a giugno 2021. Fanno parte del sistema di page experience. L'impatto è reale ma secondario rispetto alla rilevanza dei contenuti e ai [backlink](/glossary/backlinks). Più spareggio che fattore decisivo.

### Cosa ha sostituito il First Input Delay?

Interaction to Next Paint (INP) ha ufficialmente sostituito il FID come Core Web Vital a marzo 2024. INP misura la reattività su tutte le interazioni di una visita, non solo il primo click.

### Come controllo i miei Core Web Vitals?

Usa il report Core Web Vitals di Google Search Console per i dati di campo. PageSpeed Insights ti fornisce sia dati di campo sia di laboratorio per qualsiasi URL. Chrome DevTools e Lighthouse vanno bene per i test locali in fase di sviluppo.

### Qual è un buon punteggio LCP?

Google considera un LCP sotto i 2,5 secondi "buono", tra 2,5 e 4 secondi "da migliorare" e oltre i 4 secondi "scarso". La maggior parte dei siti fatica con l'LCP a causa di immagini non ottimizzate e tempi di risposta del server lenti.

---

Vuoi contenuti che caricano veloci e si posizionano bene senza gestire i dettagli tecnici? theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. In automatico. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google: Web Vitals](https://web.dev/vitals/)
- [Google Search Central: Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/)
- [Web.dev: Interaction to Next Paint (INP)](https://web.dev/inp/)
- [Ahrefs: Core Web Vitals e SEO](https://ahrefs.com/blog/core-web-vitals/)
