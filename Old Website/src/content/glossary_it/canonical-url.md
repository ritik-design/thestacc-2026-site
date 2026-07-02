---
term: "URL canonica / Canonicalizzazione"
slug: "canonical-url"
definition: "Una URL canonica indica ai motori di ricerca quale versione di una pagina è la copia principale. Scopri come la canonicalizzazione previene problemi di contenuto duplicato e come usarla correttamente."
category: "SEO"
difficulty: "Intermediate"
keyword: "url canonica"
date: "2026-04-26"
lastUpdated: "2026-04-26"
relatedTerms:
  - "duplicate-content"
  - "301-redirect"
  - "indexing"
  - "crawl-budget"
  - "technical-seo"
---

## Cosa è una URL canonica?

Una URL canonica è un elemento HTML che indica ai motori di ricerca quale versione di una pagina è la copia preferita e autoritativa quando più URL servono lo stesso contenuto o uno molto simile.

Nell'`<head>` di una pagina appare così: `<link rel="canonical" href="https://example.com/preferred-page">`. Perché esiste? Perché sul web moderno, un singolo contenuto vive spesso a più URL. Stessa pagina prodotto accessibile con e senza www, con e senza slash finali, con parametri di tracking, attraverso navigazione filtrata. Google vede ogni URL come pagina separata. Senza un tag canonical, Google deve indovinare quale indicizzare. E spesso indovina male.

I dati di Semrush da uno studio di 150.000 siti hanno trovato che il 65 % dei domini ha qualche forma di problema di [contenuto duplicato](/glossary/duplicate-content). I tag canonical sono lo strumento principale per risolverlo in scala senza ristrutturare l'intero sito.

## Perché la canonicalizzazione è importante?

Il contenuto duplicato non è una penalità. Google l'ha detto chiaramente. Ma crea problemi reali di SEO che ti costano traffico e posizionamenti.

- **La link equity viene divisa**. Se 30 siti linkano alla tua pagina ma metà linka a `example.com/page` e metà a `example.com/page/`, l'autorità è divisa. Una canonical consolida tutti i segnali su un'URL, rendendola più forte.
- **Il [crawl budget](/glossary/crawl-budget) viene sprecato**. Googlebot ha un crawl budget finito per il tuo sito. Ogni URL duplicata che scansiona è una pagina che non ha scansionato. Per siti grandi con migliaia di pagine, questo impatta direttamente quanto velocemente i nuovi contenuti vengono [indicizzati](/glossary/indexing).
- **La pagina sbagliata potrebbe posizionarsi**. Senza canonicalizzazione, Google sceglie la versione che pensa sia migliore. Potrebbe essere la tua URL mobile, una URL con parametri pesanti, o una pagina di categoria filtrata. Non la versione pulita e ottimizzata che vuoi posizionare.
- **Le analytics si frammentano**. Dati di traffico ed engagement si distribuiscono su più URL. Le tue performance reali sembrano più deboli di quanto sono perché le metriche sono divise.

Se il tuo sito ha più di una manciata di pagine, hai quasi certamente contenuto duplicato che la canonicalizzazione risolverebbe.

## Come funziona la canonicalizzazione

Il tag canonical è un suggerimento, non una direttiva. Google generalmente lo rispetta. Ma non sempre.

### Canonical auto-referenzianti

Ogni pagina del tuo sito dovrebbe puntare il proprio tag canonical a se stessa. Si chiama canonical auto-referenziante. Dice a Google: "Questa è l'URL preferita per questo contenuto, anche se la scopri attraverso un percorso diverso." La maggior parte delle piattaforme [CMS](/glossary/content-management-system) e plugin di [SEO tecnico](/glossary/technical-seo) gestisce questo automaticamente.

### Canonical cross-domain

Se sindachi contenuto. Pubblicando lo stesso articolo sul tuo blog e su Medium o LinkedIn. Puoi impostare una canonical cross-domain che punta dalla versione sindacata al tuo originale. Questo dice a Google di accreditare la [link equity](/glossary/link-equity) e i segnali di ranking al tuo dominio, non alla copia sindacata.

### Canonical vs. scelta di Google

