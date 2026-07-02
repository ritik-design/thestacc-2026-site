---
title: "Come Configurare i Redirect 301 (Guida Passo per Passo)"
description: "Scopri come configurare i redirect 301 per la SEO. Copre WordPress, .htaccess, Nginx, Shopify e Cloudflare. Con passaggi di test. Aggiornato marzo 2026."
slug: "301-redirects-guide"
keyword: "redirect 301"
author: "Siddharth Gangal"
date: "2026-04-26"
category: "SEO Tips"
image: "/blogs-preview-images/301-redirects-guide.webp"
---

Hai cambiato un URL. Forse sei migrato su un nuovo dominio. Forse hai consolidato 3 pagine in 1. Ora i visitatori ottengono un errore 404 e Google fa crollare le tue posizioni da un giorno all'altro.

Ogni URL non funzionante fa perdere la link equity che hai guadagnato in mesi di lavoro. Gli utenti rimbalzano. Google segnala il tuo sito come mal gestito. Una singola migrazione senza redirect 301 può azzerare il 40% o più del traffico organico in una settimana.

Questa guida illustra 7 passaggi per configurare correttamente i redirect 301. Imparerai il processo esatto per WordPress, Apache `.htaccess`, Nginx, Shopify e Cloudflare. Nessuna incertezza. Nessun link rotto. Nessuna perdita di posizioni.

Pubblichiamo oltre 3.500 articoli in 70+ settori. Cambi di URL, consolidamenti di pagine e migrazioni di dominio sono operazioni che gestiamo ogni settimana. I passaggi seguenti sono gli stessi che utilizziamo per i nostri siti e per i nostri clienti.

Ecco cosa imparerai:

- Come trovare ogni URL che necessita di un redirect
- Come mappare i vecchi URL verso le corrette nuove destinazioni
- Come implementare i redirect 301 su 5 piattaforme diverse
- Come correggere le catene di redirect e i loop prima che danneggino la velocità
- Come testare i redirect prima e dopo la messa online
- Come monitorare lo stato dei redirect in Google Search Console

---

## Panoramica

- **Tempo necessario:** Da 10 a 30 minuti (dipende dal numero di redirect)
- **Difficoltà:** Principiante - Intermedio
- **Cosa ti serve:** Accesso al tuo CMS, pannello di hosting o file di configurazione del server

---

## Cos'è un Redirect 301?

Il codice di stato `301` comunica ai browser e ai motori di ricerca che una pagina si è spostata definitivamente a un nuovo URL. Il browser reindirizza automaticamente i visitatori al nuovo indirizzo. Google trasferisce la link equity dal vecchio URL al nuovo.