Google tratta i tag canonical come un suggerimento forte, non un comando. Se il tag canonical confligge con altri segnali (sitemap, link interni, schemi di redirect), Google può ignorare la tua preferenza. Per questo la coerenza conta. Il tuo canonical, i tuoi [link interni](/glossary/internal-link), la tua sitemap e i tuoi [redirect 301](/glossary/301-redirect) dovrebbero tutti puntare alla stessa URL preferita.

### Variazioni comuni di URL canonica

Questi sono gli scenari di contenuto duplicato più frequenti che la canonicalizzazione risolve:

- `http://` vs `https://`
- `www.example.com` vs `example.com`
- `/page` vs `/page/` (slash finale)
- `/page` vs `/page?utm_source=google&utm_medium=cpc`
- `/page` vs `/page?ref=homepage`
- URL mobili (`m.example.com`) vs URL desktop

Ogni variazione è un'URL separata per Google. I tag canonical le uniscono in una.

## Tipi di canonicalizzazione

Ci sono modi multipli per segnalare la tua URL preferita. Il tag canonical è il più comune, ma non l'unica opzione.

- **Tag canonical HTML**. Il tag `<link rel="canonical">` nell'`<head>` della pagina. Più flessibile, funziona su qualsiasi pagina, facile da implementare.
- **Canonical in header HTTP**. Inviato come header `Link:` nella risposta HTTP. Usato per file non HTML (PDF, immagini) dove non puoi aggiungere tag HTML.
- **[Redirect 301](/glossary/301-redirect)**. Reindirizza permanentemente le URL duplicate alla versione preferita. Più forte di un tag canonical perché utenti e bot possono accedere solo all'URL preferita.
- **Segnali di [sitemap XML](/glossary/xml-sitemap)**. Includere solo URL canoniche nella tua sitemap rinforza quali versioni preferisci. Non un metodo di canonicalizzazione diretto, ma un segnale di supporto.
- **Coerenza nei link interni**. Linkare sempre alla stessa versione di una URL nel tuo sito invia a Google un segnale chiaro sulla tua versione preferita.

Per la maggior parte dei siti, il tag canonical HTML combinato con link interni coerenti gestisce oltre il 90 % dei casi.

## Esempi di URL canonica

**Esempio 1: Un e-commerce con URL pesanti di parametri**
La pagina prodotto di un negozio di abbigliamento vive a `/scarpe-running-blu`. Ma filtrare per taglia genera `/scarpe-running-blu?size=10`, e i codici di tracking aggiungono `/scarpe-running-blu?utm_source=email`. Tutte e tre mostrano lo stesso prodotto. Senza tag canonical, Google potrebbe indicizzare l'URL parametrica invece di quella pulita. Aggiungere `<link rel="canonical" href="/scarpe-running-blu">` a tutte e tre le versioni risolve istantaneamente.

**Esempio 2: Un'attività multi-località con pagine di servizio duplicate**
Un franchising di idraulici ha pagine di servizio per ogni città: `/milano/spurgo`, `/roma/spurgo`, `/napoli/spurgo`. Il contenuto è 90 % identico con solo il nome della città scambiato. Queste pagine non dovrebbero canonicalizzarsi tra loro (mirano a [parole chiave locali](/glossary/local-keywords) diverse), ma ognuna dovrebbe auto-referenziarsi. La vera soluzione è rendere ogni pagina genuinamente unica con contenuto specifico della città. Qualcosa che theStacc gestisce generando articoli specifici per location automaticamente.

**Esempio 3: Un blog che sindaca contenuto su Medium**
Un'azienda B2B ripubblica i suoi post di blog su Medium per esposizione extra. Senza un tag canonical, Google potrebbe posizionare la versione Medium invece dell'originale. Aggiungendo una URL canonica che punta al blog dell'azienda su ogni post Medium (Medium lo supporta nelle impostazioni), tutti i segnali di ranking fluiscono al dominio originale. Il [traffico organico](/glossary/organic-traffic) va al tuo sito, non a quello di Medium.

## URL canonica vs. redirect 301

Entrambi risolvono problemi di contenuto duplicato. La scelta giusta dipende se la pagina duplicata deve rimanere accessibile.

| | URL canonica | [Redirect 301](/glossary/301-redirect) |
|---|---|---|
| **L'utente vede** | Entrambe le pagine sono accessibili | L'utente è inviato alla pagina preferita |
| **Forza del segnale** | Suggerimento forte (Google può ignorare) | Definitivo (redirect forzato) |
| **Usa quando** | Entrambe le URL devono esistere (parametri, sindacazione) | URL vecchia non dovrebbe essere più visitata |
| **Link equity** | Consolidata sull'URL canonica | Passa ~95-99 % alla destinazione |
| **Esempio** | Pagina prodotto con parametri di filtro | URL vecchia di blog spostata a nuova struttura |

Quando la pagina duplicata deve rimanere accessibile (URL tracciate, risultati filtrati, contenuto sindacato), usa una canonical. Quando l'URL vecchia è morta e sepolta, usa una 301.

## Best practice per URL canoniche

- **Auto-referenzia ogni pagina**. Anche le pagine senza duplicati dovrebbero avere un tag canonical auto-referenziante. È una rete di sicurezza contro URL duplicate inaspettate da parametri, ID di sessione o stranezze del CMS.
- **Usa URL assolute, non relative**. Scrivi sempre l'URL completa: `https://example.com/page`. Non `/page`. Le canonical relative possono causare problemi con la risoluzione di protocollo e dominio.
- **Punta i canonical a pagine indicizzabili**. Non impostare mai un canonical su una pagina che è [noindex](/glossary/noindex), reindirizzata o restituisce un [404](/glossary/404-error). Confonde Google e vanifica lo scopo.
- **Audita i canonical dopo le migrazioni del sito**. Cambi di CMS, spostamenti di dominio e ridisegni rompono frequentemente i tag canonical. Esegui una scansione con Screaming Frog o Sitebulb dopo il lancio per verificare che ogni pagina punti al canonical corretto.
- **Mantieni i tuoi segnali coerenti**. Il tuo tag canonical, sitemap, link interni e hreflang (per siti internazionali) dovrebbero tutti concordare sull'URL preferita. Quando i segnali confliggono, Google fa la sua scelta. E potrebbe non essere quella che vuoi. theStacc pubblica tutti gli articoli con tag canonical appropriati e strutture URL pulite integrate.

## Domande frequenti

### I tag canonical passano link equity?

Sì. Google consolida i segnali di ranking dalle pagine duplicate all'URL canonica. Se 10 siti linkano a una versione parametrica della tua pagina e il canonical punta alla versione pulita, la versione pulita ottiene il beneficio di quei link.

### Posso canonicalizzare a un dominio diverso?

Sì. I canonical cross-domain dicono a Google che il contenuto originale vive su un dominio diverso. Caso d'uso comune: sindacare contenuto su Medium, LinkedIn o siti partner mantenendo il tuo dominio come fonte canonica.

### Cosa succede se il mio tag canonical è sbagliato?

Google può ignorarlo. Se il canonical punta a una pagina con contenuto completamente diverso, Google riconosce il disallineamento e indicizzerà le URL indipendentemente. I tag canonical funzionano solo quando le pagine hanno contenuto sostanzialmente simile.

### Come controllo i miei tag canonical?

Visualizza il sorgente della pagina e cerca `rel="canonical"`. O usa [Google Search Console](/glossary/google-search-console). Lo strumento di Ispezione URL mostra quale canonical Google ha selezionato per qualsiasi pagina. Se il canonical scelto da Google differisce dal tuo, c'è un conflitto nei tuoi segnali.

---

Vuoi ogni articolo pubblicato con tag canonical appropriati, URL pulite e [SEO tecnico](/glossary/technical-seo) gestito automaticamente? theStacc pubblica 30 articoli ottimizzati SEO sul tuo sito ogni mese. [Inizia per $1 →](https://app.thestacc.com)

## Fonti

- [Google Search Central: Consolidare URL duplicate](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Moz: Guida al tag URL canonica](https://moz.com/learn/seo/canonicalization)
- [Ahrefs: Tag canonical per SEO](https://ahrefs.com/blog/canonical-tags/)
- [Semrush: Studio sul contenuto duplicato](https://www.semrush.com/blog/duplicate-content/)
- [Google Search Console: Strumento di ispezione URL](https://support.google.com/webmasters/answer/9012289)