Prima del 2016, i redirect 301 causavano una perdita di PageRank di circa il 15% per ogni hop. Non è più così. [Google ha confermato che i redirect 30x non diluiscono più il PageRank](https://searchengineland.com/google-no-pagerank-dilution-using-301-302-30x-redirects-anymore-254608). Oggi, un `301` correttamente configurato trasmette dal 90 al 99% della link equity, secondo Moz.

Questo rende i redirect 301 lo strumento più importante per preservare la tua SEO durante qualsiasi cambio di URL. Se li salti, riparti da zero.

---

## Passaggio 1: Identifica Quali URL Necessitano di Redirect

Non puoi reindirizzare ciò che non hai trovato. Il primo passo è costruire un elenco completo degli URL che restituiscono errori o sono stati modificati.

Inizia da **Google Search Console**. Vai al report Pagine e filtra per "Non trovato (404)." Questo mostra ogni URL che Google ha tentato di scansionare ma non è riuscito a raggiungere. Esporta l'elenco completo.

Poi controlla **Google Analytics** (GA4). Osserva il report Pagine di destinazione per le pagine che hanno perso traffico improvvisamente. Un calo netto dopo un cambio di URL è un segnale forte che manca un redirect.

Esegui una **scansione del sito** con uno strumento come Screaming Frog, Sitebulb o Ahrefs Site Audit. Questi strumenti trovano link interni rotti, pagine orfane e risposte 404 che Google Search Console potrebbe non rilevare. Un [audit SEO](/blog/how-to-do-seo-audit) completo porta questi problemi in superficie rapidamente.

Tre scenari comuni che richiedono redirect 301:

1. **Cambio di slug URL**. Hai rinominato `/blog/vecchio-articolo` in `/blog/nuovo-articolo`
2. **Migrazione di dominio**. Sei passato da `vecchiosito.com` a `nuovosito.com`
3. **Consolidamento di pagine**. Hai unito 3 pagine deboli in 1 pagina più forte per [correggere i thin content](/blog/fix-thin-content)

### Quando Usare 301 vs 404 vs 410 vs Canonical

Non ogni URL morto necessita di un redirect. Usa questo schema decisionale.

| Scenario | Azione | Perché |
|---|---|---|
| La pagina si è spostata a un nuovo URL | Redirect `301` | Preserva la link equity e l'esperienza utente |
| Pagina eliminata, non esiste sostituto | `410` Gone | Indica a Google di deindexare più velocemente di un `404` |
| Pagina eliminata, potrebbe tornare | `404` Not Found | Risposta standard per pagine temporaneamente mancanti |
| Contenuto duplicato, entrambe le pagine rimangono live | Tag `canonical` | Consolida i segnali senza rimuovere la pagina |
| Vecchio dominio verso nuovo dominio | Redirect `301` (a livello di dominio) | Trasferisce tutta la link equity al nuovo dominio |

![Quando usare redirect 301 vs 404 vs 410 vs canonical](/images/blog/301-redirect-decision-framework.webp)

**Perché questo passaggio è importante:** I redirect mancanti sono invisibili. Gli utenti vedono un 404 e abbandonano. Google vede un URL morto e lo rimuove dall'indice. Perdi posizioni senza alcun avviso nel tuo pannello analytics.

**Consiglio pro:** Esporta la tua sitemap XML completa prima di apportare qualsiasi modifica agli URL. Confrontala con la scansione post-modifica per individuare ogni discrepanza.

---

## Passaggio 2: Mappa i Vecchi URL verso le Nuove Destinazioni

Un redirect è valido solo quanto la sua destinazione. Inviare tutti i vecchi URL alla homepage è un errore comune. Google tratta i redirect verso la homepage da pagine profonde come [soft 404](https://developers.google.com/search/docs/crawling-indexing/301-redirects). Perdi comunque la link equity.

Crea un foglio di calcolo con 4 colonne:

| Vecchio URL | Nuovo URL | Tipo di Redirect | Note |
|---|---|---|---|
| `/blog/vecchia-guida-seo` | `/blog/guida-seo-on-page` | 301 | Contenuto unito |
| `/servizi/web-design` | `/servizi/design` | 301 | Slug abbreviato |
| `/blog/articolo-obsoleto` | , | 410 | Nessun sostituto |

Segui queste regole di mappatura:

- **Punta sempre alla pagina più pertinente.** Abbina argomento e intento, non solo la categoria.
- **Per le migrazioni di dominio, replica la struttura URL.** Se `/chi-siamo` esisteva sul vecchio dominio, reindirizzalo a `/chi-siamo` sul nuovo dominio.
- **Raggruppa i redirect per tipo.** I cambi URL in blocco (come rimuovere `/blog/` dai percorsi) possono usare regole basate su pattern invece di voci individuali.
- **Segnala le pagine con un alto numero di backlink.** Usa Ahrefs o il report Link di Google Search Console per identificare le pagine con più link. Queste hanno la priorità più alta per una mappatura accurata.

Un [audit dei contenuti](/blog/how-to-content-audit) ti aiuta a identificare quali pagine consolidare e quali abbandonare. Eseguilo prima di iniziare la mappatura.

**Perché questo passaggio è importante:** Mappature errate inviano utenti e link equity a pagine irrilevanti. Google nota la discrepanza e potrebbe ignorare completamente il redirect. Una mappatura sbagliata può vanificare mesi di [autorità tematica](/blog/build-topical-authority) che hai costruito attorno a un cluster di keyword.

---

## Passaggio 3: Configura i Redirect 301 sulla Tua Piattaforma

L'implementazione dipende dal tuo stack tecnologico. Di seguito trovi le istruzioni esatte per 5 piattaforme.

### WordPress (Metodo Plugin)

L'opzione più rapida per i siti WordPress. Tre plugin gestiscono bene i redirect:

- **Redirection** (gratuito). Il plugin di redirect più popolare. Supporta regex, registra i 404 e importa file CSV.
- **Rank Math** (gratuito/pro). Gestore di redirect integrato in Rank Math > Reindirizzamenti.
- **Yoast SEO Premium**. Suggerisce automaticamente redirect quando cambi uno slug.

Per aggiungere un redirect in **Redirection**:

1. Vai su Strumenti > Redirection
2. Inserisci l'URL sorgente (vecchio percorso)
3. Inserisci l'URL di destinazione (nuovo percorso)
4. Seleziona "Spostato in modo permanente 301"
5. Clicca "Aggiungi Redirect"

Per i redirect in blocco, usa la funzione di importazione CSV. Formato: `URL sorgente, URL di destinazione, 301`.

### Apache (.htaccess)

Se usi Apache, aggiungi le regole di redirect al file `.htaccess` nella root del sito.

Redirect singolo:

```
Redirect 301 /vecchia-pagina https://esempio.com/nuova-pagina
```

Redirect basato su pattern con `mod_rewrite`:

```
RewriteEngine On
RewriteRule ^vecchia-directory/(.*)$ /nuova-directory/$1 [R=301,L]
```

Redirect a livello di dominio (intero sito):

```
RewriteEngine On
RewriteCond %{HTTP_HOST} ^vecchiosito\.com$ [NC]
RewriteRule ^(.*)$ https://nuovosito.com/$1 [R=301,L]
```

Esegui sempre un backup del file `.htaccess` prima di modificarlo. Un errore di sintassi qui manda offline l'intero sito.

### Nginx

Nginx usa il blocco `server` nel file di configurazione (solitamente `/etc/nginx/sites-available/`).

Redirect singolo:

```
location = /vecchia-pagina {
    return 301 https://esempio.com/nuova-pagina;
}
```

Redirect basato su pattern:

```
location /vecchia-directory/ {
    rewrite ^/vecchia-directory/(.*)$ /nuova-directory/$1 permanent;
}
```

Dopo aver modificato, testa la configurazione con `nginx -t` e ricarica con `systemctl reload nginx`.

### Shopify

Shopify dispone di uno strumento di redirect integrato. Nessun plugin necessario.

1. Vai su **Impostazioni > Navigazione > Reindirizzamenti URL**
2. Clicca "Aggiungi reindirizzamento URL"
3. Inserisci il vecchio percorso e il nuovo percorso
4. Salva

Per i redirect in blocco, clicca "Importa" e carica un CSV con 2 colonne: `Reindirizza da` e `Reindirizza a`.

Limitazione di Shopify: non puoi reindirizzare verso domini esterni con questo strumento. Per le migrazioni di dominio fuori da Shopify, sono necessari redirect a livello DNS.

### Cloudflare (Livello Edge)

I redirect di Cloudflare avvengono a livello CDN. Sono l'opzione più veloce perché il redirect si attiva prima che la richiesta raggiunga il server.

1. Vai su **Regole > Regole di reindirizzamento**
2. Crea una nuova regola
3. Imposta la condizione di corrispondenza (hostname, percorso URI o wildcard)
4. Imposta l'azione su "Reindirizzamento dinamico" o "Reindirizzamento statico"
5. Scegli `301` come codice di stato
6. Distribuisci

Cloudflare supporta pattern con wildcard, il che lo rende ideale per migrazioni di dominio in blocco.

### Confronto tra Piattaforme

| Piattaforma | Difficoltà | Supporto Bulk | Velocità | Ideale per |
|---|---|---|---|---|
| Plugin WordPress | Facile | Importazione CSV | Standard | Blog e siti di contenuto |
| `.htaccess` | Media | Pattern regex | Standard | Hosting condiviso Apache |
| Nginx | Media | Regole di riscrittura | Veloce | VPS e server dedicati |
| Shopify | Facile | Importazione CSV | Standard | Negozi e-commerce |
| Cloudflare | Facile | Regole wildcard | Il più veloce | Qualsiasi sito che usa Cloudflare |

![Configurazione redirect 301 su WordPress, Apache, Nginx, Shopify e Cloudflare](/images/blog/301-redirect-platforms.webp)

**Perché questo passaggio è importante:** Una sintassi errata rompe l'intero sito. Un file `.htaccess` mal configurato restituisce un errore 500. Una regola Nginx sbagliata crea un loop di redirect. Quando possibile, testa in staging prima.

---

## Passaggio 4: Gestisci le Catene di Redirect e i Loop

Una catena di redirect si verifica quando l'URL A reindirizza all'URL B, che reindirizza all'URL C. Invece di 1 hop, il browser ne esegue 2 o più. Ogni hop aggiunge da 50 a 100 millisecondi di latenza.

Un loop di redirect si verifica quando l'URL A reindirizza all'URL B e l'URL B reindirizza di nuovo all'URL A. Il browser rimane bloccato in un ciclo infinito e alla fine mostra una pagina di errore.

Google segue al massimo 5 hop in una catena di redirect. Oltre quel limite, Google smette di seguire. La pagina di destinazione non viene mai scansionata o indicizzata.

### Come Trovare Catene e Loop

Esegui una scansione con Screaming Frog o Ahrefs. Filtra per catene di redirect (3xx > 3xx). Puoi anche usare il [Redirect Checker gratuito di httpstatus.io](https://httpstatus.io) per testare singoli URL.

### Come Appiattire le Catene

Se la catena è A → B → C, aggiorna A in modo che punti direttamente a C. Rimuovi l'hop intermedio.

Prima:
```
/vecchia-pagina → /pagina-rinominata → /pagina-finale
```

Dopo:
```
/vecchia-pagina → /pagina-finale
/pagina-rinominata → /pagina-finale
```

Entrambi i vecchi URL ora puntano direttamente alla destinazione finale. Un hop ciascuno.

### Come Correggere i Loop

I loop si verificano solitamente quando 2 regole di redirect sono in conflitto. Controlla le regole di redirect per riferimenti circolari. La soluzione è sempre la stessa: decidi quale URL è la destinazione canonica e fai in modo che tutti gli altri URL puntino a essa.

Se usi sia redirect a livello di server (`.htaccess`) che redirect a livello di plugin (Redirection), controlla entrambi. Le regole in conflitto tra i livelli sono la causa più comune di loop.

![Confronto tra catena di redirect e redirect diretto](/images/blog/redirect-chain-vs-direct.webp)

**Perché questo passaggio è importante:** Le catene sprecano il budget di crawl e rallentano il caricamento delle pagine. Una catena di 3 hop aggiunge da 150 a 300ms di latenza prima che l'utente veda qualsiasi contenuto. I loop sono peggio. Bloccano completamente l'accesso e consumano il budget di crawl su pagine che non si risolvono mai.

---

> **Salta il lavoro tecnico. Mantieni le posizioni.** Stacc gestisce la struttura URL, i redirect e la manutenzione SEO per 30+ articoli al mese.
> [Inizia a $1 →](/pricing)

---

## Passaggio 5: Testa Ogni Redirect Prima di Andare Live

I redirect non testati causano cali di posizioni silenziosi. Un redirect che restituisce `302` invece di `301` non trasmette la link equity allo stesso modo. Un redirect che punta a un 404 è peggio di nessun redirect.

### Testa con curl

Apri il terminale ed esegui:

```bash
curl -I https://esempio.com/vecchia-pagina
```

Cerca `HTTP/1.1 301 Moved Permanently` e l'intestazione `Location:` che punta al corretto nuovo URL.

Per testare una catena, usa il flag `-L` per seguire tutti i redirect:

```bash
curl -IL https://esempio.com/vecchia-pagina
```

Mostra ogni hop nella catena con il suo codice di stato.

### Testa con Chrome DevTools

1. Apri Chrome e premi `F12` per aprire DevTools
2. Vai alla scheda **Rete**
3. Seleziona "Conserva log" (in modo che i redirect rimangano visibili)
4. Inserisci il vecchio URL nella barra degli indirizzi
5. Osserva la prima richiesta. La colonna Stato dovrebbe mostrare `301`. Le intestazioni della risposta devono mostrare il `Location` corretto.

### Testa con Strumenti Online

I redirect checker gratuiti come [httpstatus.io](https://httpstatus.io) o il [Redirect Checker di Ahrefs](https://ahrefs.com/blog/301-redirects/) ti permettono di testare senza terminale.

### Errori di Test Comuni

- **Discordanza HTTP vs HTTPS.** Testa sia le versioni `http://` che `https://` del vecchio URL. Un redirect mancante su un protocollo lascia una lacuna.
- **Incoerenza della barra finale.** `/vecchia-pagina` e `/vecchia-pagina/` sono URL diversi. Entrambi necessitano di redirect.
- **www vs non-www.** Assicurati che `www.esempio.com/vecchia-pagina` e `esempio.com/vecchia-pagina` reindirizzino correttamente.

![Come testare i redirect 301 con curl e Chrome DevTools](/images/blog/test-301-redirects.webp)

**Perché questo passaggio è importante:** Non puoi vedere un redirect rotto navigando normalmente sul tuo sito. I vecchi URL non sono nella tua navigazione. Solo un test deliberato o un avviso di Google Search Console rileverà il problema. A quel punto, potresti aver già perso settimane di posizioni.

---

## Passaggio 6: Aggiorna i Link Interni verso i Nuovi URL

I redirect sono una rete di sicurezza. Non sono un sostituto permanente per un corretto [collegamento interno](/blog/internal-linking-blog-posts).

Ogni link interno che passa attraverso un redirect aggiunge un hop non necessario. Google segue comunque il link, ma ogni redirect consuma budget di crawl. Su un sito di grandi dimensioni con migliaia di link interni, questo si accumula rapidamente.

### Cosa Aggiornare

- **Link nel corpo del contenuto**. Qualsiasi articolo o pagina che collega al vecchio URL
- **Menu di navigazione**. Link in header, footer, sidebar
- **Sitemap XML**. Rimuovi i vecchi URL e aggiungi quelli nuovi. Se hai bisogno di aiuto, segui la nostra guida su [come creare e ottimizzare la tua sitemap XML](/blog/create-xml-sitemap).
- **Dati strutturati**. Aggiorna qualsiasi [schema markup](/blog/schema-markup-for-blog-posts) che fa riferimento a vecchi URL
- **Tag canonical**. Assicurati che il canonical sulla nuova pagina punti a se stessa, non al vecchio URL

### Come Eseguire un Trova e Sostituisci a Livello di Sito

Per WordPress, usa il plugin **Better Search Replace**. Inserisci il vecchio pattern URL e quello nuovo. Esegui prima una prova a secco per visualizzare l'anteprima delle modifiche. Poi esegui.

Per siti statici o piattaforme CMS personalizzate, usa la funzione trova e sostituisci del tuo editor di codice sull'intera directory del progetto.

Dopo l'aggiornamento, [invia la sitemap aggiornata a Google](/blog/submit-website-google) tramite Search Console per velocizzare la riscansione.

**Perché questo passaggio è importante:** I link interni che passano attraverso redirect sprecano budget di crawl e aggiungono latenza. I link diretti sono sempre più veloci ed efficienti. Pulisci la fonte e mantieni i redirect solo come fallback per i link esterni che non puoi controllare.

---

## Passaggio 7: Monitora in Google Search Console

Il redirect è attivo. I test sono passati. Ma i redirect 301 possono rompersi silenziosamente durante i deployment, gli aggiornamenti del CMS o le modifiche alla configurazione del server. Il monitoraggio continuo individua i problemi prima che influenzino le posizioni.

### Controlla il Report Pagine

In Google Search Console, vai su **Pagine** (sotto Indicizzazione). Filtra per:

- **Non trovato (404)**. Nuovi errori 404 che compaiono dopo che il redirect è andato live indicano una configurazione errata.
- **Errore di reindirizzamento**. Google ha rilevato un loop, una catena o un redirect rotto.
- **Scansionato. Attualmente non indicizzato**. La nuova pagina di destinazione potrebbe non essere ancora indicizzata.

### Usa lo Strumento Ispezione URL

Inserisci il vecchio URL nello strumento Ispezione URL. Google dovrebbe mostrare "La pagina non è nell'indice" con una nota che reindirizza al nuovo URL. Se Google mostra ancora il vecchio URL come indicizzato, richiedi l'indicizzazione per il nuovo URL.

### Controlla i Core Web Vitals

Le catene di redirect aumentano il Time to First Byte (TTFB). Dopo aver implementato i redirect, controlla i **Core Web Vitals** in Search Console per eventuali picchi di latenza. Ogni hop aggiunge da 50 a 100ms. Se il tuo TTFB è aumentato, probabilmente hai una catena non appiattita.

Puoi usarlo anche come parte di una strategia più ampia per [migliorare i Core Web Vitals](/blog/improve-core-web-vitals) sull'intero sito.

### Imposta Punti di Controllo

- **Giorno 7:** Controlla i nuovi errori 404 in GSC. Verifica che i vecchi URL si risolvano correttamente.
- **Giorno 30:** Confronta il traffico organico prima e dopo il redirect. Usa il report Prestazioni filtrato per il nuovo URL.
- **Giorno 90:** Conferma che le posizioni si siano stabilizzate. I siti con redirect 301 puliti mantengono il 95% o più del traffico organico entro 2-3 mesi.

**Perché questo passaggio è importante:** I redirect possono rompersi silenziosamente. Un aggiornamento del CMS potrebbe sovrascrivere il file `.htaccess`. Un aggiornamento del plugin potrebbe reimpostare le regole di redirect. Senza monitoraggio, non lo saprai finché le posizioni non caleranno.

---

## Risultati: Cosa Aspettarsi

Google elabora la maggior parte dei redirect 301 entro 1-2 settimane. Vedrai il vecchio URL scomparire dai risultati di ricerca e il nuovo URL prendere il suo posto.

Le posizioni si stabilizzano tipicamente entro 2-3 mesi dopo una migrazione. [I siti che utilizzano redirect 301 puliti hanno mantenuto il 95% o più del traffico organico](https://ahrefs.com/blog/301-redirects/) durante questo periodo.

Google raccomanda di mantenere i redirect 301 attivi per almeno 1 anno. Rimuoverli troppo presto porta i visitatori di ritorno e i vecchi backlink a un 404.

La timeline completa:

| Traguardo | Tempistica |
|---|---|
| Google inizia a elaborare il redirect | 1-3 giorni |
| Vecchio URL rimosso dall'indice | 1-2 settimane |
| Nuovo URL si posiziona al posto del vecchio | 2-4 settimane |
| Traffico completamente stabilizzato | 2-3 mesi |
| Sicuro rimuovere il redirect | Minimo 1 anno |

![Timeline dell'impatto SEO del redirect 301](/images/blog/301-redirect-timeline.webp)

Abbina redirect puliti a una pubblicazione di contenuti costante per [aumentare il traffico organico](/blog/increase-organic-traffic) mentre i tuoi redirect si assestano.

---

## Risoluzione dei Problemi: 5 Problemi Comuni con i Redirect 301

### Problema 1: Il Redirect Restituisce 302 invece di 301

Un `302` è un redirect temporaneo. Non trasmette la link equity allo stesso modo di un `301`. Questo accade solitamente quando un plugin imposta `302` come predefinito o quando la configurazione del server usa `Redirect` senza specificare il codice di stato.

**Soluzione:** Controlla la regola di redirect. Per `.htaccess`, usa esplicitamente `Redirect 301` o `[R=301,L]`. Nel tuo plugin CMS, verifica che il tipo di redirect sia impostato su "Permanente (301)."

### Problema 2: Catena di Redirect (3+ Hop)

Hai reindirizzato A verso B l'anno scorso. Poi hai reindirizzato B verso C quest'anno. Ora A passa attraverso 2 hop per raggiungere C. Google lo segue, ma la latenza danneggia le prestazioni.

**Soluzione:** Aggiorna la regola per A in modo che punti direttamente a C. Poi aggiorna B in modo che punti direttamente a C. Appiattisci ogni catena a un singolo hop.

### Problema 3: Loop di Redirect

L'URL A reindirizza verso B. L'URL B reindirizza di nuovo verso A. Il browser mostra "ERR_TOO_MANY_REDIRECTS" e non carica nulla.

**Soluzione:** Apri le regole di redirect e cerca riferimenti circolari. Se usi sia un plugin che redirect a livello di server, controlla entrambi i livelli. Rimuovi la regola in conflitto.

### Problema 4: Redirect Misto HTTP e HTTPS

La versione HTTP del vecchio URL reindirizza alla versione HTTP del nuovo URL, che poi reindirizza a HTTPS. È una catena di 2 hop che dovrebbe essere 1 hop.

**Soluzione:** Tutti i redirect dovrebbero puntare direttamente alla versione HTTPS dell'URL di destinazione. Aggiorna ogni regola per usare `https://` nella destinazione.

### Problema 5: Soft 404 Dopo il Redirect

Il redirect funziona. Il codice di stato è `301`. Ma la pagina di destinazione ha contenuto sottile o vuoto. Google lo tratta come un "soft 404" e potrebbe non trasmettere la link equity. Questo accade spesso quando si reindirizza verso una pagina con [thin content](/blog/fix-thin-content) o una pagina di categoria generica.

**Soluzione:** Assicurati che ogni destinazione di redirect sia una pagina reale e sostanziale con contenuto unico. Se la pagina di destinazione non esiste ancora, creala prima di attivare il redirect.

![Problemi comuni con i redirect 301 e relative soluzioni](/images/blog/301-redirect-problems.webp)

---

> **Il tuo team SEO. 99 $ al mese.** 30 articoli ottimizzati, pubblicati e mantenuti. Redirect, link interni e SEO tecnica gestiti.
> [Inizia a $1 →](/pricing)

---

## Domande Frequenti

**Per quanto tempo dovresti mantenere i redirect 301?**

Google raccomanda di mantenere i redirect 301 attivi per almeno 1 anno. I siti esterni che collegano al tuo vecchio URL continueranno a inviare traffico attraverso quel redirect. Rimuoverlo prima che quei link esterni si aggiornino (la maggior parte non lo farà mai) manda i loro visitatori a un 404. In caso di dubbio, mantieni il redirect in modo permanente. Il carico sul server è trascurabile.

**I redirect 301 danneggiano la SEO?**

No. Google ha confermato nel 2016 che i redirect 30x non causano più perdita di PageRank. Un `301` correttamente configurato trasmette dal 90 al 99% della link equity all'URL di destinazione. L'unico rischio sono gli errori di implementazione come catene, loop o redirect verso pagine irrilevanti.

**Qual è la differenza tra un redirect 301 e 302?**

Un [redirect 301](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301) segnala uno spostamento permanente. Google trasferisce la link equity e alla fine deindexizza il vecchio URL. Un `302` segnala uno spostamento temporaneo. Google mantiene il vecchio URL indicizzato e potrebbe non trasferire la piena link equity. Usa `301` per qualsiasi cambio di URL permanente.

**Troppi redirect 301 possono rallentare il mio sito?**

I redirect individuali aggiungono una latenza minima (meno di 100ms). Il problema sono le catene di redirect. Ogni hop aggiunge da 50 a 100ms. Una catena di 3 hop aggiunge da 150 a 300ms prima che la pagina inizi a caricarsi. Mantieni ogni redirect a un singolo hop e l'impatto sulle prestazioni rimane trascurabile.

**Come faccio a verificare se i miei redirect 301 funzionano?**

Usa `curl -I [URL]` nel tuo terminale. La risposta dovrebbe mostrare `HTTP/1.1 301 Moved Permanently` con un'intestazione `Location:` che punta alla destinazione corretta. Puoi anche usare Chrome DevTools (scheda Rete con "Conserva log" abilitato) o strumenti online gratuiti come httpstatus.io.

**Dovrei usare un redirect 301 o un tag canonical?**

Usa un `301` quando stai rimuovendo completamente la vecchia pagina. Usa un tag `canonical` quando entrambe le pagine rimangono live ma vuoi che Google consolidi i segnali di ranking a una versione. Un esempio comune: pagine prodotto con parametri URL. L'URL filtrato rimane accessibile, ma il canonical punta all'URL pulito. Per la [keyword cannibalization](/blog/fix-keyword-cannibalization) tra 2 pagine live, un tag canonical è spesso il miglior primo passo.

---

I redirect 301 proteggono la link equity e le posizioni che hai già guadagnato. Ogni cambio di URL senza un redirect è una perdita nella tua fondamenta SEO.

Configura i redirect correttamente, testali, monitorali e abbina il lavoro a una pubblicazione di contenuti costante. Questo è il modo per [posizionarsi più in alto su Google](/blog/how-to-rank-higher-google) e mantenere le posizioni conquistate.
